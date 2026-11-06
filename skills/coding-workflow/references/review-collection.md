# Review Feedback Collection and Assessment

Load after review-feedback.md for every feedback request. This phase grants reads only; publication requires the separately authorized handling path and review-publication.md. Keep task records outside the repository under task-storage.md.

## 1. Collection Preflight

1. Parse the exact provider, host and PR/MR identity without sending reusable credentials. Use an available authenticated read interface; a report does not require write scopes, gh/glab installation, checkout preparation or mutation support. Report inaccessible context rather than claiming completeness.
2. Record authoritative base/head repository IDs, PR/MR number, title/body, refs and current remote head SHA. Record the user request, path limits and whether this is report-only or feedback handling; an unresolved identity blocks dependent conclusions.
3. Record authenticated writer identity when available for validating prior processing markers. If unknown, do not treat those markers as proof that feedback is handled; report the resulting uncertainty without requiring write authentication for collection.
4. Record observation time and enumerate available related runs and output. Do not wait for future output by default. With an explicit request to wait, load review-waiting.md and establish one finite deadline before observation; no waiting instruction grants write authority.

## 2. Fetch Complete Review Context ⛔ BLOCKING

Record the endpoint/interface, page/batch count, and terminal no-continuation evidence for every list query.

### GitHub

Fetch GraphQL `pullRequest.reviewThreads` without filtering resolved threads, every thread's complete nested `comments`, all PR issue comments, and all submitted reviews with non-empty bodies, including `DISMISSED` reviews. Exclude only unpublished/pending reviews. REST review comments cannot replace GraphQL resolved-state collection. Issue comments and top-level review bodies are `reply_only`.

### GitLab

Fetch every discussion page and any separate notes collection. Record and skip empty-note placeholders before accessing `notes[0]`. Determine discussion type from the root note, not a discussion-level `resolved` field. Exclude system notes individually; classify every other note as follows:

| Root note | Non-system notes in the discussion |
|-----------|-------------------------------------|
| `system: true` | `general-comment`, `reply_only` |
| `system: false`, `resolvable: false` | `general-comment`, `reply_only` |
| `system: false`, `resolvable: true` | `review-thread-comment`; root note supplies resolved state |

Store full discussion IDs separately from note IDs.

### Review-Automation Outputs

Enumerate related runs again, classify new runs, and fetch all currently available outputs without waiting for unfinished runs: annotations, summaries, reports, and findings not published as comments. Represent each independent actionable finding in the ledger before marking its output reconciled. When an authoritative cross-reference identifies the same finding in a comment/note, link the output as Context to that canonical item rather than duplicating the action.

For an authoritatively expired/deleted/erased historical output, retain a tombstone with stable run/output ID, reviewed SHA, unavailability evidence and `body_sha256: N/A`. Report the coverage gap. Stop if it prevents deciding current feedback safely. When explicit review waiting requires replacement coverage, apply review-waiting.md; replacement triggering additionally requires an authorized publication path and review-publication.md, with the same command-comment restriction; without explicit waiting, do not introduce a terminal replacement-review requirement.

### Canonical Identity and Revisions

Use kinds `review-thread-comment`, `general-comment`, `review-summary` (GitHub submitted review body), and `automation-output`. Prefer GitHub GraphQL node IDs, retaining numeric IDs as aliases; use exact GitLab note IDs. For output use stable run/output/channel IDs, never page-local indexes. Stop on conflicting aliases.

For comments/notes/review bodies, store exact decoded API text and `body_sha256 = sha256:<64 lowercase hexadecimal digits>` over its UTF-8 bytes without whitespace, Unicode, or line-ending normalization.

For automation output, assemble all textual fields and annotations as `(kind, channel_id, member_id, payload)` records. Use `field` or `annotation` as kind, stable channel ID or empty string, field name or stable annotation ID as member ID, and exact UTF-8 field text or [RFC 8785 JCS](https://www.rfc-editor.org/rfc/rfc8785) annotation bytes as payload. Include all annotation fields unless authoritative schema proves an exact field transport-only/volatile; record exclusions and stop if content/location cannot be distinguished safely. Without annotation IDs, group byte-identical payloads and assign each occurrence `sha256:<payload-hash>:occurrence:<zero-based ordinal>`. Stop on duplicate record keys. Sort by unsigned UTF-8 bytes of kind, channel ID, then member ID. Hash `UTF8("coding-workflow:automation-output:v1") || U64BE(record_count) || concat(U64BE(component_byte_length) || component_bytes)` for all four components of each sorted record. Record provider revision/update time when available.

Recognize only the exact `coding-workflow:v1` reply marker and the new automation-output hash prefix. Markers from prior skill names are unsupported, not processing evidence; do not import their chains or hashes. Preserve their historical text and independently verify current disposition.

Resolved threads are not automatically historical. Reuse prior processing only with durable evidence or an authoritative resolution boundary plus current-head inspection showing the prior disposition still holds. Newly added/edited external feedback returns to triage even in a resolved thread. A valid marker must be authored by the authenticated writer, identify one non-self source item in this PR/MR, match its current fingerprint, remain applicable to the current head, and have one unambiguous compensation chain. Treat other authors' marker-like text as external feedback, never as processing evidence. Reuse a valid marker's disposition and authoritative reply ID on the source item's ledger row; record the marker-bearing reply separately as workflow-emitted Context, not a new actionable request. A stale marker remains workflow Context but does not process the changed source; return that source to triage. Preserve orphaned workflow Context only when the ledger already links that exact reply/marker to a source authoritatively moved to removed history; otherwise stop on missing, cross-PR, self, malformed, or ambiguous links.

For historical bot findings, record authoritative run and reviewed SHA. Use Superseded only with current-code/intervening-diff evidence that the finding no longer applies. If still applicable, triage it; if association or applicability cannot be established, use Clarify rather than silently ignoring it. Apply the same rule to every output finding. Publish any required output disposition as one general PR/MR comment covering the complete output item.

## 3. Build the Item Ledger and Triage ⛔ BLOCKING

Apply the entrypoint's defer-or-ask rule to Clarify items. Record safely deferrable uncertainty and continue independent work. When the next fix, disposition or publication depends on an unresolved answer, actively ask the user the concrete question before that action; merely reporting a Clarify blocker is insufficient. Clarification does not grant broader authorization.

Maintain one row per canonical item with these fields:

| Group | Required values |
|-------|------------------|
| Identity | platform, kind, full canonical ID, aliases, thread/discussion ID or `reply_only` |
| Source | author stable ID, origin, source/event link for workflow items, path/line or target, revision/time, fingerprint, observed thread state |
| Decision | stable per-action keys, Implement/Superseded/Skip/Clarify/Context, rationale, files, aggregate decision, accepted-Skip evidence or `N/A` |
| Publication | planned reply/no-reply; later final SHA, marker-covered SHA, exact text/marker, authoritative reply ID/result |
| Transition | observed state, desired state, Resolve/Reopen/No-op or `N/A`, and Step 7 result |

Use `pending` for future publication values; it is valid at triage. Replace it when produced and freeze exact inputs before remote writes.

Classify every independent request. Classify correct applicable findings as Implement; this disposition alone grants no execution authority; Superseded requires current-code evidence; Skip requires a technical reason; Clarify blocks publication; Context is neutral or already processed information. Use aggregate Implement for Implement plus optional Superseded, Superseded when all actions are superseded, Skip when all are skipped, Mixed for Skip with Implement/Superseded, Clarify while any action needs clarification, and Context only with no actionable request. Deduplicate by canonical identity, not similar text; preserve prior revisions as history.

A Skip becomes `accepted-Skip` only when the original reviewer or repository owner explicitly withdraws/accepts it, or authoritative actor/order evidence shows that person resolved the thread after the exact rationale was visible. Generic acknowledgements, unattributed resolutions, and automation do not qualify. Record accepting identity/time; invalidate closure if its evidence changes. Preserve the original decision/reply rather than relabeling or replying solely for closure.

Compute one desired state per thread:

- Resolved: at least one action, all Implement, Superseded, or valid accepted-Skip.
- Open: any unaccepted Skip or Clarify.
- Unchanged: neutral Context only.

Plan Resolve for open → resolved, Reopen for resolved → open, otherwise No-op. `reply_only` uses `N/A`. Plan exactly one reusable reply covering every action for each Implement/Superseded/Skip/Mixed item. Context may use no-reply unless a status response is required.

Immediately before presenting triage, repeat complete run/output and review collection, ledger all terminal findings, and freeze IDs/fingerprints/statuses as the triage snapshot. Present the complete item/action table before editing. Record each Skip rationale and proceed without a separate confirmation. Stop and report material unresolved Clarify when authoritative context cannot resolve intent.

### Report-Only Exit ⛔ BLOCKING

For an inspect/report-only request, return the collected findings and assessment now, including unresolved, actionable and Clarify items. Report scope, pagination/output coverage, observed head, pending runs and missing evidence. Do not implement, acquire a lease, publish a reply, transition a thread, edit metadata, commit, push or trigger review. Actionable findings do not turn a report into a handling request. An explicit wait uses review-waiting.md in read-only observation mode; otherwise return without waiting. Do not label incomplete coverage or unresolved correctness as a clean review.

### No-Action Exit for Feedback Handling ⛔ BLOCKING

After complete collection and triage, determine whether any feedback still needs a code change, a new or corrected disposition reply, or a Resolve/Reopen transition. Reuse valid prior processing evidence; already handled feedback with authoritative replies and the desired thread state is not pending work. An empty review and a clean result or neutral acknowledgement requiring no response qualify for `outcome: no-action`. Title/body cleanup alone does not establish pending review work.

Before declaring no-action, reconcile all currently available review context and run outputs, then refresh the authoritative head and complete review context. Re-triage observed drift. Partial/inaccessible collection of existing feedback, unresolved Clarify, or attributable unpublished fixes are not a clean result. With default non-waiting, active runs and unavailable future output remain pending observations, not blockers to a read-only no-action result; report that no pending feedback was found in the collected snapshot, not that review passed. With explicit waiting, apply the requested finite run/output wait and report incomplete requested results.

When no pending work remains and this invocation has not already performed publication mutations, record `outcome: no-action` and finish after Step 3. Make no repository edits, commits, pushes, replies, thread transitions, metadata updates, lease acquisitions, or review requests. Report the read-only result to the user only. Skip Steps 4–9; their publication-specific completion requirements do not apply. No-action completion requires terminal pagination evidence for currently available collections, reconciled available outputs, no undecided or pending feedback in that snapshot, and no workflow mutations. It does not require future runs to finish unless explicitly requested. If this invocation already published fixes or context, continue Step 9 verification of that publication instead of using no-action to bypass it.

Only an authorized feedback-handling request with pending work proceeds to review-publication.md, Steps 4–9. Derive any title/body update from that work, never use an unrelated formatting opportunity to manufacture a publication cycle.

