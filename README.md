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
  cases/
    example.yaml             First benchmark case format
  rubrics/
    answer-quality.md        General answer scoring rubric
    agent-engineering.md     Agent/data-platform scoring rubric
    code-quality.md          Code-focused scoring rubric
scripts/
  count_chars.py             Custom Instructions character-count helper
tests/
  test_count_chars.py        Tests for prompt character counting
reports/
  .gitkeep                   Future benchmark reports
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

This is the foundation version. It contains the first prompts, repository structure, methodology, and a character-count helper. The next step is adding a runnable prompt comparison suite and the first result report.
