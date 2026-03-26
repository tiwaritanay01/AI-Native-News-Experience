from app.services.story_cluster import cluster_stories
from app.services.timeline_service import build_story_timeline
from app.services.llm_service import generate_llm_response


def generate_story_timeline(text):
    prompt = f"""
Extract the major events from this news story in chronological order.

Return a simple timeline.

News:
{text}
"""
    return generate_llm_response(prompt)