# Project Configuration and Execution Environment

Load this module only for relevant project setup, Python execution, environment configuration or scaffolding. It does not authorize unrelated installation, Git operations or publication. Follow global execution limits, including the local Docker-test restriction.

## Python Environment

Prefer an existing repository-local .venv or venv. Activate it before running Python commands or explicitly invoke that environment's interpreter. Do not use system Python for project execution, recreate an existing environment, or alter an unrelated environment. If no suitable environment exists and execution is needed, create an appropriate local virtual environment within scope; report unavailable prerequisites.

## Environment Variables

Keep environment-specific values in .env rather than hardcoding them; use the project's existing loader, such as python-dotenv or dotenv. Provide a non-secret .env.example and ensure .env is ignored by Git. Preserve established project configuration and dependency conventions; introduce a new loader only when needed.

## New Project Scaffolding

Only when creating a project from scratch within the user's request, initialize Git if needed, add stack-appropriate ignore rules including .env, and provide the formatter/configuration appropriate to that project. Prepare the initial attributable commit under git-operations.md and the precommit-review.md gate for code changes. Scaffolding does not waive user limits such as do-not-commit or local-only and does not authorize a remote push to an unverified target.
