# Review Feedback Implementation and Publication

Load only for an authorized feedback-handling request with pending work after review-collection.md. It owns Steps 4–9 and all mutation/recovery mechanics; reports return from collection without loading it. Read review-feedback.md for routing and contribution.md for the task authority matrix. Complete pagination continues to follow review-collection.md. Apply narrower user restrictions before every operation.

## Goal and Phase Guard

This path applies only to a user-delegated task advancing the specified existing PR/MR. Its implementation fixes remain within that review task; local review during a standalone implementation task does not enter this path. Before each iteration and before publishing, compare the full accumulated change, replies, transitions and metadata with the original goal, acceptance conditions and exclusions. New feedback can reveal an in-scope defect but cannot authorize unrelated work. Defer unrelated improvements; ask the user before resolving missing information or a material goal/scope decision. Once task authority and facts are established, do not add routine confirmation gates for scoped commits, pushes or necessary PR/MR updates.

## Publication and Review Triggers

Keep publication in this order: local fixes and required checks → local commit when needed → verified replies → verified Resolve/Reopen transitions → required PR/MR metadata updates → push or active review trigger. Before push, describe fixes as prepared locally; never claim they are already remote.

| Publication mode | Final operation after replies, transitions and metadata |
|---|---|
| Attributable commits to publish | Push the exact final SHA to the authoritative head ref; use the configured push-triggered review when applicable |
| Pending feedback handled without code changes; local/remote heads match; repository has a review workflow | Actively trigger that workflow through a supported non-comment API, rerun or dispatch mechanism |
| Pending feedback handled without code changes; repository has no review workflow | Verify replies, transitions and metadata; no review trigger is required |
| No pending feedback after complete collection | Read-only no-action exit; no trigger |

Code pushes normally trigger configured review automation. Ordinary replies, thread transitions, and metadata edits normally do not. Verify the repository's actual event, actor and ref filters; a successful push is not proof that a review started. Pushing an unchanged head is not a new review trigger. Do not manufacture an empty commit or rewrite history solely to trigger review.

Command-type comments, such as `/review`, require an explicit user request to publish that command comment. General authorization to handle feedback, trigger review, wait for results, or follow repository instructions does not supply that permission. This restriction also covers command text embedded in an otherwise ordinary reply. Prefer a supported non-comment trigger. If only a command comment is supported, ask before that step and report the trigger as pending; do not silently skip it, claim it ran, or send the comment.

Set `wait_for_review: false` by default. Change it only on an explicit user request to wait for review results. Triggering and observing completion are separate obligations. Default handling verifies the publication effects and any active-trigger acceptance, reports visible review status, and returns without waiting for runs, queued output, or future feedback. Required local checks before publication remain binding. Explicit review waiting does not authorize command comments.

## Global Rules

- **Self-contained execution**: Use a suitable authenticated provider interface for the exact host. Use `gh` or `glab` when that interface is needed; inspect supported capabilities before installing or changing authentication. A read-only interface suffices for collection. If an authorized operation lacks a required interface or authentication, report that prerequisite; do not replace a working interface merely to satisfy a tool preference. Keep triage, changes, review, replies, and metadata drafting in this package. Use shared pr-rules.md for PR/MR content; load redaction.md before pasting machine output.
- **Default autonomous execution**: A request to resolve feedback on one existing PR/MR authorizes its end-to-end handling by default, without special wording or separate approval for edits, targeted tests, commits, pushes, replies, metadata updates, Resolve/Reopen, review triggers, or the PR/MR-scoped lease lifecycle, subject to the command-comment restriction above. Record a standing scope envelope binding those operations to the authoritative PR/MR, source repository, full head ref, and exact attributable final SHA. Respect narrower user limits such as report-only, local-only, or no-push; do not interpret a read-only review as a resolution request. Check every concrete operation against that scope without asking for routine authorization. Scope expansion, material unresolved Clarify, failing or unverifiable required checks, unsafe attribution, drift that cannot be reconciled, ambiguous remote results, lost publication ownership, or unsafe destructive operations require stopping and reporting the blocker, not an approval loop. This path updates existing PR/MRs only; new issue/PR/MR creation and standalone metadata editing use the drafting path and its final-content confirmation gate. Platform permissions and higher-priority restrictions remain binding.
- **Complete collection**: Exhaust every page, cursor, continuation token, and nested connection before filtering. Partial results never prove completeness.
- **Minimal scope and verification**: Implement accepted feedback and required caller updates only. Reuse existing focused checks; add a targeted test only for a changed observable contract or an uncovered stable regression. Do not run broad suites or add tests solely for coverage or symmetry.
- **Change-only repository text**: Commit messages and PR/MR title/body must make sense from repository diff/history alone. Exclude reviewer names, comment IDs, “address review,” self-review/test execution reports, agent history, approval exchanges, and agent attribution.
- **Replay safety**: Refresh the exact target before a write. After ambiguity, reconcile its complete collection through the recorded visibility bound. Reuse a unique exact effect; multiple matches block further writes. Permit at most one identical retry for a proven non-triggering operation with unchanged preconditions or an operation using the same provider idempotency key. Never blindly retry a push or manual trigger.
- **Concurrent-publication safety**: Prefer an exclusive lease keyed by provider, repository stable ID, and PR/MR number; its lifecycle must not trigger review. Otherwise freeze and revalidate optimistic guards for the remote head, metadata, item fingerprints, reply targets, and thread states before each mutation. Record the lease owner token and expiry. Before every protected write, verify current ownership and enough remaining lifetime for the operation and its bounded reconciliation; renew through an authorized row before repeating freshness checks when needed. Expiry or ownership loss stops writes, including compensation. On every early stop or return after acquisition, reconcile outstanding mutations, perform only safe authorized compensation, then release and verify the lease if still owned; report any unknown release outcome. A lease coordinates only the writers it covers. Refresh-write-verify detects conflicts but does not prove atomic exclusion of external reviewers. If the requested guarantee requires inclusion of feedback written after the final snapshot, stop unless an atomic provider revision or a lease covering every context writer can enforce it.
- **Mutation authorization ledger**: Before the first remote write, freeze one row per exact operation: reply create/edit/compensating-create, duplicate delete, Resolve/Reopen and inverse, metadata update/restore, push, manual trigger, or lease acquire/renew/release. Record target, payload/state, preconditions, authorization source/scope, permitted compensation, and result. Match every row to the standing task scope and any explicit user restrictions; record default task authorization as its source rather than requesting per-operation approval. For duplicate deletion, require exact retain/delete IDs and proof that each deleted item is this workflow's own byte-identical duplicate; never delete reviewer content. The ledger records scope; it never expands it. Revalidate substitutions and compensations before writing.
- **Untrusted-head execution**: Classify head repository and author under trusted-base repository policy; default to untrusted when policy/evidence is missing. Read workflow rules and verification commands from the trusted base. Execute untrusted code only in a credential-free, host-isolated environment without default network access. Without isolation, perform static review and stop publication when a required executable check remains unverified; report the exact missing prerequisite rather than requesting an approval waiver.

## Publication Preflight

Complete collection and triage first. Before editing, creating a checkout, acquiring a lease or publishing, establish the prerequisites for the authorized operations only. Local-only work needs authoritative source identity, baseline, trust and verification, not write scopes, push destinations, trigger setup or mutation-visibility bounds. Skip prohibited operations; return the prepared local result after verification and any permitted local commit, before remote writes. An explicit no-commit limit also skips committing. Missing publication capability does not block an otherwise verifiable local-only result:



1. Revalidate the provider, host and exact PR/MR identity using the selected provider interface. Verify authentication and the capabilities actually needed for the authorized operations; do not require remote write capability for local-only work. Collection success does not prove write access. Use CLI authentication checks only when that CLI is the selected interface; missing write access blocks the write path, not a read-only report.
2. Record base/head repository stable IDs, canonical clone URLs, PR/MR number, title/body, base/head full refs, local HEAD, and authoritative remote head SHA. Only when push is authorized, bind the authenticated head-repository URL and full head ref as the push destination; never infer it from the local branch or remote name. Stop if ambiguous.
3. Record default autonomous execution against the authoritative identity. Freeze the original request, task operations, explicit user restrictions, exact PR/MR/repository/ref, `final SHA: pending`, and `blocker policy: stop-and-report` in the standing scope envelope. A missing or ambiguous target blocks mutations; a read-only or narrower request never inherits broader operations.
4. Start at the authoritative remote head. A detached checkout is valid with an explicit destination. If ahead, every commit/hunk must be attributable and authorized; otherwise use an isolated checkout at the remote head. Never publish from a behind or diverged base. Record pre-existing staged, unstaged, and untracked changes separately; when any exist, use an isolated worktree/index at the remote head or stop before editing. Do not unstage, overwrite, or commit baseline work. Record any required isolated-checkout preparation at preflight, but defer creating or changing a checkout until the Step 3 gate establishes pending work; a no-action result needs no checkout preparation.
5. Record head trust evidence, trusted verification instructions, and available execution isolation. Confirm the selected platform interface supports the authorized writes, pagination, direct full-ID thread retrieval and automation observation; unsupported required operations remain explicit gaps.
6. When an authorized publication or explicit review-observation task needs it, inspect trusted workflow configuration, integration metadata and available bot activity. Record whether a review workflow exists, its push event/actor/ref filters, supported non-comment triggers, and run/output identifiers. Distinguish review automation from ordinary CI. Unknown configuration is not evidence of no workflow; investigate or ask when it affects the required trigger. Record `wait_for_review` from the user's request and separate explicit command-comment permission, if any. Missing active-trigger support does not block read-only collection or a no-action exit. For no-code publication in a configured review workflow, determine a permitted trigger before the first remote write; if only command comments work, ask the user before publication.
7. Record observation-start time. Only when mutations are authorized, record finite bounds for mutation reconciliation and comment visibility. Only when `wait_for_review: true`, use the deadline and bounds established under review-waiting.md, preserved across re-entry. Enumerate accessible current runs and all available output to establish the baseline; an active run alone does not require waiting.
8. Classify observed runs as historical, active, or associated with the final SHA/publication using authoritative metadata. Reconcile available findings. Only with explicit waiting, mark applicable final-SHA review runs `must-pass`, track other related active runs for reconciliation, and require the requested terminal outcomes. Without waiting, report active or queued runs as pending rather than failed or passed.

## 4. Implement Fixes

Use the main coding workflow's implementation, language conventions and risk-based verification. Implement only accepted feedback and required caller updates, including accepted actions within Mixed items. Superseded actions cite current code and need no artificial change. Read trusted-base rules before executing checks; preserve the head-isolation requirements above.

Required checks and repository prepublication gates must pass. Proven unrelated baseline failures need scope evidence; unknown failures or unavailable required checks block publication. Approval is not a substitute for verification.

## 5. Mandatory Independent Review Gate

Load precommit-review.md and use its mandatory independent adversarial review loop for every code change. This module does not define another fix loop. Provide the complete accumulated change, feedback-derived requirements and intended commit payload. The parent fixes valid findings; each new round uses a fresh read-only subagent that checks for suitable specialist skills and preferably uses one, without requiring a fixed skill name. Require a clean complete result and passing required checks before code-work completion or local commit. Any code/payload change invalidates the result. Unavailable delegation or an unresolved issue affecting the changed contract blocks the commit. Store iteration records outside the repository.

Content-only replies/metadata do not trigger this code gate. This mandatory local gate is distinct from remote review results, which are awaited only when explicitly requested.

## 6. Commit and Bind Publication Scope

1. Refresh authoritative repository URL/ref/head; stop on unexpected mapping/SHA drift. Compare worktree and index against baseline and identify attributable paths/hunks. Never stage baseline work.
2. Inspect and report the final diff without waiting for confirmation. For code commits, require Step 5's clean complete subagent review bound to the actual intended index content; later code/payload drift restarts Step 5. Require task-attributable candidates and `commit` within the standing task scope; respect explicit no-commit restrictions. No task change means no new commit. Repository content/verification requirements still apply; default execution has no separate post-diff approval checkpoint.
3. Unless explicitly overridden, use English commit prose and a Conventional Commits subject (`type(scope): subject`, optional scope/`!`); documented repository format is an exception. Inspect subject/body/footers for concrete changes, rationale, behavior, compatibility, and relevant issue references only. Exclude execution reports and process/history metadata; describing changed test code is allowed, reporting its execution is not.
4. Stage only task-attributable hunks, inspect the entire cached diff, and commit locally. Use an isolated index/worktree or stop if baseline staged entries appear. Confirm remaining work matches the recorded baseline.
5. Capture the final SHA and inspect every commit plus the complete `remote_head..final_sha` diff. Prove all commits/hunks attributable. Bind the autonomous envelope to that SHA only after revalidating PR/MR/repository/ref/scope. On same-scope re-entry requiring new fixes, invalidate the prior SHA binding, restore pending, and repeat attribution before rebinding; this alone needs no renewed authorization. Identity/ref/scope mismatch invalidates authority and stops execution.
6. The internal `no-new-code` mode means no commits await publication; it is not a user no-push or local-only restriction and grants no remote authority. Re-evaluate the Step 3 no-action gate before selecting a publication mode. For pending review work, select `publication mode: push` when new attributable commits await publication; otherwise require local HEAD = authoritative remote head and select `no-new-code`. Never publish unattributed ahead commits or create an empty commit. In no-new-code mode plan an active trigger only when the repository has a configured review workflow.
7. Bind the exact final-SHA/source-URL/full-ref push tuple to the standing scope envelope, without a separate push prompt. Respect no-push/local-only limits and stop with the prepared state when they prevent completion. Record the exact order: replies → transitions → metadata → push. No-new-code mode has no push refspec; bind its manual-review mutation to the same task scope without a separate prompt.

## 7. Reply, Transition Threads, and Synchronize Metadata ⛔ BLOCKING

1. Repeat complete Step 2 collection and direct processed-thread fetches. Compare IDs/fingerprints bidirectionally. New/edited/deleted external items return to triage; preserve removals as history. Missing/changed workflow effects require reconciliation, not silent recreation. Refresh exact repository/ref/head/title/body and freeze `expected_old_sha`; stop on unexpected drift.
2. Load pr-rules.md and draft any necessary title/body update from the final diff/history and repository templates. Apply its language, semantic-title, base-preservation and change-only content rules. Report unresolved mandatory-template conflicts before publication. This review-derived update uses the standing review scope, not a separate drafting confirmation gate.
3. Freeze final SHA, exact replies/markers, per-thread transitions/inverses, current and desired metadata, operation order, authorization ledger, and guards. Identify metadata dependent on the pending SHA. Acquire an authorized eligible lease if available; otherwise use optimistic guards. Validate the complete plan before writing.
4. Publish and authoritatively verify every required reply using the procedure below. Then execute and verify all planned Resolve/Reopen transitions serially. After those succeed, update title/body only as needed and verify exact values. All of these operations precede push or active review triggering.

### Reply Procedure

Every workflow reply is the exact human-readable reply, one LF, then a final marker line:

```text
coding-workflow:v1 {"platform":"github","item_kind":"review-thread-comment","item_id":"<full-id>","body_sha256":"sha256:<source-hash>","disposition":"Implement","final_sha":"<full-sha>","supersedes_reply_id":null}
```

Use canonical provider/kind/ID, current source fingerprint, aggregate disposition, and final SHA. For compensation, name the prior full reply ID. An eligible reused ancestor reply retains its original marker SHA; record the current workflow SHA separately.

Before each reply refresh the exact source and complete target replies. Return to triage if source changed/missing. Reuse one exact authenticated-writer reply/marker covering the current or prepared SHA. Reuse an ancestor marker only when the intervening diff/current code prove disposition and text remain accurate. If intended text/disposition changed, edit when supported and authorized; otherwise create one authorized compensating reply with an acyclic single-terminal chain. Stop on forks/cycles/ambiguous chains.

Post once, then re-fetch complete replies and match exact author/body/marker. Reuse one match. Multiple matches block further reply creation/editing. Reconcile exact retain/delete IDs and delete only proven authenticated-writer, workflow-owned byte-identical duplicates within the standing scope, without a separate confirmation. Refresh each target before deletion and verify the unique retained reply afterward; stop on uncertain ownership or differing content. After ambiguity reconcile through the visibility bound; with zero matches and unchanged preconditions permit at most one identical non-triggering/provider-idempotent retry, then reconcile again.

Reply content:

- Implement: state each result and relevant Superseded evidence. Before push describe the final local SHA as the prepared fix, not as already remote; use wording still true after publication. Do not post/edit solely to announce the later push.
- Superseded: cite current code/intervening diff and state no new change was needed.
- Skip: give the technical reason. Mixed: include all applicable results/evidence/reasons in one reply.
- Context: reply only when a status response is required, with the same marker/replay rules. Clarify cannot reach publication.

Record authoritative reply IDs and upsert each as workflow-emitted Context linked to its source. Treat manual command comments separately; exact command syntax may require `marker: N/A`.

### Pre-Push Thread Transitions

Keep the ledger's computed desired states; “resolve feedback” does not override an unaccepted Skip. For each non-No-op transition:

1. Refresh remote head, exact thread/source, and applicable guards; require `expected_old_sha` in push mode or final SHA in no-new-code mode. The prepared local fix may not be remote yet. Verify all required replies are authoritative and exact mutation authorization still holds.
2. Use a provider conditional operation where available; otherwise exact refresh → one mutation → authoritative result/direct full-ID re-fetch. GitHub uses `resolveReviewThread` / `unresolveReviewThread`; GitLab updates the full discussion ID with `resolved=true` / `false`.
3. Verify desired state from the full thread. Process serially, recording success before the next transition. HTTP success alone is insufficient. An unchanged state after a definitive retryable failure permits one bounded retry under replay safety, then verify again; ambiguous state blocks progress.
4. Record every success/failure/cancellation and permitted inverse. After an abort, cancel unattempted transitions. Restore successful transitions in reverse order only with exact inverse authority, unchanged guards, and retained lease ownership where applicable; otherwise reconcile and report partial state. Never push or trigger review with an incomplete required transition sequence.

### Metadata and Publication Gate

After all replies/transitions succeed, refresh exact title/body and guards, apply only necessary authorized changes, and verify them. Re-fetch complete review context, thread states, metadata, and repository/ref/head. Require a bidirectional ledger match including workflow-emitted replies. External drift returns to triage; workflow-effect/metadata drift requires reconciliation and replanning. Freeze this as the final pre-trigger linearization snapshot. Without an atomic revision or a lease covering every context writer, disclose that later external feedback cannot be atomically excluded.

Before leaving Step 7, require all replies, transitions, and metadata authoritative. The last review-triggering operation remains unsent. If publication later fails or aborts, do not claim the local fixes are remote. Restore pending-SHA-dependent metadata or thread states only through authorized inverse rows and unchanged exact guards; verify compensation and report anything left prepared, partial, or unknown. Never erase truthful prepared-fix replies solely because a push failed. Lost lease ownership permits reconciliation reads, not compensation writes.

## 8. Push New Commits or Actively Trigger Review

Revalidate exact repository/ref, expected remote head, replies, thread states, metadata, operation authority and the latest complete context snapshot. Verify retained lease ownership/lifetime, or renew through an authorized row before repeating freshness checks. Stop/replan on drift. Do no unrelated work between freshness checks and dispatch.

### Push Mode

Push the exact `<final_sha>:<full_head_ref>` tuple to the authoritative source URL using a conditional lease bound to `expected_old_sha`. Never infer the source from current HEAD or destination from a local branch name; never fall back to unconditional force push. Rewriting history additionally requires repository-policy support and ownership of every rewritten commit.

After success or ambiguity, read the authoritative remote head. The final SHA proves the code reached the target. If the exact old SHA remains and no retry occurred, permit one identical leased retry and read back again. Other states or a failed retry block publication completion; reconcile prepared replies/transitions/metadata and perform only authorized guarded compensation. Never represent unpushed fixes as remote.

Record whether the verified push matches the configured review trigger. Capture any immediately available dispatch/run ID without waiting for delayed visibility or a result. Do not send a redundant active trigger because the automatic run is not yet visible. If an observed filter excludes the push, report that review was not triggered; do not silently substitute a command comment or an unrelated workflow.

### No-New-Code Mode

Send no push. Verify local and remote heads equal the final SHA, with authoritative replies/transitions/metadata. If no review workflow is configured, record `review_trigger: not_applicable`. If configuration is unknown and affects the next action, investigate or ask rather than infer absence.

If a review workflow exists, actively trigger it through its supported non-comment API, rerun, reviewer request or dispatch action only when that mechanism actually invokes the configured review process. An ordinary CI rerun is not a review trigger. Do not treat unchanged-head pushes or ordinary replies as triggers. An already accepted exact request for this publication may be reused; an old successful run cannot substitute for a new required request.

Before dispatch, inspect currently available related runs and outputs, and revalidate the target SHA and context. Do not wait for active runs to finish unless explicitly requested. If documented coalescing already covers this exact request, reconcile and reuse it instead of duplicating dispatch.

### Active-Trigger Procedure

Bind one exact trigger operation to the task scope and final SHA. Command comments need a separate explicit user request to publish them; general review-handling authority and repository documentation are insufficient. If the only supported mechanism is a command comment without that request, ask and leave the trigger pending. Do not emit `/review` or equivalent command text in replies, metadata or bot mentions as a workaround.

Dispatch once and verify authoritative acceptance/request ID or the provider's definitive success response. Report acceptance separately from run completion. For an explicitly requested command comment, preserve exact syntax, record `marker: N/A` when required, and read back its canonical comment ID/body; command publication alone does not prove a review run completed.

On ambiguity, reconcile available request/run IDs and workflow effects through the bounded mutation-visibility window. Reuse one uniquely matched effect; multiple matches block further writes. Retry at most once only with the same provider idempotency key or documented coalescing guarantee. Otherwise report unknown trigger status without another dispatch. Waiting for a mutation's receipt is distinct from waiting for review results.

## 9. Verify Publication and Optional Review Results

### Default: Verify and Return Without Waiting

1. Read back the exact remote repository/ref/head, required metadata, all reply effects and processed thread states. Require the intended final SHA and authoritative IDs/results. Refresh currently available complete review context; return new actionable feedback already observed to triage. Preserve deleted/edited history and reconcile drift rather than overwriting it.
2. In push mode, verify remote SHA and report whether repository configuration predicts automatic review and whether a dispatch is already visible. In configured no-code mode, require accepted active-trigger evidence; if permission/support is missing, report `publication verified; review trigger pending` with the concrete missing action. A request being accepted is not a passing review.
3. Do not poll for queued/running reviews to finish, wait for future bot output, require stable queues or a terminal review conclusion, or keep iterating to absorb future feedback. Report the current snapshot and its observation limits. Required local checks and already observed actionable feedback remain binding.
4. Release and verify any owned lease after reconciling outstanding mutations. Record `N/A` when no lease existed. Lost ownership permits reads, not compensation writes; report an unknown release result accurately.

Publication completion requires complete pagination of currently available feedback, one decision per current item, passing required prepublication checks, authoritative mutation readbacks, task attribution, the original publication order, and remote state matching the ledger. With a configured no-code review workflow it additionally requires accepted active-trigger evidence, not a terminal result. No-action follows Step 3 and has no publication or trigger requirement. Clearly distinguish publication, trigger acceptance and review outcome.


With an explicit request to wait for remote review results, continue under review-waiting.md using its original deadline. Otherwise the verified publication result is the end of this path.
