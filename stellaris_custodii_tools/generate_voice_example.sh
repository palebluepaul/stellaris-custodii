#!/bin/bash
# Example script to run the voice file generator with Doppler

# Make sure you have Doppler installed and configured
# https://docs.doppler.com/docs/install-cli

# Install dependencies if needed
pip install -r requirements.txt

# Create the output directory if it doesn't exist
mkdir -p ../mod/sound/voice

# Run the script with Doppler to inject the ELEVENLABS_API_KEY
# Test mode - only process a few lines
echo "Running in test mode (only a few lines)..."
doppler run -- python generate_voice_files.py --test

# To process all voice lines:
# doppler run -- python generate_voice_files.py

# To process with a smaller batch size (to reduce rate limiting issues):
# doppler run -- python generate_voice_files.py --batch-size 5

# To specify a different input or output:
# doppler run -- python generate_voice_files.py --input /path/to/input.txt --output /path/to/output/dir 