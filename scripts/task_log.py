"""Write a task file's timed lines: its creation, owner changes, phase log and section notes.

Every time comes from the clock, never from the caller: a time typed from memory was wrong
in live runs even with an instruction to use `date -u`.
- `task_log.py <task.md> --owner <session>`: creates the task file with its skeleton, or, if it
  exists, takes it over (rewrites the `owner:` line, logs the change). <session> is the session's
  addressable name (what others message), not a description.
- `task_log.py <task.md> <phase> <what> [<evidence>]`: appends `- <UTC> · phase <n> · <what>[ · <evidence>]`.
  The first line of phase 6 or 7 since the last owner change needs `merge-<n>.md` saved after that change.
- `task_log.py <task.md> --note <section> <text>`: appends `- <UTC> · <text>` to `## <section>`
  (closing a wait or an escalation, a pending cleanup line); creates the section before `## Log` if missing.
Exit: 0 written · 1 unwritable · 2 bad arguments.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

SECTIONS = ["## Decisions", "## Escalations", "## Waits", "## Pending cleanup", "## Log"]
OWNER_PREFIX = "owner: "
OWNER_RE = re.compile(r"[\w.-]+")
OWNER_EVENTS = (" · task file created by ", " · owner ")
REMERGE_PHASES = {"6", "7"}  # their first log line needs the saved re-merge (runs skipped it twice)
TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime(TIME_FORMAT)


def log_line(when: str, phase: str, what: str, evidence: str | None = None) -> str:
    return "- " + " · ".join([when, f"phase {phase}", what] + ([evidence] if evidence else []))


def _with_owner(text: str, owner: str, when: str) -> tuple[str, str]:
    """New text with the owner line set, and a log line naming the change."""
    header = f"{OWNER_PREFIX}{owner} · since {when}"
    if not text:
        body = "\n".join([header, "", *[f"{s}\n" for s in SECTIONS]])
        return body.rstrip("\n") + "\n", log_line(when, "0", f"task file created by {owner}")
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(OWNER_PREFIX):
            previous = line[len(OWNER_PREFIX):].split(" · ")[0]
            lines[index] = header
            return "\n".join(lines) + "\n", log_line(when, "-", f"owner {previous} → {owner}")
    return "\n".join([header, *lines]) + "\n", log_line(when, "-", f"owner set to {owner}")


def _with_note(text: str, section: str, line: str) -> str:
    """Text with `line` appended at the end of `## <section>`, created before `## Log` if missing."""
    lines = text.splitlines()
    heading = f"## {section}"
    if heading not in lines:
        at = lines.index("## Log") if "## Log" in lines else len(lines)
        lines[at:at] = [heading, line, ""]
        return "\n".join(lines) + "\n"
    end = lines.index(heading) + 1
    while end < len(lines) and not lines[end].startswith("## "):
        end += 1
    while end > lines.index(heading) + 1 and not lines[end - 1].strip():
        end -= 1
    lines.insert(end, line)
    return "\n".join(lines) + "\n"


def _remerge_missing(task: Path, phase: str) -> Path | None:
    """The merge file phase `phase` still needs, or None. Counts only what happened since the last owner change."""
    lines = task.read_text(encoding="utf-8").splitlines() if task.is_file() else []
    log = [line for line in lines if line.startswith("- ")]
    owner_at = max((i for i, line in enumerate(log) if any(e in line for e in OWNER_EVENTS)), default=-1)
    if any(f" · phase {phase} · " in line for line in log[owner_at + 1:]):
        return None
    merge_file = task.parent / f"merge-{phase}.md"
    if not merge_file.is_file():
        return merge_file
    if owner_at >= 0:
        try:
            changed = datetime.strptime(log[owner_at][2:22], TIME_FORMAT).replace(tzinfo=timezone.utc)
        except ValueError:  # a hand-typed line from an older task file: its time cannot be trusted
            return None
        if datetime.fromtimestamp(merge_file.stat().st_mtime, timezone.utc) < changed:
            return merge_file
    return None


def main(argv: list[str] | None = None, emit: Callable[[str], None] = print,
         emit_err: Callable[[str], None] | None = None, now: Callable[[], str] = utc_now) -> int:
    emit_err = emit_err or (lambda msg: print(msg, file=sys.stderr))
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("task", type=Path)
    parser.add_argument("phase", nargs="?")
    parser.add_argument("what", nargs="?")
    parser.add_argument("evidence", nargs="?")
    parser.add_argument("--owner")
    parser.add_argument("--note", nargs=2, metavar=("SECTION", "TEXT"))
    args = parser.parse_args(argv)
    modes = [bool(args.owner), bool(args.note), bool(args.phase or args.what or args.evidence)]
    if sum(modes) != 1 or (modes[2] and not args.what):
        parser.error("give one of: --owner <session> · --note <section> <text> · <phase> <what> [<evidence>]")
    if args.owner and not OWNER_RE.fullmatch(args.owner):
        parser.error("--owner takes the session's addressable name (letters, digits, - _ .), not a description")
    if args.phase in REMERGE_PHASES:
        missing = _remerge_missing(args.task, args.phase)
        if missing:
            parser.error(f"phase {args.phase} starts with the re-merge: save it with "
                         f"merge_profiles.py --out {missing} (deliver Start 5); after an owner change, again")
    when = now()
    try:
        args.task.parent.mkdir(parents=True, exist_ok=True)
        text = args.task.read_text(encoding="utf-8") if args.task.is_file() else ""
        if args.owner:
            text, line = _with_owner(text, args.owner, when)
        elif args.note:
            line = f"- {when} · {args.note[1]}"
            args.task.write_bytes(_with_note(text, args.note[0], line).encode("utf-8"))
            emit(line)
            return 0
        else:
            line = log_line(when, args.phase, args.what, args.evidence)
        if text and not text.endswith("\n"):
            text += "\n"
        args.task.write_bytes((text + line + "\n").encode("utf-8"))
    except OSError as error:
        emit_err(f"error: {args.task}: {error}")
        return 1
    emit(line)
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
