from fastapi import FastAPI
from app.agents.story_agent import get_story_intelligence
from app.agents.qa_agent import answer_question

app = FastAPI()


@app.get("/stories")
def stories():

    return get_story_intelligence()


@app.post("/ask")
def ask(data:dict):

    return answer_question(data["cluster_id"], data["question"])