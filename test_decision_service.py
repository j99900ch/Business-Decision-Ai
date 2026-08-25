from decision_intelligence.decision_service import (
    DecisionIntelligenceService,
)


print("=" * 70)
print("PRODUCTION DECISION SERVICE TEST")
print("=" * 70)


service = DecisionIntelligenceService(

    company_name="Tata Pvt Ltd",

    industry="Automotive Equipment",

    products="Motors",

    market="India",

    location="India",
)


result = service.analyze(

    business_decision=(
        "Should I increase my investment "
        "in motor inventory by 10%?"
    ),

    owner_answers=[
        {
            "question_id": "q1",
            "question": "Average monthly revenue?",
            "answer": "₹22 lakh",
        },
        {
            "question_id": "q2",
            "question": "Current motor inventory?",
            "answer": "₹35 lakh",
        },
        {
            "question_id": "q3",
            "question": "Recent demand trend?",
            "answer": "Demand increased approximately 15%.",
        },
    ],

    include_web_research=True,
)


print("\nPRIVATE EVIDENCE:")
print(
    len(result["private_evidence"])
)


print("\nPUBLIC WEB EVIDENCE:")
print(
    len(result["public_evidence"])
)


print("\nGEMINI RESULT:")
print("=" * 70)

print(
    result["response"]
)


if not result["response"].strip():

    raise AssertionError(
        "Gemini returned an empty response."
    )


print("\n" + "=" * 70)
print("PRODUCTION DECISION SERVICE TEST: PASS")
print("=" * 70)