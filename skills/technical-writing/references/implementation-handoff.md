# Implementation handoff

Load for plans that ask readers to change a system. Keep the desired behavior separate from how work is allocated. Use these checks proportionately; a small change can fit in a few paragraphs.

## Outcomes and project boundaries

Connect each outcome to the responsible project, affected code or configuration, compatibility constraints, and acceptance. Distinguish repositories that change from those that only need regression checks. For a conditional repository change, name the trigger.

Prefer compatible changes in the component that owns the responsibility. A change to a platform with a costly release process needs evidence that the owning service or adapter cannot meet the outcome with a smaller change. Include plugins, built-in skills, manifests, and environment settings when accounting for that platform's changes.

## Assignable work packages

Make each package an independently reviewable result. Group necessary scaffolding, configuration, and documentation with the result they support rather than creating administrative fragments. Describe shared rules once, then use a compact package table. Expand a package only for its distinct interface, failure handling, or recovery requirements. Separate required behavior from suggested implementation steps. Include representative examples where they clarify the contract or verification.

| Field | Information the assignee needs |
| --- | --- |
| Goal | Observable result and linked requirement |
| Inputs | Repository and code baseline, relevant sections, source entry points, configuration/fixtures, and dependency artifacts |
| Contract | Consumed and provided schemas/interfaces, revision or digest, producer, consumers, and design-fixed names or values |
| Ownership | Responsible role, allowed write paths at assignment, shared-file owner, and excluded edits |
| Start condition | Upstream outputs and checks that make the package ready; permitted substitutes |
| Outputs | Code/configuration/data artifacts, compatibility notes, and downstream action |
| Acceptance | Scenario/input, expected behavior, command or inspection method, environment, and evidence location |
| Handoff requirements | Recipient, delivery destination, required evidence, and the next consumer's action |

After execution, record actual changes and input baseline, executed and unexecuted checks, and open issues in the handoff. A plan specifies these reporting requirements before results exist.

Specify decisions an assignee cannot safely make alone and their escalation route; link existing implementation detail instead of copying complete function bodies into the plan. Name who supplies missing paths, baselines, or fixtures. A contract-definition package may start first; its consumers wait for the named artifacts. Do not present missing inputs as available.

## Parallel execution and integration

Parallel writers need nonconflicting write scopes and compatible contracts. Assign shared schemas, entrypoints, manifests, lockfiles, and test enumerations to one integrator. A shared directory can contain independent files; separate directories can still change the same logical contract.

Separate initial inventories from integration cleanup: an early package lists planned test/script migrations, and the integrator updates shared enumerations when later packages supply actual changes. State the integration order and who reruns affected checks. Parallelism does not authorize worktree creation or simultaneous writes to an unisolated checkout.

When a contract changes, its owner publishes the new artifact/digest, compatibility impact, affected consumers, fixture updates, and required rechecks. Affected owners acknowledge their updated inputs before resuming integration. Old evidence cannot certify the new contract. Unaffected work can continue.

## Acceptance and dependencies

Trace outcomes to the design/contract, work package, scenario, and eventual evidence. Use stable IDs only where they aid reference. Keep proposed checks separate from executed results.

Check both the work graph and the acceptance graph. A deployment package cannot require a test that first needs that deployment; complete local/contract checks first and use deployed integration checks to control later promotion or release. Mark substitutes and require actual integration evidence before claiming end-to-end completion.

For state changes, locate authoritative and derived data, identity associations, consistency boundaries, retries, partial failures, and recovery. Make rollback account for writes accepted after a cutover. Record performance measures and when thresholds will be established instead of inventing achieved timings.

## Deferred decisions

For each unresolved fact or owner choice, state the missing information, responsible role, resolution point, affected packages, and work that remains safe to continue. Route material owner choices to grilling through the coordinator. Reviewers report questions to the coordinator; they do not contact the user.

## Cold-reader checks

Can an assignee locate its input and allowed files, explain its output contract, and identify its stopping point? Can two assignees detect overlapping writes or incompatible dependencies? Can the integrator order their outputs and verify the outcome? If these answers require the authoring chat, correct the document before final delivery.
