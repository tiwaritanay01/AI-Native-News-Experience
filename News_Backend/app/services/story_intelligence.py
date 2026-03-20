from app.services.story_cluster import cluster_stories


def get_story_context(cluster_id):

    clusters = cluster_stories()

    if cluster_id not in clusters:
        return None

    stories = clusters[cluster_id]

    context = "\n".join(stories[:5])

    return context


def ask_story_question(cluster_id, question):

    context = get_story_context(cluster_id)

    if context is None:
        return "Story not found."

    question = question.lower()

    if "why" in question:
        return "This story appears frequently across multiple articles suggesting a major development impacting markets or companies."

    if "companies" in question:
        words = context.split()
        companies = [w for w in words if w.istitle()]
        return list(set(companies))[:5]

    if "what happened" in question:
        return context[:300]

    return "I cannot answer that yet."