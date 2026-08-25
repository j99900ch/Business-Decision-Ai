"""
=========================================================
Business DecisionAI
Unified Decision Intelligence Test

Tests:

Business Profile
+
Owner Answers
+
Private Company RAG
+
Free Web RAG
+
Unified Context

IMPORTANT:
This test does NOT call Gemini.

Therefore it does not consume Gemini API quota.
=========================================================
"""

from business.profile import load_profile

from company_data.upload_manager import (
    CompanyKnowledgeManager,
)

from web_research.web_rag import (
    retrieve_web_evidence,
)

from decision_intelligence.unified_context import (
    build_unified_decision_context,
)


# =========================================================
# COMPANY
# =========================================================

COMPANY_ID = "TATA_PVT_LTD"


# =========================================================
# LOAD PROFILE
# =========================================================

profile = load_profile(
    COMPANY_ID
)


company_profile = {

    "company_id":
        profile.company_id,

    "company_name":
        profile.company_name,

    "industry":
        profile.industry,

    "products":
        profile.products,

    "market":
        profile.market,

    "location":
        profile.location,
}


# =========================================================
# DECISION
# =========================================================

business_decision = (
    "Should I increase my investment "
    "in motor inventory by 10%?"
)


# =========================================================
# OWNER ANSWERS
# =========================================================

owner_answers = [

    {
        "question_id": "q1",

        "question":
            "What is your average monthly revenue?",

        "answer":
            "₹22 lakh",

        "answer_type":
            "currency",

        "reason":
            "Measures business scale.",
    },


    {
        "question_id": "q2",

        "question":
            "What is your current motor inventory value?",

        "answer":
            "₹35 lakh",

        "answer_type":
            "currency",

        "reason":
            "Measures inventory exposure.",
    },


    {
        "question_id": "q3",

        "question":
            "How has motor demand changed recently?",

        "answer":
            "Demand increased approximately 15%.",

        "answer_type":
            "percentage",

        "reason":
            "Measures demand trend.",
    },
]


# =========================================================
# PRIVATE COMPANY RAG
# =========================================================

print("=" * 70)

print(
    "LOADING PRIVATE COMPANY KNOWLEDGE"
)

print("=" * 70)


company_manager = (
    CompanyKnowledgeManager(
        COMPANY_ID
    )
)


private_documents = (
    company_manager.retrieve(

        query=(
            "current motor inventory "
            "revenue demand inventory "
            "investment"
        ),

        k=4,
    )
)


private_evidence = []


for document in private_documents:

    if hasattr(
        document,
        "page_content",
    ):

        content = (
            document.page_content
        )

    else:

        content = str(
            document
        )


    metadata = getattr(
        document,
        "metadata",
        {},
    )


    private_evidence.append(
        {
            "source":
                metadata.get(
                    "source",
                    "Private company document",
                ),

            "content":
                content,
        }
    )


print(
    "Private evidence retrieved:",
    len(private_evidence),
)


# =========================================================
# PUBLIC WEB RAG
# =========================================================

print("\n" + "=" * 70)

print(
    "RETRIEVING PUBLIC MARKET INTELLIGENCE"
)

print("=" * 70)


web_result = (
    retrieve_web_evidence(

        company_name=
            profile.company_name,

        industry=
            profile.industry,

        products=
            profile.products,

        market=
            profile.market,

        decision=
            business_decision,

        max_pages=5,
    )
)


public_web_evidence = (
    web_result["evidence"]
)


print(
    "Public web evidence retrieved:",
    len(public_web_evidence),
)


# =========================================================
# BUILD UNIFIED CONTEXT
# =========================================================

print("\n" + "=" * 70)

print(
    "BUILDING UNIFIED DECISION CONTEXT"
)

print("=" * 70)


context = (
    build_unified_decision_context(

        company_profile=
            company_profile,

        business_decision=
            business_decision,

        owner_answers=
            owner_answers,

        private_company_evidence=
            private_evidence,

        public_web_evidence=
            public_web_evidence,
    )
)


print(
    context[:8000]
)


# =========================================================
# VALIDATION
# =========================================================

print("\n" + "=" * 70)

print(
    "VALIDATION"
)

print("=" * 70)


required_items = [

    "BUSINESS PROFILE",

    "TATA_PVT_LTD",

    "Tata Pvt Ltd",

    "Automotive Equipment",

    "BUSINESS DECISION",

    "Should I increase my investment",

    "OWNER-PROVIDED INFORMATION",

    "₹22 lakh",

    "₹35 lakh",

    "15%",

    "PRIVATE COMPANY KNOWLEDGE",

    "PUBLIC WEB / MARKET INTELLIGENCE",

    "DECISION INTELLIGENCE RULES",
]


for item in required_items:

    if item not in context:

        raise AssertionError(
            f"Missing context section: {item}"
        )


if not private_evidence:

    raise AssertionError(
        "Private company evidence missing."
    )


if not public_web_evidence:

    raise AssertionError(
        "Public web evidence missing."
    )


print(
    "Business Profile: PASS"
)

print(
    "Owner Questionnaire: PASS"
)

print(
    "Private Company RAG: PASS"
)

print(
    "Public Web RAG: PASS"
)

print(
    "Unified Context: PASS"
)


print("\n" + "=" * 70)

print(
    "UNIFIED DECISION CONTEXT TEST: PASS"
)

print("=" * 70)