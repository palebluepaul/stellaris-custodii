# Foundation Tools Specification

## Overview
This specification outlines the foundational Python tools needed to support the development and deployment of the Custodii race mod for Stellaris. These tools will handle cross-platform path resolution, mod format checking, and other utilities to ensure consistent development across Windows (WSL) and macOS environments.

## Requirements

### Cross-Platform Compatibility
- Must work on both Windows (via WSL) and macOS
- Must handle path differences between operating systems
- Must support accessing Stellaris files on Windows partition from WSL

### Core Functionality
- Path resolution between mod development environment and game installation
- Mod descriptor validation and generation
- File format checking (UTF-8 BOM for localization files)
- Asset validation (texture formats, sizes)
- Deployment assistance

## Tool Components

### 1. Path Resolution Module

```python
# path_resolver.py

import os
import platform
import subprocess
import json
from pathlib import Path

class StellarisPathResolver:
    """Resolves paths between development environment and Stellaris installation."""
    
    def __init__(self, config_path=None):
        """Initialize with optional config file path."""
        self.config = self._load_config(config_path)
        self.platform = platform.system()
        self.is_wsl = self._check_if_wsl()
        
    def _load_config(self, config_path):
        """Load configuration from JSON file or use defaults."""
        default_config = {
            "windows_stellaris_path": "C:/Program Files (x86)/Steam/steamapps/common/Stellaris",
            "windows_workshop_path": "C:/Program Files (x86)/Steam/steamapps/workshop/content/281990",
            "windows_mod_path": "C:/Users/USERNAME/Documents/Paradox Interactive/Stellaris/mod",
            "mac_stellaris_path": "/Users/USERNAME/Library/Application Support/Steam/steamapps/common/Stellaris",
            "mac_workshop_path": "/Users/USERNAME/Library/Application Support/Steam/steamapps/workshop/content/281990",
            "mac_mod_path": "/Users/USERNAME/Documents/Paradox Interactive/Stellaris/mod",
            "mod_name": "custodii",
            "mod_id": "custodii_race"
        }
        
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)
                
        return default_config
    
    def _check_if_wsl(self):
        """Check if running in Windows Subsystem for Linux."""
        if self.platform == "Linux":
            try:
                with open('/proc/version', 'r') as f:
                    return 'microsoft' in f.read().lower()
            except:
                return False
        return False
    
    def get_stellaris_path(self):
        """Get the path to Stellaris installation."""
        if self.platform == "Windows":
            return self.config["windows_stellaris_path"]
        elif self.platform == "Darwin":  # macOS
            return self.config["mac_stellaris_path"]
        elif self.is_wsl:
            # Convert Windows path to WSL path
            win_path = self.config["windows_stellaris_path"]
            return self._windows_to_wsl_path(win_path)
        else:
            raise NotImplementedError("Unsupported platform")
    
    def get_mod_path(self):
        """Get the path to Stellaris mods directory."""
        if self.platform == "Windows":
            return self.config["windows_mod_path"]
        elif self.platform == "Darwin":  # macOS
            return self.config["mac_mod_path"]
        elif self.is_wsl:
            # Convert Windows path to WSL path
            win_path = self.config["windows_mod_path"]
            return self._windows_to_wsl_path(win_path)
        else:
            raise NotImplementedError("Unsupported platform")
    
    def _windows_to_wsl_path(self, windows_path):
        """Convert a Windows path to a WSL path."""
        # Remove drive letter and convert backslashes
        path = windows_path.replace('\\', '/')
        if ':' in path:
            drive, path = path.split(':', 1)
            return f"/mnt/{drive.lower()}{path}"
        return path
    
    def _wsl_to_windows_path(self, wsl_path):
        """Convert a WSL path to a Windows path."""
        if wsl_path.startswith('/mnt/'):
            parts = wsl_path.split('/', 3)
            if len(parts) >= 4:
                drive = parts[2].upper()
                rest = parts[3]
                return f"{drive}:\\{rest.replace('/', '\\')}"
        return wsl_path
    
    def resolve_mod_file_path(self, relative_path):
        """Resolve a mod file path relative to the development environment."""
        # Implementation depends on project structure
        return os.path.join(os.getcwd(), relative_path)
    
    def get_deployment_path(self):
        """Get the path where the mod should be deployed."""
        mod_path = self.get_mod_path()
        return os.path.join(mod_path, self.config["mod_id"])
```

### 2. Mod Descriptor Generator

```python
# mod_descriptor.py

import os
import json
from pathlib import Path

class ModDescriptorGenerator:
    """Generates and validates Stellaris mod descriptor files."""
    
    def __init__(self, path_resolver):
        """Initialize with a path resolver instance."""
        self.path_resolver = path_resolver
        self.config = path_resolver.config
    
    def generate_descriptor(self, output_path=None):
        """Generate a .mod descriptor file."""
        if output_path is None:
            output_path = os.path.join(os.getcwd(), f"{self.config['mod_id']}.mod")
        
        mod_name = self.config.get("mod_name", "Custodii Race")
        mod_id = self.config.get("mod_id", "custodii_race")
        mod_version = self.config.get("mod_version", "1.0.0")
        supported_version = self.config.get("supported_version", "3.8.*")
        
        descriptor_content = f"""name="{mod_name}"
tags={{
    "Species"
    "Graphics"
    "Sound"
}}
version="{mod_version}"
picture="thumbnail.png"
supported_version="{supported_version}"
path="mod/{mod_id}"
remote_file_id="WORKSHOP_ID"
"""
        
        with open(output_path, 'w', encoding='utf-8-sig') as f:
            f.write(descriptor_content)
        
        # Also create descriptor.mod in the mod directory
        mod_dir = os.path.join(os.getcwd(), "mod")
        os.makedirs(mod_dir, exist_ok=True)
        with open(os.path.join(mod_dir, "descriptor.mod"), 'w', encoding='utf-8-sig') as f:
            f.write(descriptor_content)
        
        return output_path
    
    def validate_descriptor(self, descriptor_path=None):
        """Validate an existing .mod descriptor file."""
        if descriptor_path is None:
            descriptor_path = os.path.join(os.getcwd(), f"{self.config['mod_id']}.mod")
        
        if not os.path.exists(descriptor_path):
            return False, "Descriptor file does not exist"
        
        required_fields = ["name", "supported_version", "path"]
        missing_fields = []
        
        with open(descriptor_path, 'r', encoding='utf-8-sig') as f:
            content = f.read()
            
        for field in required_fields:
            if field not in content:
                missing_fields.append(field)
        
        if missing_fields:
            return False, f"Missing required fields: {', '.join(missing_fields)}"
        
        return True, "Descriptor file is valid"
```

### 3. File Format Checker

```python
# format_checker.py

import os
import chardet
from pathlib import Path

class FileFormatChecker:
    """Checks and fixes file formats for Stellaris mod files."""
    
    @staticmethod
    def check_utf8_bom(file_path):
        """Check if a file is UTF-8 with BOM."""
        with open(file_path, 'rb') as f:
            raw = f.read(4)
            if raw.startswith(b'\xef\xbb\xbf'):
                return True
            return False
    
    @staticmethod
    def convert_to_utf8_bom(file_path):
        """Convert a file to UTF-8 with BOM."""
        # Detect current encoding
        with open(file_path, 'rb') as f:
            raw = f.read()
            result = chardet.detect(raw)
            encoding = result['encoding']
        
        # Read content with detected encoding
        with open(file_path, 'r', encoding=encoding, errors='replace') as f:
            content = f.read()
        
        # Write with UTF-8 BOM
        with open(file_path, 'w', encoding='utf-8-sig') as f:
            f.write(content)
        
        return True
    
    @staticmethod
    def check_localization_files(directory):
        """Check all localization files in a directory."""
        results = []
        
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.yml') and 'localisation' in root:
                    file_path = os.path.join(root, file)
                    is_utf8_bom = FileFormatChecker.check_utf8_bom(file_path)
                    results.append({
                        'path': file_path,
                        'is_utf8_bom': is_utf8_bom
                    })
        
        return results
    
    @staticmethod
    def fix_localization_files(directory):
        """Fix all localization files in a directory."""
        results = FileFormatChecker.check_localization_files(directory)
        fixed = 0
        
        for result in results:
            if not result['is_utf8_bom']:
                FileFormatChecker.convert_to_utf8_bom(result['path'])
                fixed += 1
        
        return fixed
```

### 4. Asset Validator

```python
# asset_validator.py

import os
import struct
from pathlib import Path

class AssetValidator:
    """Validates game assets for Stellaris mods."""
    
    @staticmethod
    def check_dds_format(file_path):
        """Check if a DDS file has the correct format."""
        with open(file_path, 'rb') as f:
            # Check magic number
            magic = f.read(4)
            if magic != b'DDS ':
                return False, "Not a valid DDS file"
            
            # Read header size
            f.seek(4)
            header_size = struct.unpack('<I', f.read(4))[0]
            if header_size != 124:
                return False, "Invalid DDS header size"
            
            # Read dimensions
            f.seek(12)
            height = struct.unpack('<I', f.read(4))[0]
            width = struct.unpack('<I', f.read(4))[0]
            
            # Read pixel format
            f.seek(80)
            pfsize = struct.unpack('<I', f.read(4))[0]
            if pfsize != 32:
                return False, "Invalid pixel format size"
            
            return True, {
                "width": width,
                "height": height
            }
    
    @staticmethod
    def validate_portrait_textures(directory):
        """Validate portrait textures in a directory."""
        results = []
        
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.dds') and 'portraits' in root:
                    file_path = os.path.join(root, file)
                    valid, info = AssetValidator.check_dds_format(file_path)
                    
                    if valid:
                        # Check if dimensions are appropriate for portraits
                        if info["width"] < 400 or info["height"] < 400:
                            valid = False
                            info = "Portrait texture too small"
                    
                    results.append({
                        'path': file_path,
                        'valid': valid,
                        'info': info
                    })
        
        return results
    
    @staticmethod
    def validate_room_textures(directory):
        """Validate room background textures."""
        results = []
        
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.dds') and 'rooms' in root:
                    file_path = os.path.join(root, file)
                    valid, info = AssetValidator.check_dds_format(file_path)
                    
                    if valid:
                        # Check if dimensions are appropriate for rooms
                        if info["width"] < 1366 or info["height"] < 768:
                            valid = False
                            info = "Room texture too small"
                    
                    results.append({
                        'path': file_path,
                        'valid': valid,
                        'info': info
                    })
        
        return results
```

### 5. Deployment Helper

```python
# deployment_helper.py

import os
import shutil
import subprocess
from pathlib import Path

class DeploymentHelper:
    """Helps deploy the mod to the Stellaris mods directory."""
    
    def __init__(self, path_resolver):
        """Initialize with a path resolver instance."""
        self.path_resolver = path_resolver
    
    def deploy_mod(self, source_dir=None):
        """Deploy the mod to the Stellaris mods directory."""
        if source_dir is None:
            source_dir = os.path.join(os.getcwd(), "mod")
        
        target_dir = self.path_resolver.get_deployment_path()
        
        # Create target directory if it doesn't exist
        os.makedirs(target_dir, exist_ok=True)
        
        # Copy files
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, source_dir)
                dst_path = os.path.join(target_dir, rel_path)
                
                # Create destination directory if it doesn't exist
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                
                # Copy file
                shutil.copy2(src_path, dst_path)
        
        # Copy descriptor file
        descriptor_src = os.path.join(os.getcwd(), f"{self.path_resolver.config['mod_id']}.mod")
        descriptor_dst = os.path.join(os.path.dirname(target_dir), f"{self.path_resolver.config['mod_id']}.mod")
        shutil.copy2(descriptor_src, descriptor_dst)
        
        return target_dir
    
    def clean_deployment(self):
        """Remove the deployed mod."""
        target_dir = self.path_resolver.get_deployment_path()
        
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
        
        descriptor_path = os.path.join(os.path.dirname(target_dir), f"{self.path_resolver.config['mod_id']}.mod")
        if os.path.exists(descriptor_path):
            os.remove(descriptor_path)
        
        return True
```

### 6. Main CLI Tool

```python
# custodii_tools.py

import os
import sys
import argparse
import json
from pathlib import Path

from path_resolver import StellarisPathResolver
from mod_descriptor import ModDescriptorGenerator
from format_checker import FileFormatChecker
from asset_validator import AssetValidator
from deployment_helper import DeploymentHelper

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
        
        target_dir = deployment_helper.deploy_mod()
        print(f"Deployed mod to {target_dir}")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
```

## Configuration

### Config File Format
Create a `config.json` file with the following structure:

```json
{
    "windows_stellaris_path": "C:/Program Files (x86)/Steam/steamapps/common/Stellaris",
    "windows_workshop_path": "C:/Program Files (x86)/Steam/steamapps/workshop/content/281990",
    "windows_mod_path": "C:/Users/USERNAME/Documents/Paradox Interactive/Stellaris/mod",
    "mac_stellaris_path": "/Users/USERNAME/Library/Application Support/Steam/steamapps/common/Stellaris",
    "mac_workshop_path": "/Users/USERNAME/Library/Application Support/Steam/steamapps/workshop/content/281990",
    "mac_mod_path": "/Users/USERNAME/Documents/Paradox Interactive/Stellaris/mod",
    "mod_name": "Custodii Race",
    "mod_id": "custodii_race",
    "mod_version": "1.0.0",
    "supported_version": "3.8.*"
}
```

## Usage Examples

### Initialize Mod Structure
```bash
python custodii_tools.py init --name "Custodii Race" --id "custodii_race"
```

### Generate Descriptor
```bash
python custodii_tools.py descriptor
```

### Check and Fix Localization Files
```bash
python custodii_tools.py check-format --fix
```

### Validate Assets
```bash
python custodii_tools.py validate --type portraits
```

### Deploy Mod
```bash
python custodii_tools.py deploy
```

## Dependencies
- Python 3.8+
- chardet (for encoding detection)

## Implementation Notes
- The tools assume a specific directory structure with the mod files in a `mod/` subdirectory
- WSL path conversion handles the most common case of accessing Windows files from WSL
- Asset validation is basic and could be extended for more specific checks
- Error handling should be improved for production use

## Open Questions
- Should we add support for automatic texture conversion (e.g., PNG to DDS)?
- Do we need more sophisticated validation for specific file types?
- Should we add a packaging tool for Steam Workshop uploads?
- How should we handle version control integration? 