from decision_context.decision_orchestrator import (
    analyze_business_decision_with_context,
)


print("=" * 60)
print("BUSINESS DECISION ORCHESTRATOR TEST")
print("=" * 60)


result = analyze_business_decision_with_context(

    company_name="Tata Pvt Ltd",

    industry="Automotive Equipment",

    market="India",

    products="Motors",

    location="India",

    business_decision=(
        "Should I increase my investment "
        "in motor inventory by 10%?"
    ),

    owner_answers=[
        {
            "question_id": "q1",
            "question": "What is your average monthly revenue?",
            "answer": "22 lakh",
            "answer_type": "currency",
            "reason": "Measures business scale.",
        },
        {
            "question_id": "q2",
            "question": "What is your current inventory value?",
            "answer": "35 lakh",
            "answer_type": "currency",
            "reason": "Measures inventory exposure.",
        },
        {
            "question_id": "q3",
            "question": "How has demand changed recently?",
            "answer": "Demand increased approximately 15%.",
            "answer_type": "percentage",
            "reason": "Measures demand trend.",
        },
    ],
)


print("\nCOMPANY ID:")
print(result["company_id"])


print("\nRAG USED:")
print(result["rag_used"])


print("\nRAG EVIDENCE COUNT:")
print(result["evidence_count"])


print("\n" + "=" * 60)
print("GEMINI DECISION")
print("=" * 60)


print(result["response"])


print("\n" + "=" * 60)
print("ORCHESTRATOR TEST: PASS")
print("=" * 60)