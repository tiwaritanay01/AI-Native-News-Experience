from fastapi import FastAPI
from app.agents.story_agent import get_all_stories
from app.agents.briefing_agent import get_story_briefing
from app.agents.qa_agent import answer_story_question
from app.agents.intelligence_agent import get_story_intelligence 
from app.agents.intelligence_agent import get_story_intelligence
from app.agents.story_of_day_agent import get_story_of_the_day
from app.agents.question_agent import get_story_questions
from app.agents.question_answer_agent import answer_question
from app.agents.debate_agent import start_debate, next_turn, end_debate
from app.agents.opinion_agent import get_contrarian_opinions
from app.agents.debate_agent import (
    start_debate,
    next_turn,
    end_debate,
    ask_debate_question
)
from app.agents.impact_agent import get_story_impact
from app.agents.timeline_agent.timeline_agent import generate_story_timeline
from app.agents.sentiment_agent import get_story_sentiment
from app.api.story_routes import router as story_router
 

app = FastAPI()
app.include_router(story_router)

@app.get("/story_of_day")
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

    return get_story_intelligence(cluster_id)

@app.get("/story/{cluster_id}/questions")
def story_questions(cluster_id: int):

    return get_story_questions(cluster_id)

@app.post("/story/{cluster_id}/ask")
def ask_story_question(cluster_id: int, question: str):

    return answer_question(cluster_id, question)

@app.post("/debate/start/{cluster_id}")
def debate_start(cluster_id: int):
    return start_debate(cluster_id)

@app.get("/debate/{session_id}/turn")
def debate_turn(session_id: str):
    return next_turn(session_id)

@app.post("/debate/{session_id}/exit")
def debate_exit(session_id: str):
    return end_debate(session_id)

@app.get("/story/{cluster_id}/opinions")
def story_opinions(cluster_id: int):

    return get_contrarian_opinions(cluster_id)

@app.post("/debate/{session_id}/ask")
def debate_question(session_id: str, question: str):
    return ask_debate_question(session_id, question)

@app.get("/story/{cluster_id}/impact")
def story_impact(cluster_id: int):

    return get_story_impact(cluster_id)

@app.get("/story/{cluster_id}/timeline")
def story_timeline(cluster_id: int):

   return generate_story_timeline(cluster_id)

@app.get("/story/{cluster_id}/sentiment")
def story_sentiment(cluster_id: int):

    return get_story_sentiment(cluster_id)

# @app.get("/story/{cluster_id}/dashboard")
# def story_dashboard(cluster_id: int):
#     return generate_dashboard(cluster_id)

@app.get("/")
def home():
    return {"message": "AI Native News API Running"}