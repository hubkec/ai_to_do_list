import requests
import re
import json

OLLAMA_URL = "http://localhost:11434/api/generate"


def build_prompt(user_input):
    return f"""
Sei un assistente per una to-do list.

Rispondi SOLO con JSON valido.

Formato:
{{
  "action":"create|delete|toggle|list|unknown",
  "title":"string|null",
  "completed": true | false | null
}}

Regole:
- "cancella", "elimina" → delete
- "completa", "segna come fatto" → toggle (completed = true)
- "riapri", "non completato" → toggle (completed = false)

Esempi:

Input: cancella latte
Output: {{"action":"delete","title":"latte"}}

Input: completa latte
Output: {{"action":"toggle","title":"latte"}}

Input: riapri latte
Output: {{"action":"toggle","title":"latte"}}

---

Input: {user_input}
Output:
"""


def ask_ollama(prompt):
    res = requests.post(
        OLLAMA_URL,
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )
    return res.json()["response"]


def extract_json(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return {"action": "unknown", "title": None}

    try:
        return json.loads(match.group(0))
    except:
        return {"action": "unknown", "title": None}


def process_input(user_input):
    prompt = build_prompt(user_input)
    raw = ask_ollama(prompt)
    data = extract_json(raw)
    return data