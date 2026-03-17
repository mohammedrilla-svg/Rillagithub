# Findings

## Research
- [x] Ollama API capabilities
    - **Tools**: `ollama` python library, REST API.
    - **Pattern**: System instructions + Few-shot prompting -> JSON output.
    - **Models**: Llama 3, DeepSeek, Code Llama (local).
- [x] Test case generation patterns
    - **Structure**: ID, Category, Preconditions, Steps, Expected Results.


## Constraints
- [x] Local environment only (Ollama)
- [ ] Hardware dependent (RAM/GPU for larger models)
- [ ] JSON schema enforcement (require strict prompting or output parsers)

