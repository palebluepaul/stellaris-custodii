#!/usr/bin/env python3

def extract_advisor_name(line):
    """Extract the advisor name from a line of error text."""
    start = line.find("'advisor_")
    if start == -1:
        return ""
    
    end = line.find("'", start + 1)
    if end == -1:
        return ""
    
    return line[start+1:end]

def main():
    # Read the input file
    with open('output/working/errors.txt', 'r') as file:
        lines = file.readlines()
    
    # Sort the lines by the advisor name
    sorted_lines = sorted(lines, key=extract_advisor_name)
    
    # Write the sorted lines to a new file
    with open('output/working/sorted_errors.txt', 'w') as file:
        file.writelines(sorted_lines)
    
    print(f"Sorted {len(sorted_lines)} lines and saved to output/working/sorted_errors.txt")

if __name__ == "__main__":
    main() 