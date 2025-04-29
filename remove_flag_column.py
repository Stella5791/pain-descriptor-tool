import pandas as pd

# Load the fully tagged CSV
df = pd.read_csv('pain_tags_output.csv')

# Drop the flag column
df = df.drop(columns=['flag'])

# Save the cleaned CSV
df.to_csv('pain_tags_output_clean.csv', index=False)
print("✅ Saved cleaned file as pain_tags_output_clean.csv")
