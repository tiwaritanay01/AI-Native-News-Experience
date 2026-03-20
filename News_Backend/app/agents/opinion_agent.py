from app.services.story_cluster import cluster_stories
from app.services.opinion_service import detect_contrarian_opinions


def get_contrarian_opinions(cluster_id):

    clusters = cluster_stories()

    if cluster_id not in clusters:
        return {"error": "Story not found"}

    articles = clusters[cluster_id]

    opinions = detect_contrarian_opinions(articles)

    return {
        "cluster_id": cluster_id,
        "contrarian_views": opinions
    }
    