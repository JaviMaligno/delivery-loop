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
        code, out = self.run_log("4", "step 1 committed", "evidence/c1.json")
        self.assertEqual(code, 0)
        line = f"- {NOW} · phase 4 · step 1 committed · evidence/c1.json"
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

    def test_owner_creates_skeleton_with_clock_time(self):
        code, _ = self.run_log("--owner", "deliver-abc-1")
        self.assertEqual(code, 0)
        text = self.task.read_text(encoding="utf-8")
        self.assertTrue(text.startswith(f"owner: deliver-abc-1 · since {NOW}\n"))
        for heading in ("## Decisions", "## Escalations", "## Waits", "## Pending cleanup", "## Log"):
            self.assertIn(heading, text)
        self.assertTrue(text.endswith(f"- {NOW} · phase 0 · task file created by deliver-abc-1\n"))

    def test_owner_on_existing_file_is_a_takeover(self):
        self.task.parent.mkdir(parents=True)
        self.task.write_text("owner: old · since 2026-10-20T10:00:00Z\nsize: trivial\n", encoding="utf-8")
        self.run_log("--owner", "new")
        text = self.task.read_text(encoding="utf-8")
        self.assertTrue(text.startswith(f"owner: new · since {NOW}\nsize: trivial\n"))
        self.assertTrue(text.endswith(f"- {NOW} · phase - · owner old → new\n"))

    def test_log_line_needs_phase_and_what(self):
        with self.assertRaises(SystemExit):
            self.run_log("7")

    def test_owner_with_a_log_line_is_rejected_not_half_written(self):
        with self.assertRaises(SystemExit):
            self.run_log("7", "C1 measured", "--owner", "new")
        self.assertFalse(self.task.exists())

    def test_first_line_of_phase_6_or_7_needs_its_saved_merge(self):
        self.run_log("--owner", "s")
        with self.assertRaises(SystemExit):
            self.run_log("6", "phase 6 loaded")
        self.assertNotIn("phase 6 ·", self.task.read_text(encoding="utf-8"))
        (self.task.parent / "merge-6.md").write_text("merged-at: x\n", encoding="utf-8")
        code, _ = self.run_log("6", "phase 6 loaded")
        self.assertEqual(code, 0)
        code, _ = self.run_log("6", "PR opened")
        self.assertEqual(code, 0)

    def test_other_phases_need_no_saved_merge(self):
        code, _ = self.run_log("4", "step 1 committed")
        self.assertEqual(code, 0)

    def test_default_clock_is_utc_iso(self):
        self.assertRegex(tl.utc_now(), r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


if __name__ == "__main__":
    unittest.main()
