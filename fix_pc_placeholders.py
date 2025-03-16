import json
import re

def main():
    # Load the JSON file
    print("Loading JSON file...")
    with open('output/custodii_names.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Track changes for reporting
    changes_made = 0
    already_correct = 0
    
    # Find and fix planet class entries recursively
    def process_pc_entries(data_dict, path=""):
        nonlocal changes_made, already_correct
        
        if not isinstance(data_dict, dict):
            return
        
        for key, value in list(data_dict.items()):
            current_path = f"{path}.{key}" if path else key
            
            # If this is a planet class entry
            if key.startswith("pc_"):
                if isinstance(value, dict) and 'placeholder_format' in value:
                    # Determine what the correct placeholder should be
                    if key.startswith("pc_pd_"):
                        # Remove pc_pd_ prefix and convert to uppercase
                        name_part = key[6:].upper()
                    else:
                        # Remove pc_ prefix and convert to uppercase
                        name_part = key[3:].upper()
                    
                    correct_placeholder = f"CUSTODII_PLANET_NAME_{name_part}_{{:02d}}"
                    
                    # Check if the placeholder needs to be updated
                    if value['placeholder_format'] != correct_placeholder:
                        print(f"Fixing: {key}")
                        print(f"  Old: {value['placeholder_format']}")
                        print(f"  New: {correct_placeholder}")
                        value['placeholder_format'] = correct_placeholder
                        changes_made += 1
                    else:
                        already_correct += 1
            
            # Recursively process nested dictionaries
            if isinstance(value, dict):
                process_pc_entries(value, current_path)
    
    # Process the data
    print("Processing planet class entries...")
    process_pc_entries(data)
    
    # Save the updated JSON
    print(f"\nSaving updated JSON file...")
    with open('output/custodii_names_processed_fixed.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    print(f"\nSummary:")
    print(f"- Fixed placeholders: {changes_made}")
    print(f"- Already correct: {already_correct}")
    print(f"Updated file saved as 'output/custodii_names_processed_fixed.json'")
    
    if changes_made > 0:
        print("\nYou may want to run the update_localisation.py script again with the fixed JSON file.")

if __name__ == "__main__":
    main() 