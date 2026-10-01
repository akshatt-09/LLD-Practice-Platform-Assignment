# LLD Practice Platform

A focused 2-day engineering assignment MVP for practicing Low-Level Design. The learner chooses a problem, writes a design, submits it, receives transparent structured feedback, and can review/retry previous attempts.

## Product flow
**Choose problem → Read requirements → Design → Submit → Feedback → Review → Try again**

## Stack
- React + Vite frontend
- Flask REST API
- SQLite persistence
- Rule-based evaluator for the MVP (no external AI key required)

## Run locally
### Backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

The Vite app expects the API at `http://localhost:5000/api`. For deployment set `VITE_API_URL` to the deployed backend API URL.

## Design decisions
1. A monolith keeps the MVP focused on LLD/domain design rather than infrastructure.
2. SQLite is enough for a two-day prototype and makes the app easy to run locally.
3. The evaluator checks explicit design signals rather than claiming there is one “correct” LLD. This makes feedback explainable and leaves room for multiple valid designs.
4. Attempts are persisted so the learner can compare and retry instead of solving once.
5. The evaluator is isolated behind one function so an LLM-based evaluator can be added later without changing the learner flow.

## Limitations
- The evaluator is heuristic and does not understand arbitrary UML/code semantics.
- Authentication and multi-user isolation are intentionally out of scope.
- Diagrams are not rendered in this MVP; text is sufficient for an attempt.

## Testing
See `backend/test_app.py` for evaluator/API behaviour tests.
