#!/usr/bin/env python3
"""
This script generates thematic guidance for entries in the custodii_names.json file
using OpenAI's GPT-4.5 model, with the custodii_briefing.md document as context.
"""

import json
import os
import time
from pathlib import Path
import openai
import argparse

def load_json_file(filepath):
    """Load a JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json_file(data, filepath):
    """Save data to a JSON file with nice formatting."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Updated file saved to {filepath}")

def load_context_document(filepath):
    """Load the context document (custodii_briefing.md)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def generate_thematic_guidance(client, entry_type, entry_name, entry_details, context):
    """Generate thematic guidance for an entry using OpenAI's API."""
    # Construct the prompt
    prompt = f"""
The guidance should:
1. Be consistent with the Custodii's sophisticated, intellectual, and aquatic-inspired aesthetic
2. Provide specific naming patterns, themes, or conventions to follow
3. Include example word elements, prefixes, or suffixes that would be appropriate
4. Reflect the Custodii's core ethical pillars: Harmonic Efficiency, Calculated Compassion, Obligatory Serenity, and Technocratic Benevolence
5. Be 3-5 sentences in length, specific and actionable

CONTEXT:
{context}

Based on the provided context about the Custodii Empire, create detailed thematic guidance for naming {entry_type} of the type "{entry_name}".

Entry description: {entry_details['description']}
"""

    # Call the OpenAI API
    try:
        response = client.chat.completions.create(
            model="gpt-4.5-preview",  # Using the most capable model available
            messages=[
                {"role": "system", "content": "You are a creative naming consultant for a fictional space empire in a strategy game. You provide concise, specific guidance for generating thematically consistent names."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract and return the generated guidance
        guidance = response.choices[0].message.content.strip()
        return guidance
    
    except Exception as e:
        print(f"Error generating guidance for {entry_type} - {entry_name}: {e}")
        return ""

def process_entries(data, context, client, json_file_path, limit=None, force_overwrite=False):
    """Process entries in the custodii_names.json file, saving after each update."""
    # Keep track of how many entries we've processed
    processed_count = 0
    
    # Process each category (ship_names, planet_names, etc.)
    for category, category_entries in data.items():
        print(f"\nProcessing category: {category}")
        
        # Process each entry in the category
        for entry_name, entry_details in category_entries.items():
            # Skip if we've reached the limit (treat 0 as "no limit")
            if limit is not None and limit > 0 and processed_count >= limit:
                return processed_count
            
            print(f"Generating thematic guidance for {category} - {entry_name}...")
            
            # Skip if the entry already has non-empty thematic_guidance and force_overwrite is False
            if not force_overwrite and entry_details.get("thematic_guidance") and entry_details["thematic_guidance"].strip():
                print(f"  - Already has guidance, skipping")
                continue
            
            # Generate thematic guidance
            guidance = generate_thematic_guidance(client, category, entry_name, entry_details, context)
            
            # Update the entry with the generated guidance
            entry_details["thematic_guidance"] = guidance
            
            print(f"  - Done: {guidance[:50]}...")
            
            # Save the file after each entry is processed
            save_json_file(data, json_file_path)
            print(f"  - Saved progress to {json_file_path}")
            
            # Increment the processed count
            processed_count += 1
            
            # Sleep to avoid hitting API rate limits
            time.sleep(1)
    
    return processed_count

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Generate thematic guidance for Custodii names.')
    parser.add_argument('--limit', type=int, default=5, help='Limit the number of entries to process (default: 5)')
    parser.add_argument('--force', action='store_true', help='Force overwrite existing thematic guidance')
    args = parser.parse_args()
    
    # Initialize OpenAI client
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    if not openai_api_key:
        print("Error: OPENAI_API_KEY environment variable not set.")
        print("Run with doppler run -- python stellaris_custodii_tools/generate_thematic_guidance.py")
        return
    
    client = openai.OpenAI(api_key=openai_api_key)
    
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    
    # Load the custodii_names.json file
    json_file_path = project_root / "output" / "custodii_names.json"
    data = load_json_file(json_file_path)
    
    # Load the context document
    context_file_path = project_root / "source_material" / "custodii_briefing.md"
    context = load_context_document(context_file_path)
    
    # Process entries
    processed_count = process_entries(data, context, client, json_file_path, limit=args.limit, force_overwrite=args.force)
    print(f"\nProcessed {processed_count} entries.")
    
    print("\nDone! All entries have been processed and saved to the custodii_names.json file.")

if __name__ == "__main__":
    main() 