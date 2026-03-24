import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

def generate_llm_response(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "No response from AI.")
    except Exception as e:
        print(f"LLM Error: {e}")
        return f"Error connecting to AI service: {str(e)}"