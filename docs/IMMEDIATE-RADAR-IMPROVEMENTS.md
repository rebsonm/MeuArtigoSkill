# Immediate improvements — work in progress

**Scope:** Eight immediate proposals from the separate private Radar. This is
a DRAFT feature branch, not an implemented release or a scientific validation.
No source code from third-party radar projects is copied here.

## Acceptance matrix

| Rank | Radar ID | Deliverable | Current PR state |
|---|---|---|---|
| 1 | CAS-003 | Curated difficult-case tests for claim, reference, storage and gate boundaries | Initial synthetic catalog created; live behavioral adapters not yet implemented |
| 2 | REG-001 | Immutable-versioned comparison of controlled observations | Append-only JSONL hash chain and compare CLI implemented; observed real runs pending |
| 3 | REG-018 | Audit of manuscript citations and bibliography | **Incremental read-only audit implemented** (scripts/reference_audit.py, 15 negative/positive tests). Whole-manuscript in-text citation parsing still pending |
| 4 | REG-011 | Semantic claim-to-passage examination | **First implementation added:** one [L] claim/evidence review item, source/quote/hash binding, explicit self-reported human judgment, alignment/contraevidence guards and tests. Not an automated entailment verifier or authenticated independent assessment. |
| 5 | REG-013 | One-page scientific diagnostic with uncertainties | **Initial implementation:** deterministic one-page-oriented Markdown/print A4 HTML/JSON, grouped prioritized reference/claim/protocol warnings, SHA-256 and privacy guards. Real researcher review/print validation pending. |
| 6 | REG-017 | Unified researcher panel and real storage receipts | Pending; preserve current native chat dashboard pilot and Google Drive-first |
| 7 | REG-019 | Reproducible evaluation package with privacy controls | Pending; initial ledger is a component, not the complete export |
| 8 | ENG-022 | Adversarial engineering, regression tests and incremental review | Initial unit tests and read-only CI for first slice added; ongoing |

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
