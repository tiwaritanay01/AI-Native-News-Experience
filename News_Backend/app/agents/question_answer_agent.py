from app.services.story_cluster import cluster_stories
from app.services.question_answer_service import answer_story_question


def answer_question(cluster_id, question):

    clusters = cluster_stories()

    if cluster_id not in clusters:
        return {"error": "Story not found"}

    articles = clusters[cluster_id]

    answer = answer_story_question(question, articles)

    return {
        "question": question,
        "answer": answer
    }