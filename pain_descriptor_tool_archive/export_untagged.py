
import pandas as pd

# Step 1: Load the full tagged data
df = pd.read_csv("pain_tags_clean.csv")

# Step 2: List of important columns to check
important_columns = [
    "metaphor_type",
    "metaphor_subtypes",
    "experience_tags",
    "salient_experience",
    "intensity_level"
]

# Step 3: Build a mask (True if any of the important fields are missing or blank)
mask = False
for col in important_columns:
    mask = mask | (df[col].isna() | (df[col].astype(str).str.strip() == ""))

# Step 4: Filter untagged rows
untagged = df[mask]

# Step 5: Save to a new review file
untagged.to_csv("pain_descriptors_untagged_review.csv", index=False)

print(
    f"✅ Exported {len(untagged)} untagged expressions to pain_descriptors_untagged_review.csv")
