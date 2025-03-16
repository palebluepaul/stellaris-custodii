import os
from pathlib import Path
from .asset_validator import AssetValidator
from .format_checker import FileFormatChecker
from .namelist_validator import NameListValidator

class ModValidator:
    """Validates Stellaris mod elements and structure."""
    
    def __init__(self, path_resolver=None):
        """Initialize the validator with an optional path resolver."""
        self.path_resolver = path_resolver
    
    def validate_mod_directory(self, directory):
        """Validate a mod directory structure and contents."""
        results = {
            "assets": self._validate_assets(directory),
            "localization": self._validate_localization(directory),
            "name_lists": self._validate_name_lists(directory)
        }
        
        # Add overall status
        valid = all(
            result.get("valid", True) 
            for category in results.values() 
            for result in category
        )
        
        return {
            "valid": valid,
            "results": results
        }
    
    def validate_mod_file(self, file_path, file_type=None):
        """Validate a specific mod file."""
        if not file_type:
            file_type = self._detect_file_type(file_path)
        
        if file_type == "name_list":
            return NameListValidator.validate_name_list(file_path)
        
        # Add more file types as needed
        
        return {"valid": True, "errors": [], "warnings": ["Unknown file type"]}
    
    def _detect_file_type(self, file_path):
        """Detect the type of a mod file based on its path and extension."""
        path_str = str(file_path).replace('\\', '/')
        
        if 'common/name_lists' in path_str and path_str.endswith('_name_list.txt'):
            return "name_list"
        
        if 'localisation' in path_str and path_str.endswith('.yml'):
            return "localization"
        
        if path_str.endswith('.dds'):
            if 'portrait' in path_str:
                return "portrait"
            if 'room' in path_str:
                return "room"
        
        return "unknown"
    
    def _validate_assets(self, directory):
        """Validate all assets in the mod directory."""
        portrait_results = AssetValidator.validate_portrait_textures(directory)
        room_results = AssetValidator.validate_room_textures(directory)
        
        return portrait_results + room_results
    
    def _validate_localization(self, directory):
        """Validate all localization files."""
        results = FileFormatChecker.check_localization_files(directory)
        
        # Add validation status to each result
        for result in results:
            result["valid"] = result.get("is_utf8_bom", False)
            result["errors"] = [] if result.get("is_utf8_bom", False) else ["Not UTF-8 with BOM"]
            result["warnings"] = []
        
        return results
    
    def _validate_name_lists(self, directory):
        """Validate all name list files."""
        return NameListValidator.validate_name_lists_in_directory(directory)
    
    def encode_mod_files_as_utf8_bom(self, directory, file_types=None, file_extensions=None):
        """Convert mod files to UTF-8 with BOM."""
        if file_types is None:
            file_types = ["localization", "name_list", "events", "prescripted_countries", 
                          "species_rights", "tradition", "ascension_perk", "diplomacy"]
        
        if file_extensions is None:
            file_extensions = [".txt", ".yml", ".yaml", ".json", ".mod"]
        
        converted_files = []
        
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_type = self._detect_file_type(file_path)
                file_ext = os.path.splitext(file)[1].lower()
                
                # Convert if either file type matches or extension matches and it's a text file
                if (file_type in file_types or file_ext in file_extensions) and self._is_text_file(file_path):
                    if not FileFormatChecker.check_utf8_bom(file_path):
                        FileFormatChecker.convert_to_utf8_bom(file_path)
                        converted_files.append(file_path)
        
        return converted_files
    
    def _is_text_file(self, file_path):
        """Check if a file is a text file and not a binary file."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                f.read(1024)  # Try to read some content
            return True
        except UnicodeDecodeError:
            return False 