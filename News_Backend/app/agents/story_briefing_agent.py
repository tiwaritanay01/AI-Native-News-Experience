from app.services.llm_service import generate_llm_response
from app.services.story_cluster import cluster_stories


def generate_story_brief(cluster_id_or_text):
    if isinstance(cluster_id_or_text, int):
        clusters = cluster_stories()
        articles = clusters.get(cluster_id_or_text, [])
        if not articles:
             return "No briefing available for this cluster."
        text = "\n\n".join(articles[:3])
    else:
        text = cluster_id_or_text

    prompt = f"""
Summarize this news story and provide:

1. Key Events
2. Why it matters
3. Market impact
4. What to watch next

News:
{text}
"""
    return generate_llm_response(prompt)