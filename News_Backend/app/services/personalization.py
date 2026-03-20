from app.services.impact_analysis import analyze_impact


def personalize_feed(clusters, profile):

    feed = []

    for cid, stories in clusters.items():

        impact = analyze_impact(stories)

        if profile == "investor" and "Markets" in impact:
            feed.append((cid, stories))

        elif profile == "founder" and "Startup" in impact:
            feed.append((cid, stories))

        elif profile == "tech" and "Tech" in impact:
            feed.append((cid, stories))

        elif profile == "policy" and "Policy" in impact:
            feed.append((cid, stories))

    return feed