"""
=========================================================
Business DecisionAI
Business Interview Engine

Manages AI-generated business questions and
the business owner's answers.

This module is independent from the existing
Streamlit application and decision engine.
=========================================================
"""

from dataclasses import dataclass, field

from questionnaire.question_generator import (
    generate_business_questions,
)


@dataclass
class BusinessAnswer:
    question_id: str
    question: str
    answer: str
    answer_type: str
    reason: str


@dataclass
class BusinessInterview:
    company_profile: dict
    business_decision: str

    questions: list[dict] = field(
        default_factory=list
    )

    answers: list[BusinessAnswer] = field(
        default_factory=list
    )

    def generate_questions(self) -> list[dict]:
        """
        Generate questions based on the known
        company information and business decision.
        """

        self.questions = generate_business_questions(
            company_profile=self.company_profile,
            business_decision=self.business_decision,
        )

        return self.questions

    def add_answer(
        self,
        question_id: str,
        answer: str,
    ) -> None:
        """
        Store an owner's answer for a question.
        """

        answer = str(answer).strip()

        if not answer:
            raise ValueError(
                "Answer cannot be empty."
            )

        selected_question = None

        for question in self.questions:

            if question.get("id") == question_id:

                selected_question = question
                break

        if selected_question is None:

            raise ValueError(
                f"Unknown question ID: {question_id}"
            )

        # Prevent duplicate answers for the
        # same question.
        self.answers = [
            existing_answer
            for existing_answer in self.answers
            if existing_answer.question_id
            != question_id
        ]

        self.answers.append(
            BusinessAnswer(
                question_id=selected_question["id"],
                question=selected_question["question"],
                answer=answer,
                answer_type=selected_question[
                    "answer_type"
                ],
                reason=selected_question["reason"],
            )
        )

    def get_answers_as_dict(self) -> list[dict]:
        """
        Convert collected answers into a
        structure that can later be passed
        to the decision engine.
        """

        return [
            {
                "question_id": answer.question_id,
                "question": answer.question,
                "answer": answer.answer,
                "answer_type": answer.answer_type,
                "reason": answer.reason,
            }
            for answer in self.answers
        ]

    def get_answered_count(self) -> int:
        return len(self.answers)

    def get_question_count(self) -> int:
        return len(self.questions)

    def is_complete(self) -> bool:
        """
        Return True only when all generated
        questions have been answered.
        """

        return (
            len(self.questions) > 0
            and len(self.answers)
            == len(self.questions)
        )