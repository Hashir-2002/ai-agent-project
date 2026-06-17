def web_search(question: str):
    try:
        results = DDGS().text(question, max_results=3)

        output = []

        for r in results:
            output.append(
                f"{r['title']}\n{r['body']}\n{r['href']}"
            )

        return "\n\n---\n\n".join(output)

    except Exception as e:
        return f"Search failed: {str(e)}"