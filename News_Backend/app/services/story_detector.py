from sklearn.cluster import KMeans
import numpy as np
from app.db.vector_db import collection

def detect_story_of_day():

    results = collection.get(include=["embeddings","documents"])

    embeddings = results["embeddings"]
    docs = results["documents"]

    kmeans = KMeans(n_clusters=5)

    labels = kmeans.fit_predict(embeddings)

    cluster_counts = {}

    for label in labels:
        cluster_counts[label] = cluster_counts.get(label,0)+1

    biggest_cluster = max(cluster_counts, key=cluster_counts.get)

    story = []

    for i,label in enumerate(labels):
        if label == biggest_cluster:
            story.append(docs[i])

    return story[:5]