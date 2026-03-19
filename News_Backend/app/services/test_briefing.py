from app.services.news_briefing import generate_briefing

briefings = generate_briefing()

for b in briefings:

    print()
    print("🧠 AI NEWS BRIEFING")
    print("---------------------")
    print("Story Cluster:", b["cluster"])
    print("Articles:", b["articles"])
    print()
    print("Summary:")
    print(b["summary"])
    print()