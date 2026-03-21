from app.services.llm_service import generate_llm_response


def analyze_story_impact(articles):

    context = ""

    for article in articles[:5]:
        context += article + "\n\n"

    prompt = f"""
You are a financial news analyst.

Based on the news articles below evaluate the impact on:

Stock Market
Economy
Banking Sector
Commodities
Geopolitics

Return a score from 1 to 10.

Format JSON like this:

{{
 "stock_market": number,
 "economy": number,
 "banking": number,
 "commodities": number,
 "geopolitics": number
}}

Articles:
{context}
"""

    response = generate_llm_response(prompt)

    return response