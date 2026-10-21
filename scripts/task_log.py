"""Write a task file's timed lines: its creation, owner changes and phase log.

Every time comes from the clock, never from the caller: a time typed from memory was wrong
in live runs even with an instruction to use `date -u`.
- `task_log.py <task.md> --owner <session>`: creates the task file with its skeleton, or, if it
  exists, takes it over (rewrites the `owner:` line, logs the change).
- `task_log.py <task.md> <phase> <what> [<evidence>]`: appends `- <UTC> · phase <n> · <what>[ · <evidence>]`.
Exit: 0 written · 1 unwritable · 2 bad arguments.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

SECTIONS = ["## Decisions", "## Escalations", "## Waits", "## Pending cleanup", "## Log"]
OWNER_PREFIX = "owner: "
REMERGE_PHASES = {"6", "7"}  # their first log line needs the saved re-merge (runs skipped it twice)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


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


def main(argv: list[str] | None = None, emit: Callable[[str], None] = print,
         emit_err: Callable[[str], None] | None = None, now: Callable[[], str] = utc_now) -> int:
    emit_err = emit_err or (lambda msg: print(msg, file=sys.stderr))
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("task", type=Path)
    parser.add_argument("phase", nargs="?")
    parser.add_argument("what", nargs="?")
    parser.add_argument("evidence", nargs="?")
    parser.add_argument("--owner")
    args = parser.parse_args(argv)
    if bool(args.owner) == bool(args.phase or args.what or args.evidence) or (not args.owner and not args.what):
        parser.error("give either --owner <session>, or <phase> <what> [<evidence>]; not both")
    if args.phase in REMERGE_PHASES and not args.owner:
        logged = args.task.read_text(encoding="utf-8") if args.task.is_file() else ""
        merge_file = args.task.parent / f"merge-{args.phase}.md"
        started = any(line.startswith("- ") and f" · phase {args.phase} · " in line for line in logged.splitlines())
        if not started and not merge_file.is_file():
            parser.error(f"phase {args.phase} starts with the re-merge: save it first with "
                         f"merge_profiles.py --out {merge_file} (deliver Start 5)")
    when = now()
    try:
        args.task.parent.mkdir(parents=True, exist_ok=True)
        text = args.task.read_text(encoding="utf-8") if args.task.is_file() else ""
        if args.owner:
            text, line = _with_owner(text, args.owner, when)
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
