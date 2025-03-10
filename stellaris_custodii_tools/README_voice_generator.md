# Custodii Voice Line Variant Generator

This tool generates shorter variants (3-6 words) for the Custodii advisor voice lines using the Anthropic API with Claude 3.7 Sonnet.

## Prerequisites

- Python 3.6+
- Anthropic API key
- [Doppler](https://www.doppler.com/) (recommended for managing API keys)

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Set up your Anthropic API key:

   - Using Doppler (recommended):
     ```bash
     doppler setup
     ```
     Then add your Anthropic API key to your Doppler project.

   - Or set it directly as an environment variable:
     ```bash
     export ANTHROPIC_API_KEY=your_api_key_here
     ```

## Usage

### Basic Usage

```bash
# Using Doppler to inject the API key
doppler run -- python generate_voice_variants.py

# Or directly if you've set the environment variable
python generate_voice_variants.py
```

### Command-Line Options

- `--input`: Path to the input voice lines file (default: `../mod/sound/custodii_voice_lines.txt`)
- `--output`: Path to the output variants file (default: `../mod/sound/custodii_voice_variants.txt`)
- `--briefing`: Path to the Custodii briefing file (default: `../source_material/custodii_briefing.md`)
- `--batch-size`: Number of voice lines to process in each batch (default: 10)
- `--variants`: Number of variants to generate for each voice line (default: 10)

### Examples

Process all voice lines in batches of 5, generating 10 variants for each:

```bash
doppler run -- python generate_voice_variants.py --batch-size 5 --variants 10
```

Process only a specific section of voice lines:

```bash
# Create a temporary file with just the generic phrases
grep -A 10 "GENERIC PHRASES" ../mod/sound/custodii_voice_lines.txt > /tmp/generic_phrases.txt

# Process only those lines
doppler run -- python generate_voice_variants.py --input /tmp/generic_phrases.txt --output ../mod/sound/generic_phrases_variants.txt
```

## Output Format

The output file contains the generated variants in the following format:

```
# Original: advisor_generic_phrase_custodii_01
advisor_generic_phrase_custodii_01_variant_01: "Guardianship is our privilege."
advisor_generic_phrase_custodii_01_variant_02: "Structured protection is paramount."
...
```

# Custodii Voice File Generator

This tool generates WAV audio files for the Custodii advisor voice line variants using the ElevenLabs API.

## Prerequisites

- Python 3.6+
- ElevenLabs API key
- [Doppler](https://www.doppler.com/) (recommended for managing API keys)

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Set up your ElevenLabs API key:

   - Using Doppler (recommended):
     ```bash
     doppler setup
     ```
     Then add your ElevenLabs API key to your Doppler project as `ELEVENLABS_API_KEY`.

   - Or set it directly as an environment variable:
     ```bash
     export ELEVENLABS_API_KEY=your_api_key_here
     ```

## Usage

### Basic Usage

```bash
# Using Doppler to inject the API key
doppler run -- python generate_voice_files.py

# Or directly if you've set the environment variable
python generate_voice_files.py
```

### Command-Line Options

- `--input`: Path to the input voice variants file (default: `../mod/sound/custodii_voice_variants.txt`)
- `--output`: Path to the output directory for voice files (default: `../mod/sound/voice`)
- `--batch-size`: Number of voice lines to process in each batch (default: 10)
- `--test`: Only process a few lines for testing (default: False)

### Examples

Process all voice lines in batches of 5:

```bash
doppler run -- python generate_voice_files.py --batch-size 5
```

Test the script with just a few voice lines:

```bash
doppler run -- python generate_voice_files.py --test
```

## Output Format

The script generates WAV files in the specified output directory. Each file is named after the corresponding voice line variant key:

```
advisor_generic_phrase_custodii_01_variant_01.wav
advisor_generic_phrase_custodii_01_variant_02.wav
...
```

## Tips for Voice Recording

When using the generated voice files:

1. Listen to each file to ensure the quality and pronunciation are correct
2. Adjust the volume levels if necessary
3. Consider post-processing the files for better in-game integration
4. Update the asset files to point to the generated voice files

## Troubleshooting

- **API Key Issues**: Make sure your ElevenLabs API key is correctly set up in Doppler or as an environment variable.
- **Rate Limiting**: The script includes delays between API calls to avoid rate limiting. If you encounter rate limiting errors, try reducing the batch size or increasing the delay.
- **File Format Issues**: If the generated WAV files don't work in the game, you may need to convert them to a different format or adjust the audio parameters.

## License

This tool is part of the Custodii Race Mod for Stellaris and is subject to the same license terms. 