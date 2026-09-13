# Create: Ch4oS

A Minecraft 1.21.1 / NeoForge 21.1.248 Packwiz modpack for factories, vehicles,
exploration and ambitious construction.

## Play with Prism

Import the Prism ZIP through **Add Instance → Import**, then launch the instance.
Prism handles the game, loader, account and Java selection. Packwiz downloads and
updates the mods before launch. See the [Prism guide](docs/PRISM.md) for Java 21,
memory recommendations and removal.

- **`public`** is the release selected for players; the normal ZIP follows it.
- **`beta`** is for changes and testing; the beta ZIP follows it.

Both branches are available publicly. Choose the release channel deliberately.

## About this pack

The starting gameplay files are identical to
[Create: Ch4oS 0.2.0-rc.1](https://github.com/Cha0sCollective/Create-Ch4oS/releases/tag/v0.2.0-rc.1):
229 client mods, including Distant Horizons, Tectonic, Terralith and the retained
Create integrations. This repository starts with fresh history. The original
repositories and releases remain intact.

Mods download through Packwiz. Industrialized Architecture 0.1.1b uses our unchanged,
hash-verified GitHub release mirror, with its original CurseForge identity and MIT
notice retained. Other mods use their official providers. The Prism ZIP contains
no gameplay JARs; its two JARs are Packwiz tools. Accounts, worlds, LOD caches and
research material are not included.

Client: **Prism → Packwiz → Ch4oS**. Server: **AMP → Packwiz → Ch4oS**.
Install Prism yourself; AMP manages the server runtime. No Ch4oS Installer is needed.

- [Install or update server pack files](docs/SERVER.md)
- [Change the pack](docs/CONTRIBUTING.md)
- [Maintained configuration](docs/CONFIGURATION.md)
- [Mod sources](docs/MOD-SOURCES.csv)
- [Build an import ZIP](distribution/README.md)

Project-authored files use the [MIT license](LICENSE.txt); upstream components
retain their own terms. There is no custom installer or server-management code.
