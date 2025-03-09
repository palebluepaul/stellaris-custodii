# Custodii Race Content Repository

This directory contains all the creative content for the Custodii race mod for Stellaris. The content is organized into separate directories by type, making it easy to find and update specific aspects of the Custodii lore and characteristics.

## Directory Structure

- **lore/**: Core information about the Custodii race, their ethics, and their society
- **names/**: Name lists for leaders, ships, planets, and other entities
- **dialogue/**: Dialogue samples, responses to events, and diplomatic text
- **visuals/**: Descriptions of visual elements like portraits, architecture, and ships
- **history/**: Historical events, notable figures, and timeline
- **science/**: Technology, research, and scientific approach
- **personalities/**: AI personalities, traits, and behavioral patterns

## File Format

Most content is stored in JSON format for easy parsing and integration into the mod. Each JSON file includes metadata such as:

- `id`: Unique identifier for the content
- `name`: Human-readable name
- `description`: Brief description of the content
- `content`: The actual content data
- `tags`: Keywords for categorization and searching
- `created`: Creation timestamp
- `updated`: Last update timestamp

## Usage

This content repository serves as the single source of truth for all creative aspects of the Custodii race. When implementing the mod, developers should reference this content rather than hardcoding values directly into mod files.

## Contributing

When adding or modifying content, please follow these guidelines:

1. Use the appropriate directory for the content type
2. Follow the established JSON schema for each content type
3. Update the `updated` timestamp when modifying existing content
4. Ensure all content is consistent with the established Custodii lore and characteristics 