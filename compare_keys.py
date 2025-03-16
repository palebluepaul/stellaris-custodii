#!/usr/bin/env python3

import re
import sys
from pathlib import Path

def extract_keys_from_name_list(file_path):
    """Extract all the keys referenced in the name list file."""
    keys = set()
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        # Find all strings that look like CUSTODII_SOMETHING
        matches = re.findall(r'CUSTODII_[A-Z_0-9]+', content)
        for match in matches:
            keys.add(match.upper())  # Convert to uppercase for case-insensitive comparison
    return keys

def extract_keys_from_localization(file_path):
    """Extract all defined keys from the localization file."""
    keys = set()
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Skip empty lines or ones that don't have a key
            if not line.strip() or ":" not in line:
                continue
                
            # Extract the key (everything before the first colon)
            key = line.split(':', 1)[0].strip()
            # Only add CUSTODII keys
            if key.startswith("CUSTODII_"):
                keys.add(key.upper())  # Convert to uppercase for case-insensitive comparison
    return keys

def main():
    name_list_path = Path("mod/common/name_lists/custodii_name_list.txt")
    localization_path = Path("mod/localisation/english/custodii_name_localisation_l_english.yml")
    
    # Check if files exist
    if not name_list_path.exists():
        print(f"Error: Name list file not found at {name_list_path}")
        sys.exit(1)
    
    if not localization_path.exists():
        print(f"Error: Localization file not found at {localization_path}")
        sys.exit(1)
    
    # Extract keys from both files
    name_list_keys = extract_keys_from_name_list(name_list_path)
    localization_keys = extract_keys_from_localization(localization_path)
    
    # Find keys that are in the name list but not in the localization
    missing_keys = name_list_keys - localization_keys
    
    if missing_keys:
        print(f"Found {len(missing_keys)} keys that are in the name list but missing from the localization:")
        for key in sorted(missing_keys):
            print(f"  {key}")
    else:
        print("All keys from the name list are present in the localization file.")
    
    # Optionally, find keys that are in localization but not used in name list
    unused_keys = localization_keys - name_list_keys
    if unused_keys:
        print(f"\nFound {len(unused_keys)} keys that are in the localization but not used in the name list:")
        for key in sorted(unused_keys):
            print(f"  {key}")
            
    # Check for case-sensitivity issues
    name_list_keys_lower = {k.lower() for k in name_list_keys}
    localization_keys_lower = {k.lower() for k in localization_keys}
    
    case_sensitivity_issues = name_list_keys_lower & localization_keys_lower
    if len(case_sensitivity_issues) > 0:
        print(f"\nFound {len(case_sensitivity_issues)} keys that match when ignoring case:")
        # Find some examples to show
        count = 0
        for lower_key in sorted(list(case_sensitivity_issues))[:10]:  # Show first 10 examples
            name_list_version = [k for k in name_list_keys if k.lower() == lower_key]
            loc_version = [k for k in localization_keys if k.lower() == lower_key]
            if name_list_version and loc_version and name_list_version[0] != loc_version[0]:
                print(f"  Name list: {name_list_version[0]}")
                print(f"  Localization: {loc_version[0]}")
                print("")
                count += 1
                if count >= 5:  # Limit to 5 examples
                    break
        
        if count > 0:
            print(f"The issue appears to be case sensitivity in the key names.")
            print(f"Consider either updating the name list to match the localization case or vice versa.")

if __name__ == "__main__":
    main() 