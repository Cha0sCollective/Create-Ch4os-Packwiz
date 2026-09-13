# Build a Prism import

The builder produces a standard Prism instance ZIP using ordinary Packwiz tools.
It needs Windows PowerShell 5.1, Git and internet access. It does not need an
installer repository, an installed Minecraft instance or a world capture.

From a clean committed checkout:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File distribution/Build-Prism.ps1 -Output C:\Candidates\Create-Ch4oS-Prism.zip
```

Add `-Channel beta` and choose a different output filename for the beta ZIP.
The default is `public`. A `.sha256` file accompanies each ZIP; existing ZIPs are
never overwritten. The two ordinary Packwiz tools are pinned in `prism-tools.json`
and downloaded with hash verification. Their licenses are included.

No mod JAR or external release-input directory is needed. Industrialized Architecture
uses the direct GitHub release URL and hash in its Packwiz entry, with its original
provider identity retained. All other mods use their official providers.

Keep profile version/name and runtime versions aligned with `pack/pack.toml`.
Java 21 Generational ZGC is supplied as instance arguments; memory and Java
selection come from Prism. Only instance metadata, the player guide, notices and
Packwiz tools enter the ZIP. Packwiz fetches the selected pack at launch.

## Select the player release

Work and test on `beta`. After approval, merge the selected candidate into `public`.
That changes what normal imported clients receive on their next launch. Publishing
a GitHub release alone does not advance either branch. Do this when the server is
ready for the client changes. Review world compatibility and keep backups; changing
the branch backward does not roll back player data safely.

Keep the same world line and Minecraft/NeoForge/Java requirements for an existing
import. Changes requiring different Prism metadata use a new import ZIP and a
deliberate transition. Packwiz file preservation
is not a world-migration system.

For an isolated local test, serve a copy of the pack over loopback HTTP and build
with `-PackUrl http://127.0.0.1:PORT/pack/pack.toml`. Do not distribute that test ZIP.
GitHub caching or connectivity can interrupt an update; keep hash verification
active, cancel the failed launch and retry after the problem is resolved.
