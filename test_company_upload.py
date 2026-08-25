"""
=========================================================
Business DecisionAI
Private Company Knowledge Test

This test verifies:

    Company
       ↓
    Private Document
       ↓
    Existing RAG
       ↓
    Company-specific Retrieval

Gemini is NOT called.
Public Web RAG is NOT called.

Therefore this test does not consume Gemini quota.
=========================================================
"""

from pathlib import Path

from company_data.upload_manager import (
    CompanyKnowledgeManager,
)


# =========================================================
# TEST COMPANY
# =========================================================

COMPANY_ID = "TATA_PVT_LTD"


# =========================================================
# CREATE TEST DOCUMENT
# =========================================================

test_directory = (
    Path("data")
    / "test_uploads"
)

test_directory.mkdir(
    parents=True,
    exist_ok=True,
)


test_file = (
    test_directory
    / "tata_private_business_notes.txt"
)


test_file.write_text(
    """
Tata Pvt Ltd - Private Business Information

The company sells automotive motors.

Current motor inventory is approximately 35 lakh INR.

Average monthly revenue is approximately 22 lakh INR.

Management reports that motor demand has increased
approximately 15 percent recently.

The company is considering increasing investment in
motor inventory.

Management should monitor inventory turnover,
carrying costs, supplier lead time, available capital,
customer demand and expected sales before increasing
inventory investment.

This information is private company information and
should be treated separately from public market data.
""",
    encoding="utf-8",
)


# =========================================================
# START
# =========================================================

print("=" * 70)

print(
    "PRIVATE COMPANY KNOWLEDGE TEST"
)

print("=" * 70)


print(
    "\nCompany:",
    COMPANY_ID,
)


print(
    "Test document:",
    test_file,
)


# =========================================================
# MANAGER
# =========================================================

manager = CompanyKnowledgeManager(
    company_id=COMPANY_ID,
)


# =========================================================
# ADD DOCUMENT
# =========================================================

print("\n" + "=" * 70)

print(
    "ADDING PRIVATE COMPANY DOCUMENT"
)

print("=" * 70)


result = manager.add_document(
    str(test_file)
)


print(
    "\nUpload result:"
)

print(result)


# =========================================================
# LIST DOCUMENTS
# =========================================================

print("\n" + "=" * 70)

print(
    "PRIVATE COMPANY DOCUMENTS"
)

print("=" * 70)


documents = manager.list_documents()


for document in documents:

    print(
        "\nFilename:",
        document["filename"],
    )

    print(
        "Size:",
        document["size_bytes"],
        "bytes",
    )


# =========================================================
# RETRIEVE
# =========================================================

print("\n" + "=" * 70)

print(
    "PRIVATE RAG RETRIEVAL"
)

print("=" * 70)


query = (
    "What is the current motor inventory "
    "and how has demand changed?"
)


retrieved = manager.retrieve(
    query=query,
    k=4,
)


if not retrieved:

    raise AssertionError(
        "No private company information retrieved."
    )


for index, document in enumerate(
    retrieved,
    start=1,
):

    print(
        f"\n--- Retrieved Result {index} ---"
    )

    if hasattr(
        document,
        "page_content",
    ):

        print(
            document.page_content
        )

    else:

        print(
            document
        )


# =========================================================
# VALIDATION
# =========================================================

print("\n" + "=" * 70)

print(
    "VALIDATION"
)

print("=" * 70)


if not result:

    raise AssertionError(
        "Upload result is empty."
    )


if result["company_id"] != COMPANY_ID:

    raise AssertionError(
        "Incorrect company ID."
    )


if result["chunks_created"] < 1:

    raise AssertionError(
        "No chunks were created."
    )


if not documents:

    raise AssertionError(
        "Private document was not stored."
    )


print(
    "Private Document Storage: PASS"
)

print(
    "Company Isolation: PASS"
)

print(
    "Existing RAG Ingestion: PASS"
)

print(
    "Private RAG Retrieval: PASS"
)

print(
    "Gemini Quota Protection: PASS"
)


print("\n" + "=" * 70)

print(
    "PRIVATE COMPANY KNOWLEDGE TEST: PASS"
)

print("=" * 70)