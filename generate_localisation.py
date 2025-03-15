#!/usr/bin/env python3

import re
import os

def extract_template_strings(input_file):
    """Extract all unique strings starting with TEMPLATE from the input file."""
    template_strings = set()
    
    with open(input_file, 'r') as f:
        content = f.read()
        
        # Find all words starting with TEMPLATE
        pattern = r'\bTEMPLATE[A-Za-z0-9_]+\b'
        matches = re.findall(pattern, content)
        
        for match in matches:
            template_strings.add(match)
    
    return sorted(list(template_strings))

def generate_localisation(template_strings, output_file):
    """Generate localisation entries and write them to the output file."""
    with open(output_file, 'w') as f:
        # Write localisation file header
        f.write("l_english:\n\n")
        
        for template in template_strings:
            # If it follows the pattern TEMPLATE_LIST_X_Name_Y
            if "_Name_" in template:
                # Extract the ship type and number
                parts = template.split('_')
                if len(parts) >= 5 and parts[0] == "TEMPLATE" and parts[1] == "LIST":
                    ship_type = parts[2]
                    name_num = parts[4]
                    
                    # Remove underscore from number (01 -> 01)
                    display_name = f"{ship_type}_Name{name_num}"
                    
                    # Write the localisation entry
                    f.write(f'{template}:0 "{display_name}"\n')
            else:
                # Handle other TEMPLATE strings if needed
                f.write(f'{template}:0 "{template}"\n')

def main():
    input_file = "source_material/templates/template_name_list.txt"
    output_file = "source_material/templates/template_name_localisation.txt"
    
    print(f"Extracting template strings from {input_file}...")
    template_strings = extract_template_strings(input_file)
    print(f"Found {len(template_strings)} unique template strings.")
    
    print(f"Generating localisation entries in {output_file}...")
    generate_localisation(template_strings, output_file)
    print("Done!")

if __name__ == "__main__":
    main() 