"""
Business DecisionAI
Evidence-Aware Decision Integration

Purpose:
    Combine the user's business decision with already-prepared
    private/public evidence and send the resulting context
    through the existing decision engine.

Important:
    - Does NOT modify ai/decision_engine.py
    - Does NOT modify Gemini integration
    - Does NOT modify RAG
    - Does NOT modify Web Search
    - Does NOT modify Evidence Fusion
"""

from __future__ import annotations

from typing import Iterable

from ai.decision_engine import (
    analyze_business_decision,
)
from evidence.evidence_fusion import (
    fuse_evidence,
)


def analyze_with_evidence(
    user_decision: str,
    private_documents: Iterable = None,
    public_results: Iterable = None,
) -> str:

    if not user_decision or not user_decision.strip():

        return analyze_business_decision(
            user_decision
        )

    fused = fuse_evidence(
        private_documents=private_documents,
        public_results=public_results,
    )

    evidence_context = fused.get(
        "context",
        "",
    )

    final_decision = f"""
Business Decision:

{user_decision.strip()}

======================================================
EVIDENCE AVAILABLE FOR THIS DECISION
======================================================

{evidence_context}

======================================================
EVIDENCE-AWARE DECISION INSTRUCTION
======================================================

Analyze the business decision using the evidence above
when it is relevant.

Important rules:

1. Distinguish private company evidence from public web
   evidence.

2. Do not invent facts that are not present in the
   business decision or supplied evidence.

3. Do not treat missing evidence as a known fact.

4. Use public web evidence only when relevant.

5. Consider the private company information as internal
   business context.

6. Base the final risk, confidence, reasoning and
   recommendation on the available evidence.

======================================================
END OF EVIDENCE
======================================================
"""

    return analyze_business_decision(
        final_decision
    )