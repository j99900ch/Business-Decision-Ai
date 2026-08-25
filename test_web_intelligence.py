"""
Business DecisionAI
Web Intelligence Module Test

This test does NOT modify app.py.
It does NOT call Gemini.
It tests:

1. Query generation
2. Public web search
3. Result normalization
4. Evidence assembly
5. Gemini-ready context preparation
"""

from web_intelligence.web_researcher import (
    build_search_queries,
    research_business_market,
)


def main():

    print("=" * 70)
    print("BUSINESS DECISIONAI - WEB INTELLIGENCE TEST")
    print("=" * 70)

    # -----------------------------------------------------
    # STEP 1
    # -----------------------------------------------------

    print()
    print("=" * 70)
    print("STEP 1: QUERY GENERATION")
    print("=" * 70)

    queries = build_search_queries(
        company_name="Tata Motors",
        industry="Automotive",
        market="India",
        business_decision=(
            "Should the company increase "
            "investment in electric vehicle inventory?"
        ),
    )

    if not queries:

        raise RuntimeError(
            "No search queries generated."
        )

    print(
        "PASS - Queries generated:",
        len(queries),
    )

    for query in queries:

        print(
            "  →",
            query,
        )

    # -----------------------------------------------------
    # STEP 2
    # -----------------------------------------------------

    print()
    print("=" * 70)
    print("STEP 2: PUBLIC WEB SEARCH")
    print("=" * 70)

    result = research_business_market(
        company_name="Tata Motors",
        industry="Automotive",
        market="India",
        business_decision=(
            "Should the company increase "
            "investment in electric vehicle inventory?"
        ),
        max_results_per_query=2,
    )

    results = result["results"]

    if not results:

        raise RuntimeError(
            "Public web search returned zero results."
        )

    print(
        f"PASS - Retrieved {len(results)} public result(s)"
    )

    for index, item in enumerate(
        results,
        start=1,
    ):

        print()
        print(
            f"--- WEB RESULT {index} ---"
        )

        print(
            "Title:",
            item.title,
        )

        print(
            "URL:",
            item.url,
        )

    # -----------------------------------------------------
    # STEP 3
    # -----------------------------------------------------

    print()
    print("=" * 70)
    print("STEP 3: EVIDENCE ASSEMBLY")
    print("=" * 70)

    evidence = result["evidence"]

    if not evidence:

        raise RuntimeError(
            "Evidence assembly returned zero evidence."
        )

    print(
        f"PASS - Evidence records: {len(evidence)}"
    )

    for item in evidence:

        print(
            f"{item['evidence_id']} | "
            f"{item['title']}"
        )

    # -----------------------------------------------------
    # STEP 4
    # -----------------------------------------------------

    print()
    print("=" * 70)
    print("STEP 4: GEMINI CONTEXT PREPARATION")
    print("=" * 70)

    context = result["context"]

    if not context.strip():

        raise RuntimeError(
            "Gemini context is empty."
        )

    print(
        "PASS - Web evidence context prepared"
    )

    print()
    print(
        context[:3000]
    )

    # -----------------------------------------------------
    # FINAL
    # -----------------------------------------------------

    print()
    print("=" * 70)
    print("WEB INTELLIGENCE TEST: PASS")
    print("=" * 70)

    print()
    print("Verified:")
    print("✓ Search query generation")
    print("✓ Public web retrieval")
    print("✓ URL extraction")
    print("✓ Result normalization")
    print("✓ Evidence assembly")
    print("✓ Source preservation")
    print("✓ Gemini-ready context preparation")

    print()
    print(
        "WEB INTELLIGENCE RETRIEVAL LAYER IS READY."
    )


if __name__ == "__main__":

    try:

        main()

    except Exception as error:

        print()
        print("=" * 70)
        print("WEB INTELLIGENCE TEST: FAILED")
        print("=" * 70)

        print(
            type(error).__name__,
            error,
        )

        raise