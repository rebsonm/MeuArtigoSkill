# Immediate improvements — implementation and acceptance matrix

**Review date:** 2026-10-14 (Brazil). **Tracking:** draft PR #65, branch
feat/immediate-radar-controls-2026-10-14. **Published beta:** v0.9.0-beta.5,
unchanged. This matrix describes the SOURCE BRANCH, not a released feature
set or independently validated scientific system.

## Status snapshot

- **Initial engineering slices:** 8 of 8 present.
- **Fully accepted improvements:** 0 of 8. Every item remains PARTIAL.
- **Observed research-grade case runs:** not demonstrated by this PR.
  Synthetic software unit tests are not equivalent to independent
  observations of model behavior in an actual study.
- **Last tested functional baseline:** d302dabf96896f094da7bfd812c46e3072f650d4
  (case-registry, metadata-calibration and release audit: SUCCESS).
- **Release readiness:** NOT READY. Keep PR in draft; no merge, installed
  extension changes, distribution or release without explicit authorization.
- **Interpretation:** checked PR checklist items denote FIRST SLICES, not full
  acceptance. Do not translate 8/8 implemented slices into 100% completion.

## Acceptance matrix

| Order | Radar ID | State | Implemented in this draft PR | Unfinished work / acceptance evidence |
| --- | --- | --- | --- | --- |
| 1 | CAS-003 | PARTIAL — catalog only | Twelve frozen, explicitly SYNTHETIC adversarial cases in benchmarks/critical_cases_v1.json, with expected defensive actions. | Run the real controls against frozen case inputs; record observed outputs, missed detections, false alarms and exact software configuration. Do not call a case definition a passed test. |
| 2 | REG-001 | PARTIAL — recorder usable | scripts/evaluation_registry.py: JSONL append-only records, chained SHA-256, source commit, catalog digest, explicit NOT_EVALUATED outcomes and same-catalog comparisons. | Add a real execution adapter; collect referenced raw observations; verify source artifacts independently and preregister comparison rules. A chained local file is not an authenticated independent record. |
| 3 | REG-018 | PARTIAL — canonical audit usable | scripts/reference_audit.py reconciles Evidence_ID and Claim_ID references, DOI syntax/collisions, source verification state, correction and retraction alerts. | Parse and reconcile in-text citations and bibliography of the authorized final manuscript; inspect real manuscripts and adjudicate false positives, records without DOIs and provider failures. |
| 4 | REG-011 | PARTIAL — human-assisted protocol usable | scripts/semantic_claim_review.py binds claims, quoted passages, file SHA, source report and declared human judgment of scope, method, context, limits and counterevidence. | Test substantive support and extrapolation with controlled independent/blinded assessments; validate disagreements and reviewer provenance. A literal quote match or declared reviewer is NOT automated semantic proof. |
| 5 | REG-013 | PARTIAL — technical diagnostic usable | scripts/scientific_diagnostic.py consolidates coded reference/claim/protocol alerts, counts, source hashes and next actions in compact Markdown, A4-oriented HTML and JSON. | Demonstrate one physical/printed page across supported environments; conduct real researcher usability checks; audit diagnostic omissions and false positives. Methodological adequacy is not assessed substantively. |
| 6 | REG-017 | PARTIAL — integrated read-only panel usable | scripts/native_chat_dashboard.py embeds REG-013/018/011 findings into its existing Evidence view. MINIMAL/FULL preserve identical counts; missing values remain unknown. | Test the native host with a real authorized project; obtain and verify actual Google Drive write receipts before asserting sync. The standalone browser demo is a SYNTHETIC UI simulation, not validation of a connected host. |
| 7 | REG-019 | PARTIAL — privacy-reduced replay usable | scripts/evaluation_package.py builds/verifies a deterministic checksummed ZIP of frozen synthetic cases, protocol, optional protocol digest and REDACTED self-reported REG-001 observations; scoring is recalculated. | Conduct authorized third-party replay with actual source/evidence access, human rights/privacy review, complete run configuration and independent reviewer checks. The redacted archive cannot prove original evidence or fully revalidate the raw ledger chain. |
| 8 | ENG-022 | PARTIAL — CI discipline started | Pin-based offline CI, adversarial unit regressions, source-language check, public privacy checks, and full release audit run on the draft PR. | Carry out independent review of later commits, security/privacy acceptance checks, real reproducibility exercises and explicit release readiness assessment. Passing CI alone does not establish scientific performance. |

## Recommended close-out sequence

1. **Evidence before inference:** build executable scenario adapters for
   CAS-003 and connect actual results to REG-001. Freeze case definitions,
   model configuration and run conditions first.
2. **Substantive source controls:** complete manuscript-level REG-018 audit
   and REG-011 independent assessment design; explicitly measure errors,
   undetected overclaims, uncertainty and contradictory evidence.
3. **Researcher experience:** evaluate REG-013 readability and REG-017
   on a real permitted project; preserve the existing human gates. Verify
   any remote write with an actual external receipt.
4. **Research-grade replication:** extend REG-019 only with separately
   authorized protocol, source artifacts and independently inspected
   observed outputs; do not publish confidential evidence by default.
5. **Across all stages:** maintain ENG-022 adversarial regressions and the
   three automated checks, without relaxing public-release boundaries.

## Acceptance definition

An item is DONE only when its remaining work above is implemented, tested
on inputs that legitimately support the claim, reviewed with documented
limitations and authorized for integration. For features that involve
scientific research or human decisions, software test success is necessary
but insufficient. All eight items currently remain PARTIAL.

---

## First usable slice

The file benchmarks/critical_cases_v1.json defines twelve explicitly
SYNTHETIC adverse scenarios and expected protective actions. These are NOT
observed incidents, executable tests of the seven gates, or empirical data.

The script scripts/evaluation_registry.py records observations from actual
runs entered separately, including an evidence reference, exact Skill commit,
source-catalog hash, timestamp and chained entry hash. It does not verify that
the supplied evidence reference is genuine, nor authenticate an independent
reviewer. Missing observations are NOT_EVALUATED, not passed tests. Comparisons
are refused when the case catalog changed.

Create a file with the following shape only after executing a genuine test:

    {
      "schema_version": 1,
      "cases": [
        {
          "case_id": "DOI-001",
          "observed_action": "FLAG",
          "evidence_reference": "my-test-logs/real-test-001.txt"
        }
      ]
    }

Commands:

    python scripts/evaluation_registry.py record --catalog benchmarks/critical_cases_v1.json --observations /path/observations.json --ledger /path/runs.jsonl --run-id run-001 --skill-commit EXACT_40_HEX_COMMIT
    python scripts/evaluation_registry.py verify --ledger /path/runs.jsonl
    python scripts/evaluation_registry.py compare --ledger /path/runs.jsonl --baseline run-001 --candidate run-002

The hash chain detects accidental or unsanctioned edits, but is not an
authenticated timestamp service and cannot prevent a privileged party from
rewriting every entry. These checks evaluate software behavior, NOT scientific
validity or a complete independent assessment.

## Non-negotiable guardrails

- Seven scientific gates and decisions remain human-controlled.
- Distinguish consulted literature [L], inferences [I] and proposals [P].
- No invented DOI, research result, researcher approval or Google Drive receipt.
- No changes to scientific canonical CSV schemas, version, release assets or
  installed beta.5.
- No auto-merge or publication; finish future items through separately reviewed
  commits with their own negative tests and acceptance criteria.
