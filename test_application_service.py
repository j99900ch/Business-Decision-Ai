from decision_context.application_service import (
    BusinessDecisionService,
)


print("=" * 60)
print("APPLICATION SERVICE TEST")
print("=" * 60)


service = BusinessDecisionService(
    company_name="Tata Pvt Ltd",
    industry="Automotive Equipment",
    products="Motors",
    market="India",
    location="India",
)


decision = (
    "Should I increase my investment "
    "in motor inventory?"
)


print("\nSaving business profile...")

profile_path = (
    service.save_business_profile()
)

print(
    "Profile saved:",
    profile_path,
)


print("\nRetrieving company knowledge...")

rag_evidence = (
    service.retrieve_company_knowledge(
        business_decision=decision,
        k=4,
    )
)


print(
    "RAG evidence retrieved:",
    len(rag_evidence),
)


for index, item in enumerate(
    rag_evidence,
    start=1,
):

    print(
        f"\n--- Evidence {index} ---"
    )

    print(
        "Source:",
        item["source"],
    )

    print(
        item["content"]
    )


print("\n" + "=" * 60)
print("APPLICATION SERVICE TEST: PASS")
print("=" * 60)