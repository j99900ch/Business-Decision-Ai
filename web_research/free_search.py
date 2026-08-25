"""
=========================================================
Business DecisionAI
Free Public Web Search

Uses DuckDuckGo public search results.

No paid search API key required.

This module is completely independent from:
    - app.py
    - existing RAG
    - Gemini
    - questionnaire
    - decision context
=========================================================
"""

from ddgs import DDGS


def search_web(
    query: str,
    max_results: int = 6,
) -> list[dict]:
    """
    Search the public web.

    Returns a list of:
        title
        url
        snippet
    """

    query = str(query).strip()

    if not query:
        return []

    results = []

    try:

        with DDGS() as search:

            raw_results = search.text(
                query,
                max_results=max_results,
            )

            for item in raw_results:

                title = str(
                    item.get("title", "")
                ).strip()

                url = str(
                    item.get("href", "")
                ).strip()

                snippet = str(
                    item.get("body", "")
                ).strip()

                if not url:
                    continue

                results.append(
                    {
                        "title": title,
                        "url": url,
                        "snippet": snippet,
                    }
                )

    except Exception as exc:

        raise RuntimeError(
            f"Web search failed: {exc}"
        ) from exc

    return results