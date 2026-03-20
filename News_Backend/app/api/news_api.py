from fastapi import FastAPI
from app.agents.story_agent import get_all_stories
from app.agents.briefing_agent import get_story_briefing
from app.agents.qa_agent import answer_story_question
from app.agents.intelligence_agent import get_story_intelligence    

app = FastAPI()


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