---
name: "design-review"
description: "Clarify consequential design choices in rounds, develop technical proposals or challenge an existing design before implementation through independent subagent perspectives, evidence-based cross-examination, revision and independent re-review until valid in-scope findings are closed. Use for architecture choices, implementation approaches and technical plan reviews; implemented diffs belong to code review."
---

IRON LAW: Bind every readiness verdict to the exact proposal version and completed independent review coverage; the author cannot approve their own proposal.

# Design Review

## Workflow

- [ ] Establish the mode, outcome, authority, constraints and unresolved decisions.
- [ ] (Conditional) Clarify material owner choices in dependency order; investigate facts independently.
- [ ] (Propose mode) Compare independent alternatives and select a draft.
- [ ] Freeze the draft and obtain independent reviews from every required perspective.
- [ ] Reconcile evidence, cross-examine material disputes and record dispositions.
- [ ] When revision is authorized, repeat revision and independent review until all valid in-scope findings are closed; otherwise return the read-only assessment.
- [ ] Return the current proposal, verdict, coverage and unresolved risks.

## Scope and capabilities

Use **propose and review** when asked to develop an approach. Use **review existing** when supplied a design to assess; identify the actual proposal before reviewing. Proposing a solution includes the independent review/revision loop by default; users need not request that loop separately. Reviewing an existing proposal remains read-only unless revision is explicitly requested. A comparison request may end with a recommendation, but label it unreviewed if the review stages were not performed.

This package is self-contained. Use available capabilities for source inspection, external research when needed, and native subagent delegation. It requires no other skill, provider, CLI, team runtime or state service. Select the host's actual delegation interface; never invent tool names or model availability. Inherit the available model unless the user or environment authorizes another selection. Same-model agents provide context independence, not cross-model diversity.

Use fresh-context children for independent work. Give each only the stage contract and raw inputs it needs, not the entire skill or authoring conversation. Workers return to the coordinator, remain read-only, and do not spawn children or contact the user. The coordinator alone owns drafting, user questions and reconciliation. Batch work to fit available slots; wait for completion and release finished workers where the host requires it. Never share first-pass findings with reviewers still performing their first pass.

If delegation is unavailable, continue useful drafting or explicitly labeled self-review and return **Incomplete** for the independent review. A failed or partial required reviewer leaves coverage incomplete; retry only within both the work-item attempt limit and phase deadline established below, or report the gap. Never replace a missing independent reviewer with the author's approval.

Review existing is read-only by default: return suggested revisions in the response. A request to create or revise a proposal authorizes those document changes at the requested destination, not implementation or publication. Honor narrower restrictions. Use chat when no file is needed; for authorized files follow repository or user destinations. Keep incidental worker logs outside the repository. Do not change code, install dependencies, commit, publish or send external messages as a side effect of this skill. A readiness verdict adds no execution authority.

## Load only the current stage

| Reference | When to load |
| --- | --- |
| [clarification.md](references/clarification.md) | Material owner decisions are unresolved before drafting or emerge during review, or the user requests a deeper design interview |
| [proposal.md](references/proposal.md) | Generating alternatives, selecting a draft, or preparing a material revision |
| [review.md](references/review.md) | Dispatching reviewers, cross-examining findings, reconciling or re-reviewing |

## 1. Establish the brief

Inspect relevant requirements, repository instructions, affected interfaces and existing decisions. Build a shared brief containing:

- Objective, observable success criteria, scope and exclusions.
- Constraints and evidence locators; distinguish facts, assumptions and predictions.
- Material owner decisions, unknown facts and the decisions depending on them.
- Available source material, permitted actions and artifact destination if any.

Investigate discoverable facts rather than asking the user to retrieve them. Ask about missing owner decisions before choosing a dependent design. Continue independent work, keeping unresolved branches explicitly pending. A reviewer returns questions to the coordinator; silence is not an answer. Record inaccessible evidence as a limitation, not a verified premise.

When material owner decisions remain, use clarification.md to interview in rounds based on decision dependencies. Skip the interview when the relevant decisions are already settled. Keep this method inside the package; no external interview skill is required. During review, factual disputes remain evidence questions for reviewers; only genuine owner choices return to this interview path.

Set any explicit user review budget before dispatch. By default there is no fixed cycle limit: when revision is authorized, continue until the latest complete independent review finds no new valid in-scope findings, all earlier valid in-scope findings are closed, and applicable validation passes. One cycle reviews one frozen version, including cross-examination; material revision starts another cycle. Keep the finite phase deadlines and work-item attempt limits below. If repeated findings or failed attempts cannot make progress, report the concrete blocker rather than resetting limits or claiming readiness. A read-only review may finish with findings; completion of its report is not proposal readiness. Honor explicit user limits and stricter host or repository gates.

Before dispatching any child, also set a finite phase deadline and a work-item attempt limit. A phase is initial clarification investigation, alternative generation or one complete review cycle, including cross-examination and closure checks. Clarification investigation inside an already active phase consumes that phase's budget; use clarification.md for the initial phase's lifecycle. Choose and record a concrete allowance for automated elapsed time appropriate to the task and host; start it with the phase's first dispatch and track it across batches and worker waits. Default to **two attempts per logical work item** (initial dispatch plus one retry). Identify work items by fact question, proposal direction, review perspective or specific dispute/closure question within that phase; renaming a worker does not reset attempts.

Only an explicit wait for a material owner answer, with no worker still running, may pause the phase clock. Record consumed and remaining time when pausing; on resumption set the deadline from the remaining allowance, retaining attempt and cycle counts. A phase that has already expired cannot be paused or revived this way. Worker failures, no-progress responses and waiting with active workers continue to consume time; never reclassify that elapsed time retroactively. Before resuming dependent work, check source changes and apply the normal version and coverage rules. An initial interview before any dispatch starts no phase clock.

Use bounded waits and host time observations so an unresponsive worker cannot outlive the phase's waiting budget. If the host cannot support bounded waiting, report that capability gap as Incomplete. Count each initial dispatch, replacement or request to retry an item as one attempt; a partial or no-progress completion is an unsuccessful attempt, not an extra attempt or a reason to reset counters. Keep the original phase deadline across retries. At either limit, stop retrying the affected item; at the phase deadline, stop dispatching or waiting for that phase. Interrupt unfinished workers where supported, record any that could not be stopped, retain completed results and return **Incomplete** when required work is unfinished. Do not silently reset limits or use late results to approve a snapshot after closeout; continuing requires an explicit budget change and reassessment of current inputs.

## 2. Prepare and freeze the proposal

In propose mode, use proposal.md to dispatch two independent alternatives, or three when an important design fork warrants it. Select a recommendation against the brief. Existing-review mode skips generation unless a material choice needs a bounded alternative comparison.

Assign an immutable version such as `v1` to the complete draft and brief. Preserve its text or capture a content digest when files are available. Include the rationale and rejected alternatives in the proposal itself. Record the exact requirement/source versions used where obtainable. If an input changes during review, invalidate affected coverage and review the new snapshot; unrelated results may remain diagnostic evidence, not approval of the new version.

## 3. Independent panel

Read review.md. Default to three separate fresh reviewers:

| Perspective | Responsibility |
| --- | --- |
| Architecture and simplicity | Goal fit, alternatives, unnecessary abstraction, interface and dependency tradeoffs |
| Correctness and integration | State transitions, failure modes, concurrency, compatibility and cross-module effects |
| Delivery and verification | Sequencing, acceptance checks, rollout, observability, migration and recovery |

Add a security and data reviewer when the proposal touches authorization, trust boundaries, sensitive data or data integrity. Add another domain perspective only for a concrete risk. Record why each conditional perspective applies or is unnecessary. User-requested focus supplements the panel; it does not silently remove required coverage.

Each reviewer inspects relevant original evidence and returns findings, material questions, coverage, limitations and a local verdict for the frozen version. No finding quota: an adequate proposal may have no findings. Reviewers seek realistic counterexamples, not performative hostility or unrelated redesigns.

## 4. Cross-examine and reconcile

Wait for every first-pass result before exchanging findings. Deduplicate by root cause while retaining original IDs and reviewer sources. Send disputed high-impact claims, unsupported severe findings and material author rejections to a different reviewer for targeted challenge. Allow the originating reviewer to defend, narrow or withdraw the claim. Independent corroboration is useful; votes and agreement are not evidence.

Use the evidence and disposition contracts in review.md. Preserve unresolved minority concerns and record why a finding was accepted, partially accepted, rejected or remains pending. A coordinator's rejection of a reviewer-confirmed Blocker or Major remains disputed until independently resolved or returned as an explicit owner decision; it cannot silently become Ready.

## 5. Revise and re-review

Revise only the affected sections and their dependencies. In read-only mode, present proposed changes without editing the source. A suggested fix is not an applied fix: assess readiness against the actual current proposal.

For material changes to architecture, behavior, scope, risk controls or validation, create a new immutable version and dispatch fresh reviewers covering the full required panel. Give them the full current proposal and original brief; ask for independent review before they see the old finding ledger. After that pass, provide the ledger for closure checks and examine revision-induced risks. Prior clean reviews cannot approve changed content.

For purely editorial changes, compare versions and record why meaning is unchanged; preserve applicable independent coverage with that explanation. Any unresolved earlier valid in-scope finding, including Minor, still prevents Ready. New scope or owner decisions return to the brief before dependent revision.

## 6. Verdict and delivery

Use one overall verdict, listing other outstanding conditions alongside it:

| Verdict | Condition |
| --- | --- |
| Incomplete | Required capability, source evidence or independent coverage is missing, failed, stale or partial, including required cross-examination or closure checks still pending |
| Needs decision | Coverage is sufficient to identify a material owner choice, but that choice remains unresolved |
| Needs revision | Any confirmed valid in-scope finding remains, including Minor |
| Ready | Required independent coverage is complete for the current version; no new valid in-scope findings remain, all earlier valid in-scope findings are closed, material questions are resolved and applicable validation passes |

If several conditions apply, use the first applicable row and retain all known findings. Owner acceptance of a known risk is an explicit decision, not a technical fix: report the acceptance and residual finding and keep **Needs revision** while the finding remains valid and in scope. Lowering severity alone does not close a finding. If an explicit user budget or phase limit ends with outstanding conditions, return the best current proposal with the corresponding non-Ready verdict and next required action. Do not extend exhausted limits or hand off to implementation automatically.

Deliver proportionately:

1. Current proposal or link, immutable version, recommended approach and tradeoffs.
2. Verdict and evidence supporting it; distinguish design assessment from executed experiments or implementation verification.
3. Panel perspectives, actual independent workers/model diversity, reviewed versions, cycle count and coverage gaps.
4. Findings and dispositions, including unresolved disputes, owner decisions and residual risks.
5. Changes made or suggested and the next action needed, if any.

## Delivery checks

- [ ] Every required perspective reviewed the current version, or the result is explicitly Incomplete.
- [ ] Material owner answers are recorded; unanswered or deferred choices have not become assumptions or approval.
- [ ] Every valid in-scope finding, including Minor, is actually closed in that version or remains outstanding; optional suggestions are listed separately.
- [ ] Rejected material findings have independently checked reasons; unresolved disputes and owner questions remain visible.
- [ ] No stale version, failed worker, cycle limit or suggested-only fix was treated as approval.
- [ ] Source edits and output locations match authorization; no implementation or publication was inferred.
