#!/usr/bin/env python3
"""
Update the Custodii advisor voice asset file to point to the generated voice files.

This script reads the voice variants file and the template asset file, and generates
a new asset file that includes sound definitions for all the voice variants.

Usage:
    python update_asset_file.py [--variants VARIANTS] [--template TEMPLATE] [--output OUTPUT]

Arguments:
    --variants: Path to the voice variants file (default: ../mod/sound/custodii_voice_variants.txt)
    --template: Path to the template asset file (default: ../mod/sound/custodii_advisor_voice_template.asset)
    --output: Path to the output asset file (default: ../mod/sound/custodii_advisor_voice.asset)
"""

import os
import re
import argparse
import logging
from typing import Dict, List, Set

# Constants
DEFAULT_VARIANTS_PATH = "../mod/sound/custodii_voice_variants.txt"
DEFAULT_TEMPLATE_PATH = "../mod/sound/custodii_advisor_voice_template.asset"
DEFAULT_OUTPUT_PATH = "../mod/sound/custodii_advisor_voice.asset"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def read_voice_variants(file_path: str) -> Dict[str, str]:
    """Read voice line variants from the specified file."""
    variants = {}
    
    logger.info(f"Reading voice variants from {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
            
            # Parse the line to extract key and text
            match = re.match(r'([^:]+):\s*"([^"]+)"', line)
            if match:
                key = match.group(1).strip()
                text = match.group(2).strip()
                variants[key] = text
    
    logger.info(f"Found {len(variants)} voice variants")
    return variants

def extract_sound_effect_names(template_path: str) -> Set[str]:
    """Extract sound effect names from the template file."""
    sound_effects = set()
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
        # Find all soundeffect blocks
        for match in re.finditer(r'soundeffect\s*=\s*{\s*name\s*=\s*([^\s]+)', content):
            sound_effects.add(match.group(1))
    
    logger.info(f"Found {len(sound_effects)} sound effects in template")
    return sound_effects

def group_variants_by_base_key(variants: Dict[str, str]) -> Dict[str, List[str]]:
    """Group variants by their base key (without the _variant_XX suffix)."""
    grouped = {}
    
    for key in variants.keys():
        # Extract the base key (remove _variant_XX suffix)
        match = re.match(r'(.+)_variant_\d+', key)
        if match:
            base_key = match.group(1)
            if base_key not in grouped:
                grouped[base_key] = []
            grouped[base_key].append(key)
    
    return grouped

def generate_asset_file(
    template_path: str,
    variants: Dict[str, str],
    output_path: str
) -> None:
    """Generate the asset file with sound definitions for all voice variants."""
    # Read the template file
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Extract existing sound effect names
    existing_sound_effects = extract_sound_effect_names(template_path)
    
    # Group variants by base key
    grouped_variants = group_variants_by_base_key(variants)
    
    # Create the output content
    output_content = template_content
    
    # Add sound definitions for each variant
    sound_definitions = []
    for variant_key in variants.keys():
        sound_definitions.append(f"""
sound = {{
    name = "{variant_key}"
    file = "voice/{variant_key}.wav"
    volume = 0.7
}}
""")
    
    # Add sound effect definitions for each base key
    sound_effect_definitions = []
    for base_key, variant_keys in grouped_variants.items():
        # Skip if this sound effect already exists in the template
        if base_key in existing_sound_effects:
            continue
        
        # Create a sound effect that includes all variants
        sounds = "\n        ".join([f'sound = {key}' for key in variant_keys])
        sound_effect_definitions.append(f"""
soundeffect = {{
    name = {base_key}
    sounds = {{
        {sounds}
    }}
    volume = 0.45
    max_audible = 1
    max_audible_behaviour = fail
}}
""")
    
    # Append the sound and sound effect definitions to the output content
    if sound_definitions:
        output_content += "\n\n########## VOICE VARIANT SOUND DEFINITIONS ##########\n"
        output_content += "".join(sound_definitions)
    
    if sound_effect_definitions:
        output_content += "\n\n########## VOICE VARIANT SOUND EFFECT DEFINITIONS ##########\n"
        output_content += "".join(sound_effect_definitions)
    
    # Write the output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output_content)
    
    logger.info(f"Generated asset file: {output_path}")
    logger.info(f"Added {len(sound_definitions)} sound definitions and {len(sound_effect_definitions)} sound effect definitions")

def main():
    parser = argparse.ArgumentParser(description='Update the Custodii advisor voice asset file.')
    parser.add_argument('--variants', default=DEFAULT_VARIANTS_PATH, help='Path to the voice variants file')
    parser.add_argument('--template', default=DEFAULT_TEMPLATE_PATH, help='Path to the template asset file')
    parser.add_argument('--output', default=DEFAULT_OUTPUT_PATH, help='Path to the output asset file')
    args = parser.parse_args()
    
    # Check if the input files exist
    if not os.path.exists(args.variants):
        logger.error(f"Voice variants file not found: {args.variants}")
        return
    
    if not os.path.exists(args.template):
        logger.error(f"Template asset file not found: {args.template}")
        return
    
    # Read voice variants
    variants = read_voice_variants(args.variants)
    
    # Generate the asset file
    generate_asset_file(args.template, variants, args.output)
    
    logger.info("Asset file update complete")

if __name__ == "__main__":
    main() 