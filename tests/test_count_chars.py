import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "count_chars.py"


def run_count_chars(
    path: Path, limit: int = 1500, check_metadata: bool = False
) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, str(SCRIPT), str(path), "--limit", str(limit)]
    if check_metadata:
        command.append("--check-metadata")

    return subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


class CountCharsTests(unittest.TestCase):
    def test_counts_prompt_block_and_passes_when_under_limit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            prompt = Path(tmp_dir) / "prompt.md"
            prompt.write_text(
                "# Prompt\n\n```text\nabc\n12345\n```\n\nignored text\n",
                encoding="utf-8",
            )

            result = run_count_chars(prompt, limit=10)

        self.assertEqual(result.returncode, 0)
        self.assertIn("characters: 10", result.stdout)
        self.assertIn("limit: 10", result.stdout)
        self.assertIn("status: ok", result.stdout)

    def test_fails_when_prompt_block_exceeds_limit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            prompt = Path(tmp_dir) / "prompt.md"
            prompt.write_text("```text\nabcdef\n```\n", encoding="utf-8")

            result = run_count_chars(prompt, limit=5)

        self.assertEqual(result.returncode, 1)
        self.assertIn("characters: 7", result.stdout)
        self.assertIn("status: over limit by 2", result.stdout)

    def test_checks_frontmatter_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            prompt = Path(tmp_dir) / "prompt.md"
            prompt.write_text(
                "---\n"
                "version: 0.1.0\n"
                "char_limit: 10\n"
                "measured_chars: 4\n"
                "---\n"
                "```text\nabc\n```\n",
                encoding="utf-8",
            )

            result = run_count_chars(prompt, limit=10, check_metadata=True)

        self.assertEqual(result.returncode, 0)
        self.assertIn("metadata: ok", result.stdout)

    def test_fails_when_measured_chars_metadata_is_stale(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            prompt = Path(tmp_dir) / "prompt.md"
            prompt.write_text(
                "---\nchar_limit: 10\nmeasured_chars: 999\n---\n```text\nabc\n```\n",
                encoding="utf-8",
            )

            result = run_count_chars(prompt, limit=10, check_metadata=True)

        self.assertEqual(result.returncode, 1)
        self.assertIn("metadata measured_chars: 999 != 4", result.stdout)

    def test_eval_prompt_copy_matches_compact_prompt(self) -> None:
        compact = ROOT / "prompts" / "compact.md"
        eval_copy = ROOT / "evals" / "prompts" / "compact-v0.1.0-system.txt"

        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(compact), "--compare-text", str(eval_copy)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("compare_text: ok", result.stdout)


if __name__ == "__main__":
    unittest.main()
