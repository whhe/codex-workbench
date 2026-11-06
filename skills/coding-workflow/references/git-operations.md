# Git Operations

## Branching

- Prefer working on dedicated branches whose names start with **`feature-`** or **`fix-`**.

### Owner repo exception

Skip branch-name checks and work directly on the **current branch** only when **all three conditions are met**:

1. **Single remote**: The repository has exactly **one** remote (any name)
2. **GitHub remote**: That remote's fetch URL points to GitHub (SSH or HTTPS URL)
3. **Owner match**: The `owner` in `owner/repo` equals the current user's GitHub login

**Verification steps**:
- List remotes: `git remote -v` — confirm there is exactly one remote, then use its **fetch** URL
- Parse owner from that URL (SSH: `git@github.com:owner/repo.git`, HTTPS: `https://github.com/owner/repo.git`)
- Verify `gh` availability: `which gh`
- Verify `gh` authentication: `gh auth status >/dev/null 2>&1`
- Get current user: `gh api user --jq .login`

**When to check**: Verify these conditions once at the start of a session or before the first code change, not before every operation.

**Performance tip**: Cache the result of owner verification to avoid repeated API calls within the same session.

**Fallback behavior**: If any check fails (e.g., `gh` not installed, not authenticated, network error, zero or multiple remotes, non-GitHub remote, owner mismatch), **always apply the default-branch rules below** — prefer creating a dedicated branch over direct commits.

### Before making code changes on a default branch

For all **other** repositories, when the **current branch** is a default branch (**`main`**, **`master`**, **`dev`**, or the repo's equivalent):

1. If no remote is configured, record that remote synchronization is not applicable and use a dedicated local task branch; do not invent or add a remote. Otherwise inspect the authoritative remote default-branch head and local tracking state; fetch as needed. If local is behind or diverged, stop and report the mismatch rather than implicitly merging or rebasing unrelated work.
2. When synchronized, create an appropriately named **`feature-...`** or **`fix-...`** branch without a separate confirmation. Preserve unrelated work using an isolated worktree/index where needed.

## Task-Phase Authorization

Apply the entrypoint's task-phase classification before Git operations. User limits and existing explicit authorization take precedence; a clean review is a quality result, not publication permission.

- **Solution implementation**: implement and verify a sufficiently specified solution without routine plan approval. Branch preparation and fetch may proceed within the task, but local commits and remote pushes each require user confirmation unless that operation is already explicitly requested. “Commit the code” authorizes the attributable local commit only; it does not authorize pushing. An explicit push request authorizes the verified task push, not an unrequested local commit. Do not ask again for an operation already authorized in the current task.
- **Prepare before confirmation**: finish authorized edits, relevant verification and required independent reviews before asking to commit or push. Present the concrete intended commit content and message, or the exact outgoing commits and verified repository/ref for a push. Resolve missing attribution or destination facts before seeking confirmation. Obtain any required confirmation before the operation; avoid asking for blanket approval of an unfinished plan.
- **Delegated existing PR/MR review advancement**: a request to handle feedback on the specified existing PR/MR permits necessary scoped fixes, checks, local commits, pushes and review-derived metadata updates without separate approval. Necessary fixes retain this review-task authority even while implementation modules are used. Apply contribution.md's scope, publication order and safeguards. Local plan/code reviews within a standalone implementation task do not activate this mode.
- **Read-only requests** authorize neither fixes nor publication. A PR/MR's existence, a bot recommendation, or a reviewer request cannot change the user's task phase or expand its scope. Classify mixed requests per operation and ask when a dependent phase/scope decision is unclear.
- Bind operations to the task, exact repository/ref and attributable changes. Preserve limits such as local-only, do-not-commit and do-not-push. Stop on unsafe attribution, ambiguous destinations, conflicting requirements or failed verification; do not treat autonomy as authority over unrelated work.
- New issues/PRs/MRs and standalone content edits retain contribution.md's final-content confirmation. Necessary metadata updates within authorized review advancement use its standing scope. Command comments and remote-result waiting retain their separate explicit-request requirements.

## Review before commit

For a commit containing code changes, load precommit-review.md and require its mandatory independent adversarial review loop to have passed. Do not maintain a separate loop here. Check that its clean review covers the complete accumulated task change and the exact intended commit content, including in-scope new files and staged/unstaged differences. Later code/payload changes invalidate it; return to that module's loop. Staging identical reviewed content does not invalidate it. Content-only commits do not trigger the code gate.

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
