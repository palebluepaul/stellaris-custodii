#!/usr/bin/env python3

import os
import sys
import re
import requests
import tempfile
from pathlib import Path
import argparse
from pydub import AudioSegment

# ElevenLabs API configuration
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
VOICE_ID = "gcgATH9maP3HG8oRh9Pn"
MODEL_ID = "eleven_multilingual_v2"

# Paths configuration
INPUT_DIR = "output_working"
TEMP_DIR = "temp_audio"
OUTPUT_DIR = "mod/sound/vo/custodii-advisor"

def ensure_directories_exist():
    """Ensure all required directories exist"""
    os.makedirs(TEMP_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def parse_voice_lines(file_path):
    """Extract voice line IDs and text from a file"""
    voice_lines = {}
    with open(file_path, 'r') as f:
        for line in f:
            # Match patterns like 'line_id: "text content"'
            match = re.match(r'([^:]+):\s*"([^"]+)"', line.strip())
            if match:
                line_id = match.group(1).strip()
                text = match.group(2).strip()
                voice_lines[line_id] = text
    return voice_lines

def generate_voice(text, output_path):
    """Generate voice using ElevenLabs API"""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    data = {
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
        return True
    else:
        print(f"Error generating voice: {response.status_code}, {response.text}")
        return False

def convert_mp3_to_wav(mp3_path, wav_path):
    """Convert MP3 to WAV with PCM 16 44.1kHz format"""
    audio = AudioSegment.from_mp3(mp3_path)
    audio = audio.set_frame_rate(44100).set_channels(1).set_sample_width(2)
    audio.export(wav_path, format="wav")

def process_file(file_path, test_mode=False, specific_line=None):
    """Process a single file containing voice lines"""
    print(f"Processing file: {file_path}")
    voice_lines = parse_voice_lines(file_path)
    
    if not voice_lines:
        print(f"No voice lines found in {file_path}")
        return
    
    file_name = os.path.basename(file_path)
    file_base = os.path.splitext(file_name)[0]
    
    # In test mode with a specific line, only process that one
    if test_mode and specific_line:
        if specific_line in voice_lines:
            process_voice_line(specific_line, voice_lines[specific_line], file_base)
        else:
            print(f"Line {specific_line} not found in {file_path}")
        return
    
    # In test mode without a specific line, process only the first line
    if test_mode:
        line_id = next(iter(voice_lines))
        process_voice_line(line_id, voice_lines[line_id], file_base)
        return
    
    # Process all lines in the file
    for line_id, text in voice_lines.items():
        process_voice_line(line_id, text, file_base)

def process_voice_line(line_id, text, file_base):
    """Process a single voice line"""
    print(f"Processing line: {line_id} - '{text}'")
    
    mp3_path = os.path.join(TEMP_DIR, f"{line_id}.mp3")
    wav_path = os.path.join(OUTPUT_DIR, f"{line_id}.wav")
    
    if generate_voice(text, mp3_path):
        print(f"Generated MP3: {mp3_path}")
        convert_mp3_to_wav(mp3_path, wav_path)
        print(f"Converted to WAV: {wav_path}")
    else:
        print(f"Failed to generate voice for {line_id}")

def main():
    parser = argparse.ArgumentParser(description="Generate voice lines for Stellaris mod")
    parser.add_argument("--test", action="store_true", help="Run in test mode (process only one line)")
    parser.add_argument("--file", help="Process a specific file")
    parser.add_argument("--line", help="Process a specific line (requires --file)")
    args = parser.parse_args()
    
    if not ELEVENLABS_API_KEY:
        print("Error: ELEVENLABS_API_KEY environment variable not set")
        print("Run with 'doppler run -- python voice_generator.py'")
        sys.exit(1)
    
    ensure_directories_exist()
    
    # Process a specific file
    if args.file:
        # Fix the path handling - don't add INPUT_DIR if the file already includes it
        if args.file.startswith(INPUT_DIR) or os.path.isabs(args.file):
            file_path = args.file
        else:
            file_path = os.path.join(INPUT_DIR, args.file)
            
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} not found")
            sys.exit(1)
        process_file(file_path, args.test, args.line)
        return
    
    # Process all files in the input directory
    for file_name in os.listdir(INPUT_DIR):
        if file_name.endswith(".txt"):
            file_path = os.path.join(INPUT_DIR, file_name)
            process_file(file_path, args.test)

if __name__ == "__main__":
    main() 