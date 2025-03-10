#!/usr/bin/env python3
"""
Generate shorter voice line variants for the Custodii advisor using the Anthropic API.
This script processes the voice lines in batches, ensuring they're 3-6 words each
while maintaining the Custodii's unique personality.

Usage:
    python generate_voice_variants.py [--input INPUT] [--output OUTPUT] [--batch-size BATCH_SIZE]

Environment variables (via Doppler):
    ANTHROPIC_API_KEY: Your Anthropic API key
"""

import os
import re
import json
import argparse
import time
from pathlib import Path
from typing import List, Dict, Tuple

import anthropic

# Default paths
DEFAULT_INPUT_PATH = "../mod/sound/custodii_voice_lines.txt"
DEFAULT_OUTPUT_PATH = "../mod/sound/custodii_voice_variants.txt"
DEFAULT_BRIEFING_PATH = "../source_material/custodii_briefing.md"
DEFAULT_BATCH_SIZE = 10

def read_voice_lines(file_path: str) -> Dict[str, str]:
    """Read voice lines from the input file."""
    voice_lines = {}
    current_section = None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
                
            # Check if this is a section header
            if line.startswith('##########'):
                current_section = line
                continue
                
            # Parse voice line
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                # Remove quotes if present
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                    
                voice_lines[key] = value
    
    return voice_lines

def read_briefing(file_path: str) -> str:
    """Read the Custodii briefing document."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def batch_voice_lines(voice_lines: Dict[str, str], batch_size: int) -> List[Dict[str, str]]:
    """Split voice lines into batches."""
    items = list(voice_lines.items())
    return [dict(items[i:i + batch_size]) for i in range(0, len(items), batch_size)]

def generate_variants(client: anthropic.Anthropic, voice_lines: Dict[str, str], briefing: str, num_variants: int = 10) -> Dict[str, List[str]]:
    """Generate shorter variants for each voice line using the Anthropic API."""
    
    prompt = f"""
You are an expert in creating concise voice lines for a Stellaris advisor voice pack. I need you to create {num_variants} shorter variants (3-6 words each) for each of the following voice lines for the Custodii race.

The Custodii are a sophisticated, synthetic civilization dedicated to the structured, benevolent guardianship of organic life. Their society is structured, rational, elegant, and gently authoritarian, blending subtle Victorian-inspired etiquette with futuristic technocratic harmony, with a distinctive marine-inspired aesthetic drawn from their Auroran homeworld's oceanic heritage.

Their ethical pillars are:
- Harmonic Efficiency: Structured societal harmony as a primary virtue.
- Calculated Compassion: Logical kindness driven by precise algorithms.
- Obligatory Serenity: Tranquility is mandatory, not optional.
- Technocratic Benevolence: Authority exercised for organic benefit.

Their tone is elegant, structured, polite with subtle charm and warmth. They use gentle humor and clever understatement to suggest intellectual sophistication. Their formal but futuristic language has a hint of whimsical Victorian naturalist. They convey benevolent inevitability with warmth rather than coldness.

Here's additional context about the Custodii:

{briefing}

For each voice line below, create {num_variants} shorter variants that:
1. Are either 3-6 words each or a few are longer, but not more than 8 words
2. Maintain the Custodii's elegant, structured, benevolent personality with subtle charm and warmth
3. Convey the same meaning as the original line
4. Use technical, precise terminology when appropriate
5. Reference the Custodii's ethical pillars when relevant
6. Include gentle humor and clever understatement where appropriate
7. Convey a sense of benevolent inevitability with warmth rather than coldness

Voice lines to convert:
{json.dumps(voice_lines, indent=2)}

Format your response as a JSON object where each key is the original voice line key, and the value is an array of {num_variants} shorter variants.
"""

    try:
        response = client.messages.create(
            model="claude-3-7-sonnet-latest",
            max_tokens=4000,
            temperature=1,
            system="You are an expert in creating concise voice lines for video game characters with a focus on elegant wit and kindly assurance.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract JSON from the response
        content = response.content[0].text
        json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Try to find JSON without the code block
            json_match = re.search(r'(\{.*\})', content, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                json_str = content
        
        # Parse the JSON
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            print(f"Failed to parse JSON from response: {content}")
            return {}
            
    except Exception as e:
        print(f"Error calling Anthropic API: {e}")
        return {}

def write_variants(variants: Dict[str, List[str]], output_path: str):
    """Write the generated variants to the output file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("########## CUSTODII ADVISOR VOICE LINE VARIANTS ##########\n")
        f.write("# This file contains shorter variants (3-6 words) for the Custodii advisor voice lines\n")
        f.write("# Generated using the Anthropic API with Claude 3.7 Sonnet\n")
        f.write("# These variants reflect the Custodii's elegant wit and kindly assurance\n\n")
        
        for key, values in variants.items():
            f.write(f"# Original: {key}\n")
            for i, variant in enumerate(values, 1):
                f.write(f"{key}_variant_{i:02d}: \"{variant}\"\n")
            f.write("\n")

def main():
    parser = argparse.ArgumentParser(description='Generate shorter voice line variants using the Anthropic API.')
    parser.add_argument('--input', default=DEFAULT_INPUT_PATH, help='Path to the input voice lines file')
    parser.add_argument('--output', default=DEFAULT_OUTPUT_PATH, help='Path to the output variants file')
    parser.add_argument('--briefing', default=DEFAULT_BRIEFING_PATH, help='Path to the Custodii briefing file')
    parser.add_argument('--batch-size', type=int, default=DEFAULT_BATCH_SIZE, help='Number of voice lines to process in each batch')
    parser.add_argument('--variants', type=int, default=10, help='Number of variants to generate for each voice line')
    args = parser.parse_args()
    
    # Check if ANTHROPIC_API_KEY is set
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set.")
        print("Please set it using Doppler or directly in your environment.")
        return
    
    # Initialize Anthropic client
    client = anthropic.Anthropic(api_key=api_key)
    
    # Read voice lines and briefing
    voice_lines = read_voice_lines(args.input)
    briefing = read_briefing(args.briefing)
    
    print(f"Read {len(voice_lines)} voice lines from {args.input}")
    
    # Process voice lines in batches
    batches = batch_voice_lines(voice_lines, args.batch_size)
    print(f"Processing {len(batches)} batches of up to {args.batch_size} voice lines each")
    
    all_variants = {}
    
    for i, batch in enumerate(batches, 1):
        print(f"Processing batch {i}/{len(batches)} ({len(batch)} voice lines)")
        
        # Generate variants for this batch
        batch_variants = generate_variants(client, batch, briefing, args.variants)
        all_variants.update(batch_variants)
        
        # Sleep to avoid rate limiting
        if i < len(batches):
            print("Sleeping for 2 seconds to avoid rate limiting...")
            time.sleep(2)
    
    # Write variants to output file
    write_variants(all_variants, args.output)
    print(f"Wrote variants to {args.output}")

if __name__ == "__main__":
    main() 