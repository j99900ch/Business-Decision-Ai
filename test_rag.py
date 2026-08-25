from business.profile import load_profile
from rag.rag_engine import RAGEngine


COMPANY_ID = "TATA_PVT_LTD"

DOCUMENT_PATH = (
    "data/companies/"
    "TATA_PVT_LTD/"
    "company_test.txt"
)


profile = load_profile(
    COMPANY_ID
)

print("=" * 60)
print("BUSINESS PROFILE")
print("=" * 60)

print(
    "Company:",
    profile.company_name
)

print(
    "Industry:",
    profile.industry
)

print(
    "Products:",
    profile.products
)

print(
    "Market:",
    profile.market
)


print("\n" + "=" * 60)
print("RAG INGESTION")
print("=" * 60)


engine = RAGEngine()

result = engine.ingest_document(
    company_id=COMPANY_ID,
    file_path=DOCUMENT_PATH,
)

print(result)


print("\n" + "=" * 60)
print("RAG RETRIEVAL")
print("=" * 60)


query = (
    "What products does this company sell "
    "and what should management consider "
    "before increasing inventory investment?"
)


documents = engine.retrieve(
    company_id=COMPANY_ID,
    query=query,
    k=3,
)


for index, document in enumerate(
    documents,
    start=1,
):

    print(
        f"\n--- Retrieved Result {index} ---"
    )

    print(
        "Company ID:",
        document.metadata.get(
            "company_id"
        ),
    )

    print(
        document.page_content
    )