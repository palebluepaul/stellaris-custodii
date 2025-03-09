#!/usr/bin/env python3

import os
import sys
import argparse
import json
from pathlib import Path

from stellaris_custodii_tools.path_resolver import StellarisPathResolver
from stellaris_custodii_tools.mod_descriptor import ModDescriptorGenerator
from stellaris_custodii_tools.format_checker import FileFormatChecker
from stellaris_custodii_tools.asset_validator import AssetValidator
from stellaris_custodii_tools.deployment_helper import DeploymentHelper

def main():
    parser = argparse.ArgumentParser(description="Custodii Race Mod Tools")
    parser.add_argument('--config', help='Path to configuration file')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize mod structure')
    init_parser.add_argument('--name', default='Custodii Race', help='Mod name')
    init_parser.add_argument('--id', default='custodii_race', help='Mod ID')
    
    # Generate descriptor command
    desc_parser = subparsers.add_parser('descriptor', help='Generate mod descriptor')
    
    # Check format command
    format_parser = subparsers.add_parser('check-format', help='Check file formats')
    format_parser.add_argument('--fix', action='store_true', help='Fix format issues')
    
    # Validate assets command
    validate_parser = subparsers.add_parser('validate', help='Validate assets')
    validate_parser.add_argument('--type', choices=['portraits', 'rooms', 'all'], default='all', help='Asset type to validate')
    
    # Deploy command
    deploy_parser = subparsers.add_parser('deploy', help='Deploy mod')
    deploy_parser.add_argument('--clean', action='store_true', help='Clean existing deployment')
    deploy_parser.add_argument('--no-auto-version', dest='auto_detect_version', action='store_false', 
                              help='Disable automatic version detection')
    deploy_parser.set_defaults(auto_detect_version=True)
    
    # Detect version command
    version_parser = subparsers.add_parser('detect-version', help='Detect the latest Stellaris version')
    
    args = parser.parse_args()
    
    # Load configuration
    config_path = args.config
    path_resolver = StellarisPathResolver(config_path)
    
    if args.command == 'init':
        # Update config with provided name and ID
        path_resolver.config['mod_name'] = args.name
        path_resolver.config['mod_id'] = args.id
        
        # Create directory structure
        directories = [
            "common/name_lists",
            "common/species_classes",
            "common/traits",
            "common/governments/civics",
            "common/personalities",
            "common/opinion_modifiers",
            "common/diplo_phrases",
            "common/graphical_culture",
            "events",
            "gfx/interface/icons/traits",
            "gfx/interface/icons/governments/civics",
            "gfx/interface/rooms",
            "gfx/models/portraits/custodii",
            "gfx/portraits/portraits",
            "gfx/portraits/portrait_groups",
            "gfx/portraits/city_sets",
            "gfx/models/ships/custodii_ships",
            "localisation/english",
            "prescripted_countries",
            "sound/vo/custodii-advisor",
            "sound/advisor_voice_types"
        ]
        
        for directory in directories:
            os.makedirs(os.path.join("mod", directory), exist_ok=True)
        
        # Generate descriptor
        descriptor_generator = ModDescriptorGenerator(path_resolver)
        descriptor_generator.generate_descriptor()
        
        print(f"Initialized mod structure for {args.name}")
    
    elif args.command == 'descriptor':
        descriptor_generator = ModDescriptorGenerator(path_resolver)
        descriptor_path = descriptor_generator.generate_descriptor()
        print(f"Generated descriptor at {descriptor_path}")
    
    elif args.command == 'check-format':
        results = FileFormatChecker.check_localization_files("mod/localisation")
        
        issues = [r for r in results if not r['is_utf8_bom']]
        
        if issues:
            print(f"Found {len(issues)} files with format issues:")
            for issue in issues:
                print(f"  {issue['path']} - Not UTF-8 with BOM")
            
            if args.fix:
                fixed = FileFormatChecker.fix_localization_files("mod/localisation")
                print(f"Fixed {fixed} files")
        else:
            print("All localization files have correct format")
    
    elif args.command == 'validate':
        if args.type in ['portraits', 'all']:
            results = AssetValidator.validate_portrait_textures("mod/gfx")
            issues = [r for r in results if not r['valid']]
            
            if issues:
                print(f"Found {len(issues)} portrait texture issues:")
                for issue in issues:
                    print(f"  {issue['path']} - {issue['info']}")
            else:
                print("All portrait textures are valid")
        
        if args.type in ['rooms', 'all']:
            results = AssetValidator.validate_room_textures("mod/gfx")
            issues = [r for r in results if not r['valid']]
            
            if issues:
                print(f"Found {len(issues)} room texture issues:")
                for issue in issues:
                    print(f"  {issue['path']} - {issue['info']}")
            else:
                print("All room textures are valid")
    
    elif args.command == 'deploy':
        deployment_helper = DeploymentHelper(path_resolver)
        
        if args.clean:
            deployment_helper.clean_deployment()
            print("Cleaned existing deployment")
        
        target_dir = deployment_helper.deploy_mod(auto_detect_version=args.auto_detect_version)
        print(f"Deployed mod to {target_dir}")
    
    elif args.command == 'detect-version':
        deployment_helper = DeploymentHelper(path_resolver)
        latest_version = deployment_helper.detect_latest_game_version()
        if latest_version:
            print(f"Latest Stellaris version detected: {latest_version}")
            print(f"Current supported version in config: {path_resolver.config.get('supported_version')}")
        else:
            print("Failed to detect Stellaris version")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
