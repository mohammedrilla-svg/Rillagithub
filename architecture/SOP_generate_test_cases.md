# SOP: Generate Test Cases

## Goal
To transform a raw User Story string into a structured JSON list of test cases using the local Ollama `llama3.2` model.

## Inputs
1.  `user_story` (string): The description of the feature to be tested.
2.  `model` (string): Default `llama3.2`.

## Tool Logic
1.  **Validation**: Ensure `user_story` is not empty.
2.  **Prompt Assembly**:
    *   System Prompt: Define Role (QA Senior Manual Tester) and Constraint (JSON Only).
    *   User Prompt: Inject `user_story` into the template.
    *   Schema Enforcement: Explicitly request the JSON schema defined in `gemini.md`.
3.  **Execution**: Call `ollama.generate()` via the `tools/generate_test_cases.py` script.
4.  **Parsing**:
    *   Extract valid JSON from the response.
    *   If JSON is malformed, attempting a retry (optional) or failing gracefully.
5.  **Output**: Return the JSON object to the caller.

## Edge Cases
- **Ollama Down**: Return 503 error.
- **Model not found**: Return 500 error specifying model name.
- **Empty User Story**: Return 400 Bad Request.
- **Hallucinated Format**: If model returns Markdown/text instead of JSON, attempt to strip fences.
