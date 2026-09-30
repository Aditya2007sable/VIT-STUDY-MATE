import os
from dotenv import load_dotenv

load_dotenv()


def get_client():
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None, "OPENAI_API_KEY is not configured. Add it to .env."
    try:
        from openai import OpenAI
        return OpenAI(api_key=api_key), None
    except ImportError:
        return None, "OpenAI SDK is not installed. Run: python -m pip install -U openai"


def ask_ai(prompt):
    client, error = get_client()
    if error:
        return None, error
    model = os.getenv("OPENAI_MODEL", "gpt-6-luna").strip() or "gpt-6-luna"
    try:
        response = client.responses.create(model=model, input=prompt)
        return response.output_text.strip(), None
    except Exception as exc:
        return None, f"OpenAI request failed: {exc}"
