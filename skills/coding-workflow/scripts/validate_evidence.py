#!/usr/bin/env python3
"""Validate an archival evidence record; report source-bound acceptance eligibility."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from evidence import bound_fingerprint, validate_record


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record")
    args = parser.parse_args()
    try:
        record = json.loads(Path(args.record).read_text(encoding="utf-8"))
        errors = validate_record(record)
    except (OSError, ValueError) as error:
        record, errors = None, [str(error)]
    eligible = not errors and isinstance(record, dict) and record.get("schema_version") == 2 and bound_fingerprint(record) is not None
    print(json.dumps({"valid": not errors, "evidence_id": record.get("evidence_id") if isinstance(record, dict) else None,
                      "source_bound": bool(eligible), "errors": errors}, ensure_ascii=True))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
