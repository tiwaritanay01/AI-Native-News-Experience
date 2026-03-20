from app.services.story_cluster import cluster_stories
from app.services.deep_briefing import generate_deep_briefing
from app.services.entity_extractor import extract_entities
from app.services.impact_analysis import analyze_impact


def get_story_briefing(cluster_id):

    clusters = cluster_stories()

    if cluster_id not in clusters:
        return {"error": "Story not found"}

    stories = clusters[cluster_id]

    briefing = generate_deep_briefing(cluster_id)

    entities = extract_entities(stories)
    impact = analyze_impact(stories)

    result = {
        "cluster_id": cluster_id,
        "title": briefing["title"],
        "articles": briefing["articles"],
        "summary": briefing["summary"],
        "entities": entities[:5],
        "impact": impact
    }

    return result