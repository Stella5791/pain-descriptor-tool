
import pandas as pd
import re
import os
from nltk.stem import PorterStemmer

# Initialize the stemmer
stemmer = PorterStemmer()

# Updated metaphor themes with stemmed keywords
METAPHOR_THEMES = {
    "conflict": ["battle", "war", "fight", "enemy", "attack", "struggle", "combat", "warrior"],
    "violent_action": ["tear", "rip", "twist", "pull", "break", "crush", "smash", "pound"],
    "violence_with_object": ["knife", "blade", "drill", "pierce", "stab", "needle", "dagger", "spear"],
    "weather": ["storm", "cloud", "wave", "fog", "rain", "wind", "lightning", "thunder", "tsunami", "whirlwind"],
    "confinement": ["trap", "prison", "cage", "lock", "confine", "chain", "bar", "hold"],
    "attacking_agents": ["monster", "creature", "beast", "parasite", "demon", "entity", "thing"],
    "weight_pressure": ["weight", "heavy", "load", "burden", "crush", "press", "sink", "bear"],
    "heat_temperature": ["fire", "burn", "molten", "scorch", "ice", "freeze", "boil", "sear"],
    "motion_violent": ["spin", "crash", "tumble", "whirl", "jerk", "convulse", "explode"],
    "motion_forceful": ["shoot", "surge", "thrust", "radiate", "pulse", "move", "jolt"],
    "transformative_force": ["black out", "fade", "lose consciousness", "disappear", "melt away", "detach"],
    "death": ["die", "decay", "lifeless", "rot"],
    "illness": ["infect", "sicken", "poison", "disease", "inflame", "virus", "spread"],
    "injury": ["break", "bruise", "bleed", "fracture", "wound", "tear", "scar"],
    "journey": ["path", "road", "go through", "stuck", "lost", "cross", "wander", "climb"],
    "childbirth": ["contraction", "push", "labor", "deliver", "birth", "give birth"],
    "organic_entity": ["grow inside", "root", "plant", "spread", "infest", "burrow"]
}

SIMILE_PATTERNS = [
    r"\bfeels like\b",
    r"\bas if\b",
    r"\blike a\b",
    r"\blike an\b"
]

def stem_text(text):
    words = re.findall(r"\b\w+\b", text.lower())
    return set(stemmer.stem(word) for word in words)

def detect_metaphors(text):
    text_lower = str(text).lower()
    text_stems = stem_text(text_lower)
    detected_themes = []
    simile_flag = any(re.search(pat, text_lower) for pat in SIMILE_PATTERNS)

    for theme, keywords in METAPHOR_THEMES.items():
        for keyword in keywords:
            if " " in keyword:
                if keyword in text_lower:
                    detected_themes.append(theme)
                    break
            else:
                if stemmer.stem(keyword) in text_stems:
                    detected_themes.append(theme)
                    break

    if simile_flag or detected_themes:
        label = "metaphorical ("
        if simile_flag:
            label += "simile"
            if detected_themes:
                label += ", " + ", ".join(detected_themes)
        else:
            label += ", ".join(detected_themes)
        label += ")"
        return label, ", ".join(detected_themes)
    else:
        return "", ""

# Load, run, and save
INPUT_FILE = "pain_descriptors_tagged_manual_v2.csv"
OUTPUT_FILE = "pain_descriptors_tagged_with_auto.csv"

if os.path.exists(INPUT_FILE):
    df = pd.read_csv(INPUT_FILE)
    df["auto_metaphorical_label"], df["auto_metaphor_subtypes"] = zip(*df["feels like…"].apply(detect_metaphors))
    df.to_csv(OUTPUT_FILE, index=False)
    print("✅ Improved auto-tagging complete. File saved as:", OUTPUT_FILE)
else:
    print("❌ Input file not found.")
