from app.services.story_cluster import cluster_stories
from app.services.question_generator import generate_followup_questions


def get_story_questions(cluster_id):

    clusters = cluster_stories()

    if cluster_id not in clusters:
        return {"error": "Story not found"}

    articles = clusters[cluster_id]

    questions = generate_followup_questions(articles)

    return {
        "cluster_id": cluster_id,
        "questions": questions
    }