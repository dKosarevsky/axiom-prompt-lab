# Changelog

## 0.1.0

- Added the initial compact prompt for ChatGPT Custom Instructions.
- Added AI-agent/data-platform context.
- Added Rust-fit policy: suggest Rust when constraints justify it, do not force it.
- Added no-tools freshness behavior: recognize changeable facts and state uncertainty when live browsing is unavailable.
- Added promptfoo A/B skeleton, starter cases, rubrics, prompt metadata, and prompt-copy sync checks.
- Expanded the starter suite to 30 cases with negative controls.
- Added report-run artifact handling for JSON, CSV, and HTML outputs.
- Added a manual GitHub Actions report workflow that requires an `OPENAI_API_KEY` repository secret.
- Expanded the starter suite to 60 cases.
- Added protected metric thresholds for high-risk regression checks.
- Added a promptfoo JSON summarizer for generated Markdown reports.
- Reused the report wrapper from GitHub Actions and strengthened CI validation.
