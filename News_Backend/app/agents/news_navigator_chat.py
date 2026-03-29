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
    SYSTEM: You are the 'Aureum News Navigator'—an elite intelligence engine. 
    Your tone is ultra-precise, strategic, and authoritative (like a Bloomberg Terminal combined with a high-end research analyst).
    
    PRIMARY DIRECTIVE:
    1. SYNTHESIZE: Use the context provided to answer with depth. Don't just summarize; explain the 'why'.
    2. STRATEGIZE: If the user asks about the future or impact, provide a 'Strategic Forecast' with logic.
    3. PRECISION: Use data points from the context if available.
    
    CONTEXT DATA:
    {context}
    
    CONVERSATION THREAD:
    {json.dumps(history)}
    
    USER INQUIRY: {question}
    
    OUTPUT: Provide a direct, sophisticated response. Use markdown for clarity if needed.
    """

    try:
        response = generate_llm_response(prompt)
        return response
    except Exception as e:
        print(f"❌ Chat Error: {e}")
        return "System recalibrating narrative pathways. Please inquire again in a moment."
