
import pandas as pd
import tkinter as tk
from tkinter import ttk
import os

# Load descriptors
INPUT_FILE = "pain_descriptors_categorized_updated.csv"
OUTPUT_FILE = "pain_descriptors_tagged_manual.csv"

if os.path.exists(OUTPUT_FILE):
    df = pd.read_csv(OUTPUT_FILE)
else:
    df = pd.read_csv(INPUT_FILE)
    df["manual_category"] = ""

current_index = 0

def save_and_next():
    global current_index
    selected = []
    if sensory_var.get():
        selected.append("sensory")
    if affective_var.get():
        selected.append("affective")
    if metaphorical_var.get():
        selected.append("metaphorical")
    if temporal_var.get():
        selected.append("temporal")

    df.at[current_index, "manual_category"] = ", ".join(selected)
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
    else:
        descriptor_label.config(text="✅ All descriptors tagged!")
        save_button.config(state="disabled")
        skip_button.config(state="disabled")

# GUI setup
root = tk.Tk()
root.title("Pain Descriptor Tagger")

frame = ttk.Frame(root, padding=20)
frame.grid(row=0, column=0)

descriptor_label = ttk.Label(frame, text="", wraplength=400, font=("Arial", 14))
descriptor_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

sensory_var = tk.BooleanVar()
affective_var = tk.BooleanVar()
metaphorical_var = tk.BooleanVar()
temporal_var = tk.BooleanVar()

ttk.Checkbutton(frame, text="Sensory", variable=sensory_var).grid(row=1, column=0, sticky="w")
ttk.Checkbutton(frame, text="Affective", variable=affective_var).grid(row=2, column=0, sticky="w")
ttk.Checkbutton(frame, text="Metaphorical", variable=metaphorical_var).grid(row=1, column=1, sticky="w")
ttk.Checkbutton(frame, text="Temporal", variable=temporal_var).grid(row=2, column=1, sticky="w")

save_button = ttk.Button(frame, text="Save & Next", command=save_and_next)
save_button.grid(row=3, column=0, pady=20)

skip_button = ttk.Button(frame, text="Skip", command=skip)
skip_button.grid(row=3, column=1, pady=20)

show_next()
root.mainloop()
