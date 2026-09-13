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

The repository is currently internal. Anonymous downloads will work only after
its visibility changes. Naming a branch `public` does not change visibility.

## About this pack

The starting gameplay files are identical to
[Create: Ch4oS 0.2.0-rc.1](https://github.com/Cha0sCollective/Create-Ch4oS/releases/tag/v0.2.0-rc.1):
229 client mods, including Distant Horizons, Tectonic, Terralith and the retained
Create integrations. This repository starts with fresh history. The original
repositories and releases remain intact.

Upstream mods download from their official providers. Industrialized Architecture
0.1.1b is the only bundled mod JAR, unchanged and accompanied by its notice.
The two Packwiz JARs are installation tools. Accounts, worlds, LOD caches and
research material are not included in the import ZIP.

- [Change the pack](docs/CONTRIBUTING.md)
- [Maintained configuration](docs/CONFIGURATION.md)
- [Mod sources](docs/MOD-SOURCES.csv)
- [Build an import ZIP](distribution/README.md)

Project-authored files use the [MIT license](LICENSE.txt); upstream components
retain their own terms. There is no custom installer or server-management code.
