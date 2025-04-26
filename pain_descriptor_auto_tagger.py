import pandas as pd
import re
from nltk.stem import PorterStemmer

INPUT_CSV = "pain_tags_input.csv"
OUTPUT_CSV = "pain_tags_clean.csv"

stemmer = PorterStemmer()

METAPHOR_THEMES = {
    "violence_with_object": [
        "knife", "blade", "stab", "pierce", "needle", "dagger", "spear", "drill",
        "grind", "screw", "metal", "vice", "machine", "jammed", "tightened", "cogs", "clamp"
    ],
    "heat_temperature": [
        "fire", "burn", "molten", "scorch", "boil", "sear", "hot", "blazing"
    ],
    "motion_forceful": [
        "shoot", "surge", "thrust", "pulse", "jolt", "crawl", "creep", "flutter"
    ],
    "transformative_state": [
        "blacking out", "melting", "losing consciousness", "disappearing", "vanishing",
        "unnatural", "doesn't belong", "foreign", "frankenstein", "witch", "monster"
    ],
    "weight_pressure": [
        "heavy", "load", "burden", "crush", "block", "concrete"
    ]
}

SIMILE_PATTERNS = [
    r"\bfeels like\b", r"\bas if\b", r"\blike a\b", r"\blike an\b"
]


def stem_text(text):
    """
    Tokenize and stem the text for keyword matching.
    """
    words = re.findall(r"\b\w+\b", text.lower())
    return set(stemmer.stem(word) for word in words)


def detect_metaphor_type(text):
    """
    Detects if the text contains a simile or metaphor and returns a tuple:
      ("simile" or "metaphorical" or "", list of theme subtypes)
    """
    text_lower = str(text).lower()
    simile_flag = any(re.search(pat, text_lower) for pat in SIMILE_PATTERNS)
    metaphorical = False
    subtypes = []

    for theme, keywords in METAPHOR_THEMES.items():
        for keyword in keywords:
            # Check for multi-word keywords first
            if " " in keyword and keyword in text_lower:
                metaphorical = True
                subtypes.append(theme)
                break
            # Otherwise check stemmed single words
            elif stemmer.stem(keyword) in stem_text(text_lower):
                metaphorical = True
                subtypes.append(theme)
                break

    if metaphorical or simile_flag:
        type_label = "simile" if simile_flag else "metaphorical"
        return type_label, list(set(subtypes))
    else:
        return "", []


def assign_experience_tags(text):
    """
    Assigns experience tags based on sensory, affective, or temporal keywords.
    """
    text = text.lower()
    tags = []

    # Sensory cues
    if any(word in text for word in [
        "burn", "stab", "shoot", "tight", "crawl", "crush",
        "fire", "pierce", "pain", "hot", "sting"
    ]):
        tags.append("sensory")

    # Affective or emotional reactions
    if any(word in text for word in [
        "monster", "witch", "frankenstein", "insane",
        "unravel", "losing my mind", "explode", "volcano"
    ]):
        tags.append("affective")

    # Temporal references
    if any(word in text for word in [
        "always", "constant", "sudden", "gradual", "never ends", "won't stop", "creeping"
    ]):
        tags.append("temporal")

    return tags


def prioritize_experience(tags):
    """
    Chooses a single salient experience tag, preferring affective > sensory > temporal.
    """
    if "affective" in tags:
        return "affective"
    elif "sensory" in tags:
        return "sensory"
    elif "temporal" in tags:
        return "temporal"
    return ""


def estimate_intensity(text):
    """
    Estimates the intensity level of the pain based on keywords.
    """
    text = text.lower()
    # High intensity
    if any(word in text for word in [
        "stab", "explode", "burning", "crushed", "shooting", "severe"
    ]):
        return "high"
    # Medium intensity
    elif any(word in text for word in [
        "tight", "sharp", "dull", "pounding", "nagging", "throbbing"
    ]):
        return "medium"
    # Low intensity
    elif any(word in text for word in [
        "flutter", "tingling", "light", "buzz", "flicker"
    ]):
        return "low"
    return ""


def run_auto_tagger(input_path=INPUT_CSV, output_path=OUTPUT_CSV):
    """
    Loads input CSV, applies tagging functions, and writes to output CSV.
    """
    df = pd.read_csv(input_path)

    df["metaphor_type"], df["metaphor_subtypes"] = zip(*
                                                       df["feels like…"].apply(
                                                           detect_metaphor_type)
                                                       )
    df["experience_tags"] = df["feels like…"].apply(assign_experience_tags)
    df["salient_experience"] = df["experience_tags"].apply(
        prioritize_experience)
    df["intensity_level"] = df["feels like…"].apply(estimate_intensity)

    df.to_csv(output_path, index=False)
    print(f"✅ Auto-tagging complete. File saved as: {output_path}")


if __name__ == "__main__":
    run_auto_tagger()
