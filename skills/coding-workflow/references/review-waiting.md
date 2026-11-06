# Explicit Review-Result Waiting

Load only when the user explicitly requests waiting for review results. Read review-collection.md for complete collection rules. A report-only request remains read-only; this file never supplies permission to publish, retrigger, fix code or post command comments. For an authorized handling task, review-publication.md still governs all writes and their order.

## Deadline and Observation

Use one finite deadline recorded at preflight; new findings or runs never reset it. Explain unresolved material requirements rather than guessing a wait budget when the host/repository provides none.

- Enumerate applicable runs and complete currently available outputs, binding results to the authoritative requested head and review scope; handling tasks additionally bind to their exact publication/final SHA. Track applicable final-SHA runs as must-pass; reconcile other related observed runs and findings.
- Wait within that deadline for the requested review outcomes; require acceptable terminal conclusions only for the requested scope. A historical same-SHA result or ignored trigger does not substitute for this publication's review unless authoritative coalescing links the exact accepted request to equivalent coverage.
- Return new actionable findings to triage; report-only observation returns them as findings and performs no fixes or publication. Further authorized handling follows the same replies → transitions → metadata → push/active-trigger order and scope checks. Neutral acknowledgements do not create another cycle.
- Refresh final head, metadata, replies and processed threads before reporting. Preserve pending, unavailable, failed, cancelled and ambiguous results as distinct states; report incomplete waiting at the deadline rather than claiming review passed.
- Release any retained lease on completion or early stop. Explicit waiting never grants permission to post command comments.

### Replacement Coverage When Waiting Was Requested

Only with explicit review waiting, reconcile historical-output tombstones that affect the requested coverage. Reuse an applicable push-triggered run. If a distinct replacement request is necessary, first require explicit trigger authority for a report-only task or the authorized handling path. Verify scope, invoke review-publication.md's active-trigger procedure, and preserve its command-comment restriction. Missing permitted mechanisms or ambiguous coverage remain gaps; do not force push or create an empty commit to obtain a review.

