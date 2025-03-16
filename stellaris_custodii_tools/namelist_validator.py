import os
import re
from pathlib import Path

class NameListValidator:
    """Validates name list files for Stellaris mods."""
    
    @staticmethod
    def validate_name_list(file_path):
        """Validate a name list file."""
        errors = []
        warnings = []
        
        # Check if file exists
        if not os.path.exists(file_path):
            errors.append(f"File not found: {file_path}")
            return {"valid": False, "errors": errors, "warnings": warnings}
        
        # Check encoding (must be UTF-8 with BOM)
        with open(file_path, 'rb') as f:
            raw = f.read(4)
            if not raw.startswith(b'\xef\xbb\xbf'):
                errors.append("File is not encoded as UTF-8 with BOM")
        
        # Read file content
        try:
            with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as f:
                content = f.read()
        except Exception as e:
            errors.append(f"Failed to read file: {str(e)}")
            return {"valid": False, "errors": errors, "warnings": warnings}
        
        # Check basic structure
        if not content.strip().startswith('{') and not content.strip().endswith('}'):
            errors.append("Name list file must be properly enclosed in curly braces")
        
        # Check for proper selectable syntax
        if "selectable = yes" in content:
            warnings.append("Found 'selectable = yes', should be 'selectable = { ... }' in a trigger block")
        
        # Check for proper randomized syntax
        if "randomized = yes" in content:
            warnings.append("Found 'randomized = yes', should be 'randomized = { ... }' in a trigger block")
        
        # Check for sequential name localization
        sequential_name_pattern = re.compile(r'(\w+)_SEQ')
        for match in sequential_name_pattern.finditer(content):
            # This won't actually check localization files but flags potential issues
            warnings.append(f"Sequential name {match.group(0)} may need localization")
        
        # Check for proper ship class definitions
        ship_classes = ["generic", "corvette", "destroyer", "cruiser", "battleship", 
                        "titan", "colossus", "juggernaut"]
        
        for ship_class in ship_classes:
            if f"{ship_class} = {{" not in content and f"{ship_class} ={{" not in content:
                warnings.append(f"Missing proper definition for ship class: {ship_class}")
        
        # Check for improper triggers
        trigger_pattern = re.compile(r'(\w+)\s+=\s+(yes|no)')
        for match in trigger_pattern.finditer(content):
            property_name = match.group(1)
            if property_name not in ["selectable", "randomized", "should_name_home_system_planets"]:
                warnings.append(f"Possible invalid trigger format: '{match.group(0)}', should be in trigger block")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    @staticmethod
    def validate_name_lists_in_directory(directory):
        """Validate all name list files in a directory."""
        results = []
        
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('_name_list.txt') and 'common/name_lists' in root.replace('\\', '/'):
                    file_path = os.path.join(root, file)
                    validation_result = NameListValidator.validate_name_list(file_path)
                    
                    results.append({
                        'path': file_path,
                        'valid': validation_result["valid"],
                        'errors': validation_result["errors"],
                        'warnings': validation_result["warnings"]
                    })
        
        return results 