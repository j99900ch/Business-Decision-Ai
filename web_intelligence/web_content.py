"""
Business DecisionAI
Public Web Page Content Extraction

Purpose:
    Fetch public web pages and extract readable text.

This module:
    - does NOT call Gemini
    - does NOT modify Private RAG
    - does NOT modify app.py
    - preserves the original source URL
"""

from __future__ import annotations

import re
import urllib.request
from dataclasses import dataclass
from html.parser import HTMLParser


# =========================================================
# RESULT MODEL
# =========================================================

@dataclass
class WebPageContent:
    url: str
    title: str
    text: str
    success: bool
    error: str = ""


# =========================================================
# HTML TEXT EXTRACTOR
# =========================================================

class PageTextParser(HTMLParser):

    def __init__(self):
        super().__init__()

        self.parts = []
        self.title_parts = []

        self.in_title = False
        self.skip_content = False

    def handle_starttag(
        self,
        tag,
        attrs,
    ):

        tag = tag.lower()

        if tag == "title":
            self.in_title = True

        if tag in {
            "script",
            "style",
            "noscript",
            "svg",
        }:

            self.skip_content = True

    def handle_endtag(
        self,
        tag,
    ):

        tag = tag.lower()

        if tag == "title":
            self.in_title = False

        if tag in {
            "script",
            "style",
            "noscript",
            "svg",
        }:

            self.skip_content = False

    def handle_data(
        self,
        data,
    ):

        if self.skip_content:
            return

        text = data.strip()

        if not text:
            return

        if self.in_title:

            self.title_parts.append(
                text
            )

        self.parts.append(
            text
        )

    def get_title(self):

        return clean_text(
            " ".join(
                self.title_parts
            )
        )

    def get_text(self):

        return clean_text(
            " ".join(
                self.parts
            )
        )


# =========================================================
# TEXT CLEANING
# =========================================================

def clean_text(
    text: str,
) -> str:

    text = text or ""

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


# =========================================================
# PAGE FETCH
# =========================================================

def fetch_web_page(
    url: str,
    timeout: int = 15,
) -> WebPageContent:

    if not url:

        return WebPageContent(
            url="",
            title="",
            text="",
            success=False,
            error="URL is empty.",
        )

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "Chrome/151.0 Safari/537.36"
            ),
            "Accept": (
                "text/html,"
                "application/xhtml+xml"
            ),
        },
    )

    try:

        with urllib.request.urlopen(
            request,
            timeout=timeout,
        ) as response:

            content_type = response.headers.get(
                "Content-Type",
                "",
            ).lower()

            raw = response.read()

            encoding = "utf-8"

            if "charset=" in content_type:

                encoding = (
                    content_type
                    .split("charset=")[-1]
                    .split(";")[0]
                    .strip()
                )

            html_content = raw.decode(
                encoding,
                errors="ignore",
            )

        parser = PageTextParser()

        parser.feed(
            html_content
        )

        title = parser.get_title()
        text = parser.get_text()

        if not text:

            return WebPageContent(
                url=url,
                title=title,
                text="",
                success=False,
                error="No readable text extracted.",
            )

        return WebPageContent(
            url=url,
            title=title,
            text=text,
            success=True,
        )

    except Exception as error:

        return WebPageContent(
            url=url,
            title="",
            text="",
            success=False,
            error=str(error),
        )


# =========================================================
# BATCH EXTRACTION
# =========================================================

def extract_web_pages(
    urls: list[str],
    max_chars: int = 12000,
) -> list[WebPageContent]:

    pages = []

    seen_urls = set()

    for url in urls:

        url = url.strip()

        if not url:
            continue

        if url in seen_urls:
            continue

        seen_urls.add(
            url
        )

        page = fetch_web_page(
            url
        )

        if page.success:

            page.text = page.text[
                :max_chars
            ]

        pages.append(
            page
        )

    return pages