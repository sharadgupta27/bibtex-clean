"""
@author: Sharad Kumar Gupta, Vanshika Gupta
"""

import re
import tkinter as tk
from tkinter import filedialog

# Set up Tkinter root (hidden)
root = tk.Tk()
root.withdraw()

# Ask user for input BibTeX file
input_file = filedialog.askopenfilename(
    title="Select BibTeX File",
    filetypes=[("BibTeX Files", "*.bib")]
)
if not input_file:
    print("No file selected. Exiting.")
    exit()

# Ask user where to save the cleaned BibTeX file
output_file = filedialog.asksaveasfilename(
    title="Save Cleaned BibTeX File As",
    defaultextension=".bib",
    filetypes=[("BibTeX Files", "*.bib")],
    initialfile=input_file.rsplit('/', 1)[-1].replace(".bib", "_Cleaned.bib")
)
if not output_file:
    print("No output file specified. Exiting.")
    exit()

# Define fields to remove
fields_to_remove = [
    "abstract", "file", "archivePrefix", "keywords", "eprint", "mendeley-groups",
    "link", "keyword", "mendeley-tags", "annote", "pmid", "chapter", "institution", "month"
]

# Function to clean unnecessary fields from the BibTeX content
def cleanBibtexFile(content):
    cleaned_content = []
    current_entry = []
    in_entry = False
    has_journal = False

    for line in content:
        if line.strip().startswith('@'):
            if in_entry:
                cleaned_content.extend(process_entry(current_entry, has_journal))
                cleaned_content.append('\n')  # Add a blank line between entries
            current_entry = [line]
            in_entry = True
            has_journal = False
        elif in_entry:
            if line.strip().startswith('journal ='):
                has_journal = True
            current_entry.append(line)
        else:
            cleaned_content.append(line)

    if in_entry:
        cleaned_content.extend(process_entry(current_entry, has_journal))
        cleaned_content.append('\n')  # Add a blank line after the last entry

    return cleaned_content

def process_entry(entry, has_journal):
    processed_entry = []
    for line in entry:
        if any(line.strip().startswith(field + ' =') for field in fields_to_remove):
            continue
        if has_journal and line.strip().startswith('url ='):
            continue
        processed_entry.append(line)
    return processed_entry

# Read the content of the BibTeX file
with open(input_file, 'r', encoding='utf-8') as file:
    bibtex_content = file.readlines()

# Clean the content
cleaned_bibtex = cleanBibtexFile(bibtex_content)

# Write the cleaned content to a new file
with open(output_file, 'w', encoding='utf-8') as file:
    file.writelines(cleaned_bibtex)

print(f"Cleaned BibTeX file created: {output_file}")