from app.services.story_cluster import cluster_stories
from app.services.llm_service import generate_llm_response
import json

def generate_story_timeline(cluster_id):
    """
    Builds a chronological timeline of events AND predicts future moves 
    (Story Arc Tracking vision: 'what to watch next').
    """
    clusters = cluster_stories()
    articles = clusters.get(cluster_id, [])
    if not articles:
        articles = clusters.get(str(cluster_id), [])
        
    if not articles:
        return {
            "events": [{"date": "Now", "event": "Signals are emerging for this narrative cluster. Standby for deep analysis."}],
            "sentiment_arc": "Status: Initializing Narrative Stream",
            "predictions": ["Awaiting further data for predictive modeling."]
        }
    
    text = "\n\n".join(articles[:8])  # More context for better timeline
    
    prompt = f"""
    You are a Strategic Forecaster for Business News.
    Analyze the following cluster of articles to build a complete Story Arc.
    
    1. EXTRAPOLATE TIMELINE: Key chronological events leading to now.
    2. SENTIMENT SHIFT: How has market/public sentiment changed over this arc?
    3. PREDICTIVE INSIGHT: 'What to watch next' - 3 logical future developments based on current trends.
    
    News Context:
    {text}
    
    Return as JSON with keys: 'events' (list of {{"date", "event"}}), 'sentiment_arc', 'predictions' (list).
    """

    try:
        response = generate_llm_response(prompt)
        clean_res = response.strip()
        if "```json" in clean_res:
             clean_res = clean_res.split("```json")[1].split("```")[0].strip()
        data = json.loads(clean_res)
        return data
    except Exception as e:
        print(f"❌ Timeline generation error: {e}")
        return {
            "events": [{"date": "Recent", "event": "Significant story development."}],
            "sentiment_arc": "Neutral to Bullish",
            "predictions": ["Further regulatory scrutiny expected.", "Competitor response likely."]
        }