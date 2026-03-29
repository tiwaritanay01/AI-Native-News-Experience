import json
from app.services.story_cluster import cluster_stories
from app.services.impact_service import analyze_story_impact


def get_story_impact(cluster_id):

    clusters = cluster_stories()
    articles = clusters.get(cluster_id, [])
    if not articles:
        articles = clusters.get(str(cluster_id), [])
        
    if not articles:
        return {
            "cluster_id": cluster_id,
            "impact": {"market": "Stable", "sentiment": "Neutral", "sectors": ["Global Trade"]}
        }

    articles = articles

    impact = analyze_story_impact(articles)

    try:
        impact_json = json.loads(impact)
    except:
        impact_json = {"raw": impact}

    return {
        "cluster_id": cluster_id,
        "impact": impact_json
    }