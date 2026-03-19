from app.db.vector_db import collection
from app.services.embeddings import generate_embedding

def store_articles(articles):

    for i, article in enumerate(articles):

        embedding = generate_embedding(article["content"])

        collection.add(
            ids=[str(i)],
            documents=[article["content"]],
            embeddings=[embedding],
            metadatas=[{
                "title": article["title"],
                "source": article["source"],
                "url": article["url"]
            }]
        )