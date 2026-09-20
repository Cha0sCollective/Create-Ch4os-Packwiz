"""Prepare the one-time 0.2.0/0.2.1 migration for review; never publishes anything."""
import argparse
from pathlib import Path

import release as r


def prepare(out):
    if out.exists():
        raise ValueError("Choose a new migration output directory.")
    if r.git("status", "--porcelain", "--untracked-files=normal"):
        raise ValueError("Commit or isolate local changes first.")
    sha = r.git("rev-parse", "HEAD")
    refs = {branch: r.remote(branch) for branch in ("beta", "public", "main")}
    # Setup changes packaging only. Never smuggle a pack change into migration.
    if r.git("diff", "--name-only", "v0.2.1", sha, "--", "pack", "distribution/profile.json",
             "distribution/runtime.json", "distribution/prism-tools.json"):
        raise ValueError("Migration must preserve the exact 0.2.1 pack and runtime metadata.")
    r.validate()
    out.mkdir(parents=True)
    selections = {"v0.2.0": r.git("rev-parse", "v0.2.0^{commit}"),
                  "v0.2.1": r.git("rev-parse", "v0.2.1^{commit}"), "public": sha, "beta": sha}
    for selection, source in selections.items():
        if selection.startswith("v") and r.tag_sha(selection) != source:
            raise ValueError(f"Remote {selection} does not match the local tag.")
        r.build(out, selection, source)
        body = r.notes(selection, source)
        if selection == "v0.2.0":
            body += ("\nThis fixed ZIP replaces the earlier public-following download at this address. "
                     "Previously imported instances still follow public. For rolling updates, choose "
                     f"[Public](https://github.com/{r.REPO}/releases/tag/channel-public).\n")
        (out / (selection + ".md")).write_text(body, encoding="utf-8", newline="\n")
    legacy = out / "legacy-public-download"
    legacy.mkdir()
    r.run("gh", "release", "download", "v0.2.0", "--repo", r.REPO, "--dir", str(legacy),
          "--pattern", "Create-Ch4oS-0.2.0-Prism.zip", "--pattern", "Create-Ch4oS-0.2.0-Prism.zip.sha256")
    r.write_json(legacy / "release.json", r.release("v0.2.0"))
    manifest = {"packaging": sha, "expected_branches": refs, "selections": selections,
                "files": {p.name: r.digest(p) for p in sorted(out.iterdir()) if p.is_file()},
                "legacy_zip_sha256": r.digest(legacy / "Create-Ch4oS-0.2.0-Prism.zip"),
                "approval_required": "Owner review before moving public/main/beta or publishing/replacing assets."}
    r.write_json(out / "migration.json", manifest)
    print(out / "migration.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    prepare(parser.parse_args().out.resolve())
