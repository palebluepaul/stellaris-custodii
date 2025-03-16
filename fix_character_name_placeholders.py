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
    
    # Define the correct placeholder formats based on the image
    correct_formats = {
        "full_names": "CUSTODII_FULL_NAME_{:02d}",
        "full_names_female": "CUSTODII_FULL_NAME_FEMALE_{:02d}",
        "full_names_male": "CUSTODII_FULL_NAME_MALE_{:02d}",
        "first_names": "CUSTODII_FIRST_NAME_{:02d}",
        "first_names_female": "CUSTODII_FIRST_NAME_FEMALE_{:02d}",
        "first_names_male": "CUSTODII_FIRST_NAME_MALE_{:02d}",
        "second_names": "CUSTODII_SECOND_NAME_{:02d}",
        "second_names_female": "CUSTODII_SECOND_NAME_FEMALE_{:02d}",
        "second_names_male": "CUSTODII_SECOND_NAME_MALE_{:02d}",
        "regnal_full_names": "CUSTODII_REGNAL_FULL_NAME_{:02d}",
        "regnal_full_names_female": "CUSTODII_REGNAL_FULL_NAME_FEMALE_{:02d}",
        "regnal_full_names_male": "CUSTODII_REGNAL_FULL_NAME_MALE_{:02d}",
        "regnal_first_names": "CUSTODII_REGNAL_FIRST_NAME_{:02d}",
        "regnal_first_names_female": "CUSTODII_REGNAL_FIRST_NAME_FEMALE_{:02d}",
        "regnal_first_names_male": "CUSTODII_REGNAL_FIRST_NAME_MALE_{:02d}",
        "regnal_second_names": "CUSTODII_REGNAL_SECOND_NAME_{:02d}",
        "regnal_second_names_female": "CUSTODII_REGNAL_SECOND_NAME_FEMALE_{:02d}",
        "regnal_second_names_male": "CUSTODII_REGNAL_SECOND_NAME_MALE_{:02d}"
    }
    
    # Check if character_names exists in the data
    if "character_names" in data:
        char_names = data["character_names"]
        
        # Process each section in character_names
        for section, format_str in correct_formats.items():
            if section in char_names and "placeholder_format" in char_names[section]:
                current_format = char_names[section]["placeholder_format"]
                
                # Check if the format needs updating
                if current_format != format_str:
                    print(f"Fixing: character_names.{section}")
                    print(f"  Old: {current_format}")
                    print(f"  New: {format_str}")
                    char_names[section]["placeholder_format"] = format_str
                    changes_made += 1
                else:
                    already_correct += 1
    else:
        print("Warning: 'character_names' section not found in the JSON file")
    
    # Save the updated JSON
    print(f"\nSaving updated JSON file...")
    with open('output/custodii_names_character_fixed.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    print(f"\nSummary:")
    print(f"- Fixed character name placeholders: {changes_made}")
    print(f"- Already correct: {already_correct}")
    print(f"Updated file saved as 'output/custodii_names_character_fixed.json'")
    
    if changes_made > 0:
        print("\nYou may want to run the update_localisation.py script again with the fixed JSON file.")

if __name__ == "__main__":
    main() 