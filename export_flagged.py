import pandas as pd

# Load your main tagged file
df = pd.read_csv("pain_tags_output.csv")

# Extract only the still-flagged descriptors
to_review = df[df.flag][["descriptor"]]

# Write them out for manual tagging
to_review.to_csv("flagged_descriptors.csv", index=False)

# Print how many remain
print(f"{len(to_review)} descriptors remain for review")
