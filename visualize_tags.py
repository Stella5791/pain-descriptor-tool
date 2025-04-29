import pandas as pd
import matplotlib.pyplot as plt
import ast

# Load your final tagged data
df = pd.read_csv('pain_tags_output.csv')

# Helper to parse the string-ified lists


def parse_list(cell):
    try:
        return ast.literal_eval(cell)
    except:
        return []


# Turn each dimension into its own row, drop blanks
dims = df['dimensions'].astype(str).apply(parse_list).explode()
dims = dims[dims != '']

# Count and plot
dim_counts = dims.value_counts()
plt.figure()
dim_counts.plot(kind='bar')
plt.title('Distribution of Dimensions')
plt.xlabel('Dimension')
plt.ylabel('Count')
plt.tight_layout()
plt.show()

# Do the same for metaphor_types
mets = df['metaphor_types'].astype(str).apply(parse_list).explode()
mets = mets[mets != '']
met_counts = mets.value_counts()
plt.figure()
met_counts.plot(kind='bar')
plt.title('Distribution of Metaphor Types')
plt.xlabel('Metaphor Type')
plt.ylabel('Count')
plt.tight_layout()
plt.show()
