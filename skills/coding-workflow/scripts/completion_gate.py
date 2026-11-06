#!/usr/bin/env python3
"""Assess required conditions, acceptance references and actual action authority."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from validate_acceptance_reference_registry import validate as validate_registry


def assess_references(data: dict, required_claims: set[str]) -> tuple[list[str], list[str]]:
    """Return retained diagnostics and missing required reference claims separately."""
    needed = set(data.get("required_reference_claims", [])) & required_claims
    if data.get("mode") == "deep" and "required_reference_claims" not in data:
        needed = required_claims
    covered = set()
    for reference in data.get("acceptance_references", []):
        if reference.get("source") and reference.get("verified") is True and reference.get("independent") is True:
            covered.update(reference.get("coverage", []))
    errors = []
    bindings = data.get("acceptance_reference_bindings", [])
    if bindings:
        try:
            registry = json.loads(Path(data["acceptance_reference_registry"]).read_text())
            registry_errors = validate_registry(registry)
            entries = {} if registry_errors else {r["acceptance_reference_id"]: r for r in registry["acceptance_references"]}
            errors.extend(f"invalid_acceptance_reference_registry:{error}" for error in registry_errors)
        except (OSError, ValueError, KeyError, TypeError) as error:
            entries = {}
            errors.append(f"invalid_acceptance_reference_registry:{error}")
        for binding in bindings:
            if not isinstance(binding, dict):
                errors.append("invalid_acceptance_reference_binding:unknown")
                continue
            claim = binding.get("claim_id")
            identifier = binding.get("acceptance_reference_id")
            if not isinstance(claim, str) or not isinstance(identifier, str):
                errors.append("invalid_acceptance_reference_binding:unknown")
                if isinstance(claim, str) and claim in required_claims:
                    needed.add(claim)
                continue
            if claim in required_claims:
                needed.add(claim)
            reference = entries.get(identifier, {})
            valid = reference.get("status") in {"active", "frozen"} and reference.get("source_digest") and reference.get("source") and binding.get("verified") is True and claim in reference.get("coverage", [])
            if valid:
                covered.add(claim)
            else:
                errors.append(f"invalid_acceptance_reference_binding:{claim}")
    missing = sorted(needed - covered)
    return errors + [f"missing_acceptance_reference:{claim}" for claim in missing], missing


def evaluate(data: dict) -> dict:
    index = data.get("evidence_index", {}).get("claims", {})
    levels = {}
    unsupported, conflicts, failed, required_claims = set(), set(), set(), set()
    unsupported_conditions: list[str] = []
    for name, requirement in data.get("completion_requirements", {}).items():
        required = bool(requirement.get("required"))
        status = requirement.get("status", "not_run")
        claims = requirement.get("claims", [])
        missing = []
        for claim in claims:
            evidence = index.get(claim, {})
            if not evidence.get("passed"):
                missing.append(claim)
            if required:
                required_claims.add(claim)
                if evidence.get("conflict"):
                    conflicts.add(claim)
                if evidence.get("failed"):
                    failed.add(claim)
        if required:
            if status == "passed" and not claims:
                unsupported_conditions.append(name)
            unsupported.update(missing)
            if status == "failed":
                failed.add(name)
        levels[name] = {"required": required, "status": status, "claims": claims, "missing_claims": missing}
    authority = data.get("authority", {})
    needs_authority = bool(data.get("external_action") or authority.get("required"))
    missing_auth = needs_authority and not (
        authority.get("authorized") is True and all(authority.get(key) for key in ("actor", "target", "scope"))
    )
    missing_readback = needs_authority and authority.get("readback_verified") is not True
    errors, missing_references = assess_references(data, required_claims)
    required_bad = any(r["required"] and r["status"] not in {"passed", "not_applicable"} for r in levels.values())
    if conflicts or failed or missing_auth:
        status = "blocked"
    elif unsupported or unsupported_conditions or required_bad or missing_references or missing_readback or not any(r["required"] for r in levels.values()):
        status = "provisional"
    else:
        status = "accepted"
    return {
        "schema_version": 4, "status": status, "completion_levels": levels,
        "unsupported_claims": sorted(unsupported), "conflicted_claims": sorted(conflicts),
        "unsupported_conditions": sorted(unsupported_conditions),
        "failed_conditions": sorted(failed), "missing_authorization": missing_auth,
        "missing_readback": missing_readback, "acceptance_reference_errors": errors,
        "missing_reference_claims": missing_references,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = evaluate(json.loads(Path(args.input).read_text()))
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["status"] == "accepted" else 2


if __name__ == "__main__":
    raise SystemExit(main())
