#!/usr/bin/env python3
"""Build an index only after the complete evidence batch passes validation."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from evidence import build_index


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        result = build_index(json.loads(Path(args.input).read_text(encoding="utf-8")))
    except (OSError, ValueError) as error:
        print(json.dumps({"valid": False, "errors": [str(error)]}, ensure_ascii=True))
        return 1
    Path(args.output).write_text(json.dumps(result, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(Path(args.output).resolve()), "claims": len(result["claims"])}, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
