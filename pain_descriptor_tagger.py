
import pandas as pd
import tkinter as tk
from tkinter import ttk
import re

# --- Updated METAPHOR THEMES ---
METAPHOR_THEMES = {
    "conflict": ["battle", "war", "fight", "enemy", "attacked", "struggle", "combat", "warrior"],
    "violent_action": ["tearing", "ripping", "twisting", "pulling", "breaking", "crushing", "smashing", "pounding"],
    "violence_with_object": ["knife", "blade", "drill", "piercing", "stabbing", "needle", "dagger", "spear"],
    "weather": ["storm", "cloud", "wave", "fog", "rain", "wind", "lightning", "thunder", "tsunami", "whirlwind"],
    "confinement": ["trapped", "prison", "cage", "locked", "confined", "chained", "barred", "held"],
    "attacking_agents": ["monster", "creature", "beast", "parasite", "demon", "entity", "thing", "it"],
    "weight_pressure": ["weight", "heavy", "load", "burden", "crushing", "pressing", "sinking", "bearing"],
    "heat_temperature": ["fire", "burning", "molten", "scorching", "ice", "freezing", "boiling", "searing"],
    "motion_violent": ["spinning", "crashing", "tumbling", "whirling", "jerking", "convulsing", "exploding"],
    "motion_forceful": ["shooting", "surging", "thrusting", "radiating", "pulsing", "moving", "jolting"],
    "transformative_force": ["blacking out", "fading", "losing consciousness", "disappearing", "melting away", "detaching"],
    "death": ["dying", "decaying", "lifeless", "fading", "rotting"],
    "illness": ["infected", "sickening", "poisoned", "disease", "inflamed", "virus", "spreading"],
    "injury": ["broken", "bruised", "bleeding", "fractured", "wounded", "torn", "scarred"],
    "journey": ["path", "road", "going through", "stuck", "lost", "crossing", "wandering", "climbing"],
    "childbirth": ["contractions", "pushing", "labor", "delivering", "birthing", "giving birth"],
    "organic_entity": ["growing inside", "roots", "plant", "spreading", "infesting", "burrowing"]
}


def detect_metaphors(text):
    text_lower = text.lower()
    detected_themes = []
    simile_flag = False

    # Check for simile patterns
    simile_patterns = [
        r"\bfeels like\b",
        r"\bas if\b",
        r"\blike a\b",
        r"\blike an\b"
    ]
    if any(re.search(pattern, text_lower) for pattern in simile_patterns):
        simile_flag = True

    # Check for metaphor themes
    for theme, keywords in METAPHOR_THEMES.items():
        for keyword in keywords:
            if re.search(rf"\b{keyword}\b", text_lower):
                detected_themes.append(theme)
                break

    if detected_themes or simile_flag:
        label = "Metaphorical ("
        if simile_flag:
            label += "Simile"
            if detected_themes:
                label += ", " + ", ".join(detected_themes)
        else:
            label += ", ".join(detected_themes)
        label += ")"
        return label
    else:
        return None


# --- Apply metaphor detection to dataset ---
df = pd.read_csv("pain_descriptors_categorized_updated.csv")


# Ensure the column exists and apply the function
if "feels like…" in df.columns:
    df["metaphorical_label"] = df["feels like…"].astype(
        str).apply(detect_metaphors)
else:
    raise KeyError("The column 'feels like…' is missing from the dataset.")

# Save to new file
df.to_csv("pain_descriptors_with_metaphors.csv", index=False)
print("Metaphor detection complete. File saved as pain_descriptors_with_metaphors.csv")
