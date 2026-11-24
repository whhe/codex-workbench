---
name: "technical-writing"
description: "Create or revise a requested standalone technical document, such as a Markdown file or Feishu Doc. Load for delivery when the content is ready for the requested document or draft. Begin with analysis or design when needed."
---

IRON LAW: Give the intended readers the information they need to understand, decide, or act, with supported claims and clear boundaries; keep private working context out of the document.

# Technical writing

## Workflow

- [ ] Identify the document type, audience, purpose, scope, and destination.
- [ ] Check the source status against the intended use of the document.
- [ ] Apply the research dependency when its drafting trigger applies.
- [ ] Draft from verified subject evidence, using headings that support selective reading.
- [ ] Check relevance, privacy, and the necessity of proposed changes; apply humanizer to the prose.
- [ ] Freeze the candidate, obtain independent reader reviews, fix valid findings, and re-review.
- [ ] Verify the delivered content, links, navigation, and rendered layout.

## When to load

Start here when the user asks to create or revise a standalone technical document from supplied decisions, evidence, or an existing draft. Use the corresponding content workflow for chat analysis or design, including responses formatted in Markdown.

For a request that combines analysis or design with document delivery, start with the content workflow. Load this skill when the findings or decisions needed by the document are ready, or when the user requests a draft that can carry unresolved items. Carry forward the source evidence, settled decisions, open items, and scope.

## Source status and handoff

For a document presenting a software design for direct implementation or asserting current implementation readiness, establish readiness before drafting the final artifact. Recheck before delivery that the candidate preserves the reviewed design and that the requirements and evidence supporting the verdict still apply. Formatting and editorial changes can retain coverage after a comparison confirms the technical meaning. Substantive changes to the design, implementation constraints, or acceptance criteria and changes to the underlying requirements or evidence can invalidate coverage even after drafting or reader review.

When readiness evidence is missing, stale, or invalidated, resolve a software design assessment capability from the catalog. Prefer `implementation-design` when the earlier `design-review` is also installed. Pass the exact candidate or immutable locator, relevant source versions, existing review evidence, and the authorized revision scope. Default to assessment of the supplied candidate. Distinguish permission to edit the deliverable, permission to revise design decisions, and permission to modify the source proposal. Request the assessed proposal and version, reviewed inputs, verdict, findings, and coverage back in this workflow. The document coordinator owns delivery. If the capability is unavailable or the candidate remains below Ready, report the blocker to implementation-ready delivery.

When recording an existing decision, assessment, or explicit draft, preserve the version, source status, and material open items. Attribute a prior verdict to the version and evidence it assessed. Route substantive corrections to the content workflow within the authorized revision scope. If a correction exceeds that scope, report it with the source status in a faithful record, or identify it as a blocker when it prevents the requested use.

Select the destination capability when creating or updating the requested artifact. Verify the result at the requested destination and return its path or link. If delivery is blocked, state what is missing and report the current draft or source status.

## Dependencies and authority

Resolve these skills through the available catalog, including namespaced variants. Load each when its stage is reached.

| Capability | When required | Inputs and output | If unavailable |
| --- | --- | --- | --- |
| research | The user requests research, or required source evidence for a material claim or document convention is missing; reuse relevant verified findings | Specific evidence gap, reader task, and constraints; returns primary-source findings with citations | Report the missing capability and block dependent drafting |
| grilling | A material question about intent, scope, acceptance, or a tradeoff cannot be resolved from sources | Known facts, the open decision and its dependent work; returns explicit answers or a defined deferral | Report the gap and keep dependent work blocked |
| humanizer | The prose pass before reader review, and after substantive rewrites | Current draft, intended voice and supported facts; returns final prose without editing commentary | Report the gap; do not claim the prose pass is complete |
| Independent subagents | Reader review before final delivery | Frozen draft, intended readers, relevant sources and task boundaries; returns findings to the coordinator | Keep a working draft and report the coverage gap; do not substitute author approval |

Pass the selected external working-file destination to research as explicit task instructions adapting its default repository output. Keep necessary factual evidence and source citations in the requested document. Writing authorizes the requested document changes; implementation, commits, deployments, data operations, and broader sharing need their own task authority. Reviewers stay read-only and do not delegate or contact the user.

Use grilling as bounded clarification within the agreed document task. Pass only unresolved material decisions and the actions they block. Explicit answers that settle those decisions complete the interview and unblock already-authorized writing. Ask again when an answer remains ambiguous or exposes a new material dependency.

## Establish the reader task

Read the current document in full before revising it. Distinguish agreed requirements, descriptions of the observed system, and historical decisions, including within mixed documents. An implementation mismatch does not authorize weakening a requirement or rewriting an accepted decision; report the discrepancy. Update descriptive claims from current evidence, and change agreed or historical decisions only within the authorized scope. Identify what readers need to understand, decide, or execute. Preserve the user's confirmed choices and later corrections. Ask material owner questions promptly through grilling; investigate facts the sources can establish. Respect explicitly deferred questions, record their blocking scope, and continue independent work. Do not infer an answer from silence.

When research is required, select primary sources for the actual question. Use subject evidence for factual claims and primary guidance for document conventions. A template cannot establish what a system does.

| Reference | When to load |
| --- | --- |
| [document-types.md](references/document-types.md) | Selecting coverage and completion checks for proposals, implementation plans, or architecture analysis; research other types as needed |
| [implementation-handoff.md](references/implementation-handoff.md) | The document proposes implementation, migration, cross-project changes, or parallel work |

Use the document type's structure. A design proposal explains a decision and its consequences. An implementation plan specifies changes and execution. An architecture analysis describes the observed system and its evidence. Add execution instructions to an analysis only when requested; keep them separate from current-state findings.

## Organize for selective reading

Name sections for the information they contain: the component, decision, interface, change, or operation. A reader or agent should be able to select the relevant section from its title without loading the entire document. Avoid vague headings such as "Other information" or "Further thoughts."

Separate the goal and scope, proposed changes, execution and acceptance, and background evidence where those subjects apply. Give long documents a short reading map and direct links. Open a substantial section with a brief summary of its conclusion, scope, and reading priorities; keep details below it. A short section needs no separate summary. Place definitions beside the rules that use them. Keep one authoritative definition of each contract or decision and link to it from other sections.

State the meaning of required references in the document itself. Linked sources supply evidence and detail; readers should not need the authoring chat to discover the goal, chosen behavior, prerequisites, or unresolved decisions.

## Preserve scope with the smallest sufficient change

For every proposed change, identify the agreed outcome it serves, the observed gap, and what fails if it is omitted. Compare a smaller change in the responsible component before introducing abstractions, migrations, new infrastructure, or changes to shared platforms. Retain the smallest approach that meets the stated outcome and acceptance criteria.

Put agreed deliverables in the implementation list, ordered by priority and dependency. Keep unselected enhancements outside that list. State conditional integration triggers explicitly. A required outcome may need different repository edits depending on compatibility; this does not make the outcome optional.

Research and reviews do not expand the task. Evaluate each suggested remedy for necessity and affected scope. Keep useful findings about unrelated improvements in a separate response or backlog only when relevant; do not silently add them to the document or its implementation work.

## Shareable content and evidence

Write for the intended audience, using the document's language. Keep facts, proposals, inference, and unresolved choices distinguishable. A planned check is not an executed result. Preserve uncertainty that changes a reader's decision or action.

Keep records of drafting and reviewing this document outside the delivered content, including appendices, attachments, comments, and working-record links. Incorporate document review findings as corrected content. For a requested assessment report, preserve its subject's verdict, evidence, findings, and coverage. Retain technical rationale, code baselines, contract revisions, and unresolved conditions needed by readers. Include publication history when the document's purpose calls for it.

Remove credentials, session tokens, unnecessary personal data, private machine details, and unrelated sensitive content from prose, examples, diagrams, screenshots, metadata, and link query strings. Disclose only what the intended audience needs and is authorized to receive. If a sensitive value matters operationally, use a consistent placeholder and identify the approved configuration source; never reproduce the secret. Flag an unresolved disclosure question before sharing.

Convert author-machine source paths to verified repository-relative paths or accessible repository-host links. Name the repository when a relative path would be ambiguous. Keep documented deployment paths only when readers need them to execute the work. If the repository root or remote URL is unknown, inspect it or report the gap; do not invent a link. Normalization and sanitization happen before the humanizer prose pass.

Cite consequential claims near their supporting sources and record how important observations were checked. For hosted source code and commits, link to verified revisions on the actual Git host, using immutable revisions and file/line anchors where available. For local or unpushed code, cite verified repository-relative paths and relevant symbols or lines, identify the inspected snapshot and any uncommitted changes, and provide the intended readers with the same source snapshot through the authorized destination. If readers cannot access that evidence, report the access gap. A hash alone is not a usable shared reference. Check access for the intended audience without changing permissions or expanding disclosure merely to make a link work.

## Prose and presentation

Use humanizer in embedded mode to mark AI patterns, rewrite the prose, and verify that claims, scope, numbers, conditions, and citations retain their meaning. Give it the current sanitized draft and relevant voice sample, not unrelated chat or private working notes. Read changed files fully; preserve metadata, commands, identifiers, paths, and link targets during this prose-only pass. Return only final text in the document.

Keep prose concise while preserving the context, conditions, evidence, and failure cases readers need. Explain technical distinctions that affect understanding or action.

Choose diagrams and tables by the reader question. Prefer Mermaid for system boundaries, flows, calls, dependencies, and state transitions when the destination supports it; use its native diagram format or a rendered equivalent otherwise. Keep diagrams focused and label their scope, relationships, and conditions. Do not add chart types merely to fill a template.

| Reader question | Useful representation |
| --- | --- |
| What interacts, and in what order? | Mermaid flowchart or sequence diagram |
| What states, transitions, or prerequisites exist? | Mermaid state diagram or dependency graph |
| Which project changes, and who owns which interface? | Project-impact or interface-contract table |
| Why this choice? | Options and tradeoffs comparison table |
| What runs first or in parallel? | Priority, dependency, and work-package table |
| How is completion established? | Requirement-to-scenario and acceptance-evidence table |

Place each visual beside the explanation it supports. Keep nodes, edges, conditions, identifiers, and table entries consistent with prose and evidence. State essential conclusions and rules in text without transcribing every cell or edge. Preserve the destination's resource objects and heading hierarchy. After edits, inspect representative rendered sections, including the end of long documents, for empty blocks, excessive gaps, clipped diagrams, and broken navigation. A parser check alone is not visual verification.

## Adversarial reader review

Before dispatch, freeze the complete candidate with an internal identifier or digest. One review phase covers that version through reconciliation and closure checks. Set a finite phase deadline and at most two attempts per logical review assignment, including its initial dispatch and one retry. Keep these limits across batches, replacement reviewers, and editorial fixes. A material revision made within an active phase starts a new version and phase. Redispatching the same candidate does not reset limits; resuming after an exhausted deadline or attempt limit requires an explicit budget change. Use at least two independent reader perspectives: the intended user or decision maker, and a technical reader who must explain the analysis or execute the plan. For changes spanning projects, include an affected maintainer or integrator; include security/data expertise when disclosure or state integrity warrants it.

Give fresh-context reviewers the same complete candidate without the authoring chat or other reviewers' findings. First ask each to complete a representative reader task using only the document and its declared companion artifacts: state a decision and its costs, explain a system flow, or locate an assignment's first action, inputs, output, and acceptance. Require answers with section references and explicit missing premises; reviewers must not invent missing context. Then provide the minimum source evidence needed for factual checks. Ask them to challenge missing context, unsupported claims, ambiguous boundaries, unnecessary changes, and realistic failure cases from their assigned reader's position. Each finding needs a location, evidence or a concrete counterexample, its impact, and the smallest correction. A finding quota is unnecessary.

Collect every first-pass report before comparing findings. Resolve material owner questions through grilling. Apply the smallest in-scope document fixes for evidence-backed findings and record their disposition privately. Apply the source status and handoff rules to findings about the underlying analysis or design. Independently challenge material rejections or disputed claims; author reassurance and agreement counts do not settle them.

Review the revised complete candidate with fresh readers after changes to scope, behavior, interfaces, or acceptance; after their first pass, verify closure of earlier findings. For editorial fixes, verify meaning and retain applicable coverage with a recorded explanation. Continue until all valid in-scope findings are closed, questions blocking the agreed document purpose are resolved, and the current candidate has complete reader coverage. A proposal may present a choice for its intended decision maker, and explicitly deferred choices may remain open; identify the responsible role, resolution point, and execution they block. User acceptance of a known defect does not make it fixed.

If a deadline, attempt limit, missing capability, or a question blocking the agreed document purpose prevents completion, retain useful draft work and report the exact blocker outside the document. Do not label the artifact final or approved. No readiness claim grants implementation or publication authority beyond the user's request.

## Final checks

- Can a reader identify the purpose and select useful sections without the chat?
- Does every section serve the reader's understanding, decision, or action, with this document's production records kept private?
- Are proposed changes necessary, scoped, prioritized, and tied to observable acceptance?
- For execution, are ownership, parallel boundaries, dependencies, and handoff inputs clear and free of circular prerequisites?
- Are facts supported, local paths portable, sensitive values removed, and operational placeholders consistent?
- Has humanizer preserved the technical meaning while removing AI phrasing and drafting residue?
- Have different reader perspectives reviewed this candidate and closed all valid findings?
- Do the delivered content, resource objects, source links, and internal navigation match the final candidate?
