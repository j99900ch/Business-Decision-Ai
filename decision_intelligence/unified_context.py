"""
=========================================================
Business DecisionAI
Unified Decision Intelligence Context

Combines four information layers:

1. Business Profile
2. Owner Questionnaire
3. Private Company RAG
4. Public Web RAG

This module does NOT modify:

    app.py
    ai/*
    rag/*
    questionnaire/*
    decision_context/*

It creates a clean unified package for the final
decision-analysis layer.
=========================================================
"""

from dataclasses import dataclass, field


# =========================================================
# DATA MODEL
# =========================================================

@dataclass
class UnifiedDecisionContext:

    company_profile: dict

    business_decision: str

    owner_answers: list[dict] = field(
        default_factory=list
    )

    private_company_evidence: list[dict] = field(
        default_factory=list
    )

    public_web_evidence: list[dict] = field(
        default_factory=list
    )


    # =====================================================
    # BUILD
    # =====================================================

    def build(self) -> str:

        if not self.business_decision.strip():

            raise ValueError(
                "Business decision cannot be empty."
            )


        sections = []


        # =================================================
        # 1. BUSINESS PROFILE
        # =================================================

        profile_lines = [
            "BUSINESS PROFILE",
            "================",
        ]


        for key, value in (
            self.company_profile or {}
        ).items():

            if (
                value is not None
                and str(value).strip()
            ):

                profile_lines.append(
                    f"{key}: {value}"
                )


        sections.append(
            "\n".join(profile_lines)
        )


        # =================================================
        # 2. BUSINESS DECISION
        # =================================================

        sections.append(
            "\n".join(
                [
                    "BUSINESS DECISION",
                    "=================",
                    self.business_decision.strip(),
                ]
            )
        )


        # =================================================
        # 3. OWNER ANSWERS
        # =================================================

        owner_lines = [
            "OWNER-PROVIDED INFORMATION",
            "===========================",
        ]


        if self.owner_answers:

            for index, item in enumerate(
                self.owner_answers,
                start=1,
            ):

                question = str(
                    item.get(
                        "question",
                        "",
                    )
                ).strip()

                answer = str(
                    item.get(
                        "answer",
                        "",
                    )
                ).strip()


                if question and answer:

                    owner_lines.append(
                        f"{index}. Question: {question}"
                    )

                    owner_lines.append(
                        f"   Answer: {answer}"
                    )

                    owner_lines.append("")


        else:

            owner_lines.append(
                "No additional owner information provided."
            )


        sections.append(
            "\n".join(owner_lines)
        )


        # =================================================
        # 4. PRIVATE COMPANY RAG
        # =================================================

        private_lines = [
            "PRIVATE COMPANY KNOWLEDGE",
            "=========================",
        ]


        if self.private_company_evidence:

            for index, item in enumerate(
                self.private_company_evidence,
                start=1,
            ):

                content = str(
                    item.get(
                        "content",
                        "",
                    )
                ).strip()


                source = str(
                    item.get(
                        "source",
                        "Private company document",
                    )
                ).strip()


                if content:

                    private_lines.append(
                        f"Private Evidence {index}:"
                    )

                    private_lines.append(
                        f"Source: {source}"
                    )

                    private_lines.append(
                        content
                    )

                    private_lines.append("")


        else:

            private_lines.append(
                "No private company evidence retrieved."
            )


        sections.append(
            "\n".join(private_lines)
        )


        # =================================================
        # 5. PUBLIC WEB RAG
        # =================================================

        web_lines = [
            "PUBLIC WEB / MARKET INTELLIGENCE",
            "================================",
        ]


        if self.public_web_evidence:

            for index, item in enumerate(
                self.public_web_evidence,
                start=1,
            ):

                title = str(
                    item.get(
                        "title",
                        "Public web source",
                    )
                ).strip()


                url = str(
                    item.get(
                        "url",
                        "",
                    )
                ).strip()


                content = str(
                    item.get(
                        "content",
                        "",
                    )
                ).strip()


                if content:

                    web_lines.append(
                        f"Web Evidence {index}:"
                    )

                    web_lines.append(
                        f"Title: {title}"
                    )

                    if url:

                        web_lines.append(
                            f"URL: {url}"
                        )

                    web_lines.append(
                        content
                    )

                    web_lines.append("")


        else:

            web_lines.append(
                "No public web evidence retrieved."
            )


        sections.append(
            "\n".join(web_lines)
        )


        # =================================================
        # 6. SOURCE RULES
        # =================================================

        sections.append(
            "\n".join(
                [
                    "DECISION INTELLIGENCE RULES",
                    "============================",
                    (
                        "Use business profile information "
                        "as company identity."
                    ),
                    (
                        "Treat owner answers as "
                        "owner-provided information."
                    ),
                    (
                        "Treat private company evidence "
                        "as internal company knowledge."
                    ),
                    (
                        "Treat public web evidence as "
                        "external market intelligence."
                    ),
                    (
                        "Do not mix private company facts "
                        "with public market facts."
                    ),
                    (
                        "Do not invent missing information."
                    ),
                    (
                        "If important information is missing, "
                        "state the limitation."
                    ),
                ]
            )
        )


        return "\n\n".join(
            sections
        )


# =========================================================
# CONVENIENCE FUNCTION
# =========================================================

def build_unified_decision_context(
    company_profile: dict,
    business_decision: str,
    owner_answers: list[dict] | None = None,
    private_company_evidence: list[dict] | None = None,
    public_web_evidence: list[dict] | None = None,
) -> str:

    context = UnifiedDecisionContext(

        company_profile=company_profile,

        business_decision=business_decision,

        owner_answers=owner_answers or [],

        private_company_evidence=(
            private_company_evidence or []
        ),

        public_web_evidence=(
            public_web_evidence or []
        ),
    )


    return context.build()