# Install with Prism Launcher

This is a standard Prism instance ZIP. You need Prism Launcher, internet access
and a Minecraft account. It does not install Prism or register a Windows
application.

## Import and play

1. In Prism, choose **Add Instance → Import**, then select the Prism ZIP.
2. Check **Settings → Java**: use Java 21 and set suitable memory. The import
   inherits your Prism Java selection and memory settings. Start with 8 GiB for
   Minecraft on a 16 GiB PC, or 12 GiB with at least 24 GiB of system RAM. Leave
   memory for Windows and other applications; large DH generation jobs need more
   headroom. The instance supplies the pack's Java 21 Generational ZGC arguments
   (`-XX:+UseZGC -XX:+ZGenerational`) so it uses the same collector as the release.
3. Sign in through Prism and launch the imported instance. Prism initially uses
   the ZIP filename as its name; you may rename it. Allow the
   included Packwiz pre-launch command when Prism asks. Packwiz downloads the
   selected client mods and configuration before Minecraft starts.

Industrialized Architecture 0.1.1b downloads from our unchanged GitHub release
mirror with SHA-256 verification; its MIT notice is included. Every other mod
downloads from its official provider. The ZIP contains no gameplay JARs. Its two
JARs are Packwiz installation tools. No previous pack installation or world is
required. The instance selects Minecraft 1.21.1 and NeoForge 21.1.248.

## Updates and personal files

Each launch checks the pack at:

`https://raw.githubusercontent.com/Cha0sCollective/Create-Ch4os-Packwiz/public/pack/pack.toml`

The normal ZIP follows `public`; the beta ZIP follows the same address with
`beta` in place of `public`. We change `public` only when a release is ready for players.
Publishing a release or merging development work does not change it automatically.
Packwiz updates managed files and removes mods removed from the managed pack.
Settings already marked for preservation keep your edits. Other managed settings
can be replaced by a pack update. Extra mods you add yourself are not maintained
by this pack and may become incompatible.

Worlds, screenshots, schematics and other personal files are not pack inputs.
Back up local worlds before updating; file preservation does not guarantee that
an older world is compatible with a changed mod set. New world boundaries or
Minecraft/NeoForge changes requiring new Prism metadata use a new import ZIP.
This import is for the 0.2 New World line, not RC8 world migration.

If an update fails, cancel the launch, keep the log and retry once connectivity
or the reported download problem is resolved. Do not bypass a failed update and
join a server with a partially updated pack.

To remove the instance, use Prism's instance removal after backing up wanted
local data. There is no Windows Apps uninstall entry for this import.

## Availability

The public and beta pack addresses are available without signing into GitHub.
Prism itself is installed separately by the player; this ZIP only adds an instance.
