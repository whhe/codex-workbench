# Task Storage

Load when the selected task needs persistent records, ledgers, check output or recovery artifacts. Light one-shot code tasks may keep a concise conversation record; contribution collection and publication ledgers use external storage.

## Task records and storage

Maintain one authoritative task record. Use a brief free-form record for Standard work and the structured `assets/work-record.example.json` for Deep work. Fill applicable fields; identify facts, assumptions, predictions, acceptance conditions, scope, decisions, and verification gaps. Reconcile the current source and target state before resuming. Other tooling may update this record but must not create competing records.

Store task records, evidence, check output, checkpoints, and recovery files in a per-task directory under the user's persistent application-data directory:

- macOS: the user's `Library/Application Support/coding-workflow` directory.
- Linux: `XDG_DATA_HOME/coding-workflow`, falling back to the user's `.local/share/coding-workflow` directory.
- Windows: `LOCALAPPDATA/coding-workflow`.

Use a repository identifier derived from its resolved path plus a unique task ID to prevent collisions. `scripts/task_storage.py --repository <repository>` creates and prints the directory; reuse it with `--task-id <id>` when resuming. Record the location in the conversation. Resolve symlinks and ensure storage is outside the repository. Ask for another location if the user-data location is unavailable or inside the repository. Retain files until the user requests cleanup.

All script input/output and evidence artifact paths must use this external task directory. Run checks against the repository via explicit working-directory arguments. Ordinary project build/test outputs follow project conventions; this rule concerns files introduced by the workflow itself. Keep credentials and unnecessary sensitive data out of retained records.

