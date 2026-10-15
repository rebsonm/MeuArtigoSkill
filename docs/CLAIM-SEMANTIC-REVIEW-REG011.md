# REG-011 — Human-assisted claim-to-passage assessment

This is a **bounded protocol and evidence consistency checker**, NOT an
automated semantic entailment engine. It cannot independently determine
whether a passage supports a scientific proposition or authenticate a human
reviewer's identity. Its job is to make overclaims easier to expose and harder
to silently mark as reviewed.

## What the implementation does

1. Reads the existing authorized canonical Claim Ledger and Evidence Matrix
   (no schema changes, no new ID families, no new scientific gate).
2. Reuses the existing SOURCE_VERIFICATION.json integrity assessment and
   insists on a versioned source file and literal matched passage.
3. Creates one review item per [L] Claim_ID + Evidence_ID pair, including
   outstanding link/source deficiencies. [I]/[P] are not relabelled [L].
4. Accepts **explicitly supplied**, self-reported human assessments distinguishing
   SUPPORTED, PARTIALLY_SUPPORTED, NOT_SUPPORTED and INCONCLUSIVE.
5. Requires scope, method, context, contrary-evidence consideration,
   limitations and rationale; a verdict SUPPORTED is rejected when any
   recorded dimension contradicts full support.
6. Checks the reviewer's provided exact quotation against a lawful local
   text/PDF using the existing literal locator verifier. A textual match alone
   does not justify the selected semantic judgment.
7. Binds the review to the current source file SHA-256, Claim_text hash and
   whole source-verification report checksum; detects stale edits.
8. Outputs hashes and coded states only, without source excerpts, reviewer names,
   rationale text or document file paths. No input text sent to an API.

## Usage

First verify the sources according to docs/VERIFICACAO-FONTES.md.
An offline report cannot establish live bibliographic metadata.

Generate pending review items without declaring any science reviewed:

    python scripts/semantic_claim_review.py /authorized/project

Create an assessment JSON file in the **authorized project** (this example
is synthetic documentation, NOT a completed scientific assessment):

    {
      "schema_version": 1,
      "reviews": [
        {
          "claim_id": "CLAIM-0001",
          "evidence_id": "EVID-0001",
          "claim_sha256": "<64-hex of normalized canonical Claim_text>",
          "source_sha256": "<exact current source file SHA-256>",
          "source_report_sha256": "<actual SHA-256 of SOURCE_VERIFICATION.json>",
          "reviewer_kind": "HUMAN_DECLARED",
          "reviewer": "<real reviewer name>",
          "response_reference": "<real conversation/review evidence>",
          "judgment": "PARTIALLY_SUPPORTED",
          "scope_alignment": "OVERGENERALIZED",
          "method_alignment": "ALIGNED",
          "context_alignment": "ALIGNED",
          "counterevidence_considered": true,
          "rationale": "<substantive actual interpretation>",
          "limitations": "<known evidence and sampling limitations>",
          "quoted_passage": "<literal passage from legally accessible source>"
        }
      ]
    }

Run:

    python scripts/semantic_claim_review.py /authorized/project \
      --assessments 04_Evidencias_e_Sintese/assessment.json \
      --strict --output 98_Technical_Reports/claim_review_report.json

A missing review remains PENDING_HUMAN_REVIEW. The tool never supplies a
reviewer name or judgment itself. A bad source, missing DOI verification,
unmatched quotation, retraction notice, missing human response, stale
checksum or unsupported status causes a coded hold.

Technical report exports are restricted to **new files directly inside**
`98_Technical_Reports/` in the authorized local project. They cannot
replace any canonical register, gate record, continuity document or other
existing file. Symlink and traversal attempts are denied. These files are
local and do not confirm Google Drive synchronization.

## Additional lexical risk signals (exploratory)

After a literal quotation has been verified against a currently linked source,
the checker emits only coded possible-overreach indicators for narrow English
and Portuguese patterns (causality, universality, missing outcomes, statistical
polarity, direction, method, dates, missing subgroups and unsupported quantities).
These are **review requests**, not semantic entailment decisions. Even an empty
set of indicators **does not** mean the claim is supported. A missing, stale or
unmatched excerpt is NOT_EVALUATED for this additional screening.

**Review-only correction:** heuristic risk codes are explicitly ADVISORY.
They do not change the formal review status or independently make the
`--strict` exit code fail. A valid, declared review with lexical warnings
remains `HUMAN_JUDGMENT_RECORDED_NOT_AUTHENTICATED`; the report preserves
`semantic_risk_codes` and `heuristic_review_needed` for researcher attention.
`--strict` returns 2 when required formal inputs/reviews are missing or
invalid, including stale source reports, invented passages and mismatched
evidence hashes. Exit code 0 means only that those *formal requirements*
were met; it **never means** a human was authenticated, semantic support
was established or a scientific gate approved. A compact REG-013 report now shows
possible-overreach risk counts without revealing source text or personal data.

This deterministic rule set was developed with the original 16 fictional
challenge cases visible. Results on those cases are **in-sample exploratory**,
not generalization evidence or performance validation.

## Essential limitations

- Even with all checks completed, status is
  HUMAN_JUDGMENT_RECORDED_NOT_AUTHENTICATED. This is a traceable **declaration**,
  not independent peer review or verified scientific correctness.
- A source match proves phrase presence only. A narrower excerpt cannot
  establish causal conclusions, novelty, generalizability or other claims.
- Does not modify GATE-0006, sign off as an independent reviewer, or
  automatically write to canonical Drive.
- Do not upload copyrighted source passages to public reports. The working
  assessment file retains user-supplied text locally, inside the authorized
  project; the output redacts content and stores hashes/statuses only.
- The data can still be sensitive; share only after legitimate privacy review.
- The next increment should support researcher-facing comparison in the
  native chat interface and an independent-blinded review protocol if real
  scientific validation is pursued.
