"""Small GitHub release helpers. Python 3.11+, Git, gh; no installer framework."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import tomllib
import zipfile

REPO = "Cha0sCollective/Create-Ch4os-Packwiz"
RAW = f"https://raw.githubusercontent.com/{REPO}"
ROOT = Path(__file__).resolve().parents[1]
MVT_SHA = "7ce3ef44910aeb5d95fc799badfcd73e450d4171"
PACKWIZ_SHA = "ef87d964f8cbd52b3b13ea42453ef322290e2b9e"
VERSION = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)")


def run(*args, cwd=ROOT, input=None):
    return subprocess.run(args, cwd=cwd, input=input, text=True, encoding="utf-8",
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout.strip()


def git(*args, cwd=ROOT):
    return run("git", *args, cwd=cwd)


def api(path, payload=None, method=None, missing=False):
    args = ["gh", "api", f"repos/{REPO}/{path}"]
    if payload is not None:
        args += ["--method", method or "POST", "--input", "-"]
    elif method:
        args += ["--method", method]
    try:
        value = run(*args, input=json.dumps(payload) if payload is not None else None)
        return json.loads(value) if value else None
    except subprocess.CalledProcessError as exc:
        if missing and "HTTP 404" in exc.stderr:
            return None
        raise


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def version(value):
    if not VERSION.fullmatch(value):
        raise ValueError("Enter a stable version such as 0.2.2 (without v).")
    return tuple(map(int, value.split(".")))


def check_environment(env):
    rules = env.get("protection_rules", []) if env else []
    reviewers = next((r for r in rules if r["type"] == "required_reviewers"), None)
    if not reviewers or not reviewers.get("reviewers"):
        raise ValueError("Configure public-release with a required maintainer reviewer first.")
    if reviewers.get("prevent_self_review", False):
        raise ValueError("Enable self-approval for the single-maintainer public-release environment.")


def remote(branch):
    return api(f"git/ref/heads/{branch}")["object"]["sha"]


def release(tag):
    return api(f"releases/tags/{tag}", missing=True)


def tag_sha(tag):
    ref = api(f"git/ref/tags/{tag}", missing=True)
    if not ref:
        return None
    obj = ref["object"]
    while obj["type"] == "tag":
        obj = api(f"git/tags/{obj['sha']}")["object"]
    if obj["type"] != "commit":
        raise ValueError("Version tag must resolve to a commit.")
    return obj["sha"]


def safe_file(root, name):
    path = (root / name).resolve()
    if not path.is_relative_to(root.resolve()) or path.is_symlink():
        raise ValueError(f"Unsafe pack path: {name}")
    return path


def validate(root=ROOT, aligned=False):
    pack_root = root / "pack"
    pack = tomllib.loads((pack_root / "pack.toml").read_text(encoding="utf-8"))
    index_meta = pack["index"]
    if index_meta["hash-format"] != "sha256" or index_meta["file"] != "index.toml":
        raise ValueError("Expected a sha256 index.toml.")
    index_path = pack_root / "index.toml"
    if digest(index_path) != index_meta["hash"]:
        raise ValueError("Packwiz index hash mismatch.")
    index = tomllib.loads(index_path.read_text(encoding="utf-8"))
    for item in index["files"]:
        algorithm = item.get("hash-format", index["hash-format"])
        if algorithm not in ("sha256", "sha512", "sha1"):
            raise ValueError(f"Unsupported managed-file hash: {algorithm}")
        content = safe_file(pack_root, item["file"]).read_bytes()
        if hashlib.new(algorithm, content).hexdigest() != item["hash"]:
            raise ValueError(f"Managed file hash mismatch: {item['file']}")
    runtime = json.loads((root / "distribution/runtime.json").read_text())
    if runtime["minecraft"] != pack["versions"]["minecraft"] or runtime["neoforge"]["version"] != pack["versions"]["neoforge"]:
        raise ValueError("Prism runtime and Packwiz versions differ.")
    if aligned:
        profile = json.loads((root / "distribution/profile.json").read_text())
        bcc = tomllib.loads((pack_root / "config/bcc-common.toml").read_text())
        version(pack["version"])
        if not pack["version"] == profile["version"] == bcc["general"]["modpackVersion"]:
            raise ValueError("Packwiz, BCC and profile versions differ.")
    return pack


def inspect_zip(path, selection, sha):
    fixed = selection.startswith("v")
    expected = f"{RAW}/{sha if fixed else selection}/pack/pack.toml"
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        prefix = f"Create-Ch4oS-{selection.replace('.', '-')}/"
        if any(not name.startswith(prefix) or ".." in Path(name).parts for name in names):
            raise ValueError("Unexpected ZIP layout.")
        jars = sorted(Path(name).name for name in names if name.endswith(".jar"))
        if jars != ["packwiz-installer-bootstrap.jar", "packwiz-installer.jar"]:
            raise ValueError("ZIP must contain only the two Packwiz tool JARs.")
        cfg = archive.read(prefix + "instance.cfg").decode("utf-8")
        if f'--bootstrap-no-update -s client "{expected}"' not in cfg:
            raise ValueError("ZIP follows the wrong pack URL.")
        icon_match = re.search(r"(?m)^iconKey=([^\r\n]+)$", cfg)
        if not icon_match:
            raise ValueError("ZIP has no Prism icon key.")
        icon_key = icon_match.group(1)
        expected_icon_key = f"Create-Ch4oS-{selection.replace('.', '-')}"
        legacy_fixed = {"v0.2.0", "v0.2.1", "v0.2.2"}
        if icon_key == "default":
            if selection not in legacy_fixed:
                raise ValueError("Branded ZIP uses the legacy default Prism icon.")
        else:
            if icon_key != expected_icon_key:
                raise ValueError("ZIP uses the wrong profile-specific Prism icon key.")
            icon_path = prefix + icon_key + ".png"
            if icon_path not in names:
                raise ValueError("ZIP is missing its Prism icon.")
            icon = archive.read(icon_path)
            if icon[:8] != b"\x89PNG\r\n\x1a\n" or icon[12:16] != b"IHDR":
                raise ValueError("ZIP has an invalid Prism icon.")
            if int.from_bytes(icon[16:20], "big") != 512 or int.from_bytes(icon[20:24], "big") != 512:
                raise ValueError("Prism icon must be 512 by 512 pixels.")
        if f"Pack source: {sha}\n" not in archive.read(prefix + "release.txt").decode("utf-8"):
            raise ValueError("ZIP pack provenance differs.")
        if not any(name.endswith("industrialized-architecture-LICENSE.txt") for name in names):
            raise ValueError("Missing IA notice.")
    checksum = Path(str(path) + ".sha256").read_text().split()
    if checksum != [digest(path), Path(path).name]:
        raise ValueError("ZIP checksum differs.")


def verify_published(tag, sha):
    rel = release(tag)
    if not rel or rel["draft"] or tag_sha(tag) != sha:
        raise ValueError(f"Publish fixed {tag} at {sha} before promoting public.")
    name = f"Create-Ch4oS-{tag[1:]}-Prism.zip"
    with tempfile.TemporaryDirectory() as tmp:
        run("gh", "release", "download", tag, "--repo", REPO, "--dir", tmp,
            "--pattern", name, "--pattern", name + ".sha256")
        inspect_zip(Path(tmp) / name, tag, sha)


def prepare(ver, out):
    version(ver)
    check_environment(api("environments/public-release", missing=True))
    out.mkdir(parents=True, exist_ok=True)
    # These remote reads define the candidate and compare-and-swap expectations.
    beta, public, main = remote("beta"), remote("public"), remote("main")
    git("fetch", "origin", "beta", "public", "main", "--tags")
    for old in (public, main):
        git("merge-base", "--is-ancestor", old, beta)
    # Packaging/docs-only setup commits may follow the public pack's version tag.
    old_tags = [t for t in git("tag", "--merged", public).splitlines()
                if t.startswith("v") and VERSION.fullmatch(t[1:])]
    old_tags.sort(key=lambda t: version(t[1:]), reverse=True)
    unchanged_paths = ("pack", "distribution/profile.json", "distribution/runtime.json", "distribution/prism-tools.json")
    old_tag = next((t for t in old_tags if not git("diff", "--name-only", t, public, "--", *unchanged_paths)), None)
    if old_tag is None:
        raise ValueError("Public pack content must have a fixed version before promotion.")
    previous_snapshot = git("rev-parse", old_tag + "^{commit}")
    if version(ver) <= version(old_tag[1:]):
        raise ValueError("New version must be greater than the current public version.")
    verify_published(old_tag, previous_snapshot)
    if tag_sha("v" + ver) or release("v" + ver):
        raise ValueError("Version already exists. For interrupted publication, rerun failed jobs in the original run.")
    candidate_dir = out / "candidate"
    git("worktree", "add", "--detach", str(candidate_dir), beta)
    try:
        validate(candidate_dir)
        for name, key in (("pack/pack.toml", "version"), ("pack/config/bcc-common.toml", "modpackVersion")):
            path = candidate_dir / name
            content, count = re.subn(rf'(?m)^{key} = "[^"\r\n]*"$', f'{key} = "{ver}"', path.read_text(encoding="utf-8"))
            if count != 1:
                raise ValueError(f"Expected one {key} field in {name}.")
            path.write_text(content, encoding="utf-8", newline="\n")
        profile_path = candidate_dir / "distribution/profile.json"
        profile = json.loads(profile_path.read_text())
        profile["version"] = ver
        write_json(profile_path, profile)
        run("packwiz", "refresh", cwd=candidate_dir / "pack")
        validate(candidate_dir, aligned=True)
        git("add", "pack/pack.toml", "pack/index.toml", "pack/config/bcc-common.toml", "distribution/profile.json", cwd=candidate_dir)
        if git("diff", "--cached", "--name-only", cwd=candidate_dir):
            git("-c", "user.name=github-actions[bot]", "-c", "user.email=41898282+github-actions[bot]@users.noreply.github.com",
                "commit", "-m", f"Prepare release {ver}", cwd=candidate_dir)
        if git("status", "--porcelain", cwd=candidate_dir):
            raise ValueError("Packwiz refresh changed unexpected files; review them on beta first.")
        candidate = git("rev-parse", "HEAD", cwd=candidate_dir)
        # Lease refuses concurrent manual beta pushes, including ones made after our read.
        git("push", "origin", f"--force-with-lease=refs/heads/beta:{beta}", f"{candidate}:refs/heads/beta")
    finally:
        git("worktree", "remove", "--force", str(candidate_dir))
    manifest = {"version": ver, "candidate": candidate, "previous_public": public,
                "previous_main": main, "previous_tag": old_tag, "previous_snapshot": previous_snapshot,
                "packaging": git("rev-parse", "HEAD"),
                "mvt": MVT_SHA, "packwiz": PACKWIZ_SHA}
    write_json(out / "release.json", manifest)
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as stream:
            stream.write(f"candidate={candidate}\n")


def build(out, selection, sha):
    out.mkdir(parents=True, exist_ok=True)
    fixed = selection.startswith("v")
    filename = f"Create-Ch4oS-{selection[1:] if fixed else selection.title()}-Prism.zip"
    path = out / filename
    args = ["pwsh", "-NoProfile", "-File", str(ROOT / "distribution/Build-Prism.ps1"), "-Output", str(path)]
    if fixed:
        # The local candidate tag is never pushed until approval.
        local = git("tag", "--list", selection)
        if local:
            if git("rev-parse", selection + "^{commit}") != sha:
                raise ValueError("Existing version tag resolves to another commit.")
        else:
            git("tag", selection, sha)
        args += ["-VersionTag", selection]
    else:
        args += ["-Channel", selection, "-SourceRevision", sha]
    run(*args)
    inspect_zip(path, selection, sha)
    return path


def notes(selection, sha):
    fixed = selection.startswith("v")
    url = f"{RAW}/{sha if fixed else selection}/pack/pack.toml"
    behavior = (f"Fixed snapshot **{selection}**. This installer stays on commit `{sha}` and does not follow Public or Beta."
                if fixed else f"Follows the **{selection}** branch. Packwiz installs its current files at launch.")
    extra = "\nHistorical 0.2.1 files contain beta version labels; they are preserved exactly as tagged.\n" if selection == "v0.2.1" else ""
    return (f"# Create: Ch4oS — {selection}\n\n{behavior}\n{extra}\n"
            "Import the attached Prism ZIP (not GitHub's source-code archive). Use Java 21 and allow the Packwiz pre-launch command. "
            "Mods download from their providers; this ZIP includes no gameplay JARs.\n\n"
            f"Pack revision used for installer metadata: `{sha}`.\n\n"
            "For AMP servers, stop Minecraft and back up first, then run with the Packwiz bootstrap installed:\n\n"
            f'```text\njava -jar packwiz-installer-bootstrap.jar -g -s server "{url}"\n```\n\n'
            "AMP manages Java, NeoForge, memory and backups. See "
            f"[server setup](https://github.com/{REPO}/blob/{sha}/docs/SERVER.md). "
            "Runtime changes can require a new Prism import and an AMP runtime update. "
            "Use a separate instance when switching versions; a fixed pack is not a world rollback.\n")


def package(out):
    manifest = json.loads((out / "release.json").read_text())
    for selection in ("v" + manifest["version"], "public"):
        build(out, selection, manifest["candidate"])
        changes = git("log", "--format=- %s (%h)", manifest["previous_public"] + ".." + manifest["candidate"])
        body = notes(selection, manifest["candidate"]) + "\n## Changes\n\n" + changes + "\n"
        (out / (selection + ".md")).write_text(body, encoding="utf-8", newline="\n")
    manifest["files"] = {p.name: digest(p) for p in sorted(out.iterdir()) if p.suffix in (".zip", ".sha256", ".md")}
    write_json(out / "release.json", manifest)


def check_manifest(out, manifest):
    if git("rev-parse", "HEAD") != manifest["packaging"]:
        raise ValueError("Publication must use the same packaging revision as preparation.")
    version(manifest["version"])
    for name, checksum in manifest["files"].items():
        if digest(safe_file(out, name)) != checksum:
            raise ValueError(f"Prepared artifact changed: {name}")
    report = json.loads((out / "mvt-results/report.json").read_text())
    if report["status"] != "lifecycle_passed_logs_unreviewed" or report["pack_sha"] != manifest["candidate"]:
        raise ValueError("MVT did not pass for this exact candidate.")
    for selection in ("v" + manifest["version"], "public"):
        name = f"Create-Ch4oS-{selection[1:] if selection.startswith('v') else 'Public'}-Prism.zip"
        inspect_zip(out / name, selection, manifest["candidate"])


def publish_assets(tag, sha, out, selection, rolling=False):
    existing_sha = tag_sha(tag)
    if existing_sha and existing_sha != sha and not rolling:
        raise ValueError("Refusing to move an existing version tag.")
    if not existing_sha:
        api("git/refs", {"ref": f"refs/tags/{tag}", "sha": sha})
    filename = f"Create-Ch4oS-{selection.title() if rolling else selection[1:]}-Prism.zip"
    assets = [out / filename, out / (filename + ".sha256")]
    rel = release(tag)
    title = f"Create: Ch4oS {selection.title()} — follows {selection}" if rolling else f"Create: Ch4oS {selection} — fixed version"
    body = (out / (selection + ".md")).read_text(encoding="utf-8")
    if rel is None:
        rel = api("releases", {"tag_name": tag, "name": title, "body": body, "draft": True,
                               "prerelease": selection == "beta"})
    if rolling:
        run("gh", "release", "upload", tag, *(str(p) for p in assets), "--repo", REPO, "--clobber")
    else:
        existing_assets = {a["name"]: a for a in rel["assets"]}
        for path in assets:
            if path.name in existing_assets:
                with tempfile.TemporaryDirectory() as tmp:
                    run("gh", "release", "download", tag, "--repo", REPO, "--dir", tmp, "--pattern", path.name)
                    if digest(Path(tmp) / path.name) != digest(path):
                        raise ValueError("Existing fixed asset differs; refusing to overwrite.")
            else:
                if not rel["draft"]:
                    raise ValueError("Published fixed release is missing an asset; refusing to change it.")
                run("gh", "release", "upload", tag, str(path), "--repo", REPO)
    api(f"releases/{rel['id']}", {"name": title, "body": body, "draft": False,
                                "prerelease": selection == "beta", "make_latest": "true" if selection == "public" else "false"}, method="PATCH")
    if rolling and existing_sha and existing_sha != sha:
        api(f"git/refs/tags/{tag}", {"sha": sha, "force": True}, method="PATCH")


def promotion_refs(manifest, public, main):
    candidate = manifest["candidate"]
    if public not in (manifest["previous_public"], candidate) or main not in (manifest["previous_main"], candidate):
        raise ValueError("Public or main changed after preparation. Prepare a new release.")
    return [("public", public), ("main", main)]


def publish(out):
    manifest = json.loads((out / "release.json").read_text())
    check_environment(api("environments/public-release"))
    check_manifest(out, manifest)
    refs = promotion_refs(manifest, remote("public"), remote("main"))
    verify_published(manifest["previous_tag"], manifest["previous_snapshot"])
    sha = manifest["candidate"]
    git("fetch", "origin", sha, *(old for _, old in refs))
    for _, old in refs:
        git("merge-base", "--is-ancestor", old, sha)
    publish_assets("v" + manifest["version"], sha, out, "v" + manifest["version"])
    # Both heads move together, with leases guarding manual writes during publication.
    git("push", "--atomic", "origin", *(f"--force-with-lease=refs/heads/{name}:{old}" for name, old in refs),
        *(f"{sha}:refs/heads/{name}" for name, _ in refs))
    publish_assets("channel-public", sha, out, "public", rolling=True)


def beta(out):
    sha = git("rev-parse", "HEAD")
    validate()
    build(out, "beta", sha)
    (out / "beta.md").write_text(notes("beta", sha), encoding="utf-8", newline="\n")
    if remote("beta") != sha:
        print("Beta advanced while packaging; the newer push will refresh its installer.")
        return
    publish_assets("channel-beta", sha, out, "beta", rolling=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["validate", "prepare", "package", "publish", "beta"])
    parser.add_argument("--version")
    parser.add_argument("--out", type=Path, default=ROOT / "dist/release")
    args = parser.parse_args()
    args.out = args.out.resolve()
    if args.command == "validate":
        validate()
    elif args.command == "prepare":
        prepare(args.version or "", args.out)
    else:
        globals()[args.command](args.out)


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        print(exc.stdout or "", file=sys.stderr)
        print(exc.stderr or "", file=sys.stderr)
        raise SystemExit(f"Command failed with exit code {exc.returncode}: {exc.cmd[0]}") from None
