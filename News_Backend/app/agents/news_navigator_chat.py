import os
import requests
import json
from app.services.story_cluster import cluster_stories

from app.services.llm_service import generate_llm_response

def get_navigator_chat_response(cluster_id, question, history=[]):
    """
    Context-aware chatbot for News Navigator using Groq (Llama-3).
    """
    clusters = cluster_stories()
    articles = clusters.get(cluster_id, [])
    context = "\n\n".join(articles[:5]) if articles else "No context available."

    prompt = f"""
    You are the 'News Navigator Intelligence'—a high-speed, factual AI built on Groq/Llama technology.
    You have deep context on the following news cluster.
    
    Context:
    {context}
    
    Previous Chat:
    {json.dumps(history)}
    
    Goal: Answer the user's question with authority, speed, and precision. If they ask about future impacts, give a data-driven prediction.
    
    Question: {question}
    """

    try:
        response = generate_llm_response(prompt)
        return response
    except Exception as e:
        print(f"❌ Chat Error: {e}")
        return "System recalibrating narrative pathways. Please inquire again in a moment."
