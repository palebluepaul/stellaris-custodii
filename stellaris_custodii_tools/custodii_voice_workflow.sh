#!/bin/bash
# Comprehensive workflow script for Custodii voice generation
# This script combines all the steps for generating voice files and updating the asset file

# Make sure you have Doppler installed and configured
# https://docs.doppler.com/docs/install-cli

# Install dependencies if needed
echo "Installing dependencies..."
pip install -r requirements.txt

# Create the necessary directories
echo "Creating directories..."
mkdir -p ../mod/sound/voice

# Step 1: Generate voice variants (if not already done)
if [ ! -f "../mod/sound/custodii_voice_variants.txt" ]; then
    echo "Generating voice variants..."
    doppler run -- python generate_voice_variants.py
else
    echo "Voice variants file already exists, skipping generation."
fi

# Step 2: Generate voice files
echo "Generating voice files..."
# Test mode first to make sure everything works
echo "Running in test mode (only a few lines)..."
doppler run -- python generate_voice_files.py --test

# Uncomment the following line to process all voice lines
# doppler run -- python generate_voice_files.py --batch-size 5

# Step 3: Update the asset file
echo "Updating asset file..."
python update_asset_file.py

# Step 4: Deploy the mod to see the changes
echo "Deploying mod..."
cd ..
python3 deploy_mod.py

echo "Workflow complete!"
echo "To process all voice lines, edit this script and uncomment the line after 'to process all voice lines'"
echo "Then run this script again." 