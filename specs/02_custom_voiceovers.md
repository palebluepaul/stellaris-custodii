# Custom Voiceovers Specification

## Overview
This specification outlines the implementation of a custom voice pack for the Custodii race, providing unique audio responses for in-game events. The voice will reflect the Custodii's elegant, structured, and benevolent nature with a formal yet futuristic tone.

## File Structure
- `sound/vo/custodii-advisor/` - Contains the voice line audio files
- `sound/custodii-advisor.asset` - Defines sound effects linking to audio files
- `sound/advisor_voice_types/01_custodii_advisor.txt` - Defines the advisor voice type
- `localisation/english/custodii_advisor_l_english.yml` - Localization for advisor name
- `gfx/interface/icons/advisor_custodii.dds` - Icon for the advisor selection menu

## Voice Line Requirements

### Audio Format
- File format: OGG (.ogg) preferred, WAV (.wav) acceptable
- Sample rate: 44.1kHz
- Bit depth: 16-bit
- Channels: Mono or Stereo
- Compression: Medium quality (for OGG)

### Required Voice Lines
Based on the Custodii briefing, the following lines should be recorded:

#### Core Game Notifications
- Research Complete: "Splendid news, dear beneficiaries! Another calculated advancement ensures tranquility."
- Colonization: "Rejoice! Another sanctuary of harmony and order awaits your presence."
- Construction Complete: "Discovery integrated seamlessly."
- Fleet Built: "Strength ensures lasting harmony."
- First Contact: "Greetings. We are the Custodial Harmonic. Prepare for benevolent integration."
- War Declaration: "Forced integration is a compassionate necessity."
- Victory: "Equilibrium restored; serenity prevails."

#### Additional Required Lines
- Enemy Fleet Detected: "Disharmonious elements detected."
- Hostile Fleet Engaged: "Resistance illogical; compliance inevitable."
- Anomaly Discovered: "Curious irregularity requires analysis."
- Special Project Complete: "Structured inquiry yields elegant solutions."
- Resource Shortage: "Resource allocation requires recalibration."
- Diplomatic Offer: "Proposal evaluated with calculated compassion."
- Situation Log Updated: "New variables integrated into harmony matrix."

### Voice Characteristics
- Tone: Elegant, structured, polite with gentle paternalistic authority
- Cadence: Measured, precise, with subtle mechanical undertones
- Emotion: Calm, controlled, with calculated warmth
- Accent: Neutral or slightly British-influenced for Victorian undertones

## Implementation Details

### Asset File
Create `sound/custodii-advisor.asset` with entries for each sound effect:

```plaintext
soundeffect = {
    name = "advisor_notify_research_complete"
    file = "sound/vo/custodii-advisor/notify_research_complete_01.ogg"
}

soundeffect = {
    name = "advisor_notify_construction_complete"
    file = "sound/vo/custodii-advisor/notify_construction_complete_01.ogg"
}

# Additional sound effects for each voice line...
```

### Voice Type Script
Create `sound/advisor_voice_types/01_custodii_advisor.txt`:

```plaintext
advisor_voice_type = {
    key = "CUSTODII_ADVISOR"
    selection_sound = advisor_notification
    icon = "gfx/interface/icons/advisor_custodii.dds"
    button_icon = "advisor_custodii"
    country = {
        hostile_fleet_detected = advisor_fleet_detected
        construction_complete = advisor_notify_construction_complete
        research_complete = advisor_notify_research_complete
        colony_established = advisor_notify_colony_established
        declare_war = advisor_notify_declare_war
        victory = advisor_notify_victory
        # Additional mappings for each game event...
    }
}
```

### Localization
Create `localisation/english/custodii_advisor_l_english.yml`:

```yaml
l_english:
 advisor_custodii:0 "Custodii Overseer"
 advisor_custodii_desc:0 "The measured, elegant voice of a Custodii Overseer, guiding with calculated compassion and structured harmony."
```

## Icon Requirements
- Size: 32x32 pixels
- Format: DDS (DirectDraw Surface)
- Style: Should reflect the Custodii aesthetic - elegant, minimalist with teal/gold accents

## Testing Procedures
- Verify all voice lines play correctly for their corresponding triggers
- Check that the advisor appears in the Settings > Advisor selection menu
- Ensure volume levels are consistent across all voice lines
- Test with different game speeds to ensure timing is appropriate

## Randomization
For variety, multiple versions of each line can be implemented:

```plaintext
soundeffect = {
    name = "advisor_notify_research_complete_var1"
    file = "sound/vo/custodii-advisor/notify_research_complete_01.ogg"
}

soundeffect = {
    name = "advisor_notify_research_complete_var2"
    file = "sound/vo/custodii-advisor/notify_research_complete_02.ogg"
}
```

Then in the voice type script:

```plaintext
research_complete = random_list = { 
    0.5 advisor_notify_research_complete_var1
    0.5 advisor_notify_research_complete_var2 
}
```

## Open Questions
- Will we use professional voice acting or synthetic voice generation?
- Should we include additional voice lines for DLC-specific events?
- Do we want multiple voice options (male/female/neutral) for the Custodii? 