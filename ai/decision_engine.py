"""
=========================================================
Business DecisionAI
Decision Analysis Engine
=========================================================
"""

from ai.prompt import SYSTEM_PROMPT
from ai.gemini import generate_response


def analyze_business_decision(
    user_decision: str,
    evidence_context: str = "",
) -> str:
    """
    Analyze a business decision using Gemini AI.

    Parameters
    ----------
    user_decision : str
        Business decision to analyze.

    evidence_context : str, optional
        Private RAG and/or public web evidence.
        If empty, the original decision-analysis behavior
        is preserved.

    Returns
    -------
    str
        Gemini decision analysis.
    """

    if not user_decision.strip():

        return """
Decision Summary:
No decision provided.

Risk Level:
Unknown

Confidence:
0

Reason:
Please enter a business decision.

Recommendation:
Type or speak a business decision first.
"""

    evidence_context = (
        evidence_context.strip()
        if evidence_context
        else ""
    )

    # -----------------------------------------------------
    # BUILD EVIDENCE SECTION
    # -----------------------------------------------------

    evidence_section = ""

    if evidence_context:

        evidence_section = f"""
------------------------------------------------------

EVIDENCE CONTEXT

The following evidence was retrieved from the
company's private knowledge base and/or public web
research.

Use evidence only when it is relevant to the decision.

Do not invent facts that are not supported by the
provided evidence.

Distinguish private company evidence from public
web evidence.

If the available evidence is insufficient, reduce
confidence rather than inventing information.

{evidence_context}

------------------------------------------------------
"""

    # -----------------------------------------------------
    # BUILD FINAL PROMPT
    # -----------------------------------------------------

    final_prompt = f"""
{SYSTEM_PROMPT}

------------------------------------------------------

Business Decision:

{user_decision}

{evidence_section}

Analyze this decision carefully.
"""

    response = generate_response(
        final_prompt
    )

    return response