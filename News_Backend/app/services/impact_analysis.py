import json
import re
from app.services.llm_service import generate_llm_response

def analyze_impact(stories: list):
    """
    Polished impact analyzer for Aureum Terminal v2.
    Generates structured radar and sector data for terminal visualization.
    """
    context = "\n\n".join([str(s) for s in stories[:5]])

    prompt = f"""
    Aureum Intelligence System — [Market Analysis Mode]
    Analyze the following news clusters for cross-sector impact and sentiment.
    
    Context:
    {context}
    
    Return a JSON structure (NO other text):
    {{
        "sectors": ["Sector A", "Sector B"],
        "radar": {{ "bullish": 0.0-1.0, "bearish": 0.0-1.0, "interest": 0.0-1.0 }},
        "summary": "A 1-sentence technical analysis for the terminal dashboard."
    }}
    """

    res_raw = generate_llm_response(prompt)
    
    # Extract JSON
    match = re.search(r'\{.*\}', res_raw, re.DOTALL)
    res_raw = match.group(0) if match else res_raw

    try:
        data = json.loads(res_raw)
        return data
    except Exception as e:
        print(f"❌ Impact Parse Failed: {e}. Raw: {res_raw[:100]}...")
        return {
            "sectors": ["Global Markets", "Technology"],
            "radar": { "bullish": 0.5, "bearish": 0.5, "interest": 0.8 },
            "summary": "Signals normalized. Market impact stable across sectors."
        }