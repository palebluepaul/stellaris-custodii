# Stellaris Name List Template

This repository contains a comprehensive template for creating custom name lists in Stellaris. The template includes all possible categories and sections that can be used in a name list, based on examination of vanilla game files and mod examples.

## File Structure

A complete name list implementation requires two files:

1. **Name List Definition File** (`common/name_lists/custodii_namelist.txt`): Contains the actual name list data.
2. **Localization File** (`localisation/english/name_list_custodii_l_english.yml`): Contains the display name and description for the name list.

## Important Notes

- Both files must be saved in **UTF-8 with BOM** encoding for the game to read them correctly.
- The localization file must have the correct key that matches the name list definition file.
- The `%O%` placeholder in sequential names is replaced with ordinal numbers (1st, 2nd, etc.).
- For machine empires, use `category = "Machine"` and `should_name_home_system_planets = no`.

## Name List Properties

- **key**: The unique identifier for the name list.
- **category**: The species category this name list belongs to (e.g., "Machine", "Mammalian", "Reptilian").
- **selectable**: Whether this name list can be selected in the empire creation screen.
- **randomized**: Whether this name list can be randomly assigned to AI empires.
- **should_name_home_system_planets**: Whether the game should automatically name home system planets.

## Name List Categories

The template includes the following categories:

### Ship Names
- **Generic**: Used for any ship class if a specific class is not defined.
- **Specific Ship Classes**: 
  - corvette
  - destroyer
  - cruiser
  - battleship
  - titan
  - colossus
  - juggernaut
  - transport
  - constructor
  - science
  - colonizer
  - sponsored_colonizer
- **Machine-specific Ship Classes**:
  - large_ship_ai
  - small_ship_ai

### Fleet Names
- **Random Names**: A list of unique fleet names.
- **Sequential Names**: A pattern for numbered fleets (e.g., "1st Fleet", "2nd Fleet").

### Planet Names
- **Generic**: Used for any planet class if a specific class is not defined.
- **Specific Planet Classes**: 
  - pc_continental
  - pc_desert
  - pc_arid
  - pc_tropical
  - pc_ocean
  - pc_tundra
  - pc_arctic
  - pc_savannah
  - pc_alpine
  - pc_nuked
  - pc_gaia
  - pc_ringworld_habitable
  - pc_habitat
  - pc_machine
  - pc_hive
  - pc_city
  - pc_relic
  - pc_toxic

### Character/Leader Names
- **Default**: The default naming scheme for the species.
  - **first_names**: For non-gendered species (like machines).
  - **first_names_male**: For male characters in gendered species.
  - **first_names_female**: For female characters in gendered species.
  - **second_names**: Last names or family names.
  - **full_names**: Complete names (for species that use full names directly).
  - **regnal_first_names**: Special first names for rulers.
  - **regnal_second_names**: Special last names for rulers.

### Ruler Names
- An alternative way to specify names specifically for rulers.
- Uses **full_names** to provide complete ruler names.

### Army Names
- **Generic**: Fallback for any army type not specifically defined.
- **Regular Army Types**:
  - defense_army
  - assault_army
  - slave_army
  - clone_army
  - robotic_army
  - android_army
  - psionic_army
  - xenomorph_army
  - gene_warrior_army
  - undead_army
- **Machine-specific Army Types**:
  - machine_defense
  - robotic_defense_army
- **Occupation Army Types**:
  - occupation_army
  - individual_machine_occupation_army
  - robotic_occupation_army
  - machine_occupation_army
- **Primitive Army Types**:
  - primitive_army
  - industrial_army
  - postatomic_army
- **Special Army Types**:
  - warpling_army

### Station Names
- **Resource Stations**:
  - mining_station
  - research_station
  - observation_station
- **Starbases by Level**:
  - starbase_outpost
  - starbase_starport
  - starbase_starhold
  - starbase_starfortress
  - starbase_citadel
- **Military Stations**:
  - military_station_small
  - military_station_medium
  - military_station_large
  - ion_cannon

### Asteroid Naming
- **asteroid_prefix**: Prefixes for asteroid names (e.g., "AST-", "MNR-").
- **asteroid_postfix**: Suffixes for asteroid names (e.g., "001", "Alpha").

## Usage

1. Copy the template files to your mod directory.
2. Rename the files and update the internal keys to match your mod's naming convention.
3. Replace the placeholder names with your custom names.
4. Save the files in UTF-8 with BOM encoding.
5. Test the name list in the game.

## Customization for Different Empire Types

### Machine Empires
- Set `category = "Machine"` at the top of the file.
- Set `should_name_home_system_planets = no` to prevent the game from automatically naming home system planets.
- Use `first_names` instead of gendered names.
- Include machine-specific army types like `machine_defense` and `robotic_defense_army`.

### Organic Empires
- Set `category` to the appropriate phenotype (e.g., "Mammalian", "Reptilian", etc.).
- Use gendered names with `first_names_male`, `first_names_female`, and `second_names`.

## Troubleshooting

- If the name list doesn't appear in the game, check that both files are saved in UTF-8 with BOM encoding.
- If sequential names show "%SEQ%" instead of numbers, check that the localization file is correctly set up.
- If the name list appears as "namelistXXXX", check that the localization file is in the correct directory and has the correct keys.
- If certain names aren't appearing in-game, make sure you've defined all the necessary categories for your empire type.

## References

- [Stellaris Wiki - Modding](https://stellaris.paradoxwikis.com/Modding)
- [Stellaris Name Lists Format](https://stellaris.paradoxwikis.com/Name_lists) 