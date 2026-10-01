# Research Note

## Problem
LLD practice is easy to start but difficult to evaluate consistently. A learner can design a Parking Lot, Elevator, or Vending Machine and still be unsure whether responsibilities, relationships, abstractions and trade-offs are clear.

## Existing approaches reviewed
- Generic coding-practice platforms focus heavily on correctness and automated test cases.
- Interview-preparation resources provide LLD prompts and reference discussions, but feedback is often static and does not preserve an individual learner's iteration.
- Diagramming tools help communicate a design but do not by themselves provide a practice loop or domain-specific review.

## Gap and product direction
The MVP focuses on the learner loop rather than building a large LMS: select a problem, understand its requirements, write a design, submit it, receive explainable feedback, review the attempt and try again.

The key product decision is to make feedback multi-dimensional rather than reducing an LLD to a single “correct/incorrect” result. The MVP checks for domain objects/classes, responsibility boundaries, relationships, extensibility, edge cases and explicit trade-offs. These are signals for reflection, not proof that a particular design is the only valid solution.

## Evaluation direction
A future evaluator could combine deterministic checks, static analysis of submitted code/diagrams, and an LLM reviewer. Deterministic checks provide consistency; an LLM can explain nuanced trade-offs. The evaluator should always show evidence for feedback and preserve the learner's original attempt so they can iterate.
