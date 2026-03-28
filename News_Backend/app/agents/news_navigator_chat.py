import os
import requests
import json
from app.services.story_cluster import cluster_stories

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "YOUR_GROQ_API_KEY")

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

    # If no API key, fallback or return error
    if not GROQ_API_KEY or GROQ_API_KEY == "YOUR_GROQ_API_KEY":
        return "Chat system is initializing. Please ensure GROQ_API_KEY is configured."

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        res_data = response.json()
        return res_data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"❌ Groq Chat Error: {e}")
        return "I'm having trouble reaching the Groq engine right now. Please try again in 5 seconds."
