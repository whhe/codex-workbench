# Upstream Project Resolution

Remote names (`origin`, `upstream`, `fork`, etc.) are only hints — never assume a specific name maps to the true upstream. Apply this decision order:

1. If the user gave an explicit issue, PR, or MR URL, or a provider-qualified project path such as GitHub `owner/repo` or GitLab `group/subgroup/project`, use it directly. Derive the host, provider, namespace, and project path from the URL when needed.
2. List all configured remotes (`git remote -v`) and normalize each URL to its host, provider, namespace, and project path. Remote names (`origin`, `upstream`, `fork`) are only hints.
3. If more than one candidate remains, use the matching provider CLI/API identity when available to identify a fork or namespace relationship. Never guess identity from environment variables or remote names alone.
4. Pick the upstream by evidence:
   - **1 remote** → use it as upstream.
   - **2 remotes** → use the provider-authenticated fork heuristic only when exactly one remote is clearly the current user's fork; otherwise present both candidates and ask which is upstream.
   - **≥3 remotes** → present candidates and ask which is upstream.
5. Record the chosen provider, host, namespace/project path, and use that target for all subsequent steps. Select `gh` for GitHub, `glab` for GitLab, or another available provider API/tool as appropriate.
