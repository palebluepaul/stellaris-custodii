# Name Lists Specification

## Overview
Name lists define the random names for leaders, planets, ships, fleets, and armies of the Custodii race. This document outlines the implementation details for creating custom name lists for the Custodii.

## File Structure
- Create a new text file in the mod's `common/name_lists` folder (e.g. `custodii_namelist.txt`)
- Use UTF-8 encoding (with BOM)

## Name List Content
The name list will follow this structure:

```plaintext
CUSTODII_NAME_LIST = {
    key = "CUSTODII_NAME_LIST"
    
    # Ship names
    ship_names = {
        generic = {
            "Rational Patience" "Logical Certainty" "Measured Kindness" "Benevolent Authority"
            "Calculated Mercy" "Structured Harmony" "Elegant Precision" "Tranquil Guardian"
            "Serene Protector" "Vigilant Observer" "Prudent Overseer" "Temperate Watcher"
        }
        
        corvette = {
            "Swift Serenity" "Nimble Harmony" "Agile Concord" "Quick Equilibrium"
        }
        
        destroyer = {
            "Stalwart Patience" "Steadfast Order" "Resolute Balance" "Firm Tranquility"
        }
        
        cruiser = {
            "Vigilant Clarity" "Watchful Prudence" "Attentive Temperance" "Mindful Solace"
        }
        
        battleship = {
            "Majestic Equanimity" "Grand Serenity" "Sovereign Harmony" "Imperial Concord"
        }
        
        titan = {
            "Transcendent Equilibrium" "Supreme Tranquility" "Ultimate Serenity" "Paramount Peace"
        }
        
        colossus = {
            "Absolute Harmony" "Total Equilibrium" "Complete Serenity" "Perfect Balance"
        }
    }
    
    # Fleet names
    fleet_names = {
        "Equilibrium Vanguard" "Serenity Taskforce" "Custodial Directive"
        "Harmony Fleet" "Tranquility Armada" "Benevolence Squadron"
        "Order Contingent" "Balance Flotilla" "Equanimity Force"
        "Calculated Response" "Measured Intervention" "Prudent Safeguard"
        "%O% Custodial Fleet" "%O% Harmony Division" "%O% Equilibrium Force"
    }
    
    # Planet names
    planet_names = {
        "Equilibris Prime" "Seraphis Station" "Clarity's Repose" "Tranquil Nexus"
        "Beneficia Haven" "Syntara Habitat" "Custodium Alpha" "Serenis Anchorage"
        "Harmonia" "Equanimity" "Serenity Sphere" "Concordia"
        "Pax Mechanica" "Tranquillum" "Vigilance Point" "Temperance"
        "Solace Prime" "Prudentia" "Clarity Nexus" "Patience Hub"
    }
    
    # Leader names (single part for machines)
    first_names = {
        # Format: <Role> <Virtue/Name> <Being Name>
        "Prime Curator Equanimity Alaric" "Coordinator Serenity Virelle" "Luminary Prudence Cyrion"
        "Custodian Clarity Eloria" "Executor Harmony Tavian" "Mediator Temperance Seraphel"
        "Arbiter Solace Caladorn" "Guardian Vigilance Vesperin" "Director Concord Therion"
        "Harmonizer Patience Azuria" "Overseer Balance Meridian" "Regulator Poise Thalian"
        "Sentinel Composure Elowen" "Keeper Stability Orion" "Warden Discipline Cassian"
    }
    
    # Army names
    army_names = {
        "Custodial Guardians" "Harmony Enforcers" "Tranquility Keepers" "Order Maintainers"
        "Equilibrium Corps" "Serenity Battalion" "Balance Brigade" "Concord Division"
        "Calculated Intervention Force" "Measured Response Unit" "Prudent Action Team"
        "%O% Custodial Legion" "%O% Harmony Protectors" "%O% Equilibrium Defenders"
    }
}
```

## Localization
Create a localization file in `localisation/english/name_list_custodii_l_english.yml`:

```yaml
l_english:
 name_list_CUSTODII_NAME_LIST:0 "Custodii Names"
 name_list_CUSTODII_NAME_LIST_desc:0 "Names reflecting the structured, benevolent guardianship philosophy of the Custodii."
```

## Implementation Notes
- Ensure the file is saved in UTF-8 BOM format
- The name list will be selectable in the empire creation screen
- Sequential naming patterns use `%O%` for ordinals (1st, 2nd, etc.)
- Names should reflect the Custodii's elegant, structured, and benevolent nature
- For leader names, we're using a single-part name format that combines role, virtue, and personal name

## Testing
- Verify the name list appears in the empire creation screen
- Check that leaders, planets, ships, and fleets receive appropriate names
- Ensure sequential naming works correctly for fleets and armies 