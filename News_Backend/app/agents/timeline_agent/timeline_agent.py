from app.services.story_cluster import cluster_stories
from app.services.timeline_service import build_story_timeline


import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def generate_story_timeline(text):
    prompt = f"""
Extract the major events from this news story in chronological order.

Return a simple timeline.

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