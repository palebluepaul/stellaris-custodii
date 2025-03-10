#!/usr/bin/env python3
"""
Generate voice files for Custodii advisor voice line variants using the ElevenLabs API.

This script reads the voice line variants from a file and generates a WAV file for each variant
using the ElevenLabs API. The voice files are saved in the specified output directory.

Usage:
    python generate_voice_files.py [--input INPUT] [--output OUTPUT] [--batch-size BATCH_SIZE]

Arguments:
    --input: Path to the input voice variants file (default: ../mod/sound/custodii_voice_variants.txt)
    --output: Path to the output directory for voice files (default: ../mod/sound/voice)
    --batch-size: Number of voice lines to process in each batch (default: 10)
    --test: Only process a few lines for testing (default: False)
    --single-key: Process only a single voice line with the specified key
"""

import os
import re
import time
import argparse
import logging
import tempfile
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import wave
import io

# Import ElevenLabs API
from elevenlabs.client import ElevenLabs
from elevenlabs import save

# Constants
DEFAULT_INPUT_PATH = "../mod/sound/custodii_voice_variants.txt"
DEFAULT_OUTPUT_PATH = "../mod/sound/voice"
DEFAULT_BATCH_SIZE = 10
VOICE_ID = "gcgATH9maP3HG8oRh9Pn"  # The specified voice ID
MODEL_ID = "eleven_multilingual_v2"  # The specified model
OUTPUT_FORMAT = "mp3_44100_128"  # Valid output format for ElevenLabs API

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def read_voice_variants(file_path: str) -> Dict[str, str]:
    """Read voice line variants from the specified file."""
    variants = {}
    current_key = None
    
    logger.info(f"Reading voice variants from {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
            
            # Parse the line to extract key and text
            match = re.match(r'([^:]+):\s*"([^"]+)"', line)
            if match:
                key = match.group(1).strip()
                text = match.group(2).strip()
                variants[key] = text
    
    logger.info(f"Found {len(variants)} voice variants")
    return variants

def batch_variants(variants: Dict[str, str], batch_size: int) -> List[Dict[str, str]]:
    """Split the variants into batches."""
    items = list(variants.items())
    return [dict(items[i:i + batch_size]) for i in range(0, len(items), batch_size)]

def ensure_output_directory(output_dir: str) -> None:
    """Ensure the output directory exists."""
    os.makedirs(output_dir, exist_ok=True)
    logger.info(f"Output directory: {output_dir}")

def generate_voice_files(
    client: ElevenLabs,
    variants: Dict[str, str],
    output_dir: str,
    test_mode: bool = False
) -> None:
    """Generate voice files for each variant."""
    ensure_output_directory(output_dir)
    
    # If in test mode, only process a few variants
    if test_mode:
        logger.info("Running in test mode - only processing a few variants")
        items = list(variants.items())[:3]  # Process only 3 variants in test mode
        variants = dict(items)
    
    total = len(variants)
    processed = 0
    errors = 0
    
    for key, text in variants.items():
        output_file = os.path.join(output_dir, f"{key}.mp3")
        
        # Skip if file already exists
        if os.path.exists(output_file):
            logger.info(f"File already exists, skipping: {output_file}")
            processed += 1
            continue
        
        try:
            logger.info(f"Generating voice for: {key}")
            logger.info(f"Text: {text}")
            
            # Generate audio using ElevenLabs API
            audio = client.text_to_speech.convert(
                text=text,
                voice_id=VOICE_ID,
                model_id=MODEL_ID,
                output_format=OUTPUT_FORMAT
            )
            
            # Collect audio data
            audio_data = b''
            if hasattr(audio, '__iter__') and not isinstance(audio, (bytes, bytearray)):
                for chunk in audio:
                    audio_data += chunk
            else:
                audio_data = audio
            
            # Verify we have audio data
            if not audio_data or len(audio_data) == 0:
                logger.error(f"Received empty audio data for {key}, skipping")
                errors += 1
                continue
            
            # Save the MP3 data directly to the output file
            with open(output_file, 'wb') as f:
                f.write(audio_data)
            
            logger.info(f"Saved to: {output_file}")
            
            # Add a small delay to avoid rate limiting
            time.sleep(0.5)
            
        except Exception as e:
            logger.error(f"Error generating voice for {key}: {e}")
            # Remove the output file if it was created but is empty or corrupted
            if os.path.exists(output_file) and (os.path.getsize(output_file) == 0):
                logger.info(f"Removing empty file: {output_file}")
                os.remove(output_file)
            errors += 1
        
        processed += 1
        logger.info(f"Progress: {processed}/{total} ({(processed/total)*100:.1f}%)")
    
    logger.info(f"Completed: {processed} variants processed, {errors} errors")

def process_single_key(
    client: ElevenLabs,
    variants: Dict[str, str],
    output_dir: str,
    key: str
) -> None:
    """Process a single voice line by key."""
    ensure_output_directory(output_dir)
    
    if key not in variants:
        logger.error(f"Key not found: {key}")
        logger.info(f"Available keys: {', '.join(list(variants.keys())[:10])}...")
        return
    
    text = variants[key]
    output_file = os.path.join(output_dir, f"{key}.mp3")
    
    logger.info(f"Processing single key: {key}")
    logger.info(f"Text: {text}")
    
    try:
        # Generate audio using ElevenLabs API
        audio = client.text_to_speech.convert(
            text=text,
            voice_id=VOICE_ID,
            model_id=MODEL_ID,
            output_format=OUTPUT_FORMAT
        )
        
        # Collect audio data
        audio_data = b''
        if hasattr(audio, '__iter__') and not isinstance(audio, (bytes, bytearray)):
            for chunk in audio:
                audio_data += chunk
        else:
            audio_data = audio
        
        # Verify we have audio data
        if not audio_data or len(audio_data) == 0:
            logger.error(f"Received empty audio data for {key}, skipping")
            return
        
        # Save the MP3 data directly to the output file
        with open(output_file, 'wb') as f:
            f.write(audio_data)
        
        logger.info(f"Successfully generated voice file: {output_file}")
        
    except Exception as e:
        logger.error(f"Error generating voice for {key}: {e}")
        # Remove the output file if it was created but is empty or corrupted
        if os.path.exists(output_file) and (os.path.getsize(output_file) == 0):
            logger.info(f"Removing empty file: {output_file}")
            os.remove(output_file)

def main():
    parser = argparse.ArgumentParser(description='Generate voice files for Custodii advisor voice line variants.')
    parser.add_argument('--input', default=DEFAULT_INPUT_PATH, help='Path to the input voice variants file')
    parser.add_argument('--output', default=DEFAULT_OUTPUT_PATH, help='Path to the output directory for voice files')
    parser.add_argument('--batch-size', type=int, default=DEFAULT_BATCH_SIZE, help='Number of voice lines to process in each batch')
    parser.add_argument('--test', action='store_true', help='Only process a few lines for testing')
    parser.add_argument('--single-key', help='Process only a single voice line with the specified key')
    args = parser.parse_args()
    
    # Check if the input file exists
    if not os.path.exists(args.input):
        logger.error(f"Input file not found: {args.input}")
        return
    
    # Initialize ElevenLabs client
    # The API key is expected to be in the environment
    try:
        client = ElevenLabs()
        logger.info("ElevenLabs client initialized")
    except Exception as e:
        logger.error(f"Failed to initialize ElevenLabs client: {e}")
        logger.error("Make sure ELEVENLABS_API_KEY is set in your environment")
        return
    
    # Read voice variants
    variants = read_voice_variants(args.input)
    
    # Process a single key if specified
    if args.single_key:
        process_single_key(client, variants, args.output, args.single_key)
        return
    
    # Process variants in batches
    batches = batch_variants(variants, args.batch_size)
    logger.info(f"Processing {len(variants)} variants in {len(batches)} batches")
    
    for i, batch in enumerate(batches):
        logger.info(f"Processing batch {i+1}/{len(batches)}")
        generate_voice_files(client, batch, args.output, args.test)
        
        # Add a delay between batches to avoid rate limiting
        if i < len(batches) - 1:
            logger.info("Waiting before processing next batch...")
            time.sleep(2)
    
    logger.info("Voice file generation complete")

if __name__ == "__main__":
    main() 