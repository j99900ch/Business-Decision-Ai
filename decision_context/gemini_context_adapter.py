"""
=========================================================
Business DecisionAI
Gemini Context Adapter

Connects the new Business Decision Context to the
existing Gemini service WITHOUT modifying the existing
Gemini client or decision engine.
=========================================================
"""

from ai.gemini import generate_response
from ai.prompt import SYSTEM_PROMPT

from decision_context.context_builder import (
    build_decision_context,
)


def analyze_with_business_context(
    company_profile: dict,
    business_decision: str,
    owner_answers: list[dict] | None = None,
    rag_evidence: list[dict] | None = None,
) -> str:
    """
    Analyze a business decision using:

    - Business profile
    - Owner answers
    - RAG evidence
    - Existing Gemini service

    The existing Gemini client remains unchanged.
    """

    context = build_decision_context(
        company_profile=company_profile,
        business_decision=business_decision,
        owner_answers=owner_answers or [],
        rag_evidence=rag_evidence or [],
    )

    final_prompt = f"""
{SYSTEM_PROMPT}

==================================================
BUSINESS DECISION CONTEXT
==================================================

{context}

==================================================
ANALYSIS INSTRUCTION
==================================================

Analyze the business decision using the supplied
business context.

Important rules:

1. Use the owner-provided information as stated.
2. Use retrieved company evidence when relevant.
3. Do not invent company facts.
4. If important information is missing, mention
   the limitation in the Reason section.
5. Keep the existing required output format.
6. Give a practical recommendation.
7. Confidence must reflect the quality of the
   available information.

Return only the required decision analysis format.
"""

    return generate_response(
        final_prompt
    )