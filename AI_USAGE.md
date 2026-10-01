# AI Usage

AI assistance was used as a development aid, with design decisions reviewed and simplified for the assignment scope.

## Decision 1 — MVP scope
**AI suggested:** A broader platform with authentication, multiple roles and richer assessment infrastructure.

**Decision:** Rejected most of that scope. The brief explicitly asks for a focused two-day prototype, so the implementation keeps only problem selection, practice, feedback and history.

## Decision 2 — Evaluation model
**AI suggested:** Using an LLM as the sole evaluator.

**Decision:** Rejected as the only mechanism. A pure LLM score can be opaque and unnecessarily dependent on an external key. The MVP uses transparent heuristic signals and leaves the evaluator isolated so an LLM can be added later for explanation.

## Decision 3 — Architecture
**AI suggested:** A service-oriented architecture could separate evaluation and persistence.

**Decision:** Rejected for this assignment. A Flask monolith with SQLite keeps the engineering effort focused on LLD and product behaviour, matching the scope boundary.

## Decision 4 — Feedback format
**AI suggested:** A single score and generic recommendation.

**Decision:** Rejected. Feedback is split into strengths, improvements and the next iteration step, with explicit signals for responsibilities, relationships, extensibility, edge cases and trade-offs.

## Decision 5 — Persistence
**AI suggested:** A managed database could support future scale.

**Decision:** SQLite was accepted for the MVP because attempts need persistence but production-scale infrastructure is outside the assignment scope.
