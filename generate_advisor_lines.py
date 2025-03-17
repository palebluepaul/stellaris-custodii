#!/usr/bin/env python3
import os
import re
import json
import time
import anthropic

# Initialize Anthropic client with API key from environment
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

client = anthropic.Anthropic(api_key=api_key)

# Create output directory if it doesn't exist
output_dir = "output_working"
os.makedirs(output_dir, exist_ok=True)

# Path to the custodii-advisor.asset file
asset_file_path = "mod/sound/custodii-advisor.asset"

# Path to the briefing document
briefing_file_path = "source_material/custodii_briefing.md"

# Check if files exist
if not os.path.exists(asset_file_path):
    raise FileNotFoundError(f"Asset file not found: {asset_file_path}")

if not os.path.exists(briefing_file_path):
    raise FileNotFoundError(f"Briefing file not found: {briefing_file_path}")

# Read the briefing document
try:
    with open(briefing_file_path, "r") as f:
        briefing_content = f.read()
except Exception as e:
    raise Exception(f"Error reading briefing file: {e}")

def parse_sound_effects(file_path):
    """
    Parse the custodii-advisor.asset file to extract soundeffects and their comments.
    Returns a list of dictionaries with 'name' and 'comments' keys.
    """
    try:
        with open(file_path, "r") as f:
            content = f.read()
    except Exception as e:
        raise Exception(f"Error reading asset file: {e}")
    
    sound_effects = []
    
    # Find all soundeffect blocks with their preceding comments
    # Pattern looks for comments followed by soundeffect declaration and name
    pattern = r'((?:#[^\n]*\n)+)\s*soundeffect\s*=\s*{\s*\n\s*name\s*=\s*([^\n]+)'
    
    for match in re.finditer(pattern, content):
        comments_block = match.group(1)
        sound_effect_name = match.group(2).strip()
        
        # Clean up the comments
        comment_lines = []
        for line in comments_block.split('\n'):
            line = line.strip()
            if line.startswith('#'):
                comment_lines.append(line.strip('# \t'))
        
        comments = "\n".join(filter(None, comment_lines))
        
        sound_effects.append({
            'name': sound_effect_name,
            'comments': comments
        })
    
    # If we didn't find any sound effects with the pattern above, fallback to the old method
    if not sound_effects:
        print("Warning: Using fallback method to parse sound effects")
        
        # Split content by soundeffect blocks
        blocks = content.split('soundeffect = {')
        
        for i, block in enumerate(blocks[1:], 1):  # Skip the first split
            # Extract name
            name_match = re.search(r'name\s*=\s*([^\n]+)', block)
            if not name_match:
                continue
            
            name = name_match.group(1).strip()
            
            # Look for comments before this block
            prev_block = blocks[i-1]
            comment_lines = []
            # Get the last few lines from the previous block which might be comments
            prev_lines = prev_block.split('\n')
            for line in reversed(prev_lines):
                line = line.strip()
                if line.startswith('#'):
                    comment_lines.insert(0, line.strip('# \t'))
                elif comment_lines:  # If we've found comments but now hit a non-comment line
                    break
            
            comments = "\n".join(comment_lines) if comment_lines else ""
            
            sound_effects.append({
                'name': name,
                'comments': comments
            })
    
    return sound_effects

def generate_prompt(sound_effect):
    """
    Generate a prompt for the Anthropic API based on the soundeffect information.
    """
    prompt = f"""You are writing voice lines for the Custodii advisor in the game Stellaris. 
    
Sound Effect: {sound_effect['name']}
Comments: {sound_effect['comments']}

Using the Custodii empire briefing below as reference, write 10 distinct voice lines for this sound effect.
Each voice line should be concise, match the tone described in the briefing, and follow any guidelines in the comments.
The lines should feel like notifications or comments from an AI advisor to the player during gameplay.

Format your response EXACTLY as follows, with the sound name followed by the line number and a colon, then the line in quotes:
{sound_effect['name']}_01: "First voice line"
{sound_effect['name']}_02: "Second voice line"
{sound_effect['name']}_03: "Third voice line"
...and so on until {sound_effect['name']}_10.

Do not add any extra line breaks or spacing between lines.

CUSTODII BRIEFING:
{briefing_content}
"""
    return prompt

def generate_voice_lines(sound_effect):
    """
    Generate voice lines for a given sound effect using the Anthropic API.
    Returns a string of 10 voice lines.
    """
    prompt = generate_prompt(sound_effect)
    
    try:
        response = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=1000,
            temperature=0.7,
            system="You are an expert game dialogue writer creating voice lines for a Stellaris advisor AI character.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Clean up the response by removing extra newlines
        text = response.content[0].text
        # Replace multiple newlines with a single newline
        text = re.sub(r'\n+', '\n', text)
        # Remove any leading/trailing whitespace
        text = text.strip()
        
        return text
    except Exception as e:
        print(f"Error generating voice lines for {sound_effect['name']}: {e}")
        return ""

def save_voice_lines(sound_effect_name, voice_lines):
    """
    Save voice lines to a file named after the sound effect.
    """
    # Clean the name for a valid filename
    clean_name = re.sub(r'[^\w\-_\.]', '_', sound_effect_name)
    file_name = f"{clean_name}.txt"
    file_path = os.path.join(output_dir, file_name)
    
    try:
        with open(file_path, "w") as f:
            f.write(voice_lines)
        
        print(f"Saved voice lines to {file_path}")
    except Exception as e:
        print(f"Error saving voice lines to {file_path}: {e}")

def main():
    try:
        # Parse the sound effects from the asset file
        sound_effects = parse_sound_effects(asset_file_path)
        
        if not sound_effects:
            print(f"No sound effects found in {asset_file_path}")
            return
        
        print(f"Found {len(sound_effects)} sound effects in {asset_file_path}")
        
        # Generate and save voice lines for each sound effect
        for i, sound_effect in enumerate(sound_effects):
            print(f"Generating voice lines for {sound_effect['name']} ({i+1}/{len(sound_effects)})")
            print(f"  Comments: {sound_effect['comments']}")
            
            voice_lines = generate_voice_lines(sound_effect)
            if voice_lines:
                save_voice_lines(sound_effect['name'], voice_lines)
            
            # Add a delay to avoid rate limiting
            if i < len(sound_effects) - 1:
                print("Waiting 2 seconds before next API call...")
                time.sleep(2)
        
        print(f"Voice line generation complete. Files saved to {output_dir}/")
    
    except Exception as e:
        print(f"Error in main function: {e}")

if __name__ == "__main__":
    main() 