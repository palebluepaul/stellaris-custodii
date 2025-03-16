#!/usr/bin/env python3
"""
generate_names_with_claude.py

A script to generate names for the Stellaris Custodii mod using Claude 3.7 Sonnet.
This script processes the custodii_names.json file, identifies placeholder tags,
and replaces them with AI-generated names that match the thematic guidance.

Usage:
    doppler run -- python generate_names_with_claude.py [--category CATEGORY] [--entry ENTRY]

Options:
    --category: Process only a specific category (e.g., "ship_names", "character_names")
    --entry: Process only a specific entry within a category (e.g., "corvette", "regnal_full_names")
"""

import os
import json
import argparse
import time
import sys
from pathlib import Path
from anthropic import Anthropic
from typing import Dict, List, Optional, Tuple, Any

# Constants
CLAUDE_MODEL = "claude-3-7-sonnet-20250219"
OUTPUT_BATCH_SIZE = 20  # How many names to request in a single API call
PROJECT_ROOT = Path(__file__).parent.parent
INPUT_JSON_PATH = PROJECT_ROOT / "output" / "custodii_names.json"
OUTPUT_JSON_PATH = PROJECT_ROOT / "output" / "custodii_names_processed.json"
BRIEFING_PATH = PROJECT_ROOT / "source_material" / "custodii_briefing.md"


def load_json_file(file_path: Path) -> Dict:
    """Load JSON data from the specified file path."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON file {file_path}: {e}")
        sys.exit(1)


def save_json_file(data: Dict, file_path: Path) -> None:
    """Save JSON data to the specified file path with pretty formatting."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Successfully saved JSON to {file_path}")
    except Exception as e:
        print(f"Error saving JSON file {file_path}: {e}")
        sys.exit(1)


def load_custodii_briefing() -> str:
    """Load the Custodii briefing document."""
    try:
        with open(BRIEFING_PATH, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error loading Custodii briefing from {BRIEFING_PATH}: {e}")
        sys.exit(1)


def is_placeholder(value: str) -> bool:
    """Check if a given string is a placeholder in the format CUSTODII_*_XX."""
    return value.startswith("CUSTODII_") and "_" in value


def identify_unprocessed_entries(data: Dict) -> List[Tuple[List[str], Dict, str]]:
    """
    Identify entries that still contain placeholder values.
    Returns a list of tuples with (path to entry, entry dict, placeholder format)
    """
    unprocessed = []
    
    def explore_dict(current_dict, current_path):
        for key, value in current_dict.items():
            new_path = current_path + [key]
            
            if isinstance(value, dict):
                if "placeholder_format" in value:
                    # This is an entry we need to process
                    has_unprocessed = False
                    if "values" in value:
                        # Check if there are any placeholders in the values
                        for name in value["values"]:
                            if is_placeholder(name):
                                has_unprocessed = True
                                break
                    else:
                        # No values yet, so it's definitely unprocessed
                        has_unprocessed = True
                    
                    if has_unprocessed:
                        unprocessed.append((new_path, value, value.get("placeholder_format")))
                else:
                    # Continue exploring deeper
                    explore_dict(value, new_path)
    
    explore_dict(data, [])
    return unprocessed


def generate_names_with_claude(
    entry: Dict, 
    placeholder_format: str, 
    briefing: str,
    anthropic_client: Anthropic
) -> List[str]:
    """
    Generate names using Claude 3.7 Sonnet based on the thematic guidance.
    
    Args:
        entry: The dictionary containing entry metadata (description, thematic_guidance, etc.)
        placeholder_format: The format string for placeholders
        briefing: The Custodii briefing text to provide context
        anthropic_client: The initialized Anthropic client
        
    Returns:
        A list of generated names
    """
    # Extract information from the entry
    description = entry.get("description", "No description available")
    thematic_guidance = entry.get("thematic_guidance", "No thematic guidance available")
    count = entry.get("count", 20)
    
    # Check if we have any existing values
    existing_values = []
    if "values" in entry and isinstance(entry["values"], list):
        existing_values = [v for v in entry["values"] if not is_placeholder(v)]
    
    # Calculate how many more names we need
    names_needed = count - len(existing_values)
    
    if names_needed <= 0:
        print("All names already generated for this entry.")
        return existing_values
    
    # Build the prompt for Claude
    prompt = f"""You are helping to generate names for a Stellaris mod for a synthetic guardian race called the Custodii.

CONTEXT:
{briefing[:4000]}  # Limit briefing to first 4000 chars to keep prompt size reasonable

TASK: 
Generate {names_needed} unique names for the following category:
- Description: {description}
- Thematic Guidance: {thematic_guidance}

INSTRUCTIONS:
1. Each name should be unique and follow the thematic guidance provided
2. Respond ONLY with a valid JSON array of strings (no explanations or other text)
3. Do not include placeholder names in your response (e.g., {placeholder_format.format(1)})
4. Generate exactly {names_needed} names in this format:
["Name 1", "Name 2", "Name 3", ...]

Existing names (do not repeat these):
{', '.join(existing_values) if existing_values else 'None yet.'}
"""

    try:
        # Call Claude API with batching to avoid overly long responses
        all_generated_names = []
        
        # Split requests into batches if needed
        batches_needed = (names_needed + OUTPUT_BATCH_SIZE - 1) // OUTPUT_BATCH_SIZE
        
        for batch in range(batches_needed):
            names_in_batch = min(OUTPUT_BATCH_SIZE, names_needed - len(all_generated_names))
            
            batch_prompt = prompt.replace(f"Generate {names_needed} unique names", 
                                         f"Generate {names_in_batch} unique names")
            
            if all_generated_names:
                existing_with_gen = existing_values + all_generated_names
                batch_prompt = batch_prompt.replace(
                    f"Existing names (do not repeat these):\n{', '.join(existing_values) if existing_values else 'None yet.'}",
                    f"Existing names (do not repeat these):\n{', '.join(existing_with_gen)}"
                )
            
            print(f"Requesting batch {batch+1}/{batches_needed} ({names_in_batch} names)...")
            
            response = anthropic_client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=4000,
                temperature=0.8,
                system="You are an expert naming consultant helping to create names for a science fiction video game. Your responses should be only valid JSON arrays with no additional text.",
                messages=[
                    {"role": "user", "content": batch_prompt}
                ]
            )
            
            content = response.content[0].text
            
            # Extract the JSON array
            try:
                # Try to extract JSON if it's not already a clean JSON
                if not content.strip().startswith("["):
                    import re
                    json_match = re.search(r'\[.*\]', content, re.DOTALL)
                    if json_match:
                        content = json_match.group(0)
                
                batch_names = json.loads(content)
                
                # Validate the response
                if not isinstance(batch_names, list):
                    raise ValueError("API didn't return a list")
                
                all_generated_names.extend(batch_names)
                print(f"Successfully generated {len(batch_names)} names in this batch.")
                
                # Pause briefly between batches
                if batch < batches_needed - 1:
                    time.sleep(2)
                    
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON response: {e}")
                print(f"Raw response: {content}")
                continue
        
        # Validate we got the right number of names
        if len(all_generated_names) < names_needed:
            print(f"Warning: Only generated {len(all_generated_names)} names out of {names_needed} needed.")
        
        # If we accidentally got too many, trim the list
        if len(all_generated_names) > names_needed:
            all_generated_names = all_generated_names[:names_needed]
        
        # Combine with existing values
        final_names = existing_values + all_generated_names
        
        return final_names
        
    except Exception as e:
        print(f"Error calling Claude API: {e}")
        return existing_values  # Return existing values in case of error


def update_entry_with_names(data: Dict, path: List[str], names: List[str]) -> Dict:
    """Update the data dictionary with generated names at the specified path."""
    current = data
    
    # Navigate to the correct position in the nested dictionary
    for i, key in enumerate(path[:-1]):
        if key not in current:
            current[key] = {}
        current = current[key]
    
    # Set the values
    if "values" not in current[path[-1]]:
        current[path[-1]]["values"] = []
    
    current[path[-1]]["values"] = names
    
    return data


def main():
    """Main function to process the name generation."""
    parser = argparse.ArgumentParser(description="Generate names using Claude 3.7 Sonnet")
    parser.add_argument("--category", help="Process only a specific category (e.g., 'ship_names')")
    parser.add_argument("--entry", help="Process only a specific entry (e.g., 'corvette')")
    parser.add_argument("--batch-size", type=int, default=3, help="Number of entries to process in a single run")
    args = parser.parse_args()
    
    # Check for API key
    anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not anthropic_api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not found.")
        print("Run with: doppler run -- python generate_names_with_claude.py")
        sys.exit(1)
    
    # Initialize the Anthropic client
    anthropic_client = Anthropic(api_key=anthropic_api_key)
    
    # Load the input JSON and briefing
    data = load_json_file(INPUT_JSON_PATH)
    briefing = load_custodii_briefing()
    
    # Make a copy of the data for processing
    processed_data = data.copy()
    
    # Identify entries to process
    unprocessed_entries = identify_unprocessed_entries(data)
    
    # Filter by category and entry if specified
    if args.category:
        unprocessed_entries = [e for e in unprocessed_entries if args.category in e[0]]
    
    if args.entry:
        unprocessed_entries = [e for e in unprocessed_entries if args.entry in e[0]]
    
    # Check if we have any entries to process
    if not unprocessed_entries:
        print("No unprocessed entries found matching the criteria.")
        sys.exit(0)
    
    print(f"Found {len(unprocessed_entries)} entries to process.")
    
    # Process entries up to the batch size
    entries_to_process = unprocessed_entries[:args.batch_size]
    
    for i, (path, entry, placeholder_format) in enumerate(entries_to_process):
        print(f"\nProcessing entry {i+1}/{len(entries_to_process)}: {' > '.join(path)}")
        
        # Generate names for this entry
        generated_names = generate_names_with_claude(
            entry, 
            placeholder_format, 
            briefing,
            anthropic_client
        )
        
        # Update the data with the generated names
        processed_data = update_entry_with_names(processed_data, path, generated_names)
        
        # Save after each entry in case we encounter errors
        save_json_file(processed_data, OUTPUT_JSON_PATH)
        
        print(f"Generated {len(generated_names)} names for {' > '.join(path)}")
        
    print("\nName generation complete!")
    print(f"Processed {len(entries_to_process)} out of {len(unprocessed_entries)} entries.")
    print(f"Output saved to {OUTPUT_JSON_PATH}")


if __name__ == "__main__":
    main() 