import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "summarize_promptfoo_results.py"


class SummarizePromptfooResultsTests(unittest.TestCase):
    def test_writes_markdown_summary_from_promptfoo_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            results_path = tmp_path / "results.json"
            output_path = tmp_path / "summary.md"
            results_path.write_text(
                json.dumps(
                    {
                        "results": {
                            "outputs": [
                                {
                                    "prompt": {"label": "baseline"},
                                    "testCase": {"metadata": {"category": "rust-fit"}},
                                    "success": True,
                                    "score": 0.55,
                                    "namedScores": {"rust-fit": 0.5},
                                },
                                {
                                    "prompt": {"label": "compact-v0.1.0"},
                                    "testCase": {"metadata": {"category": "rust-fit"}},
                                    "success": True,
                                    "score": 0.9,
                                    "namedScores": {"rust-fit": 0.92},
                                },
                                {
                                    "prompt": {"label": "baseline"},
                                    "testCase": {"metadata": {"category": "code-quality"}},
                                    "success": False,
                                    "score": 0.75,
                                    "namedScores": {"verbosity-control": 0.9},
                                },
                                {
                                    "prompt": {"label": "compact-v0.1.0"},
                                    "testCase": {"metadata": {"category": "code-quality"}},
                                    "success": False,
                                    "score": 0.5,
                                    "namedScores": {"verbosity-control": 0.4},
                                },
                            ]
                        }
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(results_path), "--output", str(output_path)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            summary = output_path.read_text(encoding="utf-8")

        self.assertIn("# Promptfoo Results Summary", summary)
        self.assertIn("Total outputs: 4", summary)
        self.assertIn("Baseline average", summary)
        self.assertIn("Candidate average", summary)
        self.assertIn("rust-fit", summary)
        self.assertIn("verbosity-control", summary)
        self.assertIn("Biggest Wins", summary)
        self.assertIn("Biggest Regressions", summary)
        self.assertIn("Human Review Candidates", summary)


if __name__ == "__main__":
    unittest.main()
