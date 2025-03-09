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
        print(f"Detected platform: {self.platform}")
        
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
        else:
            # Try to find config.json in the same directory as this script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(script_dir, 'config.json')
            if os.path.exists(config_path):
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
