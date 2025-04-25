import pandas as pd
import subprocess
import datetime


# Ask the user for a new pain descriptor
new_descriptor = input(
    'Take a moment. How would you describe your pain? For example: "It feels like a tight band squeezing my chest." '
).strip()

#  Load the current input CSV
df = pd.read_csv("pain_tags_input.csv")

# Append the new descriptor to the DataFrame
df.loc[len(df)] = [new_descriptor]

# Save the updated file
df.to_csv("pain_tags_input.csv", index=False)

# Create a timestamped backup
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
backup_filename = f"pain_tags_input_backup_{timestamp}.csv"
df.to_csv(backup_filename, index=False)
print(f"🗂️ Backup created: {backup_filename}")


# Run the pain_descriptor_auto_tagger.py script
print("🔄 Running the pain descriptor auto-tagger...")
subprocess.run(["python", "pain_descriptor_auto_tagger.py"], check=True)

# print("The pain descriptor auto tagger has been run. Please check the output. in the pain_tags_output.csv file.")
print("✅ Auto-tagging complete! Please check the updated pain_tags_clean.csv file.")
