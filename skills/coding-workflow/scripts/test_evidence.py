#!/usr/bin/env python3
"""Exercise evidence ingestion through files, real Git repositories and CLI adapters."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from evidence import build_index, source_snapshot, validate_record


SCRIPTS = Path(__file__).resolve().parent


class EvidenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.repo = self.base / "repo"
        self.repo.mkdir()
        self.git("init", "-q")
        (self.repo / "code.py").write_text("original\n")
        (self.repo / ".gitignore").write_text("ignored/\n")
        self.git("add", ".")
        self.counter = 0

    def git(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(["git", "-C", str(self.repo), *args], check=True, capture_output=True, text=True)

    def capture(self, code: str = "print('ok')", workdir: Path | None = None) -> tuple[Path, dict[str, object]]:
        self.counter += 1
        output = self.base / f"evidence-{self.counter}.json"
        command = shlex.join([sys.executable, "-c", code])
        result = subprocess.run([sys.executable, str(SCRIPTS / "evidence_runner.py"), "--claim-id", "C1", "--command", command,
                                 "--workdir", str(workdir or self.repo), "--output", str(output)], capture_output=True, text=True)
        self.assertTrue(output.exists(), result.stderr)
        return output, json.loads(output.read_text())

    def index(self, *records: dict[str, object]) -> dict[str, object]:
        return build_index({"acceptance_claims": ["C1"], "evidence_records": list(records)})

    def test_root_content_identity_tracks_actual_files(self) -> None:
        before = source_snapshot(str(self.repo))
        self.assertEqual(before["status"], "complete")
        nested = self.repo / "subdir"
        nested.mkdir()
        self.assertEqual(before["fingerprint"], source_snapshot(str(nested))["fingerprint"])
        ignored = self.repo / "ignored"
        ignored.mkdir()
        (ignored / "cache").write_text("ignored")
        self.assertEqual(before["fingerprint"], source_snapshot(str(self.repo))["fingerprint"])
        new = self.repo / "new file\nname.py"
        new.write_text("new")
        self.assertNotEqual(before["fingerprint"], source_snapshot(str(self.repo))["fingerprint"])
        new.unlink()
        tracked = self.repo / "code.py"
        tracked.write_text("edited\n")
        edited = source_snapshot(str(self.repo))["fingerprint"]
        self.assertNotEqual(before["fingerprint"], edited)
        tracked.chmod(tracked.stat().st_mode | 0o100)
        self.assertNotEqual(edited, source_snapshot(str(self.repo))["fingerprint"])
        tracked.unlink()
        self.assertEqual(source_snapshot(str(self.repo))["status"], "complete")

    def test_content_identity_survives_commits(self) -> None:
        before = source_snapshot(str(self.repo))["fingerprint"]
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false", "commit", "-qm", "fixture")
        self.assertEqual(before, source_snapshot(str(self.repo))["fingerprint"])
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false", "commit", "--allow-empty", "-qm", "same content")
        self.assertEqual(before, source_snapshot(str(self.repo))["fingerprint"])

    def test_deletion_identity_is_independent_of_staging_and_committing(self) -> None:
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false", "commit", "-qm", "fixture")
        original = source_snapshot(str(self.repo))["fingerprint"]
        (self.repo / "code.py").unlink()
        deleted = source_snapshot(str(self.repo))["fingerprint"]
        self.assertNotEqual(original, deleted)
        self.git("add", "-u")
        self.assertEqual(deleted, source_snapshot(str(self.repo))["fingerprint"])
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false", "commit", "-qm", "delete")
        self.assertEqual(deleted, source_snapshot(str(self.repo))["fingerprint"])

    def test_execution_affecting_permission_changes_invalidate_binding(self) -> None:
        source = self.repo / "code.py"
        source.chmod(0o744)
        before = source_snapshot(str(self.repo))["fingerprint"]
        source.chmod(0o645)
        self.assertNotEqual(before, source_snapshot(str(self.repo))["fingerprint"])
        source.chmod(0o744)
        _, record = self.capture("import os; os.chmod('code.py', 0o645)")
        self.assertEqual(record["source"]["binding"], "changed")
        self.assertFalse(self.index(record)["claims"]["C1"]["passed"])

    def test_repository_path_ending_in_newline_remains_bindable(self) -> None:
        before = source_snapshot(str(self.repo))["fingerprint"]
        destination = self.base / "repo\n"
        self.repo.rename(destination)
        self.repo = destination
        snapshot = source_snapshot(str(self.repo))
        self.assertEqual(snapshot["status"], "complete")
        self.assertEqual(before, snapshot["fingerprint"])

    def test_unreadable_source_is_explicitly_unbound(self) -> None:
        with patch("evidence.Path.open", side_effect=PermissionError("fixture denied")):
            snapshot = source_snapshot(str(self.repo))
        self.assertEqual(snapshot["status"], "unknown")
        self.assertEqual(snapshot["fingerprint"], "")
        self.assertIn("fixture denied", snapshot["errors"][0])

    def test_runner_and_both_adapters_agree_on_eligibility(self) -> None:
        output, record = self.capture()
        self.assertEqual(validate_record(record), [])
        check = subprocess.run([sys.executable, str(SCRIPTS / "validate_evidence.py"), str(output)], capture_output=True, text=True)
        self.assertEqual(check.returncode, 0, check.stdout)
        self.assertTrue(json.loads(check.stdout)["source_bound"])
        self.assertEqual(self.index(record)["claims"]["C1"]["passed"], [record["evidence_id"]])

    def test_tampered_artifact_rejects_whole_batch_including_unselected_claim(self) -> None:
        _, good = self.capture()
        _, bad = self.capture()
        bad["claim_id"] = "unselected"
        Path(bad["stdout"]["path"]).write_text("tampered")
        input_file, output = self.base / "input.json", self.base / "index.json"
        input_file.write_text(json.dumps({"acceptance_claims": ["C1"], "evidence_records": [good, bad]}))
        result = subprocess.run([sys.executable, str(SCRIPTS / "evidence_index.py"), str(input_file), "--output", str(output)], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(output.exists())
        self.assertIn("digest mismatch", result.stdout)

    def test_changed_source_and_non_git_records_are_diagnostic(self) -> None:
        _, changed = self.capture("from pathlib import Path; Path('code.py').write_text('changed')")
        self.assertEqual(changed["source"]["binding"], "changed")
        self.assertEqual(validate_record(changed), [])
        self.assertFalse(self.index(changed)["claims"]["C1"]["passed"])
        _, external = self.capture(workdir=self.base)
        self.assertEqual(external["source"]["binding"], "unknown")
        self.assertEqual(self.index(external)["claims"]["C1"]["inconclusive"], [external["evidence_id"]])

    def test_legacy_records_are_readable_but_not_passing(self) -> None:
        _, current = self.capture()
        legacy = copy.deepcopy(current)
        legacy["evidence_id"] = "legacy-v2"
        legacy["source"] = {"git_commit": "old", "dirty": False}
        legacy.pop("source_fingerprint")
        self.assertEqual(validate_record(legacy), [])
        v1 = copy.deepcopy(legacy)
        v1.update(schema_version=1, evidence_id="legacy-v1", stdout_digest=legacy["stdout"]["digest"], stderr_digest=legacy["stderr"]["digest"])
        for key in ("stdout", "stderr", "source", "redaction"):
            v1.pop(key)
        self.assertEqual(validate_record(v1), [])
        entry = self.index(current, legacy, v1)["claims"]["C1"]
        self.assertEqual(entry["passed"], [current["evidence_id"]])
        self.assertEqual(entry["inconclusive"], ["legacy-v2", "legacy-v1"])
        self.assertFalse(entry["conflict"])

    def test_unsupported_sources_remain_explicitly_unbound(self) -> None:
        (self.repo / "link").symlink_to(self.base / "missing")
        snapshot = source_snapshot(str(self.repo))
        self.assertEqual(snapshot["status"], "unknown")
        self.assertIn("symbolic link", snapshot["errors"][0])
        (self.repo / "link").unlink()
        blob = self.git("hash-object", "-w", "code.py").stdout.strip()
        self.git("update-index", "--add", "--cacheinfo", "160000", blob, "nested")
        snapshot = source_snapshot(str(self.repo))
        self.assertEqual(snapshot["status"], "unknown")
        self.assertIn("submodule", snapshot["errors"][0])

    def test_malformed_records_fail_with_diagnostics(self) -> None:
        _, record = self.capture()
        for field, value in (("result", []), ("exit_code", True), ("evidence_id", []), ("source", {"binding": "stable"})):
            with self.subTest(field=field):
                invalid = copy.deepcopy(record)
                invalid[field] = value
                with self.assertRaises(ValueError):
                    self.index(invalid)
        for field, value in (("path", "relative.stdout"), ("path", str(self.base)), ("path", str(self.base / "missing")), ("bytes", True)):
            with self.subTest(artifact=field, value=value):
                invalid = copy.deepcopy(record)
                invalid["stdout"][field] = value
                with self.assertRaises(ValueError):
                    self.index(invalid)
        with self.assertRaisesRegex(ValueError, "duplicate evidence_id"):
            self.index(record, record)

    def test_failures_and_versions_still_conflict(self) -> None:
        _, passed = self.capture()
        _, failed = self.capture("raise SystemExit(1)")
        self.assertTrue(self.index(passed, failed)["claims"]["C1"]["conflict"])
        (self.repo / "code.py").write_text("other version")
        _, newer = self.capture()
        self.assertTrue(self.index(passed, newer)["claims"]["C1"]["conflict"])


if __name__ == "__main__":
    unittest.main()
