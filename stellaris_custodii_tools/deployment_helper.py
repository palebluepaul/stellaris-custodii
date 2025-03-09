import os
import shutil
import subprocess
import sqlite3
from pathlib import Path

class DeploymentHelper:
    """Helps deploy the mod to the Stellaris mods directory."""
    
    def __init__(self, path_resolver):
        """Initialize with a path resolver instance."""
        self.path_resolver = path_resolver
    
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
    
    def deploy_mod(self, source_dir=None, auto_detect_version=True):
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
