# Evaluation Plan

This directory will hold prompt comparison cases, rubrics, runner configuration, and generated artifacts.

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

The first runnable suite should use promptfoo because it maps well to prompt A/B testing with YAML cases, provider configuration, and assertions. OpenAI Evals or API graders can be added later for structured judge workflows.

