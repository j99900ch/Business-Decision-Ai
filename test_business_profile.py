from business.profile import (
    create_profile,
    save_profile,
    load_profile,
)


profile = create_profile(
    company_name="Tata Pvt Ltd",
    industry="Automotive Equipment",
    products="Motors",
    market="India",
    location="India",
)

print("Company ID:")
print(profile.company_id)

path = save_profile(profile)

print("\nProfile saved:")
print(path)

loaded_profile = load_profile(
    profile.company_id
)

print("\nLoaded profile:")
print(loaded_profile)