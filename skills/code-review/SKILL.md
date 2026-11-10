---
name: "code-review"
description: "Review code with risk-priority checks and evidence-backed findings, read-only by default. Use for reviewing changes, assessing merge readiness, or as an independent reviewer. When the user explicitly requests fixes, route execution to coding-workflow and keep each review round read-only."
---

IRON LAW: Keep the reviewer read-only; only the executing coordinator may route explicitly authorized fixes to coding-workflow, which owns the single review/fix loop.

# Code Review — Risk-Priority with Proportional Verification

## Request Routing

- A direct review request is read-only by default. Return findings, coverage and limitations; the report can be complete while defects remain.
- A direct user request to review and fix authorizes the executing coordinator to resolve the required `coding-workflow` skill through the available catalog and load it for implementation. Pass the original request, confirmed scope, frozen baseline, current change and findings into its planning, verification and single review/fix gate. Completion requires a fresh complete review with no new valid in-scope issues, all earlier valid in-scope issues at every severity closed, and required checks passed.
- Load this dependency only for authorized implementation: it supplies the plan gate, fix execution and repeat-review orchestration. If unavailable, return any useful read-only review and explicitly report fixes incomplete; do not substitute a second loop or install a dependency silently. Existing commit, push, remote-update and publication permissions still apply.
- When invoked as a reviewer subagent, remain on the read-only path even if the original request mentions fixes. Return to the executing parent without calling the workflow or spawning another reviewer. The workflow selects review specialists without requiring this named skill; this route creates no reverse orchestration dependency.

## Read-Only Contract

This skill owns review methods and findings only. The executing parent owns fixes and any repeat-review loop. When invoked by a subagent, remain read-only and return findings to that parent; never delegate back to the parent workflow or start a fix loop. For a direct request that includes implementation, the executing coordinator follows Request Routing and passes each review round here as a read-only task. This does not expand the reviewer's authority.

Inspect code, diff, context and existing evidence. Do not execute project code or tests in the reviewed checkout if they can mutate it. Use supplied verification evidence, read-only analysis, or explicitly authorized isolated checks without publication credentials; report checks that remain unverified. Review output belongs in the conversation or an explicitly requested external report artifact, not an unsolicited tracking file in the repository.

## Uncertainty

Do not guess missing requirements, behavior or facts. Investigate available authoritative context first. A question that can safely wait is a pending item with its affected decision and resolution point; continue independent review. If it prevents a current correctness judgment, mark the affected scope incomplete and actively ask the user when reviewing directly, or return the concrete question to the executing parent when running as a subagent. The parent must ask the user before a dependent action when authoritative context cannot resolve it. Never convert an unanswered question or unavailable verification into a clean pass.

## Workflow

- [ ] Classify direct review versus explicitly authorized review-and-fix; a reviewer subagent always stays read-only. Route implementation before entering the read-only steps below.
- [ ] Step 1: Preflight ⚠️ REQUIRED
- [ ] Step 2: Risk-Priority Audit (checks A–F) ⚠️ REQUIRED
- [ ] Step 3: Present evidence-backed findings and coverage ⚠️ REQUIRED
- [ ] Step 4: Report self-check ⚠️ REQUIRED

### 1. Preflight — Establish Baseline ⚠️ REQUIRED

For a **PR URL**, fetch platform diff and metadata (base/head refs, description, comments, CI status). Confirm the local review head corresponds to that PR before computing a local baseline.

Establish the requested review scope and freeze `baseline_commit` before reviewing:

- For a branch or PR review, resolve the base branch and set `baseline_commit` to its merge base with the initial review head (`git merge-base <base> HEAD`). Use the explicit user/PR base or an authoritatively verified repository base; ask if it cannot be established. A familiar branch name alone is not evidence.
- For an uncommitted-change review, set `baseline_commit` to the initial `HEAD`.
- Record any user-specified path limits. Reuse the executing parent's frozen baseline across rounds; the reviewer itself never commits.

Collect in parallel, within that scope:

- Branch state: `git status --short --branch`
- Commits since baseline: `git log --oneline --decorate --no-merges <baseline_commit>..HEAD`
- Tracked changes, including commits, staged changes, and unstaged changes: `git diff --stat <baseline_commit>`, `git diff --name-only <baseline_commit>`, and `git diff <baseline_commit>`
- Staging layers: when staged and unstaged edits coexist, also inspect `git diff --cached <baseline_commit>` and `git diff` so edits that cancel in the final working tree do not hide the staged state.
- New files: `git ls-files --others --exclude-standard`; read each in-scope file separately, since tracked diffs omit its content.

Explore related modules, usages, contracts, entry points, ownership boundaries, and critical paths.

### 2. Risk-Priority Audit ⚠️ REQUIRED

Review every change in the established scope, including all branch/PR commits when applicable and in-scope uncommitted and new files. Consider categories A–F across the full scope; prioritize actual correctness, security and data risks, and select depth/order by relevance. Mark inapplicable categories without inventing findings or requiring six separate rounds. Reference checklists are prompts, not mandatory architecture or test changes.

#### Pass A — Behavioral Regression & Compatibility

- Did any branch logic, default value, feature flag, or input/output contract change?
- Are API parameters, defaults, and legacy-data handling backward-compatible?
- Does naming/return-value semantics match the existing codebase? Flag "interface says X, implementation does Y" drift.

Explain original → new behavior, impact scope and risk for material behavior changes and findings; do not repeat the full diff as a second report.

#### Pass B — SOLID & Architecture

- **SRP**: Does this module have exactly one reason to change?
- **OCP**: Can a new variant be added without editing existing code?
- **LSP**: Can any subclass substitute the parent without the caller knowing?
- **ISP**: Do all implementers use all interface methods?
- **DIP**: Is business logic tied to concrete I/O, storage, or hardcoded values?
- Overly loose types (`Any`/`any`/`dict`/untyped) masking domain constraints?

Prefer incremental refactor plans over large rewrites. Load [solid-checklist.md](references/solid-checklist.md) for deeper smell prompts.

#### Pass C — Security & Reliability

- Can an unauthenticated or unauthorized user reach this code path? Could tenant A's data leak to tenant B?
- What happens if two requests hit this code simultaneously? Could state change between check and act?
- If this operation fails halfway, is data left consistent?
- Unpinned deps, dependency confusion, known CVEs?
- TLS verification disabled on HTTP clients (`verify=False`, `InsecureSkipVerify`, `rejectUnauthorized: false`)?

Call out both **exploitability** and **impact**. Load [security-checklist.md](references/security-checklist.md) for deeper threat-model analysis.

#### Pass D — Performance & Stability

- What if this runs with 10×/100× data? Are resources bounded and released?
- N+1 queries? CPU-intensive work in a hot path that could be cached or batched?
- On failure: enough context to debug? Secrets leaked in logs or error output?
- What if this value is null, 0, or empty?

Load [code-quality-checklist.md](references/code-quality-checklist.md) for detailed sub-checks.

#### Pass E — Removal Candidates

- Identify unused, redundant, or feature-flagged-off code.
- Distinguish **safe delete now** vs **defer with plan**.

Load [removal-plan.md](references/removal-plan.md) if candidates are found.

#### Pass F — Test Coverage & Language-Specific Checks

- Decide whether the changed observable contract has enough discriminating verification for its risk. Reuse existing tests and checks before adding new ones.
- Missing tests count as regression risk only when the changed logic is materially unverified and the risk cannot be covered by a smaller existing, static, or manual check.
- For a bug fix, recommend that the executor add a focused regression test only when the current suite fails to catch the original failure and the case is stable and valuable to preserve. Do not recommend a duplicate when an existing discriminating test already fails on that same original failure before the fix, or when the change is documentation, configuration, wiring-only, or behavior-preserving refactoring.
- Require integration-level coverage only when a cross-module contract or boundary is not meaningfully verified by focused checks. Do not duplicate unit and integration tests that prove the same observable outcome.
- **Assertion discriminability**: verify fixtures and assertions can distinguish real behavior from bypass/no-op — including cases where filtered and unfiltered results would look the same under the data you used, or where one happy path cannot prove a branch ran. Strengthen with cardinality, identity or negative cases, or observable effects appropriate to the feature.

Language-specific gotchas (non-obvious items the general passes may miss):

| Language | Check | Flag when | Pass |
|----------|-------|-----------|------|
| Python | Naive/aware `datetime` mixing | Naive and aware datetime objects compared, subtracted, or assigned to the same field without explicit conversion | A |
| Python | ORM lazy-load on detached instance | An ORM relationship or deferred column is accessed after the session that loaded the object is closed | D |
| Python | ORM dialect portability | Queries rely on engine-specific SQL or vendor-only functions, raw SQL fragments, or dialect-only types instead of APIs the ORM can translate for every backend the project supports. Confirm compilation or execution against each dialect/version in that supported set | A, D |
| TS/React | `useEffect`/`useMemo`/`useCallback` dependency issues | A reactive dependency is missing, redundant, or is an unstable reference (new object/array/function created each render) | D |
| JS/Node | Global patches/polyfills without guards | A monkey-patch or polyfill executes unconditionally — no environment check, feature detection, or scope isolation | A |

### 3. Present Findings and Coverage

Load [output-template.md](references/output-template.md) for severity and evidence rules. Return findings with verified file/line locations, the failing scenario, observed code or documented-contract evidence, impact and suggested correction. Clearly distinguish verified failures, unverified risks and optional suggestions. Style preferences or unsupported hypothetical concerns cannot become blocking findings.

For each modified region actively try to refute correctness with a realistic failure scenario. In later independent rounds re-read the full accumulated change, including committed, staged, unstaged and in-scope new files against the frozen baseline. Inspect staging layers when they differ. Do not narrow coverage to the most recent fix. Treat any supplied rationale as a claim, not a verdict.

Return the reviewed snapshot/content identity, baseline, covered paths and staging state, findings, and any coverage or verification gaps. A partial review or unavailable prerequisite cannot be reported as a clean complete review. If no actionable findings remain, state that explicitly with checked scope and residual limits; this is evidence for the parent, not permission to commit or a claim that the parent fixed anything.

### 4. Report Self-Check

Apply the self-check in [output-template.md](references/output-template.md). Return the read-only result. Do not edit, stage, commit, push, update remote metadata, reply, resolve threads, trigger review, or implement suggested fixes. The parent can apply authorized corrections and request a fresh review; this reviewer role never orchestrates that loop.

## Constraints & Anti-Patterns

**Never:**

- Dismiss implicit behavior changes from default-value modifications.
- Label an unverified item as "passed."
- Bypass critical checks to make tests pass (removing auth, swallowing exceptions, downgrading security).
- Treat any invocation of the reviewer as permission to fix or publish; an executing parent must handle those operations separately.
- Present a partial review or unverified prerequisite as a clean review.

**Avoid:**

- Listing style/naming issues before security and correctness.
- Reporting "no issues found" without listing what was checked.
- Copy-pasting code without explaining what is wrong.
- Treating all findings as equal severity.
- Guessing at behavior instead of reading actual code and diff.

## Resources

Load on demand — only when a finding needs deeper analysis.

| File | When to load |
|------|--------------|
| [solid-checklist.md](references/solid-checklist.md) | Pass B finding needs smell prompts or refactor heuristics |
| [security-checklist.md](references/security-checklist.md) | Pass C finding needs threat-model detail |
| [code-quality-checklist.md](references/code-quality-checklist.md) | Pass D finding needs stability/performance sub-checks |
| [removal-plan.md](references/removal-plan.md) | Pass E found removal candidates |
| [output-template.md](references/output-template.md) | Steps 3–4 — findings structure, evidence rules and report self-check |
