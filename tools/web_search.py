from duckduckgo_search import DDGS

def web_search(question: str) -> str:
    try:
        results = DDGS().text(question, max_results=3)

        if not results:
            return "No search results found."

        parts = []
        for r in results:
            parts.append(f"{r['body']}")

        paragraph = " ".join(parts)

        return f"🌐 {paragraph}"

    except Exception as e:
        return f"Search failed: {str(e)}"