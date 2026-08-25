"""
=========================================================
Business DecisionAI
Web Page Loader

Downloads public web pages and extracts readable text.

No paid API required.
=========================================================
"""

import re

import requests
from bs4 import BeautifulSoup


USER_AGENT = (
    "Mozilla/5.0 "
    "(Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 "
    "(KHTML, like Gecko) "
    "Chrome/151.0 Safari/537.36"
)


def load_web_page(
    url: str,
    timeout: int = 10,
    max_characters: int = 12000,
) -> str:
    """
    Download and extract readable text from a web page.
    """

    try:

        response = requests.get(
            url,
            headers={
                "User-Agent": USER_AGENT,
            },
            timeout=timeout,
        )

        response.raise_for_status()

    except Exception:

        return ""


    content_type = response.headers.get(
        "content-type",
        "",
    ).lower()


    if (
        "text/html" not in content_type
        and "application/xhtml" not in content_type
    ):

        return ""


    try:

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

    except Exception:

        return ""


    # -----------------------------------------------------
    # Remove irrelevant page elements
    # -----------------------------------------------------

    for tag in soup(
        [
            "script",
            "style",
            "noscript",
            "svg",
            "nav",
            "footer",
            "header",
            "form",
        ]
    ):

        tag.decompose()


    text = soup.get_text(
        separator=" ",
    )


    text = re.sub(
        r"\s+",
        " ",
        text,
    ).strip()


    if not text:
        return ""


    return text[:max_characters]