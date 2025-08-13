import os
import requests

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

def chat_with_llm(user_message: str) -> str:
    if not OPENAI_API_KEY:
        raise RuntimeError("Missing OPENAI_API_KEY")

    # Minimal, readable payload; keep it simple.
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    body = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "You are a concise, helpful assistant."},
            {"role": "user", "content": user_message},
        ],
        "temperature": 0.7,
    }

    try:
        resp = requests.post(url, json=body, headers=headers, timeout=30)
    except requests.RequestException:
        raise RuntimeError("Network error talking to the model provider")

    if resp.status_code == 401:
        raise RuntimeError("Invalid or missing API key")
    if not resp.ok:
        raise RuntimeError(f"Provider error ({resp.status_code})")

    data = resp.json()
    # Defensive access; provider schemas can vary.
    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError):
        raise RuntimeError("Unexpected provider response format")
