# Scientific governance: decisions, human validation gates, snapshots, and reviewer transparency

## Purpose

Meu Artigo already separates:

- work management — `CADA_ID`;
- process events — `TRACE_ID`;
- scientific evidence — `Evidence_ID`;
- manuscript assertions — `Claim_ID`.

This layer adds the missing governance objects:

- `DEC_ID` — material scientific decision and rationale;
- `GATE_ID` — explicit human validation checkpoint;
- `SNAP_ID` — frozen project state at a meaningful milestone.

The goal is a coherent scientific chain of custody, not additional bureaucracy.

## Chain of custody

```text
Research problem
   ↓
DEC_ID       why a scientific choice was made
   ↓
CADA_ID      what work had to be done
   ↓
TRACE_ID     what actually happened
   ↓
Record / Evidence / Synthesis / Claim
   ↓
GATE_ID      where a human reviewed and accepted/rejected a critical transition
   ↓
SNAP_ID      what the official project state was at that point
   ↓
Manuscript
   ↓
EXPORT_ID    interoperable W3C PROV / RO-Crate package
```

Do not force every item through every identifier. Link only when scientifically meaningful.

---

## DEC_ID — material scientific decisions

A decision is not the same as a task or event.

Create a `DEC-####` when a choice materially affects:

- research question or contribution;
- methodological design;
- scope/boundaries;
- search strategy or filters;
- screening/full-text rules;
- evidence interpretation;
- synthesis/category structure;
- claim/proposition;
- manuscript structure when scientifically meaningful;
- target journal/submission strategy when it changes the scientific presentation.

Do not create DEC_IDs for trivial formatting or administrative preferences.

### Canonical table: `17_DECISOES`

Fields:

```text
DEC_ID
Timestamp
Scientific_stage
Decision_type
Decision_question
Decision
Alternatives_considered
Rationale
Evidence_IDs
Record_IDs
CADA_ID
Trace_ID
Gate_ID
Status
Decided_by
Impact
Affected_artifacts
Resulting_version
Supersedes_DEC_ID
Notes
```

Decision types:

- QUESTION_CONTRIBUTION
- METHOD
- SCOPE
- SEARCH
- SCREENING
- FULL_TEXT
- EVIDENCE
- SYNTHESIS
- CLAIM
- MANUSCRIPT
- JOURNAL
- SUBMISSION
- OTHER

Status:

- PROPOSED
- APPROVED
- REJECTED
- FROZEN
- SUPERSEDED

Rules:

- preserve rejected alternatives when they mattered;
- never silently overwrite an approved/frozen decision;
- a changed decision creates a new DEC_ID or explicitly supersedes the old one;
- rationale must explain why, not merely restate the decision;
- when evidence informed the choice, link Evidence_ID/Record_ID;
- AI may propose a decision, but critical scientific decisions remain human-responsible.

---

## Human Validation Gates

A gate is a controlled transition at a small number of scientifically consequential points.

The purpose is **not** to ask the user for permission after every action. Between gates, the Skill should operate autonomously.

A gate becomes READY only when its entry conditions are met.

### Default gates

```text
GATE-0001 — Question & contribution
GATE-0002 — Method & protocol
GATE-0003 — Search strategy
GATE-0004 — Corpus freeze
GATE-0005 — Synthesis / theoretical output
GATE-0006 — Claims / final scientific audit
GATE-0007 — Submission release, including anonymization and outgoing-file audit
```

Adapt or mark NOT_APPLICABLE when the design makes a gate irrelevant. Do not invent additional gates unless there is a genuine scientific-risk reason.

For GATE-0007, anonymization is part of the existing submission-release gate rather than a new gate. Approval requires a VERIFIED anonymization profile or explicit NOT_REQUIRED rationale, journal-rule reconciliation when applicable, and a passing audit of the exact outgoing files.

### Canonical table: `18_VALIDACOES`

Fields:

```text
GATE_ID
Gate_type
Scientific_stage
Name
Entry_condition
Items_to_validate
DEC_IDs
CADA_IDs
Evidence_IDs
Snapshot_before
Decision
Validated_by
Validation_date
Validation_method
Validation_evidence
Trace_ID
Snapshot_after
Status
Blocking_transition
Notes
```

Gate decision:

- APPROVED
- APPROVED_WITH_CHANGES
- REJECTED
- NOT_APPLICABLE
- PENDING

Gate status:

- PENDING
- READY
- COMPLETED
- NOT_APPLICABLE

### Independent quality evaluation is distinct from a gate

The project gates regulate actual scientific decisions; they do not empirically validate the research-assistant Skill. A separate, reproducible quality benchmark is described in [quality evaluation](../docs/AVALIACAO-QUALIDADE-CIENTIFICA.md). Scores on frozen public bibliographic facts must not be called independent semantic validation or substitute for a real review-replication protocol. Claims and conceptual categories require independently justified adjudication.

### GATE-0006 robustness requirement

GATE-0006 is not satisfied merely because each claim has a supporting citation.

Before it becomes READY/APPROVED, material claims should be checked for:

- counter-evidence;
- alternative explanations;
- boundary conditions;
- single-source dependence;
- evidentiary overstatement;
- [L]/[I]/[P] status;
- real human review.

Claims marked REVISE or REJECT block final claim freeze until resolved. Claims marked QUALIFIED must carry their qualification into the manuscript.

When a target journal is active, GATE-0006 may also check whether the claim architecture fits the journal's permitted article structure, but journal fit must never be used to suppress contradictory evidence.

For material literature-grounded claims, inspect SOURCE_VERIFICATION.json tied to the current Evidence Matrix. Where source verification is required, missing or stale reports and contradictory identifiers/locators block GATE-0006. Inconclusive verifications and editorial alerts require documented human examination, not an inferred VERIFIED status. A metadata or literal-text match is not a semantic claim audit.

### Formative researcher judgment

In new projects, `formative_gates_required=true` requires a response by the researcher at scientific approval gates GATE-0001 to GATE-0006. See [formative validation](../docs/VALIDACAO-FORMATIVA.md). Present the proposed choice, supporting basis, alternatives, and relevant limitation in accessible terms. Ask the researcher why the chosen approach fits the research question and what its most important limitation is. Keep the original human response reference. Only record their actual words as researcher rationale and limitation; never supply or silently infer these as though they were written by the researcher. A simple "approved" does not complete a formative scientific gate. Use existing `Validation_evidence` and `Notes` columns. GATE-0007 remains focused on release checks, without a mandatory didactic question. This enforces the presence and internal consistency of an explanation, not substantive understanding or authorship authentication.

### Gate behavior

If a required gate is READY:

1. summarize exactly what needs human judgment;
2. show relevant decisions/evidence/risks;
3. ask one focused approval/revision question;
4. record the human response;
5. create/update DEC_IDs as necessary;
6. record the validation TRACE event;
7. create the post-gate SNAP_ID when the gate is approved;
8. continue autonomously.

Do not represent an inferred user preference as gate approval.

---

## SNAP_ID — frozen scientific state

A snapshot is a verifiable frozen state of the canonical project at a meaningful milestone.

Typical snapshots:

- initial research input;
- question/contribution frozen;
- protocol frozen;
- search strategy frozen;
- corpus frozen;
- synthesis frozen;
- submission manuscript frozen.

### Canonical table: `19_SNAPSHOTS`

Fields:

```text
SNAP_ID
Timestamp
Milestone
Scientific_stage
Trigger
Gate_ID
DEC_IDs
CADA_IDs
Previous_SNAP_ID
Snapshot_path_or_URL
Manifest_path
Manifest_SHA256
Canonical_artifacts
Change_summary
Validation_status
EXPORT_ID
Notes
```

Use stable `SNAP-####`.

### Snapshot content

The reference filesystem implementation should create:

```text
00_Gestao_e_Continuidade/Snapshots/
└── SNAP-0004_corpus-freeze/
    ├── snapshot.json
    ├── manifest-sha256.txt
    └── payload/
        └── selected canonical artifacts
```

Exclude full-text PDFs by default.

The manifest provides fixity, not scientific validity.

### Comparing snapshots

Reference script:

`scripts/compare_snapshots.py`

It should report:

- added files;
- removed files;
- changed files;
- unchanged files;
- decision changes when available;
- state summary.

This supports questions such as:

> What changed between protocol v2 and v3?

and:

> Is the submitted manuscript the same state that was released at the final gate?

---

## Reviewer / Editor transparency report

The reviewer should not need the entire private workspace to understand the construction process.

Reference generator:

`scripts/generate_transparency_report.py`

Default outputs:

```text
06_Submissao/Arquivos_Finais/
├── RELATORIO_TRANSPARENCIA_<timestamp>.md
└── RELATORIO_TRANSPARENCIA_<timestamp>.json
```

The report should be deterministic and source-grounded. Do not generate narrative facts that are absent from canonical tables.

Sections:

1. project identity and research object;
2. methodological design and protocol status;
3. search provenance and reconciled counts;
4. corpus/screening/full-text status;
5. material scientific decisions;
6. human validation gates;
7. frozen snapshots;
8. evidence-to-claim coverage;
9. substantive AI use and human review;
10. interoperability/provenance exports;
11. unresolved traceability gaps and limitations.

### Privacy rule

The reviewer report is a **transparency view**, not a dump of the private workspace.

Do not include:

- passwords/tokens;
- private chat content that is not methodologically necessary;
- copyrighted full-text content;
- confidential participant/data material;
- unrelated internal notes.

---

## Relationship to W3C PROV / RO-Crate

When exporting provenance:

- DEC_ID → `prov:Entity` representing a decision record;
- GATE_ID → `prov:Activity` representing a human validation action;
- SNAP_ID → `prov:Entity` representing a frozen project state;
- gate validator → `prov:Agent`;
- snapshot → `prov:wasGeneratedBy` validation/snapshot activity;
- decision → may `prov:wasDerivedFrom` linked Evidence_IDs.

Use the Meu Artigo namespace for relations not directly covered by simple PROV-O mappings.

---

## Anti-Frankenstein rule

A governance feature belongs in the core only when it answers at least one of:

- What was done?
- Why was it done?
- Based on what?
- Who/what did it?
- What changed?
- Who validated the critical transition?
- What was the official state at that moment?

If it does not materially improve one of these answers, keep it outside the core.


## Explicit human decision recording

scripts/governance_events.py decision defaults to PROPOSED with no assumed researcher. APPROVED, FROZEN or REJECTED requires --decided-by and --evidence referencing the actual human response; evidence is retained in decision Notes. Completed gate decisions require --validated-by, --method and --evidence. A command records an attestation, not independent proof of human identity.
