from app.services.llm_service import generate_llm_response


def generate_story_brief(text):
    prompt = f"""
Summarize this news story and provide:

1. Key Events
2. Why it matters
3. Market impact
4. What to watch next

News:
{text}
"""
    return generate_llm_response(prompt)