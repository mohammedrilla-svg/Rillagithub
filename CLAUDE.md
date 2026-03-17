# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

B.L.A.S.T. (Blueprint, Link, Architect, Stylize, Trigger) Local Test Case Generator — an agentic AI tool that generates structured QA test cases from user stories using a local LLM (Llama 3.2) via Ollama. All inference is local; no external AI APIs are used.

## Architecture

The system follows a 3-layer architecture:

- **Layer 1 — Architecture** (`architecture/`): SOPs in Markdown defining goals, inputs, tool logic, and edge cases. Update SOPs before updating code.
- **Layer 2 — Navigation** (`backend/app.py`): FastAPI backend that routes requests between the frontend and tools. Single endpoint `POST /generate` plus `GET /health`.
- **Layer 3 — Tools** (`tools/`): Deterministic Python scripts. `generate_test_cases.py` assembles prompts, calls `ollama.generate()`, parses JSON output. `verify_ollama.py` is a connectivity handshake script.
- **Frontend** (`frontend/index.html`): Vanilla HTML/JS/CSS dark-themed chat UI served via Python's `http.server`. Calls backend at `localhost:8000`.

Key constraint: `gemini.md` is the **Project Constitution** — it defines data schemas, behavioral rules, and architectural invariants. Schema changes must be reflected there first.

## Commands

### Start everything (backend + frontend + Ollama check)
```bash
./start_system.sh
```
Note: `start_system.sh` expects a venv at `../.venv/bin/python`. Adjust `VENV_PYTHON` if your setup differs.

### Manual startup
```bash
# Backend (port 8000)
cd backend && pip install -r requirements.txt && uvicorn app:app --reload

# Frontend (port 3000)
cd frontend && python -m http.server 3000
```

### Run the test case generator standalone
```bash
python tools/generate_test_cases.py "As a user, I want to reset my password"
```

### Verify Ollama connectivity
```bash
python tools/verify_ollama.py
```

## Dependencies

Python 3.10+, Ollama with `llama3.2` model pulled (`ollama pull llama3.2`). Python packages: `fastapi`, `uvicorn`, `ollama`, `pydantic` (see `backend/requirements.txt`).

## Data Flow

1. User enters a user story in the chat UI
2. Frontend POSTs `{ "user_story": "...", "model": "llama3.2" }` to `localhost:8000/generate`
3. Backend calls `tools/generate_test_cases.py` which prompts Ollama with a system prompt (Senior QA Tester role) + the user story
4. Ollama returns JSON with `test_cases` array (each having id, title, preconditions, steps, expected_result, type) and a `summary`
5. Test case types: `Positive`, `Negative`, `EdgeCase`

## Key Design Rules

- **Local-first**: Only `localhost:11434` (Ollama) for inference. No external AI API calls.
- **Data-first**: Define JSON schemas in `gemini.md` before coding. The prompt template is fixed; users can only change the user story input, not the system instructions.
- **Planning files**: `task_plan.md` (phases/checklists), `findings.md` (research/constraints), `progress.md` (log of work done). Update these after meaningful changes.
