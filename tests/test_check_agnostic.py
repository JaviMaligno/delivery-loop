import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import check_agnostic as ca  # noqa: E402


class CheckAgnosticTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "repo"
        self.denylist = self.write("scripts/agnostic-denylist.txt", "# tools\nacme-tracker\nwidgetci\n")
        self.extra = self.write("../private.txt", "secretclient\n")

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, rel: str, text: str) -> Path:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def check(self, extra: bool = False) -> list[str]:
        lists = [self.denylist, self.extra] if extra else [self.denylist]
        return ca.check(self.root, lists, self.denylist)

    def test_term_in_skills_is_reported_with_location(self):
        self.write("skills/x/SKILL.md", "line one\nOpen the Acme-Tracker issue.\n")
        self.assertEqual(self.check(), ["skills/x/SKILL.md:2: acme-tracker"])

    def test_marked_line_is_allowed(self):
        self.write("profile/schema.md", "| tracker | acme-tracker <!-- agnostic-ok --> |\n")
        self.assertEqual(self.check(), [])

    def test_docs_and_tests_are_exempt(self):
        self.write("docs/spec.md", "acme-tracker secretclient\n")
        self.write("tests/t.py", "acme-tracker secretclient\n")
        self.assertEqual(self.check(extra=True), [])

    def test_examples_allow_tools_but_not_private_terms(self):
        self.write("examples/org/profile.md", "kind: acme-tracker\nfor SecretClient\n")
        self.assertEqual(self.check(extra=True), ["examples/org/profile.md:2: secretclient"])

    def test_every_core_text_file_is_scanned(self):
        self.write("README.md", "Works with WidgetCI.\n")
        self.write(".claude-plugin/plugin.json", '{"description": "for widgetci"}\n')
        self.write("hooks/guard.sh", "# widgetci\n")
        self.assertEqual(self.check(), [".claude-plugin/plugin.json:1: widgetci",
                                        "README.md:1: widgetci", "hooks/guard.sh:1: widgetci"])

    def test_eval_results_are_exempt_but_eval_cases_are_scanned(self):
        self.write("evals/results/run.json", '{"v": "widgetci"}\n')
        self.write("evals/case/prompt.md", "use widgetci\n")
        self.assertEqual(self.check(), ["evals/case/prompt.md:1: widgetci"])

    def test_urls_are_ignored(self):
        self.write(".claude-plugin/plugin.json", '{"repository": "https://widgetci.example/x"}\n')
        self.assertEqual(self.check(), [])

    def test_denylist_file_itself_is_exempt(self):
        self.assertEqual(self.check(), [])

    def test_extra_denylist_terms_are_reported(self):
        self.write("skills/x.md", "Built for SecretClient.\n")
        self.assertEqual(self.check(extra=True), ["skills/x.md:1: secretclient"])

    def test_word_boundary(self):
        self.write("skills/x.md", "widgetcis and prewidgetci are not the term\n")
        self.assertEqual(self.check(), [])

    def test_main_exit_codes(self):
        args = ["--root", str(self.root), "--public", str(self.denylist)]
        self.assertEqual(ca.main(args, lambda _: None), 0)
        self.write("skills/x.md", "widgetci\n")
        self.assertEqual(ca.main(args, lambda _: None), 1)

    def test_repo_core_is_agnostic(self):
        self.assertEqual(ca.check(ROOT, [ca.PUBLIC_DENYLIST], ca.PUBLIC_DENYLIST), [])


if __name__ == "__main__":
    unittest.main()
