# Maintained configuration

The exact settings live in `pack/`; a mod's generated configuration can contain additional defaults.

| Area | Pack choice |
| --- | --- |
| Terrain | Tectonic + Terralith, ordinary default world type; Y -64 to 320; larger continents and deeper oceans |
| Tectonic | Vertical scale 1.2, elevation boost 0.15; continent scale 0.11, ocean offset -0.95; ocean/deep-ocean depth -0.32/-0.75 |
| Nuclear ores | Uranium: 2 attempts, Y -64..-8, bottom-biased; lead: 4 attempts, Y -48..32, uniform; striated deposits: rarity 48, Y -56..0, bottom-biased; Nuclear 2.0.0 thorium and nitrate use upstream defaults |
| Deep Seas | 3.3.0 with additional ocean deepening off and startup screens disabled; hull, pressure and High Seas settings use upstream defaults |
| Structures | IDAS included with Labyrinth mining fatigue off; CSA global multipliers 0.7 and 1.0 |
| Logging | Only CSA's repetitive DEBUG logger is filtered; warnings/errors and other diagnostics remain |
| DH | Radius 128; 4 worker threads at 50% runtime for new installations; existing settings preserved; PRE_EXISTING_ONLY generation |
| DH transfer | No server bandwidth caps for new installations; existing servers need a manual change |
| Map sharing | MapSyncer 1.0.4beta1 from the official GitHub release, pinned by checksum; client autosync and server incremental updates disabled by default; manual sync remains available; distant synchronized regions retained on disk and loaded by Xaero only when viewed |
| Display | Borderless fullscreen at desktop resolution, VSync off, 120 FPS cap, render distance 12 and simulation distance 8 |
| Shaders | Complementary Reimagined 5.8.1 preselected, shaders initially disabled; Reimagined, Unbound 5.8.1 and Bliss 2.1.2 ship tuned first-install presets |
| Controls | Beta shader reload defaults to F8; weapon reload remains R; other bindings use upstream defaults. See [Player controls](CONTROLS.md) for assignments and shared keys |
| Update notifications | Xaero Minimap and World Map notifications disabled; NeoForge version checks, Collective checks, DH auto-updates, Iris messages and Euphoria update checks/messages also disabled |
| Resource packs | Create Ultra 2.1, Improved Create 32x 0.06, Upscaled Supplementaries 32x 1.2 and Patrix 32x release 72 enabled by default in that priority order; exact client-only Modrinth artifacts managed by Packwiz |
| Java | Java 21 Generational ZGC arguments supplied by the Prism instance; new beta Prism instances use a 12 GiB maximum heap |
| Integration | Existing continuity recipes/filters and four Tracks loot/tag corrections retained; quests remain retired |

Ore attempts and terrain settings are not guaranteed yields or geometry. This
world line began as a fresh save and does not provide an RC8 world conversion.

Experimental uses Create Nuclear 2.0.0 with upstream reactor, radiation and
configuration changes. Test existing reactors and saved-world upgrades separately;
a fresh-world MVT lifecycle does not verify migration.

Files marked `preserve = true`, including `options.txt` and the DH configuration,
retain existing player edits. To inspect which files are managed or preserved,
read `pack/index.toml`. Other config changes should be limited to intentional
pack defaults, not copied generated state. Never distribute a DH server identity,
LOD database, account, world or private server data.

Existing players can adopt the shader-reload change through **Options → Controls
→ Key Binds → Reload Shaders → F8**. Only the fresh-install `options.txt` contains
this override; preserved player options are not overwritten. Iris's reset-to-default
binding is still R, so assign F8 again if you reset it.

The first-start baseline targets a 4-core/8-thread CPU or better, 32 GB system RAM,
a GTX 1080 8 GB and 1920x1080 display. Use Java 21 with a recommended 12 GiB maximum
heap (Prism supplies 1024 MiB minimum, 12288 MiB maximum and Generational ZGC).
The roughly 60+ FPS gameplay goal is a target, not a measured performance guarantee.

Both Complementary presets use labPBR, moderate POM and a high-quality baseline,
with Advanced Color Tracing, world-space reflections and motion blur off. Bliss
uses labPBR-compatible materials and moderate POM, with LPV, the expensive DH
shadow map, screen-space reflections and motion blur off. These settings were
checked against the shipped shader sources; in-game export and visual checks
remain necessary. Complementary's `COLORED_LIGHTING=0` is its shipped default/off
value even though its source's explicit distance list starts at 128.

Use a fresh isolated Beta instance to evaluate all defaults together. The eight
preserved defaults covered here are Minecraft options, Iris settings, DH settings, borderless-window
settings, MapSyncer's client settings and the three shader preset sidecars. Existing copies retain player
settings; missing files receive the new defaults. Minecraft serializes the lowest
priority first: vanilla and generated mod packs are followed by Patrix, Upscaled
Supplementaries, Improved Create and Create Ultra. The resource-pack screen displays
those four custom packs in the reverse order, with Create Ultra at the top.

Client acceptance testing should cover dense Create machinery, moving contraptions,
DH loading, rain/night, the Nether and the End, plus large-area MapSyncer transfers.
Verify the intended Colorwheel backend using `/flywheel backend` with each shader.
If GPU performance misses the target, reduce or disable POM first, then lower shader
quality. A dedicated-server MVT pass does not verify these client behaviors.

## Mod update notifications

Packwiz supplies the reviewed mod versions. New installations disable Xaero's
update notifications with `update_notifications = false` in both
`config/xaero/minimap/client.cfg` and `config/xaero/world-map/client.cfg`.
The shipped Xaero versions require an equals sign; the previous colon-separated
lines were ignored.

Both files remain preserved so personal map settings are retained. Existing
players should turn **Update Notifications** off in each mod's settings, or close
Minecraft and set that line to `false` in both files. Pack updates do not overwrite
an existing preserved file, including one created with the previous syntax.

NeoForge version checks, Collective update checks, Distant Horizons auto-updates,
Iris update messages, Euphoria update checks and shader messages, and Deep Seas
startup screens are also disabled by the supplied settings. These choices do not
prevent the normal Packwiz update at launch. Existing preserved files can retain
different choices.

## Deep Seas and High Seas

Beta uses Create Deep Seas 3.3.0, including its High Seas content. The pack keeps
`gameplay.enableDeeperOceans = false` in `config/create_submarine-common.toml`
so Tectonic continues to own ocean geometry. Hull strength, pressure, flooding,
boat engines and sails use this release's upstream defaults.

Version 3.3.0 separates common, server and client settings. The startup-screen
choice now lives in `config/create_submarine-client.toml` as
`client.disableStartupScreens = true`. Packwiz preserves this client file;
existing installations with their own file must set that value themselves if
they want to suppress the screens. Server settings are generated per world in
`serverconfig/create_submarine-server.toml`; no generated hull or server settings
are supplied by the pack.

The [upstream compatibility notes](https://github.com/MaxCreateMC/Create-Deep-Seas#compatibility)
describe limitations with Iris: sonar/alarm coloured Veil lights are disabled,
and sails do not billow while a shader pack is active. Keep the pack's Colorwheel
setup; the author [confirms Iris/Flywheel Compat is optional](https://github.com/MaxCreateMC/Create-Deep-Seas/issues/93).
WaterWorks breaks interior water culling, but is not part of this pack.

Before promotion, test large ships and submarines, ballast and oxygen systems,
water culling with Sodium/Iris/Colorwheel/Distant Horizons, sails and boat engines,
and upgraded saved structures. Upstream reports include
[large-sublevel server lag](https://github.com/MaxCreateMC/Create-Deep-Seas/issues/98)
and an [oxygen-system duplication bug](https://github.com/MaxCreateMC/Create-Deep-Seas/issues/99);
these are reports to evaluate, not reproduced pack failures. A fresh server
lifecycle cannot validate these behaviors or existing-world upgrades.

## Guns and vehicle linkage

Beta includes the unofficial TaCZ NeoForge port 1.1.8-hotfix-r7, TaCZ Tweaks
3.0.0-alpha.10, Create Aeronautics: Transmission & Linkage 0.2.8, and
Create Aeronautics: Toolgun 0.3.6. These are
required on both clients and servers. Guns, ammunition, recipes, damage and
movement use the installed mods' upstream defaults; no extra gun or example
interaction packs are supplied. Transmission & Linkage and Toolgun use upstream settings.

The pack supplies `config/tacztweaks.json` with configuration `version` 1,
`general.compatibility.forceDisableCrawl` set to `true`, and
`general.compatibility.sableCompat` set to `true`. This disables TaCZ's crawl
system and enables Tweaks' Sable integration for Aeronautics structures.
Other settings use upstream defaults.
The file is preserved by Packwiz so later player or server edits are retained.
For installations that already have this file, close the client or stop the server
and set both `forceDisableCrawl` and `sableCompat` to `true` inside the existing
`general.compatibility` object. Retain the other settings. New installations
receive the pack default.

On multiplayer servers, TaCZ Tweaks synchronizes these compatibility settings from
the server. Enable them on the server as well as clients; a client-only change does
not override the server. Operators with permission level 2 can change synchronized
settings through the mod's configuration screen.

Gun rendering with shaders, key bindings, multiplayer synchronization, hits and
explosions on moving Sable structures, and linkage physics need in-game testing.
Dedicated-server lifecycle checks do not establish those behaviors.

## Electricity

Experimental includes [World-Wide Power Grid 0.2.4](https://github.com/Cha0sCollective/World-Wide-Power-Grid/releases/tag/0.2.4)
on clients and servers, with CEE 1.21.1-1.1.3 and Power Grid 0.6.2. The pack keeps
NeoForge 21.1.262, Create 6.0.10 and Architectury 13.0.11. WWPG's embedded dependency
ranges accept these versions; the full pack still needs player compatibility testing.

`defaultconfigs/powergrid-server.toml` sets `[electricity.solver]` to
`solverBackend = "NATIVE"` and `multiTicks = 16` for fresh worlds. Other Power Grid
values use upstream defaults. Existing worlds retain their generated server config:
stop the server or game, edit those settings in the generated
`config/powergrid-server.toml` (or `<world>/serverconfig/powergrid-server.toml`
if the installation uses world-local server configs), and restart. CEE's `microTicks` does
not control the simulation schedule with WWPG installed.

WWPG 0.2.4 loads its verified guarded native v7 engine from a checksum-named
folder within `.pg-native`, preserving administrator-installed files. Its tested
native platforms are Windows x86-64 with AVX2 and Linux x86-64 with AVX2 on
Ubuntu 24.04; other Linux distributions remain unverified upstream. Failure to
load the bundled guarded engine disables native support and reports the problem.
Power Grid's Java solver remains available as an operator-selected alternative.
Use operator commands `/wwpg` and `/wwpg errors` to inspect actual backend activity
and compatibility diagnostics. Native selection alone does not prove it was used.

Stationary circuits are the release's supported scope. Moving Sable systems,
large networks, mixed-machine behavior and real client rendering require testing
in an isolated Experimental instance. No example worlds, SDKs or example add-ons
are installed by the pack.

## Experimental loader and admin configuration

Experimental requires NeoForge **21.1.262** for Quark 4.1-487 and the modules
bundled with Forgified Fabric API 0.116.15+2.3.6. Packwiz does not upgrade an
existing Prism or AMP loader; use the current Experimental ZIP or update NeoForge
manually before launching. Java 21 and the maintained configuration defaults remain unchanged.

FTB Library 2101.1.37 requires operator permission level **4** to synchronize
server configuration changes through its GUI, replacing the earlier level 2 check.

## MapSyncer synchronization defaults

Fresh client settings set `[client] autoSyncEnabled = false`. New worlds use
`[incremental_update] incrementalUpdateMode = "DISABLED"` in the server template.
Manual `/mapsyncer sync` remains available. The 6000-tick interval is retained but
inactive while incremental updates are disabled.

Packwiz preserves existing `config/mapsyncer-client.toml` files, so current players
can use `/mapsyncer autosync off` or set `autoSyncEnabled = false` themselves.
Existing worlds retain their server config; stop the server, set
`incrementalUpdateMode = "DISABLED"` in `<world>/serverconfig/mapsyncer-server.toml`,
and restart. Updating the pack does not force either setting on existing installs.

## Beta engineering additions

Beta includes Power Components 1.3.0, Gauged 1.0.6a, Coasters Simulated 0.1.5,
and the approved unofficial Steam n Rails NeoForge 0.3.0-beta.2 port. All four
are installed on clients and servers with upstream recipes and settings. Existing
Create, Power Grid, Sable and Flywheel versions satisfy their declared requirements.

WWPG 0.2.4 retains the native solver and 16 substeps. Its stationary CEE/PG
support does not establish compatibility for every component or wire added by these
mods. Railways Navigator integration, coaster assembly and physics, custom wire
behavior, electrical components and client rendering require focused player tests.

## Easy Mob Spawn Control

Beta includes Easy Mob Spawn Control 1.6.2 on clients and servers, with upstream
defaults and no custom spawn rules or mob bans supplied by the pack. Open its
menu using `/easymsc` or `/easymobspawncontrol`; the upstream shortcut is **K**,
which shares keys with Iris and other mods. Rebind it in Controls if needed.
Multiplayer edits require operator permission level 2 or the
`easy_mob_spawn_control.admin` permission. The provider marks the client optional;
the pack includes it for the menu and singleplayer use.

## Distant Horizons 3.3.3

DH now uses config format 5 and deletes older generated configs before rebuilding
them. Back up `config/DistantHorizons.toml` and the relevant DH LOD cache before
trying an existing instance. After the upstream reset, reapply wanted settings
through supported options; do not relabel an old file as version 5. Packwiz
preservation does not stop DH from resetting its own incompatible file.

The fresh-install template uses `_version = 5`, `generatorPlan = "CHUNKS_ONLY"`
and `chunkGeneratorMode = "PRE_EXISTING_ONLY"`. This keeps the existing-terrain-only
policy; the new surface-generation feature is not enabled by the pack. Four worker
threads, the 0.50 runtime ratio, radius 128 and reviewed update settings remain.
MVT does not establish visual quality, graphics performance or existing-world
LOD-cache upgrade compatibility.

## Numismatics rename patch (Beta)

Beta uses the [Ch4oS Numismatics fork](https://github.com/Cha0sCollective/CreateNumismatics)
with the sub-account rename fix. No configuration changes or account migration are
needed. Test renaming and persistence in game before promotion.
