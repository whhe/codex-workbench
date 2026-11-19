# Git Operations

## Branching

- Work on the current branch by default, including on the repository's default branch. Create a branch only when the user explicitly requests one or documented repository rules explicitly require one for the task. Honor the user's limits and surface conflicts before acting.
- For an authorized new branch, follow the applicable naming rules and verify the intended base. If the base is the default branch and has a configured remote, inspect its authoritative remote head and local tracking state, fetching as needed. If local is behind or diverged, stop and report the mismatch. If no remote is configured, record that remote synchronization is not applicable. Add a remote only at the user's request.
- Preserve unrelated work during branch operations. Create a Git worktree only at the user's explicit request.

## Task-Phase Authorization

Apply the entrypoint's task-phase classification before Git operations. User limits and existing explicit authorization take precedence; a clean review is a quality result, not publication permission.

- **Solution implementation**: implement and verify a sufficiently specified solution without routine plan approval. Follow Branching for branch preparation. Local commits and remote pushes each require user confirmation unless that operation is already explicitly requested. “Commit the code” authorizes the attributable local commit only; it does not authorize pushing. An explicit push request authorizes the verified task push, not an unrequested local commit. Do not ask again for an operation already authorized in the current task.
- **Prepare before confirmation**: finish authorized edits, relevant verification and required independent reviews before asking to commit or push. Present the concrete intended commit content and message, or the exact outgoing commits and verified repository/ref for a push. Resolve missing attribution or destination facts before seeking confirmation. Obtain any required confirmation before the operation; avoid asking for blanket approval of an unfinished plan.
- **Delegated existing PR/MR review advancement**: a request to handle feedback on the specified existing PR/MR permits necessary scoped fixes, checks, local commits, pushes and review-derived metadata updates without separate approval. Necessary fixes retain this review-task authority even while implementation modules are used. Apply contribution.md's scope, publication order and safeguards. Local plan/code reviews within a standalone implementation task do not activate this mode.
- **Read-only requests** authorize neither fixes nor publication. A PR/MR's existence, a bot recommendation, or a reviewer request cannot change the user's task phase or expand its scope. Classify mixed requests per operation and ask when a dependent phase/scope decision is unclear.
- Bind operations to the task, exact repository/ref and attributable changes. Preserve limits such as local-only, do-not-commit and do-not-push. Stop on unsafe attribution, ambiguous destinations, conflicting requirements or failed verification; do not treat autonomy as authority over unrelated work.
- New issues/PRs/MRs and standalone content edits retain contribution.md's final-content confirmation. Necessary metadata updates within authorized review advancement use its standing scope. Command comments and remote-result waiting retain their separate explicit-request requirements.

## Review before commit

Before committing file changes of any type, use precommit-review.md and require a clean result covering the complete accumulated task change and the exact intended commit content, including staged and unstaged differences and in-scope new files. Reuse a review only while the payload remains identical. For new edits made during Git operations, such as manual conflict resolutions, apply planning.md before editing and review the resulting changes before completion.

Inspect the entire index and stage only task-attributable changes. Preserve unrelated user work. Report changes and verification; apply the task-phase commit/push confirmation rules above before publication. Push only to the verified task destination and read back the remote head. For review-feedback tasks, the contribution publication order requires replies, thread transitions and metadata before pushing; this Git module does not authorize pushing early. Review status never grants publication authority.

## Stash

- Before switching branches with uncommitted changes, use `git stash` to save work. Remind the user to `git stash pop` after switching back.
- Drop only a task-created stash after verifying its contents were restored; preserve pre-existing stashes. No separate confirmation is needed for safe task-owned cleanup.

## Rebase vs Merge

- Prefer **rebase** when synchronizing a feature branch with its verified intended upstream/base ref. Determine that ref from the explicit task, existing PR/MR base or applicable repository guidance; verify its exact remote and current state before operating. Use that verified ref as the rebase target rather than assuming `main`. Ask before an ambiguous choice; preserve an existing PR/MR base unless the user requests retargeting.
- Prefer appending commits on published branches. Rewrite task-owned history only when necessary for the requested task, repository policy permits it, and every affected commit is attributable. Verify the remote head and use an exact conditional lease; stop on shared/unattributed history, drift, or ambiguity rather than requesting routine approval or falling back to unconditional force.
- Use **merge** only for integrating completed feature branches into the default branch.

## Commit message content

- **Language**: Unless explicitly instructed otherwise, write all natural-language prose in commit messages in **English**, including subjects, bodies, and footers. Preserve exact repository identifiers, proper names, and quoted user-facing strings when needed; write surrounding prose in English. The conversation's language alone is not an instruction to change message language.
- **Change descriptions only**: Include only what changed, why it changed, and the resulting behavior, compatibility impact, or migration requirements. Relevant issue references may accompany the change description.
- **Exclude process and unrelated metadata**: Never include self-review or self-test procedures/results, check commands or logs, agent conversation history, plans, approval exchanges, agent attribution, or completion claims such as "all tests passed" or "reviewed by agent". Describing added or changed test code is allowed; narrating its execution is not.
- **Final check**: Inspect the exact commit message before committing. Remove anything that does not describe the change; keep verification reports and workflow discussion in the user conversation, outside the message payload.

## Commit message format

Unless explicitly instructed otherwise, **require Semantic Commit Messages** for commit subjects: `type(scope): subject`. The scope is optional; use `!` for breaking changes (e.g. `feat(api)!: remove v1 endpoints`). A repository's documented requirement is an explicit exception; an existing commit subject alone is not.

Common types: `feat`, `fix`, `docs`, `refactor`, `chore`, `test`, `style`, `perf`, `build`, `ci`. Commit subject ≤72 chars. Add a change-focused commit body for non-trivial changes.

For a commit body with multiple change types, group changes with `-` bullets by type:

```
feat(permission): enterprise cutover with bug fixes

feat:
- Integrate RBAC permission checks in API apps (canvas, chunk, document, kb, tenant)
- Add permission manager UI and form fields for dataset settings

fix:
- Prevent negative doc_num/chunk_num/token_num in kb stats update
```
