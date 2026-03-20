# from sklearn.cluster import KMeans
# import chromadb
# from chromadb.config import Settings


# client = chromadb.Client(
#     chromadb.config.Settings(
#         persist_directory="vector_db"
#     )
# )
# collection = client.get_or_create_collection("news")


# def cluster_stories(num_clusters=5):

#     data = collection.get(include=["embeddings", "documents"])

#     embeddings = data["embeddings"]
#     docs = data["documents"]

#     kmeans = KMeans(n_clusters=num_clusters)

#     labels = kmeans.fit_predict(embeddings)

#     clusters = {}

#     for label, doc in zip(labels, docs):
#         clusters.setdefault(label, []).append(doc)

#     return clusters

# from sklearn.cluster import KMeans
# import numpy as np
# from app.db.vector_db import collection


# def cluster_stories():

#     results = collection.get(
#         include=["embeddings", "documents"],
#         limit=1000
#     )
#     print(results.keys())
#     print("Embeddings:", results["embeddings"])
#     print("Documents:", len(results["documents"]))

#     embeddings = results["embeddings"]
#     docs = results["documents"]

#     if embeddings is None or len(embeddings) == 0:
#         print("No embeddings found in database.")
#         return {}

#     embeddings = np.array(embeddings)

#     if embeddings.ndim == 1:
#         embeddings = embeddings.reshape(1, -1)

#     kmeans = KMeans(n_clusters=5)

#     labels = kmeans.fit_predict(embeddings)

#     clusters = {}

#     for i, label in enumerate(labels):
#         clusters.setdefault(label, []).append(docs[i])

#     return clusters

from app.db.vector_db import collection
import numpy as np
import hdbscan


def cluster_stories():

    results = collection.get(
        include=["documents", "embeddings"]
    )

    embeddings = results["embeddings"]
    docs = results["documents"]

    if embeddings is None or len(embeddings) == 0:
        print("No embeddings found in database.")
        return {}

    embeddings = np.array(embeddings)

    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=5,
        metric="euclidean"
    )

    labels = clusterer.fit_predict(embeddings)

    clusters = {}

    for i, label in enumerate(labels):

        if label == -1:
            continue

        clusters.setdefault(label, []).append(docs[i])

    return clusters