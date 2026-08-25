"""
Business DecisionAI
Evidence Fusion Layer

Combines:
    1. Private company RAG evidence
    2. Public web evidence

This module does NOT call Gemini.

Purpose:
    Prepare a clean, traceable evidence context that can
    later be passed to the existing decision-analysis layer.
"""

from __future__ import annotations

from typing import Iterable


def _clean_text(value) -> str:

    if value is None:
        return ""

    return str(value).strip()


def _document_text(document) -> str:

    if hasattr(document, "page_content"):

        return _clean_text(
            document.page_content
        )

    return _clean_text(
        document
    )


def _document_metadata(document) -> dict:

    metadata = getattr(
        document,
        "metadata",
        {},
    )

    if not isinstance(metadata, dict):

        return {}

    return metadata


def build_private_evidence(
    documents: Iterable,
) -> list[dict]:

    evidence = []

    for index, document in enumerate(
        documents or [],
        start=1,
    ):

        text = _document_text(
            document
        )

        if not text:
            continue

        metadata = _document_metadata(
            document
        )

        evidence.append(
            {
                "evidence_id": (
                    f"PRIVATE-{index:03d}"
                ),
                "evidence_type": "private",
                "source": _clean_text(
                    metadata.get(
                        "source",
                        "company_knowledge",
                    )
                ),
                "file_type": _clean_text(
                    metadata.get(
                        "file_type",
                        "",
                    )
                ),
                "company_id": _clean_text(
                    metadata.get(
                        "company_id",
                        "",
                    )
                ),
                "content": text,
            }
        )

    return evidence


def build_public_evidence(
    results: Iterable,
) -> list[dict]:

    evidence = []

    for index, result in enumerate(
        results or [],
        start=1,
    ):

        title = _clean_text(
            getattr(
                result,
                "title",
                "",
            )
        )

        url = _clean_text(
            getattr(
                result,
                "url",
                "",
            )
        )

        snippet = _clean_text(
            getattr(
                result,
                "snippet",
                "",
            )
        )

        content = _clean_text(
            getattr(
                result,
                "text",
                "",
            )
        )

        # Some web-content objects may use
        # "content" instead of "text".
        if not content:

            content = _clean_text(
                getattr(
                    result,
                    "content",
                    "",
                )
            )

        if not title and not url and not content:
            continue

        evidence.append(
            {
                "evidence_id": (
                    f"WEB-{index:03d}"
                ),
                "evidence_type": "public_web",
                "title": title,
                "source": (
                    _clean_text(
                        getattr(
                            result,
                            "source",
                            "public_web",
                        )
                    )
                    or "public_web"
                ),
                "url": url,
                "content": (
                    content
                    or snippet
                ),
            }
        )

    return evidence


def build_evidence_context(
    private_evidence: Iterable = None,
    public_evidence: Iterable = None,
) -> str:

    private_items = list(
        private_evidence or []
    )

    public_items = list(
        public_evidence or []
    )

    sections = []

    # =====================================================
    # PRIVATE COMPANY EVIDENCE
    # =====================================================

    if private_items:

        lines = [
            "PRIVATE COMPANY EVIDENCE",
            "",
            (
                "Use this information as "
                "internal company knowledge."
            ),
            "",
        ]

        for item in private_items:

            lines.extend(
                [
                    (
                        f"Evidence ID: "
                        f"{item.get('evidence_id', '')}"
                    ),
                    (
                        f"Source: "
                        f"{item.get('source', '')}"
                    ),
                    (
                        f"File Type: "
                        f"{item.get('file_type', '')}"
                    ),
                    (
                        "Content:"
                    ),
                    item.get(
                        "content",
                        "",
                    ),
                    "",
                ]
            )

        sections.append(
            "\n".join(lines)
        )

    # =====================================================
    # PUBLIC WEB EVIDENCE
    # =====================================================

    if public_items:

        lines = [
            "PUBLIC WEB EVIDENCE",
            "",
            (
                "Use public web information "
                "only when relevant to the "
                "business decision."
            ),
            "",
        ]

        for item in public_items:

            lines.extend(
                [
                    (
                        f"Evidence ID: "
                        f"{item.get('evidence_id', '')}"
                    ),
                    (
                        f"Title: "
                        f"{item.get('title', '')}"
                    ),
                    (
                        f"URL: "
                        f"{item.get('url', '')}"
                    ),
                    (
                        f"Source: "
                        f"{item.get('source', '')}"
                    ),
                    "Content:",
                    item.get(
                        "content",
                        "",
                    ),
                    "",
                ]
            )

        sections.append(
            "\n".join(lines)
        )

    # =====================================================
    # EVIDENCE RULES
    # =====================================================

    sections.append(
        "\n".join(
            [
                "EVIDENCE RULES",
                "",
                (
                    "1. Distinguish private company "
                    "evidence from public web evidence."
                ),
                (
                    "2. Do not treat missing evidence "
                    "as a known fact."
                ),
                (
                    "3. Preserve evidence IDs so the "
                    "final analysis can remain traceable."
                ),
                (
                    "4. Use evidence only when it is "
                    "relevant to the business decision."
                ),
            ]
        )
    )

    return "\n\n".join(
        section
        for section in sections
        if section.strip()
    )


def fuse_evidence(
    private_documents: Iterable = None,
    public_results: Iterable = None,
) -> dict:

    private_evidence = (
        build_private_evidence(
            private_documents
        )
    )

    public_evidence = (
        build_public_evidence(
            public_results
        )
    )

    context = build_evidence_context(
        private_evidence=private_evidence,
        public_evidence=public_evidence,
    )

    return {
        "private_evidence": private_evidence,
        "public_evidence": public_evidence,
        "total_evidence": (
            len(private_evidence)
            + len(public_evidence)
        ),
        "context": context,
    }