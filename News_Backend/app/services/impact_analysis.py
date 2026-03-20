def analyze_impact(stories):

    text = " ".join(stories).lower()

    impact = []

    market_keywords = ["stock","market","shares","nasdaq","dow","earnings"]
    tech_keywords = ["ai","software","chip","technology","cloud"]
    policy_keywords = ["government","policy","regulation","law","minister"]
    startup_keywords = ["startup","funding","venture","seed","series"]

    if any(k in text for k in market_keywords):
        impact.append("Markets")

    if any(k in text for k in tech_keywords):
        impact.append("Tech")

    if any(k in text for k in policy_keywords):
        impact.append("Policy")

    if any(k in text for k in startup_keywords):
        impact.append("Startup")

    return impact