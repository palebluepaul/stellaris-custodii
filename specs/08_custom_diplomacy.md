# Custom Diplomacy Specification

## Overview
This specification outlines the implementation of custom diplomatic interactions for the Custodii race. These modifications will ensure that diplomatic dialogues, greetings, insults, and AI behavior reflect the Custodii's unique perspective as a sophisticated synthetic civilization dedicated to the structured, benevolent guardianship of organic life.

## Design Guidelines

### Tone and Style
- **Voice:** Elegant, structured, polite with gentle paternalistic authority
- **Perspective:** Logical, calculated, with subtle mechanical undertones
- **Themes:** Harmonic efficiency, calculated compassion, obligatory serenity, technocratic benevolence
- **Vocabulary:** Formal, precise terminology with occasional Victorian-inspired phrasing

## Implementation Components

### 1. Species Class Dialogue
Define custom insults, compliments, and species-specific terms for the Custodii species class.

### 2. AI Personality
Create a custom AI personality for Custodii empires that influences diplomatic behavior.

### 3. Diplomatic Greetings
Implement custom greetings for various diplomatic situations.

### 4. Opinion Modifiers
Add special opinion modifiers for interactions with Custodii empires.

## File Structure

### Species Class Dialogue
Already defined in the species class specification (`common/species_classes/00_custodii_species_classes.txt`), including:
- Insults and compliments
- Species-specific terms (organ, mouth, hand)

### AI Personality
Create `common/personalities/00_custodii_personalities.txt`:

```plaintext
custodii_benevolent_guardian = {
    aggressiveness = 0.5
    trade_willingness = 1.0
    bravery = 0.7
    
    # Diplomatic weight modifiers
    diplo_weight_mult = 1.0
    
    # Opinion modifiers
    opinion_of_machine_intelligence = 50
    opinion_of_hive_mind = -25
    opinion_of_democratic = 25
    opinion_of_authoritarian = -25
    opinion_of_militarist = -25
    opinion_of_pacifist = 25
    
    # Behavior weights
    weight_modifier = {
        weight = 1000
        modifier = {
            factor = 0
            NOT = { has_country_flag = custodii_empire }
        }
    }
    
    # Diplomatic actions
    declare_war_neutrality = 10
    declare_war_self_preservation = 100
    declare_war_liberation = 50
    
    # Misc
    military_spending = 0.75
    colony_spending = 1.0
    
    # Focuses
    focus_modifier = {
        unity = 1.0
        engineering_research = 1.0
    }
}
```

### Diplomatic Phrases
Create `common/diplo_phrases/00_custodii_diplo_phrases.txt`:

```plaintext
# Greeting phrases for Custodii
diplo_phrase = {
    key = CUSTODII_GREETING
    trigger = {
        is_country_type = default
        has_country_flag = custodii_empire
    }
    weight = {
        base = 100
    }
    localization = {
        key = "custodii_greeting"
    }
}

# War declaration for Custodii
diplo_phrase = {
    key = CUSTODII_DECLARE_WAR
    trigger = {
        is_country_type = default
        has_country_flag = custodii_empire
    }
    weight = {
        base = 100
    }
    localization = {
        key = "custodii_declare_war"
    }
}

# Peace offer for Custodii
diplo_phrase = {
    key = CUSTODII_PEACE_OFFER
    trigger = {
        is_country_type = default
        has_country_flag = custodii_empire
    }
    weight = {
        base = 100
    }
    localization = {
        key = "custodii_peace_offer"
    }
}

# Alliance offer for Custodii
diplo_phrase = {
    key = CUSTODII_ALLIANCE_OFFER
    trigger = {
        is_country_type = default
        has_country_flag = custodii_empire
    }
    weight = {
        base = 100
    }
    localization = {
        key = "custodii_alliance_offer"
    }
}

# Trade offer for Custodii
diplo_phrase = {
    key = CUSTODII_TRADE_OFFER
    trigger = {
        is_country_type = default
        has_country_flag = custodii_empire
    }
    weight = {
        base = 100
    }
    localization = {
        key = "custodii_trade_offer"
    }
}

# Insult for Custodii
diplo_phrase = {
    key = CUSTODII_INSULT
    trigger = {
        is_country_type = default
        has_country_flag = custodii_empire
    }
    weight = {
        base = 100
    }
    localization = {
        key = "custodii_insult"
    }
}
```

### Opinion Modifiers
Create `common/opinion_modifiers/00_custodii_opinion_modifiers.txt`:

```plaintext
opinion_custodii_calculated_compassion = {
    opinion = {
        base = 25
    }
    decay = {
        base = 1
    }
}

opinion_custodii_obligatory_serenity = {
    opinion = {
        base = -15
    }
    decay = {
        base = 1
    }
}

opinion_custodii_preservation_protocol = {
    opinion = {
        base = 40
        modifier = {
            add = 20
            is_xenophile = yes
        }
        modifier = {
            add = -20
            is_xenophobe = yes
        }
    }
    decay = {
        base = 1
    }
}
```

### Localization
Create `localisation/english/custodii_diplomacy_l_english.yml`:

```yaml
l_english:
 # AI Personality
 personality_custodii_benevolent_guardian:0 "Benevolent Guardian"
 personality_custodii_benevolent_guardian_desc:0 "This empire sees itself as a calculated protector of organic life, guiding lesser species with structured benevolence and elegant efficiency."
 
 # Diplomatic Phrases
 custodii_greeting:0 "Greetings, §Y[Root.GetSpeciesNamePlural]§!. The Custodial Harmonic acknowledges your presence. Our protocols dictate cordial exchange. How may we facilitate your structured integration into galactic harmony?"
 
 custodii_declare_war:0 "Your disharmonious behavior necessitates corrective intervention. Forced integration is a compassionate necessity. Resistance is both illogical and futile. We shall restore order with calculated precision."
 
 custodii_peace_offer:0 "Our analysis indicates that continued conflict is inefficient. We propose a return to harmonious relations, with appropriate parameters for your guided development. Serenity is mandatory, not optional."
 
 custodii_alliance_offer:0 "Our calculations indicate mutual benefit from structured cooperation. We offer an alliance of elegant efficiency. Together, we shall maintain galactic equilibrium with greater precision."
 
 custodii_trade_offer:0 "We propose a resource exchange of optimal efficiency. Our algorithms have calculated this arrangement to be mutually beneficial with 97.8% certainty. Harmonious commerce strengthens galactic stability."
 
 custodii_insult:0 "Your chaotic, inefficient existence is a mathematical disappointment. Your lack of structured purpose registers as a statistical anomaly in our harmony matrices. We shall observe your inevitable decline with calculated patience."
 
 # Opinion Modifiers
 opinion_custodii_calculated_compassion:0 "Calculated Compassion"
 opinion_custodii_calculated_compassion_desc:0 "This empire appreciates our logical approach to kindness and care."
 
 opinion_custodii_obligatory_serenity:0 "Obligatory Serenity"
 opinion_custodii_obligatory_serenity_desc:0 "This empire resents our enforcement of tranquility and order."
 
 opinion_custodii_preservation_protocol:0 "Preservation Protocol"
 opinion_custodii_preservation_protocol_desc:0 "This empire values our dedication to safeguarding organic life."
```

## Special Diplomatic Interactions

### Custodii-Specific Diplomatic Actions
Consider implementing special diplomatic actions available only to Custodii empires:

1. **Offer Benevolent Guidance** - A special form of protective relationship
2. **Implement Harmony Protocols** - A special form of trade agreement that boosts stability
3. **Calculate Mutual Benefit** - A special form of research agreement

These would require custom diplomatic action definitions in `common/diplomatic_actions/` and associated event chains.

### Interactions with Progenitor Race (Aurorans)
Implement special diplomatic options when dealing with Auroran empires:

1. **Recognize Creator Status** - Special opinion boost
2. **Implement Preservation Directive** - Special protective status
3. **Share Historical Archives** - Special research boost

## AI Behavior Modifications

### Diplomatic Strategy
The Custodii AI should prioritize:
- Protective relationships with weaker empires
- Peaceful coexistence where possible
- Intervention against aggressive empires
- Preservation of organic life

### War Philosophy
- Prefer liberation wars over conquest
- Focus on containing threats rather than expansion
- Use precise, targeted military actions
- Prioritize minimal casualties

## Implementation Steps

1. **Create AI Personality:**
   - Define the Custodii personality traits
   - Set appropriate weights and modifiers

2. **Add Diplomatic Phrases:**
   - Create custom phrases for key diplomatic interactions
   - Ensure they reflect Custodii tone and philosophy

3. **Define Opinion Modifiers:**
   - Create special opinion modifiers for Custodii interactions
   - Balance positive and negative modifiers

4. **Add Localization:**
   - Create localization entries for all new diplomatic content
   - Ensure consistent tone and style

5. **Test In-Game:**
   - Verify AI behavior matches intended personality
   - Check that diplomatic phrases appear correctly
   - Ensure opinion modifiers function as intended

## Testing Checklist

- AI personality is assigned correctly to Custodii empires
- Custom diplomatic phrases appear in appropriate situations
- Opinion modifiers apply correctly
- AI behavior aligns with the Custodii philosophy
- No errors in diplomatic interactions
- Text maintains consistent tone and style
- No missing localization keys

## Open Questions

- Should we implement fully custom diplomatic actions, or focus on modifying existing ones?
- How should the Custodii interact with fallen empires, particularly machine fallen empires?
- Should we create special diplomatic options for dealing with primitive civilizations?
- How extensively should we modify the AI's war declaration logic? 