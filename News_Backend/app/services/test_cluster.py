from app.services.story_cluster import cluster_stories

clusters = cluster_stories()

for cluster, stories in clusters.items():
    print("CLUSTER", cluster)
    print(len(stories), "articles")
    print()