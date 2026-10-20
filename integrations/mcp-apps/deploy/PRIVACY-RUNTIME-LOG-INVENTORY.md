# Meu Artigo — last privacy/retention evidence (no public release authorization)

**Scope:** privacy disclosure evidence for the GitHub Pages site. The project owner confirmed **Rebson de Morais Mendes**, individual publisher and controller for processing under this project, and `rebsonm@gmail.com` as support/privacy inbox. Source-only work is **not** live policy verification.

## VPS — read-only, redacted operator audit

Run `integrations/mcp-apps/scripts/v1-privacy-log-inventory.sh --audit` on the **existing VPS** after retrieving the file from one **exact reviewed GitHub commit SHA**. Save it privately, inspect it, run `bash -n`, then run it as root. Never execute remote contents via `curl | bash`, and do not pass any bearer token, Auth0 client secret, researcher details, journal log events or `systemctl show -p Environment` output.

The script prints only allowlisted service-state classes, whether systemd stdout is journal/file/null, whether the existing V1 Nginx site file has an `access_log off` declaration, and sanitized `journald` configuration values such as `MaxRetentionSec` and size limits. The inventory is **read only**, does not change any service, file or provider settings, and does not print log events, private file paths or tokens. Output can be pasted in a support conversation after review.

**Interpretation limits:** `access_log off` at one site declaration is not proof of effective Nginx logging across includes/locations. `journald MaxRetentionSec=0` or a missing setting does **not** mean “zero retention” or “never retained”: disk quotas/rotation may still apply. A default or unset setting does not supply a factual number of days. Service availability and logs from other providers cannot be established by this script.

## Read-only VPS audit observed on 19 October 2026

The owner executed the pinned script from GitHub commit `ddd75040ff23db97aa258f079dbdc83919e4662f` in their VPS via SSH. The script finished with `V1_PRIVACY_INVENTORY_END=PASS_READ_ONLY` and `V1_PRIVACY_INVENTORY_WRITES=NONE`. Redacted result categories (no network addresses, identities, documents or logs):

| Field | Actual result | Interpretation |
| --- | --- | --- |
| V1, legacy and E05 services | `active`, all `STDOUT=JOURNAL` | Operational stdout uses systemd journal; not zero logging |
| Existing Nginx site | `FOUND` and `ACCESS_LOG=OFF_DIRECTIVE_PRESENT` | An `access_log off` declaration exists; no full effective-config proof |
| Nginx error log | `INHERITED_OR_UNVERIFIED` | Error-log policy remains unverified |
| Nginx effective logging | `REQUIRES_FULL_CONFIG_REVIEW` | Do not claim full disablement of logs |
| `journald` | `Storage`, `MaxRetentionSec`, `SystemMaxUse`, `RuntimeMaxUse`, `SystemKeepFree`, `RuntimeKeepFree` all `INHERITED_OR_DEFAULT` | No numerical retention established |
| Auth0 | `LOG_RETENTION=NOT_VERIFIED_CHECK_TENANT_PLAN`, `LOG_STREAMS=NOT_VERIFIED_CHECK_AUTH0_DASHBOARD` | Still requires provider tenant check |

**Evidence conclusion:** Read-only VPS inspection = PASS. Actual effective time-to-delete logs = NOT_VERIFIED. Avoid claiming no logs or a fixed retention time. No source document, log event or bearer data was read or printed.

## Auth0 — dashboard evidence observed on 19 October 2026

The owner supplied a screenshot of **Monitoring → Log Streams**, whose notice reads: "This feature is not available for free plans. To configure a log stream, please upgrade your account to any paid plan." **No configured Log Streams were visible in that screenshot.** This supports a **Free-plan indication**, and proves neither the creation of an external stream nor provider-wide absence of authentication logs. A separate **Settings → Subscription** confirmation was not supplied; record the effective tenant subscription as *Free-indicated, not independently confirmed*.

The provider's current [Auth0 Pricing](https://auth0.com/pt/pricing) shows **Log Retention: 1 Day (Free), 5 Days (Essentials), 10 Days (Professional), 30 Days (Enterprise)** and no Log Streaming entitlement for Free. Accordingly **1 day is the provider's published Free-tier retention, conditional on the tenant actually using that tier**, not an independently measured deletion test. Auth0's [expired-log policy](https://support.auth0.com/center/s/article/retrieving-logs-after-auth0-retention-period-has-expired) describes expiration after the applicable retention window.

There is **no evidence of active Auth0 Log Streams** in the screenshot. This does not rule out operational logs held by ChatGPT, the VPS, third parties, or other independent logging mechanisms. Do not inspect or share user events, tokens, emails or credentials. For formal legal approval, verify the current subscription in the Auth0 tenant and review relevant subprocessors, cross-border transfer and retention policies separately.

## Final policy decision and publication gate

The site privacy page must accurately distinguish (1) no centrally stored research manuscripts in the display-only MCP, (2) transient per-request display projection, (3) possible infrastructure logs, and (4) Auth0 identity/logging and its confirmed retention plan. Record the legal basis per processing purpose, responsible contact, subprocessors and rights response, and obtain the publisher's express approval of final text. Only then remove DRAFT/noindex safeguards, integrate reviewed source into `main`, and run the existing **manual** GitHub Pages workflow. A CI-green candidate does **not** authorize publishing legal policies. Later tests with a separate consenting researcher remain mandatory before public Plugin acceptance, but are not needed to inventory VPS log configuration.
