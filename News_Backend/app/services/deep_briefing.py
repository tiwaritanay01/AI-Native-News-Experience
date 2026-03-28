from app.services.story_cluster import cluster_stories
from app.services.entity_extractor import extract_entities
from app.services.story_title import generate_story_title
from app.services.impact_analysis import analyze_impact
from app.services.llm_service import generate_llm_response
import json

def generate_deep_briefing(cluster_id):
    clusters = cluster_stories()
    if cluster_id not in clusters:
        return None

    stories = clusters[cluster_id]
    context = "\n\n".join(stories[:10])  # Use up to 10 stories for context

    prompt = f"""
    Synthesize the following {len(stories)} news articles into a single, high-level intelligence briefing for a busy executive.
    
    Structure:
    1. EXECUTIVE SUMMARY (3-4 sentences summarizing the core event).
    2. KEY PLAYERS & STAKES (Who is involved and what do they stand to gain/lose?).
    3. THE CRITICAL 'WHY' (Why does this matter right now?).
    4. TREND LINE (Where is this story heading?).
    5. FOLLOW-UP QUESTIONS: Provide 3 provocative questions the user might want to explore further.
    
    Articles:
    {context}
    
    Return the response as a valid JSON with keys: "title", "summary", "key_players", "why_it_matters", "trend_line", "follow_up_questions" (list).
    """

    try:
        raw_response = generate_llm_response(prompt)
        clean_response = raw_response.strip()
        if "```json" in clean_response:
            clean_response = clean_response.split("```json")[1].split("```")[0].strip()
        elif "```" in clean_response:
            clean_response = clean_response.split("```")[1].split("```")[0].strip()
            
        briefing_data = json.loads(clean_response)
        
        return {
            "title": briefing_data.get("title", generate_story_title(stories)),
            "articles": len(stories),
            "summary": briefing_data.get("summary", ""),
            "key_players": briefing_data.get("key_players", ""),
            "why_it_matters": briefing_data.get("why_it_matters", ""),
            "trend_line": briefing_data.get("trend_line", ""),
            "follow_up_questions": briefing_data.get("follow_up_questions", []),
            "entities": extract_entities(stories)[:5],
            "impact": analyze_impact(stories)
        }
    except Exception as e:
        print(f"❌ Synthesis error: {e}")
        return {
            "title": generate_story_title(stories),
            "articles": len(stories),
            "summary": " ".join(stories[:3])[:500],
            "key_players": "Investigation pending.",
            "why_it_matters": "Significant market impact detected.",
            "trend_line": "Developing story.",
            "follow_up_questions": ["What happens next?", "Who is most affected?", "How will markets react?"],
            "entities": extract_entities(stories)[:5],
            "impact": analyze_impact(stories)
        }