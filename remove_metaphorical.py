import pandas as pd
import ast

# Load the existing tagged CSV
df = pd.read_csv('pain_tags_output.csv')

# Remove 'metaphorical' from the dimensions list
def clean_dimensions(dim_str):
    try:
        dims = ast.literal_eval(dim_str)
    except Exception:
        dims = [d.strip().strip("[]'\"") for d in dim_str.split(',')]
    cleaned = [d for d in dims if d != 'metaphorical']
    return cleaned

df['dimensions'] = df['dimensions'].apply(clean_dimensions)
df.to_csv('pain_tags_output.csv', index=False)
print("✅ Removed 'metaphorical' and updated pain_tags_output.csv")
