from app.services.story_cluster import cluster_stories
from app.services.entity_extractor import extract_entities
from app.services.story_title import generate_story_title
from app.services.impact_analysis import analyze_impact


def generate_deep_briefing(cluster_id):

    clusters = cluster_stories()

    if cluster_id not in clusters:
        return None

    stories = clusters[cluster_id]

    title = generate_story_title(stories)
    entities = extract_entities(stories)
    impact = analyze_impact(stories)

    summary = " ".join(stories[:3])[:500]

    briefing = {
        "title": title,
        "articles": len(stories),
        "summary": summary,
        "entities": entities[:5],
        "impact": impact
    }

    return briefing