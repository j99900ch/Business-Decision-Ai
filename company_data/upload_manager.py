"""
=========================================================
Business DecisionAI
Private Company Knowledge Manager

Purpose:
    Manage documents uploaded by a business owner.

Architecture:

    Company
       ↓
    Uploaded Document
       ↓
    Existing RAGEngine
       ↓
    Company-specific Vector Store
       ↓
    Private Company Knowledge

IMPORTANT:
    This module does NOT modify the existing RAG system.

It simply provides a safe management layer around the
already-tested RAGEngine.
=========================================================
"""

from pathlib import Path
import shutil
from datetime import datetime

from rag.rag_engine import RAGEngine


# =========================================================
# DIRECTORIES
# =========================================================

COMPANY_DATA_ROOT = Path("data") / "companies"


# =========================================================
# MANAGER
# =========================================================

class CompanyKnowledgeManager:
    """
    Manage private documents for one company.
    """

    def __init__(
        self,
        company_id: str,
    ):

        company_id = str(
            company_id
        ).strip()

        if not company_id:

            raise ValueError(
                "company_id is required."
            )

        self.company_id = company_id

        self.company_directory = (
            COMPANY_DATA_ROOT
            / company_id
        )

        self.documents_directory = (
            self.company_directory
            / "documents"
        )

        self.documents_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.rag_engine = RAGEngine()


    # =====================================================
    # SAVE DOCUMENT
    # =====================================================

    def save_document(
        self,
        file_path: str,
    ) -> dict:
        """
        Copy a company document into the company's
        private document directory.

        The original uploaded file is not modified.
        """

        source = Path(
            file_path
        )

        if not source.exists():

            raise FileNotFoundError(
                f"File not found: {source}"
            )

        if not source.is_file():

            raise ValueError(
                "The supplied path is not a file."
            )


        # -------------------------------------------------
        # Prevent unsupported hidden/system files
        # -------------------------------------------------

        if source.name.startswith("."):

            raise ValueError(
                "Hidden files are not accepted."
            )


        destination = (
            self.documents_directory
            / source.name
        )


        # -------------------------------------------------
        # If same filename exists, create a safe version
        # -------------------------------------------------

        if destination.exists():

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            destination = (
                self.documents_directory
                / (
                    f"{source.stem}_"
                    f"{timestamp}"
                    f"{source.suffix}"
                )
            )


        shutil.copy2(
            source,
            destination,
        )


        return {
            "company_id": self.company_id,
            "filename": destination.name,
            "path": str(destination),
            "size_bytes": destination.stat().st_size,
        }


    # =====================================================
    # INDEX DOCUMENT
    # =====================================================

    def index_document(
        self,
        file_path: str,
    ) -> dict:
        """
        Send a company document into the existing RAG
        ingestion pipeline.

        Existing RAGEngine remains untouched.
        """

        path = Path(
            file_path
        )

        if not path.exists():

            raise FileNotFoundError(
                f"Document not found: {path}"
            )


        result = (
            self.rag_engine.ingest_document(
                company_id=self.company_id,
                file_path=str(path),
            )
        )


        return result


    # =====================================================
    # SAVE + INDEX
    # =====================================================

    def add_document(
        self,
        file_path: str,
    ) -> dict:
        """
        Complete company knowledge workflow:

            Upload
              ↓
            Private storage
              ↓
            Existing RAG ingestion
        """

        saved = self.save_document(
            file_path
        )


        indexed = self.index_document(
            saved["path"]
        )


        return {
            "company_id": self.company_id,

            "filename": saved[
                "filename"
            ],

            "path": saved[
                "path"
            ],

            "size_bytes": saved[
                "size_bytes"
            ],

            "documents_loaded": indexed.get(
                "documents_loaded",
                0,
            ),

            "chunks_created": indexed.get(
                "chunks_created",
                0,
            ),
        }


    # =====================================================
    # LIST DOCUMENTS
    # =====================================================

    def list_documents(self) -> list[dict]:
        """
        Return all private company documents.
        """

        if not self.documents_directory.exists():

            return []


        documents = []


        for path in sorted(
            self.documents_directory.iterdir()
        ):

            if not path.is_file():

                continue


            documents.append(
                {
                    "filename": path.name,

                    "path": str(path),

                    "size_bytes": path.stat().st_size,

                    "modified": datetime.fromtimestamp(
                        path.stat().st_mtime
                    ).isoformat(
                        timespec="seconds"
                    ),
                }
            )


        return documents


    # =====================================================
    # RETRIEVE PRIVATE KNOWLEDGE
    # =====================================================

    def retrieve(
        self,
        query: str,
        k: int = 4,
    ):
        """
        Retrieve company-specific information from the
        existing RAG vector store.
        """

        query = str(
            query
        ).strip()

        if not query:

            raise ValueError(
                "Query cannot be empty."
            )


        return self.rag_engine.retrieve(
            company_id=self.company_id,
            query=query,
            k=k,
        )