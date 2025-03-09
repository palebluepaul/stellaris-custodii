# Ships Specification

## Overview
This specification outlines the implementation of a custom ship set for the Custodii race. The ships will reflect the Custodii's elegant, structured, and futuristic aesthetic with Victorian-inspired elements, creating a unique visual identity for their fleet.

## Design Guidelines

### Visual Style
- **Form:** Elegant, symmetrical designs with smooth curves and geometric precision
- **Materials:** Polished metallic surfaces with crystalline accents
- **Color Palette:** Silver/white primary structures with teal or gold accent lighting
- **Aesthetic:** Refined futuristic with subtle Victorian-inspired elements (arches, spires)
- **Lighting:** Subtle teal or gold illumination for engines and active systems

### Ship Classes
The following ship classes need custom models:

1. **Corvette** - Small, agile scout/patrol vessel
2. **Destroyer** - Medium escort vessel
3. **Cruiser** - Versatile medium warship
4. **Battleship** - Heavy capital ship
5. **Titan** - Massive flagship
6. **Colossus** - Planet-destroying superweapon
7. **Constructor** - Civilian construction vessel
8. **Science Ship** - Research and survey vessel
9. **Transport** - Troop carrier
10. **Colony Ship** - Colonization vessel
11. **Starbase** - Space station (multiple tiers)

## Implementation Approach

We will use a hybrid approach, potentially modifying existing ship models with custom textures and elements to create a unique Custodii aesthetic.

### Option 1: Retexture Existing Ships

#### Base Selection
- Identify suitable base ship set (Mammalian or Machine Intelligence recommended)
- Extract models and textures for modification

#### Texture Modifications
- Create new diffuse textures with Custodii color scheme and patterns
- Add emissive maps for glowing elements
- Modify normal maps if needed for surface details

### Option 2: Custom Ship Models

#### Model Creation
- Create new 3D models in Blender/Maya
- Design according to Custodii aesthetic guidelines
- Create UV maps and textures
- Export to Stellaris mesh format

## File Structure

### Models and Textures
- `gfx/models/ships/custodii_ships/` - Directory for all ship models and textures
  - `custodii_corvette.mesh` - 3D model file for corvette
  - `custodii_corvette_diffuse.dds` - Color/pattern texture
  - `custodii_corvette_normal.dds` - Surface detail texture
  - `custodii_corvette_specular.dds` - Shininess/reflectivity map
  - `custodii_corvette_emissive.dds` - Glowing elements texture
  - (Similar files for each ship class)

### Asset Definition
Create `gfx/models/ships/custodii_ships.asset`:

```plaintext
# Corvette definition
mesh = {
    name = "custodii_corvette_mesh"
    file = "gfx/models/ships/custodii_ships/custodii_corvette.mesh"
}

entity = {
    name = "custodii_01_corvette_entity"
    pdxmesh = "custodii_corvette_mesh"
    
    # Attach points for weapons
    locator = {
        name = "small_gun_01"
        position = { 0 0 0 }
        rotation = { 0 0 0 }
    }
    # Additional locators as needed
    
    # Engine effects
    attach = { "engine_effect_locator" = "ship_effect_engine" }
    
    scale = 1.0
}

# Repeat similar definitions for each ship class:
# - custodii_01_destroyer_entity
# - custodii_01_cruiser_entity
# - custodii_01_battleship_entity
# - etc.
```

### Graphical Culture Integration
The ship set will use the same graphical culture defined for city graphics in `common/graphical_culture/00_custodii_graphical_culture.txt`:

```plaintext
custodii_01 = {
    # City definitions (as in city graphics spec)
    
    # Ship-specific settings
    ship_color = yes
    ship_lighting = {
        # Lighting settings (as in city graphics spec)
    }
}
```

## Technical Specifications

### Model Requirements
- **Polygon Count:**
  - Corvette: 5,000-10,000 triangles
  - Destroyer: 10,000-15,000 triangles
  - Cruiser: 15,000-20,000 triangles
  - Battleship: 20,000-30,000 triangles
  - Titan/Colossus: 30,000-50,000 triangles
  - Civilian ships: 5,000-15,000 triangles
  - Starbases: 15,000-40,000 triangles (depending on tier)

### Texture Requirements
- **Diffuse Map:**
  - Resolution: 1024x1024 or 2048x2048
  - Format: DDS (BC3/DXT5 with alpha)
  - Color depth: 32-bit
- **Normal Map:**
  - Resolution: Same as diffuse
  - Format: DDS (BC5/ATI2)
- **Specular Map:**
  - Resolution: Same as diffuse
  - Format: DDS (BC1/DXT1)
- **Emissive Map:**
  - Resolution: Same as diffuse
  - Format: DDS (BC1/DXT1)

### Weapon Attachment
- Define locator points in models for weapon attachment
- Use standard naming conventions for compatibility:
  - `small_gun_XX` - Small weapon hardpoints
  - `medium_gun_XX` - Medium weapon hardpoints
  - `large_gun_XX` - Large weapon hardpoints
  - `turret_muzzle_XX` - Muzzle flash points
  - `engine_effect_locator` - Engine glow point

## Implementation Steps

1. **Preparation:**
   - Extract and analyze existing ship models
   - Identify suitable base for modification or reference

2. **For Texture Modification Approach:**
   - Create new textures based on design guidelines
   - Test with existing models in-game

3. **For Custom Model Approach:**
   - Create 3D models according to specifications
   - Create UV maps and textures
   - Export to Stellaris format
   - Test in-game

4. **Integration:**
   - Define entities in asset files
   - Link to graphical culture
   - Test in-game with all ship classes

## Ship Sections and Components

If creating fully custom ships with multiple sections (bow, mid, stern):

1. **Section Definitions:**
   Create `common/ship_sizes/00_custodii_ship_sizes.txt` to define custom sections if needed

2. **Component Slots:**
   Define weapon hardpoints and utility slots in section definitions

3. **Compatibility:**
   Ensure compatibility with vanilla weapon and utility components

## Testing Checklist

- All ship classes appear correctly in-game
- Ships scale appropriately relative to each other
- Weapons attach correctly to hardpoints
- Engine effects display properly
- No texture stretching or UV issues
- No clipping or floating geometry
- Ships match the Custodii aesthetic
- Ships animate correctly during movement and combat
- All ship sections (if using multiple) fit together properly

## Open Questions

- Do we want to create entirely new models or modify existing ones?
- Should we include special visual effects for weapons or engines?
- Do we need custom turret models or can we use vanilla ones?
- Should we create multiple section variants for each ship class?
- What level of detail is appropriate for performance across different hardware? 