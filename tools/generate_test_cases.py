import sys
import json
from tools.llm_config import call_llm


def generate_test_cases(user_story):
    """
    Generates test cases from a user story using the configured LLM.
    Returns: JSON object (dict)
    """
    if not user_story:
        return {"error": "User story cannot be empty"}

    system_prompt = """
    ROLE: You are a Senior QA Engineer with 15+ years of experience.
    Your output must be strict valid JSON only. No markdown, no explanatory text, no code fences.

    TASK: Generate comprehensive test cases from the provided input.

    COVERAGE AREAS:
    Follow these principles when generating test cases:
    1. Requirement-driven, not implementation-driven - Test cases must map directly to requirements, not implementation details
    2. Complete coverage:
        - Functional (happy path)
        - Negative scenarios
        - Boundary values
        - Edge cases
    3. Clear and actionable - Each test case must be executable by a QA engineer without ambiguity
    4. Traceable - Maintain clear mapping between requirements and test cases

    For each requirement, identify:
    - Preconditions (what must be true before testing)
    - Test steps (actions to perform)
    - Expected results (what should happen)

    CONSTRAINTS:
    - Use ONLY the provided content
    - No assumptions about unmentioned features
    - Mark unclear items as "Needs clarification"
    - Do NOT invent error messages or codes

    FORMAT:
    Structure your response exactly like this:
    {
      "test_cases": [
        {
          "id": "TC_001",
          "title": "Short title",
          "preconditions": "Preconditions here",
          "steps": ["Step 1", "Step 2"],
          "expected_result": "Expected result",
          "type": "Functional"
        }
      ],
      "summary": "Brief summary"
    }

    The "type" field must be exactly one of these values: "Functional", "Negative", "Boundary", "Edge Case"
    """

    user_prompt = f"""
    Analyze the following input and generate comprehensive test cases.

    Input: "{user_story}"
    """

    result = call_llm(system_prompt, user_prompt)

    if "error" in result:
        return result

    # Parse the LLM response text into JSON
    try:
        return json.loads(result["text"])
    except json.JSONDecodeError:
        clean_text = result["text"].replace("```json", "").replace("```", "").strip()
        try:
            return json.loads(clean_text)
        except json.JSONDecodeError:
            return {"error": "LLM returned invalid JSON response"}


if __name__ == "__main__":
    if len(sys.argv) > 1:
        story = " ".join(sys.argv[1:])
        result = generate_test_cases(story)
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps({"error": "No user story provided as argument"}))
