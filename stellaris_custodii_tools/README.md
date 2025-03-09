# Custodii Race Mod Tools

This package contains a set of Python tools to assist in the development and deployment of the Custodii Race mod for Stellaris.

## Features

- Cross-platform path resolution (Windows, macOS, WSL)
- Mod descriptor generation and validation
- File format checking for localization files
- Asset validation for textures
- Mod deployment to the game directory

## Installation

1. Clone the repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `config.json` file with your specific paths and settings. You can use the provided `config.json` as a template.

For macOS users, you'll need to update the paths in the configuration file to match your system.

## Usage

### Initialize Mod Structure

```bash
python custodii_tools.py init --name "Custodii Race" --id "custodii_race"
```

This will create the basic directory structure for the mod and generate the descriptor files.

### Generate Descriptor

```bash
python custodii_tools.py descriptor
```

This will generate or update the mod descriptor files.

### Check Localization Files

```bash
python custodii_tools.py check-format
```

To automatically fix format issues:

```bash
python custodii_tools.py check-format --fix
```

### Validate Assets

```bash
python custodii_tools.py validate --type portraits
```

Available types: `portraits`, `rooms`, `all`

### Deploy Mod

```bash
python custodii_tools.py deploy
```

To clean existing deployment before deploying:

```bash
python custodii_tools.py deploy --clean
```

## Development

The tools are organized into several modules:

- `path_resolver.py`: Handles cross-platform path resolution
- `mod_descriptor.py`: Generates and validates mod descriptor files
- `format_checker.py`: Checks and fixes file formats
- `asset_validator.py`: Validates game assets
- `deployment_helper.py`: Helps deploy the mod to the game directory
- `custodii_tools.py`: Main CLI tool

## License

This project is licensed under the MIT License. 