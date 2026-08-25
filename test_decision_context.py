"""
Test the Decision Context Builder.

This test does NOT modify or call the existing
Streamlit application.
"""

from business.profile import load_profile

from decision_context.context_builder import (
    build_decision_context,
)


COMPANY_ID = "TATA_PVT_LTD"


profile = load_profile(
    COMPANY_ID
)


company_profile = {
    "company_id": profile.company_id,
    "company_name": profile.company_name,
    "industry": profile.industry,
    "products": profile.products,
    "market": profile.market,
    "location": profile.location,
}


business_decision = (
    "Should I increase my investment "
    "in motor inventory?"
)


owner_answers = [
    {
        "question_id": "q1",
        "question": "What is your average monthly revenue?",
        "answer": "₹22 lakh",
        "answer_type": "currency",
        "reason": "Measures business scale.",
    },
    {
        "question_id": "q2",
        "question": "What is your current motor inventory value?",
        "answer": "₹35 lakh",
        "answer_type": "currency",
        "reason": "Measures current inventory exposure.",
    },
    {
        "question_id": "q3",
        "question": "How has motor demand changed recently?",
        "answer": "Demand increased approximately 15%.",
        "answer_type": "percentage",
        "reason": "Measures demand trend.",
    },
]


rag_evidence = [
    {
        "source": "company_test.txt",
        "content": (
            "The company sells motors to automotive "
            "customers and maintains motor inventory "
            "to support customer demand."
        ),
    },
    {
        "source": "company_test.txt",
        "content": (
            "Management should consider inventory "
            "turnover, demand trends, carrying costs, "
            "supplier lead time and available capital "
            "before increasing investment."
        ),
    },
]


print("=" * 60)
print("DECISION CONTEXT TEST")
print("=" * 60)


context = build_decision_context(
    company_profile=company_profile,
    business_decision=business_decision,
    owner_answers=owner_answers,
    rag_evidence=rag_evidence,
)


print(context)


print("\n" + "=" * 60)
print("VALIDATION")
print("=" * 60)


required_items = [
    "TATA_PVT_LTD",
    "Tata Pvt Ltd",
    "Automotive Equipment",
    "Should I increase my investment",
    "₹22 lakh",
    "₹35 lakh",
    "15%",
    "company_test.txt",
    "inventory turnover",
]


for item in required_items:

    if item not in context:

        raise AssertionError(
            f"Missing expected context: {item}"
        )


print("Business Profile: PASS")
print("Business Decision: PASS")
print("Owner Answers: PASS")
print("RAG Evidence: PASS")
print("Context Assembly: PASS")

print("\nDECISION CONTEXT TEST: PASS")