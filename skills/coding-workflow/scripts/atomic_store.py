#!/usr/bin/env python3
"""Atomic JSON read/write helper for resumable task state."""
from __future__ import annotations
import argparse, json, os, tempfile
from pathlib import Path

def write_atomic(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(name, path)
        json.loads(path.read_text(encoding="utf-8"))
    finally:
        if os.path.exists(name): os.unlink(name)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()
    write_atomic(Path(args.output), json.loads(Path(args.input).read_text(encoding="utf-8")))
    print(json.dumps({"written": str(Path(args.output).resolve()), "atomic": True}))
    return 0

if __name__ == "__main__": raise SystemExit(main())
