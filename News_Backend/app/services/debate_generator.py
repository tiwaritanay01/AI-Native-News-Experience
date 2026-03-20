def generate_debate(stories):

    text = " ".join(stories[:3])

    pro_view = "Supporters argue that this development could accelerate innovation and economic growth."

    con_view = "Critics warn that this development may create risks including regulation, market volatility, or geopolitical tension."

    debate = {
        "pro": pro_view,
        "con": con_view
    }

    return debate