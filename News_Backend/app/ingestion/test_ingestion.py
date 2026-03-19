import feedparser

RSS_FEEDS = [
    "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
    "https://feeds.reuters.com/reuters/businessNews",
    "https://feeds.bbci.co.uk/news/business/rss.xml"
]

def fetch_business_news():

    articles = []

    for feed_url in RSS_FEEDS:

        feed = feedparser.parse(feed_url)

        for entry in feed.entries:

            articles.append({
                "title": entry.title,
                "content": entry.get("summary", ""),
                "source": feed.feed.get("title", "Unknown"),
                "url": entry.link
            })

    return articles


news = fetch_business_news()

for article in news[:10]:
    print(article["title"])
    print(article["source"])
    print(article["url"])
    print()