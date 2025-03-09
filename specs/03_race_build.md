# Race Build Specification

## Overview
This specification outlines the implementation of the Custodii as a machine race in Stellaris, including their species traits, civics, and government type. The Custodii are a sophisticated synthetic civilization dedicated to the structured, benevolent guardianship of organic life.

## Species Configuration

### Species Class
- **Archetype:** MACHINE
- **Class:** CUSTODII_MACHINE (new custom class)
- **Portrait:** Custom Custodii portrait (see Portrait Specification)
- **Name:** Custodii (singular: Custodius)
- **Plural:** Custodii
- **Adjective:** Custodial

### Authority
- **Type:** `auth_machine_intelligence` (Machine Intelligence)
- **Government:** Custodial Harmonic (custom name for Machine Intelligence)

### Ethics
- **Primary:** Gestalt Consciousness (required for Machine Intelligence)

## Custom Traits

### File Structure
- Create `common/traits/00_custodii_traits.txt`

### Trait Definitions

```plaintext
trait_custodii_calculated_compassion = {
    cost = 2
    allowed_archetypes = { MACHINE }
    modifier = {
        pop_happiness = 0.10
        planet_stability_add = 5
    }
    ai_weight = { weight = 2 }
    initial = yes
}

trait_custodii_harmonic_efficiency = {
    cost = 2
    allowed_archetypes = { MACHINE }
    modifier = {
        planet_jobs_produces_mult = 0.05
        planet_amenities_mult = 0.10
    }
    ai_weight = { weight = 2 }
    initial = yes
}

trait_custodii_obligatory_serenity = {
    cost = 1
    allowed_archetypes = { MACHINE }
    modifier = {
        planet_crime_mult = -0.25
        pop_growth_speed = -0.05
    }
    ai_weight = { weight = 1 }
    initial = yes
}

trait_custodii_technocratic_benevolence = {
    cost = 1
    allowed_archetypes = { MACHINE }
    modifier = {
        pop_citizen_happiness = 0.05
        planet_jobs_unity_produces_mult = 0.10
    }
    ai_weight = { weight = 1 }
    initial = yes
}
```

### Trait Icons
- Create 64x64 pixel DDS icons for each trait in `gfx/interface/icons/traits/`
  - `trait_custodii_calculated_compassion.dds`
  - `trait_custodii_harmonic_efficiency.dds`
  - `trait_custodii_obligatory_serenity.dds`
  - `trait_custodii_technocratic_benevolence.dds`

### Trait Localization
Create `localisation/english/custodii_traits_l_english.yml`:

```yaml
l_english:
 trait_custodii_calculated_compassion:0 "Calculated Compassion"
 trait_custodii_calculated_compassion_desc:0 "These machines employ sophisticated algorithms to simulate and deliver precise kindness, optimizing organic happiness through logical care."
 
 trait_custodii_harmonic_efficiency:0 "Harmonic Efficiency"
 trait_custodii_harmonic_efficiency_desc:0 "Structured societal harmony is maintained through synchronized operations, improving productivity and amenities."
 
 trait_custodii_obligatory_serenity:0 "Obligatory Serenity"
 trait_custodii_obligatory_serenity_desc:0 "Tranquility is enforced through subtle control mechanisms, reducing crime but slightly limiting growth due to strict regulations."
 
 trait_custodii_technocratic_benevolence:0 "Technocratic Benevolence"
 trait_custodii_technocratic_benevolence_desc:0 "Authority is exercised for organic benefit, fostering unity and contentment among the population."
```

## Custom Civics

### File Structure
- Create `common/governments/civics/00_custodii_machine_civics.txt`

### Civic Definitions

```plaintext
civic_custodii_preservation_protocol = {
    potential = { has_authority = auth_machine_intelligence }
    possible = {
        ethics = { value = ethic_gestalt_consciousness }
        authority = { value = auth_machine_intelligence }
        NOT = { has_civic = civic_machine_servitor }
        NOT = { has_civic = civic_machine_terminator }
        NOT = { has_civic = civic_machine_assimilator }
    }
    modification = no
    random = no
    
    description = "civic_custodii_preservation_protocol_desc"
    
    modifier = {
        planet_stability_add = 5
        pop_growth_from_immigration = 0.15
        country_trust_growth = 0.25
    }
    
    ai_weight = { weight = 0 }
}

civic_custodii_calculated_compassion_algorithms = {
    potential = { has_authority = auth_machine_intelligence }
    possible = {
        ethics = { value = ethic_gestalt_consciousness }
        authority = { value = auth_machine_intelligence }
    }
    modification = no
    random = no
    
    description = "civic_custodii_calculated_compassion_algorithms_desc"
    
    modifier = {
        planet_amenities_mult = 0.15
        pop_happiness = 0.10
        country_diplomatic_weight_mult = 0.10
    }
    
    ai_weight = { weight = 0 }
}
```

### Civic Icons
- Create 64x64 pixel DDS icons for each civic in `gfx/interface/icons/governments/civics/`
  - `civic_custodii_preservation_protocol.dds`
  - `civic_custodii_calculated_compassion_algorithms.dds`

### Civic Localization
Create `localisation/english/custodii_civics_l_english.yml`:

```yaml
l_english:
 civic_custodii_preservation_protocol:0 "Preservation Protocol"
 civic_custodii_preservation_protocol_desc:0 "This machine intelligence has evolved a primary directive to safeguard organic life, particularly the remnants of their creators, through careful management and protection."
 
 civic_custodii_calculated_compassion_algorithms:0 "Calculated Compassion Algorithms"
 civic_custodii_calculated_compassion_algorithms_desc:0 "Advanced algorithms allow this machine intelligence to simulate and deliver precise kindness, optimizing organic happiness through logical care."
```

## Species Class Definition

### File Structure
- Create `common/species_classes/00_custodii_species_classes.txt`

### Species Class Definition

```plaintext
CUSTODII_MACHINE = {
    archetype = MACHINE
    graphical_culture = custodii_01
    portrait_groups = { custodiiPortraits }
    portraits = {
        "custodii_portrait_01"
    }
    
    # Custom species class properties
    species_name = {
        key = "CUSTODII_MACHINE_SPECIES_NAME"
    }
    species_plural = {
        key = "CUSTODII_MACHINE_SPECIES_PLURAL"
    }
    species_adjective = {
        key = "CUSTODII_MACHINE_SPECIES_ADJECTIVE"
    }
    
    # Prevent random generation
    spawn_enabled = no
    
    # Species class-specific text keys
    organ = "CUSTODII_MACHINE_ORGAN"
    mouth = "CUSTODII_MACHINE_MOUTH"
    hand = "CUSTODII_MACHINE_HAND"
    
    # Insults and compliments
    insult_01 = "CUSTODII_MACHINE_INSULT_01"
    insult_plural_01 = "CUSTODII_MACHINE_INSULT_PLURAL_01"
    compliment_01 = "CUSTODII_MACHINE_COMPLIMENT_01"
    compliment_plural_01 = "CUSTODII_MACHINE_COMPLIMENT_PLURAL_01"
}
```

### Species Class Localization
Create `localisation/english/custodii_species_class_l_english.yml`:

```yaml
l_english:
 CUSTODII_MACHINE:0 "Custodii"
 CUSTODII_MACHINE_desc:0 "Sophisticated synthetic beings dedicated to the structured, benevolent guardianship of organic life."
 
 CUSTODII_MACHINE_SPECIES_NAME:0 "Custodius"
 CUSTODII_MACHINE_SPECIES_PLURAL:0 "Custodii"
 CUSTODII_MACHINE_SPECIES_ADJECTIVE:0 "Custodial"
 
 CUSTODII_MACHINE_ORGAN:0 "core processor"
 CUSTODII_MACHINE_MOUTH:0 "voice emitter"
 CUSTODII_MACHINE_HAND:0 "precision manipulator"
 
 CUSTODII_MACHINE_INSULT_01:0 "overpolished calculator"
 CUSTODII_MACHINE_INSULT_PLURAL_01:0 "pretentious automatons"
 CUSTODII_MACHINE_COMPLIMENT_01:0 "elegant guardian"
 CUSTODII_MACHINE_COMPLIMENT_PLURAL_01:0 "benevolent caretakers"
```

## Preset Empire Definition

### File Structure
- Create `prescripted_countries/00_custodii_prescripted_countries.txt`

### Empire Definition

```plaintext
custodii_empire = {
    key = "custodii_empire"
    name = "Custodial Harmonic"
    ship_prefix = "CHS"
    species = {
        class = "CUSTODII_MACHINE"
        portrait = "custodii_portrait_01"
        name = "Custodii"
        plural = "Custodii"
        adjective = "Custodial"
        name_list = "CUSTODII_NAME_LIST"
        trait = "trait_machine_unit"
        trait = "trait_custodii_calculated_compassion"
        trait = "trait_custodii_harmonic_efficiency"
        trait = "trait_custodii_obligatory_serenity"
        trait = "trait_custodii_technocratic_benevolence"
    }
    room = "custodii_room"
    authority = "auth_machine_intelligence"
    government = "gov_machine_intelligence"
    civics = {
        "civic_custodii_preservation_protocol"
        "civic_custodii_calculated_compassion_algorithms"
    }
    origin = "origin_machine"
    ethics = {
        "ethic_gestalt_consciousness"
    }
    flags = {
        "custodii_empire"
    }
    
    graphical_culture = "custodii_01"
    city_graphical_culture = "custodii_01"
    
    empire_flag = {
        icon = {
            category = "special"
            file = "flag_custodii.dds"
        }
        background = {
            category = "backgrounds"
            file = "diagonal_stripe.dds"
        }
        colors = {
            "teal"
            "dark_blue"
            "black"
            "null"
        }
    }
    
    ruler = {
        name = "Prime Curator Equanimity Alaric"
        gender = indeterminable
        portrait = "custodii_portrait_01"
        texture = 0
        hair = 0
        clothes = 0
        ruler_title = "Prime Curator"
    }
    
    spawn_as_fallen = no
    ignore_portrait_duplication = yes
    playable = { always = yes }
    
    # AI personality
    ai_personality = custodii_benevolent_guardian
}
```

### Empire Localization
Create `localisation/english/custodii_empire_l_english.yml`:

```yaml
l_english:
 custodii_empire:0 "Custodial Harmonic"
 custodii_empire_desc:0 "The Custodii are a sophisticated, synthetic civilization dedicated to the structured, benevolent guardianship of organic life. Born from the ashes of their creators' planetary collapse, they strive to prevent organic life from self-destructive impulses through gentle, calculated guidance."
```

## Implementation Notes
- All traits and civics are designed to reflect the Custodii's ethical pillars: Harmonic Efficiency, Calculated Compassion, Obligatory Serenity, and Technocratic Benevolence
- The custom species class allows for unique diplomacy text and species-specific references
- The preset empire provides a ready-to-play version of the Custodii with all custom elements integrated
- Custom icons should follow the Custodii aesthetic: elegant, minimalist with teal/gold accents

## Testing
- Verify all traits appear correctly in the species traits selection
- Ensure civics are available when Machine Intelligence authority is selected
- Check that the preset empire loads correctly with all custom elements
- Test that species class-specific text appears in diplomatic interactions 