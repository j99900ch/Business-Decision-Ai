"""
Business DecisionAI
Public Web Intelligence Orchestrator

Flow:

Business Decision
        ↓
Search Queries
        ↓
Public Web Search
        ↓
Web Page Content Extraction
        ↓
Evidence Assembly
        ↓
Gemini-ready Context
"""

from __future__ import annotations

from web_intelligence.web_search import (
    search_public_web,
)

from web_intelligence.web_content import (
    extract_web_pages,
)

from web_intelligence.evidence import (
    assemble_web_evidence,
    build_web_context,
)


def build_search_queries(
    company_name: str = "",
    industry: str = "",
    market: str = "",
    business_decision: str = "",
) -> list[str]:

    queries = []

    if company_name.strip():

        queries.append(
            f'"{company_name.strip()}" '
            f'business market news'
        )

    if industry.strip():

        queries.append(
            f'"{industry.strip()}" '
            f'market trends {market.strip()}'
        )

    if business_decision.strip():

        queries.append(
            business_decision.strip()
            + " market business"
        )

    unique_queries = []

    for query in queries:

        query = query.strip()

        if query and query not in unique_queries:

            unique_queries.append(
                query
            )

    return unique_queries


def research_business_market(
    company_name: str = "",
    industry: str = "",
    market: str = "",
    business_decision: str = "",
    max_results_per_query: int = 3,
) -> dict:
    """
    Execute public-web research.

    Returns:
        {
            "queries": [...],
            "results": [...],
            "pages": [...],
            "evidence": [...],
            "context": "..."
        }
    """

    queries = build_search_queries(
        company_name=company_name,
        industry=industry,
        market=market,
        business_decision=business_decision,
    )

    all_results = []

    for query in queries:

        results = search_public_web(
            query=query,
            max_results=max_results_per_query,
        )

        all_results.extend(
            results
        )

    # -----------------------------------------------------
    # Deduplicate search results by URL
    # -----------------------------------------------------

    unique_results = []

    seen_urls = set()

    for result in all_results:

        if not result.url:
            continue

        if result.url in seen_urls:
            continue

        seen_urls.add(
            result.url
        )

        unique_results.append(
            result
        )

    # -----------------------------------------------------
    # Extract actual public page content
    # -----------------------------------------------------

    page_urls = [
        result.url
        for result in unique_results
        if result.url
    ]

    pages = extract_web_pages(
        page_urls
    )

    # -----------------------------------------------------
    # Build page lookup
    # -----------------------------------------------------

    page_by_url = {
        page.url: page
        for page in pages
        if page.success
    }

    # -----------------------------------------------------
    # Add extracted content to search results
    #
    # We intentionally preserve the existing result
    # objects and simply attach content dynamically.
    # -----------------------------------------------------

    for result in unique_results:

        page = page_by_url.get(
            result.url
        )

        if page:

            result.text = page.text

            if page.title and not result.title:

                result.title = page.title

    # -----------------------------------------------------
    # Existing evidence assembly
    # -----------------------------------------------------

    evidence = assemble_web_evidence(
        unique_results
    )

    # -----------------------------------------------------
    # Include extracted page content in evidence
    # -----------------------------------------------------

    for item, result in zip(
        evidence,
        unique_results,
    ):

        page = page_by_url.get(
            result.url
        )

        if page and page.success:

            item["content"] = page.text

            item["content_extracted"] = True

        else:

            item["content"] = (
                result.snippet or ""
            )

            item["content_extracted"] = False

    # -----------------------------------------------------
    # Existing Gemini-ready context
    # -----------------------------------------------------

    context = build_web_context(
        evidence
    )

    return {
        "queries": queries,
        "results": unique_results,
        "pages": pages,
        "evidence": evidence,
        "context": context,
    }