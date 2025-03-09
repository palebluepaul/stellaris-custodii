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
