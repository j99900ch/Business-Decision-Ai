"""
=========================================================
Business DecisionAI
Web Research Engine

Purpose:
    Uses Gemini + Google Search grounding to research
    current public web information relevant to a
    business decision.

IMPORTANT:
    This module is isolated from the existing:
        - app.py
        - ai/
        - rag/
        - questionnaire/
        - decision_context/

It does NOT modify the existing decision engine.
=========================================================
"""

from google import genai
from dotenv import load_dotenv

import os
from typing import Any


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()

API_KEY = os.getenv("Business_Gemini_Key")

if not API_KEY:
    raise ValueError(
        "Business_Gemini_Key was not found in .env"
    )


# =========================================================
# GEMINI CLIENT
# =========================================================

client = genai.Client(
    api_key=API_KEY
)


# =========================================================
# MODEL
# =========================================================

MODEL_NAME = os.getenv(
    "WEB_RESEARCH_MODEL",
    "gemini-3.7-flash"
)


# =========================================================
# RESULT CONTAINER
# =========================================================

class WebResearchResult:
    """
    Stores the web research response and source citations.
    """

    def __init__(
        self,
        answer: str,
        sources: list[dict],
        search_queries: list[str],
    ):

        self.answer = answer

        self.sources = sources

        self.search_queries = search_queries

    def as_dict(self) -> dict:

        return {
            "answer": self.answer,
            "sources": self.sources,
            "search_queries": self.search_queries,
        }


# =========================================================
# SOURCE EXTRACTION
# =========================================================

def _extract_sources(
    interaction: Any,
) -> list[dict]:
    """
    Extract URL citations returned by Gemini.
    """

    sources = []

    try:

        for step in interaction.steps:

            if getattr(
                step,
                "type",
                None
            ) != "model_output":

                continue

            content_blocks = getattr(
                step,
                "content",
                []
            )

            for block in content_blocks:

                if getattr(
                    block,
                    "type",
                    None
                ) != "text":

                    continue

                annotations = getattr(
                    block,
                    "annotations",
                    []
                )

                for annotation in annotations:

                    if getattr(
                        annotation,
                        "type",
                        None
                    ) != "url_citation":

                        continue

                    url = getattr(
                        annotation,
                        "url",
                        None
                    )

                    title = getattr(
                        annotation,
                        "title",
                        None
                    )

                    if not url:
                        continue

                    source = {
                        "title": title or "Web source",
                        "url": url,
                    }

                    if source not in sources:

                        sources.append(
                            source
                        )

    except Exception:
        return sources

    return sources


# =========================================================
# SEARCH QUERY EXTRACTION
# =========================================================

def _extract_search_queries(
    interaction: Any,
) -> list[str]:
    """
    Extract the actual Google Search queries used by Gemini.
    """

    queries = []

    try:

        for step in interaction.steps:

            if getattr(
                step,
                "type",
                None
            ) != "google_search_call":

                continue

            arguments = getattr(
                step,
                "arguments",
                None
            )

            if not arguments:
                continue

            step_queries = getattr(
                arguments,
                "queries",
                []
            )

            if isinstance(
                step_queries,
                list
            ):

                for query in step_queries:

                    if query and query not in queries:

                        queries.append(
                            str(query)
                        )

    except Exception:
        return queries

    return queries


# =========================================================
# MAIN RESEARCH FUNCTION
# =========================================================

def research_business_market(
    company_name: str,
    industry: str,
    products: str,
    market: str,
    business_decision: str,
) -> WebResearchResult:
    """
    Research current public web information relevant
    to a business decision.

    Parameters
    ----------
    company_name:
        Company being analyzed.

    industry:
        Company's industry.

    products:
        Main products/services.

    market:
        Target market/country.

    business_decision:
        Decision being evaluated.

    Returns
    -------
    WebResearchResult
    """

    company_name = str(
        company_name or ""
    ).strip()

    industry = str(
        industry or ""
    ).strip()

    products = str(
        products or ""
    ).strip()

    market = str(
        market or ""
    ).strip()

    business_decision = str(
        business_decision or ""
    ).strip()


    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if not company_name:

        raise ValueError(
            "Company name is required."
        )

    if not business_decision:

        raise ValueError(
            "Business decision is required."
        )


    # -----------------------------------------------------
    # RESEARCH PROMPT
    # -----------------------------------------------------

    research_prompt = f"""
You are the Web Market Research layer of
Business DecisionAI.

Research current PUBLIC information from the web
that is relevant to the following business decision.

COMPANY
-------
{company_name}

INDUSTRY
--------
{industry or "Not provided"}

PRODUCTS / SERVICES
-------------------
{products or "Not provided"}

MARKET
------
{market or "Not provided"}

BUSINESS DECISION
-----------------
{business_decision}


RESEARCH OBJECTIVE
------------------

Find and analyze relevant current information that
could materially affect this business decision.

Prioritize:

1. Current market conditions
2. Industry trends
3. Recent demand trends
4. Relevant company information
5. Competitor activity when relevant
6. Supply-chain conditions
7. Pricing and cost pressures
8. Economic conditions
9. Regulatory developments
10. Recent credible business news
11. Customer or sector demand signals
12. Other information directly relevant to the decision


IMPORTANT RESEARCH RULES
------------------------

- Search the public web.
- Prefer recent information.
- Prefer authoritative and credible sources.
- Distinguish facts from interpretation.
- Do not invent company information.
- Do not assume that similarly named companies are
  the same company.
- If information about the exact company cannot be
  verified, explicitly say so.
- Do not treat search snippets as verified facts.
- Do not make an investment decision merely because
  a market trend is positive or negative.


OUTPUT FORMAT
-------------

MARKET RESEARCH SUMMARY:

- Give a concise synthesis of the most relevant
  findings.

CURRENT MARKET SIGNALS:

- List important current signals as separate points.

BUSINESS IMPACT:

- Explain how those signals could affect the
  specific business decision.

KEY RISKS:

- List the major risks separately.

KEY OPPORTUNITIES:

- List the major opportunities separately.

RESEARCH LIMITATIONS:

- Clearly mention important information that could
  not be verified.

Keep the response factual, concise and business-focused.
Use separate bullet points rather than long paragraphs.
"""


    # -----------------------------------------------------
    # GEMINI + GOOGLE SEARCH
    # -----------------------------------------------------

    interaction = client.interactions.create(

        model=MODEL_NAME,

        input=research_prompt,

        tools=[
            {
                "type": "google_search"
            }
        ],
    )


    # -----------------------------------------------------
    # RESPONSE
    # -----------------------------------------------------

    answer = getattr(
        interaction,
        "output_text",
        ""
    )

    if not answer:

        raise RuntimeError(
            "Gemini web research returned an empty response."
        )


    # -----------------------------------------------------
    # SOURCES
    # -----------------------------------------------------

    sources = _extract_sources(
        interaction
    )


    # -----------------------------------------------------
    # SEARCH QUERIES
    # -----------------------------------------------------

    search_queries = _extract_search_queries(
        interaction
    )


    return WebResearchResult(

        answer=answer.strip(),

        sources=sources,

        search_queries=search_queries,
    )


# =========================================================
# SIMPLE HELPER
# =========================================================

def get_web_research(
    company_name: str,
    industry: str,
    products: str,
    market: str,
    business_decision: str,
) -> dict:
    """
    Convenience function returning a normal dictionary.
    """

    result = research_business_market(

        company_name=company_name,

        industry=industry,

        products=products,

        market=market,

        business_decision=business_decision,
    )

    return result.as_dict()