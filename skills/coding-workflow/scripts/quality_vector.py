#!/usr/bin/env python3
"""Generate a non-collapsed quality vector from evidence records."""
from __future__ import annotations
import argparse, json
from pathlib import Path

DIMS = ["functional", "regression", "hidden", "property", "mutation", "boundary", "replay", "gui", "long_running", "rollback", "artifact", "static", "state_flow", "browser", "independent_acceptance", "user_validation", "production"]
VALID = {"passed", "failed", "partial", "not_run", "not_applicable", "unknown", "blocked", "not_ready"}


def classify_product_completion(spec: dict) -> dict:
    """Return explicit product-facing completion levels without collapsing them."""
    levels = ["artifact", "static", "state_flow", "browser", "independent_acceptance", "user_validation", "production"]
    result = {}
    for level in levels:
        item = spec.get(level, {"status": "unknown", "evidence": []})
        if isinstance(item, str): item = {"status": item, "evidence": []}
        if item.get("status") not in VALID: raise SystemExit(f"invalid completion status for {level}: {item.get('status')}")
        result[level] = item
    return result


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("input")
    p.add_argument("--output", required=True)
    a = p.parse_args()
    spec = json.loads(Path(a.input).read_text(encoding="utf-8"))
    vector = {}
    for dim in DIMS:
        item = spec.get(dim, {"status": "unknown", "evidence": []})
        if isinstance(item, str): item = {"status": item, "evidence": []}
        status = item.get("status", "unknown")
        if status not in VALID: raise SystemExit(f"invalid status for {dim}: {status}")
        vector[dim] = {"status": status, "evidence": item.get("evidence", []), "rationale": item.get("rationale", "")}
    out = {"schema_version": 1, "quality_vector": vector, "completion_levels": classify_product_completion(spec)}
    Path(a.output).write_text(json.dumps(out, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"output": str(Path(a.output).resolve()), "dimensions": len(vector)}, ensure_ascii=False))
    return 0

if __name__ == "__main__": raise SystemExit(main())
