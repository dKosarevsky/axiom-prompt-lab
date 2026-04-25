import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class EvalScaffoldContractTests(unittest.TestCase):
    def test_smoke_config_persists_default_html_output(self) -> None:
        config = (ROOT / "evals" / "promptfooconfig.yaml").read_text(encoding="utf-8")

        self.assertIn("outputPath: ../reports/runs/latest/results.html", config)

    def test_report_config_uses_repeated_runs_and_separate_judge(self) -> None:
        report_config_path = ROOT / "evals" / "promptfooconfig.report.yaml"

        self.assertTrue(report_config_path.exists())
        config = report_config_path.read_text(encoding="utf-8")
        self.assertRegex(config, r"\brepeat:\s*3\b")
        self.assertIn("grader:", config)

    def test_all_case_assertions_have_metric_labels(self) -> None:
        for case_path in sorted((ROOT / "evals" / "cases").glob("*.yaml")):
            text = case_path.read_text(encoding="utf-8")
            assert_count = len(re.findall(r"^\s*- type:", text, flags=re.MULTILINE))
            metric_count = len(re.findall(r"^\s*metric:", text, flags=re.MULTILINE))

            self.assertGreater(assert_count, 0, case_path)
            self.assertEqual(metric_count, assert_count, case_path)

    def test_no_tools_freshness_mode_is_documented(self) -> None:
        readme = (ROOT / "evals" / "README.md").read_text(encoding="utf-8")

        self.assertIn("no-tools mode", readme)
        self.assertIn("Freshness cases should not expect live browsing", readme)

    def test_report_artifact_directory_and_changelog_exist(self) -> None:
        self.assertTrue((ROOT / "reports" / "runs" / ".gitkeep").exists())
        self.assertTrue((ROOT / "reports" / "runs" / "latest" / ".gitkeep").exists())
        self.assertTrue((ROOT / "reports" / "runs" / "report" / ".gitkeep").exists())

        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("## 0.1.0", changelog)
        self.assertIn("compact prompt", changelog.lower())


if __name__ == "__main__":
    unittest.main()
