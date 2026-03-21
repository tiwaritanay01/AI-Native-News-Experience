from app.services.story_cluster import cluster_stories
from app.services.sentiment_service import analyze_sentiment


def get_story_sentiment(cluster_id):

    clusters = cluster_stories()

    if cluster_id not in clusters:
        return {"error": "Story not found"}

    articles = clusters[cluster_id]

    sentiment = analyze_sentiment(articles[:20])

    return {
        "cluster_id": cluster_id,
        "sentiment": sentiment
    }