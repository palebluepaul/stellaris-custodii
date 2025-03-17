# Custodii Advisor Voice Line Generator

This script generates voice lines for the Custodii advisor in Stellaris using the Anthropic Claude 3.7 Sonnet API.

## Prerequisites

- Python 3.6+
- An Anthropic API key (supplied through environment variables)

## Installation

1. Clone this repository
2. Install the required packages:

```bash
pip install anthropic
```

## Usage

The script expects the `ANTHROPIC_API_KEY` environment variable to be set, which can be done with Doppler or manually:

```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

Then run the script:

```bash
python generate_advisor_lines.py
```

The script will:
1. Parse the `mod/sound/custodii-advisor.asset` file to extract all sound effects and their comments
2. For each sound effect, generate 10 voice lines using Claude 3.7 Sonnet
3. Save each set of voice lines to a separate text file in the `output_working` directory

## Testing a Single Sound Effect

You can test generating lines for a single sound effect using:

```bash
python generate_single_line.py <sound_effect_name> [custom_comment_text]
```

If you don't provide custom comment text, the script will attempt to find the comments for that sound effect in the asset file.

Example:
```bash
python generate_single_line.py advisor_notification_colony_established
```

Or with custom comments:
```bash
python generate_single_line.py advisor_notification_colony_established "Played when a new colony is established. Frequency: Common - can be moderate length"
```

## Output

The output files will be named after the corresponding sound effects and will contain 10 voice lines each, formatted as:

```
sound_name_01: "First voice line"
sound_name_02: "Second voice line"
...
sound_name_10: "Tenth voice line"
```

This format makes it easy to directly use the lines for Stellaris sound effects.

## Customization

You can adjust the following parameters in the script:

- `temperature`: Controls the randomness of the generated voice lines (default: 0.7)
- `max_tokens`: Controls the maximum length of the generated voice lines (default: 1000)

## Notes

- The script includes a 2-second delay between API calls to avoid rate limiting
- The voice lines are generated based on the Custodii briefing document in `source_material/custodii_briefing.md` 