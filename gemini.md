# Project Constitution

## Data Schemas

### 1. Test Case Object
```json
{
  "id": "TC_001",
  "title": "Short description of the test",
  "preconditions": "What needs to be true before starting",
  "steps": [
    "Step 1: Action",
    "Step 2: Action"
  ],
  "expected_result": "What should happen",
  "type": "Positive|Negative|EdgeCase"
}
```

### 2. Application Payload (Input)
```json
{
  "user_story": "The raw input from the user describing the feature.",
  "model": "llama3.2"
}
```

### 3. Application Payload (Output)
```json
{
  "test_cases": [
    { "ref": "#Test Case Object" }
  ],
  "summary": "Brief summary of generated coverage."
}
```

## Behavioral Rules
1. **Role**: The AI acts as a Senior QA Manual Tester.
2. **Determinism**: Always output valid JSON. If the model fails to output JSON, retry or show a raw error.
3. **Template Adherence**: The `PromptTemplate` stored in the code must always be used; do not allow the user to override the *instruction*, only the *context* (User Story).
4. **Tone**: Professional, precise, and technical.

## Architectural Invariants
1. **Local-First**: No external API calls (OpenAI/Anthropic) allowed. Only `localhost:11434` (Ollama).
2. **Separation of Concerns**: 
    - **Frontend**: Handles User Input & Displaying Results (HTML/JS/CSS).
    - **Backend**: Handles Prompt Assembly & Ollama Communication (Python/FastAPI).
