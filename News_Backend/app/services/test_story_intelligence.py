from app.services.story_intelligence import ask_story_question
from app.services.story_cluster import cluster_stories


clusters = cluster_stories()

first_cluster = list(clusters.keys())[0]

print("Testing cluster:", first_cluster)

print()

print("Q: Why is this story important?")
print(ask_story_question(first_cluster,"why is this story important"))

print()

print("Q: What companies are involved?")
print(ask_story_question(first_cluster,"companies involved"))

print()

print("Q: What happened?")
print(ask_story_question(first_cluster,"what happened"))