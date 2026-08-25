"""
Business DecisionAI
Public Web Evidence Assembly
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Iterable

from web_intelligence.web_search import (
    WebSearchResult,
)


def assemble_web_evidence(
    results: Iterable[WebSearchResult],
) -> list[dict]:
    """
    Convert raw search results into a stable evidence structure.

    This structure is intentionally independent of Gemini.
    """

    evidence = []

    for index, result in enumerate(
        results,
        start=1,
    ):

        evidence.append(
            {
                "evidence_id": f"WEB-{index:03d}",
                "title": result.title,
                "url": result.url,
                "snippet": result.snippet,
                "source_type": "public_web",
            }
        )

    return evidence


def build_web_context(
    evidence: list[dict],
) -> str:
    """
    Convert web evidence into controlled LLM context.

    The caller can later combine this with:
        - business profile
        - private RAG evidence
        - owner answers
        - business decision
    """

    if not evidence:

        return (
            "PUBLIC WEB EVIDENCE\n"
            "--------------------\n"
            "No public web evidence was retrieved."
        )

    sections = [
        "PUBLIC WEB EVIDENCE",
        "--------------------",
    ]

    for item in evidence:

        sections.append(
            "\n".join(
                [
                    f"Evidence ID: {item['evidence_id']}",
                    f"Title: {item['title']}",
                    f"URL: {item['url']}",
                    f"Snippet: {item['snippet']}",
                ]
            )
        )

    sections.append(
        "\n".join(
            [
                "WEB EVIDENCE INSTRUCTION",
                "-------------------------",
                (
                    "Use public web evidence only when "
                    "relevant to the business decision. "
                    "Do not treat missing web information "
                    "as a known fact."
                ),
            ]
        )
    )

    return "\n\n".join(
        sections
    )