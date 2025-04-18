
import pandas as pd
import re

# Load the file you are actively tagging
INPUT_FILE = "pain_descriptors_tagged_manual_v2.csv"
OUTPUT_FILE = "pain_descriptors_tagged_with_auto.csv"

# Updated metaphor themes
METAPHOR_THEMES = {
    "conflict": [
        "battle", "war", "fight", "enemy", "attacked", "struggle", "combat", "warrior"
    ],
    "violent_action": [
        "tearing", "ripping", "twisting", "pulling", "breaking", "crushing", "smashing", "pounding"
    ],
    "violence_with_object": [
        "knife", "blade", "drill", "piercing", "stabbing", "needle", "dagger", "spear"
    ],
    "weather": [
        "storm", "cloud", "wave", "fog", "rain", "wind", "lightning", "thunder", "tsunami", "whirlwind"
    ],
    "confinement": [
        "trapped", "prison", "cage", "locked", "confined", "chained", "barred", "held"
    ],
    "attacking_agents": [
        "monster", "creature", "beast", "parasite", "demon", "entity", "thing", "it"
    ],
    "weight_pressure": [
        "weight", "heavy", "load", "burden", "crushing", "pressing", "sinking", "bearing"
    ],
    "heat_temperature": [
        "fire", "burning", "molten", "scorching", "ice", "freezing", "boiling", "searing"
    ],
    "motion_violent": [
        "spinning", "crashing", "tumbling", "whirling", "jerking", "convulsing", "exploding"
    ],
    "motion_forceful": [
        "shooting", "surging", "thrusting", "radiating", "pulsing", "moving", "jolting"
    ],
    "transformative_force": [
        "blacking out", "fading", "losing consciousness", "disappearing", "melting away", "detaching"
    ],
    "death": [
        "dying", "decaying", "lifeless", "rotting"
    ],
    "illness": [
        "infected", "sickening", "poisoned", "disease", "inflamed", "virus", "spreading"
    ],
    "injury": [
        "broken", "bruised", "bleeding", "fractured", "wounded", "torn", "scarred"
    ],
    "journey": [
        "path", "road", "going through", "stuck", "lost", "crossing", "wandering", "climbing"
    ],
    "childbirth": [
        "contractions", "pushing", "labor", "delivering", "birthing", "giving birth"
    ],
    "organic_entity": [
        "growing inside", "roots", "plant", "spreading", "infesting", "burrowing"
    ]
}

SIMILE_PATTERNS = [
    r"\bfeels like\b",
    r"\bas if\b",
    r"\blike a\b",
    r"\blike an\b"
]

def detect_metaphors(text):
    text_lower = str(text).lower()
    detected_themes = []
    simile_flag = any(re.search(pat, text_lower) for pat in SIMILE_PATTERNS)

    for theme, keywords in METAPHOR_THEMES.items():
        for keyword in keywords:
            if re.search(rf"\b{re.escape(keyword)}\b", text_lower):
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

# Run detection
df = pd.read_csv(INPUT_FILE)
df["auto_metaphorical_label"], df["auto_metaphor_subtypes"] = zip(*df["feels like…"].apply(detect_metaphors))
df.to_csv(OUTPUT_FILE, index=False)
print("✅ Auto metaphor tagging complete. File saved as:", OUTPUT_FILE)
