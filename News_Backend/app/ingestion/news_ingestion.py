import feedparser
from sentence_transformers import SentenceTransformer
from app.db.vector_db import collection

model = SentenceTransformer("all-MiniLM-L6-v2")

RSS_FEEDS = [
    "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
    "https://feeds.bbci.co.uk/news/business/rss.xml",
]


def fetch_business_news():

    articles = []

    for feed_url in RSS_FEEDS:

        feed = feedparser.parse(feed_url)

        for entry in feed.entries:

            articles.append({
                "title": entry.title,
                "content": entry.get("summary", ""),
                "url": entry.link,
                "published": entry.get("published", "")   # NEW FIELD
            })

    return articles


def store_articles(articles):
    if not articles:
        return

    texts = [article["title"] + " " + article.get("content", "") for article in articles]
    embeddings = model.encode(texts).tolist()

    ids = [str(i) for i in range(len(articles))]
    metadatas = [{
        "url": article["url"],
        "published": article.get("published", "")
    } for article in articles]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas
    )


news = fetch_business_news()

store_articles(news)

print("Stored", len(news), "articles in vector DB")
print("Vector database saved.")