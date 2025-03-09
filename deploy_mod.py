#!/usr/bin/env python3
"""
Deploy the Custodii Race mod to the Stellaris mods directory.
"""

import os
import sys
from stellaris_custodii_tools.path_resolver import StellarisPathResolver
from stellaris_custodii_tools.deployment_helper import DeploymentHelper

def main():
    """Deploy the mod to the Stellaris mods directory."""
    # Initialize the path resolver
    path_resolver = StellarisPathResolver()
    
    # Initialize the deployment helper
    deployment_helper = DeploymentHelper(path_resolver)
    
    # Deploy the mod
    try:
        target_dir = deployment_helper.deploy_mod()
        print(f"Mod deployed successfully to: {target_dir}")
        print("You can now enable the mod in the Stellaris launcher.")
    except Exception as e:
        print(f"Error deploying mod: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 