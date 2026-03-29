from app.services.llm_service import generate_llm_response


def analyze_story_impact(articles):

    context = ""

    for article in articles[:5]:
        context += article + "\n\n"

    prompt = f"""
    You are an AI market intelligence analyst.
    Evaluate the impact of the following news on key sectors.
    
    1. EXRACT SCORES (1-10): Evaluate impact for Stock Market, Economy, Banking, Commodities, and Geopolitics.
    2. SUMMARIZE: Provide a 2-sentence sophisticated impact summary in the "raw" field.

    Return ONLY a JSON object:
    {{
      "stock_market": number,
      "economy": number,
      "banking": number,
      "commodities": number,
      "geopolitics": number,
      "raw": "Sophisticated summary here."
    }}

    Articles:
    {context}
    """

    response = generate_llm_response(prompt)

    return response