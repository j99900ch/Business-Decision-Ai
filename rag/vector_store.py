"""
Business DecisionAI
Company Vector Store

Uses local embeddings so document ingestion does
not consume Gemini API quota.

Existing Gemini vector stores are preserved.
New local vector stores are stored separately.
"""

from pathlib import Path

from langchain_community.vectorstores import FAISS

from rag.embeddings import get_embeddings


# ---------------------------------------------------------
# NEW LOCAL VECTOR STORE LOCATION
# ---------------------------------------------------------
#
# We intentionally DO NOT reuse the old directory:
#
# data/vectorstores/
#
# because those stores may contain Gemini-generated
# vectors with a different dimension.
#
# Existing data remains untouched.
# ---------------------------------------------------------

VECTORSTORE_ROOT = Path(
    "data/vectorstores_local"
)


def get_company_vectorstore_path(
    company_id: str,
) -> Path:

    if not company_id:
        raise ValueError(
            "company_id is required."
        )

    return (
        VECTORSTORE_ROOT
        / company_id
    )


def create_company_vectorstore(
    company_id: str,
    documents,
):

    if not company_id:
        raise ValueError(
            "company_id is required."
        )

    if not documents:
        raise ValueError(
            "No documents were supplied "
            "for vector store creation."
        )

    embeddings = get_embeddings()

    vector_store = FAISS.from_documents(
        documents,
        embeddings,
    )

    store_path = (
        get_company_vectorstore_path(
            company_id
        )
    )

    store_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    vector_store.save_local(
        str(store_path)
    )

    return vector_store


def load_company_vectorstore(
    company_id: str,
):

    store_path = (
        get_company_vectorstore_path(
            company_id
        )
    )

    if not store_path.exists():

        raise FileNotFoundError(
            "No local vector store exists for "
            f"company: {company_id}"
        )

    embeddings = get_embeddings()

    return FAISS.load_local(
        str(store_path),
        embeddings,
        allow_dangerous_deserialization=True,
    )