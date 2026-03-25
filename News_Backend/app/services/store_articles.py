from app.db.vector_db import collection
from app.services.embeddings import generate_embedding

def store_articles(articles):
    for i, article in enumerate(articles):
        # Use .get() to avoid KeyErrors if fields are missing
        content = article.get("content", article.get("description", "No content available"))
        title = article.get("title", "No Title")
        url = article.get("url", "")
        
        # Safely handle the 'source' field which is often a dict
        source_data = article.get("source", {})
        source_name = source_data.get("name", "Unknown Source") if isinstance(source_data, dict) else str(source_data)
        
        # Generate embedding for the content
        embedding = generate_embedding(content)

        collection.add(
            ids=[str(i)],
            documents=[content],
            embeddings=[embedding],
            metadatas=[{
                "title": title,
                "source": source_name,
                "url": url
            }]
        )