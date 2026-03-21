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

    for i, article in enumerate(articles):

        text = article["title"] + " " + article["content"]

        embedding = model.encode(text).tolist()

        collection.add(
            ids=[str(i)],
            embeddings=[embedding],
            documents=[text],
            metadatas=[{
                "url": article["url"],
                "published": article["published"]   # NEW METADATA
            }]
        )


news = fetch_business_news()

store_articles(news)

print("Stored", len(news), "articles in vector DB")
print("Vector database saved.")