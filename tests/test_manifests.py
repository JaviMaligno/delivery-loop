import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


class ManifestsTest(unittest.TestCase):
    """One plugin, two harnesses: the manifests must not drift apart."""

    def test_versions_and_names_match_across_harnesses(self):
        claude = load(".claude-plugin/plugin.json")
        codex = load(".codex-plugin/plugin.json")
        listed = load(".claude-plugin/marketplace.json")["plugins"][0]
        self.assertEqual(claude["name"], codex["name"])
        self.assertEqual({claude["version"], codex["version"], listed["version"]}, {claude["version"]})

    def test_codex_manifest_points_at_the_shared_skills(self):
        self.assertEqual(load(".codex-plugin/plugin.json")["skills"], "./skills/")
        entry = load(".agents/plugins/marketplace.json")["plugins"][0]
        self.assertEqual((entry["name"], entry["source"]["path"]), ("delivery-loop", "./"))


if __name__ == "__main__":
    unittest.main()
