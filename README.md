# Codex Workbench

Reusable skills for coding work and evidence-based problem analysis, plus a portable bundle of my personal Codex environment. Use a skill on its own, or ask Codex to help bring the full setup to another computer.

## Skills

| Skill | What it helps with |
|---|---|
| [code-review](skills/code-review/SKILL.md) | Review code read-only, or request fixes through the coding workflow |
| [coding-workflow](skills/coding-workflow/SKILL.md) | Make and verify authorized changes, debug problems and handle Git or PR/MR work |
| [implementation-design](skills/implementation-design/SKILL.md) | Produce or assess a software design that gives developers enough information to implement it |
| [problem-analysis](skills/problem-analysis/SKILL.md) | Discuss open-ended questions, diagnose uncertain causes and recommend directions or decision criteria |
| [skill-conventions](skills/skill-conventions/SKILL.md) | Create and maintain clear, reusable skill packages |
| [technical-writing](skills/technical-writing/SKILL.md) | Create or revise a standalone technical document, such as a Markdown file or Feishu Doc |

## Install a skill

With Node.js and npm installed, run the command for the skill you want. Each command installs one skill globally for Codex using [Skills CLI](https://github.com/vercel-labs/skills):

```sh
npx skills add whhe/codex-workbench --skill code-review --global --agent codex
npx skills add whhe/codex-workbench --skill coding-workflow --global --agent codex
npx skills add whhe/codex-workbench --skill implementation-design --global --agent codex
npx skills add whhe/codex-workbench --skill problem-analysis --global --agent codex
npx skills add whhe/codex-workbench --skill skill-conventions --global --agent codex
npx skills add whhe/codex-workbench --skill technical-writing --global --agent codex
```

Start a new Codex chat and try:

> Use $code-review to review this project and report the problems you find.

Or:

> Use $code-review to review and fix the current changes.

Or:

> Use $coding-workflow to implement the approved agent-platform queue design and verify tenant isolation.

Or:

> Use $implementation-design to design tenant-isolated agent job queues for this codebase. Return the independently reviewed proposal in this chat with the components, interfaces, implementation sequence, and acceptance checks the developer will need.

For a deeper design discussion:

> Use $implementation-design to question the important design choices first, then propose and independently review an approach.

For an open-ended engineering or business question:

> What does an enterprise agent platform need to get right, and which requirements depend on our organization?

> Signup completion dropped from 8% to 5% after we changed tracking. What evidence would help us tell whether fewer people completed signup?

To deliver technical content as a document:

> Save the agreed queue design to `docs/queue-design.md` for the developers who will implement it.

When a request combines analysis or design with a document, start with the analysis or design. Use `technical-writing` to deliver the resulting proposal, draft, or assessment at the requested destination.

`implementation-design` independently reviews the proposals it develops. `coding-workflow` independently reviews authorized file changes. An assessment of an existing design or code change is read-only by default. For code fixes requested during a review, `code-review` uses `coding-workflow`.

`technical-writing` uses `research` when requested or when required source evidence is missing, `humanizer` for the prose pass, and `grilling` for material owner questions. It also requires independent subagents before final delivery. Missing capabilities leave the dependent stage incomplete.

Installing a skill does not apply my personal environment settings. If installation or discovery fails, ask Codex to inspect the setup and explain what is missing. `coding-workflow` and `implementation-design` need subagent support for their independent reviews; ask Codex to check compatibility before relying on them.

## Bring the environment to another computer

Download or clone the complete repository, including hidden files, and open it in Codex. Ask:

> Read .codex/RESTORE.md and merge this environment into my local setup. Install or update the skills while keeping local-only files and settings. Report changes, conflicts and verification results.

Codex follows the [merge guide](.codex/RESTORE.md) and handles the detailed checks, backups and installation steps. Follow its handoff if a restart or sign-in is needed. Credentials, chat history and machine-specific state are excluded; models and integrations may need separate setup.

## Check or troubleshoot

Open this repository in Codex and ask:

> Check the installed skills and their requirements. Run the relevant runtime tests where supported, and distinguish script test results from skill discovery and actual task behavior. Report anything still unverified.

## License

[MIT](LICENSE) © He Wang
