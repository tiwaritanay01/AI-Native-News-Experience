def generate_timeline(stories):

    timeline = []

    for i, article in enumerate(stories[:5]):

        event = {
            "step": i + 1,
            "event": article[:120]
        }

        timeline.append(event)

    return timeline