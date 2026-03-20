from app.services.story_cluster import cluster_stories
from app.services.story_title import generate_story_title
from app.services.entity_extractor import extract_entities
from app.services.impact_analysis import analyze_impact


def get_story_intelligence():

    clusters = cluster_stories()

    results = []

    for cid, stories in clusters.items():

        title = generate_story_title(stories)
        entities = extract_entities(stories)
        impact = analyze_impact(stories)

        results.append({
            "cluster_id": cid,
            "title": title,
            "articles": len(stories),
            "entities": entities[:5],
            "impact": impact
        })

    return results