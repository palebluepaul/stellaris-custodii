#!/usr/bin/env python3
import os
import re
from pathlib import Path

# Path to the Stellaris workshop folder
workshop_path = os.path.expanduser("~/Library/Application Support/Steam/steamapps/workshop/content/281990")
output_file = "starbase_strings.txt"

# Regular expression to find strings starting with "starbase_"
pattern = re.compile(r'starbase_\w+')

# Set to store unique matches
unique_matches = set()

# Counter for files processed
files_processed = 0

print(f"Searching in: {workshop_path}")
print("This may take a while depending on the number of mods installed...")

# Walk through all files in the workshop directory
for root, dirs, files in os.walk(workshop_path):
    for file in files:
        file_path = os.path.join(root, file)
        files_processed += 1
        
        if files_processed % 1000 == 0:
            print(f"Processed {files_processed} files, found {len(unique_matches)} unique matches so far...")
        
        try:
            # Try to open the file as text
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Find all matches in the file
                matches = pattern.findall(content)
                
                # Add matches to the set of unique matches
                if matches:
                    unique_matches.update(matches)
        except Exception as e:
            # Skip files that can't be read as text
            continue

# Sort the unique matches
sorted_matches = sorted(unique_matches)

# Write the results to a file
with open(output_file, 'w', encoding='utf-8') as f:
    for match in sorted_matches:
        f.write(f"{match}\n")

print(f"\nSearch complete!")
print(f"Processed {files_processed} files")
print(f"Found {len(unique_matches)} unique strings starting with 'starbase_'")
print(f"Results written to: {output_file}")
