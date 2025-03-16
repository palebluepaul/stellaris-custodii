import os
import shutil
import subprocess
import sqlite3
from pathlib import Path
from .mod_validator import ModValidator
from .format_checker import FileFormatChecker

class DeploymentHelper:
    """Helps deploy the mod to the Stellaris mods directory."""
    
    def __init__(self, path_resolver):
        """Initialize with a path resolver instance."""
        self.path_resolver = path_resolver
        self.validator = ModValidator(path_resolver)
    
    def detect_latest_game_version(self):
        """Detect the latest Stellaris game version from the launcher database."""
        try:
            # Determine the path to the launcher database based on platform
            if self.path_resolver.platform == "Darwin":  # macOS
                launcher_db_path = os.path.expanduser("~/Documents/Paradox Interactive/Stellaris/launcher-v2.sqlite")
            elif self.path_resolver.platform == "Windows":
                launcher_db_path = os.path.join(os.environ["USERPROFILE"], "Documents", "Paradox Interactive", "Stellaris", "launcher-v2.sqlite")
            elif self.path_resolver.is_wsl:
                # For WSL, we need to convert the Windows path
                win_path = os.path.join("C:", "Users", os.environ.get("USER", "USERNAME"), "Documents", "Paradox Interactive", "Stellaris", "launcher-v2.sqlite")
                launcher_db_path = self.path_resolver._windows_to_wsl_path(win_path)
            else:
                # Default fallback
                launcher_db_path = os.path.expanduser("~/Documents/Paradox Interactive/Stellaris/launcher-v2.sqlite")
            
            # Check if the database file exists
            if not os.path.exists(launcher_db_path):
                print(f"Launcher database not found at {launcher_db_path}")
                return None
            
            # Connect to the database and query for the latest version
            conn = sqlite3.connect(launcher_db_path)
            cursor = conn.cursor()
            
            # Query the mods table for required versions
            cursor.execute("SELECT requiredVersion FROM mods WHERE requiredVersion IS NOT NULL")
            versions = cursor.fetchall()
            conn.close()
            
            if not versions:
                print("No version information found in the launcher database")
                return None
            
            # Process versions to find the latest one
            # Remove 'v' prefix if present and filter out invalid versions
            clean_versions = []
            for version_tuple in versions:
                version = version_tuple[0]
                if version.startswith('v'):
                    version = version[1:]
                
                # Only consider versions that follow the major.minor.* pattern
                if version and '.' in version and '*' in version:
                    parts = version.split('.')
                    if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
                        clean_versions.append((int(parts[0]), int(parts[1])))
            
            if not clean_versions:
                print("No valid version patterns found")
                return None
            
            # Find the latest version
            latest_version = max(clean_versions)
            latest_version_str = f"{latest_version[0]}.{latest_version[1]}.*"
            
            print(f"Detected latest game version: {latest_version_str}")
            return latest_version_str
            
        except Exception as e:
            print(f"Error detecting game version: {str(e)}")
            return None
    
    def ensure_utf8_bom_encoding(self, source_dir):
        """Ensure all text files that require UTF-8 BOM are properly encoded."""
        print("Ensuring proper UTF-8 BOM encoding for mod files...")
        
        # List of file types that need UTF-8 BOM encoding
        # Adding more file types that might need UTF-8 BOM encoding
        utf8_bom_required_types = [
            "localization", "name_list", "events", "prescripted_countries",
            "species_rights", "tradition", "ascension_perk", "diplomacy"
        ]
        
        # List of file extensions that might need checking
        utf8_bom_extensions = [".txt", ".yml", ".yaml", ".json", ".mod"]
        
        # Get all files that need conversion
        converted_files = []
        
        for root, _, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_type = self.validator._detect_file_type(file_path)
                file_ext = os.path.splitext(file)[1].lower()
                
                # Convert if either file type matches or extension matches and it's a text file
                if (file_type in utf8_bom_required_types or file_ext in utf8_bom_extensions) and self._is_text_file(file_path):
                    if not FileFormatChecker.check_utf8_bom(file_path):
                        FileFormatChecker.convert_to_utf8_bom(file_path)
                        converted_files.append(file_path)
        
        if converted_files:
            print(f"Converted {len(converted_files)} files to UTF-8 BOM encoding")
            for file in converted_files[:5]:  # Show first 5 files
                print(f"  - {os.path.relpath(file, source_dir)}")
            if len(converted_files) > 5:
                print(f"  - and {len(converted_files) - 5} more...")
        else:
            print("All files already have correct encoding")
        
        return converted_files
    
    def _is_text_file(self, file_path):
        """Check if a file is a text file and not a binary file."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                f.read(1024)  # Try to read some content
            return True
        except UnicodeDecodeError:
            return False
    
    def validate_mod(self, source_dir):
        """Validate the mod before deployment."""
        print("Validating mod files...")
        
        # Validate whole directory
        validation_results = self.validator.validate_mod_directory(source_dir)
        
        # Count issues
        error_count = 0
        warning_count = 0
        
        for category, results in validation_results["results"].items():
            for result in results:
                error_count += len(result.get("errors", []))
                warning_count += len(result.get("warnings", []))
        
        # Print summary
        if validation_results["valid"]:
            print(f"Validation passed with {warning_count} warnings")
        else:
            print(f"Validation failed with {error_count} errors and {warning_count} warnings")
        
        # Print specific name list validation errors and warnings
        name_list_results = validation_results["results"].get("name_lists", [])
        for result in name_list_results:
            if not result.get("valid", True) or result.get("warnings", []):
                print(f"\nIssues in name list file: {os.path.basename(result['path'])}")
                
                for error in result.get("errors", []):
                    print(f"  ERROR: {error}")
                
                for warning in result.get("warnings", []):
                    print(f"  WARNING: {warning}")
        
        return validation_results
    
    def clean_stellaris_cache(self):
        """Clear the Stellaris cache folder to ensure clean deployment."""
        try:
            # Determine the path to the Stellaris cache folder based on platform
            if self.path_resolver.platform == "Darwin":  # macOS
                cache_dir = os.path.expanduser("~/Documents/Paradox Interactive/Stellaris/cache")
            elif self.path_resolver.platform == "Windows":
                cache_dir = os.path.join(os.environ["USERPROFILE"], "Documents", "Paradox Interactive", "Stellaris", "cache")
            elif self.path_resolver.is_wsl:
                # For WSL, we need to convert the Windows path
                win_path = os.path.join("C:", "Users", os.environ.get("USER", "USERNAME"), "Documents", "Paradox Interactive", "Stellaris", "cache")
                cache_dir = self.path_resolver._windows_to_wsl_path(win_path)
            else:
                # Default fallback for Linux
                cache_dir = os.path.expanduser("~/Documents/Paradox Interactive/Stellaris/cache")
            
            if os.path.exists(cache_dir) and os.path.isdir(cache_dir):
                print(f"Clearing Stellaris cache at: {cache_dir}")
                for item in os.listdir(cache_dir):
                    item_path = os.path.join(cache_dir, item)
                    if os.path.isfile(item_path):
                        os.unlink(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                print("Cache cleared successfully")
                return True
            else:
                print(f"Cache directory not found at {cache_dir}, skipping cache clear")
                return False
        except Exception as e:
            print(f"Error clearing cache: {str(e)}")
            return False
    
    def deploy_mod(self, source_dir=None, auto_detect_version=True, validate=True, ensure_encoding=True):
        """Deploy the mod to the Stellaris mods directory."""
        if source_dir is None:
            source_dir = os.path.join(os.getcwd(), "mod")
        
        # Auto-detect and update the game version if requested
        if auto_detect_version:
            latest_version = self.detect_latest_game_version()
            if latest_version and latest_version != self.path_resolver.config.get("supported_version"):
                print(f"Updating supported version from {self.path_resolver.config.get('supported_version')} to {latest_version}")
                self.path_resolver.config["supported_version"] = latest_version
                
                # Update the config file
                config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
                if os.path.exists(config_path):
                    import json
                    with open(config_path, 'w') as f:
                        json.dump(self.path_resolver.config, f, indent=4)
        
        # Clear Stellaris cache
        self.clean_stellaris_cache()
        
        # Ensure proper encoding
        if ensure_encoding:
            self.ensure_utf8_bom_encoding(source_dir)
        
        # Validate mod
        if validate:
            validation_results = self.validate_mod(source_dir)
            # Continue deployment even with warnings, but stop on errors if not valid
            if not validation_results["valid"]:
                print("WARNING: Deployment will continue despite validation errors")
                print("Check the Stellaris error.log after running the game to confirm if these issues are resolved")
        
        target_dir = self.path_resolver.get_deployment_path()
        
        # Clean the existing mod directory if it exists
        if os.path.exists(target_dir):
            print(f"Removing existing mod directory: {target_dir}")
            shutil.rmtree(target_dir)
        
        # Clean the descriptor file if it exists
        descriptor_dst = os.path.join(os.path.dirname(target_dir), f"{self.path_resolver.config['mod_id']}.mod")
        if os.path.exists(descriptor_dst):
            os.remove(descriptor_dst)
        
        # Create target directory
        os.makedirs(target_dir, exist_ok=True)
        
        # Copy files
        print(f"Copying mod files from {source_dir} to {target_dir}")
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
        shutil.copy2(descriptor_src, descriptor_dst)
        
        print(f"Mod deployed successfully to: {target_dir}")
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
