def simulate_impact(stories):

    text = " ".join(stories).lower()

    impacts = []

    if "stock" in text or "market" in text:
        impacts.append("Investors")

    if "ai" in text or "technology" in text:
        impacts.append("Tech Industry")

    if "government" in text or "policy" in text:
        impacts.append("Policy Makers")

    if "startup" in text or "funding" in text:
        impacts.append("Startup Ecosystem")

    return impacts