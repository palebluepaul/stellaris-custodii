import json
import os

def update_placeholder_formats():
    # File paths
    source_file = "output/custodii_names_processed.json"
    target_file = "output/custodii_names.json"
    
    # Read both files
    with open(source_file, 'r') as f_source:
        source_data = json.load(f_source)
    
    with open(target_file, 'r') as f_target:
        target_data = json.load(f_target)
    
    # Counter for changes
    count_updates = 0
    
    # Iterate through top-level categories in source data
    for category in source_data:
        if category not in target_data:
            print(f"Warning: Category '{category}' not found in target file")
            continue
        
        # Iterate through subcategories
        for subcategory in source_data[category]:
            # Check if subcategory exists in target file
            if subcategory not in target_data[category]:
                print(f"Warning: Subcategory '{subcategory}' in '{category}' not found in target file")
                continue
            
            # Update placeholder_format if it exists in source
            if "placeholder_format" in source_data[category][subcategory]:
                target_data[category][subcategory]["placeholder_format"] = source_data[category][subcategory]["placeholder_format"]
                count_updates += 1
                
            # Update count if it exists in source
            if "count" in source_data[category][subcategory]:
                target_data[category][subcategory]["count"] = source_data[category][subcategory]["count"]
                count_updates += 1
    
    # Write the updated data back to the target file
    with open(target_file, 'w') as f_target:
        json.dump(target_data, f_target, indent=2)
    
    print(f"Update complete. {count_updates} values updated.")

if __name__ == "__main__":
    update_placeholder_formats()
    print("Script completed successfully!") 