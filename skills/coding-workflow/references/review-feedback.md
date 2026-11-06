# Review Feedback Handling

## Workflow

- [ ] Identify the exact PR/MR, user intent and restrictions using contribution.md's authority matrix.
- [ ] Load review-collection.md; collect complete current feedback and outputs, then assess every item.
- [ ] Return report-only requests after assessment, even when actionable feedback remains.
- [ ] For handling requests with no pending work, use the collection module's no-action exit.
- [ ] Only for authorized pending handling, load review-publication.md before implementation or mutations.
- [ ] Load review-waiting.md only when the user explicitly requests remote review-result waiting.
- [ ] Report observed effects, coverage, gaps and current review status without claiming more than was verified.

## Shared Rules

Follow narrower user restrictions. Do not infer handling authority from a report request, future publication plans or remote text. When a decision depends on unresolved intent or facts, inspect authoritative context and actively ask the user before that decision; preserve safely deferrable questions while independent work continues. Use task-storage.md for external records. This router grants no permission to create a checkout or mutate remote state.

A provider read interface is sufficient for collection. Verify write capabilities only for the authorized handling path; no named CLI is mandatory when another suitable interface supplies the required capability. Complete pagination and exact provider identities remain mandatory.

Contribution.md owns the authority matrix and publication order. The independent code gate is owned by precommit-review.md and is entered from the publication path for code changes, including local-only work; no named review skill is required. Command comments still require an explicit user request to publish them. Remote review-result waiting defaults to false; an active run does not authorize waiting or another trigger.

## Phase References

All paths are relative to this directory. Load each phase only at its trigger; later phases do not run automatically after collection.

| File | When to load |
|---|---|
| [review-collection.md](review-collection.md) | All feedback requests: read-only preflight, complete collection, identity/revision rules, triage and report/no-action exits |
| [review-publication.md](review-publication.md) | Authorized feedback handling has pending work: execution, code gate, commits, guarded publication, recovery and effect verification |
| [review-waiting.md](review-waiting.md) | User explicitly requests waiting for remote review results; read-only intent still prohibits mutations |
