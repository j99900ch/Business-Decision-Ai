"""
Business DecisionAI
Public Web Search Layer

Uses the free/open-source DDGS package.
No paid API key is required.

Purpose:
    Search public web pages and return normalized results
    for the evidence layer.

This module does NOT call Gemini.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from ddgs import DDGS


@dataclass
class WebSearchResult:
    title: str
    url: str
    snippet: str
    source: str = "public_web"


def _clean_text(value) -> str:

    if value is None:
        return ""

    return " ".join(
        str(value).split()
    ).strip()


def search_public_web(
    query: str,
    max_results: int = 5,
) -> List[WebSearchResult]:
    """
    Search the public web using DDGS.

    No paid API key is required.

    Returns the same WebSearchResult structure
    used by the existing web-intelligence pipeline.
    """

    if not query or not query.strip():

        return []

    query = query.strip()

    try:

        search_results = list(
            DDGS().text(
                query,
                max_results=max_results,
            )
        )

    except Exception as error:

        raise RuntimeError(
            f"Public web search failed: {error}"
        ) from error

    results = []

    seen_urls = set()

    for item in search_results:

        if not isinstance(item, dict):
            continue

        title = _clean_text(
            item.get("title", "")
        )

        url = _clean_text(
            item.get("href", "")
            or item.get("url", "")
        )

        snippet = _clean_text(
            item.get("body", "")
            or item.get("snippet", "")
        )

        if not url:
            continue

        if url in seen_urls:
            continue

        seen_urls.add(url)

        results.append(
            WebSearchResult(
                title=title,
                url=url,
                snippet=snippet,
                source="public_web",
            )
        )

        if len(results) >= max_results:
            break

    return results