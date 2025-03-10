#!/bin/bash
# Example script to run the voice variant generator with Doppler

# Make sure you have Doppler installed and configured
# https://docs.doppler.com/docs/install-cli

# Install dependencies if needed
pip install -r requirements.txt

# Run the script with Doppler to inject the ANTHROPIC_API_KEY
doppler run -- python generate_voice_variants.py --batch-size 5 --variants 10

# To process a specific section, you can create a temporary file with just those lines
# For example, to process only the generic phrases:
# grep -A 10 "GENERIC PHRASES" ../mod/sound/custodii_voice_lines.txt > /tmp/generic_phrases.txt
# doppler run -- python generate_voice_variants.py --input /tmp/generic_phrases.txt --output ../mod/sound/generic_phrases_variants.txt 