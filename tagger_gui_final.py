
import pandas as pd
import tkinter as tk
from tkinter import ttk
import os

# Load descriptors
INPUT_FILE = "pain_descriptors_categorized_updated.csv"
OUTPUT_FILE = "pain_descriptors_tagged_manual_v2.csv"

if os.path.exists(OUTPUT_FILE):
    df = pd.read_csv(OUTPUT_FILE)
else:
    df = pd.read_csv(INPUT_FILE)
    df["manual_category"] = ""
    df["metaphor_subtypes"] = ""

current_index = 0

METAPHOR_SUBTYPES = [
    "conflict", "violent_action", "violence_with_object", "weather",
    "confinement", "attacking_agents", "weight_pressure", "heat_temperature",
    "motion_violent", "motion_forceful", "transformative_force", "death",
    "illness", "injury", "journey", "childbirth", "organic_entity"
]


def save_and_next():
    global current_index
    selected_categories = []
    if sensory_var.get():
        selected_categories.append("sensory")
    if affective_var.get():
        selected_categories.append("affective")
    if metaphorical_var.get():
        selected_categories.append("metaphorical")
    if temporal_var.get():
        selected_categories.append("temporal")

    selected_subtypes = [key for key, var in subtype_vars.items() if var.get()]

    df.at[current_index, "manual_category"] = ", ".join(selected_categories)
    df.at[current_index, "metaphor_subtypes"] = ", ".join(selected_subtypes)
    df.to_csv(OUTPUT_FILE, index=False)
    current_index += 1
    show_next()


def skip():
    global current_index
    current_index += 1
    show_next()


def show_next():
    if current_index < len(df):
        descriptor = df.iloc[current_index]["feels like…"]
        descriptor_label.config(text=descriptor)

        sensory_var.set(False)
        affective_var.set(False)
        metaphorical_var.set(False)
        temporal_var.set(False)
        for var in subtype_vars.values():
            var.set(False)
    else:
        descriptor_label.config(text="✅ All descriptors tagged!")
        save_button.config(state="disabled")
        skip_button.config(state="disabled")


# GUI setup
root = tk.Tk()
root.title("Pain Descriptor Tagger v2")

frame = ttk.Frame(root, padding=20)
frame.grid(row=0, column=0)

descriptor_label = ttk.Label(
    frame, text="", wraplength=400, font=("Arial", 14))
descriptor_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

# Top-level categories
sensory_var = tk.BooleanVar()
affective_var = tk.BooleanVar()
metaphorical_var = tk.BooleanVar()
temporal_var = tk.BooleanVar()

ttk.Label(frame, text="Main Categories:", font=("Arial", 10, "bold")
          ).grid(row=1, column=0, sticky="w", pady=(0, 5))
ttk.Checkbutton(frame, text="Sensory", variable=sensory_var).grid(
    row=2, column=0, sticky="w")
ttk.Checkbutton(frame, text="Affective", variable=affective_var).grid(
    row=3, column=0, sticky="w")
ttk.Checkbutton(frame, text="Metaphorical", variable=metaphorical_var).grid(
    row=2, column=1, sticky="w")
ttk.Checkbutton(frame, text="Temporal", variable=temporal_var).grid(
    row=3, column=1, sticky="w")

# Metaphor subtypes
ttk.Label(frame, text="Metaphor Subtypes:", font=("Arial", 10, "bold")).grid(
    row=4, column=0, columnspan=2, pady=(10, 0), sticky="w")
subtype_vars = {}
for i, subtype in enumerate(METAPHOR_SUBTYPES):
    row = 5 + i // 2
    col = i % 2
    var = tk.BooleanVar()
    ttk.Checkbutton(frame, text=subtype.replace("_", " "),
                    variable=var).grid(row=row, column=col, sticky="w")
    subtype_vars[subtype] = var

# Save/skip buttons
save_button = ttk.Button(frame, text="Save & Next", command=save_and_next)
save_button.grid(row=row+1, column=0, pady=20)

skip_button = ttk.Button(frame, text="Skip", command=skip)
skip_button.grid(row=row+1, column=1, pady=20)

# Help text
help_text = (
    "Help:\n"
    "- Sensory: direct physical sensations (e.g. burning, stabbing)\n"
    "- Affective: emotional reactions (e.g. terrifying, unbearable)\n"
    "- Metaphorical: figurative comparisons (e.g. like a monster)\n"
    "- Temporal: references to time (e.g. constant, sudden)\n"
    "- Metaphor subtypes allow you to capture specific metaphor themes\n"
    "Note: Descriptors can be multi-layered — capturing both experiential "
    "(sensory/affective) and figurative (metaphorical/submetaphorical) dimensions."
)

help_label = ttk.Label(frame, text=help_text, wraplength=500,
                       font=("Arial", 9), foreground="gray")
help_label.grid(row=row+2, column=0, columnspan=2, pady=(0, 10))

show_next()
root.mainloop()
