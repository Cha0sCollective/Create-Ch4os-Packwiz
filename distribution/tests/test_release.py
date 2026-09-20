import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import zipfile

MODULE = Path(__file__).resolve().parents[1] / "release.py"
spec = importlib.util.spec_from_file_location("release", MODULE)
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)


class ReleaseTests(unittest.TestCase):
    def test_single_maintainer_gate(self):
        good = {"protection_rules": [{"type": "required_reviewers", "prevent_self_review": False,
                                      "reviewers": [{"type": "User", "reviewer": {"login": "owner"}}]}]}
        r.check_environment(good)
        for env in (None, {}, {"protection_rules": []}):
            with self.assertRaises(ValueError):
                r.check_environment(env)
        good["protection_rules"][0]["prevent_self_review"] = True
        with self.assertRaises(ValueError):
            r.check_environment(good)

    def test_version_input_is_stable_and_not_shell_syntax(self):
        self.assertLess(r.version("0.2.9"), r.version("0.2.10"))
        for value in ("v0.2.2", "0.2.2-beta.1", "01.2.3", "1.2.3\n", "$(echo bad)", "1.2.3; x"):
            with self.assertRaises(ValueError):
                r.version(value)

    def test_promotion_retry_and_concurrent_public_changes(self):
        manifest = {"candidate": "new", "previous_public": "old", "previous_main": "main"}
        self.assertEqual(r.promotion_refs(manifest, "old", "main"), [("public", "old"), ("main", "main")])
        self.assertEqual(r.promotion_refs(manifest, "new", "new"), [("public", "new"), ("main", "new")])
        for public, main in (("unrelated", "main"), ("old", "unrelated")):
            with self.assertRaises(ValueError):
                r.promotion_refs(manifest, public, main)

    def test_validate_real_pack_and_detect_corruption(self):
        r.validate()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(r.ROOT / "pack", root / "pack")
            shutil.copytree(r.ROOT / "distribution", root / "distribution", ignore=shutil.ignore_patterns("__pycache__", "tests"))
            path = root / "pack/config/bcc-common.toml"
            path.write_bytes(path.read_bytes() + b"\n# corrupted\n")
            with self.assertRaisesRegex(ValueError, "Managed file hash mismatch"):
                r.validate(root)

    def test_unaligned_historical_version_is_not_accepted_for_future_promotion(self):
        # Existing 0.2.1 deliberately remains untouched by migration.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            archive = root / "snapshot.zip"
            r.git("archive", "--format=zip", "--output=" + str(archive), "v0.2.1")
            with zipfile.ZipFile(archive) as z:
                z.extractall(root)
            r.validate(root)
            with self.assertRaises(ValueError):
                r.validate(root, aligned=True)

    def zip_fixture(self, out, selection="v0.2.0", source="a" * 40, url_ref=None):
        path = out / "pack.zip"
        prefix = f"Create-Ch4oS-{selection}/"
        target = url_ref or (source if selection.startswith("v") else selection)
        with zipfile.ZipFile(path, "w") as z:
            z.writestr(prefix + "instance.cfg", f'PreLaunchCommand=java -jar packwiz-installer-bootstrap.jar --bootstrap-no-update -s client "{r.RAW}/{target}/pack/pack.toml"\n')
            z.writestr(prefix + "release.txt", f"Pack source: {source}\n")
            z.writestr(prefix + ".minecraft/packwiz-installer-bootstrap.jar", b"tool")
            z.writestr(prefix + ".minecraft/packwiz-installer.jar", b"tool")
            z.writestr(prefix + ".minecraft/third-party-notices/industrialized-architecture-LICENSE.txt", "notice")
        Path(str(path) + ".sha256").write_text(f"{r.digest(path)}  {path.name}\n")
        return path

    def test_fixed_zip_rejects_public_url_and_modified_archive(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = self.zip_fixture(root)
            r.inspect_zip(path, "v0.2.0", "a" * 40)
            path = self.zip_fixture(root, url_ref="public")
            with self.assertRaisesRegex(ValueError, "wrong pack URL"):
                r.inspect_zip(path, "v0.2.0", "a" * 40)
            path = self.zip_fixture(root)
            with zipfile.ZipFile(path, "a") as z:
                z.writestr("Create-Ch4oS-v0.2.0/.minecraft/mods/gameplay.jar", b"bad")
            with self.assertRaisesRegex(ValueError, "only the two Packwiz"):
                r.inspect_zip(path, "v0.2.0", "a" * 40)

    def test_rolling_url_and_fixed_url_resolve_differently(self):
        # Independent of remote availability: the selected reference is encoded in
        # the real Prism command, not inferred from a ZIP filename or release title.
        with tempfile.TemporaryDirectory() as tmp:
            path = self.zip_fixture(Path(tmp), "beta")
            r.inspect_zip(path, "beta", "a" * 40)
            path = self.zip_fixture(Path(tmp), "v0.2.0", url_ref="beta")
            with self.assertRaises(ValueError):
                r.inspect_zip(path, "v0.2.0", "a" * 40)

    def test_failed_or_wrong_candidate_mvt_blocks_publication(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            (out / "mvt-results").mkdir()
            manifest = {"packaging": "tooling", "candidate": "candidate", "version": "0.2.2", "files": {}}
            for status, sha in (("failed", "candidate"), ("error", "candidate"),
                                ("running", "candidate"), ("lifecycle_passed_logs_unreviewed", "other")):
                r.write_json(out / "mvt-results/report.json", {"status": status, "pack_sha": sha})
                with patch.object(r, "git", return_value="tooling"), self.assertRaisesRegex(ValueError, "MVT did not pass"):
                    r.check_manifest(out, manifest)

    def test_conflicting_tag_is_never_moved(self):
        with patch.object(r, "tag_sha", return_value="old"), patch.object(r, "api") as api:
            with self.assertRaisesRegex(ValueError, "Refusing to move"):
                r.publish_assets("v0.2.2", "new", Path("unused"), "v0.2.2")
            api.assert_not_called()

    def test_fixed_upload_retry_checks_existing_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            name = "Create-Ch4oS-0.2.2-Prism.zip"
            (out / name).write_bytes(b"prepared zip")
            (out / (name + ".sha256")).write_text("checksum")
            (out / "v0.2.2.md").write_text("notes")
            calls = []
            def command(*args, **kwargs):
                calls.append(args)
                if args[:3] == ("gh", "release", "download"):
                    dest = Path(args[args.index("--dir") + 1])
                    shutil.copyfile(out / name, dest / name)
                return ""
            rel = {"id": 1, "draft": True, "assets": [{"name": name}]}
            with patch.object(r, "tag_sha", return_value="sha"), patch.object(r, "release", return_value=rel), \
                    patch.object(r, "run", side_effect=command), patch.object(r, "api"):
                r.publish_assets("v0.2.2", "sha", out, "v0.2.2")
            uploads = [args for args in calls if args[:3] == ("gh", "release", "upload")]
            self.assertEqual(len(uploads), 1)
            self.assertIn(str(out / (name + ".sha256")), uploads[0])
            self.assertFalse(any("--clobber" in args for args in calls))

    def test_changed_fixed_asset_blocks_retry(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            name = "Create-Ch4oS-0.2.2-Prism.zip"
            (out / name).write_bytes(b"new bytes")
            (out / "v0.2.2.md").write_text("notes")
            def command(*args, **kwargs):
                if args[:3] == ("gh", "release", "download"):
                    dest = Path(args[args.index("--dir") + 1])
                    (dest / name).write_bytes(b"old bytes")
                return ""
            with patch.object(r, "tag_sha", return_value="sha"), \
                    patch.object(r, "release", return_value={"id": 1, "draft": True, "assets": [{"name": name}]}), \
                    patch.object(r, "run", side_effect=command), patch.object(r, "api") as api:
                with self.assertRaisesRegex(ValueError, "refusing to overwrite"):
                    r.publish_assets("v0.2.2", "sha", out, "v0.2.2")
                api.assert_not_called()


class GitRaceTests(unittest.TestCase):
    def test_atomic_branch_update_refuses_concurrent_writer(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            remote = root / "remote.git"
            local = root / "local"
            r.run("git", "init", "--bare", str(remote), cwd=root)
            r.run("git", "init", str(local), cwd=root)
            def git(*args):
                return r.git(*args, cwd=local)
            git("config", "user.name", "Test")
            git("config", "user.email", "test@example.invalid")
            git("remote", "add", "origin", str(remote))
            git("commit", "--allow-empty", "-m", "base")
            base = git("rev-parse", "HEAD")
            git("push", "origin", f"{base}:refs/heads/public", f"{base}:refs/heads/main", f"{base}:refs/heads/beta")
            git("commit", "--allow-empty", "-m", "candidate")
            candidate = git("rev-parse", "HEAD")
            git("commit", "--allow-empty", "-m", "manual public edit")
            other = git("rev-parse", "HEAD")
            git("push", "origin", f"{other}:refs/heads/public", f"{other}:refs/heads/beta")
            with self.assertRaises(subprocess.CalledProcessError):
                git("push", "--atomic", "origin", f"--force-with-lease=refs/heads/public:{base}",
                    f"--force-with-lease=refs/heads/main:{base}", f"{candidate}:refs/heads/public", f"{candidate}:refs/heads/main")
            self.assertIn(base + "\trefs/heads/main", git("ls-remote", "origin", "refs/heads/main"))
            with self.assertRaises(subprocess.CalledProcessError):
                git("push", "origin", f"--force-with-lease=refs/heads/beta:{base}", f"{candidate}:refs/heads/beta")


if __name__ == "__main__":
    unittest.main()
