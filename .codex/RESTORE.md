# Merge a Codex Environment

Use this guide to supplement an existing environment or initialize a new one. Install missing skills and update existing skill files while preserving target-only content. Merge instructions and configuration without replacing entire files or directories. This directory is a configuration bundle, not a replacement for the Codex user directory.

## Start here

Transfer the complete repository, including skills/, to the target computer. Install and sign in to Codex, open the repository, and ask:

> Read .codex/RESTORE.md and merge this repository's environment into my local environment. Install or update the listed skills without deleting target-only files or replacing whole directories. Preserve local instruction rules, configuration values, plugins and connections. Report changes, conflicts, backups and verification results.

The base merge includes global instructions, reviewed configuration defaults and the skills listed in environment-inventory.json. Restore plugins and service connections only when separately requested. Credentials and application state are excluded.

## Merge contract

| Target | Add when missing | When already present |
|---|---|---|
| Skill package | Install the complete reviewed package | Update matching files and add missing files; retain target-only files |
| Global instructions | Add rules whose meaning is absent locally | Preserve local rules; skip equivalents and report conflicts |
| Configuration | Add reviewed missing keys and compatible tables | Preserve all existing values, including false, empty values and disabled settings |
| Plugin or connection | Add missing requested capabilities | Preserve installation, enabled state, settings and authentication |

Broken or unreadable targets, dangling symlinks, incompatible TOML structures and uncertain instruction conflicts are unresolved items, not missing items. Report them and continue independent work. Do not replace them or write through symlinks automatically. Skill updates are part of the default restore scope. Whole-directory or whole-file replacement that discards unrelated local content is not. Repeated runs with identical inputs must produce no changes or duplicate rules. Deleting target-only files requires an explicit request.

## 1. Inspect and plan

- Identify the supplied repository and target Codex home (CODEX_HOME, default ~/.codex). User skills normally go under ~/.agents/skills; inspect the actual catalog and discovery locations before deciding a skill is missing. A same-name skill in another active location is still an existing skill. Check declared skill names as well as folder names.
- Read local AGENTS.md and AGENTS.override.md, when present, and inspect existing configuration. An override can prevent ordinary global AGENTS.md from taking effect; preserve it and merge applicable missing guidance into the effective global instruction file instead. Report any limits on activation.
- Read the skills list in environment-inventory.json. Each entry declares a name and source repository; an optional path locates a package in the supplied checkout. Paths are relative to the repository root. The inventory excludes versions, digests, plugins and Lark CLI skills.
- Review model/provider availability and preserve local execution permissions. config.template.toml contains captured preferences, including approval_policy = "never" and sandbox_mode = "danger-full-access"; apply missing settings only after reviewing suitability.
- Identify missing items, equivalent existing items, conflicts and unavailable items. Preserve unrelated skills, old rule links, application-managed MCP wiring, notification paths, trust settings, credentials, history, databases and caches.

## 2. Install, update and merge

Keep an installation record outside this repository and skill discovery paths. Record added and updated paths, before/after content identities, target-only files retained, added instruction rules, added configuration keys, and skipped/conflicting items. Before editing an existing regular file, save its original contents in a codex-backup.* directory under the target Codex home and record the backup location. A merge with no existing-file edits needs no backup directory.

### Skills

Include every skills entry in the default merge, whether missing or already installed. Inspect the active catalog to locate existing same-name packages, including packages installed in another discovery location; update the existing installation rather than creating a duplicate. Resolve ambiguous multiple installations before dependent writes.

Select the source as follows:

- When source is whhe/codex-workbench and the declared path contains a complete local package whose SKILL.md name matches the entry, use that package from the supplied checkout, including uncommitted changes for local validation. Report that this uses the checkout rather than the published release.
- Otherwise retrieve the latest available package from source, resolving its location by the declared skill name. A missing local package may use this online fallback; an unreadable, incomplete or name-mismatched local package is a conflict to report before selecting another version. If retrieval is unavailable, leave the installed version intact and report the update as unavailable.

Prepare each selected source package as a complete directory in task-owned staging outside skill discovery paths, and verify it before modifying the installation. Compare source and target files, then apply a file-level merge:

- Add source files absent from the target; overwrite matching regular files whose contents differ after backing up their original contents. An ordinary same-path difference is an authorized update, not a reason to skip an existing skill.
- Retain files and directories present only in the target, even if absent from the selected source. Report retained differences that may affect behavior; do not claim an exact version match when such differences remain.
- Skip identical files. Do not empty, delete or replace the target directory, use deletion-based synchronization, or recursively copy through unresolved symlinks. File/directory type conflicts and ambiguous installation ownership require investigation before affected writes. For a recognized installer-managed link, use its supported update mechanism only if it preserves target-only content; otherwise report the limitation.
- Recheck target identities before each update to avoid overwriting concurrent edits. Write each file atomically where supported. If an update fails, restore task-updated files from backups and remove only unchanged task-created additions; preserve intervening edits and report any partial or uncertain state. A source-preparation failure leaves the installation untouched.

Record selected sources and installation metadata needed for future updates and rollback in the external installation record. Keep version and digest observations out of the inventory. Apply the same merge rules to local and downloaded packages; a newer source does not authorize deletion of target-only content.

### Global instructions

Install or confirm required skills before adding instruction rules that depend on them. If a required package is unavailable, defer only its dependent additions and report them; preserve pre-existing local instructions. Treat this repository's .codex/AGENTS.md as a template during preparation, not as instructions to activate before dependencies exist.

For a missing effective global instruction file, install its reviewed applicable rules. For an existing file, compare rules by meaning: retain its contents and add only non-conflicting missing guidance in an appropriate Markdown section. Do not concatenate the whole template or duplicate equivalent rules. Local choices prevail over template defaults. Report skipped conflicts, including incompatible workflow routing, rather than adding rules that contradict or override local guidance.

### Configuration

For a missing config.toml, create it from the reviewed template. For an existing file, merge only missing reviewed keys by their full TOML path. Preserve existing values, unrelated tables, comments and application-managed settings. A value is not missing merely because it differs from the template. Validate TOML after editing and verify every pre-existing setting retains its value. Where a structure conflicts or the file cannot be safely read and edited, leave affected content unchanged and report it.

### Integrations

Plugins and connections are not inventoried here. Restore them only when separately requested, through supported interfaces and local authentication. Preserve locally disabled plugins and existing connections; report pending sign-ins or unavailable product support.

## 3. Verify and report

Verify that all selected source files were installed or updated as planned and target-only files remain unchanged. Verify configuration values and unrelated files are unchanged except for recorded instruction/configuration additions. Check backups and installed file identities, validate configuration, and check added instructions for duplication and conflicts.

Separate file-level checks from runtime checks. Once file checks pass, ask the user to restart Codex and open a new chat for activation checks; do not close their running application automatically. Until those checks are observed, report "files merged; runtime verification pending" and provide this handoff prompt:

> Verify the merged global instructions and skill discovery. Check the requested model and, for installed or updated coding-workflow, specialist selection and independent subagent capability without editing a real project. Report verified items, preserved local differences and anything still untested.

Verify integrations separately only when requested. Copying files does not establish working authentication or connectivity. If a preserved local workflow differs, report that difference instead of replacing it to satisfy the template.

Report added and updated items, retained target-only files, preserved settings, skipped conflicts, missing packages, deferred instruction additions, verification results, pending sign-ins and installation record/backup locations. Claim completion only for the requested scope and checks actually observed. Repeating the merge with unchanged inputs should propose no duplicate additions. Do not retire old skills or Cursor rule links during this merge.

## Undo this merge

Use the installation record to undo only this task's changes. Restore each updated file from its backup only if its current identity still matches the task's recorded result; preserve subsequent edits and report conflicts. Remove task-created files only when they remain unchanged. Retain all pre-existing target-only files, unrelated packages, configuration values, plugins and connections. Never delete an entire skill or configuration directory to undo a file-level merge.
