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
