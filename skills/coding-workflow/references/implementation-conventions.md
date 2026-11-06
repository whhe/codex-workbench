# Implementation Conventions

## Simplicity First

- **Minimum code that solves the problem.** No speculative features, abstractions for single-use code, or "flexibility" that wasn't requested.
- No error handling for impossible scenarios. If 200 lines could be 50, rewrite.
- Ask: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## Surgical Changes

- **Minimize the diff** — no unrelated reformatting, reordering, or renaming. Auto-format **only changed files**.
- Don't "improve" adjacent code, comments, or formatting. Match existing style, even if you'd do it differently.
- If you notice unrelated issues, **mention them — don't fix them** unless asked.
- Remove imports/variables/functions that **your changes** made unused. Don't remove pre-existing dead code unless asked.
- **Litmus test:** every changed line should trace directly to the user's request.

## Documentation and User-Facing Text

- Update the documentation, configuration and routing affected by the change; preserve unrelated material.
- When changing user-facing text, follow the project's existing i18n/localization mechanism and update relevant locales together. This applies across implementation languages; do not introduce a new localization system merely to satisfy this convention.

## Style & Formatting

- Write all **code comments** in English. (Conversational responses follow the user's language preference.)
- Class/function-level: describe purpose and contract. Inline: explain **why**, not what. (Bad: `Loop users` | Good: `Adults only per policy §4.2`)
- **No end-of-line comments.** Place comments on a separate line above the relevant code.
- **End files with a newline** (POSIX standard).

## Code Quality

- Keep environment-specific values in configuration. Extract shared business constants when it improves clarity; introduce dependencies or abstractions only for a concrete need.
- Ensure naming, defaults, return values, and state semantics stay consistent with the existing codebase.
- New logic should reuse existing abstractions rather than branching with ad-hoc if/else.
- Errors, logs, and messages must be sufficient for debugging; never swallow exceptions or log misleading info.
- New deps must be justified. Lock files and config changes must match actual code usage.

## Python

- Annotate all new/modified function signatures. Avoid bare `dict`, `list`, `Any` when a concrete type or `TypedDict` is viable.
- Handle `None` explicitly; prefer `x is None` / `x is not None` over `== None`.
- Catch the narrowest exception type. Never `except Exception` to silence errors. Do not mix data/auth/network errors into one handler.
- Re-raise or wrap with context (`raise ... from e`) rather than swallowing.
- Use `with` / `async with` for files, HTTP clients, DB connections, and locks.
- Flag `verify=False`, unbounded retries, open-ended polling, and blocking `time.sleep` in async code as high-risk.
- Never call blocking I/O inside `async def` — use `asyncio.to_thread` or an async-native library.
- Verify `await` is not missing on coroutine calls. In event-loop frameworks (FastAPI, aiohttp), treat any synchronous network call as a bug.
- Always use timezone-aware datetimes (`datetime.now(tz=UTC)`). Never mix naive and aware objects.
- Watch for N+1 queries, repeated full-table scans, and redundant I/O inside loops. Prefer batch operations.
- Serialize ORM objects to dicts/Pydantic models **inside** the session scope. Preload relationships with `selectinload` / `joinedload`.

## TypeScript / JavaScript

- Avoid excessive `any` and unsafe type assertions. New enums/config must stay consistent with consumer-side types.
- Follow the project's existing i18n mechanism for user-visible text and update applicable locales together. Introduce i18n infrastructure only when the task requires it.
- Data source forms, options, and mappings should follow the project's existing config patterns. No scattered hardcoding.
- Verify `useEffect` / `useState` dependencies are correct. Avoid unnecessary re-renders and state drift.
- Patches and polyfills should only activate under necessary conditions. Do not pollute globals or break other runtime versions.

## Testing

- When inspection and existing evidence establish no relevant uncovered risk, add no test code; state the reason and use proportionate existing checks. A small diff alone does not establish absence of risk.
- Choose verification in proportion to the behavior's risk and the project's existing coverage. Do not treat TDD or test count as a goal by itself.
- Add or update a test when it protects a changed observable contract, reproduces a bug that the current suite misses, or guards a high-risk boundary. A single discriminating test can be enough; do not require a happy-path and edge-case pair by default.
- Before adding a test, check whether an existing test already proves the behavior and extend it instead of duplicating coverage. Do not add tests for documentation, configuration-only, wiring-only, or behavior-preserving refactors unless they expose a real unverified risk.
- Assert observable outcomes, not implementation details or coverage percentages. If a test would not fail for a plausible regression, do not add it. Update tests when a changed contract makes their expectation obsolete; remove them only when they exclusively cover removed behavior. Preserve shared coverage.
- Follow the project's test naming and fixture conventions; keep sessions, temporary files, and mocks isolated between tests.
