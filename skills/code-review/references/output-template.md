# Review Output Template

Output the review directly in the conversation. Export a report file only when explicitly requested, to an external artifact location; do not create tracking files in the reviewed repository. Preserve prior reports unless replacement is authorized.

## Severity Levels

| Level | Description | Action |
|-------|-------------|--------|
| **High (blocker)** | Verified serious security exposure, data loss or critical correctness failure | Block merge on the demonstrated impact |
| **High** | Material regression with a realistic failing scenario and significant impact | Fix before merge |
| **Medium** | Evidence-backed defect with bounded functional or maintenance impact | Fix or explicitly track according to impact |
| **Low** | Evidence-backed defect with limited impact | Prioritize by actual impact |

Assign severity from the failing scenario and consequences, not from a checklist label, SOLID preference, file length or missing abstraction. Design suggestions without a demonstrated defect are optional observations, not blocking findings.

## Template

Use only sections that add relevant information. A small review may consist of findings plus snapshot, coverage and limits; do not emit empty severity sections or a duplicate behavior-change table.

```
## Code Review Summary

**Branch**: <branch> → <base>
**Files reviewed**: X files, Y lines changed
**Overall assessment**: APPROVE / REQUEST_CHANGES / COMMENT

---

## Findings

### High (blocker)
(none or numbered list)

### High
1. **[file:line — symbol]** Brief title
   - Impact area (business / security / performance / compatibility / maintainability)
   - Evidence (code snippet or diff excerpt)
   - Risk explanation
   - Suggested fix
   - Test status (verified / unverified + reason)

### Medium
2. (continue numbering across sections)

### Low
...

(If no issues found: state what was checked, areas not covered, and residual risks.)

---

## Changes Impacting Existing Logic

| Location | Original Behavior | New Behavior | Impact Scope | Risk |
|----------|-------------------|--------------|--------------|------|
| `file:line` — `symbol` | ... | ... | ... | None / Risk + reason |

## Removal / Iteration Plan
(if applicable — safe-to-remove items and deferred items)

## Reviewed Snapshot and Coverage
- Frozen baseline and exact reviewed content identity
- Covered paths, staged/unstaged layers and in-scope new files
- Missing context or incomplete checks; distinguish a complete review from a partial one

## Test & Verification Notes
- Checks performed / not performed
- Language-specific checks applied
- Existing test changes and their coverage; recommended executor follow-up, distinct from checks actually performed by this read-only reviewer

## Merge Recommendation
- Ready to merge / Mergeable after fixes / Not recommended
- Blockers (if any)
- Optional improvements (suggest splitting into separate PRs)
```

## Evidence Rules

- Every finding must include `file`, `lines`, and `symbol`. Include code snippet for High/Medium.
- Prefer quoting actual diff code over abstract descriptions.
- If a line range cannot be reliably determined, write "line range unverified" with explanation.

## Pre-Publish Self-Check

Before finalizing the report:

- Re-read the full diff to confirm no runtime / security / data-consistency issue more severe than the reported findings was missed.
- If low-risk style issues (copy, i18n, minor hardcoding) are included, verify higher-risk stability/security/compatibility issues are already covered.
- Confirm findings are ordered by severity (High blocker → High → Medium → Low).
- Eliminate cross-section duplication — the same issue should not appear in full in both "Findings" and "Changes Impacting Existing Logic."
- Keep one coherent report without repeated summaries or duplicated findings.
- For regenerated reports, verify no leftover content from the previous version.
- Identify the reviewed snapshot and coverage. A fresh independent round need not receive earlier verdicts; verify current code and contracts on their own evidence.
- Verify language-specific checks were applied for all languages present in the diff; list which checks were performed in "Test & Verification Notes."
