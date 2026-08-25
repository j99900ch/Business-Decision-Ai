from web_intelligence.web_researcher import (
    research_business_market,
)


def main():

    print("=" * 70)
    print("WEB RESEARCH + PAGE EXTRACTION TEST")
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

    print()
    print("STEP 1: SEARCH")
    print("-" * 70)

    print(
        "Queries:",
        len(result["queries"]),
    )

    print(
        "Search results:",
        len(result["results"]),
    )

    if not result["results"]:

        raise RuntimeError(
            "No public web search results returned."
        )

    print("PASS - Public search returned results")

    print()
    print("STEP 2: PAGE EXTRACTION")
    print("-" * 70)

    successful_pages = [
        page
        for page in result["pages"]
        if page.success
    ]

    print(
        "Pages attempted:",
        len(result["pages"]),
    )

    print(
        "Pages successfully extracted:",
        len(successful_pages),
    )

    if not successful_pages:

        raise RuntimeError(
            "No web page content could be extracted."
        )

    print(
        "PASS - Public page content extracted"
    )

    print()
    print("STEP 3: EVIDENCE")
    print("-" * 70)

    print(
        "Evidence records:",
        len(result["evidence"]),
    )

    extracted_count = sum(
        1
        for item in result["evidence"]
        if item.get(
            "content_extracted",
            False,
        )
    )

    print(
        "Evidence with page content:",
        extracted_count,
    )

    if extracted_count == 0:

        raise RuntimeError(
            "Evidence contains no extracted page content."
        )

    print(
        "PASS - Extracted page content attached "
        "to evidence"
    )

    print()
    print("STEP 4: GEMINI CONTEXT")
    print("-" * 70)

    context = result["context"]

    if not context.strip():

        raise RuntimeError(
            "Web context is empty."
        )

    print(
        "Context characters:",
        len(context),
    )

    print(
        "PASS - Web context prepared"
    )

    print()
    print("--- SAMPLE CONTEXT ---")
    print(
        context[:2500]
    )

    print()
    print("=" * 70)
    print("WEB RESEARCH + PAGE EXTRACTION TEST: PASS")
    print("=" * 70)


if __name__ == "__main__":
    main()