"""
=========================================================
Business DecisionAI
Free Web RAG

Pipeline:

Business Decision
        ↓
Search Query Generation
        ↓
Public Web Search
        ↓
Web Page Retrieval
        ↓
LangChain Documents
        ↓
Recursive Text Splitting
        ↓
Relevant Web Evidence
        ↓
Ready for Gemini

No paid search API required.
=========================================================
"""

from dataclasses import dataclass

from langchain_core.documents import Document
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)

from web_research.free_search import (
    search_web,
)

from web_research.web_loader import (
    load_web_page,
)


# =========================================================
# RESULT
# =========================================================

@dataclass
class WebEvidence:

    title: str

    url: str

    snippet: str

    content: str


# =========================================================
# QUERY BUILDER
# =========================================================

def build_research_queries(
    company_name: str,
    industry: str,
    products: str,
    market: str,
    decision: str,
) -> list[str]:
    """
    Build several focused searches rather than one huge query.
    """

    company_name = str(
        company_name or ""
    ).strip()

    industry = str(
        industry or ""
    ).strip()

    products = str(
        products or ""
    ).strip()

    market = str(
        market or ""
    ).strip()

    decision = str(
        decision or ""
    ).strip()


    queries = []


    if company_name:

        queries.append(
            f'"{company_name}" '
            f'"{market}" '
            f'latest business news'
        )


    if industry:

        queries.append(
            f'"{industry}" '
            f'"{market}" '
            f'latest market trends'
        )


    if products:

        queries.append(
            f'"{products}" '
            f'"{market}" '
            f'latest demand market'
        )


    queries.append(
        f'"{market}" '
        f'{decision} '
        f'market conditions'
    )


    # Remove duplicates while preserving order.

    unique_queries = []

    for query in queries:

        query = query.strip()

        if query and query not in unique_queries:

            unique_queries.append(query)


    return unique_queries[:4]


# =========================================================
# SEARCH
# =========================================================

def collect_search_results(
    queries: list[str],
    results_per_query: int = 4,
) -> list[dict]:
    """
    Run multiple searches and remove duplicate URLs.
    """

    collected = []

    seen_urls = set()


    for query in queries:

        results = search_web(
            query=query,
            max_results=results_per_query,
        )


        for result in results:

            url = result.get(
                "url",
                "",
            ).strip()


            if not url:
                continue


            if url in seen_urls:
                continue


            seen_urls.add(url)

            result["query"] = query

            collected.append(
                result
            )


    return collected


# =========================================================
# LOAD WEB DOCUMENTS
# =========================================================

def load_web_documents(
    search_results: list[dict],
    max_pages: int = 8,
) -> list[Document]:
    """
    Download public pages and convert them into
    LangChain Documents.
    """

    documents = []


    for result in search_results[:max_pages]:

        url = result.get(
            "url",
            "",
        )

        title = result.get(
            "title",
            "Web Source",
        )

        snippet = result.get(
            "snippet",
            "",
        )


        content = load_web_page(
            url
        )


        if not content:

            # Search snippet is still useful evidence.

            content = snippet


        if not content:

            continue


        document = Document(

            page_content=content,

            metadata={
                "title": title,
                "url": url,
                "search_query": result.get(
                    "query",
                    "",
                ),
            },
        )


        documents.append(
            document
        )


    return documents


# =========================================================
# SPLIT DOCUMENTS
# =========================================================

def split_web_documents(
    documents: list[Document],
) -> list[Document]:
    """
    Split web documents using LangChain.
    """

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=1200,

        chunk_overlap=180,

        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )


    return splitter.split_documents(
        documents
    )


# =========================================================
# BUILD WEB EVIDENCE
# =========================================================

def retrieve_web_evidence(
    company_name: str,
    industry: str,
    products: str,
    market: str,
    decision: str,
    max_pages: int = 8,
) -> dict:
    """
    Complete free web-RAG retrieval pipeline.

    Returns:
        queries
        search_results
        documents
        chunks
        evidence
    """

    queries = build_research_queries(

        company_name=company_name,

        industry=industry,

        products=products,

        market=market,

        decision=decision,
    )


    search_results = collect_search_results(
        queries=queries,
        results_per_query=4,
    )


    documents = load_web_documents(

        search_results=search_results,

        max_pages=max_pages,
    )


    chunks = split_web_documents(
        documents
    )


    evidence = []


    # We keep a controlled number of chunks.
    # This prevents huge prompts and protects
    # your Gemini quota.

    for chunk in chunks[:12]:

        evidence.append(
            {
                "title": chunk.metadata.get(
                    "title",
                    "Web source",
                ),

                "url": chunk.metadata.get(
                    "url",
                    "",
                ),

                "search_query": chunk.metadata.get(
                    "search_query",
                    "",
                ),

                "content": chunk.page_content,
            }
        )


    return {

        "queries": queries,

        "search_results": search_results,

        "documents": documents,

        "chunks": chunks,

        "evidence": evidence,
    }


# =========================================================
# BUILD GEMINI-READY CONTEXT
# =========================================================

def build_web_context(
    evidence: list[dict],
) -> str:
    """
    Convert retrieved web evidence into a compact
    context block that can later be passed to Gemini.
    """

    if not evidence:

        return (
            "No public web evidence was retrieved."
        )


    sections = []


    for index, item in enumerate(
        evidence,
        start=1,
    ):

        title = item.get(
            "title",
            "Web source",
        )

        url = item.get(
            "url",
            "",
        )

        content = item.get(
            "content",
            "",
        )


        sections.append(
            "\n".join(
                [
                    f"WEB EVIDENCE {index}",
                    f"Title: {title}",
                    f"URL: {url}",
                    "Content:",
                    content,
                ]
            )
        )


    return "\n\n".join(
        sections
    )