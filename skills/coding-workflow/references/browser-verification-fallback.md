# Browser Verification Fallback

Use this ladder when the preferred browser session is unavailable. Do not close a user's browser or alter their profile without explicit authorization.

1. **Isolated managed session**: use a separate temporary browser session/profile.
2. **Temporary local profile**: launch a disposable Chromium profile for the local artifact.
3. **Playwright/CDP DOM run**: load the page and exercise selectors/events without relying on the user's profile.
4. **Static state-flow runner**: execute pure transition functions and inspect before/after state when the UI cannot run.
5. **Manual handoff**: provide the URL/path and a bounded click script for human execution.

Record every rung attempted and its result. If all fail, mark `browser: blocked` and list the unverified interactions. Never promote a blocked GUI check to passed because static checks succeeded.

Minimum fallback coverage:

- open/close one dialog;
- submit valid and invalid semantic input;
- confirm one state-changing action;
- inspect the resulting state on every affected work surface;
- refresh/restart if persistence is claimed;
- capture console errors or runtime exceptions when a browser runner is available.
