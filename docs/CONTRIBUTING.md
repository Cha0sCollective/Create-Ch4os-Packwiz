# Contributing

Keep this an ordinary Packwiz pack. `pack/` is the source of truth for mods,
configuration, recipes and tags. Use `beta` for work and testing; `public` moves
only when I select the release players should receive. `main` tracks
the accepted release; the promotion workflow keeps it aligned with public.

For normal manual changes, edit, commit and push beta as usual. To promote, run
**Actions → Promote beta to public** from public and enter the next stable version.
Review its artifacts and MVT logs, then approve the waiting publication job yourself.
The single-maintainer environment allows self-approval. Pull beta afterward because
the workflow may add a version-alignment commit. See the [release process](../distribution/README.md)
for retries and fixed versions. Direct public pushes bypass these checks and publishing.

## Add, remove or configure a mod

Run Packwiz commands from `pack/`:

```text
packwiz modrinth install <exact-version-URL>
packwiz curseforge install <exact-file-URL>
packwiz remove <mod-name>
packwiz refresh
```

Choose the correct client/server side and inspect declared dependencies. Use
exact official releases and hashes. Review compatibility before removing mods
that supply blocks, items or saved state. Keep research observations separate
from actual gameplay validation.

Edit intended defaults under `pack/config/`, `pack/defaultconfigs/` or the existing
integration datapack. Preserve LF line endings and run `packwiz refresh` after
changes. `preserve = true` in the index keeps existing player edits; other managed
files can be replaced on update. Do not copy a whole personal config directory.
Update the [configuration guide](CONFIGURATION.md) and [source list](MOD-SOURCES.csv)
when a change affects them. Keep the Packwiz, BCC and distribution version fields
aligned when changing the release version.

Prefer small original configuration, recipes and tags. Do not copy restricted
AOCA integration or upstream assets. Mods remain official downloads; the
unchanged Industrialized Architecture JAR is mirrored as a GitHub release asset. Keep its SHA-256 and original CurseForge
identity unchanged. Its notice is also managed in `pack/third-party-notices/` so
empty server and client installations receive the attribution.
Create: Tracks has an explicitly accepted source-availability exception and
includes upstream art with separate restrictions; its JAR/assets are not bundled.

## Validate and deliver

Build the [Prism ZIP](../distribution/README.md), verify hashes and test the affected
behavior in an isolated instance. Check managed updates and preservation when
changing packaging. Record the exact revision, ZIP checksum and actual results
in the PR. Reuse valid unchanged coverage; do not claim a hash check proves gameplay.

Use a fresh independent review for consequential changes. Approving the workflow's
publication job selects the tested beta commit as the player update. Do not change repository
visibility, publish releases or touch production as a side effect of pack work.
