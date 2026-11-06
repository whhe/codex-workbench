#!/usr/bin/env python3
"""Allocate persistent workflow storage outside the target repository."""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import re
import sys
import uuid


def task_directory(repository: Path, task_id: str, data_root: Path | None = None) -> Path:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}", task_id):
        raise ValueError("task ID must be 1-80 letters, digits, underscores or hyphens")
    repository = repository.resolve(strict=True)
    if not repository.is_dir():
        raise ValueError("repository must be a directory")
    if data_root is None:
        if sys.platform == "darwin":
            data_root = Path.home() / "Library/Application Support"
        elif os.name == "nt":
            value = os.environ.get("LOCALAPPDATA")
            if not value:
                raise ValueError("LOCALAPPDATA unavailable; choose external storage")
            data_root = Path(value)
        else:
            data_root = Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local/share")
    if not data_root.is_absolute():
        raise ValueError("application-data directory must be absolute")
    repo_id = hashlib.sha256(str(repository).encode()).hexdigest()[:20]
    directory = (data_root / "coding-workflow" / repo_id / task_id).resolve()
    if directory == repository or repository in directory.parents:
        raise ValueError("workflow storage must be outside the repository")
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument("--task-id", default=None)
    args = parser.parse_args()
    try:
        print(task_directory(args.repository, args.task_id or uuid.uuid4().hex))
    except (OSError, ValueError) as error:
        parser.exit(1, f"{error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
