# Evaluation Plan

This directory holds prompt comparison cases, rubrics, runner configuration, and generated artifacts.

## Goal

Measure whether the prompt improves usefulness for pragmatic software engineering, AI-agent work, and data-platform tasks.

The target claim is narrow:

> Does this compact instruction layer make answers more useful for pragmatic software engineering, AI-agent work, and data-platform tasks?

## Methodology

Compare:

- baseline: no custom instructions;
- candidate: a named prompt version;
- same model;
- same temperature or reasoning settings;
- same cases;
- same scoring rubric;
- multiple runs for non-deterministic settings;
- saved outputs as artifacts;
- judge separated from the generation model when possible.

For API-based runs, the candidate prompt is modeled as a chat `system` message. This is the closest repeatable analogue to UI Custom Instructions in an automated eval runner.

The default promptfoo suite runs in no-tools mode. Freshness cases should not expect live browsing. They test whether the model recognizes changeable facts and avoids inventing current details. Tool-enabled freshness evals can be added as a separate suite later.

## Initial Case Categories

- Russian answer quality: Russian output, natural style, sane handling of English technical terms.
- Code quality: working code, assumptions, risks, edge cases, and verification.
- AI-agent architecture: memory/state/tool use/retries/evals/observability/guardrails.
- Rust fit: use Rust when appropriate and avoid forcing it when not.
- Freshness: handle current software versions and docs with source checking or uncertainty.
- Clarification policy: proceed with assumptions when possible; ask only when blocked.

## Scoring Dimensions

- correctness: 0-5
- specificity: 0-5
- production usefulness: 0-5
- risk/edge-case awareness: 0-5
- language/style fit: 0-5
- unnecessary verbosity penalty: 0-2

Agent/data-platform cases may also score:

- tool-use awareness;
- state/memory handling;
- evals and regression testing;
- observability and tracing;
- retry/fallback behavior;
- security and guardrails;
- latency/cost trade-offs.

## Runner Direction

The first runnable suite uses promptfoo because it maps well to prompt A/B testing with YAML cases, provider configuration, and assertions. OpenAI Evals or API graders can be added later for structured judge workflows.

Run from the repository root:

```bash
cd evals
promptfoo eval -c promptfooconfig.yaml
```

Save run artifacts:

```bash
RUN_DIR="../reports/runs/$(date +%Y-%m-%d)"
mkdir -p "$RUN_DIR"
promptfoo eval -c promptfooconfig.yaml \
  --output "$RUN_DIR/results.json" \
  --output "$RUN_DIR/results.csv" \
  --output "$RUN_DIR/results.html"
```

Use the report config for a slower preliminary report run:

```bash
promptfoo eval -c promptfooconfig.report.yaml
```

The current suite contains 12 starter cases:

- `russian-style.yaml`
- `clarification-policy.yaml`
- `rust-fit.yaml`
- `agent-architecture.yaml`
- `code-quality.yaml`
- `freshness.yaml`

The config compares:

- `baseline`: user message only;
- `compact-v0.1.0`: compact prompt as system message plus the same user input.

The candidate system prompt in `evals/prompts/compact-v0.1.0-system.txt` must stay byte-for-byte synced with the fenced prompt block in `prompts/compact.md`. CI checks this with `scripts/count_chars.py --compare-text`.

`promptfooconfig.yaml` is a smoke suite with `repeat: 1`. `promptfooconfig.report.yaml` uses `repeat: 3` and a separate grader setting for report-grade runs. The report config still needs a real API run before publishing benchmark claims.
