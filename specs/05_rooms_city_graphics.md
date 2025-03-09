# Rooms & City Graphics Specification

## Overview
This specification outlines the implementation of custom room backgrounds and city graphics for the Custodii race. These visual elements will reflect the Custodii's elegant, structured, and futuristic aesthetic with Victorian-inspired elements.

## Room Background

### Design Guidelines
- **Style:** Elegant, symmetrical, minimalist structure with smooth curves and geometric precision
- **Materials:** Clean metallic surfaces accented with delicate crystalline patterns
- **Lighting:** Soft, ambient lighting with subtle teal or gold highlights
- **Elements:** Control interfaces, monitoring screens, and subtle mechanical elements
- **Atmosphere:** Tranquil, ordered, and sophisticated environment suggesting benevolent oversight

### Technical Specifications
- **Resolution:** 1366x768 pixels (minimum), 1920x1080 pixels (recommended)
- **Format:** DDS (DirectDraw Surface)
- **Compression:** DXT5 (if transparency needed) or DXT1 (if fully opaque)
- **Color Depth:** 32-bit

### File Structure
- `gfx/interface/rooms/room_custodii.dds` - The room background image

### Sprite Definition
Create `interface/custodii_room.gfx`:

```plaintext
spriteTypes = {
    spriteType = {
        name = "GFX_room_custodii"
        textureFile = "gfx/interface/rooms/room_custodii.dds"
        noOfFrames = 1
        effectFile = "gfx/FX/buttonstate.lua"
    }
}
```

## City Graphics

### Design Guidelines
- **Style:** Futuristic Victorian-inspired shapes—domes, arches, and spires with refined sci-fi minimalism
- **Materials:** Polished metallic and crystalline structures with subtle illumination
- **Color Palette:** Silver/white primary structures with teal or gold accent lighting
- **Layout:** Ordered, symmetrical city planning with clear hierarchical structure
- **Elements:** Elevated walkways, observation domes, maintenance facilities, and data processing centers

### Technical Specifications
- **Resolution:** 3840x2160 pixels (panoramic cityscape)
- **Format:** DDS (DirectDraw Surface)
- **Compression:** DXT5 or DXT1
- **Number of Images:** 5 levels of development (L1-L5)

### City Levels
1. **Level 1:** Basic outpost with minimal structures
2. **Level 2:** Small settlement with primary facilities
3. **Level 3:** Established colony with diverse structures
4. **Level 4:** Developed city with advanced infrastructure
5. **Level 5:** Metropolis with impressive architectural features

### File Structure
- `gfx/portraits/city_sets/custodii_city_l01.dds` - Level 1 city
- `gfx/portraits/city_sets/custodii_city_l02.dds` - Level 2 city
- `gfx/portraits/city_sets/custodii_city_l03.dds` - Level 3 city
- `gfx/portraits/city_sets/custodii_city_l04.dds` - Level 4 city
- `gfx/portraits/city_sets/custodii_city_l05.dds` - Level 5 city

### Graphical Culture Definition
Create `common/graphical_culture/00_custodii_graphical_culture.txt`:

```plaintext
custodii_01 = {
    city_graphical_culture = custodii_01
    city_texture = "custodii_city_"
    city_amount = 5
    
    # Prevent random generation for other species
    spawn_odds = { weight = 0 }
    
    # Lighting settings
    ship_color = yes
    ship_lighting = {
        cam_light_1_dir = { 0.0 1.0 0.0 }
        cam_light_2_dir = { 0.0 -1.0 0.0 }
        cam_light_3_dir = { 1.0 0.0 0.0 }
        
        cam_light_1_col = { 0.7 0.9 1.0 }
        cam_light_2_col = { 0.5 0.7 0.8 }
        cam_light_3_col = { 0.8 0.8 0.9 }
        
        cam_light_1_int = 1.0
        cam_light_2_int = 0.5
        cam_light_3_int = 0.5
        
        rim_light_dir = { 0.0 1.0 0.0 }
        rim_light_col = { 0.5 0.8 1.0 }
        rim_light_int = 1.0
        
        # Fallback to vanilla if needed
        fallback = mammalian_01
    }
}
```

### Localization
Add to `localisation/english/custodii_graphics_l_english.yml`:

```yaml
l_english:
 custodii_01:0 "Custodial Architecture"
```

## Implementation Steps

### Room Background
1. **Create Artwork:**
   - Design the room background according to guidelines
   - Save as DDS in the correct resolution
   
2. **Add to Interface:**
   - Create the sprite definition file
   - Place the image in the correct directory

3. **Link to Empire:**
   - In the preset empire definition, add `room = "custodii"` (without the "GFX_room_" prefix)
   - Alternatively, make it selectable in the empire creation UI

### City Graphics
1. **Create Artwork:**
   - Design 5 levels of city development
   - Ensure visual progression between levels
   - Save as DDS files in the correct resolution
   
2. **Add Graphical Culture:**
   - Create the graphical culture definition
   - Place city images in the correct directory
   
3. **Link to Species:**
   - In the species class definition, set `graphical_culture = custodii_01`
   - This will automatically use the city graphics for colonies

## Testing Checklist

### Room Background
- Room appears correctly in empire creation screen
- Room appears correctly in diplomacy screen
- No visual artifacts or stretching
- Lighting and colors match the Custodii aesthetic

### City Graphics
- All 5 city levels appear correctly on planets
- City levels progress properly as colonies develop
- No visual artifacts or stretching
- Cities match the Custodii aesthetic
- City appears correctly in empire creation background

## Reference Images
Consider using the following as inspiration:
- Victorian architecture with futuristic elements
- Clean, minimalist sci-fi environments
- Symmetrical, ordered city layouts
- Elegant control rooms with advanced interfaces

## Open Questions
- Should we include animated elements in the room background?
- Do we want to create multiple room variations for different diplomatic stances?
- Should city graphics include any special features for machine worlds or habitats? 