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
