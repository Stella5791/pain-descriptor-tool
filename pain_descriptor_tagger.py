
import pandas as pd
import tkinter as tk
from tkinter import ttk

# Load data
input_file = "pain_descriptors_categorized_updated.csv"
output_file = "pain_descriptors_tagged_manual.csv"
df = pd.read_csv(input_file)

# Work only with uncategorized
uncategorized = df[df['category'] == "uncategorized"].copy()
uncategorized['manual_category'] = ""

# Track current index
index = 0

def save_and_next():
    global index
    selected = []
    if var_sensory.get(): selected.append("sensory")
    if var_affective.get(): selected.append("affective")
    if var_metaphorical.get(): selected.append("metaphorical")
    if var_temporal.get(): selected.append("temporal")

    uncategorized.at[uncategorized.index[index], 'manual_category'] = ", ".join(selected)
    uncategorized.to_csv(output_file, index=False)

    index += 1
    if index < len(uncategorized):
        update_display()
    else:
        lbl_descriptor.config(text="All done!")
        btn_next.config(state="disabled")

def skip():
    global index
    index += 1
    if index < len(uncategorized):
        update_display()
    else:
        lbl_descriptor.config(text="All done!")
        btn_next.config(state="disabled")

def update_display():
    desc = uncategorized.iloc[index]['feels like…']
    lbl_descriptor.config(text=desc)
    var_sensory.set(False)
    var_affective.set(False)
    var_metaphorical.set(False)
    var_temporal.set(False)

# GUI setup
root = tk.Tk()
root.title("Pain Descriptor Tagger")
root.geometry("700x300")

lbl_descriptor = tk.Label(root, text="", wraplength=650, font=("Arial", 14), justify="left")
lbl_descriptor.pack(pady=20)

frame = tk.Frame(root)
frame.pack()

var_sensory = tk.BooleanVar()
var_affective = tk.BooleanVar()
var_metaphorical = tk.BooleanVar()
var_temporal = tk.BooleanVar()

chk1 = ttk.Checkbutton(frame, text="Sensory", variable=var_sensory)
chk2 = ttk.Checkbutton(frame, text="Affective", variable=var_affective)
chk3 = ttk.Checkbutton(frame, text="Metaphorical", variable=var_metaphorical)
chk4 = ttk.Checkbutton(frame, text="Temporal", variable=var_temporal)

chk1.grid(row=0, column=0, padx=10, pady=5)
chk2.grid(row=0, column=1, padx=10, pady=5)
chk3.grid(row=0, column=2, padx=10, pady=5)
chk4.grid(row=0, column=3, padx=10, pady=5)

btn_next = ttk.Button(root, text="Save & Next", command=save_and_next)
btn_next.pack(pady=10)

btn_skip = ttk.Button(root, text="Skip", command=skip)
btn_skip.pack()

update_display()
root.mainloop()
