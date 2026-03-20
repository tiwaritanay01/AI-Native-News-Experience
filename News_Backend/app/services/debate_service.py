from app.services.llm_service import generate_llm_response

def generate_debate_turn(role, history, articles):

    context = "\n".join(articles[:5])
    history_text = "\n".join(history)

    prompt = f"""
You are a financial analyst in a debate.

Role: {role}

Debate rules:
- Stay focused on the story
- Respond to the opponent's argument
- Speak in 3 sentences
- Do not repeat points

Story context:
{context}

Debate so far:
{history_text}

Provide the next argument.
"""

    return generate_llm_response(prompt)