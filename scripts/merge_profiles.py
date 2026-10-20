"""Discover, parse and merge layered delivery profiles.

Levels, far to near: L0 the plugin defaults (profile/defaults.md), the user file
(~/.claude/delivery/profile.md), then every .delivery/profile.md from the
filesystem root down to the working directory, then the local repo profile
(<git common dir>/delivery/profile.md: never committed, shared by worktrees).
Fields: nearest level wins unless locked with [invariant]. Rules: by id within
a section; nearest wins unless an invariant with that id exists in any section.
Grammar: profile/schema.md.
Exit: 0 merged · 1 malformed or unreadable · 3 nothing beyond L0 · 4 inside a git
repo without a repo-level profile.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

SECTION_RE = re.compile(r"^##\s+(.+?)\s*$")
FIELD_RE = re.compile(r"^-\s+([a-z0-9][a-z0-9-]*):\s+(.*?)\s*$")
RULE_RE = re.compile(r"^-\s+\[(invariant\s+)?([a-z0-9][a-z0-9-]*)\]\s+(.+?)\s*$", re.IGNORECASE)
LOCK_RE = re.compile(r"\s*\[invariant\]$", re.IGNORECASE)
FENCE = "```"
RULES_MARK = "Rules:"
SOURCE_PREFIX = "Source:"
RESERVED_SECTIONS = {"conflicts", "skipped"}
DEFAULTS = Path(__file__).resolve().parent.parent / "profile" / "defaults.md"
USER_FILE = Path(".claude") / "delivery" / "profile.md"
LEVEL_FILE = Path(".delivery") / "profile.md"
LOCAL_REPO_FILE = Path("delivery") / "profile.md"


class ProfileError(Exception):
    pass


@dataclass
class Rule:
    id: str
    invariant: bool
    text: str


@dataclass
class Section:
    fields: dict[str, str] = field(default_factory=dict)
    locked: set[str] = field(default_factory=set)
    rules: list[Rule] = field(default_factory=list)
    source: str | None = None


@dataclass
class MergedSection:
    fields: dict[str, tuple[str, str]] = field(default_factory=dict)
    locked: set[str] = field(default_factory=set)
    rules: list[tuple[Rule, str]] = field(default_factory=list)
    source: tuple[str, str] | None = None


@dataclass
class Merged:
    sections: dict[str, MergedSection] = field(default_factory=dict)
    conflicts: list[str] = field(default_factory=list)


@dataclass
class Discovery:
    paths: list[Path]
    skipped: list[Path]
    repo_root: Path | None
    repo_level: bool


def parse(text: str, path: str) -> dict[str, Section]:
    sections: dict[str, Section] = {}
    current: Section | None = None
    in_rules = False
    in_fence = False
    for lineno, raw in enumerate(text.lstrip("﻿").splitlines(), start=1):
        line = raw.strip()
        if line.startswith(FENCE):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        where = f"{path}:{lineno}"
        heading = SECTION_RE.match(line)
        if heading:
            name = heading.group(1).strip().lower()
            if name in RESERVED_SECTIONS:
                raise ProfileError(f"{where}: section name '{name}' is reserved")
            current = sections.setdefault(name, Section())
            in_rules = False
            continue
        if current is None:
            continue
        if line == RULES_MARK:
            in_rules = True
            continue
        if line.startswith(SOURCE_PREFIX):
            current.source = line[len(SOURCE_PREFIX):].strip()
            continue
        if not line.startswith("- "):
            continue
        if in_rules:
            _parse_rule(current, line, where)
        else:
            _parse_field(current, line, where)
    return sections


def _parse_rule(section: Section, line: str, where: str) -> None:
    match = RULE_RE.match(line)
    if not match:
        raise ProfileError(f"{where}: rule needs an id: '- [id] text' or '- [invariant id] text'")
    rule = Rule(match.group(2).lower(), bool(match.group(1)), match.group(3))
    if any(r.id == rule.id for r in section.rules):
        raise ProfileError(f"{where}: duplicate rule id '{rule.id}'")
    section.rules.append(rule)


def _parse_field(section: Section, line: str, where: str) -> None:
    match = FIELD_RE.match(line)
    if not match or not match.group(2):
        raise ProfileError(f"{where}: field needs the form '- key: value' (non-empty value)")
    key, value = match.group(1), match.group(2)
    if key in section.fields:
        raise ProfileError(f"{where}: duplicate key '{key}'")
    locked = LOCK_RE.search(value)
    if locked:
        value = value[: locked.start()]
        section.locked.add(key)
    section.fields[key] = value


def merge(levels: list[tuple[str, dict[str, Section]]]) -> Merged:
    merged = Merged()
    for label, profile in levels:
        for name, section in profile.items():
            target = merged.sections.setdefault(name, MergedSection())
            for key, value in section.fields.items():
                _merge_field(merged, name, target, key, value, key in section.locked, label)
            if section.source is not None:
                target.source = (section.source, label)
            for rule in section.rules:
                _merge_rule(merged, name, target, rule, label)
    return merged


def _merge_field(merged: Merged, name: str, target: MergedSection, key: str, value: str,
                 locked: bool, label: str) -> None:
    if key in target.locked:
        if target.fields[key][0] != value:
            merged.conflicts.append(_conflict(f"{name}/{key}", target.fields[key][1], label))
        return
    target.fields[key] = (value, label)
    if locked:
        target.locked.add(key)


def _find_invariant(merged: Merged, rule_id: str) -> tuple[str, Rule, str] | None:
    for name, section in merged.sections.items():
        for existing, existing_label in section.rules:
            if existing.id == rule_id and existing.invariant:
                return name, existing, existing_label
    return None


def _merge_rule(merged: Merged, name: str, target: MergedSection, rule: Rule, label: str) -> None:
    invariant = _find_invariant(merged, rule.id)
    if invariant:
        inv_section, existing, existing_label = invariant
        if existing.text != rule.text or inv_section != name:
            merged.conflicts.append(_conflict(f"{name}/{rule.id}", existing_label, label,
                                              f"{inv_section}/{rule.id}"))
        return
    for index, (existing, _) in enumerate(target.rules):
        if existing.id == rule.id:
            target.rules[index] = (rule, label)
            return
    target.rules.append((rule, label))


def _conflict(item: str, kept: str, rejected: str, invariant: str | None = None) -> str:
    where = f" ({invariant})" if invariant and invariant != item else ""
    return f"{item}: invariant from {kept}{where} kept; {rejected} tried to change it"


def dedupe(paths: list[Path], normcase: Callable[[str], str] = os.path.normcase) -> list[Path]:
    seen: set[str] = set()
    out: list[Path] = []
    for path in paths:
        key = normcase(str(path))
        if key not in seen:
            seen.add(key)
            out.append(path)
    return out


def _same(a: Path, b: Path) -> bool:
    return os.path.normcase(str(a)) == os.path.normcase(str(b))


def _git_toplevel(cwd: Path) -> Path | None:
    for directory in [cwd, *cwd.parents]:
        if (directory / ".git").exists():
            return directory
    return None


def _git_common_dir(toplevel: Path) -> Path | None:
    dot_git = toplevel / ".git"
    if dot_git.is_dir():
        return dot_git
    if not dot_git.is_file():
        return None
    line = dot_git.read_text(encoding="utf-8").strip()
    if not line.startswith("gitdir:"):
        return None
    gitdir = Path(line[len("gitdir:"):].strip())
    if not gitdir.is_absolute():
        gitdir = toplevel / gitdir
    commondir = gitdir / "commondir"
    if commondir.is_file():
        return (gitdir / commondir.read_text(encoding="utf-8").strip()).resolve()
    return gitdir.resolve()


def discover(cwd: Path, home: Path) -> Discovery:
    cwd, home = cwd.resolve(), home.resolve()
    found: list[Path] = []
    skipped: list[Path] = []
    user = home / USER_FILE
    if user.is_file():
        found.append(user)
    toplevel = _git_toplevel(cwd)
    above_repo = set(toplevel.parents) if toplevel else set()
    for directory in [*reversed(cwd.parents), cwd]:
        candidate = directory / LEVEL_FILE
        if not candidate.is_file():
            continue
        if _same(directory, home):
            raise ProfileError(f"{candidate}: not a valid level; use {(home / USER_FILE).as_posix()}")
        if directory in above_repo and (directory / ".git").exists():
            skipped.append(candidate)
            continue
        found.append(candidate)
    repo_level = bool(toplevel) and (toplevel / LEVEL_FILE).is_file()
    common = _git_common_dir(toplevel) if toplevel else None
    local = common / LOCAL_REPO_FILE if common else None
    if local and local.is_file():
        found.append(local.resolve())
        repo_level = True
    return Discovery(dedupe(found), skipped, toplevel, repo_level)


def collect(cwd: Path, home: Path, defaults: Path = DEFAULTS) -> list[Path]:
    return dedupe([defaults.resolve(), *discover(cwd, home).paths])


def _tag(label: str) -> str:
    return f" ← {label}"


def render(merged: Merged, levels: list[tuple[str, str]], skipped: list[str] | None = None,
           repo_level: str | None = None) -> str:
    out = ["# Merged delivery profile", "", "Levels (far → near):"]
    out += [f"- {label}: {path}" for label, path in levels]
    if repo_level is not None:
        out.append(f"repo level: {repo_level}")
    for name, section in merged.sections.items():
        out += ["", f"## {name}"]
        for key, (value, label) in section.fields.items():
            lock = " [invariant]" if key in section.locked else ""
            out.append(f"- {key}: {value}{lock}{_tag(label)}")
        if section.rules:
            out.append(RULES_MARK)
            for rule, label in section.rules:
                tag = f"invariant {rule.id}" if rule.invariant else rule.id
                out.append(f"- [{tag}] {rule.text}{_tag(label)}")
        if section.source:
            out.append(f"{SOURCE_PREFIX} {section.source[0]}{_tag(section.source[1])}")
    if merged.conflicts:
        out += ["", "## Conflicts"]
        out += [f"- {c}" for c in merged.conflicts]
    if skipped:
        out += ["", "## Skipped", "git roots above the repo (nested worktree or cloned profile repo):"]
        out += [f"- {s}" for s in skipped]
    return "\n".join(out) + "\n"


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError) as error:
        raise ProfileError(f"{path}: cannot read ({error})") from error


def main(argv: list[str] | None = None, emit: Callable[[str], None] = print,
         emit_err: Callable[[str], None] | None = None) -> int:
    emit_err = emit_err or (lambda msg: print(msg, file=sys.stderr))
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--cwd", type=Path, default=Path.cwd())
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument("--defaults", type=Path, default=DEFAULTS)
    args = parser.parse_args(argv)
    try:
        found = discover(args.cwd, args.home)
        paths = dedupe([args.defaults.resolve(), *found.paths])
        levels = [(f"L{i}", parse(_read(p), str(p))) for i, p in enumerate(paths)]
    except ProfileError as error:
        emit_err(f"error: {error}")
        return 1
    repo_state = None
    if found.repo_root is not None:
        repo_state = str(found.repo_root / LEVEL_FILE) if found.repo_level else "none"
    emit(render(merge(levels), [(label, str(p)) for (label, _), p in zip(levels, paths)],
                [str(s) for s in found.skipped], repo_state))
    if len(paths) == 1:
        return 3
    if found.repo_root is not None and not found.repo_level:
        return 4
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
