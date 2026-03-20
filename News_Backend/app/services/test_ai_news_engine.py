from app.services.story_cluster import cluster_stories
from app.services.story_title import generate_story_title
from app.services.entity_extractor import extract_entities
from app.services.impact_analysis import analyze_impact
from app.services.story_timeline import generate_timeline
from app.services.personalization import personalize_feed


clusters = cluster_stories()

print("\nAI NEWS ENGINE\n")

for cid, stories in clusters.items():

    title = generate_story_title(stories)
    entities = extract_entities(stories)
    impact = analyze_impact(stories)
    timeline = generate_timeline(stories)

    print("📰 STORY")
    print("Title:", title)
    print("Articles:", len(stories))
    print("Entities:", entities[:5])
    print("Impact:", impact)

    print("Timeline:")
    for t in timeline:
        print("-", t["event"])

    print()


print("\nPERSONALIZED FEED (Investor)\n")

feed = personalize_feed(clusters, "investor")

for cid, stories in feed:

    title = generate_story_title(stories)

    print("📈", title, "-", len(stories), "articles")