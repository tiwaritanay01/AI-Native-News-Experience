from fastapi import APIRouter

from app.agents.personalization_agent import get_personalized_feed
from app.agents.relevance_agent import explain_relevance
from app.agents.dashboard_agent import generate_dashboard

router = APIRouter()

@router.get("/personalized_feed")
def personalized_feed(user_profile: str):

    feed = get_personalized_feed(user_profile)

    return {
        "user_profile": user_profile,
        "stories": feed
    }


@router.get("/story/{cluster_id}/relevance")
def story_relevance(cluster_id: int, user_profile: str):

    data = explain_relevance(cluster_id, user_profile)

    return data


@router.get("/story/{cluster_id}/dashboard")
def story_dashboard(cluster_id: int):

    data = generate_dashboard(cluster_id)

    return data