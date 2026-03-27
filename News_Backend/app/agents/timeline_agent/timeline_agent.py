from app.services.story_cluster import cluster_stories
from app.services.timeline_service import build_story_timeline
from app.services.llm_service import generate_llm_response


def generate_story_timeline(cluster_id_or_text):
    if isinstance(cluster_id_or_text, int):
        clusters = cluster_stories()
        articles = clusters.get(cluster_id_or_text, [])
        if not articles:
             return "No timeline available for this cluster."
        text = "\n\n".join(articles[:3])
    else:
        text = cluster_id_or_text

    prompt = f"""
Extract the major events from this news story in chronological order.

Return a simple timeline.

News:
{text}
"""
    return generate_llm_response(prompt)