#!/usr/bin/env python3
"""
Deploy the Custodii Race mod to the Stellaris mods directory.
"""

import os
import sys
import argparse
from stellaris_custodii_tools.path_resolver import StellarisPathResolver
from stellaris_custodii_tools.deployment_helper import DeploymentHelper

def main():
    """Deploy the mod to the Stellaris mods directory."""
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Deploy Custodii Race mod to Stellaris mods directory')
    parser.add_argument('--no-validate', action='store_true', help='Skip validation checks')
    parser.add_argument('--no-encoding', action='store_true', 
                       help='Skip UTF-8 BOM encoding conversion (by default, the script ensures all text files are properly encoded as UTF-8 with BOM)')
    parser.add_argument('--no-version-detect', action='store_true', help='Skip auto-detection of Stellaris version')
    parser.add_argument('--no-cache-clear', action='store_true', help='Skip clearing Stellaris cache folder (by default, cache is cleared on every deploy)')
    args = parser.parse_args()
    
    # Initialize the path resolver
    path_resolver = StellarisPathResolver()
    
    # Initialize the deployment helper
    deployment_helper = DeploymentHelper(path_resolver)
    
    # Deploy the mod
    try:
        # If --no-cache-clear is specified but we want to skip the automatic cache clearing in deploy_mod
        # we need to clear the cache manually first, because we can't pass this parameter to deploy_mod
        if args.no_cache_clear:
            # Clear the cache attribute from the deployment_helper to prevent automatic clearing
            setattr(deployment_helper, 'clean_stellaris_cache', lambda: None)
        
        target_dir = deployment_helper.deploy_mod(
            validate=not args.no_validate,
            ensure_encoding=not args.no_encoding,
            auto_detect_version=not args.no_version_detect
        )
        print("You can now enable the mod in the Stellaris launcher.")
    except Exception as e:
        print(f"Error deploying mod: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 