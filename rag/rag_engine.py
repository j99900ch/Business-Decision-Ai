from rag.document_loader import (
    load_document,
)

from rag.chunker import (
    split_documents,
)

from rag.vector_store import (
    create_company_vectorstore,
)

from rag.retriever import (
    retrieve_company_information,
)


class RAGEngine:

    def ingest_document(
        self,
        company_id: str,
        file_path: str,
    ):

        if not company_id:
            raise ValueError(
                "company_id is required."
            )

        documents = load_document(
            file_path
        )

        for document in documents:

            document.metadata[
                "company_id"
            ] = company_id

        chunks = split_documents(
            documents
        )

        for chunk in chunks:

            chunk.metadata[
                "company_id"
            ] = company_id

        create_company_vectorstore(
            company_id,
            chunks,
        )

        return {
            "company_id": company_id,
            "documents_loaded": len(
                documents
            ),
            "chunks_created": len(
                chunks
            ),
        }

    def retrieve(
        self,
        company_id: str,
        query: str,
        k: int = 4,
    ):

        return retrieve_company_information(
            company_id=company_id,
            query=query,
            k=k,
        )