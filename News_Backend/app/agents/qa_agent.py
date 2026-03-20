from app.services.story_cluster import cluster_stories


def answer_question(cluster_id, question):

    clusters = cluster_stories()

    if cluster_id not in clusters:
        return {"answer": "Story not found."}

    stories = clusters[cluster_id]

    context = " ".join(stories[:5]).lower()

    question = question.lower()

    if "why" in question:

        return {
            "answer": "Multiple articles indicate a significant development affecting companies or markets."
        }

    if "companies" in question:

        words = context.split()
        companies = [w for w in words if w.istitle()]

        return {
            "answer": list(set(companies))[:5]
        }

    if "next" in question or "happen next" in question:

        return {
            "answer": "Based on current coverage, analysts expect further developments such as market reactions, policy responses, or company announcements."
        }

    return {"answer": "I cannot answer that yet."}