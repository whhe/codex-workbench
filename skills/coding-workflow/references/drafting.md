# Issue and PR/MR Drafting

This path handles new issues/PRs/MRs and standalone title/body updates. Use available provider tools; load only the applicable content references listed below. Required metadata updates arising from review-feedback handling use the review path's authorization, not this path's confirmation gate.

**Scope boundary:** The English and semantic-format requirements apply to PR/MR titles and bodies. If the same task also creates commits, evaluate commit messages under the repository's commit-message policy separately.

## Workflow

| Marker | Meaning |
|--------|---------|
| `⚠️ REQUIRED` | Must not be skipped |
| `⛔ BLOCKING` | Prerequisite — blocks all subsequent steps |

- [ ] Step 1: Preflight ⚠️ REQUIRED
- [ ] Step 2: Task-Specific Context Gathering ⚠️ REQUIRED
- [ ] Step 3: Draft Content ⚠️ REQUIRED
- [ ] Step 4: Confirmation Gate ⛔ BLOCKING
- [ ] Step 5: Execute & Report ⚠️ REQUIRED

### 1. Preflight ⚠️ REQUIRED

Identify in this order:

1. **Upstream project** — resolve the provider, host, and project path. Accept GitHub `owner/repo` and GitLab `group/subgroup/project` paths, or derive the equivalent from an explicit issue/PR/MR URL. Otherwise load [preflight-upstream.md](preflight-upstream.md) for the full resolution algorithm.
2. **Task type** — classify: Create issue / Update issue / Create PR / Update PR / Create MR / Update MR.
3. **Templates** — detect upstream templates:
   - Issue: `.github/ISSUE_TEMPLATE/*.md|*.yml`, `.github/ISSUE_TEMPLATE.md`, or repo issue-form config
   - GitLab issue: `.gitlab/issue_templates/*.md` or the repository's documented issue-template location
   - PR: `.github/PULL_REQUEST_TEMPLATE.md`, `.github/PULL_REQUEST_TEMPLATE/*.md`, or `docs/PULL_REQUEST_TEMPLATE.md`
   - MR: `.gitlab/merge_request_templates/*.md` or the repository's documented merge-request template location

### 2. Task-Specific Context Gathering ⚠️ REQUIRED

For PR/MR tasks, load [pr-rules.md](pr-rules.md) before collecting commits or diffs. Resolve and verify the base using its **Base branch selection** rules first; for an existing PR/MR, read its current base from platform metadata.

- **Create issue**: keyword-search upstream for duplicates (open + closed). Surface likely matches before drafting. Collect reproduction facts (environment, steps, expected vs actual).
- **Update issue**: read current state (title, body, labels, linked refs, recent comments). Identify what needs updating.
- **Create PR/MR**: enumerate commits since base branch, summarize diff, identify linked issues, flag breaking changes.
- **Update PR/MR**: read current title, body, labels, comments, review status, enumerate new commits since last update, and identify what changed.

### 3. Draft Content ⚠️ REQUIRED

Apply the rules file matching the task type: load [issue-rules.md](issue-rules.md) for issues, or reuse [pr-rules.md](pr-rules.md) already loaded in Step 2 for PR/MR drafts. If the draft will include pasted logs, errors, or command output, also load [redaction.md](redaction.md).

### 4. Confirmation Gate ⛔ BLOCKING

Present the full draft to the user:

- Final **title** and **body** (exact markdown)
- **Target**: provider host and project path; issue/PR/MR number if updating; for new PRs/MRs: `head → base`
- **Side effects** (labels to add/remove)
- **Open questions** (unchecked template items requiring user input; redaction placeholders with originals)

Wait for explicit go-ahead (e.g. "create it", "update it", or the same intent in the user's language). Do not proceed on implicit or partial approval.

### 5. Execute & Report ⚠️ REQUIRED

Perform only the confirmed actions; do not bundle extra changes. Return the resulting URL(s) and numbers.

## Anti-Patterns

**Never:**

- Act without explicit user "go" (Step 4).
- Paste raw logs without applying redaction rules.
- Write fix implementations in an issue body.
- Invent template sections the upstream template lacks.
- Skip duplicate search before creating an issue.
- Include issue/PR/MR references (`#N`, URLs) in titles — all references go in the body.

**Avoid:**

- Bundling unrelated edits into one PR/MR update.
- Repeating points already made earlier in a thread.
- Using non-imperative verbs in issue titles ("Adding feature" → "Add feature").
- Overly vague PR/MR subjects ("Fix bug" → "Fix null pointer exception in user authentication").

## Pre-Publish Self-Check

Before Step 4, verify:

- [ ] Title: no `#N`, issue/PR/MR URL fragments; imperative mood for issues; required semantic format for PR/MR unless explicitly overridden by user instructions or documented repository requirements.
- [ ] PR/MR language and format: English prose and a semantic title unless explicitly instructed otherwise; conversation language alone does not override the default.
- [ ] PR/MR content: title, body, and footers describe only changes, rationale, behavior, and compatibility/migration impact; no self-review, self-test narrative/results, agent conversation history, or unrelated metadata, including in template sections.
- [ ] Related issues/PRs/MRs: inline linking keywords only (`Closes #N`, `Fixes #N`, `Refs #N`, `See #N`); no standalone `## Related` section unless the upstream template names it.
- [ ] Content matches the **single** loaded rules file for this artifact (`issue-rules.md` or `pr-rules.md`).
- [ ] PRs/MRs: body covers every non-trivial commit; breaking changes use the repository's title notation (`!` when using semantic format) and explain impact and migration in the body, following the upstream template when present.
- [ ] Issues: reproduction steps complete; expected vs actual behavior stated; environment details included.
- [ ] Pasted logs: Bucket 1 applied; Bucket 2 placeholders + originals only under Open questions.
- [ ] File refs: `path:line` or `path:start-end` format; no absolute paths.
- [ ] Template checkboxes: resolved or listed as open question.

## Resources

| File | When to load |
|------|--------------|
| [preflight-upstream.md](preflight-upstream.md) | Step 1 only if the upstream project or URL was not explicit in the user message |
| [issue-rules.md](issue-rules.md) | Step 3–4: issue draft or update |
| [pr-rules.md](pr-rules.md) | Step 2 before selecting the base or collecting commits/diffs; reuse in Steps 3–4 for PR/MR drafting and confirmation |
| [redaction.md](redaction.md) | Step 3: body will include pasted logs, errors, or command output |
