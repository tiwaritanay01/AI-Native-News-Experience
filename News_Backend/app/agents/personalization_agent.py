from app.services.story_cluster import cluster_stories
import ollama


def get_personalized_feed(user_profile):

    clusters = cluster_stories()

    stories = []

    for cluster_id, articles in clusters.items():

        text = " ".join(articles[:3])

        prompt = f"""
You are a financial news assistant.

User profile: {user_profile}

Based on this news story, decide if it is relevant to the user.

Return:
1. relevance score (1–10)
2. short explanation

News:
{text}
"""

        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}]
        )

        stories.append({
            "cluster_id": cluster_id,
            "analysis": response["message"]["content"]
        })

    return stories