#!/usr/bin/env python3
import os
import sys
import anthropic
import re

# Get API key from environment variables
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("ANTHROPIC_API_KEY not found in environment variables")
    sys.exit(1)

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=api_key)

# Path to the briefing document
briefing_file_path = "source_material/custodii_briefing.md"
# Path to the asset file
asset_file_path = "mod/sound/custodii-advisor.asset"

# Check if files exist
if not os.path.exists(briefing_file_path):
    print(f"Briefing file not found: {briefing_file_path}")
    sys.exit(1)

if not os.path.exists(asset_file_path):
    print(f"Asset file not found: {asset_file_path}")
    sys.exit(1)

# Read the briefing document
try:
    with open(briefing_file_path, "r") as f:
        briefing_content = f.read()
except Exception as e:
    print(f"Error reading briefing file: {e}")
    sys.exit(1)

def find_sound_effect_comments(file_path, sound_effect_name):
    """
    Find the comments for a specific sound effect in the asset file.
    Returns the raw comment text.
    """
    try:
        with open(file_path, "r") as f:
            content = f.read()
        
        # Find the specific sound effect block
        # Look for pattern: comments followed by soundeffect = { name = sound_effect_name
        pattern = r'((?:#[^\n]*\n)+)\s*soundeffect\s*=\s*{\s*\n\s*name\s*=\s*' + re.escape(sound_effect_name) + r'\s*\n'
        match = re.search(pattern, content)
        
        if match:
            # Extract the comments
            comments_block = match.group(1)
            # Clean up the comments
            comment_lines = []
            for line in comments_block.split('\n'):
                line = line.strip()
                if line.startswith('#'):
                    comment_lines.append(line.strip('# \t'))
            
            return "\n".join(filter(None, comment_lines))
        
        # If not found with the pattern above, try a more direct approach
        blocks = content.split('soundeffect = {')
        for i, block in enumerate(blocks[1:], 1):  # Skip the first split which is before any soundeffect
            if f'name = {sound_effect_name}' in block:
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
                
                if comment_lines:
                    return "\n".join(comment_lines)
        
        print(f"No comments found for {sound_effect_name}. Searching for similar sound effects...")
        # If we can't find an exact match, try to find sound effects with similar names
        similar_effects = []
        for pattern in [
            r'name\s*=\s*(\S*' + re.escape(sound_effect_name) + r'\S*)',  # Contains the name
            r'name\s*=\s*(\S*' + re.escape(sound_effect_name.split('_')[0]) + r'.*?' + re.escape(sound_effect_name.split('_')[-1]) + r'\S*)'  # Contains first and last part
        ]:
            matches = re.findall(pattern, content)
            similar_effects.extend(matches)
        
        if similar_effects:
            print(f"Found similar sound effects: {similar_effects}")
            print(f"Try using one of these exact names instead.")
        
        return ""
    except Exception as e:
        print(f"Error reading asset file: {e}")
        return ""

def generate_prompt(sound_effect_name, comment_text):
    """
    Generate a prompt for the Anthropic API based on the soundeffect information.
    """
    prompt = f"""You are writing voice lines for the Custodii advisor in the game Stellaris. 
    
Sound Effect: {sound_effect_name}
Comments: {comment_text}

Using the Custodii empire briefing below as reference, write 10 distinct voice lines for this sound effect.
Each voice line should be concise, match the tone described in the briefing, and follow any guidelines in the comments.
The lines should feel like notifications or comments from an AI advisor to the player during gameplay.

Format your response EXACTLY as follows, with the sound name followed by the line number and a colon, then the line in quotes:
{sound_effect_name}_01: "First voice line"
{sound_effect_name}_02: "Second voice line"
{sound_effect_name}_03: "Third voice line"
...and so on until {sound_effect_name}_10.

Do not add any extra line breaks or spacing between lines.

CUSTODII BRIEFING:
{briefing_content}
"""
    return prompt

def generate_voice_lines(sound_effect_name, comment_text):
    """
    Generate voice lines for a given sound effect using the Anthropic API.
    Returns a string of 10 voice lines.
    """
    prompt = generate_prompt(sound_effect_name, comment_text)
    
    try:
        print("Calling Anthropic API...")
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
        print(f"Error generating voice lines: {e}")
        return ""

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_single_line.py <sound_effect_name> [custom_comment_text]")
        print("Example: python generate_single_line.py advisor_notification_colony_established 'Played when a new colony is established. Frequency: Common - can be moderate length'")
        sys.exit(1)
    
    sound_effect_name = sys.argv[1]
    
    # Use custom comment text if provided, otherwise get from asset file
    if len(sys.argv) > 2:
        comment_text = sys.argv[2]
    else:
        comment_text = find_sound_effect_comments(asset_file_path, sound_effect_name)
        if not comment_text:
            print(f"Warning: No comments found for {sound_effect_name} in the asset file.")
            sys.exit(1)
    
    print(f"Generating voice lines for {sound_effect_name}")
    print(f"Comments: {comment_text}")
    
    voice_lines = generate_voice_lines(sound_effect_name, comment_text)
    if voice_lines:
        print("\nGenerated Voice Lines:")
        print("----------------------")
        print(voice_lines)

if __name__ == "__main__":
    main() 