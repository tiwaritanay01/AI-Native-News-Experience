from vector_search import search_news

query = "Indian stock market crash"

results = search_news(query)

for doc in results["documents"][0]:
    print(doc)
    print()