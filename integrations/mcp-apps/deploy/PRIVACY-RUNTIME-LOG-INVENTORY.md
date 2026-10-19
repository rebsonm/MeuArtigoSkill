# Meu Artigo — last privacy/retention evidence (no public release authorization)

**Scope:** privacy disclosure evidence for the GitHub Pages site. The project owner confirmed **Rebson de Morais Mendes**, individual publisher and controller for processing under this project, and `rebsonm@gmail.com` as support/privacy inbox. Source-only work is **not** live policy verification.

## VPS — read-only, redacted operator audit

Run `integrations/mcp-apps/scripts/v1-privacy-log-inventory.sh --audit` on the **existing VPS** after retrieving the file from one **exact reviewed GitHub commit SHA**. Save it privately, inspect it, run `bash -n`, then run it as root. Never execute remote contents via `curl | bash`, and do not pass any bearer token, Auth0 client secret, researcher details, journal log events or `systemctl show -p Environment` output.

The script prints only allowlisted service-state classes, whether systemd stdout is journal/file/null, whether the existing V1 Nginx site file has an `access_log off` declaration, and sanitized `journald` configuration values such as `MaxRetentionSec` and size limits. The inventory is **read only**, does not change any service, file or provider settings, and does not print log events, private file paths or tokens. Output can be pasted in a support conversation after review.

**Interpretation limits:** `access_log off` at one site declaration is not proof of effective Nginx logging across includes/locations. `journald MaxRetentionSec=0` or a missing setting does **not** mean “zero retention” or “never retained”: disk quotas/rotation may still apply. A default or unset setting does not supply a factual number of days. Service availability and logs from other providers cannot be established by this script.

## Auth0 — tenant-specific evidence from the administrator

Auth0 retention depends on the effective paid/free plan. Auth0's public pricing identifies retention tiers of 1, 5, 10 and 30 days; **do not assume which one is active for this tenant**. Sign into your own authorized Auth0 dashboard and record only the plan tier and whether any Log Streams are enabled. Never export events, user emails, account IDs, settings containing secrets or bearer tokens. Provider documentation: https://auth0.com/pricing and https://support.auth0.com/center/s/article/retrieving-logs-after-auth0-retention-period-has-expired .

A Log Stream, if enabled, can forward event data to a destination with its **own** retention policy. This must be reviewed separately before public privacy promises.

## Final policy decision and publication gate

The site privacy page must accurately distinguish (1) no centrally stored research manuscripts in the display-only MCP, (2) transient per-request display projection, (3) possible infrastructure logs, and (4) Auth0 identity/logging and its confirmed retention plan. Record the legal basis per processing purpose, responsible contact, subprocessors and rights response, and obtain the publisher's express approval of final text. Only then remove DRAFT/noindex safeguards, integrate reviewed source into `main`, and run the existing **manual** GitHub Pages workflow. A CI-green candidate does **not** authorize publishing legal policies. Later tests with a separate consenting researcher remain mandatory before public Plugin acceptance, but are not needed to inventory VPS log configuration.
