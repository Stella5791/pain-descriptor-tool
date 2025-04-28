import pandas as pd

# Load the main tagged CSV and your manual edits
main = pd.read_csv("pain_tags_output.csv")
edits = pd.read_csv("flagged_descriptors.csv")

# Apply each manual edit one row at a time
for _, row in edits.iterrows():
    dims_text = row.get("dimensions")
    mets_text = row.get("metaphor_types")
    if pd.notna(dims_text) and pd.notna(mets_text):
        # Prepare the lists
        dims = [d.strip() for d in dims_text.split(",")]
        mets = [m.strip() for m in mets_text.split(",")]
        # Find matching rows in the main file
        matches = main["descriptor"] == row["descriptor"]
        for idx in main[matches].index:
            main.at[idx, "dimensions"] = dims
            main.at[idx, "metaphor_types"] = mets
            main.at[idx, "flag"] = False

# Save the merged results back to CSV
main.to_csv("pain_tags_output.csv", index=False)
print("✅ Merged your manual tags into pain_tags_output.csv")
