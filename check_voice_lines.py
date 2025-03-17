import os
import re
import glob

# Directory containing the voice line files
voice_files_dir = 'output_working'

# Patterns to look for
ship_name_patterns = [
    r'SS \w+',       # Ship names like "SS Inquiry"
    r'USS \w+',      # Federation style names
    r'the \w+ ship',  # References like "the Discovery ship"
    r'vessel \w+',   # "vessel Discovery"
]

leader_name_patterns = [
    r'Admiral \w+',    # Admiral names
    r'Captain \w+',    # Captain names
    r'Commander \w+',  # Commander names
    r'Governor \w+',   # Governor names
    r'Emperor \w+',    # Emperor names
    r'Professor \w+',  # Professor names
    r'Dr\. \w+',       # Doctor names
]

# Combine all patterns
all_patterns = ship_name_patterns + leader_name_patterns

def check_file(file_path):
    problematic_lines = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.strip().split('\n')
        
        for line in lines:
            for pattern in all_patterns:
                matches = re.findall(pattern, line)
                if matches:
                    problematic_lines.append((line, matches))
    
    return problematic_lines

def main():
    print("Checking voice files for ship names and leader names...")
    
    # Get all text files in the directory
    files = glob.glob(os.path.join(voice_files_dir, '*.txt'))
    
    files_with_issues = 0
    total_issues = 0
    
    for file_path in files:
        problematic_lines = check_file(file_path)
        
        if problematic_lines:
            files_with_issues += 1
            total_issues += len(problematic_lines)
            
            print(f"\nIssues found in {os.path.basename(file_path)}:")
            for line, matches in problematic_lines:
                print(f"  - {line}")
                print(f"    Matches: {', '.join(matches)}")
    
    print(f"\nSummary: Found {total_issues} issues in {files_with_issues} files out of {len(files)} total files.")

if __name__ == "__main__":
    main() 