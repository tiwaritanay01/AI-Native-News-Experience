from app.services.llm_service import generate_llm_response


def detect_contrarian_opinions(articles):

    context = ""

    for article in articles[:5]:
        context += article + "\n\n"

    prompt = f"""
You are a financial news analyst.

From the following articles identify two opposing viewpoints
about the story.

Return in this format:

Viewpoint A:
<short explanation>

Viewpoint B:
<short explanation>

Articles:
{context}
"""

    response = generate_llm_response(prompt)

    return response