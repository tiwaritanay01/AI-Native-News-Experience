import ollama

def generate_followup_questions(text: str):
    prompt = f"""
    You are a news analyst.

    Based on the news story below, generate 3 intelligent follow-up questions
    that a reader might ask.

    News Story:
    {text}

    Return only the questions as a list.
    """

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]