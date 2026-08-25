"""
=========================================================
Business DecisionAI
AI Business Question Generator

This module is isolated from the existing Streamlit app.

Purpose:
Generate decision-specific questions that collect
missing business information from the business owner.
=========================================================
"""

import ast
import json
import re

from ai.gemini import generate_response


QUESTION_GENERATION_PROMPT = """
You are the Business Assessment Agent for Business DecisionAI.

Your job is to identify the most important information
a business owner needs to provide before an AI can evaluate
a business decision.

You will receive:

1. Business profile
2. Business decision

Generate between 5 and 7 questions.

Rules:

1. Questions must be directly relevant to the decision.
2. Do not ask for information already available in the profile.
3. Prefer measurable business information.
4. Ask about financial impact when relevant.
5. Ask about demand and sales when relevant.
6. Ask about operational constraints when relevant.
7. Ask about risk or available capital when relevant.
8. Do not ask unnecessary personal questions.
9. Questions must be understandable to a normal business owner.
10. Do not provide the business recommendation yet.

Return ONLY one object containing a "questions" list.

Each question must contain:

id
question
reason
answer_type

Allowed answer_type values:

number
text
percentage
currency
choice
"""


def _clean_model_output(text: str) -> str:
    """
    Clean common formatting added by an LLM.
    """

    if not text:
        raise ValueError(
            "Question generator returned an empty response."
        )

    cleaned = text.strip()

    # Remove markdown code fences.
    cleaned = re.sub(
        r"```(?:json|python)?",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )

    cleaned = cleaned.replace(
        "```",
        ""
    ).strip()

    return cleaned


def _extract_json(text: str) -> dict:
    """
    Parse Gemini output safely.

    First tries strict JSON.
    Then tries Python literal syntax as a fallback.
    """

    cleaned = _clean_model_output(text)

    # --------------------------------------------------
    # Find the object portion.
    # --------------------------------------------------

    start = cleaned.find("{")
    end = cleaned.rfind("}")

    if start == -1 or end == -1 or end <= start:

        raise ValueError(
            "Could not find an object in Gemini response."
        )

    object_text = cleaned[
        start:end + 1
    ].strip()

    # --------------------------------------------------
    # Attempt 1: strict JSON
    # --------------------------------------------------

    try:

        result = json.loads(
            object_text
        )

        if isinstance(result, dict):
            return result

    except json.JSONDecodeError:
        pass

    # --------------------------------------------------
    # Attempt 2: Python dictionary syntax
    #
    # Example:
    # {'questions': [...]}
    # --------------------------------------------------

    try:

        result = ast.literal_eval(
            object_text
        )

        if isinstance(result, dict):
            return result

    except (ValueError, SyntaxError):
        pass

    # --------------------------------------------------
    # Neither format worked.
    # --------------------------------------------------

    raise ValueError(
        "Gemini returned an unsupported question format."
    )


def generate_business_questions(
    company_profile: dict,
    business_decision: str,
) -> list[dict]:
    """
    Generate decision-specific business questions.

    Parameters
    ----------
    company_profile:
        Dictionary containing known business information.

    business_decision:
        The decision the owner wants to evaluate.

    Returns
    -------
    list[dict]
        Structured business questions.
    """

    if not isinstance(
        company_profile,
        dict
    ):

        raise ValueError(
            "company_profile must be a dictionary."
        )

    if not business_decision.strip():

        raise ValueError(
            "Business decision cannot be empty."
        )

    profile_text = json.dumps(
        company_profile,
        indent=2,
        ensure_ascii=False,
    )

    prompt = f"""
{QUESTION_GENERATION_PROMPT}

--------------------------------------------------
BUSINESS PROFILE
--------------------------------------------------

{profile_text}

--------------------------------------------------
BUSINESS DECISION
--------------------------------------------------

{business_decision}

--------------------------------------------------

Generate the questions now.

Return ONLY the object.
"""

    response = generate_response(
        prompt
    )

    result = _extract_json(
        response
    )

    questions = result.get(
        "questions"
    )

    if not isinstance(
        questions,
        list
    ):

        raise ValueError(
            "Gemini response does not contain "
            "a valid 'questions' list."
        )

    cleaned_questions = []

    allowed_types = {
        "number",
        "text",
        "percentage",
        "currency",
        "choice",
    }

    for index, question in enumerate(
        questions[:7],
        start=1,
    ):

        if not isinstance(
            question,
            dict
        ):
            continue

        question_text = str(
            question.get(
                "question",
                ""
            )
        ).strip()

        reason = str(
            question.get(
                "reason",
                ""
            )
        ).strip()

        answer_type = str(
            question.get(
                "answer_type",
                "text"
            )
        ).strip().lower()

        if not question_text:
            continue

        if not reason:

            reason = (
                "This information helps "
                "evaluate the business decision."
            )

        if answer_type not in allowed_types:

            answer_type = "text"

        cleaned_questions.append(
            {
                "id": f"q{index}",
                "question": question_text,
                "reason": reason,
                "answer_type": answer_type,
            }
        )

    if not cleaned_questions:

        raise ValueError(
            "No usable business questions "
            "were generated."
        )

    return cleaned_questions