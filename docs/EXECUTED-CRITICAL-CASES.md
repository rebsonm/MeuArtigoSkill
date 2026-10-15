# CAS-003 + REG-001 — Executed offline synthetic control probes

The command in this increment executes **actual local control functions**
against **isolated synthetic research data**. It is not a live academic
evaluation, not evidence that any invented DOI exists, and not a validation
of an LLM's semantic reliability.

Twelve fixed case IDs map to existing scripts; a case-catalog change fails
closed until the adapters receive deliberate review. Two bibliographic
probes inject fictional Crossref/OpenAlex replies into the real metadata
matching logic. They make **zero actual external provider requests**.
The source records are synthetic, and the gate case runs as a separate
local process against a temporary CSV. No human scientific gate is approved.

## Execute offline

Use a new output directory, not one containing actual project documents:

    python scripts/run_critical_cases.py \
      --catalog benchmarks/critical_cases_v1.json \
      --output-dir /tmp/meu-artigo-synthetic-run-001 \
      --skill-commit EXACT_40_HEX_CHECKED_OUT_REVISION \
      --strict

The executor writes:

- summary.json: full expected-versus-observed table, reason codes,
  per-case evidence hashes, number not evaluated, and explicit limits.
- observations.json: actual software observation actions and local
  evidence references, suitable for the existing REG-001 recorder.
- evidence/CASE-ID.json: redacted evidence of executed code conditions,
  including control return status and synthetic fixture type.
- evaluation_runs.jsonl: REG-001 append-only record bound to the exact
  declared software revision and frozen catalog.
- evaluation-replay.zip: REG-019 privacy-reduced scored package with
  no original research corpus.

The output is *not* a manuscript or part of a canonical research project.
Re-running a case creates a new run directory rather than replacing history.

A passing expected-versus-observed result means the **specific synthetically
constructed condition** produced a coded software response. It does not
prove general false-positive/false-negative rates, actual paper identity,
source-access permissions or effective human oversight. A failure or
exception remains NOT_EVALUATED or mismatched, never silently passed.

## Case mapping and scope

- DOI-001/DOI-002: real metadata matching logic, **mocked** provider replies.
- LOC-003/TRC-007/INF-011/PRO-012: actual claim-integrity audit.
- SUP-004: a **synthetic declared judgment** with deliberately contradictory
  alignment; no semantic model/independent human review.
- GAT-005: local governance CLI refuses gate approval without a substantive
  researcher rationale and limitation, with a byte-for-byte unchanged CSV.
- STO-006: read-only dashboard does not certify a Drive synchronization
  without an observed remote receipt. This **does not** test remote writes.
- ANON-008: identity/e-mail scanner on synthetic manuscript text.
- ACC-009: actual rights guard refuses metadata-only full-text access.
- DUP-010: actual conservative bibliographic import detects/records an
  exact DOI duplicate, without silently counting it twice.

All original scientific gate approvals remain human-controlled. The
operator-supplied source revision SHA is a provenance **declaration**,
not an independently authenticated software attestation.

## Acceptance still pending

Independent evaluation needs preregistered samples, representative real
inputs under explicit rights, a blind ground-truth review, confidence
intervals/uncertainty, false alarms, missed errors, and actual provider
responses collected with source provenance. These are NOT delivered by
this synthetic execution harness.
