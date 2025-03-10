#!/bin/bash
# Example script to run the asset update script

# Create the output directory if it doesn't exist
mkdir -p ../mod/sound

# Run the asset update script
python update_asset_file.py

# To specify different input or output files:
# python update_asset_file.py --variants /path/to/variants.txt --template /path/to/template.asset --output /path/to/output.asset

# Deploy the mod to see the changes
cd ..
python3 deploy_mod.py 