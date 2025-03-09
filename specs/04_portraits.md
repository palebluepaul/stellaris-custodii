# Portraits Specification

## Overview
This specification outlines the implementation of custom animated portraits for the Custodii race. The portraits will reflect the Custodii's elegant, refined futuristic aesthetic with sleek synthetic forms, symmetrical and graceful design, and subtle teal or gold highlights.

## Portrait Design Guidelines

### Visual Characteristics
- **Form:** Humanoid, precise, elegantly minimalistic
- **Materials:** Polished metallic and porcelain-like surfaces
- **Accents:** Subtle luminous teal or gold highlights
- **Style:** Refined futuristic aesthetics with Victorian-inspired elements
- **Expression:** Calm, controlled, with an air of gentle authority

### Animation Requirements
- **Idle Animation:** Subtle movements showing mechanical precision
  - Slight head movements
  - Occasional blinking lights or interface elements
  - Minimal "breathing" motion to suggest life without being too organic
- **Speaking Animation:** Synchronized mouth/voice emitter movement when communicating
- **Special States:** Optional variations for diplomatic stances (friendly, neutral, hostile)

## Implementation Approach

We will use a hybrid approach, leveraging existing machine portrait animations while creating custom textures and potentially some model modifications.

### Option 1: Retexturing Existing Machine Portraits

#### Base Selection
- Identify a suitable base portrait from Synthetic Dawn DLC
- Recommended: Machine Consciousness (most elegant) or Driven Assimilator (most humanoid)

#### Texture Modifications
- Create new diffuse texture (color/pattern)
- Create new normal map (surface details)
- Create new specular map (shininess/reflectivity)
- Add subtle emissive elements (glowing parts)

#### File Structure
- `gfx/models/portraits/custodii/` - Directory for texture files
  - `custodii_diffuse.dds` - Main color/pattern texture
  - `custodii_normal.dds` - Surface detail texture
  - `custodii_specular.dds` - Shininess/reflectivity map
  - `custodii_emissive.dds` - Glowing elements texture

### Option 2: Custom Model with Existing Animation Rig

#### Model Creation
- Create a new 3D model in Blender/Maya
- Rig it to match the skeleton/animation points of an existing machine portrait
- Export to Stellaris mesh format

#### File Structure
- `gfx/models/portraits/custodii/` - Directory for model and texture files
  - `custodii_portrait.mesh` - 3D model file
  - Texture files as in Option 1

### Portrait Definition

#### Portrait File
Create `gfx/portraits/portraits/01_custodii_portraits.txt`:

```plaintext
portraits = {
    custodii_portrait_01 = {
        entity = "custodii_portrait_entity"  # For custom model
        # OR
        entity = "robot_01_portrait_entity"  # If using existing animation with new textures
        
        species = {
            set = "CUSTODII_MACHINE"
        }
        
        # Portrait textures
        texturefile = "gfx/models/portraits/custodii/custodii_diffuse.dds"
        
        # Animation states
        portrait_state = { 
            state = "idle" 
            animation = "idle" 
        }
        portrait_state = { 
            state = "speaking" 
            animation = "speaking" 
        }
    }
}
```

#### Portrait Group
Create or modify `gfx/portraits/portrait_groups/00_portrait_groups.txt` to add:

```plaintext
custodiiPortraits = {
    default = custodii_portrait_01
    
    game_setup = {
        add = {
            portraits = {
                custodii_portrait_01
            }
        }
    }
    
    species = {
        set = "CUSTODII_MACHINE"
    }
}
```

#### Entity Definition
If creating a custom model, create `gfx/models/portraits/custodii/custodii_portraits.asset`:

```plaintext
entity = {
    name = "custodii_portrait_entity"
    pdxmesh = "custodii_portrait_mesh"
    
    # Animation definitions
    state = { name = "idle" animation = "idle" }
    state = { name = "speaking" animation = "speaking" }
    
    scale = 1.0
}

meshsettings = {
    name = "custodii_portrait_mesh"
    texture_diffuse = "custodii_diffuse.dds"
    texture_normal = "custodii_normal.dds"
    texture_specular = "custodii_specular.dds"
    texture_emissive = "custodii_emissive.dds"
}
```

## Technical Specifications

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

### Model Requirements (if creating custom)
- **Polygon Count:** 5,000-10,000 triangles (balance between detail and performance)
- **UV Mapping:** Single UV set, no overlapping UVs
- **Rig Compatibility:** Must match animation points of base machine portraits
- **Export Format:** .mesh (via Clausewitz Maya exporter or Jorodox tools)

## Implementation Steps

1. **Preparation:**
   - Extract and analyze existing machine portraits
   - Identify suitable base for modification

2. **For Texture Modification Approach:**
   - Create new textures based on design guidelines
   - Test with existing model in-game

3. **For Custom Model Approach:**
   - Create 3D model according to specifications
   - Rig to match existing animation points
   - Export to Stellaris format
   - Create textures
   - Test in-game

4. **Integration:**
   - Define portrait in portrait files
   - Add to portrait groups
   - Link to species class
   - Test in empire creation and in-game

## Testing Checklist
- Portrait appears correctly in empire creation screen
- Animation plays smoothly in-game
- No texture stretching or UV issues
- Lighting interacts properly with the model
- Speaking animation syncs with voice lines
- No clipping with room backgrounds

## Open Questions
- Do we want multiple portrait variations or a single definitive Custodii appearance?
- Should we include special diplomatic stance variations (friendly/hostile)?
- Will we need to create custom animations or can we rely on existing ones?
- What level of detail is appropriate for performance across different hardware? 