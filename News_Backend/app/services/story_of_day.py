from app.services.story_cluster import cluster_stories

def detect_story_of_day():

    clusters = cluster_stories()

    biggest_cluster = max(clusters.items(), key=lambda x: len(x[1]))

    cluster_id = biggest_cluster[0]
    stories = biggest_cluster[1]

    return cluster_id, stories