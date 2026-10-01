# Design Note

## User flow
1. Learner selects an LLD problem.
2. Learner reads requirements and optional hints.
3. Learner writes a solution as text (code/diagram can be described in the same submission).
4. Learner submits.
5. Evaluator returns a score plus strengths and concrete improvements.
6. Learner reviews history and retries.

## Core domain model
- `Problem`: requirements, hints, difficulty and timebox.
- `Attempt`: a learner's submitted solution, timestamp and evaluation.
- `Evaluation`: score, strengths, improvements and detected design signals.
- `Evaluator`: isolated service/function that evaluates an attempt.

## Evaluation approach
The MVP uses explainable heuristic checks. It looks for evidence of classes/interfaces, responsibility boundaries, relationships, extensibility, edge cases and trade-offs. This is deliberately not presented as an absolute correctness score because multiple LLD designs can be valid.

## Key trade-offs
- Rule-based feedback over an external LLM: less nuanced, but deterministic, cheap and runnable without secrets.
- SQLite over a managed database: less scalable, but minimal setup and sufficient for the assignment.
- Text editor over a full UML editor: narrower, but much faster to build and still tests the core learner loop.
- Monolith over services: simpler deployment and clearer focus on domain design.
