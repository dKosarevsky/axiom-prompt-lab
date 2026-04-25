import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "count_chars.py"


def run_count_chars(path: Path, limit: int = 1500) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(path), "--limit", str(limit)],
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


if __name__ == "__main__":
    unittest.main()
