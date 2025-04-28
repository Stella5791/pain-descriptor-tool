import pandas as pd
import re
import json
from nltk.stem import PorterStemmer

# Load taxonomy configuration
with open('taxonomy.json', 'r') as f:
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
    Classify a descriptor into dimensions and metaphor types
    using simple keyword matching.
    """
    stems = normalize_text(text)
    # Determine dimensions
    dims = []
    for d in dimensions:
        for kw in stemmed_keywords.get(d, []):
            if kw in stems:
                dims.append(d)
                break
    # Determine metaphor types
    mets = []
    for m in metaphor_types:
        for kw in stemmed_keywords.get(m, []):
            if kw in stems:
                mets.append(m)
                break
    # Fallbacks
    if not dims:
        dims = ['unspecified']
    if not mets:
        mets = ['other']
    return dims, mets


def batch_process(input_csv, output_csv):
    """
    Run rule-based tagging on all descriptors.
    Flags any items where both dims and mets are fallback values.
    """
    df = pd.read_csv(input_csv)
    # Prepare output columns
    df['dimensions'] = None
    df['metaphor_types'] = None
    df['flag'] = False

    for idx, row in df.iterrows():
        dims, mets = classify_descriptor_rulebased(row['descriptor'])
        df.at[idx, 'dimensions'] = dims
        df.at[idx, 'metaphor_types'] = mets
        if dims == ['unspecified'] and mets == ['other']:
            df.at[idx, 'flag'] = True

    df.to_csv(output_csv, index=False)
    print(f'✅ Batch processing complete. Saved to {output_csv}')


def manual_review(output_csv):
    """
    Group flagged descriptors and prompt user for manual tagging.
    """
    df = pd.read_csv(output_csv)
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
        dims_input = input(f"Enter dimensions (choose from {dimensions}, comma-separated): ")
        mets_input = input(f"Enter metaphor types (choose from {metaphor_types}, comma-separated): ")
        dims = [d.strip() for d in dims_input.split(',') if d.strip() in dimensions]
        mets = [m.strip() for m in mets_input.split(',') if m.strip() in metaphor_types]
        # Update DataFrame
        for text in texts:
            idx = df[df['descriptor'] == text].index
            df.at[idx, 'dimensions'] = dims
            df.at[idx, 'metaphor_types'] = mets
            df.at[idx, 'flag'] = False

    df.to_csv(output_csv, index=False)
    print(f'✅ Manual review complete. Updated {output_csv}')


def add_descriptor(text, output_csv):
    """
    Add a new descriptor, auto-tag it, and append to CSV.
    """
    df = pd.read_csv(output_csv)
    # Check for duplicates by normalized form
    existing_norms = { ' '.join(normalize_text(t)): t for t in df['descriptor'] }
    norm = ' '.join(normalize_text(text))
    if norm in existing_norms:
        print(f"Descriptor already exists: '{existing_norms[norm]}'")
        return

    dims, mets = classify_descriptor_rulebased(text)
    flag = dims == ['unspecified'] and mets == ['other']
    new_row = {'descriptor': text, 'dimensions': dims, 'metaphor_types': mets, 'flag': flag}
    df = df.append(new_row, ignore_index=True)
    df.to_csv(output_csv, index=False)
    print(f"✅ Added and tagged '{text}'. Saved to {output_csv}")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Pain Descriptor Tagging Tool')
    parser.add_argument('--batch', action='store_true', help='Run batch auto-tagging')
    parser.add_argument('--review', action='store_true', help='Run manual review on flagged items')
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
