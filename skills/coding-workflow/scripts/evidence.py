#!/usr/bin/env python3
"""Validate and index evidence against stable repository content identities."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
from datetime import datetime


DIGEST = re.compile(r"sha256:[0-9a-f]{64}\Z")
RESULTS = {"passed", "failed", "blocked", "inconclusive"}


def digest_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def is_digest(value: object) -> bool:
    return isinstance(value, str) and DIGEST.fullmatch(value) is not None


def file_identity(info: os.stat_result | None) -> tuple[int, ...] | None:
    """Detect capture races without treating reads that update access time as writes."""
    if info is None:
        return None
    return (info.st_dev, info.st_ino, info.st_mode, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def source_snapshot(workdir: str) -> dict[str, object]:
    """Hash tracked and nonignored new files at the repository root, or explain gaps."""
    snapshot: dict[str, object] = {"status": "unknown", "fingerprint": "", "errors": []}

    def git(directory: str, *args: str) -> bytes:
        process = subprocess.run(["git", "-C", directory, *args], capture_output=True)
        if process.returncode:
            raise ValueError("Git source inspection failed: " + os.fsdecode(process.stderr).strip())
        return process.stdout

    try:
        root = os.fsdecode(git(workdir, "rev-parse", "--show-toplevel").removesuffix(b"\n"))
        snapshot["repository"] = root
        commit = subprocess.run(["git", "-C", root, "rev-parse", "--verify", "HEAD"], capture_output=True)
        snapshot["git_commit"] = os.fsdecode(commit.stdout).strip() if commit.returncode == 0 else ""
        status = git(root, "status", "--porcelain=v1", "-z")
        snapshot["dirty"] = bool(status)
        stages = git(root, "ls-files", "--stage", "-z")
        if any(entry.startswith(b"160000 ") for entry in stages.split(b"\0")):
            raise ValueError("submodule content binding is unsupported")

        def population() -> list[bytes]:
            return sorted(set(git(root, "ls-files", "--cached", "--others", "--exclude-standard", "-z").split(b"\0")) - {b""})

        names = population()
        hasher = hashlib.sha256()
        observed: list[tuple[Path, os.stat_result | None]] = []
        for name in names:
            relative = Path(os.fsdecode(name))
            if relative.is_absolute() or ".." in relative.parts:
                raise ValueError("source path escapes repository")
            path = Path(root) / relative
            for parent in [path, *path.parents]:
                if parent == Path(root):
                    break
                if parent.is_symlink():
                    raise ValueError(f"symbolic link content binding is unsupported: {relative}")
            try:
                before = path.stat()
            except FileNotFoundError:
                # Missing tracked paths are observed for races, but contribute no content.
                observed.append((path, None))
                continue
            else:
                if not stat.S_ISREG(before.st_mode):
                    raise ValueError(f"source is not a regular file: {relative}")
                file_hash = hashlib.sha256()
                with path.open("rb") as stream:
                    opened = os.fstat(stream.fileno())
                    if file_identity(opened) != file_identity(before):
                        raise ValueError(f"source changed during capture: {relative}")
                    for block in iter(lambda: stream.read(1024 * 1024), b""):
                        file_hash.update(block)
                    if file_identity(os.fstat(stream.fileno())) != file_identity(opened):
                        raise ValueError(f"source changed during capture: {relative}")
                content = file_hash.hexdigest()
            entry = [os.fsdecode(name), stat.S_IMODE(before.st_mode) & 0o111, content]
            hasher.update(json.dumps(entry, ensure_ascii=True, separators=(",", ":")).encode() + b"\n")
            observed.append((path, before))
        if population() != names:
            raise ValueError("source file population changed during capture")
        for path, before in observed:
            try:
                after = path.stat()
            except FileNotFoundError:
                after = None
            if path.is_symlink() or file_identity(before) != file_identity(after):
                raise ValueError("source changed during capture: " + str(path))
        snapshot.update(status="complete", fingerprint="sha256:" + hasher.hexdigest(), file_count=len(names))
    except (OSError, ValueError) as error:
        snapshot["errors"] = [str(error)]
    return snapshot


def bind_source(before: dict[str, object], after: dict[str, object]) -> dict[str, object]:
    """Describe whether both observations identify the same complete repository content."""
    complete = before.get("status") == after.get("status") == "complete"
    stable = complete and before.get("repository") == after.get("repository") and before.get("fingerprint") == after.get("fingerprint")
    return {"binding": "stable" if stable else ("changed" if complete else "unknown"), "before": before, "after": after,
            "git_commit": after.get("git_commit", ""), "dirty": after.get("dirty", False)}


def bound_fingerprint(record: dict[str, object]) -> str | None:
    """Return a content identity only when both observations and the declared identity agree."""
    source = record.get("source")
    if not isinstance(source, dict) or source.get("binding") != "stable":
        return None
    before, after = source.get("before"), source.get("after")
    if not isinstance(before, dict) or not isinstance(after, dict):
        return None
    fingerprint = before.get("fingerprint")
    if (before.get("status") == after.get("status") == "complete" and is_digest(fingerprint)
            and fingerprint == after.get("fingerprint") == record.get("source_fingerprint")
            and isinstance(before.get("repository"), str) and Path(before["repository"]).is_absolute()
            and before["repository"] == after.get("repository")):
        return fingerprint
    return None


def validate_record(record: object) -> list[str]:
    """Validate archival v1/v2 records and v2 artifacts independently of acceptance eligibility."""
    if not isinstance(record, dict):
        return ["record must be an object"]
    errors: list[str] = []
    for key in ("evidence_id", "claim_id", "command", "workdir", "started_at", "finished_at"):
        if not isinstance(record.get(key), str) or not record[key]:
            errors.append(f"{key} must be a nonempty string")
    for key in ("started_at", "finished_at"):
        value = record.get(key)
        if isinstance(value, str):
            try:
                timestamp = datetime.fromisoformat(value[:-1] + "+00:00" if value.endswith("Z") else value)
                if timestamp.utcoffset() is None:
                    raise ValueError("timezone required")
            except ValueError:
                errors.append(f"{key} must be an ISO timestamp with timezone")
    for key in ("environment", "scope"):
        if not isinstance(record.get(key), dict):
            errors.append(f"{key} must be an object")
    if not isinstance(record.get("independent_acceptance_reference"), str):
        errors.append("independent_acceptance_reference must be a string")
    status, code = record.get("result"), record.get("exit_code")
    if not isinstance(status, str) or status not in RESULTS:
        errors.append("invalid result")
    if type(code) is not int:
        errors.append("exit_code must be int")
    elif isinstance(status, str) and ((status == "passed" and code != 0) or (status in {"failed", "blocked"} and code == 0)):
        errors.append("result and exit_code disagree")
    version = record.get("schema_version")
    if type(version) is not int or version not in (1, 2):
        errors.append("unsupported schema_version")
    elif version == 1:
        for key in ("stdout_digest", "stderr_digest"):
            if not is_digest(record.get(key)):
                errors.append(f"{key} must be a SHA-256 digest")
    else:
        for key in ("source", "redaction"):
            if not isinstance(record.get(key), dict):
                errors.append(f"{key} must be an object")
        for name in ("stdout", "stderr"):
            item = record.get(name)
            if not isinstance(item, dict):
                errors.append(f"{name} must be an object")
                continue
            location = item.get("path")
            if not isinstance(location, str) or not Path(location).is_absolute():
                errors.append(f"{name} artifact path must be absolute")
                continue
            try:
                content = Path(location).read_bytes()
            except (OSError, ValueError) as error:
                errors.append(f"{name} artifact unavailable: {error}")
                continue
            if digest_bytes(content) != item.get("digest"):
                errors.append(f"{name} digest mismatch")
            if type(item.get("bytes")) is not int or item["bytes"] != len(content):
                errors.append(f"{name} byte count mismatch")
            if type(item.get("truncated")) is not bool:
                errors.append(f"{name} truncated must be bool")
        source = record.get("source")
        if isinstance(source, dict) and "binding" in source:
            binding = source["binding"]
            if binding not in ("stable", "changed", "unknown"):
                errors.append("invalid source binding")
            if binding == "stable" and bound_fingerprint(record) is None:
                errors.append("stable source binding is inconsistent")
    return errors


def build_index(data: object) -> dict[str, object]:
    """Validate the complete batch before indexing; unbound records remain diagnostic only."""
    if not isinstance(data, dict):
        raise ValueError("input must be an object")
    claims, records = data.get("acceptance_claims"), data.get("evidence_records")
    if not isinstance(claims, list) or any(not isinstance(c, str) or not c for c in claims):
        raise ValueError("acceptance_claims must be a list of nonempty strings")
    if not isinstance(records, list):
        raise ValueError("evidence_records must be a list")
    errors, seen = [], set()
    for position, record in enumerate(records):
        errors.extend(f"record[{position}]: {error}" for error in validate_record(record))
        if isinstance(record, dict) and isinstance(record.get("evidence_id"), str):
            identity = record["evidence_id"]
            if identity in seen:
                errors.append(f"record[{position}]: duplicate evidence_id {identity}")
            seen.add(identity)
    if errors:
        raise ValueError("; ".join(errors))
    index: dict[str, dict[str, object]] = {}
    for record in records:
        claim = record["claim_id"]
        if claim not in claims:
            continue
        entry = index.setdefault(claim, {"passed": [], "failed": [], "inconclusive": [], "fingerprints": [], "acceptance_references": [], "conflict": False})
        fingerprint = bound_fingerprint(record) if record["schema_version"] == 2 else None
        status = record["result"]
        bucket = "inconclusive"
        if fingerprint:
            bucket = "passed" if status == "passed" else ("failed" if status == "failed" or record["exit_code"] != 0 else "inconclusive")
            entry["fingerprints"].append(fingerprint)
        entry[bucket].append(record["evidence_id"])
        entry["acceptance_references"].append(record["independent_acceptance_reference"])
    for entry in index.values():
        entry["fingerprints"] = sorted(set(entry["fingerprints"]))
        entry["acceptance_references"] = sorted(set(entry["acceptance_references"]))
        entry["conflict"] = bool(entry["passed"] and entry["failed"]) or len(entry["fingerprints"]) > 1
    return {"schema_version": 1, "acceptance_claims": sorted(set(claims)), "claims": index}
