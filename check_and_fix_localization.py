#!/usr/bin/env python3

import json
import re
import os

# Define file paths
json_file_path = "output/working/custodii_names_processed.json"
yml_file_path = "output/working/custodii_name_localisation_l_english.yml"

# Function to read and parse the JSON file
def parse_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# Function to read the YML file
def read_yml_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

# Function to extract placeholders from the JSON data
def extract_placeholders_from_json(json_data):
    placeholders = {}
    
    # Process ship names
    for ship_type, ship_data in json_data.get("ship_names", {}).items():
        placeholder_format = ship_data.get("placeholder_format", "")
        values = ship_data.get("values", [])
        
        for i, value in enumerate(values):
            placeholder = placeholder_format.format(i + 1)
            placeholders[placeholder] = value
    
    # Process leader names sections if they exist
    for leader_type in ["ruler_names", "leader_names", "character_names"]:
        if leader_type in json_data:
            for gender, gender_data in json_data[leader_type].items():
                placeholder_format = gender_data.get("placeholder_format", "")
                values = gender_data.get("values", [])
                
                for i, value in enumerate(values):
                    placeholder = placeholder_format.format(i + 1)
                    placeholders[placeholder] = value
    
    # Process any other sections with placeholders
    for section_name, section_data in json_data.items():
        if section_name not in ["ship_names", "ruler_names", "leader_names", "character_names"]:
            if isinstance(section_data, dict) and "placeholder_format" in section_data:
                placeholder_format = section_data.get("placeholder_format", "")
                values = section_data.get("values", [])
                
                for i, value in enumerate(values):
                    placeholder = placeholder_format.format(i + 1)
                    placeholders[placeholder] = value
    
    return placeholders

# Function to extract existing placeholders from the YML content
def extract_existing_placeholders_from_yml(yml_content):
    # Pattern to match placeholders: KEY:0 "Value"
    pattern = r'([A-Z0-9_]+):0\s+"([^"]+)"'
    matches = re.findall(pattern, yml_content)
    
    existing_placeholders = {key: value for key, value in matches}
    return existing_placeholders

# Function to find missing placeholders
def find_missing_placeholders(json_placeholders, yml_placeholders):
    missing = {}
    for key, value in json_placeholders.items():
        if key not in yml_placeholders:
            missing[key] = value
    return missing

# Function to append missing placeholders to the YML file
def append_missing_placeholders_to_yml(yml_file_path, missing_placeholders):
    with open(yml_file_path, 'a', encoding='utf-8') as f:
        f.write("\n# Generated missing entries\n")
        for key, value in missing_placeholders.items():
            f.write(f'{key}:0 "{value}"\n')

# Main function
def main():
    print("Checking for missing localizations...")
    
    # Parse the JSON file
    json_data = parse_json_file(json_file_path)
    
    # Extract placeholders from JSON
    json_placeholders = extract_placeholders_from_json(json_data)
    print(f"Found {len(json_placeholders)} placeholders in JSON file")
    
    # Read the YML file
    yml_content = read_yml_file(yml_file_path)
    
    # Extract existing placeholders from YML
    yml_placeholders = extract_existing_placeholders_from_yml(yml_content)
    print(f"Found {len(yml_placeholders)} placeholders in YML file")
    
    # Find missing placeholders
    missing_placeholders = find_missing_placeholders(json_placeholders, yml_placeholders)
    print(f"Found {len(missing_placeholders)} missing placeholders")
    
    if missing_placeholders:
        print("Missing placeholders:")
        for key, value in missing_placeholders.items():
            print(f"  {key}: {value}")
        
        # Create backup of the original YML file
        backup_path = yml_file_path + ".backup"
        if not os.path.exists(backup_path):
            with open(yml_file_path, 'r', encoding='utf-8') as src, open(backup_path, 'w', encoding='utf-8') as dst:
                dst.write(src.read())
            print(f"Created backup at {backup_path}")
        
        # Append missing placeholders to the YML file
        append_missing_placeholders_to_yml(yml_file_path, missing_placeholders)
        print(f"Added {len(missing_placeholders)} missing entries to {yml_file_path}")
    else:
        print("No missing placeholders found. All entries are properly localized.")

if __name__ == "__main__":
    main() 