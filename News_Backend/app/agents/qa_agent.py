from app.services.story_cluster import cluster_stories


def answer_story_question(cluster_id, question):

    clusters = cluster_stories()

    if cluster_id not in clusters:
        return {"answer": "Story not found"}

    stories = clusters[cluster_id]

    context = " ".join(stories[:5]).lower()

    q = question.lower()

    if "why" in q:
        return {
            "answer": "Multiple news articles report this event indicating a significant development affecting companies or markets."
        }

    if "company" in q or "companies" in q:
        words = context.split()
        companies = [w for w in words if w.istitle()]
        return {"answer": list(set(companies))[:5]}

    if "what happened" in q or "summary" in q:
        return {"answer": context[:400]}

    if "next" in q:
        return {
            "answer": "Analysts expect further developments such as market reactions, policy responses, or company announcements."
        }

    return {"answer": "I cannot answer that yet."}