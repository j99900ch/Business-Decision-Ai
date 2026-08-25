"""
=========================================================
Business DecisionAI
Production Decision Intelligence Service

Combines:

1. Business Profile
2. Private Company RAG
3. Public Web RAG
4. Optional Owner Answers
5. Existing Gemini Context Adapter

IMPORTANT:
Existing tested modules are not modified.
=========================================================
"""

from business.profile import (
    create_profile,
    save_profile,
)

from company_data.upload_manager import (
    CompanyKnowledgeManager,
)

from web_research.web_rag import (
    retrieve_web_evidence,
)

from decision_intelligence.unified_context import (
    build_unified_decision_context,
)

from ai.gemini import generate_response
from ai.prompt import SYSTEM_PROMPT


class DecisionIntelligenceService:

    def __init__(
        self,
        company_name: str,
        industry: str = "",
        products: str = "",
        market: str = "",
        location: str = "",
    ):

        company_name = str(
            company_name
        ).strip()

        if not company_name:

            raise ValueError(
                "Company name is required."
            )

        self.profile = create_profile(
            company_name=company_name,
            industry=industry,
            products=products,
            market=market,
            location=location,
        )

        save_profile(
            self.profile
        )

        self.company_manager = (
            CompanyKnowledgeManager(
                self.profile.company_id
            )
        )


    # =====================================================
    # COMPANY DOCUMENT
    # =====================================================

    def add_company_document(
        self,
        file_path: str,
    ) -> dict:

        return self.company_manager.add_document(
            file_path
        )


    # =====================================================
    # LIST DOCUMENTS
    # =====================================================

    def list_company_documents(self):

        return self.company_manager.list_documents()


    # =====================================================
    # PRIVATE COMPANY RAG
    # =====================================================

    def retrieve_private_knowledge(
        self,
        decision: str,
        k: int = 4,
    ):

        try:

            documents = (
                self.company_manager.retrieve(
                    query=decision,
                    k=k,
                )
            )

        except Exception:

            return []


        evidence = []


        for document in documents:

            content = getattr(
                document,
                "page_content",
                "",
            )


            if not content:

                content = str(
                    document
                )


            metadata = getattr(
                document,
                "metadata",
                {},
            )


            evidence.append(
                {
                    "source": metadata.get(
                        "source",
                        "Private company document",
                    ),

                    "content": content,
                }
            )


        return evidence


    # =====================================================
    # PUBLIC WEB RESEARCH
    # =====================================================

    def retrieve_public_market_intelligence(
        self,
        decision: str,
        max_pages: int = 5,
    ):

        try:

            result = retrieve_web_evidence(

                company_name=
                    self.profile.company_name,

                industry=
                    self.profile.industry,

                products=
                    self.profile.products,

                market=
                    self.profile.market,

                decision=
                    decision,

                max_pages=max_pages,
            )

            return result.get(
                "evidence",
                []
            )

        except Exception:

            return []


    # =====================================================
    # FINAL ANALYSIS
    # =====================================================

    def analyze(
        self,
        business_decision: str,
        owner_answers=None,
        include_web_research=True,
    ):

        business_decision = str(
            business_decision
        ).strip()


        if not business_decision:

            raise ValueError(
                "Business decision is required."
            )


        # -------------------------------------------------
        # PROFILE
        # -------------------------------------------------

        company_profile = {

            "company_id":
                self.profile.company_id,

            "company_name":
                self.profile.company_name,

            "industry":
                self.profile.industry,

            "products":
                self.profile.products,

            "market":
                self.profile.market,

            "location":
                self.profile.location,
        }


        # -------------------------------------------------
        # PRIVATE RAG
        # -------------------------------------------------

        private_evidence = (
            self.retrieve_private_knowledge(
                decision=business_decision,
                k=4,
            )
        )


        # -------------------------------------------------
        # PUBLIC WEB RAG
        # -------------------------------------------------

        public_evidence = []


        if include_web_research:

            public_evidence = (
                self.retrieve_public_market_intelligence(
                    decision=business_decision,
                    max_pages=5,
                )
            )


        # -------------------------------------------------
        # UNIFIED CONTEXT
        # -------------------------------------------------

        unified_context = (
            build_unified_decision_context(

                company_profile=
                    company_profile,

                business_decision=
                    business_decision,

                owner_answers=
                    owner_answers or [],

                private_company_evidence=
                    private_evidence,

                public_web_evidence=
                    public_evidence,
            )
        )


        # -------------------------------------------------
        # ONE GEMINI REQUEST
        # -------------------------------------------------

        final_prompt = f"""
{SYSTEM_PROMPT}

==================================================
BUSINESS DECISION INTELLIGENCE
==================================================

{unified_context}

==================================================
FINAL ANALYSIS RULES
==================================================

Analyze the decision using all supplied information.

SOURCE PRIORITY:

1. Owner-provided information
2. Private company evidence
3. Public market intelligence
4. General business reasoning

IMPORTANT:

- Do not invent company facts.
- Do not treat public web information as private company
  information.
- Clearly consider current market conditions when
  public evidence is available.
- If evidence is insufficient, reduce confidence.
- Mention important missing information in Reason.
- Give practical business guidance.
- Do not claim certainty.
- This is decision support, not financial advice.

Return ONLY this format:

Decision Summary:
<short summary>

Risk Level:
Low / Medium / High

Confidence:
<number between 0 and 100>

Reason:
1. <point>
2. <point>
3. <point>

Recommendation:
<clear actionable recommendation>
"""


        response = generate_response(
            final_prompt
        )


        return {
            "response": response,

            "company_profile":
                company_profile,

            "private_evidence":
                private_evidence,

            "public_evidence":
                public_evidence,

            "owner_answers":
                owner_answers or [],
        }