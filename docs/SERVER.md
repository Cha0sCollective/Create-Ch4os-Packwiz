# Server installation with AMP

Use an AMP instance with Minecraft **1.21.1**, NeoForge **21.1.248** and **Java 21**.
AMP manages Java, memory, backups and starting or stopping Minecraft.

Stop Minecraft in AMP. Back up an existing server, then open PowerShell in its
Minecraft directory—the folder containing `mods` and `server.properties`.
For a new server, start without an unrelated modpack or save.

Download the Packwiz bootstrap:

```powershell
Invoke-WebRequest -Uri "https://github.com/packwiz/packwiz-installer-bootstrap/releases/download/v0.0.3/packwiz-installer-bootstrap.jar" -OutFile "packwiz-installer-bootstrap.jar" -ErrorAction Stop
```

Install the server pack files:

```powershell
java -jar packwiz-installer-bootstrap.jar -g -s server "https://raw.githubusercontent.com/Cha0sCollective/Create-Ch4os-Packwiz/public/pack/pack.toml"
```

Run these in PowerShell, not the Minecraft console. If `java` is unavailable,
replace it with `& 'C:\path\to\java.exe'`, using the Java path configured in AMP.
Start Minecraft through AMP only after the installation succeeds.

## Update

Stop the server, take an AMP backup, and run the install command again. You only
need to download the bootstrap once. If an update fails, resolve the error and
rerun it before starting Minecraft.

Packwiz updates managed mods and configs and removes mods it previously managed
when they leave the pack. Settings marked for preservation keep your edits;
other managed defaults may be replaced. Worlds and operator data stay outside
the pack. Unmanaged old mods are not cleaned up automatically, and AOCA/RC8 worlds
are not migrated. Update Java or NeoForge through AMP when a release requires it.
