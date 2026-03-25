from fastapi import FastAPI
from app.api.news_api import app
from app.ingestion.news_ingestion import fetch_business_news
from app.services.store_articles import store_articles

@app.get("/ingest")
def ingest_news():
    articles = fetch_business_news()
    store_articles(articles)
    return {"status": "success", "message": "news stored"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
