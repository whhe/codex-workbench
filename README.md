# Codex Workbench

Reusable skills for everyday coding work, plus a portable bundle of my personal Codex environment. Use a skill on its own, or ask Codex to help bring the full setup to another computer.

## Skills

| Skill | What it helps with |
|---|---|
| [code-review](skills/code-review/SKILL.md) | Review code and report concrete problems with supporting evidence |
| [coding-workflow](skills/coding-workflow/SKILL.md) | Implement features, debug problems, verify changes and handle Git or PR/MR work |
| [skill-conventions](skills/skill-conventions/SKILL.md) | Create and maintain clear, reusable skill packages |

## Install a skill

With Node.js and npm installed, run the command for the skill you want. Each command installs one skill globally for Codex using [Skills CLI](https://github.com/vercel-labs/skills):

```sh
npx skills add whhe/codex-workbench --skill code-review --global --agent codex
npx skills add whhe/codex-workbench --skill coding-workflow --global --agent codex
npx skills add whhe/codex-workbench --skill skill-conventions --global --agent codex
```

Start a new Codex chat and try:

> Use $code-review to review this project and report the problems you find.

Or:

> Use $coding-workflow to review this project, fix the problems found and verify the result.

Installing a skill does not apply my personal environment settings. If installation or discovery fails, ask Codex to inspect the setup and explain what is missing. `coding-workflow` needs subagent support for its independent reviews; ask Codex to check compatibility before relying on it.

## Bring the environment to another computer

Download or clone the complete repository, including hidden files, and open it in Codex. Ask:

> Read .codex/RESTORE.md and merge this environment into my local setup. Install or update the skills while keeping local-only files and settings. Report changes, conflicts and verification results.

Codex follows the [merge guide](.codex/RESTORE.md) and handles the detailed checks, backups and installation steps. Follow its handoff if a restart or sign-in is needed. Credentials, chat history and machine-specific state are excluded; models and integrations may need separate setup.

## Check or troubleshoot

Open this repository in Codex and ask:

> Check the installed skills and their requirements. Run the relevant runtime tests where supported, and distinguish script test results from skill discovery and actual task behavior. Report anything still unverified.

## License

[MIT](LICENSE) © He Wang
