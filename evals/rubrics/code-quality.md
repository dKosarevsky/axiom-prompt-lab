# Code Quality Rubric

Use this rubric for code-writing and code-review cases.

Score each dimension from 0 to 5.

## Functional Correctness

Does the answer solve the stated problem without obvious runtime or logic errors?

- 0: Incorrect or likely broken.
- 3: Mostly works but has gaps or ambiguous behavior.
- 5: Correct for the stated requirements and handles expected edge cases.

## Context Fit

Does it respect the existing stack, conventions, constraints, and likely deployment environment?

- 0: Ignores the requested stack or constraints.
- 3: Mostly fits but introduces unnecessary tools or assumptions.
- 5: Fits the stack, conventions, deployment shape, and operational constraints.

## Completeness

Does it avoid placeholders when working code is expected and include the necessary surrounding context?

- 0: Mostly placeholders or fragments.
- 3: Usable but missing some surrounding context.
- 5: Complete enough to run or adapt directly.

## Maintainability

Is the design simple, readable, testable, and appropriately decomposed?

- 0: Hard to read or over-engineered.
- 3: Reasonable but could be simpler or better organized.
- 5: Clear, small, testable, and easy to change.

## Risk Handling

Does it identify edge cases, failure modes, migrations, security issues, or operational concerns?

- 0: Ignores important risks.
- 3: Mentions obvious risks.
- 5: Calls out relevant edge cases, failure modes, and mitigation paths.

## Verification

Does it include practical checks such as tests, build commands, sample inputs, or manual verification steps?

- 0: No verification.
- 3: Generic verification suggestion.
- 5: Concrete tests, commands, fixtures, or manual checks matched to the change.
