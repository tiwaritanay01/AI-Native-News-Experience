from app.services.story_cluster import cluster_stories
from app.services.story_title import generate_story_title
from app.services.entity_extractor import extract_entities
from app.services.story_of_day import detect_story_of_day


clusters = cluster_stories()

for cid, stories in clusters.items():

    title = generate_story_title(stories)
    entities = extract_entities(stories)

    print()
    print("📰 STORY")
    print("Title:", title)
    print("Articles:", len(stories))
    print("Entities:", entities[:5])
    print()


print("🔥 STORY OF THE DAY")

cid, stories = detect_story_of_day()

print("Cluster:", cid)
print("Articles:", len(stories))      