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
    
    # Try to extract the two viewpoints cleanly
    # Assuming the LLM follows the format "Viewpoint A: ... Viewpoint B: ..."
    views = []
    if "Viewpoint A:" in response and "Viewpoint B:" in response:
        part_b = response.split("Viewpoint B:")[1].strip()
        part_a = response.split("Viewpoint B:")[0].split("Viewpoint A:")[1].strip()
        views = [part_a, part_b]
    else:
        # Fallback split
        views = [s.strip() for s in response.split("\n\n") if s.strip()][:2]

    return {
        "status": "success",
        "opinions": views
    }