# Server pack files with Packwiz

AMP owns Java, NeoForge, memory, process control, backups and console access.
Create a Minecraft 1.21.1 / NeoForge 21.1.248 instance in AMP using Java 21.
For a new pack installation, use an instance without an unrelated modpack or save.
Stop Minecraft in AMP and take an AMP backup before changing an existing instance.
Open PowerShell on the server host in the instance's Minecraft directory (the
folder containing `mods` and `server.properties`, not AMP's application directory).

Download the ordinary [Packwiz installer bootstrap](https://github.com/packwiz/packwiz-installer-bootstrap/releases/download/v0.0.3/packwiz-installer-bootstrap.jar)
into it. SHA-256: `a8fbb24dc604278e97f4688e82d3d91a318b98efc08d5dbfcbcbcab6443d116c`.
Run from that server directory:

```powershell
java -jar packwiz-installer-bootstrap.jar -g -s server https://raw.githubusercontent.com/Cha0sCollective/Create-Ch4os-Packwiz/public/pack/pack.toml
```

Replace `public` with `beta` for testing. The same tree serves both sides;
`-s server` excludes client-only mods. Industrialized Architecture downloads from
our unchanged, hash-verified GitHub mirror. Its notice is also installed.
No Prism installation or previous modpack is needed.

Run the command in the host shell, not Minecraft's console. If `java` is not on
PATH, use the Java executable configured for this instance in AMP:

```powershell
& 'C:\path\shown\in\AMP\bin\java.exe' -jar packwiz-installer-bootstrap.jar -g -s server https://raw.githubusercontent.com/Cha0sCollective/Create-Ch4os-Packwiz/public/pack/pack.toml
```

Replace that example path with the actual executable. Keep Java, NeoForge and
memory configuration in AMP; this pack does not install or manage them. Start
Minecraft through AMP only after Packwiz succeeds. Review the EULA yourself.

## Update

Stop Minecraft and back up the complete server directory through AMP, then run the same
Packwiz command there. Read release compatibility notes first. Start only after
it succeeds. On failure, resolve the reported issue and rerun; do not start a
partially updated pack.

Packwiz updates tracked files and removes mods it previously managed when they
leave the pack. It does not reconcile an arbitrary old mod directory or migrate
AOCA/RC8 worlds. Unmanaged extra mods remain your responsibility. Existing
`preserve = true` settings retain edits; other managed defaults can be replaced.
Worlds are not downloaded or transferred. Backups remain necessary. Changes to
Minecraft or NeoForge also require updating the server runtime separately.
