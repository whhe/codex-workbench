# Clarify Decisions in Rounds

Use this interview before drafting when important owner choices are missing, or when reviewers uncover such a choice. A request for deeper questioning permits exploring consequential branches of the current design, not inventing future requirements. When the brief is already adequate, proceed without an interview.

## Build the decision tree

Identify decisions that change scope, observable behavior, acceptance criteria or a meaningful technical tradeoff the owner has reserved. Relate dependent choices to their prerequisites. Keep a compact decision ledger in the existing brief or conversation: ID, question, prerequisites, options and recommendation where supported, owner answer/status, and affected proposal sections or acceptance criteria. Use open, resolved or explicitly deferred status; deferred does not mean resolved.

Separate decisions from facts. Investigate inspectable repository or external facts within the authorized scope; use a fresh read-only worker for a bounded independent investigation when useful. Supply its question, evidence locations, source-trust boundary, permitted actions and expected evidence/limitations. It returns to the coordinator and does not interview the user, edit files or delegate. Such work consumes the same attempt and automated-time limits as other workers; record its logical work item. Ask the owner only for information or choices that available evidence cannot establish. Report inaccessible evidence rather than guessing.

If no alternative-generation or review phase is active, open an initial clarification-investigation phase before the first fact worker. Record its finite time allowance, deadline and stable fact-question IDs; retain this one phase's elapsed time and attempt counts across interview rounds. It does not consume a proposal review cycle. Complete it when its required investigations and material owner choices are resolved; on exhaustion or deferral, report the outstanding dependencies honestly. Keep unresolved investigations and their consumed limits when proceeding with independent work: changing interview round, phase name or mode cannot restart them. Dependent design work waits for resolution; exhausted investigations require an explicit budget change before another attempt. During an active proposal/review phase, use that existing phase rather than opening a nested clarification phase.

## Ask the current questions

The frontier contains open material decisions whose prerequisites are settled. In one round, ask these independent questions together, using stable IDs and explaining what each answer changes. Offer concrete alternatives and a reasoned recommendation when evidence supports one; use an open question when the alternatives or owner intent are not yet known. Keep costs and consequences visible so a short answer is unambiguous.

Wait for the owner's actual answers before asking dependent questions. A fact investigation still running is an unsettled prerequisite; only its downstream questions wait. Continue unrelated investigation and ask other ready questions without waiting for that fact. Workers never ask the owner directly.

For example, whether a migration must run without downtime can be asked now; the acceptable duration of a maintenance window depends on permission to have one. Do not ask both as if they were independent.

## Incorporate answers

Record the answer and its effects, then recompute the frontier. Preserve existing confirmed requirements; do not reopen them without new evidence, a demonstrated conflict or an owner-requested reconsideration. Resolve a broad "yes" only when its referent is clear. Summarize ambiguous or conflicting answers as a pending question rather than choosing an interpretation.

Silence, elapsed time, an unanswered recommendation or a request to defer never accepts a choice. Explicit delegation of routine technical choices lets the coordinator decide within the existing objective and authority; record the decision and rationale. It does not resolve missing business intent, authorize extra scope or accept material risks on the owner's behalf.

An answer that materially changes requirements or the proposal invalidates affected coverage and follows the normal new-version/full-panel rules. Preserve unrelated findings and their dispositions. User answers are decision inputs, not technical proof that a disputed failure cannot occur. Technical disagreements continue through independent evidence-based cross-examination.

## Pause and finish honestly

While waiting for the owner, respect the entrypoint's clock rules: workers still running keep the phase clock running. Pause only a live phase with no running workers, preserve elapsed time and attempts, and never erase a timeout. If an owner answer arrives after closeout, reassess the current inputs and remaining budgets; it does not retrospectively approve the old snapshot or reset exhausted limits.

Finish the interview when no material open decisions remain for the current objective. An empty frontier caused by pending fact investigations, deferred owner choices or circular prerequisites is not completion: report the dependency and continue independent work or ask the question needed to unblock it. Do not traverse hypothetical branches merely to exhaust a decision tree.

Return the updated brief, recorded decisions, unresolved choices/facts and affected design sections to the coordinator's next stage. If issuing an overall review verdict, use the entrypoint's coverage and verdict rules; do not label missing review coverage Ready because an interview ended. When the relevant choices are explicit, continue already-authorized design work without a second blanket approval request. Implementation and publication remain outside this interview's authority.
