import json
import re
import os

def main():
    # Read the JSON file
    with open('output/custodii_names_processed.json', 'r', encoding='utf-8') as f:
        name_data = json.load(f)
    
    # Read the localization file
    with open('output/custodii_name_localisation.txt', 'r', encoding='utf-8') as f:
        loc_content = f.read()
    
    # Track which entries were found and updated
    updated_entries = set()
    all_loc_entries = set()
    
    # Create a mapping between placeholder formats and values
    placeholder_to_value = {}
    
    # Print debug info
    print("Processing JSON data...")
    
    # Recursively process name data to handle nested structures
    def process_name_data(data, prefix=""):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict) and 'placeholder_format' in value and 'values' in value:
                    # This is a name entry
                    if 'SEQ' in value['placeholder_format']:
                        # Handle SEQ entries
                        base_key = value['placeholder_format'].split('_{')[0]
                        
                        if value['values']:
                            val = value['values'][0]
                            placeholder_to_value[base_key] = val
                            print(f"SEQ mapping: {base_key} -> {val}")
                    else:
                        # Handle regular numbered entries
                        format_pattern = value['placeholder_format'].replace('{:02d}', '')
                        
                        for i, val in enumerate(value['values'], 1):
                            key = f"{format_pattern}{i:02d}"
                            placeholder_to_value[key] = val
                            print(f"Regular mapping: {key} -> {val}")
                else:
                    # Recursively process nested structures
                    new_prefix = f"{prefix}.{key}" if prefix else key
                    process_name_data(value, new_prefix)
    
    # Process the JSON data
    process_name_data(name_data)
    
    # Extract all localization keys
    print("\nFinding localization keys...")
    loc_keys = re.findall(r'(CUSTODII_[A-Za-z0-9_]+):0 "[^"]+"', loc_content)
    all_loc_entries.update(loc_keys)
    
    print(f"Found {len(loc_keys)} localization keys")
    print(f"Found {len(placeholder_to_value)} placeholder mappings")
    
    # Print some examples of both
    print("\nExample localization keys:")
    for key in list(loc_keys)[:5]:
        print(f"  - {key}")
    
    print("\nExample placeholder mappings:")
    keys_list = list(placeholder_to_value.keys())[:5]
    for key in keys_list:
        print(f"  - {key} -> {placeholder_to_value[key]}")
    
    # Update the localization file
    print("\nUpdating localization entries...")
    update_count = 0
    
    for key in loc_keys:
        if key in placeholder_to_value:
            # Replace the placeholder with the actual value
            pattern = f'{key}:0 "[^"]+"'
            replacement = f'{key}:0 "{placeholder_to_value[key]}"'
            
            # Debug specific keys
            if key == "CUSTODII_UNDEAD_ARMY_SEQ":
                print(f"Updating {key} -> {placeholder_to_value[key]}")
                print(f"Pattern: {pattern}")
                print(f"Replacement: {replacement}")
            
            new_content = re.sub(pattern, replacement, loc_content)
            
            # Check if replacement worked
            if new_content != loc_content:
                loc_content = new_content
                updated_entries.add(key)
                update_count += 1
                if update_count % 100 == 0:
                    print(f"Updated {update_count} entries so far...")
    
    # Write the updated content directly to the original file
    with open('output/custodii_name_localisation.txt', 'w', encoding='utf-8') as f:
        f.write(loc_content)
    
    # Report entries that weren't found in the JSON
    not_found = all_loc_entries - updated_entries
    if not_found:
        print(f"\nWARNING: {len(not_found)} entries in the localization file were not found in the JSON:")
        # Print first 20 unfound entries as examples
        for entry in sorted(list(not_found)[:20]):
            print(f"  - {entry}")
        if len(not_found) > 20:
            print(f"  ... and {len(not_found) - 20} more")
    
    print(f"\nSuccessfully updated {len(updated_entries)} entries in the localization file.")
    print(f"Localization file has been updated directly.")

if __name__ == "__main__":
    main() 