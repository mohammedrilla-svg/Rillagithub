# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Smart Test Case Generator — an AI-powered tool that generates structured QA test cases from user stories or PRD documents. Supports multiple LLM providers (Claude, Gemini, Ollama) configurable via a single `.env` file.

## Architecture

- **Frontend** (`frontend/index.html`): Vanilla HTML/JS/CSS dark-themed chat UI. Supports text input, file upload (PDF, Word, Excel), and export (Excel, CSV).
- **Backend** (`backend/app.py`): FastAPI app with two endpoints — `POST /generate` for text input, `POST /upload` for file uploads, `GET /health` for status.
- **Tools** (`tools/`):
  - `generate_test_cases.py` — Core tool that builds the QA prompt and calls the configured LLM
  - `llm_config.py` — Generic LLM provider config supporting Claude, Gemini, and Ollama
  - `extract_text.py` — Extracts text from PDF (pdfplumber), Word (python-docx), Excel (openpyxl)
- **Config** (`.env`): Single file to switch LLM provider, model, API keys, and endpoint URLs

## Commands

### Start the system
```bash
./start_system.sh
```

### Manual startup
```bash
# Backend (port 8000)
cd backend && pip install -r requirements.txt && uvicorn app:app --reload

# Frontend (port 3000)
cd frontend && python -m http.server 3000
```

### Stop servers
```bash
lsof -ti:8000 -ti:3000 | xargs kill -9
```

## LLM Configuration

All LLM settings are in `.env` (see `.env.example`):

```bash
# Claude
LLM_PROVIDER=claude
LLM_MODEL=claude-opus-4-6
ANTHROPIC_API_KEY=your-key

# Gemini
LLM_PROVIDER=gemini
LLM_MODEL=gemini-2.0-flash
GEMINI_API_KEY=your-key

# Ollama (local)
LLM_PROVIDER=ollama
LLM_MODEL=llama3.2
```

No code changes needed to switch providers — just update `.env` and restart.

## Dependencies

Python 3.10+. Packages: `fastapi`, `uvicorn`, `requests`, `pydantic`, `python-dotenv`, `python-multipart`, `pdfplumber`, `python-docx`, `openpyxl` (see `backend/requirements.txt`).

## Data Flow

1. User enters a user story or uploads a PRD file (PDF/Word/Excel)
2. For file uploads: `extract_text.py` extracts text content
3. Text is sent to `generate_test_cases.py` which builds a QA prompt
4. `llm_config.py` routes the request to the configured LLM provider
5. LLM returns JSON with `test_cases` array (id, title, preconditions, steps, expected_result, type)
6. Test case types: Functional, Negative, Boundary, Edge Case
7. Frontend renders color-coded cards; user can export to Excel or CSV

## Key Design Decisions

- **No Anthropic SDK** — Claude API calls use raw HTTP via `requests` library
- **Single config file** — `.env` controls all LLM settings
- **Client-side export** — Excel/CSV export runs in browser using SheetJS, no backend needed
