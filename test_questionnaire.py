"""
Test the Business DecisionAI questionnaire independently.

This test does NOT start Streamlit and does NOT modify
the existing decision engine.
"""

from business.profile import load_profile

from questionnaire.interview_engine import (
    BusinessInterview,
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
    "Should I increase my investment in "
    "motor inventory?"
)


print("=" * 60)
print("BUSINESS INTERVIEW TEST")
print("=" * 60)

print(
    "Company:",
    profile.company_name
)

print(
    "Decision:",
    business_decision
)


interview = BusinessInterview(
    company_profile=company_profile,
    business_decision=business_decision,
)


print("\nGenerating questions...\n")


questions = interview.generate_questions()


print("=" * 60)
print("GENERATED QUESTIONS")
print("=" * 60)


for question in questions:

    print(
        f"\n{question['id']}. "
        f"{question['question']}"
    )

    print(
        f"Reason: {question['reason']}"
    )

    print(
        f"Answer type: "
        f"{question['answer_type']}"
    )


print("\n" + "=" * 60)
print("TESTING ANSWERS")
print("=" * 60)


# For testing only, provide sample answers.
sample_answers = [
    "2200000",
    "3500000",
    "15%",
    "700000",
    "10%",
    "45 days",
    "Medium",
]


for question, answer in zip(
    questions,
    sample_answers,
):

    interview.add_answer(
        question_id=question["id"],
        answer=answer,
    )


print(
    "\nAnswered:",
    interview.get_answered_count(),
    "/",
    interview.get_question_count(),
)


print(
    "Complete:",
    interview.is_complete(),
)


print("\nStructured answers:\n")


for answer in interview.get_answers_as_dict():

    print(answer)