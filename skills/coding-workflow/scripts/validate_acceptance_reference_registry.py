#!/usr/bin/env python3
"""Validate governed independent acceptance-reference registry entries."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

REQUIRED = {"acceptance_reference_id", "owner", "reviewer", "version", "status", "source", "source_digest", "frozen_at", "coverage", "known_gaps"}
VALID = {"draft", "reviewed", "frozen", "active", "stale", "superseded"}


def validate(data: object, require_active: bool = False) -> list[str]:
    """Check the whole registry before any governed binding can be trusted."""
    if not isinstance(data, dict) or not isinstance(data.get("acceptance_references"), list):
        return ["acceptance_references must be a list"]
    entries = data["acceptance_references"]
    errors: list[str] = []
    seen: set[str] = set()
    has_active = False
    now = datetime.now(timezone.utc)
    for i, entry in enumerate(entries):
        prefix = f"acceptance_references[{i}]"
        if not isinstance(entry, dict):
            errors.append(f"{prefix} must be an object")
            continue
        missing = sorted(REQUIRED - entry.keys())
        if missing:
            errors.append(f"{prefix} missing: {', '.join(missing)}")
        for key in sorted(REQUIRED - {"coverage", "known_gaps"}):
            value = entry.get(key)
            if not isinstance(value, str) or not value:
                errors.append(f"{prefix} {key} must be a non-empty string")
        identifier = entry.get("acceptance_reference_id")
        if isinstance(identifier, str):
            if identifier in seen:
                errors.append(f"duplicate acceptance_reference_id: {identifier}")
            seen.add(identifier)
        status = entry.get("status")
        if not isinstance(status, str) or status not in VALID:
            errors.append(f"{prefix} invalid status")
        if status in ("frozen", "active"):
            has_active = True
            if not entry.get("frozen_at"):
                errors.append(f"{prefix} is not frozen")
        for key in ("coverage", "known_gaps"):
            values = entry.get(key)
            if not isinstance(values, list) or not all(isinstance(value, str) for value in values):
                errors.append(f"{prefix} {key} must be a list of strings")
        review = entry.get("review_after")
        if review is not None:
            try:
                if not isinstance(review, str):
                    raise ValueError("review_after must be a timestamp string")
                when = datetime.fromisoformat(review.replace("Z", "+00:00"))
                if when.tzinfo is None:
                    when = when.replace(tzinfo=timezone.utc)
                if when < now and status == "active":
                    errors.append(f"{prefix} active past review_after")
            except ValueError:
                errors.append(f"{prefix} invalid review_after")
    if require_active and not has_active:
        errors.append("no active or frozen Acceptance Reference")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("registry")
    parser.add_argument("--require-active", action="store_true")
    args = parser.parse_args()
    try:
        data = json.loads(Path(args.registry).read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        result = {"valid": False, "count": 0, "errors": [f"cannot read registry: {error}"]}
    else:
        errors = validate(data, args.require_active)
        entries = data.get("acceptance_references") if isinstance(data, dict) else None
        result = {"valid": not errors, "count": len(entries) if isinstance(entries, list) else 0, "errors": errors}
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
