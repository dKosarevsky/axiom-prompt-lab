# axiom-prompt-lab

A small prompt lab for testing whether a compact instruction layer improves answers for pragmatic software engineering, AI-agent work, and data-platform tasks.

The project is intentionally benchmark-first. It does not claim that a custom prompt makes a model "smarter"; it tests a narrower question: does the prompt make answers more useful for the target workflows?

## What Problem This Solves

General custom instructions often improve tone but miss engineering-specific behavior: clear assumptions, fewer unnecessary clarification loops, realistic code quality, tool-use awareness, eval thinking, observability, latency and cost trade-offs, and practical verification steps.

This repository separates:

- reusable prompts;
- benchmark cases;
- scoring rubrics;
- result reports;
- small utility scripts.

## Who It Is For

The primary target is engineers using ChatGPT or API-based assistants for:

- AI-agent architecture and evaluation;
- data-platform and pipeline work;
- pragmatic software engineering;
- code review, debugging, and implementation planning;
- Rust-aware decisions where Rust is useful, but not forced.

## Quick Start

Use the compact prompt for ChatGPT Custom Instructions:

1. Open [prompts/compact.md](prompts/compact.md).
2. Copy only the fenced `text` block.
3. Paste it into ChatGPT Custom Instructions.
4. Check the character count:

```bash
python3 scripts/count_chars.py prompts/compact.md
```

Use [prompts/full.md](prompts/full.md) for Projects, GPTs, API system prompts, or agent environments where a longer instruction layer is acceptable.

Run local quality checks:

```bash
python3 -m unittest discover -s tests
python3 scripts/count_chars.py prompts/compact.md --check-metadata --compare-text evals/prompts/compact-v0.1.0-system.txt
```

Run the promptfoo A/B skeleton when you have an API key and want to spend eval budget:

```bash
cd evals
promptfoo eval -c promptfooconfig.yaml
```

Persist JSON/CSV/HTML run artifacts:

```bash
RUN_DIR="../reports/runs/$(date +%Y-%m-%d)"
mkdir -p "$RUN_DIR"
promptfoo eval -c promptfooconfig.yaml \
  --output "$RUN_DIR/results.json" \
  --output "$RUN_DIR/results.csv" \
  --output "$RUN_DIR/results.html"
```

Run the report suite with saved JSON/CSV/HTML outputs:

```bash
OPENAI_API_KEY=... scripts/run_promptfoo_report.sh 2026-04-26
```

Or trigger `.github/workflows/eval-report.yml` after adding an `OPENAI_API_KEY` repository secret.

Summarize a completed JSON run:

```bash
python3 scripts/summarize_promptfoo_results.py \
  reports/runs/2026-04-26/results.json \
  --output reports/2026-04-26-summary.md
```

## Repository Layout

```text
prompts/
  compact.md                 Compact prompt for ChatGPT Custom Instructions
  full.md                    Expanded prompt for agent and API contexts
  variants/
    general.md               General-purpose baseline variant
    agent-data-platform.md   Targeted agent/data-platform variant
evals/
  README.md                  Benchmark methodology and roadmap
  promptfooconfig.yaml       Runnable promptfoo A/B config
  promptfooconfig.report.yaml Repeated-run report config
  cases/
    *.yaml                   Promptfoo-compatible starter cases
  prompts/
    *.json                   Chat prompt templates for baseline and candidate
    compact-v0.1.0-system.txt Synced eval copy of the compact prompt
  rubrics/
    answer-quality.md        General answer scoring rubric
    agent-engineering.md     Agent/data-platform scoring rubric
    code-quality.md          Code-focused scoring rubric
scripts/
  count_chars.py             Custom Instructions character-count helper
  count_eval_cases.py        Eval suite case-count helper
  run_promptfoo_report.sh    Report-run wrapper that saves JSON/CSV/HTML outputs
  summarize_promptfoo_results.py Promptfoo JSON-to-Markdown summarizer
tests/
  test_count_chars.py        Tests for prompt character counting
reports/
  runs/                      Saved promptfoo run artifacts
  2026-04-26-initial.md      Preflight report and API credential blocker
  2026-04-26-initial-template.md First report template
```

## Benchmark Philosophy

Benchmarks should compare prompt behavior, not vibes.

The intended comparison:

- baseline: no custom instructions;
- candidate: a named prompt version;
- same model and settings;
- same test cases;
- same scoring rubric;
- multiple runs where non-determinism matters;
- outputs stored as artifacts;
- judge separated from the generation model when possible.

Initial scoring dimensions:

- correctness;
- specificity;
- production usefulness;
- risk and edge-case awareness;
- language and style fit;
- unnecessary verbosity penalty.

For agent/data-platform cases, additional dimensions include tool-use awareness, state and memory handling, evals and regression testing, observability, retries and fallbacks, security and guardrails, and latency/cost trade-offs.

## Current Status

Current status: benchmark-ready preflight, not benchmark-backed yet. It contains prompts, version metadata, 60 promptfoo-compatible starter cases, scoring rubrics, character-count/sync helpers, CI checks, an eval report workflow, and a report template.

The next milestone is running the first benchmark with an `OPENAI_API_KEY` and publishing completed artifacts and scores.
