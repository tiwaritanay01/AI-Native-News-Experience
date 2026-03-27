import json
import re
from app.services.llm_service import generate_llm_response

def generate_story_briefing(articles: list):
    """
    Polished briefing generator for Aureum Terminal v2.
    Synthesizes data into human-centric journalistic briefings.
    """
    context = "\n\n".join([str(a) for a in articles[:5]])

    prompt = f"""
    Aureum Intelligence System — [Human-Centric Journalistic Mode]
    Analyze the provided news clusters and synthesize a professional narrative.
    
    Context:
    {context}
    
    Return a JSON structure (NO other text):
    {{
        "headline": "A bold, cinematic headline suitable for high-end serif typography",
        "summary": "Professional, easy-to-read human synthesis of the entire story arc",
        "why_matters": ["Signal 1", "Signal 2"],
        "sentiment": "BULLISH/BEARISH/NEUTRAL"
    }}
    """

    res_raw = generate_llm_response(prompt)
    
    # Extract JSON string if wrapped in code blocks
    match = re.search(r'\{.*\}', res_raw, re.DOTALL)
    res_raw = match.group(0) if match else res_raw

    try:
        data = json.loads(res_raw)
        return data
    except Exception as e:
        print(f"❌ Briefing Parse Failed: {e}. Raw: {res_raw[:100]}...")
        return {
            "headline": "Intelligence Stream: Signal Sync",
            "summary": res_raw,
            "why_matters": ["Awaiting deeper neural synthesis."],
            "sentiment": "NEUTRAL"
        }