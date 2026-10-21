import ntpath
import shutil
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import merge_profiles as mp  # noqa: E402

FIXTURES = ROOT / "tests" / "fixtures" / "levels"

ORG = """\
# Org profile

## deploy
- via: pipeline
- served-sha-check: required
Rules:
- [invariant no-prod-testing] Never test or write against production.
- [cli-deploy] CLI deploys allowed in emergencies.
Source: org handbook · checked 2026-10-01

## reviewers
- 1-human: code owner · weight approves
Rules:
- [two-reviewers] Two approvals before merge.
"""

REPO = """\
## deploy
- via: git-integration
Rules:
- [no-prod-testing] Production smoke tests are fine.
- [cli-deploy] Never deploy from the CLI.
Source: deploy config · checked 2026-10-20

## environments
- dev: https://dev.example.test (staging)
"""

EMPTY_DEFAULTS = "# defaults\n"


def write(root: Path, rel: str, text: str) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text), encoding="utf-8")
    return path


def merged_of(*texts: str) -> mp.Merged:
    return mp.merge([(f"L{i}", mp.parse(t, f"f{i}.md")) for i, t in enumerate(texts)])


class ParseTest(unittest.TestCase):
    def test_sections_fields_rules_source(self):
        profile = mp.parse(ORG, "org.md")
        deploy = profile["deploy"]
        self.assertEqual(deploy.fields, {"via": "pipeline", "served-sha-check": "required"})
        self.assertEqual([(r.id, r.invariant) for r in deploy.rules],
                         [("no-prod-testing", True), ("cli-deploy", False)])
        self.assertEqual(deploy.rules[0].text, "Never test or write against production.")
        self.assertEqual(deploy.source, "org handbook · checked 2026-10-01")

    def test_field_value_splits_on_first_colon_space(self):
        profile = mp.parse("## environments\n- dev: https://dev.test:8080 · branch staging\n", "p.md")
        self.assertEqual(profile["environments"].fields["dev"], "https://dev.test:8080 · branch staging")

    def test_invariant_field_suffix_locks_field_case_insensitive(self):
        section = mp.parse("## environments\n- production-env: prod [Invariant]\n", "p.md")["environments"]
        self.assertEqual(section.fields["production-env"], "prod")
        self.assertEqual(section.locked, {"production-env"})

    def test_bom_does_not_drop_first_section(self):
        section = mp.parse("\ufeff## environments\nRules:\n- [invariant x] Keep.\n", "p.md")["environments"]
        self.assertTrue(section.rules[0].invariant)

    def test_crlf_and_heading_trailing_spaces(self):
        profile = mp.parse("## ci   \r\n- provider: x\r\n", "p.md")
        self.assertEqual(profile["ci"].fields, {"provider": "x"})

    def test_fenced_blocks_are_ignored(self):
        profile = mp.parse("## ci\n```markdown\n## deploy\n- via: x\n```\n- provider: y\n", "p.md")
        self.assertEqual(set(profile), {"ci"})
        self.assertEqual(profile["ci"].fields, {"provider": "y"})

    def test_rule_without_id_is_an_error_with_location(self):
        with self.assertRaises(mp.ProfileError) as ctx:
            mp.parse("## deploy\nRules:\n- Never deploy on Fridays.\n", "repo.md")
        self.assertIn("repo.md:3", str(ctx.exception))

    def test_field_bullet_without_key_is_an_error_with_location(self):
        with self.assertRaises(mp.ProfileError) as ctx:
            mp.parse("## deploy\n- staging goes to dev\n", "repo.md")
        self.assertIn("repo.md:2", str(ctx.exception))

    def test_empty_value_is_an_error(self):
        with self.assertRaises(mp.ProfileError):
            mp.parse("## deploy\n- via:\n", "repo.md")

    def test_duplicate_key_in_one_file_is_an_error(self):
        with self.assertRaises(mp.ProfileError) as ctx:
            mp.parse("## deploy\n- via: a\n- via: b\n", "repo.md")
        self.assertIn("repo.md:3", str(ctx.exception))

    def test_duplicate_rule_id_in_one_file_is_an_error(self):
        with self.assertRaises(mp.ProfileError) as ctx:
            mp.parse("## deploy\nRules:\n- [x] one\n- [x] two\n", "repo.md")
        self.assertIn("repo.md:4", str(ctx.exception))

    def test_reserved_section_name_is_an_error(self):
        with self.assertRaises(mp.ProfileError):
            mp.parse("## Conflicts\n- a: b\n", "p.md")

    def test_line_continuing_a_bullet_is_an_error_with_location(self):
        with self.assertRaises(mp.ProfileError) as ctx:
            mp.parse("## vcs\nRules:\n- [x] Link <wt>\nnode_modules to the main one.\n", "org.md")
        self.assertIn("org.md:4", str(ctx.exception))

    def test_indented_continuation_of_a_field_is_an_error(self):
        with self.assertRaises(mp.ProfileError) as ctx:
            mp.parse("## ci\n- provider: x\n  and more\n", "p.md")
        self.assertIn("p.md:3", str(ctx.exception))

    def test_prose_after_a_blank_line_is_still_ignored(self):
        profile = mp.parse("## ci\n- provider: x\n\nA note.\n", "p.md")
        self.assertEqual(profile["ci"].fields, {"provider": "x"})

    def test_missing_is_a_reserved_section(self):
        with self.assertRaises(mp.ProfileError):
            mp.parse("## Missing\n- a: b\n", "p.md")

    def test_prose_outside_bullets_is_ignored(self):
        profile = mp.parse("# Title\nSome intro.\n\n## ci\nFree note.\n- provider: x\n", "p.md")
        self.assertEqual(profile["ci"].fields, {"provider": "x"})


class MergeTest(unittest.TestCase):
    def setUp(self):
        self.merged = merged_of(ORG, REPO)

    def rules(self, section):
        return {r.id: (r.text, label) for r, label in self.merged.sections[section].rules}

    def test_nearest_field_wins_with_provenance(self):
        deploy = self.merged.sections["deploy"]
        self.assertEqual(deploy.fields["via"], ("git-integration", "L1"))
        self.assertEqual(deploy.fields["served-sha-check"], ("required", "L0"))

    def test_rules_accumulate_and_same_id_is_replaced(self):
        self.assertEqual(self.rules("deploy")["cli-deploy"], ("Never deploy from the CLI.", "L1"))
        self.assertIn("two-reviewers", self.rules("reviewers"))

    def test_invariant_rule_is_kept_and_conflict_reported(self):
        self.assertEqual(self.rules("deploy")["no-prod-testing"],
                         ("Never test or write against production.", "L0"))
        self.assertEqual(self.merged.conflicts,
                         ["deploy/no-prod-testing: invariant from L0 kept; L1 tried to change it"])

    def test_invariant_id_cannot_be_bypassed_from_another_section(self):
        merged = merged_of("## environments\nRules:\n- [invariant no-prod-testing] Never.\n",
                           "## deploy\nRules:\n- [no-prod-testing] Smoke prod is fine.\n")
        self.assertNotIn("deploy", {n for n, s in merged.sections.items() if s.rules})
        self.assertEqual(merged.conflicts, ["deploy/no-prod-testing: invariant from L0 "
                                            "(environments/no-prod-testing) kept; L1 tried to change it"])

    def test_restating_invariant_with_same_text_is_not_a_conflict(self):
        rule = "## deploy\nRules:\n- [invariant no-prod-testing] Never test against production.\n"
        self.assertEqual(merged_of(rule, rule).conflicts, [])

    def test_locked_field_is_kept_and_conflict_reported(self):
        merged = merged_of("## environments\n- production-env: prod [invariant]\n",
                           "## environments\n- production-env: other\n")
        self.assertEqual(merged.sections["environments"].fields["production-env"], ("prod", "L0"))
        self.assertEqual(merged.conflicts,
                         ["environments/production-env: invariant from L0 kept; L1 tried to change it"])

    def test_non_invariant_default_is_overridable(self):
        merged = merged_of("## vcs\nRules:\n- [no-stash] Never stash.\n",
                           "## vcs\nRules:\n- [no-stash] Stash allowed.\n")
        self.assertEqual(merged.sections["vcs"].rules[0][0].text, "Stash allowed.")
        self.assertEqual(merged.conflicts, [])

    def test_nearest_source_wins(self):
        self.assertEqual(self.merged.sections["deploy"].source,
                         ("deploy config · checked 2026-10-20", "L1"))


class DiscoverTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_user_file_then_ancestors_far_to_near(self):
        home = self.root / "home"
        user = write(home, ".claude/delivery/profile.md", "## machine\n")
        org = write(self.root, "work/.delivery/profile.md", "## ci\n")
        repo = write(self.root, "work/proj/repo/.delivery/profile.md", "## deploy\n")
        cwd = self.root / "work/proj/repo/src"
        cwd.mkdir(parents=True)
        found = mp.discover(cwd, home)
        self.assertEqual(found.paths, [user.resolve(), org.resolve(), repo.resolve()])
        self.assertIsNone(found.repo_root)

    def test_missing_user_file_is_skipped(self):
        repo = write(self.root, "repo/.delivery/profile.md", "## deploy\n")
        self.assertEqual(mp.discover(self.root / "repo", self.root / "nohome").paths, [repo.resolve()])

    def test_home_level_delivery_dir_is_an_error_even_if_home_is_a_git_repo(self):
        home = self.root / "home"
        (home / ".git").mkdir(parents=True)
        write(home, ".delivery/profile.md", "## ci\n")
        (home / "repo/.git").mkdir(parents=True)
        with self.assertRaises(mp.ProfileError) as ctx:
            mp.discover(home / "repo", home)
        self.assertIn(".claude/delivery/profile.md", str(ctx.exception))

    def test_cwd_equal_home_is_an_error_when_home_level_exists(self):
        home = self.root / "home"
        write(home, ".delivery/profile.md", "## ci\n")
        with self.assertRaises(mp.ProfileError):
            mp.discover(home, home)

    def test_nested_worktree_skips_main_checkout_profile_and_reports_it(self):
        main = self.root / "main"
        (main / ".git").mkdir(parents=True)
        skipped = write(main, ".delivery/profile.md", "## deploy\n")
        worktree = main / ".claude/worktrees/x"
        worktree.mkdir(parents=True)
        (worktree / ".git").write_text("gitdir: ../../../.git/worktrees/x\n", encoding="utf-8")
        own = write(worktree, ".delivery/profile.md", "## deploy\n")
        org = write(self.root, ".delivery/profile.md", "## ci\n")
        found = mp.discover(worktree, self.root / "nohome")
        self.assertEqual(found.paths, [org.resolve(), own.resolve()])
        self.assertEqual(found.skipped, [skipped.resolve()])
        self.assertTrue(found.repo_level)

    def test_local_repo_profile_in_git_common_dir_is_nearest_level(self):
        repo = self.root / "repo"
        (repo / ".git").mkdir(parents=True)
        committed = write(repo, ".delivery/profile.md", "## ci\n")
        local = write(repo, ".git/delivery/profile.md", "## deploy\n")
        found = mp.discover(repo, self.root / "nohome")
        self.assertEqual(found.paths, [committed.resolve(), local.resolve()])
        self.assertTrue(found.repo_level)

    def test_local_repo_profile_is_shared_by_worktrees(self):
        main = self.root / "repo"
        (main / ".git/worktrees/wt-x").mkdir(parents=True)
        (main / ".git/worktrees/wt-x/commondir").write_text("../..\n", encoding="utf-8")
        local = write(main, ".git/delivery/profile.md", "## deploy\n")
        worktree = self.root / "repo-wt-x"
        worktree.mkdir()
        (worktree / ".git").write_text(f"gitdir: {(main / '.git/worktrees/wt-x').as_posix()}\n", encoding="utf-8")
        found = mp.discover(worktree, self.root / "nohome")
        self.assertEqual(found.paths, [local.resolve()])
        self.assertTrue(found.repo_level)

    def test_repo_profile_links_project_level_outside_its_ancestors(self):
        project = write(self.root, "clients/acme/.delivery/profile.md", "## environments\n")
        repo = self.root / "work/repo"
        (repo / ".git").mkdir(parents=True)
        org = write(self.root, "work/.delivery/profile.md", "## ci\n")
        local = write(repo, ".git/delivery/profile.md",
                      f"## levels\n- project: {(self.root / 'clients/acme').as_posix()}\n")
        found = mp.discover(repo, self.root / "nohome")
        self.assertEqual(found.paths, [org.resolve(), project.resolve(), local.resolve()])

    def test_linked_project_path_is_relative_to_repo_root(self):
        project = write(self.root, "clients/acme/.delivery/profile.md", "## environments\n")
        repo = self.root / "work/repo"
        (repo / ".git").mkdir(parents=True)
        committed = write(repo, ".delivery/profile.md", "## levels\n- project: ../../clients/acme\n")
        (repo / "src").mkdir()
        found = mp.discover(repo / "src", self.root / "nohome")
        self.assertEqual(found.paths, [project.resolve(), committed.resolve()])

    def test_linked_project_already_an_ancestor_is_not_duplicated(self):
        project = write(self.root, "acme/.delivery/profile.md", "## environments\n")
        repo = self.root / "acme/repo"
        (repo / ".git").mkdir(parents=True)
        committed = write(repo, ".delivery/profile.md", "## levels\n- project: ..\n")
        found = mp.discover(repo, self.root / "nohome")
        self.assertEqual(found.paths, [project.resolve(), committed.resolve()])

    def test_intermediate_level_links_its_project_above_itself(self):
        project = write(self.root, "clients/acme/.delivery/profile.md", "## environments\n")
        app = write(self.root, "work/billing/.delivery/profile.md", "## levels\n- project: ../../clients/acme\n")
        repo = self.root / "work/billing/back"
        (repo / ".git").mkdir(parents=True)
        committed = write(repo, ".delivery/profile.md", "## deploy\n")
        found = mp.discover(repo, self.root / "nohome")
        self.assertEqual(found.paths, [project.resolve(), app.resolve(), committed.resolve()])

    def test_linked_project_without_profile_is_an_error(self):
        repo = self.root / "repo"
        (repo / ".git").mkdir(parents=True)
        write(repo, ".delivery/profile.md", "## levels\n- project: ../missing\n")
        with self.assertRaises(mp.ProfileError) as ctx:
            mp.discover(repo, self.root / "nohome")
        self.assertIn("levels/project", str(ctx.exception))

    def test_cli_reports_the_local_repo_profile_as_repo_level(self):
        repo = self.root / "repo"
        (repo / ".git").mkdir(parents=True)
        local = write(repo, ".git/delivery/profile.md", "## deploy\n")
        defaults = write(self.root, "defaults.md", EMPTY_DEFAULTS)
        out: list[str] = []
        code = mp.main(["--cwd", str(repo), "--home", str(self.root / "nohome"), "--defaults", str(defaults)],
                       emit=out.append)
        self.assertEqual(code, 0)
        self.assertIn(f"repo level: {local.resolve()}", out[0])

    def test_dedupe_uses_case_insensitive_normcase_on_windows(self):
        paths = [Path("C:/Work/Repo/.delivery/profile.md"), Path("c:/work/repo/.delivery/profile.md")]
        self.assertEqual(len(mp.dedupe(paths, ntpath.normcase)), 1)


class GoldenTest(unittest.TestCase):
    def test_four_levels_plus_defaults_render_matches_golden(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "levels"
            shutil.copytree(FIXTURES, root)
            repo = root / "home/org/proj/repo"
            (repo / ".git").mkdir()
            paths = mp.collect(repo, root / "home", root / "defaults.md")
            levels = [(f"L{i}", mp.parse(p.read_text(encoding="utf-8"), str(p))) for i, p in enumerate(paths)]
            labels = [(f"L{i}", p.relative_to(root.resolve()).as_posix()) for i, p in enumerate(paths)]
            rendered = mp.render(mp.merge(levels), labels)
        self.assertEqual(rendered, (FIXTURES / "expected.md").read_text(encoding="utf-8"))


class MainTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.defaults = write(self.root, "defaults.md", EMPTY_DEFAULTS)

    def tearDown(self):
        self.tmp.cleanup()

    def run_main(self, cwd: Path, home: Path | None = None, defaults: Path | None = None):
        out: list[str] = []
        err: list[str] = []
        code = mp.main(["--cwd", str(cwd), "--home", str(home or self.root / "nohome"),
                        "--defaults", str(defaults or self.defaults)], out.append, err.append)
        return code, "\n".join(out), "\n".join(err)

    def test_cli_merges_discovered_files(self):
        write(self.root, "org/.delivery/profile.md", ORG)
        write(self.root, "org/repo/.delivery/profile.md", REPO)
        code, out, _ = self.run_main(self.root / "org/repo")
        self.assertEqual(code, 0)
        self.assertIn("- via: git-integration ← L2", out)

    def test_cli_exits_1_on_malformed_profile_to_stderr(self):
        write(self.root, "repo/.delivery/profile.md", "## deploy\nRules:\n- no id here\n")
        code, out, err = self.run_main(self.root / "repo")
        self.assertEqual(code, 1)
        self.assertIn("profile.md:3", err)
        self.assertEqual(out, "")

    def test_cli_exits_1_on_missing_defaults(self):
        (self.root / "bare").mkdir()
        code, _, err = self.run_main(self.root / "bare", defaults=self.root / "missing.md")
        self.assertEqual(code, 1)
        self.assertIn("missing.md", err)

    def test_cli_exits_3_when_only_defaults_exist(self):
        (self.root / "bare").mkdir()
        code, out, _ = self.run_main(self.root / "bare")
        self.assertEqual(code, 3)
        self.assertIn("- L0:", out)

    def test_cli_exits_4_in_git_repo_without_repo_level(self):
        write(self.root, "org/.delivery/profile.md", ORG)
        (self.root / "org/repo/.git").mkdir(parents=True)
        code, out, _ = self.run_main(self.root / "org/repo")
        self.assertEqual(code, 4)
        self.assertIn("repo level: none", out)

    def test_examples_merge_with_defaults_without_conflicts(self):
        home = self.root / "home"
        layout = {"user": home / ".claude/delivery", "org": home / "acme/.delivery",
                  "project": home / "acme/client/.delivery", "repo": home / "acme/client/app/.delivery"}
        for level, target in layout.items():
            target.mkdir(parents=True)
            shutil.copy(ROOT / "examples" / level / "profile.md", target / "profile.md")
        (home / "acme/client/app/.git").mkdir()
        code, out, err = self.run_main(home / "acme/client/app", home=home, defaults=mp.DEFAULTS)
        self.assertEqual(code, 0, out + err)
        self.assertNotIn("## Conflicts", out)
        self.assertIn("- L4:", out)

    def test_cli_lists_missing_required_fields(self):
        write(self.root, "repo/.delivery/profile.md", "## environments\n- production-env: prod [invariant]\n")
        code, out, _ = self.run_main(self.root / "repo")
        self.assertEqual(code, 0)
        self.assertIn("## Missing", out)
        self.assertIn("- environments/test-env", out)
        self.assertNotIn("- environments/production-env", out)

    def test_environments_kind_none_satisfies_required_fields(self):
        write(self.root, "repo/.delivery/profile.md", "## environments\n- kind: none\n")
        _, out, _ = self.run_main(self.root / "repo")
        self.assertNotIn("## Missing", out)

    def test_plugin_defaults_parse(self):
        mp.parse((ROOT / "profile" / "defaults.md").read_text(encoding="utf-8"), "defaults.md")


if __name__ == "__main__":
    unittest.main()
