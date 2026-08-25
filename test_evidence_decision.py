"""
Business DecisionAI
Evidence-Aware Decision Engine Test

Purpose:
    Verify that the existing decision engine can accept
    optional private/public evidence without changing the
    existing Gemini output format.

This test does not modify:
    - app.py
    - ai/gemini.py
    - RAG
    - Web Intelligence
    - Evidence Fusion
"""

from ai.decision_engine import analyze_business_decision


def main():

    print("=" * 70)
    print("EVIDENCE-AWARE DECISION ENGINE TEST")
    print("=" * 70)

    decision = (
        "Should the company increase motor inventory "
        "investment by 15 percent?"
    )

    evidence_context = """
PRIVATE COMPANY EVIDENCE

Evidence ID: PRIVATE-001
Source: company_test.csv
Content:
Current motor inventory is 120 units and current demand
is 95 units for Motor A.

PUBLIC WEB EVIDENCE

Evidence ID: WEB-001
Title: Automotive Market Information
Source: public_web
URL: https://example.com
Content:
Public market information should be considered only when
relevant to the inventory decision.

EVIDENCE RULES

Use the supplied evidence when relevant.
Do not invent facts that are not supported by the evidence.
Distinguish private company evidence from public web evidence.
If evidence is insufficient, reduce confidence rather than
inventing information.
"""

    print()
    print("STEP 1: BUSINESS DECISION")
    print("-" * 70)
    print(decision)

    print()
    print("STEP 2: EVIDENCE CONTEXT")
    print("-" * 70)
    print("Private + public evidence prepared.")

    print()
    print("STEP 3: GEMINI DECISION ANALYSIS")
    print("-" * 70)

    response = analyze_business_decision(
        decision,
        evidence_context=evidence_context,
    )

    if not response:
        raise RuntimeError(
            "Decision engine returned an empty response."
        )

    print(response)

    required_sections = [
        "Decision Summary:",
        "Risk Level:",
        "Confidence:",
        "Reason:",
        "Recommendation:",
    ]

    print()
    print("STEP 4: OUTPUT FORMAT VALIDATION")
    print("-" * 70)

    for section in required_sections:

        if section not in response:

            raise RuntimeError(
                f"Missing required output section: {section}"
            )

        print(f"PASS - {section}")

    print()
    print("=" * 70)
    print("EVIDENCE-AWARE DECISION ENGINE TEST: PASS")
    print("=" * 70)

    print()
    print("Verified:")
    print("✓ Existing Gemini integration remains usable")
    print("✓ Evidence context can be supplied")
    print("✓ Existing decision output format is preserved")
    print("✓ Decision Summary is present")
    print("✓ Risk Level is present")
    print("✓ Confidence is present")
    print("✓ Reason is present")
    print("✓ Recommendation is present")


if __name__ == "__main__":
    main()