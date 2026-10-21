"""Append one timed line to a task file's phase log.

The time comes from the clock, never from the caller: a time typed from memory was wrong
in live runs even with an instruction to use `date -u`.
Line: `- <UTC> · phase <n> · <what>[ · <evidence>]`. Creates the file and its dirs if missing.
Exit: 0 written · 1 unwritable.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main(argv: list[str] | None = None, emit: Callable[[str], None] = print,
         emit_err: Callable[[str], None] | None = None, now: Callable[[], str] = utc_now) -> int:
    emit_err = emit_err or (lambda msg: print(msg, file=sys.stderr))
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("task", type=Path)
    parser.add_argument("phase")
    parser.add_argument("what")
    parser.add_argument("evidence", nargs="?")
    args = parser.parse_args(argv)
    parts = [now(), f"phase {args.phase}", args.what] + ([args.evidence] if args.evidence else [])
    line = "- " + " · ".join(parts)
    try:
        args.task.parent.mkdir(parents=True, exist_ok=True)
        text = args.task.read_text(encoding="utf-8") if args.task.is_file() else ""
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
