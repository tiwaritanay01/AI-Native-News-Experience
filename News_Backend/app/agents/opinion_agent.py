from app.services.story_cluster import cluster_stories
from app.services.opinion_service import detect_contrarian_opinions


def get_contrarian_opinions(cluster_id):

    clusters = cluster_stories()
    articles = clusters.get(cluster_id, [])
    if not articles:
        articles = clusters.get(str(cluster_id), [])
        
    if not articles:
        return {
            "cluster_id": cluster_id,
            "contrarian_views": ["Awaiting narrative saturation for contrasting intelligence.", "Neutral-to-positive signals dominating current node."]
        }

    articles = articles

    opinions = detect_contrarian_opinions(articles)

    return {
        "cluster_id": cluster_id,
        "contrarian_views": opinions
    }
    