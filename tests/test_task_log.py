import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import task_log as tl  # noqa: E402

NOW = "2026-10-21T13:09:00Z"


class TaskLogTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.task = Path(self.tmp.name) / "tasks" / "abc-1" / "task.md"

    def tearDown(self):
        self.tmp.cleanup()

    def run_log(self, *args: str) -> tuple[int, list[str]]:
        out: list[str] = []
        code = tl.main([str(self.task), *args], out.append, lambda _: None, now=lambda: NOW)
        return code, out

    def test_appends_line_with_clock_time(self):
        self.task.parent.mkdir(parents=True)
        self.task.write_text("owner: s\n", encoding="utf-8")
        code, out = self.run_log("7", "C1 measured", "evidence/c1.json")
        self.assertEqual(code, 0)
        line = f"- {NOW} · phase 7 · C1 measured · evidence/c1.json"
        self.assertEqual(self.task.read_text(encoding="utf-8"), f"owner: s\n{line}\n")
        self.assertEqual(out, [line])

    def test_evidence_is_optional_and_missing_newline_is_added(self):
        self.task.parent.mkdir(parents=True)
        self.task.write_text("owner: s", encoding="utf-8")
        self.run_log("0", "phase 0 loaded")
        self.assertEqual(self.task.read_text(encoding="utf-8"),
                         f"owner: s\n- {NOW} · phase 0 · phase 0 loaded\n")

    def test_creates_task_file_and_dirs(self):
        self.run_log("0", "start")
        self.assertTrue(self.task.is_file())

    def test_default_clock_is_utc_iso(self):
        self.assertRegex(tl.utc_now(), r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


if __name__ == "__main__":
    unittest.main()
