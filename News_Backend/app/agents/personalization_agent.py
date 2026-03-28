from app.services.story_cluster import cluster_stories
from app.services.llm_service import generate_llm_response
import json

def get_personalized_feed(user_profile: str):
    """
    Analyzes news stories against a user profile (e.g., 'Investor', 'Founder', 'Student')
    and adapts the content style and relevance scoring.
    """
    clusters = cluster_stories()
    personalized_stories = []

    for cluster_id, articles in clusters.items():
        text = " ".join(articles[:5])
        
        prompt = f"""
        Role: Personalized Financial News Curator
        User Persona: {user_profile}
        
        Analyze this news cluster for the specific needs of the persona.
        - If 'Investor': Focus on portfolio impact, ROI, and volatility.
        - If 'Startup Founder': Focus on funding trends, competitor moves, and talent shifts.
        - If 'Student': Focus on explaining 'Why' this is happening and defining jargon.
        
        News Context:
        {text}
        
        Return a JSON with:
        1. "relevance_score": (1-10)
        2. "persona_summary": A summary tailored to their specific interests.
        3. "action_item": One specific takeaway or thing they should watch for.
        """

        try:
            response = generate_llm_response(prompt)
            clean_res = response.strip()
            if "```json" in clean_res:
                clean_res = clean_res.split("```json")[1].split("```")[0].strip()
            data = json.loads(clean_res)
            
            personalized_stories.append({
                "cluster_id": cluster_id,
                "relevance": data.get("relevance_score", 5),
                "summary": data.get("persona_summary", ""),
                "action": data.get("action_item", "Monitor this story.")
            })
        except Exception as e:
            print(f"❌ Personalization error for {cluster_id}: {e}")
            personalized_stories.append({
                "cluster_id": cluster_id,
                "relevance": 5,
                "summary": "General market movement detected.",
                "action": "Stay updated."
            })

    # Sort by relevance
    personalized_stories.sort(key=lambda x: x["relevance"], reverse=True)
    return personalized_stories