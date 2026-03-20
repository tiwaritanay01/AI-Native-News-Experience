import re

def generate_story_title(stories):

    text = " ".join(stories[:5])

    words = re.findall(r"\b[A-Z][a-zA-Z]+\b", text)

    freq = {}

    for w in words:
        freq[w] = freq.get(w,0) + 1

    sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    keywords = [w[0] for w in sorted_words[:3]]

    if len(keywords) >= 3:
        title = f"{keywords[0]} {keywords[1]} {keywords[2]} News"
    else:
        title = "Breaking News Story"

    return title