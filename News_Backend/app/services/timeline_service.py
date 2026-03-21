from app.services.llm_service import generate_llm_response


def build_story_timeline(articles):

    context = ""

    for i, article in enumerate(articles[:8]):
        context += f"Article {i+1}: {article}\n\n"

    prompt = f"""
You are a financial news analyst.

Using the following articles create a chronological timeline
of the story.

Return 4–6 key events in order.

Format:

Day 1:
Event description

Day 2:
Event description

Articles:
{context}
"""

    timeline = generate_llm_response(prompt)

    return timeline