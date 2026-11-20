# Goblin Mod — Minecraft 1.21.1 / NeoForge

Development source project targeting NeoForge 21.1.172, Java 21 and GeckoLib 4.9.3.

## Included features
- Goblin entity based on the supplied Blockbench geometry and embedded 64×64 texture.
- Spawn Egg item model using the supplied spawn-egg image as its texture.
- GeckoLib idle, walk and melee attack animation definitions.
- Five original OGG/Vorbis sound assets: idle, alert, attack, hurt and death.
- English and Persian (fa_ir) names and sound subtitles.
- Target goals for players, villagers, iron golems, piglins, piglin brutes and illagers. Goblins are not included as targets.
- Stone sword (70%) / stone axe (30%) equipment selection.
- Goblin does not burn in sunlight.
- Biome spawn modifier/tag for plains, forests, taiga and selected cave biomes.

## Requirements
- 64-bit Java 21 JDK
- Gradle 8.8 or newer (Gradle 8.10.2 is suitable)
- Internet access on the first Gradle build so Gradle can download Minecraft/NeoForge/GeckoLib dependencies

## Windows build
1. Install a Java 21 JDK and Gradle 8.10.2 or newer.
2. Open PowerShell or Command Prompt in this `GoblinMod` folder.
3. Confirm `java -version` reports 21 and `gradle --version` runs.
4. Run `gradle build`.
5. If successful, find the mod JAR in `build\libs\`.

You can also double-click `build_windows.bat` after installing Java and Gradle. It runs `gradle clean build` and keeps the console open so errors remain visible. On Linux/macOS, run `./build_linux.sh`.

## Offline resource validation
Run `python validate_assets.py`. It checks JSON syntax, animation-to-geometry bone references, PNG signatures/dimensions and OGG/Vorbis decoding (when ffprobe is installed). This is not a substitute for compiling Java or testing in Minecraft.

## Important validation status
This archive is a development source snapshot, **not a verified release JAR**. Java 21 is available in the preparation environment, but Gradle is not installed and outbound DNS/network access to the Gradle distribution host is unavailable. Therefore a NeoForge compile and an in-game test have not been completed here. After building, inspect UV orientation, held-item placement, spawn behavior, animation timing and sound playback in Minecraft 1.21.1. The mod requires GeckoLib 4.9.3 (or compatible 4.9.x) in the mods folder at runtime.

## Build without installing anything (GitHub Actions)
Upload this folder to a new GitHub repository. The workflow in `.github/workflows/build.yml` builds the mod automatically; download the JAR from the run's **Artifacts** section (`goblin-mod-jar`). GeckoLib 4.9.3 must still be placed in the `mods` folder together with the Goblin JAR (NeoForge 21.1.x, Minecraft 1.21.1).

## Changes in this revision (not compiled here)
- Removed an invalid `isSunSensitive` override (Monster mobs do not burn in sunlight by default).
- Added `finalizeSpawn` so the stone sword/axe is actually equipped.
- Registered a spawn placement (ground, monster light rules) so natural spawns work correctly.
