from app.db.vector_db import collection

results = collection.get(
    include=["documents", "embeddings"],
    limit=10
)

docs = results["documents"]
emb = results["embeddings"]

print("Documents:", 0 if docs is None else len(docs))
print("Embeddings:", 0 if emb is None else len(emb))