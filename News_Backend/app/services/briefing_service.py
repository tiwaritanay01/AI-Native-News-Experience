from app.services.llm_service import generate_llm_response


def generate_story_briefing(articles):

    context = ""

    for article in articles[:5]:
        context += article + "\n\n"

    prompt = f"""
You are an AI financial news analyst.

Analyze the following news articles and produce a structured briefing.

Articles:
{context}

Return the result in this format:

KEY EVENTS:
- ...

WHY IT MATTERS:
- ...

MARKET IMPACT:
- ...

WHAT TO WATCH NEXT:
- ...
"""

    result = generate_llm_response(prompt)

    return result