---
name: "problem-analysis"
description: "Discuss open-ended questions, diagnose causes, and suggest directions or decision criteria. Includes exploratory software discussions. Use the design workflow to draft or review a buildable software design."
---

IRON LAW: Ground consequential conclusions in checkable evidence. When the evidence leaves material uncertainty, state what observation would change the answer.

# Problem Analysis

## Scope and skill selection

Use this skill when the user needs to understand a problem, surface requirements and success criteria, explain a phenomenon, or weigh a decision. Discuss possible directions and suggest priorities, tradeoffs, or tests. A recommendation can describe what to pursue and under what conditions. Leave programming work packages, exact implementation steps, and a ready-to-build design to the software design workflow. Answer simple factual or conceptual questions directly.

Route by the requested outcome. Use this skill to discuss what an enterprise agent platform needs to get right, why those concerns matter, and which requirements depend on the organization. For a proposal that developers should be able to implement, or a review of whether a software design meets that bar, start with the software design workflow. It owns the clarification needed for that design. Inspect the implementation for questions about current code behavior. Use the coding workflow for authorized repository changes.

Use the catalog descriptions to choose the skill for the current stage. Read only the chosen skill's instructions and any references that stage needs. Reassess when the requested outcome changes. When another investigation skill also fits, honor an explicit selection or choose one primary workflow. This analysis can use available evidence and tools on its own. For a distinct follow-on deliverable, hand off the goal, evidence, constraints, and acceptance criteria to the best-fit capability if available. If the necessary capability is unavailable, deliver the supported analysis and identify the requested work still pending.

## Workflow

- [ ] **Frame the question.** Identify the problem to explore, the phenomenon to explain, or the choice to make. For exploratory scoping, identify the intended users and outcomes. Explain why each major concern matters and which constraints determine its priority. For diagnosis, check definitions, population, denominator, and period where relevant. Inspect available evidence before asking. Ask for the specific missing fact or preference when a useful answer depends on it. Give a conditional answer if that still helps.
- [ ] **Weigh the evidence.** Distinguish observations, inferences, and unknowns. Tie consequential claims to a source, supplied observation, or reproducible calculation. Keep plausible explanations or options that would change the answer, the evidence needed, or the next action. Check the freshness and scope of decision-critical evidence.
- [ ] **Choose the next check when needed.** Use the lowest-cost feasible observation that could distinguish the remaining explanations or change the choice. For a decision, state what would reverse the recommendation. When a pilot is warranted, define the metric, comparison or baseline, observation window, and the result that would continue, change, or stop the action.
- [ ] **Deliver what was requested.** For exploratory scoping, present the key concerns, what good looks like, and the questions that would materially change priorities. Treat organization-specific requirements as conditional until supported. For diagnosis, a decision, or a test, give the result with its key evidence and unresolved conditions. Match the depth to the stakes. A bounded question can take one paragraph. Update the conclusion when new evidence changes it.

Collect and report only evidence needed for the question. Keep tool use within the user's authorization. Carry existing authority into a follow-on stage only for the operations it covers. Report proposed checks, completed actions, and observed effects according to what actually happened.

## Example

Signup completion dropped from 8% to 5% when tracking changed. Compare backend completions and analytics for the same eligible population and periods. Stable backend completion with falling analytics supports investigating measurement first. A decline in both warrants checking where users dropped out. If backend records are unavailable, report which interpretations remain open and what comparison would distinguish them.
