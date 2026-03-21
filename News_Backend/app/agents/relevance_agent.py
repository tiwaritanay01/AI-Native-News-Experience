from app.services.story_cluster import cluster_stories
import ollama


def explain_relevance(cluster_id, user_profile):

    clusters = cluster_stories()

    story = clusters.get(cluster_id)

    if not story:
        return {"error": "Story not found"}

    text = " ".join(story[:3])

    prompt = f"""
Explain why this news story matters to a {user_profile}.

Story:
{text}

Return concise bullet points.
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "cluster_id": cluster_id,
        "user_profile": user_profile,
        "explanation": response["message"]["content"]
    }