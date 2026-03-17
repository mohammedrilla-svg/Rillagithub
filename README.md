# Smart Test Case Generator

An AI-powered tool that generates comprehensive QA test cases from User Stories or PRD documents. Supports multiple LLM providers (Claude, Gemini, Ollama) — configurable via a single `.env` file.

## Features

*   **Multi-LLM Support**: Switch between Claude, Gemini, or Ollama by changing `.env`
*   **File Upload**: Upload PRD documents (PDF, Word, Excel) to generate test cases
*   **Export**: Download test cases as Excel (.xlsx) or CSV
*   **Structured Output**: JSON test cases with Functional, Negative, Boundary, and Edge Case categorization
*   **Dark-themed UI**: Chat-like interface for easy interaction

## Quick Start

### 1. Clone and Install
```bash
git clone https://github.com/mohammedrilla-svg/Rillagithub.git
cd Rillagithub
pip install -r backend/requirements.txt
```

### 2. Configure LLM Provider
Copy `.env.example` to `.env` and set your provider:

```bash
cp .env.example .env
```

**For Claude:**
```
LLM_PROVIDER=claude
LLM_MODEL=claude-opus-4-6
ANTHROPIC_API_KEY=your-key-here
```

**For Gemini:**
```
LLM_PROVIDER=gemini
LLM_MODEL=gemini-2.0-flash
GEMINI_API_KEY=your-key-here
```

**For Ollama (local, free):**
```
LLM_PROVIDER=ollama
LLM_MODEL=llama3.2
```
Requires [Ollama](https://ollama.com/) installed with `ollama pull llama3.2`.

### 3. Start the System
```bash
./start_system.sh
```

*   **Frontend**: http://localhost:3000
*   **Backend**: http://localhost:8000

## Project Structure

```
├── backend/app.py              # FastAPI backend (/generate, /upload, /health)
├── frontend/index.html         # Chat UI with file upload and export
├── tools/
│   ├── generate_test_cases.py  # Core test case generation logic
│   ├── llm_config.py           # Multi-LLM provider configuration
│   └── extract_text.py         # PDF, Word, Excel text extraction
├── .env.example                # LLM config template
└── start_system.sh             # One-command startup script
```

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | Vanilla HTML + CSS + JavaScript |
| Backend | Python + FastAPI |
| LLM | Claude API / Gemini API / Ollama (configurable) |
| File Parsing | pdfplumber, python-docx, openpyxl |
| Excel Export | SheetJS (client-side) |
