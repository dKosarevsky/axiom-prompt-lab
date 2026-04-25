# Initial Benchmark Report Template

Date: 2026-04-26

## Prompt Versions

- Baseline: no custom instructions
- Candidate: compact v0.1.0

## Model And Settings

- Provider:
- Model:
- Endpoint:
- Temperature/reasoning settings:
- Runs per case:
- Judge:

## Cases

- Russian style:
- Clarification policy:
- Rust fit:
- Agent architecture:
- Code quality:
- Freshness:

## Scoring Method

Use the rubrics in `evals/rubrics/`.

Report both:

- aggregate score by category;
- qualitative notes where the candidate helped or hurt.

## Results

| Category | Baseline | Compact v0.1.0 | Delta | Notes |
| --- | ---: | ---: | ---: | --- |
| Russian style |  |  |  |  |
| Clarification policy |  |  |  |  |
| Rust fit |  |  |  |  |
| Agent architecture |  |  |  |  |
| Code quality |  |  |  |  |
| Freshness |  |  |  |  |

## Where The Prompt Helped

- 

## Where The Prompt Hurt

- 

## Known Limitations

- Preliminary suite only.
- Small case count.
- LLM judging may be noisy.
- No multi-run variance reported unless `repeat` is increased.

## Next Prompt Changes

- 

