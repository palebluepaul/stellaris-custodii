#!/usr/bin/env python3
import re
import json

def extract_max_count(name_list_content, category, subcategory):
    """Extract the highest number found in placeholder names like CUSTODII_CORVETTE_Name_40"""
    pattern = rf"CUSTODII_{subcategory.upper()}_Name_(\d+)"
    
    # Ship name patterns
    if category.lower() == "ship_names":
        if subcategory.lower() == "ship":
            pattern = r"CUSTODII_SHIP_Name_(\d+)"
        elif subcategory.lower() == "exploration":
            pattern = r"CUSTODII_EXPLORATION_Name_(\d+)"
    
    # Ship class patterns
    elif category.lower() == "ship_class_names":
        pattern = r"CUSTODII_SHIP_CLASS_Name_(\d+)"
    
    # Fleet name patterns
    elif category.lower() == "fleet_names":
        pattern = r"CUSTODII_FLEET_NAME_Name_(\d+)"
    
    # Army name patterns
    elif category.lower() == "army_names":
        # Most army names use sequential naming, so we default to 20
        return 20
    
    # For planetary names, the pattern is different
    elif category.lower() == "planet_names":
        # Adjust pattern for planet names which follow a different convention
        planetary_type = subcategory.split('_')[-1].upper()
        pattern = rf"CUSTODII_PLANET_NAME_{planetary_type}_(\d+)"
    
    # For character names, may use a different pattern
    elif category.lower() == "character_names":
        # Handle different character name types
        if "full_names" in subcategory:
            pattern = r"CUSTODII_CHARACTER_FULL_NAME_(\d+)"
        elif "first_names" in subcategory:
            pattern = r"CUSTODII_CHARACTER_FIRST_NAME_(\d+)"
        elif "second_names" in subcategory:
            pattern = r"CUSTODII_CHARACTER_SECOND_NAME_(\d+)"
        elif "regnal" in subcategory:
            pattern = r"CUSTODII_CHARACTER_REGNAL_NAME_(\d+)"
    
    matches = re.findall(pattern, name_list_content, re.IGNORECASE)
    if matches:
        return max(int(num) for num in matches)
    return 20  # Default to 20 if not found

def extract_description(tags_content, category, subcategory):
    """Extract description from tags file"""
    if category.lower() == "ship_names":
        pattern = rf"- {subcategory} \(CUSTODII > ship_names\): \"(.*?)\""
        match = re.search(pattern, tags_content)
        if match:
            return match.group(1)
    
    elif category.lower() == "ship_class_names":
        pattern = rf"- {subcategory} \(CUSTODII > ship_class_names\): \"(.*?)\""
        match = re.search(pattern, tags_content)
        if match:
            return match.group(1)
    
    elif category.lower() == "fleet_names":
        pattern = rf"- {subcategory} \(CUSTODII > fleet_names\): \"(.*?)\""
        match = re.search(pattern, tags_content)
        if match:
            return match.group(1)
    
    elif category.lower() == "army_names":
        pattern = rf"- {subcategory} \(CUSTODII > army_names\): \"(.*?)\""
        match = re.search(pattern, tags_content)
        if match:
            return match.group(1)
    
    elif category.lower() == "planet_names":
        # For planet names, we need to handle the pc_ prefix
        if subcategory.startswith("pc_"):
            pattern = rf"- names \(CUSTODII > planet_names > {subcategory}\): \"(.*?)\""
        else:
            pattern = rf"- names \(CUSTODII > planet_names > {subcategory}\): \"(.*?)\""
        
        match = re.search(pattern, tags_content)
        if match:
            return match.group(1)
        
        # Special handling for variations like pc_pd_cold_cave, etc.
        # Try to find the most similar planet type description
        planet_type_base = subcategory.split('_')[-1]
        pattern = rf"- names \(CUSTODII > planet_names > pc_[a-z_]*{planet_type_base}[a-z_]*\): \"(.*?)\""
        match = re.search(pattern, tags_content)
        if match:
            return match.group(1)
    
    elif category.lower() == "character_names":
        pattern = rf"- {subcategory} \(CUSTODII > character_names > default\): \"(.*?)\""
        match = re.search(pattern, tags_content)
        if match:
            return match.group(1)
    
    return ""

def get_placeholder_format(category, subcategory):
    """Generate the placeholder format"""
    if category.lower() == "ship_names":
        if subcategory.lower() == "explorationship":
            return "CUSTODII_EXPLORATION_Name_{:02d}"
        return f"CUSTODII_{subcategory.upper()}_Name_{{:02d}}"
    
    elif category.lower() == "ship_class_names":
        return "CUSTODII_SHIP_CLASS_Name_{:02d}"
    
    elif category.lower() == "fleet_names":
        return "CUSTODII_FLEET_NAME_Name_{:02d}"
    
    elif category.lower() == "army_names":
        return f"CUSTODII_{subcategory.upper()}_SEQ_{{:02d}}"
    
    elif category.lower() == "planet_names":
        # Extract just the type part of the planet name (after the last underscore)
        planet_type = subcategory.split('_')[-1].upper()
        return f"CUSTODII_PLANET_NAME_{planet_type}_{{:02d}}"
    
    elif category.lower() == "character_names":
        if "full_names" in subcategory:
            return "CUSTODII_CHARACTER_FULL_NAME_{:02d}"
        elif "first_names" in subcategory:
            return "CUSTODII_CHARACTER_FIRST_NAME_{:02d}"
        elif "second_names" in subcategory:
            return "CUSTODII_CHARACTER_SECOND_NAME_{:02d}"
        elif "regnal" in subcategory:
            return "CUSTODII_CHARACTER_REGNAL_NAME_{:02d}"
    
    return ""

def normalize_planet_id(planet_id):
    """Normalize planet ID to match the tags file."""
    # Handle special cases like ringworld_habitable
    if planet_id == "pc_ringworld":
        return "pc_ringworld_habitable"
    return planet_id

def extract_planet_types(name_list_content):
    """Extract all planet types from name list content"""
    # Extract all pc_ entries with names blocks
    planet_pattern = r"(pc_[a-zA-Z_]+)\s*=\s*{\s*names\s*="
    all_planets = re.findall(planet_pattern, name_list_content)
    
    # Also add generic 
    if "generic" not in all_planets:
        all_planets.append("generic")
    
    return all_planets

def get_character_name_types():
    """Return list of character name types from tags"""
    return [
        "full_names", "full_names_female", "full_names_male",
        "first_names", "first_names_female", "first_names_male",
        "second_names", "second_names_female", "second_names_male",
        "regnal_full_names", "regnal_full_names_female", "regnal_full_names_male",
        "regnal_first_names", "regnal_first_names_female", "regnal_first_names_male",
        "regnal_second_names", "regnal_second_names_female", "regnal_second_names_male"
    ]

def get_army_name_types(tags_content):
    """Extract army name types from tags content"""
    army_pattern = r"- ([a-zA-Z_]+) \(CUSTODII > army_names\): \"(.*?)\""
    matches = re.findall(army_pattern, tags_content)
    return [match[0] for match in matches]

def main():
    # Read input files
    try:
        with open("output/custodii_name_list.txt", "r") as f:
            name_list_content = f.read()
        with open("output/custodii_name_tags.md", "r") as f:
            tags_content = f.read()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    # Initialize data structure
    data = {
        "ship_names": {},
        "ship_class_names": {},
        "fleet_names": {},
        "army_names": {},
        "planet_names": {},
        "character_names": {}
    }

    # Process ship_names
    ship_types = [
        "generic", "corvette", "destroyer", "cruiser", "battleship", 
        "titan", "colossus", "juggernaut", "battlecruiser", "dreadnought",
        "flagship", "explorationship", "carrier", "science", "colonizer",
        "constructor", "transport", "large_ship_ai", "small_ship_ai"
    ]
    
    for ship_type in ship_types:
        count = extract_max_count(name_list_content, "ship_names", ship_type)
        desc = extract_description(tags_content, "ship_names", ship_type)
        placeholder = get_placeholder_format("ship_names", ship_type)
        
        if count > 0:
            data["ship_names"][ship_type] = {
                "description": desc,
                "count": count,
                "thematic_guidance": "",
                "placeholder_format": placeholder
            }

    # Process ship_class_names
    ship_class_types = ["generic"]
    
    for ship_class_type in ship_class_types:
        count = extract_max_count(name_list_content, "ship_class_names", ship_class_type)
        desc = extract_description(tags_content, "ship_class_names", ship_class_type)
        placeholder = get_placeholder_format("ship_class_names", ship_class_type)
        
        data["ship_class_names"][ship_class_type] = {
            "description": desc,
            "count": count,
            "thematic_guidance": "",
            "placeholder_format": placeholder
        }

    # Process fleet_names
    fleet_types = ["random_names"]
    
    for fleet_type in fleet_types:
        count = extract_max_count(name_list_content, "fleet_names", fleet_type)
        desc = extract_description(tags_content, "fleet_names", fleet_type)
        placeholder = get_placeholder_format("fleet_names", fleet_type)
        
        data["fleet_names"][fleet_type] = {
            "description": desc,
            "count": count,
            "thematic_guidance": "",
            "placeholder_format": placeholder
        }

    # Process army_names
    army_types = get_army_name_types(tags_content)
    
    for army_type in army_types:
        count = extract_max_count(name_list_content, "army_names", army_type)
        desc = extract_description(tags_content, "army_names", army_type)
        placeholder = get_placeholder_format("army_names", army_type)
        
        data["army_names"][army_type] = {
            "description": desc,
            "count": count,
            "thematic_guidance": "",
            "placeholder_format": placeholder
        }

    # Extract all planet types
    planet_types = extract_planet_types(name_list_content)
    
    # Process planet_names
    for planet_type in planet_types:
        if planet_type == "generic":
            count = extract_max_count(name_list_content, "planet_names", "generic")
            planet_id = "generic"
        else:
            # Extract the planet identifier
            planet_id = normalize_planet_id(planet_type)
            count = extract_max_count(name_list_content, "planet_names", planet_type)
        
        desc = extract_description(tags_content, "planet_names", planet_id)
        placeholder = get_placeholder_format("planet_names", planet_type)
        
        # Some special cases for known planet types that might be missing
        special_planet_types = {
            "pc_pd_cold_cave": "Names for frigid subterranean cave worlds with icy environments",
            "pc_pd_dry_cave": "Names for arid underground cave systems with minimal moisture",
            "pc_pd_wet_cave": "Names for humid subterranean worlds with abundant water features",
            "pc_pd_superhabitable": "Names for exceptionally habitable worlds",
            "pc_pd_tidally_locked": "Names for planets with one side always facing their star",
            "pc_pd_cave": "Names for worlds with extensive cave systems"
        }
        
        if desc == "" and planet_id in special_planet_types:
            desc = special_planet_types[planet_id]
            
        data["planet_names"][planet_id] = {
            "description": desc,
            "count": count if count > 0 else 20,
            "thematic_guidance": "",
            "placeholder_format": placeholder
        }

    # Process character names
    character_name_types = get_character_name_types()
    
    for char_type in character_name_types:
        count = 20  # Most character name lists have around 20 options
        desc = extract_description(tags_content, "character_names", char_type)
        placeholder = get_placeholder_format("character_names", char_type)
        
        data["character_names"][char_type] = {
            "description": desc,
            "count": count,
            "thematic_guidance": "",
            "placeholder_format": placeholder
        }

    # Save to JSON file
    with open("output/custodii_names.json", "w") as f:
        json.dump(data, f, indent=2)
    
    print("Conversion complete! Data saved to output/custodii_names.json")
    
    # Count the entries in each category
    ship_count = len(data["ship_names"])
    ship_class_count = len(data["ship_class_names"])
    fleet_count = len(data["fleet_names"])
    army_count = len(data["army_names"])
    planet_count = len(data["planet_names"])
    char_count = len(data["character_names"])
    
    print(f"\nStatistics:")
    print(f"- Ship types: {ship_count}")
    print(f"- Ship class types: {ship_class_count}")
    print(f"- Fleet types: {fleet_count}")
    print(f"- Army types: {army_count}")
    print(f"- Planet types: {planet_count}")
    print(f"- Character name types: {char_count}")
    
    # Print a sample of the output
    print("\nSample of the JSON structure:")
    sample = {}
    
    # Include one sample from each category
    if "corvette" in data["ship_names"]:
        sample["ship_names"] = {"corvette": data["ship_names"]["corvette"]}
    
    if "generic" in data["ship_class_names"]:
        sample["ship_class_names"] = {"generic": data["ship_class_names"]["generic"]}
    
    if "random_names" in data["fleet_names"]:
        sample["fleet_names"] = {"random_names": data["fleet_names"]["random_names"]}
    
    if army_types and army_types[0] in data["army_names"]:
        sample["army_names"] = {army_types[0]: data["army_names"][army_types[0]]}
    
    if "pc_pd_cold_cave" in data["planet_names"]:
        sample["planet_names"] = {"pc_pd_cold_cave": data["planet_names"]["pc_pd_cold_cave"]}
    
    if "full_names" in data["character_names"]:
        sample["character_names"] = {"full_names": data["character_names"]["full_names"]}
    
    print(json.dumps(sample, indent=2))

if __name__ == "__main__":
    main() 