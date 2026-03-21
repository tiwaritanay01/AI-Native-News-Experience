from app.agents.story_briefing_agent import generate_story_brief
from app.agents.timeline_agent.timeline_agent import generate_story_timeline
from app.agents.impact_agent import get_story_impact
from app.agents.sentiment_agent import get_story_sentiment
from app.agents.opinion_agent import detect_contrarian_opinions
from app.agents.followup_agent import generate_followup_questions


def generate_dashboard(cluster_id):

    briefing = generate_story_brief(cluster_id)

    timeline = generate_story_timeline(cluster_id)

    impact = get_story_impact(cluster_id)

    sentiment = get_story_sentiment(cluster_id)

    opinions = detect_contrarian_opinions(cluster_id)

    questions = generate_followup_questions(cluster_id)

    return {
        "briefing": briefing,
        "timeline": timeline,
        "impact_radar": impact,
        "sentiment": sentiment,
        "contrarian_opinions": opinions,
        "follow_up_questions": questions
    }