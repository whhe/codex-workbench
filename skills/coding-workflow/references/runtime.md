# Runtime Tools

Use the project environment where available. The bundled runtime uses Python 3.10+ and the standard library. Resolve script and asset paths relative to this skill's directory; run commands from the external task directory or provide absolute paths. Never create runtime records, evidence artifacts, or checkpoints inside the target repository or installed skill package.

## Storage

Run `python <skill>/scripts/task_storage.py --repository <repository>`. It prints a persistent per-repository, per-task directory outside the repository. Preserve the printed location and task ID for resumption. Use `--task-id <id>` to reopen it. If allocation fails, ask the user for an external location; do not fall back to the working directory.

The storage allocator verifies resolved paths, including symlinks. Other runtime tools accept explicit paths and rely on the caller to use the allocated task directory. Test fixtures may use external disposable temporary directories; retained task records use the persistent directory.

## Optional risk routing

Write `signals.json` in the task directory and run:

```text
python <skill>/scripts/risk_router.py <task>/signals.json --output <task>/risk.json
```

Input accepts a signals object or `{"signals": {...}}`. The canonical policy is `risk-policy.json`. Actual production, sensitive-data, security, external-effect and irreversible-impact signals trigger Deep. Local persistence, concurrency, permissions and migration implementation trigger Standard. Three failed fixes add debug/recovery checks without changing the mode. The host must determine actual impact; the script does not inspect code or infer safety from missing signals.

## Structured task record

Copy `assets/work-record.example.json` to external storage, replace example content, and add applicable fields. Validate with `scripts/validate_work_record.py <task>/work.json`. Required fields are schema_version, work_id, raw_request, outcome, scope, claims, acceptance, risk, completion_requirements and authority. Claims contain claim_id, type (fact/assumption/prediction) and statement; acceptance and completion conditions link claim IDs.

Declare required checks before implementation. Supported statuses: passed, failed, partial, not_run, not_applicable, blocked, unknown, not_ready. Keep the required flag separate from status. Record revisions rather than changing the acceptance threshold silently.

For actual external actions set `external_action: true`, `authority.required: true`, and record actor, target, scope, existing authorization, and any applicable expiry. Completion requires observed target readback (`readback_verified: true`); authorization by itself is insufficient. Deep local implementation does not require external-action authorization.

## Evidence pipeline

Deep work requires structured evidence; Standard may use it when helpful. Evidence command timeouts must be finite positive numbers.

1. Execute a check with `scripts/evidence_runner.py --claim-id C1 --command "<check command>" --workdir <repository> --scope-file <file> --scope-test <test> --acceptance-reference-id R1 --output <task>/evidence.json`.
2. Optionally inspect a record using `scripts/validate_evidence.py <task>/evidence.json`. It reports archival validity and `source_bound` separately; valid diagnostic records cannot establish passing acceptance.
3. Write an index input containing `acceptance_claims` and `evidence_records` (the full records). Run `scripts/evidence_index.py <task>/index-input.json --output <task>/index.json`. The shared evidence module validates every record, including records outside the selected claims, before building any index. Invalid records, missing or modified artifacts, relative artifact paths and duplicate evidence IDs reject the entire batch with diagnostics and a nonzero exit. No replacement index is written on rejection; check the exit code before using an existing output path.
4. Review conflicting passes/failures and source divergence before completion. Preserve prior evidence and record explicit reconciliation decisions.

Records retain redacted stdout/stderr and command text (execution uses the original command), environment, scope, source state and acceptance-reference ID. Output is decoded as UTF-8 with replacement for invalid bytes, redacted before truncation, then stored up to `--max-output-bytes` per stream without splitting UTF-8 characters. Stream metadata reports stored bytes and whether redacted output was truncated; the limit does not bound process output held in memory. Redaction is best effort: avoid commands that expose secrets. Evidence command execution currently supports macOS/Linux only; other platforms are rejected before any command starts. On timeout the runner kills the inherited process group, reaps the direct process and drains captured output before sampling source state and writing a blocked check (exit 124). Output draining has a five-second cleanup timeout; if cleanup fails, execution exits nonzero with a diagnostic and no new evidence record. Check the exit code before reusing any existing output file. Children that detach into another session escape this group cleanup; this is not process containment or a sandbox, and commands must not leave detached background work. The runner does not enforce authority; run only already-authorized commands. The runner samples repository content before and after execution. The content fingerprint includes repository-relative file paths, contents, executable attributes, and nonignored new files across the entire repository, even for a subdirectory workdir. Deleted files contribute no content; staging or committing a deletion does not change that content identity. Ignored untracked files are excluded; commit IDs are metadata and do not change content identity. Only complete, matching observations provide a stable source binding.

The runtime does not track symbolic-link targets or recurse into submodules. Encountering these, unreadable files, capture races or Git inspection failures yields explicit unknown binding diagnostics. Changed content during execution also makes the record ineligible. Historical v1/v2 records remain readable when structurally valid, but commit-only records and non-Git checks cannot establish source-bound passing acceptance. They stay in the index inconclusive bucket, outside fingerprint conflicts; existing conflicts between bound versions and bound passes/failures remain unchanged.

Artifact paths must be absolute. Standalone validation and index ingestion use the same validation implementation in `scripts/evidence.py`; callers need not maintain a separate validation step. Source metadata and JSON are local evidence, not authenticated attestations. Before/after sampling does not detect transient changes that revert between observations, and cannot prove that a command tested its declared scope. Human review still checks scope and the final code version.

External research, when needed, must record source URL, retrieval time, publication time when available, supporting passage and limitations. Search results are discovery; unavailable retrieval leaves the affected claim unknown. Runtime tools do not themselves supply browsing capabilities.

Use `scripts/atomic_store.py` for atomic resumable JSON writes where needed and `scripts/quality_vector.py` for optional diagnostics. These do not replace acceptance checks.

## Acceptance references

For Standard work a traceable specification, expected result or reproduction is sufficient; a registry is optional. Deep critical claims require a basis independent of the new implementation.

The completion input accepts direct `acceptance_references` entries:

```json
{
  "acceptance_references": [
    {"acceptance_reference_id": "R1", "source": "Specification section or reproduction locator", "coverage": ["C1"], "independent": true, "verified": true}
  ],
  "required_reference_claims": ["C1"]
}
```

Set `required_reference_claims` to the predeclared critical required claims. Deep defaults to all required claims if the field is absent; Standard defaults to none. Verification, independence, authorization and readback flags require literal JSON `true`; strings and numbers do not establish those checks. A verified flag records a performed check; it is not evidence by itself.

For governed registries, copy `acceptance-references.json` into external task storage and populate it using `acceptance-references.schema.json`. Validate with `scripts/validate_acceptance_reference_registry.py <task>/references.json --require-active`. This optional registry records ownership, review, coverage, digest, gaps and lifecycle.

Bind registry references with `acceptance_reference_registry` (absolute path) and `acceptance_reference_bindings` entries containing claim_id, acceptance_reference_id and verified. The standalone validator and completion gate share whole-registry format and lifecycle validation. Any registry error (including an unrelated entry, duplicate ID, missing freeze or expired active entry) prevents its bindings from supporting completion and is reported. A registry remains optional; direct independent references do not require one. Bindings for required claims must resolve to active/frozen entries with a source and digest covering the claim. Optional missing references do not block required conditions. Explicit bindings to required completion claims require valid reference coverage even in Standard mode. A valid verified independent direct reference can supply that coverage when the governed binding is unusable; the invalid registry or binding still contributes no coverage. Diagnostics remain visible rather than invalidating unrelated or alternative valid references.

## Optional completion gate

Run `scripts/completion_gate.py <task>/completion-input.json --output <task>/decision.json`.

The output retains registry/binding diagnostics and missing-reference messages in acceptance_reference_errors, and lists uncovered required reference claims separately in missing_reference_claims. Diagnostics may coexist with accepted status: missing_reference_claims controls reference-related completion, while required evidence, failed checks, conflicts, authority and readback keep their existing gates.

Input includes mode, evidence_index (the validated index object), completion_requirements, acceptance_references or optional registry bindings, required_reference_claims, and authority/external_action when relevant. Each requirement has required, status and claims fields. A required condition marked passed must link a non-empty claims list; otherwise completion remains provisional and unsupported_conditions lists the condition name. Optional conditions and explicit not_applicable conditions may use empty lists. Do not mark failed checks not_applicable to bypass them.

- accepted (exit 0): required conditions passed with evidence and applicable references; external action authority and readback satisfied.
- provisional (exit 2): required evidence, references, check results or target readback remain incomplete; also used when no required conditions were declared.
- blocked (exit 2): a required condition failed, required evidence conflicts, or actual external execution lacks authority.

Optional check failures are retained in the evidence but do not decide completion. Local Deep work is not automatically an external action. Human review must verify appropriate scoping, current evidence and applicable authorization; the gate cannot establish these from caller-supplied JSON alone.

## Runtime changes

Compare baseline and candidate on the same inputs, checks and environment. Select the smallest relevant existing checks from test_kernel.py, test_runtime.py, test_workflow.py and test_evidence.py; broaden only for affected boundaries or a demonstrated dependency. Add or update a regression case only when a meaningful changed contract or risk is not adequately verified by existing checks; do not duplicate an already discriminating case. If no new test code is warranted, state why the existing checks or inspection suffice. Evaluate semantic behavior, not heading counts or wording. Full model comparisons are warranted only when the change's impact requires them.
