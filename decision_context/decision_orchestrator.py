"""
=========================================================
Business DecisionAI
Decision Orchestrator

Safe integration layer between:

Streamlit UI
    ↓
Business Profile
    ↓
RAG Retrieval
    ↓
Decision Context
    ↓
Existing Gemini Context Adapter

IMPORTANT:
This module does NOT modify the existing:
- ai/decision_engine.py
- ai/gemini.py
- rag modules
- questionnaire modules
- UI design
=========================================================
"""

from business.profile import (
    create_profile,
    save_profile,
)

from rag.rag_engine import (
    RAGEngine,
)

from decision_context.gemini_context_adapter import (
    analyze_with_business_context,
)


def _profile_to_dict(profile):
    """
    Convert BusinessProfile dataclass into
    the dictionary expected by the context layer.
    """

    return {
        "company_id": profile.company_id,
        "company_name": profile.company_name,
        "industry": profile.industry,
        "products": profile.products,
        "market": profile.market,
        "location": profile.location,
    }


def _documents_to_evidence(documents):
    """
    Convert LangChain Document objects returned
    by the RAG retriever into the structure expected
    by DecisionContext.
    """

    evidence = []

    for document in documents or []:

        # Support LangChain Document objects
        if hasattr(document, "page_content"):

            content = str(
                document.page_content
            ).strip()

            metadata = getattr(
                document,
                "metadata",
                {},
            ) or {}

        # Also support dictionary-style results
        elif isinstance(document, dict):

            content = str(
                document.get(
                    "content",
                    document.get(
                        "page_content",
                        "",
                    ),
                )
            ).strip()

            metadata = document.get(
                "metadata",
                {},
            ) or {}

        else:

            content = str(
                document
            ).strip()

            metadata = {}

        if not content:
            continue

        source = (
            metadata.get("source")
            or metadata.get("file_name")
            or metadata.get("filename")
            or "Company Knowledge Base"
        )

        evidence.append(
            {
                "source": str(source),
                "content": content,
            }
        )

    return evidence


def build_company_context(
    company_name: str,
    industry: str = "",
    market: str = "",
    products: str = "",
    location: str = "",
):
    """
    Create and persist the business profile.

    This function is intentionally independent
    from the existing UI.
    """

    company_name = str(
        company_name or ""
    ).strip()

    if not company_name:

        raise ValueError(
            "Company name is required."
        )

    profile = create_profile(
        company_name=company_name,
        industry=industry or "",
        products=products or "",
        market=market or "",
        location=location or market or "",
    )

    save_profile(profile)

    return profile


def retrieve_company_context(
    company_id: str,
    business_decision: str,
    k: int = 4,
):
    """
    Retrieve relevant company information
    from the existing RAG system.

    RAG failure is intentionally handled safely.
    The application can still use Gemini without
    company documents.
    """

    if not company_id:
        return []

    if not business_decision.strip():
        return []

    try:

        engine = RAGEngine()

        documents = engine.retrieve(
            company_id=company_id,
            query=business_decision,
            k=k,
        )

        return _documents_to_evidence(
            documents
        )

    except Exception:
        # RAG is an enhancement layer.
        # It must never break the existing
        # business decision application.
        return []


def analyze_business_decision_with_context(
    company_name: str,
    industry: str,
    market: str,
    business_decision: str,
    products: str = "",
    location: str = "",
    owner_answers=None,
):
    """
    MAIN ORCHESTRATOR

    Combines:

    1. Business Profile
    2. Business Decision
    3. Owner Answers
    4. RAG Company Evidence
    5. Existing Gemini Context Adapter

    Returns:
        {
            "response": "...",
            "company_id": "...",
            "rag_used": True/False,
            "evidence_count": number,
        }
    """

    if not str(
        business_decision or ""
    ).strip():

        raise ValueError(
            "Business decision cannot be empty."
        )

    # -----------------------------------------------------
    # 1. CREATE / SAVE BUSINESS PROFILE
    # -----------------------------------------------------

    profile = build_company_context(
        company_name=company_name,
        industry=industry,
        market=market,
        products=products,
        location=location,
    )

    company_profile = _profile_to_dict(
        profile
    )

    # -----------------------------------------------------
    # 2. RETRIEVE COMPANY KNOWLEDGE USING RAG
    # -----------------------------------------------------

    rag_evidence = retrieve_company_context(
        company_id=profile.company_id,
        business_decision=business_decision,
        k=4,
    )

    # -----------------------------------------------------
    # 3. OWNER ANSWERS
    # -----------------------------------------------------

    safe_owner_answers = (
        owner_answers
        if isinstance(owner_answers, list)
        else []
    )

    # -----------------------------------------------------
    # 4. SEND EVERYTHING TO EXISTING
    #    DECISION CONTEXT + GEMINI
    # -----------------------------------------------------

    response = analyze_with_business_context(
        company_profile=company_profile,
        business_decision=business_decision,
        owner_answers=safe_owner_answers,
        rag_evidence=rag_evidence,
    )

    return {
        "response": response,
        "company_id": profile.company_id,
        "rag_used": len(rag_evidence) > 0,
        "evidence_count": len(rag_evidence),
    }