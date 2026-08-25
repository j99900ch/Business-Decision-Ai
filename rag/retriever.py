from rag.vector_store import (
    load_company_vectorstore,
)


def retrieve_company_information(
    company_id: str,
    query: str,
    k: int = 4,
):

    if not query.strip():

        raise ValueError(
            "Query cannot be empty."
        )

    vector_store = (
        load_company_vectorstore(
            company_id
        )
    )

    documents = vector_store.similarity_search(
        query,
        k=k,
    )

    return documents