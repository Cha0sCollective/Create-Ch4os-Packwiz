# Experimental mod development

`experimental` starts from the complete Beta pack, initially release **0.3.0**.
It is a separate rolling channel for testing self-developed mods. Each push runs
Packwiz/runtime validation and Prism packaging checks, then updates the
[Experimental prerelease](https://github.com/Cha0sCollective/Create-Ch4os-Packwiz/releases/tag/channel-experimental).
Packaging does not run MVT or establish client, server or gameplay compatibility.

## Install and test

Import this ZIP into Prism as a new instance:

```text
https://github.com/Cha0sCollective/Create-Ch4os-Packwiz/releases/download/channel-experimental/Create-Ch4oS-Experimental-Prism.zip
```

Its name is **Create: Ch4oS - experimental** and its identity is
`Create-Ch4oS-experimental`, separate from Public, Beta and fixed versions.
It follows `experimental` at launch and currently requires **NeoForge 21.1.262**.
Java 21, memory settings and the icon are unchanged. Existing Prism instances need
their NeoForge component updated or a fresh import; Packwiz cannot change it.
Use disposable worlds for builds that change saved
blocks or items; keep your ordinary play instances separate.

For an isolated test server, install the bootstrap as described in
[server setup](SERVER.md), then run this in the server directory:

```text
java -jar packwiz-installer-bootstrap.jar -g -s server "https://raw.githubusercontent.com/Cha0sCollective/Create-Ch4os-Packwiz/experimental/pack/pack.toml"
```

Use matching Experimental clients. Keep test server data separate from production.

## Add your mod builds

Work in the local Experimental checkout. Publish your compiled JAR as a release
asset in your mod's repository or another stable HTTPS download, then add it as a
Packwiz-managed artifact with an exact download and checksum. Use the proper side,
inspect dependency ranges, and record the version, source repository and hash in
the existing source catalogs. Do not commit compiled JARs into this pack.

To try an unpublished local JAR on just your own client, place it in the isolated
Experimental instance's `mods` folder. That unmanaged file is not included in
other installations and must be removed manually when replaced by a managed build.

Run `packwiz refresh` from `pack/` after changing pack files, then commit and push
normally to `experimental`. Wait for **Update Experimental installer** to succeed;
the rolling release records the exact installer commit and includes a SHA-256 file.
If packaging fails, review the failed run and use **Re-run failed jobs** after
addressing the cause, or push a correction. Branch-following installations see pack
changes on their next launch even before installer packaging completes.

## Bring in pack updates or graduate a mod

Fetch origin, then merge `origin/beta` into `experimental` and resolve any conflicts.
Review compatibility with your mod builds, refresh Packwiz if pack files changed,
and validate the hashes before pushing. Experimental does not automatically advance
when Beta or Public changes. Retain the current pack version until normal promotion
aligns it; Experimental builds are identified by their commit and mod versions.

When a mod is ready for Beta, deliberately copy or cherry-pick its focused mod,
configuration and source-catalog changes into Beta. Avoid merging all experimental
gameplay changes at once. The existing **Promote beta to public** workflow still
selects Beta exclusively; Experimental is never promoted automatically.
