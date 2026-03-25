from fastapi import FastAPI
from app.ingestion.news_ingestion import fetch_business_news
from app.services.store_articles import store_articles
from app.services.story_detector import detect_story_of_the_day

app = FastAPI()

@app.get("/")
def home():
    return {"status": "success", "message": "AI-Native News Backend is Online"}

@app.get("/ingest")
def ingest_news():
    articles = fetch_business_news()
    store_articles(articles)
    return {"message":"news stored"}

@app.get("/story-of-day")
def story():
    story = detect_story_of_the_day()
    return {"story": story}
