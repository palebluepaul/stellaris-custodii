#!/usr/bin/env python3
"""
Utility script to create a snapshot of all Custodii content files.
The snapshot will include the README at the top, followed by all content files
with clear file name headers.
"""

import os
import json
import datetime
import shutil
from pathlib import Path

def create_snapshot():
    """Create a timestamped snapshot of all content files."""
    # Create snapshot directory if it doesn't exist
    snapshot_dir = Path("content/snapshots")
    snapshot_dir.mkdir(exist_ok=True, parents=True)
    
    # Generate timestamp for the snapshot filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    snapshot_file = snapshot_dir / f"custodii_content_snapshot_{timestamp}.md"
    
    # Start with the README
    readme_path = Path("content/README.md")
    content = []
    
    if readme_path.exists():
        with open(readme_path, "r") as f:
            readme_content = f.read()
            content.append("# CUSTODII CONTENT SNAPSHOT\n")
            content.append(f"*Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
            content.append("## README\n\n")
            content.append(readme_content)
            content.append("\n\n" + "=" * 80 + "\n\n")
    
    # Get all content files
    content_files = []
    for root, _, files in os.walk("content"):
        for file in files:
            if file.endswith(".json") or file.endswith(".md"):
                if "snapshots" not in root and file != "README.md":  # Skip snapshots and README
                    content_files.append(os.path.join(root, file))
    
    # Sort content files for consistent order
    content_files.sort()
    
    # Process each content file
    for file_path in content_files:
        rel_path = os.path.relpath(file_path, ".")
        content.append(f"## FILE: {rel_path}\n\n")
        
        with open(file_path, "r") as f:
            file_content = f.read()
            
            # For JSON files, try to pretty-print them
            if file_path.endswith(".json"):
                try:
                    json_data = json.loads(file_content)
                    file_content = json.dumps(json_data, indent=2)
                except json.JSONDecodeError:
                    # If JSON parsing fails, use the original content
                    pass
            
            content.append("```\n")
            content.append(file_content)
            content.append("\n```\n\n")
            content.append("-" * 80 + "\n\n")
    
    # Write the snapshot file
    with open(snapshot_file, "w") as f:
        f.write("\n".join(content))
    
    print(f"Snapshot created: {snapshot_file}")
    return snapshot_file

if __name__ == "__main__":
    snapshot_file = create_snapshot() 