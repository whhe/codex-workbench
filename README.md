# Codex Workbench

Reusable skills for everyday coding work, plus a portable bundle of my personal Codex environment. Use a skill on its own, or ask Codex to help bring the full setup to another computer.

## Skills

| Skill | What it helps with |
|---|---|
| [code-review](skills/code-review/SKILL.md) | Review code read-only, or request fixes through the coding workflow |
| [coding-workflow](skills/coding-workflow/SKILL.md) | Implement features, debug problems, verify changes and handle Git or PR/MR work |
| [design-review](skills/design-review/SKILL.md) | Clarify design choices, develop proposals and challenge them through independent subagent reviews |
| [skill-conventions](skills/skill-conventions/SKILL.md) | Create and maintain clear, reusable skill packages |

## Install a skill

With Node.js and npm installed, run the command for the skill you want. Each command installs one skill globally for Codex using [Skills CLI](https://github.com/vercel-labs/skills):

```sh
npx skills add whhe/codex-workbench --skill code-review --global --agent codex
npx skills add whhe/codex-workbench --skill coding-workflow --global --agent codex
npx skills add whhe/codex-workbench --skill design-review --global --agent codex
npx skills add whhe/codex-workbench --skill skill-conventions --global --agent codex
```

Start a new Codex chat and try:

> Use $code-review to review this project and report the problems you find.

Or:

> Use $code-review to review and fix the current changes.

Or:

> Use $coding-workflow to implement the agreed solution.

Or:

> Use $design-review to propose an approach for this feature.

For a deeper design discussion:

> Use $design-review to question the important design choices first, then propose and independently review an approach.

Proposal and implementation requests include independent review/revision loops by default. `code-review` stays read-only unless you ask for fixes; its fix path requires `coding-workflow`.

Installing a skill does not apply my personal environment settings. If installation or discovery fails, ask Codex to inspect the setup and explain what is missing. `coding-workflow` and `design-review` need subagent support for their independent reviews; ask Codex to check compatibility before relying on them.

## Bring the environment to another computer

Download or clone the complete repository, including hidden files, and open it in Codex. Ask:

> Read .codex/RESTORE.md and merge this environment into my local setup. Install or update the skills while keeping local-only files and settings. Report changes, conflicts and verification results.

Codex follows the [merge guide](.codex/RESTORE.md) and handles the detailed checks, backups and installation steps. Follow its handoff if a restart or sign-in is needed. Credentials, chat history and machine-specific state are excluded; models and integrations may need separate setup.

## Check or troubleshoot

Open this repository in Codex and ask:

> Check the installed skills and their requirements. Run the relevant runtime tests where supported, and distinguish script test results from skill discovery and actual task behavior. Report anything still unverified.

## License

[MIT](LICENSE) © He Wang
