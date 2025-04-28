#!/usr/bin/env python
import pandas as pd
import os
from pain_descriptor_auto_tagger import (
    detect_metaphor_type,
    assign_experience_tags,
    prioritize_experience,
    estimate_intensity
)

infile = "pain_descriptors_untagged_review.csv"
if not os.path.exists(infile):
    raise FileNotFoundError(
        f"{infile} not found – run export_untagged.py first")
df = pd.read_csv(infile)

df[["metaphor_type", "metaphor_subtypes"]] = (
    df["feels like…"]
    .apply(detect_metaphor_type)
    .apply(pd.Series)
)
df["experience_tags"] = df["feels like…"].apply(assign_experience_tags)
df["salient_experience"] = df["experience_tags"].apply(prioritize_experience)
df["intensity_level"] = df["feels like…"].apply(estimate_intensity)

outfile = "pain_tags_auto_filled.csv"
df.to_csv(outfile, index=False)
print(f"✅ Wrote {len(df)} auto‐filled rows to {outfile}")
