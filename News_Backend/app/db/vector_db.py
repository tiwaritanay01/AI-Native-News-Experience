import chromadb

# persistent database stored in project folder
client = chromadb.PersistentClient(path="vector_db")

collection = client.get_or_create_collection(
    name="news"
)