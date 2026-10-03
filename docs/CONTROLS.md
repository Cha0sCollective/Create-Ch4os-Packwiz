# Player controls

Extra controls for Create: Ch4oS beta **0.2.8**, Minecraft 1.21.1. These are the
pack's fresh-install defaults and the installed mods' default bindings. Your
**Options → Controls → Key Binds** screen shows your actual assignments.
Vanilla movement, inventory and interaction controls still apply.

**Shader reload is F8. Weapon reload stays R.** Existing instances keep their
`options.txt`: search for **Reload Shaders** in Key Binds and assign **F8** yourself.
Pack updates preserve your choices. Minecraft's **Reset** button restores a mod's
upstream binding; for Iris reload that is R, so set F8 again after resetting it.

Use Controlling's search to find an action by name and its conflict filter to
inspect shared keys. **Unbound** means no shortcut is assigned; you can choose
one if you use that feature. On keyboards without a number pad, rebind Jade's
Numpad controls. Left and right modifier keys are distinguished where relevant.

## Inventory, crafting and information

| Mod | Action | Default | When to use it |
| --- | --- | --- | --- |
| JEI | Show/hide item list | Ctrl+O | In an inventory screen |
| JEI | Focus item search | Ctrl+F | In an inventory screen |
| JEI | Show recipes | R | Hover an item; left-click also works in JEI's item list |
| JEI | Show uses | U | Hover an item; right-click also works in JEI's item list |
| JEI | Bookmark item | A | Hover an item |
| JEI | Previous recipe view | Backspace | In the recipe viewer |
| JEI | Previous/next recipe page | Page Up / Page Down | In the recipe viewer |
| JEI | Previous/next recipe category | Shift+Page Up / Shift+Page Down | In the recipe viewer |
| JEI | Pause cycling ingredients | Left Shift | Hold in the recipe viewer |
| JEI | Clear search | Right-click | On the search field |
| JEI | Previous/next search | Up / Down | With search focused |
| Backpacked | Open backpack | B | With a backpack available |
| Backpacked | Open backpack management | V | Backpack management |
| Curios | Open accessory inventory | G | Manage equipped Curios |
| Corpse | Open death history | U | In the world |
| Quark | Hotbar swapper | Z, then 1 / 2 / 3 | Select an inventory row to swap with the hotbar |
| Quark | Sort player/container inventory | Unbound | Use the inventory sort buttons or assign shortcuts |
| Quark | Insert/extract items; shift lock | Unbound | Optional inventory shortcuts |
| Supplementaries | Quiver | V | With the relevant equipment |
| Jade | Open configuration | Numpad 0 | Configure the looked-at-block/entity overlay |
| Jade | Show/hide overlay | Numpad 1 | In the world |
| Jade | Toggle fluid information | Numpad 2 | In the world |
| Jade | Show recipes / uses | Numpad 3 / Numpad 4 | For the looked-at target, through JEI |
| Jade | Narrate target | Numpad 5 | Read the target's information |
| Jade | Show extra details | Left Shift | Hold while looking at a target |
| Toast Control | Clear toasts | J | Dismiss the corner notifications |
| FTB Teams | Open team GUI | Unbound | Assign a shortcut if desired |

Mouse Tweaks adds inventory drag/scroll gestures rather than a separate gameplay
key. Polymorph adds a recipe-selection button to supported crafting screens.
Controlling adds search and conflict tools to Key Binds rather than a gameplay
shortcut. Their screen controls remain available without assigning new keys.

## Maps, waypoints and claims

| Mod | Action | Default | When to use it |
| --- | --- | --- | --- |
| Xaero's World Map | Open world map | M | In the world |
| Xaero's World Map | Open settings | ] | World-map settings |
| Xaero's World Map | Quick confirm | Right Shift | Map-screen confirmation |
| Xaero's Minimap | Open settings | Y | Minimap settings |
| Xaero's Minimap | Create waypoint | B | Name and edit a new waypoint |
| Xaero's Minimap | Open waypoint list | U | Manage waypoints |
| Xaero's Minimap | Enlarge minimap | Z | In the world |
| Xaero's Minimap | Instant waypoint | Numpad + | Quickly mark a location |
| Open Parties and Claims | Open menu | Apostrophe (') | Parties and claims |
| Xaero's maps | Keyboard zoom and optional map/waypoint/overlay toggles | Unbound | Assign keys for the features you use |

MapSyncer adds no dedicated gameplay key. See [Maps and distant terrain](MAPS.md)
for map sharing and the optional synchronization command.

## Movement and building

| Mod | Action | Default | When to use it |
| --- | --- | --- | --- |
| Personality | Crawl | C | Personality's crawl feature |
| Personality | Sit | Z | Personality's sit feature |
| Quark | Lock block rotation | K | Building with a fixed placement orientation |
| Quark | Variant selector | R | With a supported block variant available |
| Quark | Auto-walk | Unbound | Optional movement shortcut |
| Climbable Ropes | Lock rope camera | Left Alt | On a rope |
| Create Hypertube | Escape tube | Left Shift | Inside a hypertube |
| Immersive Aircraft | Dismount | R | While piloting an aircraft |
| Immersive Aircraft | Boost | B | While piloting an aircraft |
| Immersive Aircraft | Separate fallback flight controls | Unbound | Optional alternatives to the normal movement controls |
| Ornithopter Glider | Boost glider | Space | Using a glider |
| Create: Stuff & Additions | Flying | Space | With the relevant flight equipment |
| Create: Stuff & Additions | Increase/decrease reach | Up / Down | With the relevant reach equipment |
| Aeroworks | Joystick free camera | Left Shift | Using a joystick |

TaCZ's separate C-key crawl system is disabled by the maintained TaCZ Tweaks
configuration. That setting does not disable Personality's crawl. Existing
servers must retain `forceDisableCrawl = true`; see [Configuration](CONFIGURATION.md).

## Graphics and camera

| Mod | Action | Default | When to use it |
| --- | --- | --- | --- |
| Iris | Reload shaders | **F8** | Recompile/reload the selected shader pack |
| Iris | Toggle shaders | K | Enable or disable shaders |
| Iris | Shader-pack selection | O | Open shader selection/settings |
| Quark | Camera mode | F12 | Quark's camera feature |
| Quark | Back | Mouse button 4 | Quark's supported screen navigation; usually a side button |

F8 is a beta pack override. Shader presets and their initial disabled state are
described in [Configuration](CONFIGURATION.md). Cosmetic and developer/debug
controls are outside this quick reference.

## Guns

These actions apply when using a TaCZ gun. Equipment, gun state and available
attachments can affect which actions are available.

| Mod | Action | Default |
| --- | --- | --- |
| TaCZ | Shoot / aim | Left mouse / Right mouse |
| TaCZ | Reload | R |
| TaCZ | Inspect gun | H |
| TaCZ | Switch firing mode | G |
| TaCZ | Interact | O |
| TaCZ | Attachment refit | Z |
| TaCZ | Change scope zoom / melee | V / V |
| TaCZ | Open configuration | Alt+T |
| TaCZ | Crawl | C, **disabled by pack configuration** |
| TaCZ Tweaks | Bolt; reduce sensitivity; tilt gun; unload | Unbound |

## Create tools and vehicles

Most of these shortcuts are contextual: hold the named tool, wear the equipment
or open its screen first. Follow its tooltip/Ponder for the remaining mouse and
scroll interactions. Shared tool keys have not been reassigned by the pack.

| Mod | Action | Default | Context |
| --- | --- | --- | --- |
| Ponder / Create | Ponder | Hold W | Hover a supported item in an inventory |
| Create | Schematic tool menu | Left Alt | Using schematic tools |
| Create | Toolbox toolbelt | Left Alt | With a toolbox available |
| Create | Rotate placement menu | Unbound | Optional placement shortcut |
| Create | Shift / Ctrl / Alt modifiers | Left Shift / Left Ctrl / Left Alt | Create tool modifiers |
| Copycats+ | Fill copycat | Left Alt | Copycat interactions |
| Create: Mobile Packages | Open portable stock ticker | G | Portable stock ticker |
| Create: Mobile Packages | Open player networks | H | Player networks screen |
| Create: Big Cannons | Pitch mode | C | Controlling a cannon |
| Create: Big Cannons | Fire controlled cannon | Left mouse | Controlling a cannon |
| Create: Tweaked Controllers | Mouse focus / reset | Left Alt / R | Using a controller |
| Create: Tweaked Controllers | Exit controller | Tab | Using a controller |
| Simulated (bundled with Aeronautics) | Physics Staff rotate mode | Tab | Using the Physics Staff |
| Simulated (bundled with Aeronautics) | Keyboard scroll up/down | Unbound | Optional Physics Staff controls |
| Create Aeronautics: Toolgun | Open menu | Tab | Using the Toolgun |
| Create Aeronautics: Toolgun | Rotate magnetic object | Tab | Magnetic-object tool mode |
| Create: Power Grid | Alternate wire placement | Left Ctrl | Placing wires |
| Create: Power Grid | Rotate component / place trace | R / T | Circuit editor |
| Create: Power Grid | Delete area / pick component / switch layer | D / S / X | Circuit editor |
| Gadgets & Gizmos | Toggle force gizmo / diagram | G / H | Physics goggles |
| Gadgets & Gizmos | Toggle interactive mode / edit overlay | J / K | Physics goggles |
| Gadgets & Gizmos | Toggle propulsion | Unbound | Optional shortcut |
| Gadgets & Gizmos | Cycle scope mode modifier | Left Alt | Contraption network linker |
| Create: Dreams & Desires | Activate handheld saw / drill | Left Alt | Using the named tool |
| Create: Tracks | Open tuning | J | Tracks tuning |
| Create: Pipe Organs | Open MIDI configuration | Semicolon (;) | MIDI configuration |
| Create Aeronautics Curios Compat | Remote use | Y | Using the relevant accessory |
| Create Railways Navigator | Route overlay options | R | Route overlay |

Petrolpark's Library also registers feature-specific shortcuts: **C** for pocket
crafting, **X** for deletable items, and **0 / - / =** for extra hotbar slots
10–12 (slots 13–17 are unbound). A registered library key does not mean that every
feature is provided by the installed mods; use it only when the relevant item or
feature is available.

## Shared keys to check first

A shared key can be harmless when actions run in separate screens, or cause two
actions in the world. The conflict list alone cannot prove the result. Rebind
the actions you use if they interfere; this update changes only Iris reload.

| Key | Notable overlapping actions |
| --- | --- |
| B | Backpack, new waypoint, aircraft boost |
| C | Personality crawl, cannon pitch mode, optional library pocket crafting; TaCZ crawl is disabled |
| G | Curios inventory, gun firing mode, portable stock ticker, physics-goggles force gizmo |
| H | Gun inspection, player networks, physics-goggles diagram |
| J | Clear toasts, Tracks tuning, physics-goggles interactive mode |
| K | Iris shader toggle, Quark rotation lock, physics-goggles overlay editor |
| O | Iris shader selection, TaCZ interact; JEI's overlay uses Ctrl+O |
| R | Weapon reload, Quark variants, aircraft dismount, controller mouse reset, route overlay; JEI recipes and Power Grid rotation apply in their screens |
| U | Waypoint list, death history; JEI's Show Uses uses U over an item |
| V | Backpack management, quiver, gun zoom/melee |
| Y | Minimap settings, Aeronautics Curios remote use |
| Z | Hotbar swapper, sit, enlarge minimap, gun attachment refit |
| Tab | Vanilla player list, Toolgun modes, Physics Staff rotate mode, controller exit |
| Left Alt / Left Shift | Several held-tool/equipment modifiers and ordinary Minecraft actions |

## Reference scope

Bindings were checked statically against the exact Packwiz-managed artifacts'
key registrations and English labels, including JEI modifier keys. F8 is the
only binding supplied in `pack/options.txt`; the others come from the installed
mods. This guide covers common QoL controls and player-facing equipment controls,
not every debug, cosmetic or permission-dependent action. In-game behavior and
conflict testing remain player tests. Changing mod versions can change defaults.

For exact versions and upstream links, use the [source catalog](MOD-SOURCES.md).
The [Controlling project](https://modrinth.com/mod/controlling) explains the key
search/conflict tools, and [Quark's feature guide](https://quarkmod.net/) describes
its inventory and building helpers.
