import re

def extract_entities(stories):

    text = " ".join(stories)

    entities = re.findall(r"\b[A-Z][a-zA-Z]+\b", text)

    freq = {}

    for e in entities:
        freq[e] = freq.get(e,0)+1

    sorted_entities = sorted(freq.items(), key=lambda x:x[1], reverse=True)

    return [e[0] for e in sorted_entities[:10]]