"""Fail if the plugin core names a concrete tool, company or client.

Scans every text file in the repo except docs/, tests/, .git/, .github/, evals/results/ and the denylist (agnostic-ok)
files. examples/ is checked only against extra --denylist terms (it may name
tools, never a real org). URLs and lines containing `agnostic-ok` are ignored.
Terms: scripts/agnostic-denylist.txt (public: tool names) plus every extra
--denylist file (private: company and client names). Exit 1 on findings.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Callable

EXEMPT_DIRS = {"docs", "tests", ".git", ".github", "__pycache__"}  # agnostic-ok
TOOLS_ALLOWED_DIRS = {"examples"}
GENERATED_DIR = ("evals", "results")
TEXT_SUFFIXES = {".md", ".py", ".json", ".txt", ".yml", ".yaml", ".toml", ".sh", ".js", ".mjs", ".ts"}
ALLOW_MARK = "agnostic-ok"
URL_RE = re.compile(r"https?://\S+")
PUBLIC_DENYLIST = Path(__file__).resolve().parent / "agnostic-denylist.txt"


def load_terms(paths: list[Path]) -> list[str]:
    terms: list[str] = []
    for path in paths:
        for line in path.read_text(encoding="utf-8").splitlines():
            term = line.strip().lower()
            if term and not term.startswith("#") and term not in terms:
                terms.append(term)
    return terms


def _compile(terms: list[str]) -> list[tuple[str, re.Pattern[str]]]:
    return [(t, re.compile(rf"(?<![\w-]){re.escape(t)}(?![\w-])", re.IGNORECASE)) for t in terms]


def scanned_files(root: Path, exempt: set[Path]) -> list[Path]:
    files = []
    for path in root.rglob("*"):
        rel = path.relative_to(root)
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES or path.resolve() in exempt:
            continue
        if EXEMPT_DIRS & set(rel.parts[:-1]) or rel.parts[:2] == GENERATED_DIR:
            continue
        files.append(path)
    return sorted(files, key=lambda p: p.relative_to(root).as_posix())


def check(root: Path, denylists: list[Path], public: Path | None = None) -> list[str]:
    """`public` = the denylist whose terms are allowed under examples/ (default: first file)."""
    public = public or (denylists[0] if denylists else None)
    all_terms = _compile(load_terms(denylists))
    extra_terms = _compile(load_terms([d for d in denylists if d != public]))
    exempt = {p.resolve() for p in denylists}
    findings: list[str] = []
    for path in scanned_files(root, exempt):
        rel = path.relative_to(root)
        patterns = extra_terms if rel.parts[0] in TOOLS_ALLOWED_DIRS else all_terms
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if ALLOW_MARK in line:
                continue
            line = URL_RE.sub("", line)
            findings += [f"{rel.as_posix()}:{lineno}: {term}" for term, pattern in patterns if pattern.search(line)]
    return findings


def main(argv: list[str] | None = None, emit: Callable[[str], None] = print) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--public", type=Path, default=PUBLIC_DENYLIST)
    parser.add_argument("--denylist", type=Path, action="append", default=[],
                        help="extra denylist file (repeatable)")
    args = parser.parse_args(argv)
    denylists = [args.public, *args.denylist] if args.public.is_file() else args.denylist
    findings = check(args.root, denylists, args.public)
    for finding in findings:
        emit(finding)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
