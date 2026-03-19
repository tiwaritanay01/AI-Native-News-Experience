from app.services.story_cluster import cluster_stories


def generate_briefing():

    clusters = cluster_stories()

    briefings = []

    for cluster_id, stories in clusters.items():

        # take top 5 articles from cluster
        top_articles = stories[:5]

        text_block = "\n".join(top_articles)

        # simple extractive summary
        summary = text_block[:500]

        briefing = {
            "cluster": cluster_id,
            "articles": len(stories),
            "summary": summary
        }

        briefings.append(briefing)

    return briefings