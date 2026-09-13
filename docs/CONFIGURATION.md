# Maintained configuration

The exact settings live in `pack/`; a mod's generated configuration can contain additional defaults.

| Area | Pack choice |
| --- | --- |
| Terrain | Tectonic + Terralith, ordinary default world type; Y -64 to 320; larger continents and deeper oceans |
| Tectonic | Vertical scale 1.2, elevation boost 0.15; continent scale 0.11, ocean offset -0.95; ocean/deep-ocean depth -0.32/-0.75 |
| Nuclear ores | Uranium: 2 attempts, Y -64..-8, bottom-biased; lead: 4 attempts, Y -48..32, uniform; striated deposits: rarity 48, Y -56..0, bottom-biased |
| Deep Seas | Its additional ocean deepening is off; retained hull/pressure behavior is unchanged |
| Structures | IDAS included with Labyrinth mining fatigue off; CSA global multipliers 0.7 and 1.0 |
| Logging | Only CSA's repetitive DEBUG logger is filtered; warnings/errors and other diagnostics remain |
| DH | Radius 128; 4 worker threads at 75% runtime for new installations; existing settings preserved; PRE_EXISTING_ONLY generation |
| DH transfer | No server bandwidth caps for new installations; existing servers need a manual change |
| Map sharing | MapSyncer 1.0.3; generated terrain shared, TICK updates every 6000 ticks; per-world defaults |
| Display | Borderless fullscreen, VSync/shaders off, 120 FPS cap, 12-chunk render/simulation distance |
| Shaders | Three downloaded archives: Bliss and two Complementary variants; installed patchers generate additional choices |
| Java | Java 21 Generational ZGC arguments supplied by the Prism instance; new beta Prism instances use a 12 GiB maximum heap |
| Integration | Existing continuity recipes/filters and four Tracks loot/tag corrections retained; quests remain retired |

Ore attempts and terrain settings are not guaranteed yields or geometry. This
world line began as a fresh save and does not provide an RC8 world conversion.

Files marked `preserve = true`, including `options.txt` and the DH configuration,
retain existing player edits. To inspect which files are managed or preserved,
read `pack/index.toml`. Other config changes should be limited to intentional
pack defaults, not copied generated state. Never distribute a DH server identity,
LOD database, account, world or private server data.
