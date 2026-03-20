from app.services.story_cluster import cluster_stories
from app.services.story_title import generate_story_title
from app.services.entity_extractor import extract_entities
from app.services.impact_analysis import analyze_impact
from app.services.story_timeline import generate_timeline
from app.services.debate_generator import generate_debate
from app.services.briefing_service import generate_story_briefing


def get_story_intelligence(cluster_id):

    clusters = cluster_stories()

    if cluster_id not in clusters:
        return {"error": "Story not found"}

    stories = clusters[cluster_id]

    briefing = generate_story_briefing(stories)

    entities = extract_entities(stories)
    impact = analyze_impact(stories)

    result = {
        "cluster_id": cluster_id,
        "briefing": briefing,
        "entities": entities[:5],
        "impact": impact,
        "articles": len(stories)
    }

    return result