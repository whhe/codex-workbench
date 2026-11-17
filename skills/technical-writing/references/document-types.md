# Document types

Load the relevant type before writing. Choose coverage from the reader task. For a mixed document, identify the primary task and link to supporting material. Headings can follow the subject.

The coverage and completion checks below apply the cited guidance to this skill. The sources do not prescribe the project workflow.

Google recommends short, useful, accurate documentation, updating documentation with code, and linking rather than duplicating existing guidance. It distinguishes design documents used for design feedback from current implementation documentation. [Google: Documentation Best Practices](https://google.github.io/styleguide/docguide/best_practices.html)

## Design proposal / internal RFC

### Reader questions

What problem warrants a decision? What changes for whom? Why this option? What tradeoffs and risks am I accepting? What remains undecided?

### Evidence

Google describes design documents as a way to obtain feedback on a proposed implementation and later archive decisions. An internal document called an RFC should not imply IETF status: the IETF RFC series includes several statuses and archival publication rules specific to its own process. [Google: Documentation Best Practices](https://google.github.io/styleguide/docguide/best_practices.html), [IETF: About RFCs](https://www.ietf.org/process/rfcs/)

### Coverage

- Problem and evidence, intended users, measurable goals, explicit non-goals, and constraints.
- Existing behavior and proposed behavior, with a concrete example when helpful; affected contracts, data, operations, compatibility, and security concerns.
- The selected approach, credible alternatives including retaining the current approach, and the decisive tradeoffs. State assumptions and unresolved decisions with an owner or resolution condition.
- Minimal change boundary, priority and sequencing, parallelizable investigations or implementation areas, validation strategy, and rollout or recovery considerations proportional to risk.

### Limits

Omit IETF publication conventions, unused architecture sections, fabricated alternatives, and deployment or rollback sections for a conceptual decision with no operational change. Preserve a decision's rationale without reproducing meeting dialogue or review history.

### Completion checks

A decision maker can identify the requested decision, compare viable options against the goals, and locate material risks. An implementer can identify scope boundaries and what evidence would demonstrate success. Unresolved questions that block the decision are explicit; the document does not present them as settled facts.

## Implementation plan / parallel-agent handoff

### Reader questions

What am I authorized to change? What must exist first? What can others change concurrently? What contract do I deliver? How will integration and completion be verified?

### Evidence

NASA's requirements checklist emphasizes clear, independently referenceable, traceable and verifiable requirements; it separates product requirements from implementation choices and personnel assignments. Keep desired behavior and work allocation distinct so a task list does not become the requirements. [NASA: How to Write a Good Requirement](https://www.nasa.gov/reference/appendix-c-how-to-write-a-good-requirement/)

### Coverage

Use [implementation-handoff.md](implementation-handoff.md) for project boundaries, work-package fields, parallel ownership, dependency order, verification, and escalation. Its rules apply proportionately to implementation plans.

### Limits

Avoid artificial parallelism, reopening settled choices, commands that add no execution value, and speculative file inventories presented as verified facts.

### Completion checks

A new implementer can start without the chat, locate inputs, identify permitted edits, and explain its output contract. Two parallel workers can identify overlapping resources before editing. An integrator can order the outputs and verify the agreed behavior. Every required outcome has observable acceptance evidence; unresolved prerequisites are visible.

The linked handoff and parallel-ownership rules are project applications. The cited NASA guidance does not prescribe agent orchestration.

## Descriptive architecture analysis

### Reader questions

What exists within this boundary? How do its parts interact? Why is it structured this way? What evidence supports the explanation, and where is knowledge incomplete?

### Evidence

arc42 offers tailorable coverage of goals, constraints, context, building blocks, runtime, deployment, decisions, qualities, risks, and terminology. C4 offers audience-specific levels of abstraction and explicitly says to use only levels that add value. Diataxis distinguishes understanding-oriented explanation from instructions and recommends context, connections, reasons, and bounded scope. [arc42: Template Overview](https://arc42.org/overview/), [C4: Diagrams](https://c4model.com/diagrams), [Diataxis: Explanation](https://diataxis.fr/explanation/)

### Coverage

- System boundary, audience, observation scope or version, domain terms, actors, external dependencies, and the central architectural question.
- Responsibilities and interfaces of major components; representative runtime or data flows; deployment boundaries when they explain behavior. Trace important claims to inspected code, configuration, specifications, or other authoritative evidence.
- Design rationale when known, constraints and quality tradeoffs, failure behavior, and known risks. Label inferred rationale and gaps; do not turn a plausible explanation into historical fact.
- Use diagrams only when they clarify a reader question. Give them a title, scope, clear element types, labeled relationships, and a legend where needed; keep abstractions consistent. These checks follow the C4 diagram review checklist. [C4: Review checklist](https://c4model.com/diagrams/checklist)

### Limits

Omit task allocation, rollout, and implementation acceptance criteria when the purpose is understanding the current system. Do not fill every arc42 section or draw every C4 level. If improvements are requested, separate current-state findings from a linked proposal or plan.

### Completion checks

A reader unfamiliar with the code can explain the boundary, main responsibilities, and one representative flow. Another reader can trace consequential factual claims to evidence and distinguish observation from inference. Diagrams agree with prose and the observed system. Unknowns remain explicit; recommendations do not masquerade as existing behavior.
