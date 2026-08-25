"""
=========================================================
Business DecisionAI
Decision Context Builder

Combines:
- Business Profile
- Owner Answers
- RAG Evidence

This module does NOT modify the existing Gemini
decision engine.
=========================================================
"""

from dataclasses import dataclass, field


@dataclass
class DecisionContext:
    company_profile: dict
    business_decision: str
    owner_answers: list[dict] = field(default_factory=list)
    rag_evidence: list[dict] = field(default_factory=list)

    def build(self) -> str:
        """
        Build a clean context package for the AI decision layer.
        """

        if not self.business_decision.strip():
            raise ValueError(
                "Business decision cannot be empty."
            )

        sections = []

        # -------------------------------------------------
        # BUSINESS PROFILE
        # -------------------------------------------------

        profile_lines = [
            "BUSINESS PROFILE",
            "----------------",
        ]

        for key, value in self.company_profile.items():

            if value is not None and str(value).strip():

                profile_lines.append(
                    f"{key}: {value}"
                )

        sections.append(
            "\n".join(profile_lines)
        )

        # -------------------------------------------------
        # BUSINESS DECISION
        # -------------------------------------------------

        sections.append(
            "\n".join([
                "BUSINESS DECISION",
                "-----------------",
                self.business_decision.strip(),
            ])
        )

        # -------------------------------------------------
        # OWNER ANSWERS
        # -------------------------------------------------

        answer_lines = [
            "OWNER-PROVIDED INFORMATION",
            "---------------------------",
        ]

        if self.owner_answers:

            for item in self.owner_answers:

                question = str(
                    item.get("question", "")
                ).strip()

                answer = str(
                    item.get("answer", "")
                ).strip()

                if question and answer:

                    answer_lines.append(
                        f"Question: {question}"
                    )

                    answer_lines.append(
                        f"Answer: {answer}"
                    )

                    answer_lines.append("")

        else:

            answer_lines.append(
                "No additional owner information provided."
            )

        sections.append(
            "\n".join(answer_lines)
        )

        # -------------------------------------------------
        # RAG EVIDENCE
        # -------------------------------------------------

        evidence_lines = [
            "COMPANY KNOWLEDGE / RAG EVIDENCE",
            "--------------------------------",
        ]

        if self.rag_evidence:

            for index, item in enumerate(
                self.rag_evidence,
                start=1,
            ):

                content = str(
                    item.get("content", "")
                ).strip()

                source = str(
                    item.get("source", "Company document")
                ).strip()

                if content:

                    evidence_lines.append(
                        f"Evidence {index}:"
                    )

                    evidence_lines.append(
                        f"Source: {source}"
                    )

                    evidence_lines.append(
                        content
                    )

                    evidence_lines.append("")

        else:

            evidence_lines.append(
                "No company documents were retrieved."
            )

        sections.append(
            "\n".join(evidence_lines)
        )

        # -------------------------------------------------
        # FINAL INSTRUCTION
        # -------------------------------------------------

        sections.append(
            "\n".join([
                "DECISION CONTEXT INSTRUCTION",
                "----------------------------",
                (
                    "Use the information above as business "
                    "context. Distinguish between owner-provided "
                    "information and retrieved company evidence. "
                    "Do not invent missing facts."
                ),
            ])
        )

        return "\n\n".join(sections)


def build_decision_context(
    company_profile: dict,
    business_decision: str,
    owner_answers: list[dict] | None = None,
    rag_evidence: list[dict] | None = None,
) -> str:
    """
    Convenience function for building the final context.
    """

    context = DecisionContext(
        company_profile=company_profile,
        business_decision=business_decision,
        owner_answers=owner_answers or [],
        rag_evidence=rag_evidence or [],
    )

    return context.build()