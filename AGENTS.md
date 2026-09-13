# Repository guidance

This is the Packwiz-only Create: Ch4oS repository. Keep it lightweight: ordinary
Packwiz files, native Prism import metadata and concise user/contributor docs.
Do not add a custom installer, update framework, hosting service or server manager.

- `public` is the owner-selected player release. Work on `beta` or a focused branch
  based on it; moving `public`, merging and release publication need owner approval.
- Preserve the selected mod versions, gameplay and world boundary unless the owner
  requests a change. The starting pack matches Create: Ch4oS 0.2.0-rc.1.
- Edit maintained files under `pack/`, retain LF bytes, run ordinary `packwiz refresh`
  after changes, and verify the hashes. Keep personal data and generated state out
  of Git and ZIPs. Upstream mods stay official downloads; only the declared unchanged
  Industrialized Architecture JAR may be bundled with its license and attribution.
- Preserve unrelated local work. Test in isolated instances; never modify a live
  server or the user's running instance as part of a packaging check.
- Reuse valid evidence. Distinguish a package/hash check from a real Prism import
  and game launch; unperformed gameplay checks stay unperformed.
- Use a fresh read-only independent reviewer for consequential changes. The local
  saved reviewer/explorer profiles are copied unchanged from Create: Ch4oS commit
  217a467dfd7b627924451751e59a82471a9529fc. Follow the shared retained CLI workflow
  when Desktop cannot select them; verify actual role/model/effort and permissions.
  Keep review bounded to the change and reuse unchanged validation.
- The shared workflow is documented in Ch4oS-Orchestration. Do not silently copy
  later policy updates across repositories or build an additional audit framework.

Write documentation for players and contributors, not as a record of agent handoffs.
Record exact candidate revisions, relevant checks and limitations in the PR.
