from app.services.story_cluster import cluster_stories
from app.services.story_title import generate_story_title
from app.services.entity_extractor import extract_entities
from app.services.impact_analysis import analyze_impact
from app.services.story_timeline import generate_timeline
from app.services.debate_generator import generate_debate


def get_story_intelligence(cluster_id):

    clusters = cluster_stories()

    if cluster_id not in clusters:
        return {"error": "Story not found"}

    stories = clusters[cluster_id]

    title = generate_story_title(stories)
    entities = extract_entities(stories)
    impact = analyze_impact(stories)
    timeline = generate_timeline(stories)
    debate = generate_debate(stories)

    summary = " ".join(stories[:3])[:500]

    result = {
        "cluster_id": cluster_id,
        "title": title,
        "summary": summary,
        "entities": entities[:5],
        "impact": impact,
        "timeline": timeline,
        "debate": debate,
        "articles": len(stories)
    }

    return result