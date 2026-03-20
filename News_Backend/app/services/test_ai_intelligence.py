from app.services.story_cluster import cluster_stories
from app.services.deep_briefing import generate_deep_briefing
from app.services.debate_generator import generate_debate
from app.services.impact_simulator import simulate_impact


clusters = cluster_stories()

cluster_id = list(clusters.keys())[0]

stories = clusters[cluster_id]

briefing = generate_deep_briefing(cluster_id)
debate = generate_debate(stories)
impact = simulate_impact(stories)


print("\n🧠 AI DEEP BRIEFING\n")

print("Title:", briefing["title"])
print("Articles:", briefing["articles"])
print("Impact:", briefing["impact"])
print("Entities:", briefing["entities"])

print("\nSummary:\n")
print(briefing["summary"])


print("\n⚖️ DEBATE\n")

print("Pro View:", debate["pro"])
print("Con View:", debate["con"])


print("\n🌍 IMPACT SIMULATION\n")

print("Affected Groups:", impact)