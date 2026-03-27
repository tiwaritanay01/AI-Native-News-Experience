from app.services.llm_service import generate_llm_response
from app.services.story_cluster import cluster_stories


def generate_followup_questions(cluster_id_or_text):
    if isinstance(cluster_id_or_text, int):
        clusters = cluster_stories()
        articles = clusters.get(cluster_id_or_text, [])
        if not articles:
             return ["What more can you tell me?", "What are the next steps?", "Is there any related news?"]
        text = "\n\n".join(articles[:3])
    else:
        text = cluster_id_or_text

    prompt = f"""
    You are a news analyst.

    Based on the news story below, generate 3 intelligent follow-up questions
    that a reader might ask.

    News Story:
    {text}

    Return only the questions as a list.
    """

    return generate_llm_response(prompt)