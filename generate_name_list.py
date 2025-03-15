#!/usr/bin/env python3
import os
import sys
import shutil
import argparse
import re
from collections import defaultdict

def extract_race_name(filename):
    """Extract race name from briefing filename (e.g., 'custodii' from 'custodii_briefing.md')."""
    base_name = os.path.basename(filename)
    match = re.match(r'([^_]+)_briefing\.md', base_name)
    if match:
        return match.group(1)
    else:
        raise ValueError(f"Could not extract race name from filename: {filename}. Expected format is 'racename_briefing.md'")

def find_name_lists(content, race_name_upper):
    """Identify all sections in the template where names need to be generated."""
    lines = content.split('\n')
    sections = []
    current_path = []
    
    # Pattern to match lines with name lists (containing RACE_NAME pattern entries)
    name_list_pattern = re.compile(rf'{race_name_upper}_\w+')
    
    # Pattern to detect section starts
    section_start_pattern = re.compile(r'\s*(\w+)\s*=\s*\{')
    
    # Pattern to detect section ends
    section_end_pattern = re.compile(r'\s*\}')
    
    in_list = False
    
    for line in lines:
        # Track section hierarchy
        section_start = section_start_pattern.match(line)
        if section_start:
            section_name = section_start.group(1)
            current_path.append(section_name)
        
        # Check if line contains name entries
        if name_list_pattern.search(line) and not in_list:
            in_list = True
            # Use the last element in the current path as the tag
            if current_path:
                tag = current_path[-1]
                # Create section path (excluding the last element which is the tag)
                parent_path = " > ".join(current_path[:-1]) if len(current_path) > 1 else "root"
                sections.append({
                    'tag': tag,
                    'section': parent_path
                })
        elif in_list and not name_list_pattern.search(line):
            in_list = False
        
        section_end = section_end_pattern.match(line)
        if section_end and current_path:
            current_path.pop()
    
    return sections

def print_name_generation_info(sections):
    """Print information about each name list that needs to be generated."""
    for section in sections:
        print(f"Generate names for '{section['tag']}' list in section '{section['section']}'")

def write_name_lists_to_file(sections, output_file, race_name):
    """Write name list tags and sections to a file with description placeholders."""
    # Group sections by their parent categories
    categories = defaultdict(list)
    
    for section in sections:
        # Extract the top-level category from the section path
        path_parts = section['section'].split(' > ')
        if len(path_parts) > 1:
            category = path_parts[1]  # Index 1 should be ship_names, planet_names, etc.
        else:
            category = "Other"
        
        categories[category].append(section)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# Name List Tags for Race: {race_name}\n\n")
        
        # Write each category and its sections
        for category, category_sections in categories.items():
            f.write(f"## {category.title()}\n")
            
            for section in category_sections:
                tag = section['tag']
                section_path = section['section']
                f.write(f"- {tag} ({section_path}): [DESCRIPTION]\n")
            
            f.write("\n")
    
    print(f"Name list tags written to {output_file}")

def analyze_template_file(template_path, race_name, tag_file=None):
    """Analyze a template file and print name list information."""
    race_name_upper = race_name.upper()
    
    with open(template_path, 'r', encoding='utf-8') as template_file:
        content = template_file.read()
    
    # Find and print name lists
    content_with_race_name = content.replace("TEMPLATE_LIST", race_name_upper)
    sections = find_name_lists(content_with_race_name, race_name_upper)
    print(f"\nName lists in {template_path}:")
    print_name_generation_info(sections)
    
    # Write to file if specified
    if tag_file:
        write_name_lists_to_file(sections, tag_file, race_name)
    
    return sections

def process_file(template_path, output_path, race_name, overwrite=False):
    """Process a template file and replace placeholders with race name."""
    if os.path.exists(output_path) and not overwrite:
        print(f"Skipping {output_path} (already exists, use --overwrite to force)")
        return False
    
    race_name_upper = race_name.upper()
    
    with open(template_path, 'r', encoding='utf-8') as template_file:
        content = template_file.read()
    
    # Replace TEMPLATE and TEMPLATE_LIST with race name in uppercase
    content = content.replace("TEMPLATE_LIST", race_name_upper)
    content = content.replace("TEMPLATE", race_name_upper)
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(content)
    
    print(f"Created {output_path}")
    return True

def main():
    parser = argparse.ArgumentParser(description='Generate name lists for Stellaris races')
    parser.add_argument('briefing_file', help='Path to the race briefing file (e.g., custodii_briefing.md)')
    parser.add_argument('--output-dir', default='output', help='Directory to store generated files')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing files')
    parser.add_argument('--template-dir', default='source_material/templates', help='Directory containing template files')
    parser.add_argument('--print-info', action='store_true', help='Print information about name lists that need to be generated')
    parser.add_argument('--tag-file', help='Output file to write name list tags with description placeholders')
    
    args = parser.parse_args()
    
    # Check if briefing file exists
    if not os.path.isfile(args.briefing_file):
        print(f"Error: Briefing file not found: {args.briefing_file}")
        return 1
    
    # Extract race name from filename
    try:
        race_name = extract_race_name(args.briefing_file)
        print(f"Race name: {race_name}")
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    
    # If tag-file is not specified but print-info is true, set a default tag file
    tag_file = args.tag_file
    if args.print_info and not tag_file:
        tag_file = os.path.join(args.output_dir, f"{race_name}_name_tags.md")
    
    # Define template files and their output paths
    templates = [
        {
            'template': os.path.join(args.template_dir, 'template_name_list.txt'),
            'output': os.path.join(args.output_dir, f"{race_name}_name_list.txt")
        },
        {
            'template': os.path.join(args.template_dir, 'template_name_localisation.txt'),
            'output': os.path.join(args.output_dir, f"{race_name}_name_localisation.txt")
        }
    ]
    
    # Process each template file
    processed_count = 0
    all_sections = []
    
    for template_info in templates:
        if not os.path.isfile(template_info['template']):
            print(f"Warning: Template file not found: {template_info['template']}")
            continue
        
        # If print_info flag is set, analyze the template file first
        if args.print_info:
            sections = analyze_template_file(template_info['template'], race_name)
            all_sections.extend(sections)
        
        if process_file(template_info['template'], template_info['output'], race_name, args.overwrite):
            processed_count += 1
    
    # Write all sections to the tag file if specified
    if tag_file and all_sections:
        write_name_lists_to_file(all_sections, tag_file, race_name)
    
    print(f"Processed {processed_count} files.")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 