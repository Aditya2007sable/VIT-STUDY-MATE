import json
from database.database import get_connection
from modules.ai_client import ask_ai


def _clean_json(raw):
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1] if "\n" in raw else raw
        if raw.endswith("```"):
            raw = raw[:-3]
    return raw.strip()


def generate_quiz(module_title, text, count=5):
    count = max(3, min(int(count), 10))
    prompt = f"""Create exactly {count} multiple-choice questions from the uploaded module only.

Rules:
- Do not use outside knowledge.
- Each question has exactly four options.
- The answer must be A, B, C, or D.
- Questions should be suitable for a first-year engineering student.
- Return ONLY valid JSON; no markdown.
- Structure: {{"questions":[{{"question":"...","options":["...","...","...","..."],"answer":"A"}}]}}

Module: {module_title}

Uploaded module:
{text[:14000]}
"""
    raw, error = ask_ai(prompt)
    if error:
        print(error)
        return []
    try:
        data = json.loads(_clean_json(raw))
        valid = []
        for q in data.get("questions", []):
            answer = str(q.get("answer", "")).upper()
            options = q.get("options")
            if isinstance(q, dict) and isinstance(q.get("question"), str) and isinstance(options, list) and len(options) == 4 and answer in {"A", "B", "C", "D"}:
                valid.append({"question": q["question"], "options": [str(x) for x in options], "answer": answer})
        return valid[:count]
    except (json.JSONDecodeError, AttributeError, TypeError):
        print("OpenAI returned an invalid quiz format. Try again.")
        return []


def save_quiz_result(module, score, total):
    percentage = score / total * 100 if total else 0
    conn = get_connection()
    conn.execute("INSERT INTO quiz_results(module,score,total,percentage) VALUES(?,?,?,?)", (module, score, total, percentage))
    conn.commit()
    conn.close()
