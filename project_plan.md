# Custodii Race Mod Project Plan

## Overview
This document outlines the implementation plan for the Custodii race mod for Stellaris. The plan is organized into phases, with each phase building upon the previous one to create a comprehensive and polished mod.

## Phase 1: Foundation Setup (DONE)

### 1.1 Development Environment Setup
- Set up development environment on both WSL and macOS
- Install required tools and dependencies
- Create project repository structure
- Implement foundation tools (Python utilities)

### 1.2 Mod Structure Initialization
- Create basic mod directory structure
- Generate initial descriptor files
- Set up localization framework
- Create placeholder files for key components

### 1.3 Foundation Tools Implementation
- Implement path resolution for cross-platform development
- Create mod descriptor generator and validator
- Develop file format checker for localization files
- Build asset validation tools
- Create deployment helper

## Phase 2: Core Race Definition (Week 2)

### 2.1 Name Lists
- Implement Custodii name lists for leaders, ships, fleets, and planets
- Create localization entries for name lists
- Test name list integration in-game

### 2.2 Species Class and Traits
- Define Custodii machine species class
- Create custom traits reflecting Custodii ethical pillars
- Implement trait icons and localization
- Test traits in empire creation

### 2.3 Civics and Government
- Create custom civics for Custodii
- Implement civic icons and localization
- Configure government type and ethics
- Test civics in empire creation

### 2.4 Preset Empire
- Create prescripted empire definition
- Configure starting traits, civics, and ethics
- Set up empire flag and colors
- Test preset empire in-game

## Phase 3: Visual Assets - Part 1 (Week 3)

### 3.1 Portrait Development
- Select approach (retexture existing or create new)
- Create/modify portrait textures
- Configure portrait files and definitions
- Test portrait in-game

### 3.2 Room Background
- Design room background image
- Create sprite definition
- Link room to empire
- Test room in-game

### 3.3 City Graphics
- Design city graphics for all 5 development levels
- Create graphical culture definition
- Link city graphics to species
- Test city progression in-game

## Phase 4: Visual Assets - Part 2 (Week 4)

### 4.1 Ship Design Concept
- Finalize ship design approach (retexture or new models)
- Create concept art for key ship classes
- Define ship aesthetic guidelines

### 4.2 Ship Implementation
- Create/modify ship models and textures
- Configure ship asset files
- Link ships to graphical culture
- Test ships in-game

### 4.3 Additional Visual Elements
- Create custom icons for traits and civics
- Design empire flag
- Create any additional visual elements
- Test all visual elements for consistency

## Phase 5: Audio and Text (Week 5)

### 5.1 Custom Voiceovers
- Record/source voice lines for advisor
- Process audio files to correct format
- Configure advisor voice type
- Test advisor voice in-game

### 5.2 Event Responses
- Identify key events for customization
- Create Custodii-specific event text
- Implement event overrides
- Test custom events in-game

### 5.3 Diplomatic Text
- Create custom diplomatic phrases
- Implement AI personality
- Configure opinion modifiers
- Test diplomatic interactions in-game

## Phase 6: Integration and Polish (Week 6)

### 6.1 Balance and Refinement
- Test all mod components together
- Balance traits, civics, and other gameplay elements
- Refine text and visual assets based on testing
- Fix any integration issues

### 6.2 Compatibility Testing
- Test with various game versions
- Check compatibility with popular mods
- Resolve any conflicts or issues

### 6.3 Documentation
- Create user documentation
- Write installation instructions
- Document known issues and compatibility notes

### 6.4 Packaging and Release
- Prepare mod for distribution
- Create Steam Workshop page
- Publish initial release

## Dependencies and Critical Path

### Critical Dependencies
1. Foundation tools must be completed before any deployment testing
2. Species class and traits must be defined before portrait integration
3. Graphical culture must be defined before ship and city implementation
4. Portrait must be completed before room background integration
5. All visual and gameplay elements must be completed before final integration

### Parallel Work Streams
- Visual asset creation can proceed in parallel with gameplay mechanics
- Audio work can proceed independently of other components
- Text content can be developed alongside visual assets

## Resource Allocation

### Development Tools
- Python for utility scripts
- Image editing software for textures and icons
- 3D modeling software (if creating custom models)
- Audio editing software for voice processing

### Testing Environment
- Stellaris installation on both Windows and macOS
- Test saves at various game stages
- Multiple test configurations (different ethics, origins, etc.)

## Risk Management

### Identified Risks
1. **Cross-platform compatibility issues** - Mitigated by foundation tools
2. **Game updates breaking mod** - Plan for quick updates after game patches
3. **Asset creation complexity** - Fallback plans for using modified vanilla assets
4. **Integration challenges** - Regular testing of components together

### Contingency Plans
- If custom models prove too complex, fall back to retexturing existing assets
- If voice acting is unavailable, use text-to-speech with post-processing
- If certain events cannot be overridden, focus on the most impactful ones

## Open Questions and Decisions

1. **Portrait Approach**: Decide between retexturing existing portraits vs. creating new models
2. **Ship Design**: Determine whether to create entirely new models or modify existing ones
3. **Voice Implementation**: Choose between professional voice acting, synthetic voices, or a hybrid approach
4. **Event Scope**: Determine which vanilla events to override vs. creating new Custodii-specific events
5. **Compatibility**: Decide which major mods to ensure compatibility with

## Success Criteria

The Custodii race mod will be considered successful when:

1. All specified components are implemented and working together
2. The mod provides a cohesive, unique gameplay experience
3. Visual and audio assets maintain a consistent aesthetic
4. The mod can be easily installed and used on both Windows and macOS
5. Players can create and play as the Custodii race with all custom elements 