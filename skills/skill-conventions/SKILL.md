---
name: "skill-conventions"
description: "Create, edit, or review skill packages for clear triggering, self-containment, portable instructions, and lightweight structure."
---

IRON LAW: Keep each skill's responsibility explicit; any skill dependency must have a declared one-way contract and a defined missing-dependency outcome.

# Skill Conventions

Apply these conventions to the complete skill package.

## Workflow

- [ ] Establish the requested capability, target package, authorized changes and unresolved choices.
- [ ] Preserve existing supported metadata and invocation/authorization behavior; choose the smallest useful package structure.
- [ ] Write a discriminating description, essential constraints and conditional reference pointers.
- [ ] Verify package validity, referenced resources, realistic task behavior and any changed executable helpers.

## Frontmatter

For new repository skills, default to two keys: `name` and `description`, with quoted string values (no block scalars `>-`, `|`, `|+`). The examples below describe this repository default, not the complete supported skill format.

When updating an existing skill, preserve supported metadata and `agents/openai.yaml` UI, policy and dependency configuration, including explicit-only invocation. Do not delete or regenerate them merely to match the new-package default. Format or invocation migrations require an explicit task need and resolved scope; uncertainty about the intended behavior requires asking before changing it. If another active authoring policy conflicts with preserving the existing format or behavior, surface that conflict and ask before a destructive cleanup rather than silently discarding configuration.

```yaml
# Good
---
name: "my-skill"
description: "What it does and when to use it."
---

# Bad — block scalar, extra keys
---
name: my-skill
description: >-
  block scalar
capabilities: [...]
---
```

### Description

`description` is the **sole input** for skill-trigger matching. It must convey what the skill does and the situations it applies to, enabling the model to match by **understanding user intent** — not by scanning for literal tokens.

- Describe capability and problem space in natural sentences.
- Include representative scenarios and action verbs so the model grasps the semantic scope.
- Do NOT reduce the description to a bare keyword list or multilingual word dump — this encourages shallow token-matching instead of intent-based reasoning.

```yaml
# Good — capability + scope + scenarios as natural language
description: "Risk-priority code review with proportional verification and an optional fix loop. Use when the user asks to review code changes, evaluate merge readiness, audit for security or performance risks, or identify regressions in a branch or PR."

# Bad — keyword bag, no semantic context
description: "code review, inspect, review, audit, check, PR, security"
```

## Core Constraint (Iron Law)

Every skill MUST declare a core constraint immediately after the frontmatter, before any heading. It answers: **"What is the one mistake the model will most likely make with this skill?"**

```markdown
IRON LAW: Every finding MUST cite file, line range, and code evidence.

# Code Review — Risk-Priority with Fix Loop
...
```

## Structure

Default to **SKILL.md only**. Expand to multi-file only when the skill needs executable scripts or domain knowledge too large for a single file.

```
skill-name/
├── assets/         # Static files used in output (images, templates); never loaded into context
├── references/     # Domain knowledge, loaded on demand; one nesting level max
├── scripts/        # Executed, not loaded into context; flat files only, no sub-packages
└── SKILL.md        # Required — workflow + instructions (≤ 500 lines)
```

**Constraints:**
- Use the listed top-level entries for new packages. Preserve an existing supported `agents/` directory and its configuration when updating a package. Add optional metadata only for an actual requested need. Do not add a skill README.md; keep installation and repository navigation outside skill packages.
- Do not create `scripts/`, `references/`, or `assets/` unless actually needed — SKILL.md-only is the default.
- Overflow domain knowledge from SKILL.md into `references/`.
- SKILL.md must include a load-timing table for each reference file:

  | File | When to load |
  |------|--------------|
  | security-checklist.md | Pass C finding needs threat-model detail |

## Skill Workflow Structure

Complex skills should include a **trackable checklist** near the top of the skill body — either directly after the Iron Law line, or as the first content under the skill's `## Workflow` heading (which itself follows the H1 title). Do not bury the checklist deeper in the file.

| Marker | Meaning |
|--------|---------|
| `⚠️ REQUIRED` | Must not be skipped |
| `⛔ BLOCKING` | Prerequisite — blocks all subsequent steps |
| `(conditional)` | Depends on earlier choices or runtime conditions |

**Execution gates** — distinguish implementation authority from publication authority and delegated review handling. An adequately specified task permits implementation without routine plan approval; commit/push confirmation follows the active task-phase rules and existing explicit authorization. A broad autonomy statement must not override those gates. Confirm final content and target before creating an MR/PR; a dedicated issue/PR drafting workflow retains its final-content confirmation gate. Keep a declared read-only reviewer non-mutating even when the overall task includes fixes; its executing parent owns the implementation. For destructive or high-cost operations, require a clear task need, exact targets, attribution, and safety checks; stop and report unsafe or ambiguous scope rather than using a routine approval prompt as a substitute for evidence. Respect explicit user limits and higher-priority policy.

## Uncertainty and Progressive Loading

Entrypoints route tasks and state shared authority/uncertainty rules. Move substantial task-specific procedures into named references with precise load conditions; read only selected paths. Do not preload unrelated reference modules or give every subagent the entire workflow.

For missing facts or intent, inspect authoritative context before assuming. Safely deferrable questions stay explicitly pending while independent work proceeds. If a current action or correctness judgment depends on the answer, actively ask the user before that action; a reviewer subagent returns the question to its parent. Never substitute guesses, silence or elapsed time for confirmation.

## Writing

- **Language.** English unless the user explicitly requests another language.
- **Justify token cost.** Only add what the model does not already know. If a line doesn't improve output quality, consistency, or reliability — cut it.
- **Imperative form.** "Analyze the input" not "You should analyze the input."
- **Questions over directives.** "Can an unauthenticated user reach this path?" is more effective than "Check security."
- **Anti-patterns.** List what the model should NOT do — the lazy defaults it would fall into without guidance.
- **Pre-delivery checklist.** Complex skills should end with concrete, verifiable self-checks. Each item must be specific enough to verify by inspecting output ("no placeholder text remaining"), not vague ("ensure quality").

## Portability

- **Portable inputs** — required information must ship with the package, have an explicit public source, or be obtainable through documented configuration on the target machine. Do not assume access to another machine's files, installed packages, or unrecorded history. Declare unavailable prerequisites and their fallback or blocking behavior.
- **No secrets or internal URLs** — no API keys, tokens, credentials, or org-internal hostnames.
- **No machine-specific content** — no absolute paths (`/Users/...`, `C:\...`) or machine-specific env vars. Use placeholders.
- **Platform-agnostic** — do not assume specific tools, MCP servers, or IDE features. Phrase conditionally if unavoidable ("if the Shell tool is available, ...").
- **CommonMark only** — headings, lists, code blocks, tables, links. No HTML, embedded images, or diagram syntax.
- **Skill dependencies are allowed** — declare a concrete stage need, required/optional status, inputs, outputs and missing-dependency behavior; load only when that stage is reached and preserve invocation policy and user authority.
- **Self-contained responsibility** — explain the skill's own contract without hidden conversation context. Prefer capability-based specialist selection at relevant stages instead of fixed skill-name dependencies. Declare the trigger, catalog-based resolution, inputs, outputs, mutation limits and behavior when no specialist fits; missing required capabilities still block dependent actions. Explicit required dependencies must have a concrete justification. Prohibit circular orchestration; a reviewer reports findings rather than delegating back to an executor. Avoid vague instructions such as “see skill X step 3.”
- Within-directory file references are fine. All other references MUST be web URLs — no filesystem paths outside the skill directory. Resolve declared skill dependencies by catalog name rather than sibling filesystem paths.

## Delivery Checks

- [ ] Description distinguishes the intended requests from neighboring skills.
- [ ] Existing supported metadata, invocation policy and authorization remain intact unless their change was requested.
- [ ] Every retained reference has a valid package-local target and a precise loading condition; no unconditional bulk load is introduced.
- [ ] New directories and resources have actual callers; no skill README or unused scaffold is introduced.
- [ ] Material questions are resolved or explicitly deferred; required dependent actions do not rely on guesses.
- [ ] Validation covers the changed contract, including executable behavior when scripts change; report unverified limits.
