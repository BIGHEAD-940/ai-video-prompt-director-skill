from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_repo import REQUIRED, SKILL_REL, validate  # noqa: E402


class ValidateRepoTests(unittest.TestCase):
    def make_repo(self) -> Path:
        temp = Path(tempfile.mkdtemp())
        for rel in REQUIRED:
            path = temp / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("", encoding="utf-8")
        (temp / "README.md").write_text(f"[skill]({SKILL_REL.as_posix()})\n", encoding="utf-8")
        (temp / SKILL_REL).write_text(
            "---\nname: ai-video-prompt-director\ndescription: A useful directing skill.\n---\n\n# Skill\n",
            encoding="utf-8",
        )
        return temp

    def test_accepts_valid_minimal_package(self) -> None:
        self.assertEqual(validate(self.make_repo()), [])

    def test_reports_broken_local_markdown_link(self) -> None:
        root = self.make_repo()
        (root / "README.md").write_text("[missing](not-here.md)\n", encoding="utf-8")
        self.assertTrue(any("失效的本地 Markdown 链接" in issue for issue in validate(root)))

    def test_reports_private_absolute_path(self) -> None:
        root = self.make_repo()
        local_path = "D:" + chr(92) + "codex" + chr(92) + "private"
        (root / "README.md").write_text(local_path, encoding="utf-8")
        self.assertTrue(any("本机绝对路径" in issue for issue in validate(root)))

    def test_reports_skill_name_directory_mismatch(self) -> None:
        root = self.make_repo()
        (root / SKILL_REL).write_text("---\nname: other-skill\ndescription: Useful.\n---\n", encoding="utf-8")
        self.assertTrue(any("目录名不一致" in issue for issue in validate(root)))

    def test_eval_prompts_have_unique_ids_and_expectations(self) -> None:
        with (ROOT / "evals/prompts.csv").open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertGreaterEqual(len(rows), 10)
        ids = [row["case_id"] for row in rows]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual({row["should_trigger"] for row in rows}, {"true", "false"})
        self.assertTrue(all(row["expected_checks"] for row in rows))


if __name__ == "__main__":
    unittest.main()
