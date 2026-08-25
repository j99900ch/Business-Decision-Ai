"""
=========================================================
Business DecisionAI
Web Research Test

This test ONLY tests the new web research layer.

Existing application files are NOT modified.
=========================================================
"""

from web_research.web_researcher import (
    research_business_market,
)


COMPANY_NAME = "Tata Pvt Ltd"

INDUSTRY = "Automotive Equipment"

PRODUCTS = "Motors"

MARKET = "India"

BUSINESS_DECISION = (
    "Should I increase my investment "
    "in motor inventory by 10%?"
)


print("=" * 70)

print(
    "BUSINESS DECISIONAI"
)

print(
    "LIVE WEB MARKET RESEARCH TEST"
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
print(BUSINESS_DECISION)


print("\n" + "=" * 70)

print(
    "SEARCHING PUBLIC WEB..."
)

print("=" * 70)


result = research_business_market(

    company_name=COMPANY_NAME,

    industry=INDUSTRY,

    products=PRODUCTS,

    market=MARKET,

    business_decision=BUSINESS_DECISION,
)


print("\n" + "=" * 70)

print(
    "MARKET RESEARCH"
)

print("=" * 70)

print(
    result.answer
)


print("\n" + "=" * 70)

print(
    "SEARCH QUERIES USED"
)

print("=" * 70)


if result.search_queries:

    for index, query in enumerate(
        result.search_queries,
        start=1,
    ):

        print(
            f"{index}. {query}"
        )

else:

    print(
        "No search queries were returned."
    )


print("\n" + "=" * 70)

print(
    "WEB SOURCES"
)

print("=" * 70)


if result.sources:

    for index, source in enumerate(
        result.sources,
        start=1,
    ):

        print(
            f"\nSource {index}"
        )

        print(
            "Title:",
            source.get("title")
        )

        print(
            "URL:",
            source.get("url")
        )

else:

    print(
        "No URL citations were returned."
    )


print("\n" + "=" * 70)

print(
    "WEB RESEARCH TEST: PASS"
)

print("=" * 70)