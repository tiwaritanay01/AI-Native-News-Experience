from app.db.vector_db import collection
from app.services.embeddings import model
from app.services.story_cluster import clear_cluster_cache

def store_articles(articles):
    if not articles:
        return

    contents = [article.get("content", article.get("description", "No content available")) for article in articles]
    embeddings = model.encode(contents).tolist()
    
    ids = [str(i) for i in range(len(articles))]
    
    metadatas = []
    for article in articles:
        source_data = article.get("source", {})
        source_name = source_data.get("name", "Unknown Source") if isinstance(source_data, dict) else str(source_data)
        metadatas.append({
            "title": article.get("title", "No Title"),
            "source": source_name,
            "url": article.get("url", "")
        })

    collection.add(
        ids=ids,
        documents=contents,
        embeddings=embeddings,
        metadatas=metadatas
    )
    
    # Invalidate cluster cache as data changed
    clear_cluster_cache()