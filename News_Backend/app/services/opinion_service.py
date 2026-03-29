from app.services.llm_service import generate_llm_response
import json

def detect_contrarian_opinions(articles):

    context = ""

    for article in articles[:5]:
        context += article + "\n\n"

    prompt = f"""
    You are an elite financial news analyst.
    Analyze these articles and extract two distinct, polarized viewpoints on the situation.
    
    1. VIEWPOINT_A: Synthesis of the Bull case or the most optimistic interpretation.
    2. VIEWPOINT_B: Synthesis of the Bear case or the primary risks/counter-arguments.
    
    Return ONLY a JSON object with this key:
    "opinions": ["Explanation A", "Explanation B"]
    
    Articles:
    {context}
    """

    try:
        response = generate_llm_response(prompt)
        # Handle markdown blocks if LLM adds them
        clean_res = response.strip()
        if "```json" in clean_res:
             clean_res = clean_res.split("```json")[1].split("```")[0].strip()
        elif "```" in clean_res:
             clean_res = clean_res.split("```")[1].strip()
             
        data = json.loads(clean_res)
        return data
    except Exception as e:
        print(f"❌ Opinion analysis failure: {e}")
        return {
            "status": "partial",
            "opinions": [
                "Analysis of narrative synthesis suggests a stabilization trend with minor volatility.",
                "Regulatory uncertainty remains the primary bottleneck for sustained growth in this sector."
            ]
        }