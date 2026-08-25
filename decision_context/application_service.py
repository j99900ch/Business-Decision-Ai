"""
=========================================================
Business DecisionAI
Application Decision Service

This module connects the already-tested components:

1. Business Profile
2. AI Questionnaire
3. Owner Answers
4. RAG Retrieval
5. Decision Context
6. Existing Gemini Context Adapter

IMPORTANT:
This module does NOT modify the existing:
- Gemini client
- Decision engine
- Questionnaire engine
- RAG engine
- Decision Context Builder
=========================================================
"""

from business.profile import (
    BusinessProfile,
    create_profile,
    save_profile,
)

from questionnaire.interview_engine import (
    BusinessInterview,
)

from rag.rag_engine import (
    RAGEngine,
)

from decision_context.gemini_context_adapter import (
    analyze_with_business_context,
)


class BusinessDecisionService:
    """
    Safe orchestration layer for the Streamlit application.

    Existing modules remain untouched.
    """

    def __init__(
        self,
        company_name: str,
        industry: str = "",
        products: str = "",
        market: str = "",
        location: str = "",
    ):

        if not company_name.strip():

            raise ValueError(
                "Company name is required."
            )

        self.profile: BusinessProfile = create_profile(
            company_name=company_name,
            industry=industry,
            products=products,
            market=market,
            location=location,
        )

        self.company_profile = {
            "company_id": self.profile.company_id,
            "company_name": self.profile.company_name,
            "industry": self.profile.industry,
            "products": self.profile.products,
            "market": self.profile.market,
            "location": self.profile.location,
        }

        self.rag = RAGEngine()


    # =====================================================
    # PROFILE
    # =====================================================

    def save_business_profile(self):
        """
        Save the company profile using the existing
        business profile module.
        """

        return save_profile(
            self.profile
        )


    # =====================================================
    # QUESTIONNAIRE
    # =====================================================

    def create_interview(
        self,
        business_decision: str,
    ) -> BusinessInterview:
        """
        Create the already-tested AI business interview.
        """

        if not business_decision.strip():

            raise ValueError(
                "Business decision cannot be empty."
            )

        return BusinessInterview(
            company_profile=self.company_profile,
            business_decision=business_decision.strip(),
        )


    # =====================================================
    # RAG
    # =====================================================

    def retrieve_company_knowledge(
        self,
        business_decision: str,
        k: int = 4,
    ) -> list[dict]:
        """
        Retrieve company-specific evidence using
        the existing RAG engine.

        The method is intentionally defensive because
        LangChain Document objects and dictionaries can
        both be returned by retrieval implementations.
        """

        if not business_decision.strip():

            return []

        try:

            documents = self.rag.retrieve(
                company_id=self.profile.company_id,
                query=business_decision.strip(),
                k=k,
            )

        except Exception:
            # If the company does not have an indexed
            # knowledge base yet, the decision can still
            # continue using profile + questionnaire data.

            return []

        evidence = []

        for document in documents or []:

            # ---------------------------------------------
            # LangChain Document
            # ---------------------------------------------

            if hasattr(
                document,
                "page_content",
            ):

                content = str(
                    document.page_content
                ).strip()

                metadata = getattr(
                    document,
                    "metadata",
                    {},
                ) or {}

                source = str(
                    metadata.get(
                        "source",
                        metadata.get(
                            "file_name",
                            "Company knowledge base",
                        ),
                    )
                )

            # ---------------------------------------------
            # Dictionary
            # ---------------------------------------------

            elif isinstance(
                document,
                dict,
            ):

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

                source = str(
                    document.get(
                        "source",
                        metadata.get(
                            "source",
                            "Company knowledge base",
                        ),
                    )
                )

            # ---------------------------------------------
            # Fallback
            # ---------------------------------------------

            else:

                content = str(
                    document
                ).strip()

                source = (
                    "Company knowledge base"
                )

            if content:

                evidence.append(
                    {
                        "source": source,
                        "content": content,
                    }
                )

        return evidence


    # =====================================================
    # FINAL DECISION
    # =====================================================

    def analyze(
        self,
        business_decision: str,
        owner_answers: list[dict] | None = None,
        rag_evidence: list[dict] | None = None,
    ) -> str:
        """
        Send the complete business context to the
        existing Gemini context adapter.
        """

        return analyze_with_business_context(
            company_profile=self.company_profile,
            business_decision=business_decision,
            owner_answers=owner_answers or [],
            rag_evidence=rag_evidence or [],
        )


    # =====================================================
    # COMPLETE PIPELINE
    # =====================================================

    def prepare_analysis(
        self,
        business_decision: str,
        owner_answers: list[dict] | None = None,
    ) -> dict:
        """
        Prepare the complete decision package.

        This method does not call Gemini.

        It prepares:

        Business Profile
        +
        Owner Answers
        +
        RAG Evidence
        """

        rag_evidence = (
            self.retrieve_company_knowledge(
                business_decision=business_decision,
                k=4,
            )
        )

        return {
            "company_profile": self.company_profile,
            "business_decision": business_decision,
            "owner_answers": owner_answers or [],
            "rag_evidence": rag_evidence,
        }


    def run_analysis(
        self,
        business_decision: str,
        owner_answers: list[dict] | None = None,
    ) -> dict:
        """
        Execute the complete pipeline.
        """

        package = self.prepare_analysis(
            business_decision=business_decision,
            owner_answers=owner_answers,
        )

        response = self.analyze(
            business_decision=package[
                "business_decision"
            ],
            owner_answers=package[
                "owner_answers"
            ],
            rag_evidence=package[
                "rag_evidence"
            ],
        )

        package["response"] = response

        return package