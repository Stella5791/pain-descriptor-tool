import pandas as pd
import re
import json
import os
from nltk.stem import PorterStemmer

# Load taxonomy configuration
taxonomy_path = 'taxonomy.json'
with open(taxonomy_path, 'r') as f:
    taxonomy = json.load(f)

dimensions = taxonomy['dimensions']
metaphor_types = taxonomy['metaphor_types']
raw_keywords = taxonomy['keywords']

# Initialize stemmer and pre-stem keywords for matching
stemmer = PorterStemmer()
stemmed_keywords = {
    category: set(stemmer.stem(word.lower()) for word in words)
    for category, words in raw_keywords.items()
}

def normalize_text(text):
    """
    Lowercase, tokenize, and stem the input text.
    Returns a list of stemmed tokens.
    """
    text = str(text).lower()
    tokens = re.findall(r"\b\w+\b", text)
    return [stemmer.stem(token) for token in tokens]

def classify_descriptor_rulebased(text):
    """
    Classify a descriptor into dimensions and metaphor types via keyword matching.
    """
    stems = normalize_text(text)
    dims = [d for d in dimensions if any(kw in stems for kw in stemmed_keywords.get(d, []))]
    mets = [m for m in metaphor_types if any(kw in stems for kw in stemmed_keywords.get(m, []))]
    if not dims:
        dims = ['unspecified']
    if not mets:
        mets = ['other']
    return dims, mets

def batch_process(input_csv, output_csv):
    """
    Auto-tag all descriptors, preserving any existing manual tags in output_csv.
    """
    # Read raw input
    df = pd.read_csv(input_csv)
    text_col = df.columns[0]
    df = df.rename(columns={text_col: 'descriptor'})

    # Prepare new columns
    df['dimensions'] = None
    df['metaphor_types'] = None
    df['flag'] = False

    # Load existing output to preserve manual tags
    existing = {}
    if os.path.exists(output_csv):
        old_df = pd.read_csv(output_csv)
        if 'descriptor' not in old_df.columns:
            old_text_col = old_df.columns[0]
            old_df = old_df.rename(columns={old_text_col: 'descriptor'})
        for idx, row in old_df.iterrows():
            desc = row['descriptor']
            existing[desc] = (row.get('dimensions'), row.get('metaphor_types'), row.get('flag', True))

    # Process each descriptor
    for idx, row in df.iterrows():
        desc = row['descriptor']
        if desc in existing and existing[desc][2] == False:
            # Preserve manual tags
            df.at[idx, 'dimensions'] = existing[desc][0]
            df.at[idx, 'metaphor_types'] = existing[desc][1]
            df.at[idx, 'flag'] = False
        else:
            # Auto-classify
            dims, mets = classify_descriptor_rulebased(desc)
            df.at[idx, 'dimensions'] = dims
            df.at[idx, 'metaphor_types'] = mets
            df.at[idx, 'flag'] = (dims == ['unspecified'] and mets == ['other'])

    df.to_csv(output_csv, index=False)
    print(f'✅ Batch processing complete. Saved to {output_csv}')

def manual_review(output_csv):
    """
    Group flagged items for batch review in the CLI, assigning tags iteratively.
    """
    df = pd.read_csv(output_csv)
    if 'descriptor' not in df.columns:
        text_col = df.columns[0]
        df = df.rename(columns={text_col: 'descriptor'})
    flagged = df[df['flag']]
    if flagged.empty:
        print('No flagged items for review!')
        return

    # Group by normalized text to batch similar entries
    groups = {}
    for text in flagged['descriptor']:
        norm = ' '.join(normalize_text(text))
        groups.setdefault(norm, []).append(text)

    for norm, texts in groups.items():
        print(f"\nGroup of similar descriptors:\n{texts}")
        dims_input = input(f"Enter dimensions (choose from {dimensions}): ")
        mets_input = input(f"Enter metaphor types (choose from {metaphor_types}): ")
        dims = [d.strip() for d in dims_input.split(',') if d.strip() in dimensions]
        mets = [m.strip() for m in mets_input.split(',') if m.strip() in metaphor_types]
        for text in texts:
            for i in df[df['descriptor'] == text].index:
                df.at[i, 'dimensions'] = dims
                df.at[i, 'metaphor_types'] = mets
                df.at[i, 'flag'] = False

    df.to_csv(output_csv, index=False)
    print(f'✅ Manual review complete. Updated {output_csv}')

def add_descriptor(text, output_csv):
    """
    Add a new descriptor, auto-tag it, and append to CSV.
    """
    if not os.path.exists(output_csv):
        print(f"Output file not found: {output_csv}")
        return
    df = pd.read_csv(output_csv)
    if 'descriptor' not in df.columns:
        text_col = df.columns[0]
        df = df.rename(columns={text_col: 'descriptor'})

    existing_norms = {' '.join(normalize_text(t)): t for t in df['descriptor']}
    norm = ' '.join(normalize_text(text))
    if norm in existing_norms:
        print(f"Descriptor already exists: '{existing_norms[norm]}'")
        return

    dims, mets = classify_descriptor_rulebased(text)
    flag = (dims == ['unspecified'] and mets == ['other'])
    new_row = {'descriptor': text, 'dimensions': dims, 'metaphor_types': mets, 'flag': flag}
    df = df.append(new_row, ignore_index=True)
    df.to_csv(output_csv, index=False)
    print(f"✅ Added and tagged '{text}'. Saved to {output_csv}")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Pain Descriptor Tagging Tool')
    parser.add_argument('--batch', action='store_true', help='Run batch auto-tagging')
    parser.add_argument('--review', action='store_true', help='Run manual review')
    parser.add_argument('--add', type=str, metavar='TEXT', help='Add a new descriptor')
    parser.add_argument('--input', type=str, default='pain_tags_input.csv', help='Input CSV path')
    parser.add_argument('--output', type=str, default='pain_tags_output.csv', help='Output CSV path')
    args = parser.parse_args()

    if args.batch:
        batch_process(args.input, args.output)
    elif args.review:
        manual_review(args.output)
    elif args.add:
        add_descriptor(args.add, args.output)
    else:
        print("Please specify an action: --batch, --review, or --add")
