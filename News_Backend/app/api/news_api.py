from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from app.agents.story_agent import get_all_stories
from app.agents.briefing_agent import get_story_briefing
from app.agents.qa_agent import answer_story_question
from app.agents.intelligence_agent import get_story_intelligence
from app.agents.story_of_day_agent import get_story_of_the_day
from app.agents.question_agent import get_story_questions
from app.agents.question_answer_agent import answer_question
from app.agents.debate_agent import start_debate, next_turn, end_debate, ask_debate_question
from app.agents.opinion_agent import get_contrarian_opinions
from app.agents.impact_agent import get_story_impact
from app.agents.timeline_agent.timeline_agent import generate_story_timeline
from app.agents.sentiment_agent import get_story_sentiment
from app.agents.dashboard_agent import generate_dashboard
from app.api.story_routes import router as story_router

# New Engines
from app.services.video_service import video_service
from app.services.translation_service import translation_service
from app.services.market_service import market_service

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,
)

app.include_router(story_router)

@app.get("/story-of-day")
def story_of_day():
    return get_story_of_the_day()

@app.get("/stories")
def stories():
    return get_all_stories()

@app.get("/story/{cluster_id}")
def story(cluster_id: int):
    return get_story_briefing(cluster_id)

@app.get("/story/{cluster_id}/intelligence")
def story_intelligence(cluster_id: int):
    return get_story_intelligence(cluster_id)

@app.post("/ask")
def ask(data: dict):
    cluster_id = data["cluster_id"]
    question = data["question"]
    return answer_story_question(cluster_id, question)

@app.get("/story/{cluster_id}/briefing")
def story_briefing(cluster_id: int):
    return get_story_briefing(cluster_id)

@app.get("/story/{cluster_id}/questions")
def story_questions(cluster_id: int):
    return get_story_questions(cluster_id)

@app.get("/story/{cluster_id}/opinions")
def story_opinions(cluster_id: int):
    return get_contrarian_opinions(cluster_id)

@app.get("/story/{cluster_id}/impact")
def story_impact(cluster_id: int):
    return get_story_impact(cluster_id)

@app.get("/story/{cluster_id}/timeline")
def story_timeline(cluster_id: int):
    return generate_story_timeline(cluster_id)

@app.get("/story/{cluster_id}/sentiment")
def story_sentiment(cluster_id: int):
    return get_story_sentiment(cluster_id)

@app.get("/story/{cluster_id}/dashboard")
def story_dashboard(cluster_id: int):
    return generate_dashboard(cluster_id)

# ─── Cinematic & Vernacular Engines ────────────────────────────────

@app.get("/api/story/{cluster_id}/video")
def get_story_video(cluster_id: int):
    """Generates cinematic video frames/metadata using Hugging Face."""
    briefing = get_story_briefing(cluster_id)
    # The briefing agent returns a dict, we extract summary
    summary = briefing.get("summary", "A breaking news story.") if isinstance(briefing, dict) else str(briefing)
    return video_service.generate_video_frames(summary)

@app.get("/api/story/{cluster_id}/translate")
def translate_story(cluster_id: int, lang: Optional[str] = "Hindi"):
    """Translates news briefing to vernacular languages using Gemini."""
    briefing = get_story_briefing(cluster_id)
    summary = briefing.get("summary", "") if isinstance(briefing, dict) else str(briefing)
    return {
        "status": "success",
        "language": lang,
        "original": summary[:100] + "...",
        "translated": translation_service.translate(summary, lang)
    }

@app.get("/api/market/ticker")
def get_market_ticker():
    """Fetches real-time Bloomberg-style market tickers using yfinance."""
    return market_service.get_live_ticker()

@app.get("/")
def home():
    return {
        "message": "AI Native News API Online",
        "engines": ["TPU-v5e", "Gemini-Pro", "HuggingFace-Cinematic", "Vernacular-JAX"]
    }