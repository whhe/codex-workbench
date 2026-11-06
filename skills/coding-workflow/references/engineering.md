# Implementation and Verification

Use this module only for implementation/debugging or verification of code behavior. Read implementation-conventions.md before editing source, scripts or tests. Use precommit-review.md for the mandatory independent review gate; it is the single owner of that loop. Use task-storage.md only when persistent records are needed. Load project-config.md for Python execution environments, environment variables or new-project scaffolding; follow global execution limits for all checks.

## Before implementation

Establish the goal and scope under the entrypoint before modifications. Read planning.md and pass its independent plan review gate before editing source, scripts or tests. It has the same trigger scope as precommit-review.md, regardless of risk or whether new tests are needed. If a contribution or review task introduces code changes, enter this gate before those changes too.

If the target belongs to an existing Git checkout, load git-operations.md and satisfy its applicable pre-edit branch/ownership/synchronization checks before source edits; do not postpone them until a commit or push. These preparatory checks do not authorize publication or change the task phase. Keep existing PR/MR head/ref constraints and unrelated work intact. For a non-Git target, branch checks are not applicable; do not initialize Git merely to satisfy this preflight.

## Risk and effort

Judge the consequences of the requested action, including affected data, users, reversibility, and environment. Read `references/risk-policy.json` when assigning a level; it is the canonical signal-to-level mapping. The router script is optional. Record the reasons for escalation or evidence supporting de-escalation.

| Level | Typical scope | Required process |
|---|---|---|
| Light | Small reversible local change without behavior, trust, or external-effect claims | Scope, targeted acceptance check, concise result; no separate task record |
| Standard | Ordinary feature, integration, behavioral change, reusable code, or local state/concurrency work | Brief scope, acceptance conditions, decisions, checks and source version; persist when spanning turns, resuming, or tracking multiple acceptance conditions |
| Deep | Actions affecting production, live data migration, sensitive data, security boundaries, consequential external writes or irreversible effects | Structured task record with applicable fields, validated and indexed evidence, independent acceptance references for critical claims, recovery plan, and required-condition review |

Persistence, concurrency, permissions-related code, and migration code alone do not establish Deep risk: distinguish local implementation from live execution and actual security impact. Three failed fixes trigger diagnosis and recovery, without automatically changing the risk or authorization level. Evaluate real risk separately.

Use `scripts/risk_router.py` when classification is disputed or repeatability helps. Supply impact-qualified signals rather than marking production risk merely because a project will eventually be deployed. Unknown material impact requires investigation or clarification, not an assumed low-risk classification.

## Implementation and verification

Load `references/implementation-conventions.md` for source, script, or test edits. Prefer existing checks and independent expected results. Add or update test code only for a meaningful changed contract or uncovered risk that existing checks do not adequately verify. When inspection and existing evidence establish no relevant uncovered risk, add no test code; use proportionate existing checks or inspection and state the reason. Uncertainty is not evidence of no risk. Documentation and low-impact configuration edits do not require a new test suite.

Before collecting evidence, identify required acceptance conditions and applicable checks. Revise them only with an explicit reason recorded alongside the earlier conditions. Optional checks do not prevent completion.

- Light: run targeted checks and report their actual results.
- Standard: retain commands, results, covered acceptance conditions, and source version; evidence scripts are optional.
- Deep: validate structured evidence and build a conflict-aware index. Read `references/runtime.md` for the pipeline.

Preserve failures, conflicts, and evidence from older code versions. Reassess old evidence after changes; a newer pass does not silently erase a failure. A check supports only its covered behavior. Browser blockage, missing user validation, and untested production behavior remain distinct gaps.

## Acceptance references

An acceptance reference is an explicit basis for judging correctness: a specification, expected input/output, existing regression, or a real fault reproduction. Prefer a basis independent of the new implementation. Implementation-generated tests alone cannot establish correctness for a critical Deep claim.

Standard work needs traceable references for key behavior, without mandatory registry maintenance. Deep work needs independent references for critical risk claims. The registry and its validation script are optional tools for repeatable governance. If a missing reference affects a required acceptance condition, completion remains pending; otherwise report the limitation.

## Targeted checks

- Debugging: establish expected/actual behavior, reproduction or reliable incident evidence, environment, timeline, competing explanations, and prior attempts before core fixes.
- State, retry, concurrency: define state meanings, transitions, invariants, mutation authority, repeat execution, side effects, and recovery. Preserve failing sequences when useful.
- Browser interaction: verify actions and resulting state, affected views, and persistence when claimed. Read the browser fallback reference only when relevant; static success cannot establish interactive success.
- Three failed fixes: stop stacking patches, inventory reality, revisit hypotheses and architecture, select one bounded change, and establish replay and rollback.

Share the same record across all checks. These checks grant no extra scope or authority.

## Completion and reporting

For Light and Standard work, assess the declared required conditions directly; the completion script is optional. Deep work requires explicit review of every required condition; the script remains optional, but structured evidence is required. For actual external actions, confirm existing authorization and read back the resulting target state. Existing user authorization applies; ask only for missing material scope or authority.

Use these user-facing outcomes:

- Completed: all required conditions verified, relevant conflicts resolved, and authority sufficient.
- Pending verification: required evidence or acceptance references unavailable, stale, or incomplete.
- Blocked: a required condition failed, required evidence conflicts, or authority for the requested external action is missing.

Report what changed, what was actually verified, and material gaps. Add recovery details or a user decision only when relevant. Avoid imposing a fixed report template on routine tasks.

