"""
Business DecisionAI
Full Intelligence Integration Test

Verifies:

    Private RAG
        +
    Public Web Search
        +
    Web Page Extraction
        +
    Evidence Fusion
        +
    Evidence-Aware Decision Engine

No Streamlit/app.py changes are made by this test.
"""

from pathlib import Path

from ai.decision_engine import (
    analyze_business_decision,
)

from evidence.evidence_fusion import (
    fuse_evidence,
)

from rag.rag_engine import (
    RAGEngine,
)

from web_intelligence.web_researcher import (
    research_business_market,
)

from web_intelligence.web_content import (
    extract_web_pages,
)


# =========================================================
# CONFIGURATION
# =========================================================

COMPANY_ID = "PRIVATE_RAG_E2E_TEST"

COMPANY_NAME = "Tata Motors"

INDUSTRY = "Automotive"

MARKET = "India"

BUSINESS_DECISION = (
    "Should the company increase investment "
    "in electric vehicle inventory?"
)

TEST_CSV = Path(
    "test_private_rag_files/company_test.csv"
)


# =========================================================
# MAIN TEST
# =========================================================

def main():

    print("=" * 70)
    print("BUSINESS DECISIONAI - FULL INTELLIGENCE TEST")
    print("=" * 70)

    # =====================================================
    # STEP 1
    # PRIVATE RAG RETRIEVAL
    # =====================================================

    print()
    print("STEP 1: PRIVATE COMPANY RAG")
    print("-" * 70)

    if not TEST_CSV.exists():

        raise RuntimeError(
            f"Test company data not found: {TEST_CSV}"
        )

    rag_engine = RAGEngine()

    private_documents = rag_engine.retrieve(
        company_id=COMPANY_ID,
        query=BUSINESS_DECISION,
        k=4,
    )

    if not private_documents:

        raise RuntimeError(
            "Private RAG returned no documents."
        )

    print(
        f"PASS - Retrieved "
        f"{len(private_documents)} private document(s)"
    )

    # =====================================================
    # STEP 2
    # PUBLIC WEB RESEARCH
    # =====================================================

    print()
    print("STEP 2: PUBLIC WEB RESEARCH")
    print("-" * 70)

    web_research = research_business_market(
        company_name=COMPANY_NAME,
        industry=INDUSTRY,
        market=MARKET,
        business_decision=BUSINESS_DECISION,
        max_results_per_query=2,
    )

    web_results = web_research.get(
        "results",
        [],
    )

    if not web_results:

        raise RuntimeError(
            "Public web research returned no results."
        )

    print(
        f"PASS - Retrieved "
        f"{len(web_results)} public result(s)"
    )

    for result in web_results[:5]:

        print(
            f"  → {result.title} | {result.url}"
        )

    # =====================================================
    # STEP 3
    # WEB PAGE CONTENT EXTRACTION
    # =====================================================

    print()
    print("STEP 3: WEB PAGE CONTENT EXTRACTION")
    print("-" * 70)

    urls = [
        result.url
        for result in web_results
        if result.url
    ]

    web_pages = extract_web_pages(
        urls=urls[:3],
        max_chars=6000,
    )

    successful_pages = [
        page
        for page in web_pages
        if page.success
        and page.text.strip()
    ]

    if not successful_pages:

        raise RuntimeError(
            "No public web page content could be extracted."
        )

    print(
        f"PASS - Extracted "
        f"{len(successful_pages)} public web page(s)"
    )

    for page in successful_pages:

        print(
            f"  → {page.title or 'Untitled'}"
            f" | {page.url}"
            f" | {len(page.text)} chars"
        )

    # =====================================================
    # STEP 4
    # BUILD WEB CONTENT EVIDENCE
    # =====================================================

    print()
    print("STEP 4: PUBLIC WEB CONTENT EVIDENCE")
    print("-" * 70)

    class WebContentEvidence:

        def __init__(
            self,
            page,
        ):

            self.title = page.title

            self.url = page.url

            self.text = page.text

            self.source = "public_web_page"

            self.snippet = page.text[:1000]

    web_content_results = [
        WebContentEvidence(page)
        for page in successful_pages
    ]

    print(
        f"PASS - Prepared "
        f"{len(web_content_results)} page-content evidence record(s)"
    )

    # =====================================================
    # STEP 5
    # EVIDENCE FUSION
    # =====================================================

    print()
    print("STEP 5: EVIDENCE FUSION")
    print("-" * 70)

    fused = fuse_evidence(
        private_documents=private_documents,
        public_results=web_content_results,
    )

    private_evidence = fused.get(
        "private_evidence",
        [],
    )

    public_evidence = fused.get(
        "public_evidence",
        [],
    )

    total_evidence = fused.get(
        "total_evidence",
        0,
    )

    evidence_context = fused.get(
        "context",
        "",
    )

    if not private_evidence:

        raise RuntimeError(
            "Private evidence was not created."
        )

    if not public_evidence:

        raise RuntimeError(
            "Public web evidence was not created."
        )

    if not evidence_context.strip():

        raise RuntimeError(
            "Evidence context is empty."
        )

    print(
        f"PASS - Private evidence: "
        f"{len(private_evidence)}"
    )

    print(
        f"PASS - Public evidence: "
        f"{len(public_evidence)}"
    )

    print(
        f"PASS - Total evidence: "
        f"{total_evidence}"
    )

    # =====================================================
    # STEP 6
    # EVIDENCE TRACEABILITY
    # =====================================================

    print()
    print("STEP 6: EVIDENCE TRACEABILITY")
    print("-" * 70)

    for item in private_evidence:

        evidence_id = item.get(
            "evidence_id",
            "",
        )

        if not evidence_id.startswith(
            "PRIVATE-"
        ):

            raise RuntimeError(
                "Invalid private evidence ID."
            )

        print(
            f"PASS - {evidence_id}"
        )

    for item in public_evidence:

        evidence_id = item.get(
            "evidence_id",
            "",
        )

        if not evidence_id.startswith(
            "WEB-"
        ):

            raise RuntimeError(
                "Invalid public evidence ID."
            )

        print(
            f"PASS - {evidence_id}"
        )

    # =====================================================
    # STEP 7
    # EVIDENCE-AWARE GEMINI DECISION
    # =====================================================

    print()
    print("STEP 7: EVIDENCE-AWARE GEMINI ANALYSIS")
    print("-" * 70)

    response = analyze_business_decision(
        BUSINESS_DECISION,
        evidence_context=evidence_context,
    )

    if not response:

        raise RuntimeError(
            "Gemini returned an empty response."
        )

    required_sections = [
        "Decision Summary:",
        "Risk Level:",
        "Confidence:",
        "Reason:",
        "Recommendation:",
    ]

    for section in required_sections:

        if section not in response:

            raise RuntimeError(
                f"Missing required output section: "
                f"{section}"
            )

        print(
            f"PASS - {section}"
        )

    print()
    print("Gemini Decision:")
    print("-" * 70)
    print(response)

    # =====================================================
    # FINAL
    # =====================================================

    print()
    print("=" * 70)
    print("FULL INTELLIGENCE INTEGRATION TEST: PASS")
    print("=" * 70)

    print()
    print("Verified:")
    print("✓ Private company RAG retrieval")
    print("✓ Public web search")
    print("✓ Public web page extraction")
    print("✓ Web content evidence preparation")
    print("✓ Private + public evidence fusion")
    print("✓ Evidence ID traceability")
    print("✓ Evidence-aware Gemini analysis")
    print("✓ Existing five-field decision format")
    print("✓ No app.py changes")


if __name__ == "__main__":
    main()