"""
Test the new Business Context → Existing Gemini connection.

This does NOT modify app.py or ai/decision_engine.py.
"""

from business.profile import load_profile

from decision_context.gemini_context_adapter import (
    analyze_with_business_context,
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
        "reason": "Measures inventory exposure.",
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
print("CONTEXT → EXISTING GEMINI TEST")
print("=" * 60)

print(
    "\nCompany:",
    profile.company_name
)

print(
    "Decision:",
    business_decision
)

print("\nSending combined context to Gemini...\n")


response = analyze_with_business_context(
    company_profile=company_profile,
    business_decision=business_decision,
    owner_answers=owner_answers,
    rag_evidence=rag_evidence,
)


print("=" * 60)
print("GEMINI DECISION")
print("=" * 60)

print(response)

print("\n" + "=" * 60)
print("TEST: PASS")
print("=" * 60)