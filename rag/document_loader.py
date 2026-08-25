"""
Business DecisionAI
Universal Company Document Loader

Supported:
- PDF
- TXT
- CSV

Returns LangChain Documents so the existing
RAG pipeline remains unchanged.
"""

from pathlib import Path
import csv

from langchain_core.documents import Document
from pypdf import PdfReader


def load_document(file_path: str) -> list[Document]:

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    extension = path.suffix.lower()

    # =====================================================
    # PDF
    # =====================================================

    if extension == ".pdf":

        reader = PdfReader(
            str(path)
        )

        documents = []

        for page_number, page in enumerate(
            reader.pages,
            start=1,
        ):

            text = (
                page.extract_text()
                or ""
            ).strip()

            if not text:
                continue

            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": path.name,
                        "file_type": "pdf",
                        "page": page_number,
                    },
                )
            )

        return documents

    # =====================================================
    # TXT
    # =====================================================

    if extension == ".txt":

        text = path.read_text(
            encoding="utf-8",
            errors="ignore",
        ).strip()

        if not text:
            return []

        return [
            Document(
                page_content=text,
                metadata={
                    "source": path.name,
                    "file_type": "txt",
                },
            )
        ]

    # =====================================================
    # CSV
    # =====================================================

    if extension == ".csv":

        rows = []

        with open(
            path,
            "r",
            encoding="utf-8-sig",
            errors="ignore",
            newline="",
        ) as file:

            reader = csv.DictReader(
                file
            )

            for row in reader:

                cleaned_row = []

                for key, value in row.items():

                    key = (
                        str(key)
                        .strip()
                        if key is not None
                        else ""
                    )

                    value = (
                        str(value)
                        .strip()
                        if value is not None
                        else ""
                    )

                    if key and value:

                        cleaned_row.append(
                            f"{key}: {value}"
                        )

                if cleaned_row:

                    rows.append(
                        " | ".join(
                            cleaned_row
                        )
                    )

        if not rows:
            return []

        # Keep CSV data as a single logical
        # company document. Your existing
        # chunker will handle splitting.

        csv_text = (
            f"Company Data File: {path.name}\n\n"
            + "\n".join(rows)
        )

        return [
            Document(
                page_content=csv_text,
                metadata={
                    "source": path.name,
                    "file_type": "csv",
                },
            )
        ]

    # =====================================================
    # UNSUPPORTED FILE
    # =====================================================

    raise ValueError(
        "Unsupported file type: "
        f"{extension}. "
        "Supported files are PDF, TXT and CSV."
    )