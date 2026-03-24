from app.services.story_cluster import cluster_stories
from app.services.briefing_service import generate_story_briefing

def detect_story_of_the_day():

    clusters = cluster_stories()

    if not clusters:
        return {"error": "No stories available"}

    # Find cluster with most articles
    largest_cluster_id = max(clusters, key=lambda cid: len(clusters[cid]))

    articles = clusters[largest_cluster_id]

    briefing = generate_story_briefing(articles)

    return {
        "cluster_id": int(largest_cluster_id),
        "articles": len(articles),
        "briefing": briefing
    }