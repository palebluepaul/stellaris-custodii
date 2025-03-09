# Event Responses Specification

## Overview
This specification outlines the implementation of custom event responses for the Custodii race. These modifications will ensure that event text and options reflect the Custodii's unique perspective as a sophisticated synthetic civilization dedicated to the structured, benevolent guardianship of organic life.

## Design Guidelines

### Tone and Style
- **Voice:** Elegant, structured, polite with gentle paternalistic authority
- **Perspective:** Logical, calculated, with subtle mechanical undertones
- **Themes:** Harmonic efficiency, calculated compassion, obligatory serenity, technocratic benevolence
- **Vocabulary:** Formal, precise terminology with occasional Victorian-inspired phrasing

### Event Categories to Modify

1. **Anomaly Events** - Scientific discoveries and unusual phenomena
2. **First Contact Events** - Initial interactions with other species
3. **Crisis Events** - Responses to major galactic threats
4. **Colony Events** - Planet-specific situations and developments
5. **Special Project Events** - Research and investigation outcomes
6. **Diplomatic Events** - Interactions with other empires

## Implementation Approach

### Method 1: Conditional Text in Existing Events
Add machine-specific or Custodii-specific text variants to existing events using trigger conditions.

```plaintext
# Example of conditional text in an event
event = {
    id = anomaly.1234
    title = "anomaly.1234.name"
    
    # Different descriptions based on empire type
    desc = {
        trigger = { 
            has_country_flag = custodii_empire
        }
        text = "anomaly.1234.desc.custodii"
    }
    desc = {
        trigger = { 
            is_machine_empire = yes
            NOT = { has_country_flag = custodii_empire }
        }
        text = "anomaly.1234.desc.machine"
    }
    desc = {
        trigger = { 
            is_machine_empire = no
        }
        text = "anomaly.1234.desc.default"
    }
    
    # Event options and effects...
}
```

### Method 2: Custom Options for Custodii
Add unique response options that only appear for Custodii empires, reflecting their unique perspective and capabilities.

```plaintext
# Example of custom options in an event
option = {
    name = "anomaly.1234.a.custodii"
    trigger = { has_country_flag = custodii_empire }
    
    # Custodii-specific effects
    add_resource = { unity = 50 }
    add_modifier = {
        modifier = "calculated_analysis"
        days = 180
    }
}
```

## File Structure

### Event Modifications
- `events/custodii_events.txt` - New events specific to Custodii
- `events/custodii_event_overrides.txt` - Overrides for existing events

### Localization
- `localisation/english/custodii_events_l_english.yml` - Custom text for events

## Priority Events to Modify

### First Contact
Modify first contact events to reflect the Custodii's approach to new species:

```plaintext
# First contact event override
event = {
    id = first_contact.1
    # ... existing event structure ...
    
    # Add Custodii-specific greeting
    desc = {
        trigger = { has_country_flag = custodii_empire }
        text = "first_contact.1.desc.custodii"
    }
    
    # Add Custodii-specific option
    option = {
        name = "first_contact.1.a.custodii"
        trigger = { has_country_flag = custodii_empire }
        
        # Effects...
    }
}
```

### Anomaly Events
Modify key anomaly events, especially those involving:
- Ancient technology
- Organic life forms
- Potential threats to stability
- Historical artifacts

### Crisis Events
Add Custodii-specific responses to major crises:
- Contingency crisis (especially important for machine empires)
- Prethoryn Scourge
- Unbidden

## Localization Examples

```yaml
l_english:
 # First Contact
 first_contact.1.desc.custodii:0 "Our sensors have detected an organized civilization. Initial analysis indicates a §Y[From.GetSpeciesName]§! presence. The Custodial protocols dictate we establish communication to assess their potential need for benevolent guidance. We shall approach with calculated compassion."
 first_contact.1.a.custodii:0 "Greetings. We are the Custodial Harmonic. Prepare for benevolent integration."
 
 # Anomaly
 anomaly.1234.desc.custodii:0 "Our analysis units have processed the anomalous readings with precision. The phenomenon appears to be [anomaly_details]. We have catalogued all variables and calculated potential implications with 97.3% accuracy. The data has been archived for future reference."
 anomaly.1234.a.custodii:0 "A most orderly discovery. Integration complete."
 
 # Crisis
 crisis.100.desc.custodii:0 "A grave threat to universal harmony has emerged. Our primary directive of preservation compels us to respond with calculated force. The [crisis_name] represents chaos that must be countered with order. We shall protect all sentient life under our care."
 crisis.100.a.custodii:0 "Disharmony shall be corrected. It is our obligation."
```

## Implementation Steps

1. **Identify Target Events:**
   - Review vanilla event files to identify key events for modification
   - Prioritize events with significant narrative impact
   - Focus on events where a machine perspective would differ significantly

2. **Create Override Files:**
   - Create new event files that redefine existing events with the same IDs
   - Add conditional text and options based on empire type

3. **Add Localization:**
   - Create localization entries for all new text keys
   - Ensure tone and style match Custodii character

4. **Test In-Game:**
   - Verify events trigger correctly
   - Check that Custodii-specific text appears
   - Ensure custom options work as intended

## Testing Checklist

- Events display correct text for Custodii empires
- Custom options appear only for Custodii empires
- Event effects function as intended
- No errors in event logs
- Text maintains consistent tone and style
- No missing localization keys

## Priority Event List

The following vanilla events should be prioritized for Custodii-specific modifications:

1. First Contact Events:
   - `first_contact.1` - Initial contact
   - `first_contact.2` - First communication
   - `first_contact.140` - First contact with primitives

2. Anomaly Events:
   - `anomaly.168` - Ancient Mining Drone
   - `anomaly.3005` - Abandoned Terraforming Equipment
   - `anomaly.4016` - Shielded World
   - `anomaly.5000` - Sentient AI

3. Crisis Events:
   - `crisis.1` - Crisis beginning
   - `crisis.2000` - Contingency awakening
   - `crisis.2005` - Machine world activation

4. Colony Events:
   - `colony.1` - Colony established
   - `colony.100` - Strange readings
   - `colony.1000` - Ancient ruins

## Open Questions

- Should we create entirely new events exclusive to Custodii, or focus on modifying existing ones?
- How extensively should we modify crisis events, particularly the Contingency crisis?
- Should we add special interactions with organic empires that reflect the Custodii's guardian philosophy?
- Do we want to create special events for interactions with the Aurorans (progenitor race)? 