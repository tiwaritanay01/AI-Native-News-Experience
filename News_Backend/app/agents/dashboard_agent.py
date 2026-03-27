from app.agents.story_briefing_agent import generate_story_brief
from app.agents.timeline_agent.timeline_agent import generate_story_timeline
from app.agents.impact_agent import get_story_impact
from app.agents.sentiment_agent import get_story_sentiment
from app.agents.opinion_agent import get_contrarian_opinions
from app.agents.followup_agent import generate_followup_questions


def generate_dashboard(cluster_id):
    try:
        if cluster_id == 0:
            from app.agents.story_agent import get_all_stories
            all_stories = get_all_stories()
            if all_stories:
                cluster_id = all_stories[0]["cluster_id"]
            else:
                raise ValueError("No stories found in the database.")

        # Sequential agents to prevent CPU/Memory usage spike
        briefing = generate_story_brief(cluster_id)
        timeline = generate_story_timeline(cluster_id)
        impact = get_story_impact(cluster_id)
        sentiment = get_story_sentiment(cluster_id)
        opinions = get_contrarian_opinions(cluster_id)
        questions = generate_followup_questions(cluster_id)

        return {
            "briefing": briefing,
            "timeline": timeline,
            "impact": impact,
            "sentiment": sentiment,
            "opinions": opinions,
            "relevance": briefing,
            "follow_up_questions": questions
        }
    except Exception as e:
        print(f"Error generating dashboard for cluster {cluster_id}: {e}")
        return {
            "briefing": "Loading briefing...",
            "timeline": [],
            "impact": {},
            "sentiment": "neutral",
            "opinions": [],
            "relevance": "N/A",
            "follow_up_questions": []
        }