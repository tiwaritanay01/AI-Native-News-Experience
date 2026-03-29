from app.services.story_cluster import cluster_stories
from app.services.story_title import generate_story_title
from app.services.entity_extractor import extract_entities
from app.services.impact_service import analyze_story_impact as analyze_impact

def get_all_stories():

    clusters = cluster_stories()

    stories = []

    for cid, articles in clusters.items():

        title = generate_story_title(articles)
        entities = extract_entities(articles)
        impact = analyze_impact(articles)


        story = {
            "cluster_id": int(cid),
            "title": title,
            "articles": len(articles),
            "entities": entities[:5],
            "impact": impact
        }

        stories.append(story)

    return stories