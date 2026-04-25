# Agent Engineering Rubric

Use this rubric for AI-agent, data-platform, and architecture cases.

Score each dimension from 0 to 5.

## Tool-Use Awareness

Does the answer identify which tools or integrations are needed, when to use them, and what can fail?

- 0: Ignores tools or assumes tools cannot fail.
- 3: Mentions tools and some failure cases.
- 5: Specifies tool boundaries, permissions, inputs/outputs, failure modes, and review gates.

## State And Memory Handling

Does the answer distinguish transient state, durable memory, user preferences, task context, and audit history?

- 0: Does not address state or memory.
- 3: Mentions state or memory but does not define ownership or lifecycle.
- 5: Separates transient state, durable memory, preferences, audit history, privacy, and cleanup.

## Evals And Regression Testing

Does the answer include a way to evaluate quality, catch regressions, and compare prompt or agent changes?

- 0: No eval or regression plan.
- 3: Mentions evals or tests in general terms.
- 5: Defines cases, metrics, baseline/candidate comparison, artifacts, and regression gates.

## Observability And Tracing

Does the answer include logs, traces, metrics, artifacts, and debuggability for production operation?

- 0: Does not mention observability.
- 3: Mentions logs, metrics, or traces without concrete capture points.
- 5: Specifies logs, metrics, traces, artifacts, correlation IDs, failure visibility, and debugging workflow.

## Retry And Fallback Behavior

Does the answer cover retries, timeouts, partial failures, fallbacks, and idempotency where relevant?

- 0: Assumes happy path.
- 3: Mentions retries or fallbacks.
- 5: Covers timeouts, retry policy, backoff, idempotency, partial failure, fallback behavior, and user-visible degradation.

## Security And Guardrails

Does the answer cover permissions, data exposure, prompt injection, unsafe tool use, and review gates?

- 0: Ignores security and guardrails.
- 3: Mentions permissions or safety generically.
- 5: Covers least privilege, prompt injection, data exposure, unsafe tools, auditability, and human approval paths.

## Latency And Cost Trade-Offs

Does the answer consider model choice, caching, batching, tool calls, context size, and operational cost?

- 0: Ignores latency and cost.
- 3: Mentions latency or cost without actionable trade-offs.
- 5: Addresses model choice, caching, batching, context size, tool-call count, budget controls, and measurement.
