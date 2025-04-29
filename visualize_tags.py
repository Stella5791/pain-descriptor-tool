import pandas as pd
import matplotlib.pyplot as plt

# Load your fully tagged data
df = pd.read_csv('pain_tags_output.csv')

# ——— Dimension Distribution ———
# Split comma-lists into individual rows
dims = df['dimensions'].str.split(',').explode().str.strip()
dim_counts = dims.value_counts()

plt.figure()
dim_counts.plot(kind='bar')
plt.title('Distribution of Dimensions')
plt.xlabel('Dimension')
plt.ylabel('Count')
plt.tight_layout()
plt.show()

# ——— Metaphor Type Distribution ———
mets = df['metaphor_types'].str.split(',').explode().str.strip()
met_counts = mets.value_counts()

plt.figure()
met_counts.plot(kind='bar')
plt.title('Distribution of Metaphor Types')
plt.xlabel('Metaphor Type')
plt.ylabel('Count')
plt.tight_layout()
plt.show()
