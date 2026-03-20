from app.services.llm_service import generate_llm_response


def answer_story_question(question, articles):

    context = ""

    for article in articles[:5]:
        context += article + "\n\n"

    prompt = f"""
You are an AI financial news analyst.

Answer the user's question based on the news articles below.

Articles:
{context}

Question:
{question}

Provide a clear explanation.
"""

    answer = generate_llm_response(prompt)

    return answer