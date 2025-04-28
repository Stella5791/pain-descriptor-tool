import pandas as pd
import re
from nltk.stem import PorterStemmer

INPUT_CSV = "pain_tags_input.csv"
OUTPUT_CSV = "pain_tags_clean.csv"

stemmer = PorterStemmer()

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
    "transformative_state": ["black out", "fade", "lose consciousness", "disappear", "melt away", "detach"],
    "death": ["die", "decay", "lifeless", "rot"],
    "illness": ["infect", "sicken", "poison", "disease", "inflame", "virus", "spread"],
    "injury": ["break", "bruise", "bleed", "fracture", "wound", "tear", "scar"],
    "journey": ["path", "road", "go through", "stuck", "lost", "cross", "wander", "climb"],
    "childbirth": ["contraction", "push", "labor", "deliver", "birth", "give birth"],
    "organic_entity": ["grow inside", "root", "plant", "spread", "infest", "burrow"]
}

SIMILE_PATTERNS = [
    r"\bfeels like\b", r"\bas if\b", r"\blike a\b", r"\blike an\b"
]


def stem_text(text):
    words = re.findall(r"\b\w+\b", text.lower())
    return set(stemmer.stem(word) for word in words)


def detect_metaphor_type(text):
    text_lower = str(text).lower()
    simile_flag = any(re.search(pat, text_lower) for pat in SIMILE_PATTERNS)
    metaphorical = False
    subtypes = []
    for theme, keywords in METAPHOR_THEMES.items():
        for keyword in keywords:
            if " " in keyword and keyword in text_lower:
                metaphorical = True
                subtypes.append(theme)
                break
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
    text = str(text).lower()
    tags = []
    if any(word in text for word in [
        "burn", "stab", "shoot", "tight", "crawl", "crush",
        "fire", "pierce", "pain", "hot", "sting"
    ]):
        tags.append("sensory")
    if any(word in text for word in [
        "monster", "witch", "frankenstein", "insane",
        "unravel", "losing my mind", "explode", "volcano"
    ]):
        tags.append("affective")
    if any(word in text for word in [
        "always", "constant", "sudden", "gradual", "never ends", "won't stop", "creeping"
    ]):
        tags.append("temporal")
    return tags


def prioritize_experience(tags):
    if "affective" in tags:
        return "affective"
    elif "sensory" in tags:
        return "sensory"
    elif "temporal" in tags:
        return "temporal"
    return ""


def estimate_intensity(text):
    text = str(text).lower()
    if any(word in text for word in [
        "stab", "explode", "burning", "crushed", "shooting", "severe"
    ]):
        return "high"
    elif any(word in text for word in [
        "tight", "sharp", "dull", "pounding", "nagging", "throbbing"
    ]):
        return "medium"
    elif any(word in text for word in [
        "flutter", "tingling", "light", "buzz", "flicker"
    ]):
        return "low"
    return ""


def run_auto_tagger(input_path=INPUT_CSV, output_path=OUTPUT_CSV):
    df = pd.read_csv(input_path)
    df["metaphor_type"], df["metaphor_subtypes"] = zip(
        *df["feels like…"].apply(detect_metaphor_type))
    df["experience_tags"] = df["feels like…"].apply(assign_experience_tags)
    df["salient_experience"] = df["experience_tags"].apply(
        prioritize_experience)
    df["intensity_level"] = df["feels like…"].apply(estimate_intensity)
    df.to_csv(output_path, index=False)
    print(f"✅ Auto-tagging complete. File saved as: {output_path}")


if __name__ == "__main__":
    run_auto_tagger()
