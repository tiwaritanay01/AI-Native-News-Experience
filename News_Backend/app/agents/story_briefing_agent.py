import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def generate_story_brief(text):
    prompt = f"""
Summarize this news story and provide:

1. Key Events
2. Why it matters
3. Market impact
4. What to watch next

News:
{text}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]