"""
=========================================================
Business DecisionAI
Free Web RAG Test

IMPORTANT:
This test does NOT call Gemini.

It tests only:

Public Web Search
        ↓
Page Retrieval
        ↓
LangChain Documents
        ↓
LangChain Chunking
        ↓
Evidence Collection

Therefore it does not consume Gemini API quota.
=========================================================
"""

from web_research.web_rag import (
    retrieve_web_evidence,
    build_web_context,
)


COMPANY_NAME = "Tata Pvt Ltd"

INDUSTRY = "Automotive Equipment"

PRODUCTS = "Motors"

MARKET = "India"

DECISION = (
    "Should I increase my investment "
    "in motor inventory by 10%?"
)


print("=" * 70)

print(
    "BUSINESS DECISIONAI"
)

print(
    "FREE WEB RAG TEST"
)

print("=" * 70)


print("\nCompany:")
print(COMPANY_NAME)

print("\nIndustry:")
print(INDUSTRY)

print("\nProducts:")
print(PRODUCTS)

print("\nMarket:")
print(MARKET)

print("\nDecision:")
print(DECISION)


print("\n" + "=" * 70)

print(
    "BUILDING RESEARCH QUERIES..."
)

print("=" * 70)


result = retrieve_web_evidence(

    company_name=COMPANY_NAME,

    industry=INDUSTRY,

    products=PRODUCTS,

    market=MARKET,

    decision=DECISION,

    max_pages=6,
)


print("\nResearch Queries:")

for index, query in enumerate(
    result["queries"],
    start=1,
):

    print(
        f"{index}. {query}"
    )


print("\n" + "=" * 70)

print(
    "SEARCH RESULTS"
)

print("=" * 70)


print(
    "Results:",
    len(result["search_results"])
)


for index, item in enumerate(
    result["search_results"],
    start=1,
):

    print(
        f"\n{index}. {item.get('title')}"
    )

    print(
        item.get("url")
    )


print("\n" + "=" * 70)

print(
    "LANGCHAIN DOCUMENTS"
)

print("=" * 70)


print(
    "Documents loaded:",
    len(result["documents"])
)

print(
    "Chunks created:",
    len(result["chunks"])
)


print("\n" + "=" * 70)

print(
    "WEB EVIDENCE"
)

print("=" * 70)


for index, item in enumerate(
    result["evidence"][:5],
    start=1,
):

    print(
        f"\n--- Evidence {index} ---"
    )

    print(
        "Title:",
        item.get("title")
    )

    print(
        "URL:",
        item.get("url")
    )

    content = item.get(
        "content",
        "",
    )

    print(
        "Content preview:"
    )

    print(
        content[:500]
    )


print("\n" + "=" * 70)

print(
    "GEMINI-READY WEB CONTEXT"
)

print("=" * 70)


web_context = build_web_context(
    result["evidence"]
)


print(
    web_context[:3000]
)


print("\n" + "=" * 70)

print(
    "VALIDATION"
)

print("=" * 70)


if not result["queries"]:

    raise AssertionError(
        "No research queries generated."
    )


if not result["search_results"]:

    raise AssertionError(
        "No public web search results returned."
    )


if not result["documents"]:

    raise AssertionError(
        "No web documents loaded."
    )


if not result["chunks"]:

    raise AssertionError(
        "No LangChain chunks created."
    )


if not result["evidence"]:

    raise AssertionError(
        "No web evidence created."
    )


if not web_context.strip():

    raise AssertionError(
        "Web context is empty."
    )


print(
    "Search: PASS"
)

print(
    "Web Retrieval: PASS"
)

print(
    "LangChain Documents: PASS"
)

print(
    "LangChain Chunking: PASS"
)

print(
    "Evidence Assembly: PASS"
)

print(
    "Gemini Context Preparation: PASS"
)


print("\n" + "=" * 70)

print(
    "FREE WEB RAG TEST: PASS"
)

print("=" * 70)