from app.services.llm_service import generate_llm_response


def generate_followup_questions(articles):

    context = ""

    for article in articles[:5]:
        context += article + "\n\n"

    prompt = f"""
You are an AI news analyst.

Based on the following news articles, generate 5 intelligent follow-up questions
that a reader might ask to understand the story better.

Articles:
{context}

Return only the questions as bullet points.
"""

    response = generate_llm_response(prompt)

    return response