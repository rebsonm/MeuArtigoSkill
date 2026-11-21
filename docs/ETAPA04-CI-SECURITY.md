# Stage 04 — isolated CI/security candidate

Pinned main: `5c7bf4ff599d73a660bb709616a689140b2edbe7`

Scope: supply-chain gating, tracked-file secrets audit, existing #76 bridge tests, and CodeQL JS/TS coverage when MCP Apps source enters the candidate tree.

- No OAuth/Drive/production access. No merges or deployment.
- Python and GitHub Actions CodeQL remain under GitHub's existing default setup. This branch adds only JS/TS CodeQL, avoiding duplicate Python/Actions scan configurations. Ensure repository code scanning settings admit that job.
- npm: any optional MCP Apps `package.json` MUST have `package-lock.json`. Use Node 22/npm 10 to create it from the exact reviewed #74/#75 manifest before incorporation. Validate with `npm ci --ignore-scripts --no-audit --no-fund`, production `npm audit --omit=dev --audit-level=high`, then explicit bundle and smoke. No `npm install` fallback in CI.
- The current `main` does not contain `integrations/mcp-apps`, so npm install, npm audit, actual OAuth and JS CodeQL cannot be positively certified by running this branch alone. They must be re-run against candidate integration after #74 and #75.
- The scanner is limited to tracked working-tree files and high-confidence regexes; it does not check git history, GitHub repository secrets, or encrypted binary content. Enable GitHub secret scanning/push protection independently if available.
- No creation of an empty/fake Node lock. A lock must be generated from registry-resolved versions, verified, committed, and reviewed with the MCP Apps feature branch. This candidate will fail closed if a future feature PR adds a manifest without a lock.
- Existing local bridge source should stay identical to main; `tests/test_local_research_bridge.py` confirms private launch URL remains in 0600 transient file and cannot appear in process output.
- Required evidence: CI run for this branch SHA; CodeQL JS result on a branch that actually contains JS/TS; Node lock hash and `npm ci` evidence. No real security certificate or OAuth acceptance is asserted.
