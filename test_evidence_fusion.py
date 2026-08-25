from langchain_core.documents import Document

from evidence.evidence_fusion import (
    fuse_evidence,
)
from web_intelligence.web_search import (
    WebSearchResult,
)


def main():

    print("=" * 70)
    print("BUSINESS DECISIONAI - EVIDENCE FUSION TEST")
    print("=" * 70)

    # =====================================================
    # PRIVATE TEST EVIDENCE
    # =====================================================

    private_documents = [
        Document(
            page_content=(
                "The company currently maintains "
                "120 units of motor inventory."
            ),
            metadata={
                "source": "company_inventory.txt",
                "file_type": "txt",
                "company_id": "TATA_PVT_LTD",
            },
        )
    ]

    # =====================================================
    # PUBLIC TEST EVIDENCE
    # =====================================================

    public_results = [
        WebSearchResult(
            title="Automotive Market Information",
            url="https://example.com/automotive",
            snippet=(
                "Public information about "
                "automotive market conditions."
            ),
        )
    ]

    # =====================================================
    # FUSION
    # =====================================================

    result = fuse_evidence(
        private_documents=private_documents,
        public_results=public_results,
    )

    # =====================================================
    # VALIDATION
    # =====================================================

    if len(
        result["private_evidence"]
    ) != 1:

        raise RuntimeError(
            "Private evidence fusion failed."
        )

    if len(
        result["public_evidence"]
    ) != 1:

        raise RuntimeError(
            "Public evidence fusion failed."
        )

    if result["total_evidence"] != 2:

        raise RuntimeError(
            "Evidence count is incorrect."
        )

    context = result["context"]

    required_items = [
        "PRIVATE COMPANY EVIDENCE",
        "PUBLIC WEB EVIDENCE",
        "PRIVATE-001",
        "WEB-001",
        "company_inventory.txt",
        "Automotive Market Information",
        "EVIDENCE RULES",
    ]

    for item in required_items:

        if item not in context:

            raise RuntimeError(
                f"Missing expected evidence: {item}"
            )

    print()
    print("PASS - Private evidence assembled")
    print("PASS - Public evidence assembled")
    print("PASS - Evidence IDs preserved")
    print("PASS - Source information preserved")
    print("PASS - Combined context created")

    print()
    print("--- FUSED EVIDENCE CONTEXT ---")
    print()
    print(context)

    print()
    print("=" * 70)
    print("EVIDENCE FUSION TEST: PASS")
    print("=" * 70)


if __name__ == "__main__":
    main()