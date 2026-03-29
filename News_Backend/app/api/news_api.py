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

from app.db.user_db import register_user, login_user, get_user_persona

@app.post("/register")
def register(data: dict):
    success = register_user(data["username"], data["password"], data["persona"])
    return {"status": "success" if success else "error"}

@app.post("/login")
def login(data: dict):
    persona = login_user(data["username"], data["password"])
    if persona:
        return {"status": "success", "persona": persona, "username": data["username"]}
    return {"status": "error", "message": "Invalid credentials"}

@app.get("/user/{username}/persona")
def user_persona(username: str):
    return {"persona": get_user_persona(username)}

from app.agents.news_navigator_chat import get_navigator_chat_response

@app.post("/navigator/chat")
def navigator_chat(data: dict):
    cluster_id = data.get("cluster_id")
    question = data.get("question")
    history = data.get("history", [])
    response = get_navigator_chat_response(cluster_id, question, history)
    return {"status": "success", "response": response}

from app.agents.personalization_agent import get_personalized_feed

@app.get("/personalized-feed/{username}")
def personalized_feed(username: str):
    persona = get_user_persona(username)
    return get_personalized_feed(persona)

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

@app.get("/api/health")
def health_check():
    """Health check endpoint used by deployment scripts to confirm startup."""
    from app.services.hardware_engine import get_hardware_type
    return {
        "status": "online",
        "hardware": get_hardware_type(),
        "version": "2.2"
    }

@app.get("/api/test-gemini")
def test_gemini():
    """Health check specifically for the Gemini API connection."""
    import os
    import google.generativeai as genai
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        return {"status": "error", "message": "GEMINI_API_KEY is not set."}
    
    try:
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Ping. Reply with exactly 'Pong'.")
        return {
            "status": "success",
            "model": "gemini-1.5-flash",
            "response": response.text
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}