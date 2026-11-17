# Workflow Records

Load when the selected task needs persistent records, ledgers, check output or recovery artifacts. Light one-shot code tasks may keep a concise conversation record; contribution collection and publication ledgers use external storage.

## Task records and storage

Maintain one authoritative task record. Use a brief free-form record for Standard work and the structured `assets/work-record.example.json` for Deep work. Fill applicable fields; identify facts, assumptions, predictions, acceptance conditions, scope, decisions, and verification gaps. Reconcile the current source and target state before resuming. Other tooling may update this record but must not create competing records.

Use the persistent session directory supplied by the coordinator under the active global or host storage instructions. If none has been supplied, resolve it under those instructions before writing records. Pass absolute input/output paths to runtime tools.

Keep one record per task and use distinct filenames for concurrent tasks or workers sharing the session directory. Record artifact paths in the task record and reuse them on continuation. Reconcile existing records before creating replacements.

Run checks against the repository via explicit working-directory arguments. Ordinary project build/test outputs follow project conventions. Keep credentials and unnecessary sensitive data out of retained records.
