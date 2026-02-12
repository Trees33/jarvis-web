from ddgs import DDGS

def search_web(query):
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=5)
        text = ""
        for r in results:
            text += f"{r['title']} — {r['body']}\n"
        return text