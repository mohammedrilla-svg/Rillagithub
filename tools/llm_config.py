"""
LLM Configuration - Change your model provider here.
Supported providers: "ollama", "claude", "gemini"
"""

import os
import json
import requests
import time

# --- CHANGE THESE SETTINGS ---
LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "ollama")  # "ollama", "claude", or "gemini"
LLM_MODEL = os.environ.get("LLM_MODEL", "llama3.2")
# --- END SETTINGS ---

# Provider configurations
PROVIDERS = {
    "ollama": {
        "url": os.environ.get("OLLAMA_API_URL", "http://localhost:11434"),
        "requires_key": False,
    },
    "claude": {
        "url": os.environ.get("CLAUDE_API_URL", "https://api.anthropic.com/v1/messages"),
        "key_env": "ANTHROPIC_API_KEY",
        "requires_key": True,
    },
    "gemini": {
        "url": os.environ.get("GEMINI_API_URL", "https://generativelanguage.googleapis.com/v1beta/models"),
        "key_env": "GEMINI_API_KEY",
        "requires_key": True,
    },
}


def get_api_key():
    """Get the API key for the current provider."""
    provider = PROVIDERS.get(LLM_PROVIDER)
    if not provider:
        return None, f"Unknown provider: {LLM_PROVIDER}"
    if not provider["requires_key"]:
        return None, None
    key = os.environ.get(provider["key_env"], "")
    if not key:
        return None, f"{provider['key_env']} environment variable is not set"
    return key, None


def call_llm(system_prompt, user_prompt):
    """
    Call the configured LLM provider.
    Returns: dict with response text or error.
    """
    if LLM_PROVIDER == "ollama":
        return _call_ollama(system_prompt, user_prompt)
    elif LLM_PROVIDER == "claude":
        return _call_claude(system_prompt, user_prompt)
    elif LLM_PROVIDER == "gemini":
        return _call_gemini(system_prompt, user_prompt)
    else:
        return {"error": f"Unknown provider: {LLM_PROVIDER}. Use 'ollama', 'claude', or 'gemini'."}


def _call_ollama(system_prompt, user_prompt):
    try:
        import ollama
        response = ollama.generate(
            model=LLM_MODEL,
            system=system_prompt,
            prompt=user_prompt,
            format='json',
            stream=False
        )
        return {"text": response['response']}
    except Exception as e:
        return {"error": str(e)}


def _call_claude(system_prompt, user_prompt):
    api_key, err = get_api_key()
    if err:
        return {"error": err}

    url = PROVIDERS["claude"]["url"]
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    payload = {
        "model": LLM_MODEL,
        "max_tokens": 4096,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_prompt}],
    }

    return _request_with_retry(url, headers, payload, "claude")


def _call_gemini(system_prompt, user_prompt):
    api_key, err = get_api_key()
    if err:
        return {"error": err}

    url = f"{PROVIDERS['gemini']['url']}/{LLM_MODEL}:generateContent?key={api_key}"
    headers = {"content-type": "application/json"}
    payload = {
        "system_instruction": {"parts": [{"text": system_prompt}]},
        "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
        "generationConfig": {"responseMimeType": "application/json"},
    }

    return _request_with_retry(url, headers, payload, "gemini")


def _request_with_retry(url, headers, payload, provider):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=60)

            if response.status_code == 429:
                retry_after = int(response.headers.get("retry-after", 5))
                time.sleep(retry_after)
                continue

            if response.status_code >= 500:
                time.sleep(2 ** attempt)
                continue

            if response.status_code != 200:
                error_body = response.json().get("error", {})
                return {"error": f"API error {response.status_code}: {error_body.get('message', response.text)}"}

            data = response.json()

            # Extract text based on provider response format
            if provider == "claude":
                return {"text": data["content"][0]["text"]}
            elif provider == "gemini":
                return {"text": data["candidates"][0]["content"]["parts"][0]["text"]}

        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            return {"error": "Request timed out after multiple attempts"}
        except requests.exceptions.ConnectionError:
            return {"error": f"Cannot connect to {provider} API. Check your connection."}
        except Exception as e:
            return {"error": str(e)}

    return {"error": "Failed after multiple retries"}
