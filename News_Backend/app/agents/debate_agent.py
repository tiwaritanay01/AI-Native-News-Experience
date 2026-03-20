import time
import uuid
from app.services.story_cluster import cluster_stories
from app.services.debate_service import generate_debate_turn
from app.services.llm_service import generate_llm_response

debate_sessions = {}

DEBATE_DURATION = 180   # 3 minutes


def start_debate(cluster_id):

    clusters = cluster_stories()

    if cluster_id not in clusters:
        return {"error": "Story not found"}

    session_id = str(uuid.uuid4())

    debate_sessions[session_id] = {
        "cluster_id": cluster_id,
        "history": [],
        "start_time": time.time()
    }

    return {"session_id": session_id}


def next_turn(session_id):

    session = debate_sessions.get(session_id)

    if not session:
        return {"error": "Invalid session"}

    if time.time() - session["start_time"] > DEBATE_DURATION:
        return {"message": "Debate finished"}

    clusters = cluster_stories()
    articles = clusters[session["cluster_id"]]

    history = session["history"]

    analyst_a = generate_debate_turn("Bullish Analyst", history, articles)
    history.append("Analyst A: " + analyst_a)

    analyst_b = generate_debate_turn("Bearish Analyst", history, articles)
    history.append("Analyst B: " + analyst_b)

    return {
        "analyst_a": analyst_a,
        "analyst_b": analyst_b
    }

def ask_debate_question(session_id, question):

    session = debate_sessions.get(session_id)

    if not session:
        return {"error": "Invalid session"}

    clusters = cluster_stories()
    articles = clusters[session["cluster_id"]]

    history = session["history"]

    context = "\n".join(articles[:5])
    history_text = "\n".join(history)

    prompt = f"""
A debate is happening between two analysts.

Story context:
{context}

Debate history:
{history_text}

User question:
{question}

Both analysts should respond briefly.

Format:
Analyst A:
Analyst B:
"""

    response = generate_llm_response(prompt)

    return {"response": response}


def end_debate(session_id):

    if session_id in debate_sessions:
        del debate_sessions[session_id]

    return {"message": "Debate ended"}