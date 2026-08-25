"""
Business DecisionAI
Local Embedding Engine

Company documents are embedded locally so that
document ingestion does not consume Gemini API quota.

Gemini remains available for final AI reasoning.
"""

import hashlib
import math
import re

from langchain_core.embeddings import Embeddings


# =========================================================
# CONFIGURATION
# =========================================================

EMBEDDING_DIMENSION = 384


# =========================================================
# TOKENIZATION
# =========================================================

def _tokenize(text: str) -> list[str]:
    """
    Convert text into normalized searchable tokens.
    """

    text = str(text).lower()

    return re.findall(
        r"[a-zA-Z0-9₹]+",
        text,
    )


# =========================================================
# DETERMINISTIC TOKEN HASH
# =========================================================

def _hash_token(
    token: str,
) -> tuple[int, float]:
    """
    Convert a token into:

    - deterministic vector position
    - deterministic sign

    No API call is made.
    """

    digest = hashlib.sha256(
        token.encode("utf-8")
    ).digest()

    position = (
        int.from_bytes(
            digest[:4],
            "big",
        )
        % EMBEDDING_DIMENSION
    )

    sign = (
        1.0
        if digest[4] % 2 == 0
        else -1.0
    )

    return position, sign


# =========================================================
# TEXT → VECTOR
# =========================================================

def _embed_text(
    text: str,
) -> list[float]:
    """
    Convert text into a deterministic
    normalized local vector.
    """

    vector = [
        0.0
        for _ in range(
            EMBEDDING_DIMENSION
        )
    ]

    tokens = _tokenize(text)

    if not tokens:

        return vector

    for token in tokens:

        position, sign = _hash_token(
            token
        )

        vector[position] += sign

    # -----------------------------------------------------
    # L2 NORMALIZATION
    # -----------------------------------------------------

    magnitude = math.sqrt(
        sum(
            value * value
            for value in vector
        )
    )

    if magnitude > 0:

        vector = [
            value / magnitude
            for value in vector
        ]

    return vector


# =========================================================
# LANGCHAIN EMBEDDINGS IMPLEMENTATION
# =========================================================

class LocalBusinessEmbeddings(
    Embeddings
):
    """
    LangChain-compatible local embeddings.

    This class intentionally inherits from
    langchain_core.embeddings.Embeddings.

    Therefore FAISS can correctly use:

        embed_documents()
        embed_query()

    without calling the object itself.

    No Gemini API is used.
    """

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        return [
            _embed_text(text)
            for text in texts
        ]

    def embed_query(
        self,
        text: str,
    ) -> list[float]:

        return _embed_text(text)


# =========================================================
# PUBLIC FACTORY
# =========================================================

def get_embeddings():
    """
    Return the local embedding engine.

    The function name is intentionally preserved
    so existing RAG code does not need to change.
    """

    return LocalBusinessEmbeddings()