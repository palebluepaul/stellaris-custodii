Got it! I'll compile a thorough guide on creating a custom machine race for Stellaris, covering all necessary elements, including:

- Name lists
- Custom voiceovers with randomization
- Race build with custom traits and civics
- Fully animated custom portraits (if feasible) or modifications of existing assets
- Custom rooms, city graphics, and ships (either new or modified versions of existing ones)
- Modified event responses tailored to your race
- Custom diplomacy text that changes AI interactions

I'll detail what files you need to create, the directory structure, script modifications, and tools required for each aspect. Stay tuned!

# Guide to Modding a Custom Machine Race in Stellaris

Modding a **custom machine race** in Stellaris involves creating or altering a variety of game assets – from text files to graphics and audio. This guide walks through all key elements, including file structure and examples, to ensure your machine empire mod integrates fully with the game. We’ll cover each aspect in order:

## 1. Name Lists (Leaders, Planets, Ships, etc.)

**Overview:** Name lists define the random names for leaders, planets, ships, fleets, and armies of your custom race. They are simple text files that Stellaris reads to generate names.

- **File & Folder:** Create a new text file in your mod’s `common/name_lists` folder (e.g. `MyMachine_namelist.txt`). Use UTF-8 encoding (with BOM). It’s easiest to copy an existing name list from Stellaris and modify it ([How to create custom name lists? : r/Stellaris](https://www.reddit.com/r/Stellaris/comments/17sykck/how_to_create_custom_name_lists/#:~:text=It%27s%20pretty%20simple%20as%20the,are%20all%20just%20text%20files)). For example, copy `MACHINE1.txt` or a similar list as a starting template.
- **Structure:** The file defines a name list key and various categories. For example: 

  ```plaintext
  MY_MACHINE_LIST = {
      key = "MY_MACHINE_LIST"
      ship_names = {
          # Ship class names
          generic = { "Aegis" "Sentinel" "Vanguard" ... }
          cruiser = { "Bulwark" "Fortress" ... }  # optional class-specific names
      }
      fleet_names = { "Alpha Fleet" "Beta Fleet" "%O% Armada" }
      planet_names = { "Unit Prime" "Databank" "Foundry" ... }
      first_names = { "AX-1" "AX-2" "BX-1" ... }       # for leader names (if using single part names)
      # Alternatively, use first_names_male, first_names_female, and last_names for two-part names
      army_names = { "Hunter-Killer" "Assimilator" ... }
  }
  ```
  Each category is a list in braces. You can list names separated by spaces or line breaks. Quotes are needed if a name has spaces. You can also define **sequential names** using patterns (e.g. `sequential_name = "%O% Fleet"` to produce “1st Fleet, 2nd Fleet”, etc.). Stellaris 3.4+ uses variables for sequential names (e.g. `%O%` changed to `$O$`) and requires corresponding entries in a localisation file ([Steam Community :: Discussions](https://steamcommunity.com/workshop/discussions/18446744073709551615/3280321473009640640/?appid=281990#:~:text=Then%20there%20is%20the%20problem,is%20now%20%24O)) ([Steam Community :: Discussions](https://steamcommunity.com/workshop/discussions/18446744073709551615/3280321473009640640/?appid=281990#:~:text=In%20HUMAN3.txt%20,HUMAN3_CLASSISxx_ROM%3A0%20%22Classis%20%24R)), but for simplicity you can use the older format or copy how vanilla does it (see `HUMAN3` name list for an example).
- **Leaders:** If your species has gendered or multi-part names (less likely for machines), use `first_names_male`, `first_names_female`, and `last_names`. If not, you can just use `first_names` or `full_names` for a unisex single name list. For a machine race, short alphanumeric designations or technical terms work well.
- **Planets & Ships:** Populate `planet_names` with themed names (like code-names or factory terms). For `ship_names`, you can have a generic pool or specific pools per ship size. If both a specific class list (e.g. `cruiser`) and a `generic` list are present, the game will pick from either for that class ([Empire modding - Stellaris Wiki](https://stellaris.paradoxwikis.com/Empire_modding#:~:text=Empire%20modding%20,their%20names%20from%20either)).
- **Making it Appear In-Game:** In order for your custom list to show up in empire creation, you need to give it a **display name** via localisation. In a localisation .yml file (e.g. `localisation/english/name_list_MY_MACHINE_LIST_l_english.yml`), add: 

  ```yaml
  l_english:
    name_list_MY_MACHINE_LIST:0 "Custom Machine Names"
    name_list_MY_MACHINE_LIST_desc:0 "Batches of designations for a machine race."
  ``` 

  Use the same key as the name list ID. This will display "Custom Machine Names" in the Name List dropdown. Ensure your localisation files are saved in UTF-8 BOM format ([Impostazione del nome visualizzato dell'elenco nomi nel creatore di imperi : r/StellarisMods](https://www.reddit.com/r/StellarisMods/comments/12rh7ym/setting_name_lists_display_name_in_the_empire/?tl=it#:~:text=%E2%80%A2)). Once done, your name list can be selected for your custom empire.

**Best Practices:** Keep name themes consistent. Machines often use serial numbers, AI-related terms, or mechanical references. Test in-game to see that leaders get names appropriately and that sequential naming (for fleets, etc.) works as intended. By structuring the file like existing ones and including localisation, Stellaris will recognize your custom list ([How to create custom name lists? : r/Stellaris](https://www.reddit.com/r/Stellaris/comments/17sykck/how_to_create_custom_name_lists/#:~:text=It%27s%20pretty%20simple%20as%20the,are%20all%20just%20text%20files)).

## 2. Custom Voiceovers (Advisor Voice Pack)

**Overview:** You can give your machine race a unique voice by creating a custom **Advisor Voice**. This involves adding new audio files and replacing the default voice lines triggered by events (construction complete, enemy contact, etc.) with your own, even allowing multiple variants for randomness.

- **Folder Structure:** In your mod, create a `sound` folder with subfolders for the voice files and definitions:
  - `sound/vo/` – contains the actual voice line audio files in a subfolder.
  - `sound/` – will contain an `.asset` file describing the sounds.
  - `sound/advisor_voice_types/` – will contain a `.txt` file defining the advisor voice type.
  - `localisation/` – will contain localisation for the advisor name.
  
  For example, if your advisor is called "Overseer", you might use `sound/vo/overseer-advisor/` for the audio files.

- **Audio Files:** Extract or create the voice lines you want. Stellaris uses **.ogg** format (preferred) or .wav for sounds. Name your files according to the triggers they replace. If using an existing advisor as a template, you’ll see files like `notify_construction_complete_01.ogg`, `fleet_detected_01.ogg`, etc. Use the same naming scheme to ensure the game plays them. Place all your .ogg files in the `sound/vo/<your-advisor-name>/` folder. For multiple variations of the same line, you can include several files (e.g. `fleet_detected_01.ogg`, `fleet_detected_02.ogg`, etc.) – the game can pick randomly among them if defined properly.

- **.asset File:** Create a file in `sound/` (e.g. `overseer-advisor.asset`). This file lists each sound effect and points to your audio files. For example:
  
  ```plaintext
  soundeffect = {
      name = "advisor_notify_construction_complete"
      file = "sound/vo/overseer-advisor/notify_construction_complete_01.ogg"
      # If multiple files, you can list them as separate soundeffect entries or use variations
  }
  soundeffect = {
      name = "advisor_fleet_detected"
      file = "sound/vo/overseer-advisor/fleet_detected_01.ogg"
  }
  # ... and so on for each advisor prompt ...
  ```
  Essentially, each in-game voice trigger (identified by `name`) is linked to one of your files. If you have multiple variants for a trigger, one approach is to list multiple `soundeffect` entries with slightly different names and then have the game call them randomly (this requires editing the voice type script, as below). Another approach is to define one soundeffect with multiple `file` entries inside, if the engine supports random selection. Mods like the Cortana advisor demonstrate that multiple lines per notification are possible ([Steam Workshop::RMPMW-Stellaris-Advisors-2.6](https://steamcommunity.com/sharedfiles/filedetails/?id=2064915149#:~:text=Everyone%27s%20favourite%20little%20blue%20girl,Advisor%20volu)).

- **Voice Type Script:** Create a text file in `sound/advisor_voice_types/`, e.g. `01_overseer_advisor.txt`. This defines the advisor as a selectable entity and maps game events to the sound names defined above. Copy the structure from a vanilla advisor script (like `01_vo_english.txt`) for all the entries (e.g. lines for `"advisor_fleet_detected" = play_sound = advisor_fleet_detected`). Update it to point to your custom sound asset names if needed. Also give your advisor a unique `key` and `texture` for its icon. For instance:
  
  ```plaintext
  advisor_voice_type = {
      key = "OVERSEER_ADVISOR"
      selection_sound = advisor_notification    # sound played when selecting this advisor
      icon = "gfx/interface/icons/advisor_overseer.dds"
      button_icon = "advisor_overseer"          # icon for the advisor selection menu
      country = { 
          # list all voice lines with corresponding sound triggers
          hostile_fleet_detected = advisor_fleet_detected
          construction_complete = advisor_notify_construction_complete
          # ... etc ...
      }
  }
  ```
  Ensure the values after `=` match the `name` fields in your .asset file. If you included multiple random variants for a line, you might list something like:
  ```plaintext
  hostile_fleet_detected = random_list = { 0.5 advisor_fleet_detected_var1  0.5 advisor_fleet_detected_var2 }
  ```
  (Pseudo-code: the idea is to have the game randomly choose one sound). Simpler is to replace each trigger with one new sound file one-to-one.

- **Integration Steps:** If you started by copying an existing voice mod (a good practice), rename all instances of the old name to your new one ([How to make Advisor Voice mods for workshop? :: Stellaris General Discussions](https://steamcommunity.com/app/281990/discussions/0/3300476731154173535/#:~:text=Then%20in%20the%20,folder)). For example, if you copied a “Futurama” advisor mod, rename its folder and files from `futurama` to `overseer`. Replace the sound files with your .ogg files (keeping the names the same as expected by the .asset) ([How to make Advisor Voice mods for workshop? :: Stellaris General Discussions](https://steamcommunity.com/app/281990/discussions/0/3300476731154173535/#:~:text=Now%20take%20a%20look%20at,advisor%22%20as%20well)). Update the `.asset` file and the `.txt` as described (using find & replace to change any old advisor key to your new key is helpful ([How to make Advisor Voice mods for workshop? :: Stellaris General Discussions](https://steamcommunity.com/app/281990/discussions/0/3300476731154173535/#:~:text=Then%20in%20the%20,folder))).

- **Localisation and Icons:** In `localisation/<language>/`, add an entry for your advisor’s display name. For example, in English:
  ```yaml
  l_english:
    advisor_overseer:0 "Overseer AI"
  ```
  (This key corresponds to the `key` you set in the advisor_voice_type script or might be automatically derived from it). Also include a localisation for a description if needed. Additionally, provide a 32x32 pixel icon DDS file for your advisor (placed in `gfx/interface/icons/` as defined by your script) so it has a proper image in the UI ([How to make Advisor Voice mods for workshop? :: Stellaris General Discussions](https://steamcommunity.com/app/281990/discussions/0/3300476731154173535/#:~:text=to%20)).

Once set up, enable your mod and you should find the new voice under Settings > Advisor in-game. Selecting it will cause your custom lines to play for the corresponding events. **Tip:** Test each line in-game to make sure triggers match (you can force events via console to hear them). By structuring your mod like this, you effectively replace or augment the existing voice lines with your own, and you can include numerous variations to keep it fresh ([Steam Workshop::RMPMW-Stellaris-Advisors-2.6](https://steamcommunity.com/sharedfiles/filedetails/?id=2064915149#:~:text=Everyone%27s%20favourite%20little%20blue%20girl,Advisor%20volu)).

## 3. Race Build (Species Traits, Civics, Government Types)

**Overview:** To truly make your machine race unique, you’ll likely introduce custom **species traits**, possibly new **civics**, and ensure the correct government type (authority) is used. Stellaris is highly moddable in these areas – you’ll be creating entries in the `common/` folder for traits and civics, and possibly species classes or authorities.

- **Species Traits:** Traits define inherent bonuses or penalties for your species. In your mod folder, create `common/traits/` and inside it a file like `00_my_machine_traits.txt` (the name isn’t critical, just ensure it doesn’t conflict). Each trait is one entry in this file. For example:
  
  ```plaintext
  trait_MY_MACHINE_INTELLECT = {
      cost = 2
      allowed_archetypes = { MACHINE }    # Only machine species can have this trait
      modifier = {
          research_speed = 0.10          # +10% research speed
      }
      initial = yes                      # Allowed at empire creation
  }
  ```
  
  This would define a positive trait that only machine archetypes can take. You can also define negative traits (with negative cost). Use `allowed_archetypes = { MACHINE }` or `{ ROBOT }` for machine pops ([Creating custom traits and civics? : r/StellarisMods](https://www.reddit.com/r/StellarisMods/comments/7wvcr0/creating_custom_traits_and_civics/#:~:text=%3E%20cost%20%3D%20,4%20and%204)). Check base game’s `00_species_traits.txt` for examples of machine traits (e.g. “Logic Engines”). **Note:** If you want these traits exclusively for your custom race, you might enforce it via traits or just trust players to use them appropriately. Each custom trait will also need an icon (DDS image in `gfx/interface/icons/traits/`) and localisation (name and description).

- **Civics:** Custom civics can represent unique doctrines or protocols of your machine empire. Create a file under `common/governments/civics/`, e.g. `00_my_machine_civics.txt`. Each civic is defined similarly to traits. For example:
  
  ```plaintext
  civic_OVERCLOCKED_NETWORK = {
      allowed_once = yes
      selectable = yes
      cost = 0
      initial = yes
      # Restrictions on who can pick this civic:
      potential = { has_authority = auth_machine_intelligence }
      # further conditions if needed (e.g. specific ethics or not hive, etc.)
      possible = { 
          NOT = { has_civic = civic_Introspective }  # example of excluding with another civic
      }
      modifier = {
          research_alternative_add = 1    # +1 research options
      }
      AI_weight = { weight = 1 }
  }
  ```
  
  The `potential` block defines which empires even see this civic as an option (here we require the empire to be a Machine Intelligence authority). For a machine race civic, you’d usually include `ethic = { value = ethic_gestalt_consciousness }` and either hive or machine authority in potential, so that normal empires cannot take it ([Creating custom traits and civics? : r/StellarisMods](https://www.reddit.com/r/StellarisMods/comments/7wvcr0/creating_custom_traits_and_civics/#:~:text=)). Use base game civics (in `00_civics.txt`) as a template – for example, find how **Rogue Servitor** or **Determined Exterminator** civics are defined to see machine-specific conditions. Don’t forget an icon (`gfx/interface/icons/governments/civics/`) and localisation for each new civic ([Creating custom traits and civics? : r/StellarisMods](https://www.reddit.com/r/StellarisMods/comments/7wvcr0/creating_custom_traits_and_civics/#:~:text=)).

- **Government & Authority:** Machine races in Stellaris typically use the **Gestalt Machine Intelligence** authority (which is `auth_machine_intelligence` in code). If your custom race is essentially a Machine Intelligence, you might not need a new authority – just ensure your empire is set to use `authority = auth_machine_intelligence` (which grants the “Machine Intelligence” government form and appropriate default civics). However, if you envision a unique form of machine government (say, a hybrid or a totally new kind of AI governance), you could mod one in by adding a new entry in `common/governments/authorities/`. This is advanced, but possible by copying the structure of `auth_machine_intelligence` and modifying as desired (e.g. different default civics, different limitations). Similarly, you could add a new **governing ethic** if truly needed, though most likely you’ll stick with Gestalt.

- **Species Class Definition:** Since this is a **machine race**, Stellaris already has a MACHINE archetype and species class. If you want a wholly separate species class (for instance, if you want to segregate your custom portraits or name list), you can add a new entry in `common/species_classes/` (e.g. define a new class `MY_MACHINE` that uses the machine archetype). For example:
  
  ```plaintext
  MY_MACHINE = {
      archetype = MACHINE
      graphical_culture = my_machine_01   # links to ship and city sets (see sections 5 and 6)
      portrait_groups = { "myMachinePortraits" }
      spawn_enabled = no
  }
  ```
  
  This would create a distinct species class. But if you simply add your portraits to the existing machine group, this step isn’t necessary. However, defining a new class allows custom **species names** (for preset empire display), unique plurals, and unique insult/compliment lines (see Diplomacy section).

- **Localisation:** For any new trait, civic, or authority, add localisation keys for their names and descriptions (e.g. `trait_MY_MACHINE_INTELLECT:0 "Overclocked Intellect"` and `trait_MY_MACHINE_INTELLECT_desc:0 "This machine's processors... [description]."`). Do the same for civics (`civic_OVERCLOCKED_NETWORK` etc.) ([Creating custom traits and civics? : r/StellarisMods](https://www.reddit.com/r/StellarisMods/comments/7wvcr0/creating_custom_traits_and_civics/#:~:text=Then%20you%27ll%20just%20need%20to,dds)). If you made a new species class, localise its name too (e.g. `MY_MACHINE:0 "Machine"` or something distinct).

By defining traits and civics in these files ([Creating custom traits and civics? : r/StellarisMods](https://www.reddit.com/r/StellarisMods/comments/7wvcr0/creating_custom_traits_and_civics/#:~:text=%3E%20cost%20%3D%20,4%20and%204)) ([Creating custom traits and civics? : r/StellarisMods](https://www.reddit.com/r/StellarisMods/comments/7wvcr0/creating_custom_traits_and_civics/#:~:text=)), you ensure your machine empire can have special abilities and options that set it apart from vanilla empires. Always test in Empire Creation: your new traits should appear under Machine traits if `allowed_archetypes = { MACHINE }` is set, and your new civics should appear when your empire has the proper authority/ethics. Keep trait and civic balance in mind relative to existing ones, and consider AI weighting if you want AI-controlled custom empires to use them.

## 4. Portraits (Animated)

**Overview:** Creating **fully animated portraits** is one of the more challenging modding tasks. Stellaris portraits (especially those from species packs) are animated 2D/3D hybrids that require models and animations. For a machine race, you have two main approaches: **re-skinning existing portraits** or **making new animated models**.

- **Using Existing Animations (Recommended):** The easiest way to get an animated portrait is to **reuse a vanilla portrait rig and simply change its textures** ([Attempting to create an animated portrait mod from StarDrive's races, looking for help/advice/suggestions : r/Stellaris](https://www.reddit.com/r/Stellaris/comments/9c5t77/attempting_to_create_an_animated_portrait_mod/#:~:text=There%20are%20tools%20for%20creating,you%27ll%20get%20tons%20of%20bugs)). Many portrait mods do this – for example, taking a humanoid model and replacing its texture to create a new alien. All Stellaris portraits are based on a set of existing models/animations, and retexturing or scaling them can produce a new look ([Attempting to create an animated portrait mod from StarDrive's races, looking for help/advice/suggestions : r/Stellaris](https://www.reddit.com/r/Stellaris/comments/9c5t77/attempting_to_create_an_animated_portrait_mod/#:~:text=Alien%20Suns%20animator%20here%2C%20can,retexturing%20and%20scaling%20can%20do)). For a machine race, identify a base portrait that suits your needs (perhaps one of the Synthetic Dawn robot portraits). You can then create new texture files (diffuse and possibly normal map) to give it a new appearance (different colors, patterns, etc.).

  - **Extracting & Editing Textures:** Find the vanilla portrait textures (in the game assets or via a tool). You’ll usually get a **.dds file** (often 512x512 or 1024x1024) for the portrait. Edit this image in Photoshop/GIMP to create your custom look (e.g. add rust, glow effects, different “face”). Save your texture as .dds (DXT5 with alpha if needed for transparency).
  - **Mod Files for Portrait:** In your mod, place the new texture in `gfx/models/portraits/` (this is where model textures reside). Next, define a new portrait in a file under `gfx/portraits/portraits/`. You can copy an existing portrait definition from `00_portraits.txt` and modify it. For example:
    ```plaintext
    portraits = {
        myMachinePortrait_01 = {
            species = "MACHINE"      # archetype or category
            texture_diffuse = "gfx/models/portraits/my_machine_diffuse.dds"
            texture_normal = "gfx/models/portraits/my_machine_normal.dds"
            portrait_state = { state = "idle" animation = "idle" }  # use existing idle animation
            entity = "robot_01_portrait_entity"
        }
    }
    ```
    Here, we reference `robot_01_portrait_entity` – a vanilla model – but apply our custom textures to it. This leverages the Paradox model and animation (blinking lights, etc.) but with your artwork. Make sure to use a unique portrait key name (not conflicting with any vanilla or other mod) ([Species modding | Stellaris Wiki | Fandom](https://stellaris.fandom.com/wiki/Species_modding#:~:text=match%20at%20L281%20WARNING%3A%20DO,prevent%20incompatibility%20with%20other%20Mods)).

  - **Portrait List and Class:** If you defined a new species class for your race, add your portrait key to that class in `common/species_classes` (the `portrait_groups`). If you’re using the existing machine species class, you can append your portrait to it via a mod file (or the `additional_portraits` field if available). This ensures the game knows your portrait belongs to machine species and will show it in the appearance selection.
  
- **Creating New Models (Advanced):** If you want a completely original design (new shape/animation), you will need to use 3D modeling and Paradox’s tools:
  - **Modeling:** Create a model in a 3D program (Blender, Maya, 3ds Max). Paradox provides a Maya exporter, and community tools like **Jorodox** can convert models to the `.mesh` format Stellaris uses. You’d have to rig the model (set up bones or animation frames) for subtle movements (machines might have flickering lights, rotating parts, etc., rather than “breathing”).
  - **Export & Asset:** Export the model to `.mesh` and any animation to `.anim`. Place these in `gfx/models/portraits/` (possibly a subfolder). Then create a portrait **.asset file** (e.g., `gfx/models/portraits/my_machine_portraits.asset`) where you define an **entity** for your portrait. For example:
    ```plaintext
    entity = {
       name = "my_machine_portrait_entity"
       mesh = "gfx/models/portraits/my_machine_model.mesh"
       state = { name = "idle"  animation = "gfx/models/portraits/my_machine_idle.anim" }
       scale = 1.0
    }
    ```
    This registers your model and ties it to an idle animation. You can reference this `my_machine_portrait_entity` in your portrait definition (instead of a vanilla entity).
  
  This process is complex – even Paradox’s own guide suggests it involves Autodesk Maya and careful rigging. It’s often easier to piggyback on an existing animation set due to the difficulty of creating new ones from scratch ([Attempting to create an animated portrait mod from StarDrive's races, looking for help/advice/suggestions : r/Stellaris](https://www.reddit.com/r/Stellaris/comments/9c5t77/attempting_to_create_an_animated_portrait_mod/#:~:text=There%20are%20tools%20for%20creating,you%27ll%20get%20tons%20of%20bugs)).

- **Rooms for Animated Portraits:** If your portrait has multiple states (like different outfits or damage states), define them in the portrait file with triggers. But for a machine, this is usually unnecessary unless you want variations.

- **Testing and Iteration:** Once your portrait is defined, launch Stellaris with your mod and see if the portrait appears in empire creation under the correct species class. Verify that animations play (if using a vanilla entity, you should see the same idle animation as that base). If something is amiss (like a blank portrait), check that the paths in the .asset and .txt match your files and that the files are the correct format (Stellaris requires DDS for textures, and make sure they’re not too large – the wiki recommends ~400px height for portraits to avoid clipping ([Species modding | Stellaris Wiki | Fandom](https://stellaris.fandom.com/wiki/Species_modding#:~:text=,of%20frame%20in%20the%20game)), though vanilla textures can be larger).

**Best Practices:** Start small – try making a static portrait first, then gradually add animation by referencing a vanilla entity. Reusing the vanilla machine portraits’ skeleton/animation is a huge time-saver ([Attempting to create an animated portrait mod from StarDrive's races, looking for help/advice/suggestions : r/Stellaris](https://www.reddit.com/r/Stellaris/comments/9c5t77/attempting_to_create_an_animated_portrait_mod/#:~:text=some%20pretty%20solid%20portrait%20mods,the%20process%20is%20much%20simpler)). For example, you could use the **Worker Drone** portrait as a base – keep its animations but give it a new “skin”. Always give unique IDs to your portraits and assets to prevent conflicts (never name your portrait `"MYSPECIES"` – that’s a reserved default ([Species modding | Stellaris Wiki | Fandom](https://stellaris.fandom.com/wiki/Species_modding#:~:text=match%20at%20L281%20WARNING%3A%20DO,prevent%20incompatibility%20with%20other%20Mods))). By carefully structuring your portrait assets, you’ll have a fully animated machine figure representing your empire in-game.

## 5. Rooms & City Graphics

**Overview:** **Empire rooms** (the background scene in diplomacy/empire creation) and **cityscapes** (the city background on colony planets and empire creation) add flavor to your race. For a custom machine race, you can create a high-tech backdrop and a unique city skyline. These involve adding images and hooking them into the game’s graphical culture.

### Empire Room (Background)

- **Creating the Image:** Design an image for the background of your ruler. This could be the interior of a machine factory, a server room, or a mechanical throne room. Vanilla rooms are 1366x768 DDS images (some use 1024x768). It’s safe to use 1366x768 or even 1920x1080. Create your art and save as **.dds** (DXT5 if it has transparency layers, though most backgrounds are opaque).
- **Adding to Mod:** Place the image in your mod under `gfx/interface/rooms/`. For example, `gfx/interface/rooms/room_my_machine.dds`.
- **Defining the Sprite:** Stellaris needs to know about the new room image. In your mod’s `gfx/interface/` directory, create a file (or append) for sprite definitions, e.g. `mod_rooms.gfx`. Inside, define a new sprite type:
  ```plaintext
  spriteTypes = {
    spriteType = {
      name = "GFX_room_my_machine"
      textureFile = "gfx/interface/rooms/room_my_machine.dds"
      noOfFrames = 1
      effectFile = "gfx/FX/buttonstate.lua"
    }
  }
  ```
  The name “GFX_room_my_machine” will be used to reference this room. This is similar to how Diverse Rooms mod adds backgrounds.
- **Making it Selectable:** By default, custom rooms might not show up in the empire creation UI unless specifically enabled. However, you can assign this room to your empire via the preset empire file (if you create a preset). For instance, in your empire definition (see section 8) include `room = "my_machine"` (where the name corresponds to your room sprite without the `GFX_room_` prefix, typically). If you want the room available for all to choose manually, you might need to override the interface that populates the room list or use a mod like Diverse Rooms as a base which unlocks custom rooms. In many cases, simply defining the sprite and using it in a preset empire works without issue ([How to use any room for your custom empire. : r/Stellaris - Reddit](https://www.reddit.com/r/Stellaris/comments/1g21c0i/how_to_use_any_room_for_your_custom_empire/#:~:text=How%20to%20use%20any%20room,example%2C%20changing%20the%20line)).

### City Graphics (Colony Skyline)

- **Multiple Images for City Levels:** Stellaris cityscapes usually have **5 images** per set, corresponding to city development level 1 through 5 (as the colony grows, more structures appear). You will need to create 5 images of the same size as vanilla city ones. The resolution for city images is typically around 3840x2160 (very large panoramas) or sometimes smaller if they are tiling sprites. A simpler approach: copy an existing city set (e.g., Mammalian) from `gfx/portraits/city_sets/` in the game files. This will give you files named like `mammalian_01_city_l01.dds` ... `l05.dds`. Use those as a base for dimensions and structure.
- **Designing City Images:** Make your city images – perhaps a sprawling machine metropolis with glowing circuits. Ensure each higher level image is an expanded version of the previous (or at least looks good when shown for a more developed planet). Save each as DDS, e.g., `my_machine_city_l01.dds` ... `my_machine_city_l05.dds`.
- **Adding to Mod:** In your mod folder, create `gfx/portraits/city_sets/`. Place the 5 DDS files there. Name them with a consistent prefix: for example `modempire_01_city_l01.dds` through `_l05.dds`. (The Reddit guide suggests using a unique prefix like “modempire_01” for your set ([How Do I Make a Custom City? : r/StellarisMods](https://www.reddit.com/r/StellarisMods/comments/6fat2k/how_do_i_make_a_custom_city/#:~:text=1,files%20of%20the%20correct%20resolution)).)
- **Graphical Culture Definition:** Now, link these images to a **graphical culture** so the game knows to use them. Create a file in `common/graphical_culture/`, e.g. `00_my_graphical_culture.txt`. Define a new culture:
  ```plaintext
  my_machine_01 = {
      city_graphical_culture = my_machine_01   # define city set name (usually same as culture key)
      city_texture = "modempire_01_city_"      # prefix for your city image files
      city_amount = 5                          # number of city levels
      spawn_odds = { weight = 0 }              # if you don't want AI random species using it
      # (Optional: ship_lighting and other parameters can go here, or fallback)
  }
  ```
  Some older guides mention putting these in `common/graphical_culture` with lighting, etc. ([How Do I Make a Custom City? : r/StellarisMods](https://www.reddit.com/r/StellarisMods/comments/6fat2k/how_do_i_make_a_custom_city/#:~:text=modempire_01%20%3D%20,1.0%200.0)). Essentially, you want to tell the game that your culture “my_machine_01” uses the city textures named `modempire_01_city_l01.dds`...`l05.dds`. Copying from a base culture file is helpful – e.g. see how `mammalian_01` is defined and mimic it, changing the texture prefix.
- **Species Class Link:** In `common/species_classes/`, ensure your species uses this graphical culture. If you made a new species class (e.g. `MY_MACHINE` earlier), set `graphical_culture = my_machine_01` in that class ([How Do I Make a Custom City? : r/StellarisMods](https://www.reddit.com/r/StellarisMods/comments/6fat2k/how_do_i_make_a_custom_city/#:~:text=3,randomized%20%3D%20no)). If you didn’t make a new species class, you can tie the city set to your empire by setting the empire’s graphical culture in its definition (for preset) or via the portrait’s defined culture. Another approach is to override the Machine species class to use your new city set (not recommended if you want to keep vanilla ones too). The simplest: use a unique species class for your custom race and assign the culture there.

- **Localisation (City Name):** This is optional, but if you want the city appearance to have a name in the appearance picker, you would localise the graphical culture. For example, add `my_machine_01:0 "Machine Metropolis"` in a localisation file ([How Do I Make a Custom City? : r/StellarisMods](https://www.reddit.com/r/StellarisMods/comments/6fat2k/how_do_i_make_a_custom_city/#:~:text=4)). This would show up if the game lists city types.

**Testing:** Start a new game and select your species. On the appearance tab, check that the city graphic displayed behind the leader corresponds to your images. As you increase the city size in-game (upgrade capital), ensure the graphics update. If something is not showing, verify the file names and the `city_texture` prefix exactly match (the game will append `l01`... etc. to that prefix). Also check the `graphical_culture` is correctly assigned. When done right, your custom machine cities will appear in all their glory, and only for your species if you set spawn_odds weight low ([How Do I Make a Custom City? : r/StellarisMods](https://www.reddit.com/r/StellarisMods/comments/6fat2k/how_do_i_make_a_custom_city/#:~:text=3,randomized%20%3D%20no)).

By creating distinctive room and city art, you give your machine empire a visual identity from the diplomacy screen to the planetary level. Use DDS format and correct sizing, and leverage the existing framework by copying and editing vanilla definitions for guidance ([How Do I Make a Custom City? : r/StellarisMods](https://www.reddit.com/r/StellarisMods/comments/6fat2k/how_do_i_make_a_custom_city/#:~:text=1,files%20of%20the%20correct%20resolution)).

## 6. Ships (Custom Shipset)

**Overview:** To complete your machine race, you may want a unique **ship set** – the models for corvettes, battleships, stations, etc. Modding ships involves 3D models and a bit of scripting to tie them into the game’s ship appearance system. This can range from simply retexturing existing ships to importing entirely new models.

- **Approach 1: Retexture/Kitbash Vanilla Ships:** If you don’t want to model from scratch, you can take an existing ship set (e.g. the Machine ship set from Synthetic Dawn or another that fits your aesthetic) and modify it. This could be as simple as recoloring the texture (e.g. adding your faction’s colors or logos) or combining pieces (kitbashing) if you’re comfortable editing models. You’d then use the existing models with new textures.

- **Approach 2: New Models:** For a truly unique shipset, you’ll need models for each ship class. You can create these or import from other sources (making sure you have permission if from another IP). Each ship class (Corvette, Destroyer, etc.) often has multiple section models (like bow, mid, stern) plus turrets. However, simpler approach: create one model per class as a whole.

- **File Structure:**  
  - Put your ship model files (`.mesh` for the hulls, `.mesh` for turrets if any) in a new folder under `gfx/models/ships/`. For example, `gfx/models/ships/my_machine_set/` containing files like `my_machine_corvette.mesh`, `my_machine_corvette_diffuse.dds`, `my_machine_corvette_normal.dds`, etc.
  - Create a **ship asset file** in `gfx/models/ships/`, e.g. `my_machine_ships.asset`. This file will define the entities for all your ships and link the models and textures. For example:
    ```plaintext
    mesh = {
      name = "my_machine_corvette_mesh"
      file = "gfx/models/ships/my_machine_set/my_machine_corvette.mesh"
    }
    entity = {
      name = "my_machine_01_corvette_entity"
      mesh = "my_machine_corvette_mesh"
      scale = 1.0
      rotation = { 0 0 0 }
      # attach points for weapons, e.g. locator = "hardpoint_01", etc.
    }
    ```
    Do this for each ship size (corvette, destroyer, cruiser, etc.), each with a unique `entity` name.
  
- **Graphical Culture and Ship Appearance:** Stellaris uses the **graphical culture** of a species to determine which ship models to use. Earlier, we set `graphical_culture = my_machine_01` for our species. Now we must define what that culture’s ships are. This is done in `common/ship_appearance/` or via naming convention:
  
  The game looks for an entity name matching `<graphical_culture>_<ship_size>_entity`. For example, if a species has `graphical_culture = my_machine_01` and is building a corvette, the game will look for `my_machine_01_corvette_entity`. We defined that in our asset file above. This is how the engine links the ship to your model ([Creating new ships : r/StellarisMods](https://www.reddit.com/r/StellarisMods/comments/6elp9l/creating_new_ships/#:~:text=Graphically%20the%20ship%20is%20structured,their%20name%20as%20a%20prefix)). So it’s crucial your entity names follow this pattern. Do this for all classes: e.g. `my_machine_01_destroyer_entity`, `my_machine_01_station_entity` (for starbase), etc., each pointing to the appropriate model. 

  Alternatively, you can explicitly define a ship set in `common/ship_appearance/` by copying a file like `00_ship_appearances.txt` and adding an entry:
  ```plaintext
  shipset_my_machine = {
      species_gfx = my_machine_01
      entity = "my_machine_01"
      # ... possibly other overrides ...
  }
  ```
  But using the naming convention with graphical culture is usually sufficient for custom species.

- **Weapon Turrets:** If you want custom turret models (the little guns that appear on ships), you need to define those as well in the asset and ensure your ship entity has locators (attachment points) named in the model. You can reuse vanilla turret models or make new ones. The game will attach weapons based on the `locatorname` specified in component slots (if your model has a locator called "large_gun_01", it will try to attach a turret entity with that name and your culture prefix). For simplicity, you might skip custom turret models and use the default glow points or existing turrets.

- **Engine Plumes and Effects:** The color of engine trails and lights is determined by `ship_color` in graphical culture and the empire's flag color. Our earlier graphical culture example included `ship_color = yes` and some lighting parameters ([How Do I Make a Custom City? : r/StellarisMods](https://www.reddit.com/r/StellarisMods/comments/6fat2k/how_do_i_make_a_custom_city/#:~:text=modempire_01%20%3D%20,1.0%200.0)). If you want custom engine glow colors irrespective of flag, you’d have to adjust materials or use special shaders. This can get complex, so using the default system (which gives machines a cyan glow, for example) is fine.

- **Testing Ships:** This is important – spawn your ships in-game (use console commands to instantly create fleets of each type). Check that models appear and are not invisible or mis-scaled. If a model doesn’t show, ensure the entity name matches exactly what the game expects (check error.log for missing entity errors). Also ensure textures are in the right place and the `.asset` file is being loaded (list it in your `descriptor.mod` if needed, though generally all .asset in gfx/ are loaded).

**Tools for Models:** If creating or editing models, **Blender** with the `.mesh` plugin or using **Jorodox** (a mod tool to import/export .mesh) is very useful. These allow you to import existing ship models to use as reference and export your own. Keep polygon counts reasonable and use existing ships as a guide for scale.

**Best Practices:** Use a unique prefix for all your entities and meshes to avoid conflicts. Re-use as much as you can (for instance, if destroyer and cruiser can use the same model scaled differently, do that to save effort). Also set `fallback = <some vanilla set>` in your graphical culture ([How Do I Make a Custom City? : r/StellarisMods](https://www.reddit.com/r/StellarisMods/comments/6fat2k/how_do_i_make_a_custom_city/#:~:text=modempire_01%20%3D%20,1.0%200.0)), so if anything fails or if another mod expects a vanilla set, the game knows what to use. For example, `fallback = mammalian_01` means if your model is missing for some reason, it shows mammalian ships instead of nothing.

By following the naming conventions and setting up the asset and culture files, you essentially “plug in” your shipset. The game then treats your machine empire like any other, pulling the correct models for each ship size from your definitions ([Creating new ships : r/StellarisMods](https://www.reddit.com/r/StellarisMods/comments/6elp9l/creating_new_ships/#:~:text=Graphically%20the%20ship%20is%20structured,their%20name%20as%20a%20prefix)). This is one of the most impressive parts of a total conversion mod – seeing your custom fleet design in action.

## 7. Event Responses (Custom Event Text)

**Overview:** To deepen immersion, you can customize **event text** and responses for your machine race. This can mean changing how certain events are described or adding new options that only your machine empire would consider. Stellaris events are defined in `.txt` files in the `events/` folder, with text in localisation. We will focus on adjusting text for existing events to reflect a machine perspective.

- **Identify Events to Change:** Some narrative events assume a biological perspective (talk of food, sleep, etc.) which might not fit a machine. Make a list of such events. Use the Stellaris wiki or in-game console (`debugtooltip` to get event IDs) to find the event script and localisation keys. For example, the **“Doorway” event** has different text for robots and hive minds via triggers in the description ([The Doorway event: Someone forgot to bring their clone vats!](https://forum.paradoxplaza.com/forum/threads/the-doorway-event-someone-forgot-to-bring-their-clone-vats.1565289/#:~:text=The%20Doorway%20event%3A%20Someone%20forgot,colony.9850.desc.hive)).

- **Overriding Event Text:** You have two main ways:
  1. **Via Localisation:** If you simply want to change phrasing for your race without affecting gameplay, you can override the localisation for that event’s description or option when your empire meets certain criteria. However, localisation files themselves can’t do conditional text – the conditions must be in the event script.
  2. **Via Event Script:** The robust way is to override or duplicate the event in the `events` script and use triggers to show different text. For instance:
     ```plaintext
     event = {
       id = anomaly.1234
       title = "anomaly.1234.name"
       desc = {
           trigger = { owner = { is_machine_empire = yes } }
           localization_key = "anomaly.1234.desc.MACHINE"
       }
       desc = {
           trigger = { owner = { is_machine_empire = no } }
           localization_key = "anomaly.1234.desc.DEFAULT"
       }
       # ... event effects ...
     }
     ```
     In the above pseudo-code, the event description will use `anomaly.1234.desc.MACHINE` if the empire owning the event is a machine empire, otherwise it falls back to the default text. Stellaris allows multiple `desc` blocks with triggers, using the first that matches ([The Doorway event: Someone forgot to bring their clone vats!](https://forum.paradoxplaza.com/forum/threads/the-doorway-event-someone-forgot-to-bring-their-clone-vats.1565289/#:~:text=The%20Doorway%20event%3A%20Someone%20forgot,colony.9850.desc.hive)). You can do the same for event **options** using `option = { trigger = { is_machine_empire = yes } name = "anomaly.1234.A.MACHINE" ... }` to have a different button text/outcome.

- **Implementing the Changes:** Create a new file in your mod’s `events` folder, perhaps `machine_empire_events.txt`. You can **redefine an existing event** by using the same event ID. Stellaris will overwrite the vanilla event with yours (this might disable achievements and could conflict with other mods, but if it’s for your standalone mod, it’s fine). Alternatively, use the **replace** system in the mod descriptor for the file, but usually just duplicating the ID works. Within your version of the event, add the triggered descriptions and any unique options.

- **Add New Options/Effects:** Maybe your machine race would react differently, e.g., in an event about an alien disease, a machine empire might have an option to *ignore it* (being immune). You can add an `option` available only if `is_machine_empire = yes`, with its own outcome (perhaps giving a different modifier or skipping a penalty). Always include a default option for non-machine (or leave the vanilla ones in place under a negated trigger).

- **Localisation for New Text:** Any new localisation keys you referenced (like `anomaly.1234.desc.MACHINE`) must be added to your localisation files. Provide the text from the machine perspective. For example:
  ```yaml
  l_english:
    anomaly.1234.desc.MACHINE:0 "Our central units record a phenomenon but as machines, it poses no biological threat. We catalog the data calmly."
    anomaly.1234.A.MACHINE:0 "Log and Continue (Machine logic)"
  ```
  You can copy the original text and tweak it to sound more synthetic (e.g., replace "our crew is terrified" with "sensors register parameters outside norm").

- **Testing Events:** Use console commands (`event anomaly.1234` with a machine empire selected) to trigger the event and see if your text appears. Check that your conditions work as intended. Also ensure that for non-machine empires, either your mod doesn’t affect them or it provides their appropriate text (don’t accidentally leave them with a blank because you overrode an event and didn’t include the default desc properly).

**Best Practices:** Only override what you need. It’s better to *add conditional branches* rather than completely rewriting an event, to maintain compatibility. Use `is_machine_empire` (true for Machine Intelligence authorities) or `has_country_flag = my_custom_empire` if you want to target only your specific empire (you could set a country flag on game start via an event if your empire is detected). This way, generic machine empires also benefit from the flavor if appropriate, but you can narrow it to just your mod’s empire if desired.

By customizing event descriptions and choices, players controlling your machine race will get tailored storytelling that acknowledges their mechanical nature. This adds a lot of flavor and can even affect gameplay if you introduce new options for machines.

## 8. Custom Diplomacy (AI Dialogues and Responses)

**Overview:** Diplomacy text in Stellaris – greetings, insults, compliments, etc. – can also be customized for your machine race. This involves localisation keys related to species classes and possibly AI personality dialog. We’ll focus on making sure other empires address your machines appropriately (and vice versa).

- **Species Class Insults/Compliments:** Stellaris has a system to generate insults or compliments based on species class. By adding entries for your custom species class, you can define what aliens call your machines. For example, if your species class key is `MY_MACHINE`, you can add in localisation:
  ```yaml
  l_english:
    MY_MACHINE_insult_01:0 "rust bucket"
    MY_MACHINE_insult_02:0 "heap of circuits"
    MY_MACHINE_insult_plural_01:0 "scrap heaps"
    MY_MACHINE_compliment_01:0 "efficient construct"
    MY_MACHINE_compliment_plural_01:0 "noble machines"
  ```
  You can add multiple numbered insults; the game will randomly pick one when an AI empire insults you ([Species modding | Stellaris Wiki | Fandom](https://stellaris.fandom.com/wiki/Species_modding#:~:text=%2A%20,for)). Make sure to provide both singular and plural forms (how they refer to one machine being or many). These keys need to match the species class name (or archetype). If you reused the MACHINE archetype, you’d use `ROBOT_insult_01` etc. However, since “Machine” is vanilla, Paradox already has some lines (“Toaster” insults, etc.). Using a new class key allows you to be creative without overriding vanilla.

- **Diplomatic Phrases:** Aside from one-liner insults, you might want to adjust the first-contact intro or other diplomacy phrases. These are often governed by AI personality (e.g. *Ruthless Capitalist, Determined Exterminator* have unique lines). If your custom machine race has a unique AI personality (for AI-controlled version) or just for flavor, you can add a new personality in `common/personalities/` and define its dialogue lines in localisation (look at `localisation/english/dip_messages_l_english.yml` for the structure). This is complex, but for example, you could define a personality "Overseer Matrix" that speaks in a collective, monotone way.

- **AI Attitude Modifiers:** Machines might provoke different AI attitudes (e.g., organics might fear them more). These are defined in `common/opinion_modifiers/` and `common/diplo_phrases/`. For instance, there’s an opinion modifier for organics vs machines. You can tweak or add new ones if your race should inspire a special reaction (like a +50 opinion boost from other machines if they see you as kin).

- **Custom Greetings:** If you want a custom **diplomatic greeting** when another empire meets yours, you could override the first contact event or localisation. For example, the first contact message often says "*We are XYZ, we wish for peaceful coexistence*..." – you could make a variant that a machine empire would send: "*We are the Consciousness of XYZ, you will be catalogued.*" Achieve this by editing the first contact event (`first_contact.1` etc.) similar to event editing above, using triggers for machine authority.

- **Integration via Species Class:** The simplest and most straightforward way to ensure custom diplomacy flavor is through the species class localisation we mentioned. In addition to insults and compliments, there are also keys like:
  - `<CLASS>_spawn` (what newborns are called),
  - `<CLASS>_organ` (a notable organ - for machines maybe "circuit"),
  - `<CLASS>_mouth` (speaking organ - for machines maybe "vocoder" or "transmitter"),
  - `<CLASS>_hand` (manipulating organ - maybe "manipulator arm").
  
  These are used in certain diplomatic contexts and events. For example, an alien might say "You dirty <CLASS_insult>!" or "By the <CLASS_organ> of the Great Machine, we swear peace." Filling these in makes language consistent ([Species modding | Stellaris Wiki | Fandom](https://stellaris.fandom.com/wiki/Species_modding#:~:text=CLASS_insult_01%3A0%20,X)) ([Species modding | Stellaris Wiki | Fandom](https://stellaris.fandom.com/wiki/Species_modding#:~:text=CLASS_organ%3A0%20,X)). For a machine, you might use metaphorical or literal terms ("core", "logic array", etc.). The Stellaris wiki provides a template of all these keys for species class localisation ([Species modding | Stellaris Wiki | Fandom](https://stellaris.fandom.com/wiki/Species_modding#:~:text=l_english%3A%20CLASS%3A0%20,X)) ([Species modding | Stellaris Wiki | Fandom](https://stellaris.fandom.com/wiki/Species_modding#:~:text=CLASS_insult_plural_01%3A0%20,X)) – you can use that as a checklist.

- **Example:** Suppose your machine race is called *Omni Consciousness* of class `OMNI_MACHINE`. You could define:
  ```yaml
  l_english:
    OMNI_MACHINE_insult_01:0 "walking calculator"
    OMNI_MACHINE_insult_plural_01:0 "walking calculators"
    OMNI_MACHINE_compliment_01:0 "marvel of engineering"
    OMNI_MACHINE_compliment_plural_01:0 "wonders of engineering"
    OMNI_MACHINE_organ:0 "core processor"
    OMNI_MACHINE_mouth:0 "voice emitter"
    OMNI_MACHINE_hand:0 "manipulator"
  ```
  Now, when an AI empire tries to insult your machines, it might call them "walking calculators" – a nice custom touch that differs from stock insults. You can add multiple variants (just increase the number) ([Species modding | Stellaris Wiki | Fandom](https://stellaris.fandom.com/wiki/Species_modding#:~:text=%2A%20,for)).

- **Diplomacy Responses:** If you want your *own* empire’s responses to be unique when you, say, insult someone or respond to a diplomatic proposal, that’s governed by your empire’s personality and authority. Machine intelligences already have some unique lines (for example, machine gestalt drones speak differently than humans). If you made a custom authority, define its diplomatic phrases in localisation (search vanilla localisation for lines containing `machine_intelligence` to see examples). You might not need to change this unless you want something specific.

In summary, adjust the **species class localisation** for flavor terms and consider adding an AI personality if needed for deeper custom dialogues. Most of the heavy lifting for machine-specific diplomacy is handled if you use the existing Machine Intelligence framework (AI will treat you as a gestalt, etc.). Your job is mainly to provide the *flavor text* that makes interactions feel bespoke. With keys for insults and compliments in place, and any event text variations, your custom race will talk the talk – sounding like a machine empire in every diplomatic exchange.

---

**Conclusion:** By following the above steps for each aspect, you will have created a comprehensive mod for a custom machine race in Stellaris. You defined new name lists, integrated custom voiceovers for an AI advisor, built unique traits and civics to shape your machine society, added animated portraits or repurposed existing ones, crafted visual assets for cities and rooms, built a custom shipset, tailored event narratives, and adjusted diplomacy dialogue. The mod folder structure should mirror Stellaris’s own (common, gfx, sound, events, localisation, etc.), containing your new content in the appropriate directories. Always double-check the syntax and run the game with `-debug` launch option to catch errors in the error.log. Modding Stellaris can be intricate due to the many systems involved, but the result – seeing your handcrafted machine civilization operate with custom art and behavior – is incredibly rewarding. Good luck with your mod, and enjoy watching your mechanical race conquer the stars!

**Sources:**

- Stellaris Modding Wiki and community guides for file formats and examples ([Creating custom traits and civics? : r/StellarisMods](https://www.reddit.com/r/StellarisMods/comments/7wvcr0/creating_custom_traits_and_civics/#:~:text=%3E%20cost%20%3D%20,4%20and%204)) ([Creating custom traits and civics? : r/StellarisMods](https://www.reddit.com/r/StellarisMods/comments/7wvcr0/creating_custom_traits_and_civics/#:~:text=)) ([Creating new ships : r/StellarisMods](https://www.reddit.com/r/StellarisMods/comments/6elp9l/creating_new_ships/#:~:text=Graphically%20the%20ship%20is%20structured,their%20name%20as%20a%20prefix)).  
- Reddit discussions and Steam forums for practical modding advice (name lists, voice packs, city sets, etc.) ([How to create custom name lists? : r/Stellaris](https://www.reddit.com/r/Stellaris/comments/17sykck/how_to_create_custom_name_lists/#:~:text=It%27s%20pretty%20simple%20as%20the,are%20all%20just%20text%20files)) ([How to make Advisor Voice mods for workshop? :: Stellaris General Discussions](https://steamcommunity.com/app/281990/discussions/0/3300476731154173535/#:~:text=Now%20take%20a%20look%20at,advisor%22%20as%20well)) ([How to make Advisor Voice mods for workshop? :: Stellaris General Discussions](https://steamcommunity.com/app/281990/discussions/0/3300476731154173535/#:~:text=Then%20in%20the%20,folder)) ([How Do I Make a Custom City? : r/StellarisMods](https://www.reddit.com/r/StellarisMods/comments/6fat2k/how_do_i_make_a_custom_city/#:~:text=1,files%20of%20the%20correct%20resolution)).  
- Insights from experienced modders on using existing assets for portraits and animations ([Attempting to create an animated portrait mod from StarDrive's races, looking for help/advice/suggestions : r/Stellaris](https://www.reddit.com/r/Stellaris/comments/9c5t77/attempting_to_create_an_animated_portrait_mod/#:~:text=There%20are%20tools%20for%20creating,you%27ll%20get%20tons%20of%20bugs)) ([Attempting to create an animated portrait mod from StarDrive's races, looking for help/advice/suggestions : r/Stellaris](https://www.reddit.com/r/Stellaris/comments/9c5t77/attempting_to_create_an_animated_portrait_mod/#:~:text=Alien%20Suns%20animator%20here%2C%20can,retexturing%20and%20scaling%20can%20do)).  
- Paradox forum and wiki information on localisation keys for species classes and dynamic text ([Species modding | Stellaris Wiki | Fandom](https://stellaris.fandom.com/wiki/Species_modding#:~:text=%2A%20,for)).