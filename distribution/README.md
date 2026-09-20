# Releases and Prism imports

## Everyday changes

Edit your local beta repository, commit, and push to `beta` normally. Small manual
changes need no special tooling. The Beta release ZIP is refreshed automatically
after packaging checks. Beta installations follow the branch at launch, including
changes that have not passed a server smoke test.
If another push arrives during packaging, the next successful Beta run refreshes
its installer metadata. If that refresh fails, rerun **Update Beta installer** from
beta, especially when Minecraft, NeoForge or tool pins changed.

To release to players:

1. Push your beta changes.
2. Open **Actions → Promote beta to public → Run workflow**, leave the workflow
   branch set to **public**, enter a new version such as `0.2.2`, and explicitly
   accept the Minecraft EULA for the disposable test server.
3. Review the run summary, release notes, ZIP checksums and MVT phase logs in its
   downloadable artifact. Approve **public-release** when the server is ready.

There is one maintainer. The environment permits that maintainer to approve their
own run; no second account is required. A green lifecycle result still requires
log review. It does not prove real-client behavior or existing-world upgrades.

The workflow aligns Packwiz, BCC and profile version labels, runs ordinary
`packwiz refresh`, and commits those changes to beta if needed. **Pull beta before
making your next local edit**, since the workflow may have added a version commit.
It tests a captured commit; later beta pushes are not included in that release.

Approval publishes a fixed snapshot, advances public and main together to the
tested commit, and refreshes Public's installer. Public remains GitHub's Latest
release. Existing version tags and fixed assets are never overwritten by this
workflow. Packaging/documentation-only commits may follow a version tag when the
pack, profile, runtime and tool pins still match that tag exactly.

You can still push manually. **A direct public push bypasses this process** and
can reach players immediately; it does not trigger release publishing or MVT.
Use the promotion workflow for normal releases. Main follows approved public;
avoid separate development on main.

## If a run fails

- Before approval: public is unchanged. Fix the problem on beta and start again.
  Failed preparation may already have added the version commit to beta.
- During publication: choose **Re-run failed jobs** on that same run. This reuses
  the tested candidate and exact ZIP bytes. Do not start another run with the
  same version. An existing matching draft/tag is resumed; conflicting bytes stop
  publication. Prepared artifacts are retained for 30 days.
- Concurrent public/main edits stop promotion. Preserve those edits and reconcile
  beta before preparing another candidate. An atomic Git push prevents updating
  only one of public/main. A fixed release can exist even if branch promotion fails.
- If Public's ZIP upload fails after promotion, public has already advanced.
  Retry the failed publication job; do not roll the branch or a live world backward.
- If the original artifacts have expired, stop and inspect the published state.
  Do not rebuild and overwrite an existing numbered release.

## One-time repository setup

Install these workflow files on public (the default branch) and beta. Configure
**Settings → Environments → public-release** with `Cha0sArbiter` as its required
reviewer, **Prevent self-review disabled**, and administrator bypass disabled.
Allow deployments from public. The preparation job refuses to run without the
reviewer gate or if self-review is blocked. No branch protection changes are needed.

The initial migration preserves `v0.2.0` and `v0.2.1`, replaces the old rolling
0.2.0 download with a fixed snapshot, and creates the 0.2.1 fixed release plus
`channel-public` and `channel-beta`. Historical 0.2.1 version-label inconsistencies
remain unchanged; future promotions enforce matching labels. IA's release is untouched.
Already-imported legacy 0.2.0 instances continue to follow public.

Prepare the four migration ZIPs, notes, checksums and a backup of the legacy
download from a clean setup checkout with
`python distribution/migrate.py --out C:\Candidates\migration`.
This command only prepares local artifacts; publication and branch synchronization
remain an owner-approved setup action. Its manifest records the expected branch
heads and tag commits so concurrent manual work can be detected before publication.

## Build a ZIP locally

Use a clean committed checkout, Git, PowerShell 5.1 on Windows or PowerShell 7,
and internet access. No installed game, server or world is needed.

```powershell
pwsh -NoProfile -File distribution/Build-Prism.ps1 -Channel public -Output C:\Candidates\Create-Ch4oS-Public-Prism.zip
pwsh -NoProfile -File distribution/Build-Prism.ps1 -Channel beta -Output C:\Candidates\Create-Ch4oS-Beta-Prism.zip
pwsh -NoProfile -File distribution/Build-Prism.ps1 -VersionTag v0.2.0 -Output C:\Candidates\Create-Ch4oS-0.2.0-Prism.zip
```

On Windows PowerShell 5.1 use `powershell.exe -NoProfile -ExecutionPolicy Bypass`
instead of `pwsh -NoProfile`. For rolling imports, `-SourceRevision <commit>` selects
the installer metadata source without changing which branch the instance follows.
`-VersionTag` resolves the tag to a full commit SHA and uses that SHA for the pack
URL. It cannot be combined with `-Channel`, `-SourceRevision` or `-PackUrl`.

Each ZIP has a `.sha256` file and distinct Prism identity. Existing local artifacts
are not overwritten. The selected revision supplies runtime settings, profile,
Packwiz tool pins and licenses; provenance records both pack and packaging commits.
Only metadata, instructions, notices and the two hash-verified Packwiz tools enter
the ZIP. Gameplay mods download from their providers, including the unchanged IA
mirror. Fixed versions depend on continued availability of those downloads.

For an isolated installation test use `-PackUrl http://127.0.0.1:PORT/pack/pack.toml`.
Do not distribute that ZIP. Production releases always use their channel or SHA URL.

Release helpers and their tests require Python 3.11+, `gh` and Git. CI pins Packwiz
and the MVT harness by commit; the harness records the resolved Java 21 server image.
Run `python -m unittest discover -s distribution/tests -v` for release safeguards
and `python distribution/release.py validate` for managed-file and runtime checks.

Keep Java/Minecraft/NeoForge requirements and world compatibility under review.
Changing Prism runtime metadata requires users to import a new ZIP; Packwiz alone
does not upgrade Prism's loader or AMP's runtime. Back up worlds before updates.
