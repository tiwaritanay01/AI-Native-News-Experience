from transformers import pipeline

sentiment_model = pipeline(
    "sentiment-analysis",
    model="ProsusAI/finbert"
)

def analyze_sentiment(articles):

    results = sentiment_model(articles)

    positive = 0
    negative = 0
    neutral = 0

    for r in results:

        label = r["label"].lower()

        if label == "positive":
            positive += 1
        elif label == "negative":
            negative += 1
        else:
            neutral += 1

    total = len(results)

    return {
        "positive": round((positive / total) * 100, 2),
        "neutral": round((neutral / total) * 100, 2),
        "negative": round((negative / total) * 100, 2)
    }