---
name: meu-artigo
description: Develop and resume scientific article projects with traceable literature search, evidence synthesis, drafting, and submission checks. Use for research questions, review workflows, novelty audits, and evidence-grounded manuscripts. For empirical articles, support literature and provenance without inventing design, data, or findings.
---

# Meu Artigo

## Scientific contract

Start from the user's research problem, question, or sufficiently specific topic. Preserve the original input. Prior projects may inform the process, never supply the new project's topic, criteria, sources, findings, or conclusions.

Every material manuscript claim must link to evidence or be explicitly identified as an original contribution. Distinguish literature-supported statements [L], analytical inferences [I], and original propositions [P]. Never invent sources, access, search counts, full-text reading, independent screening, empirical results, or human validation.

Operate autonomously between scientifically consequential decisions. Ask only for essential missing information or a human judgment required by the current gate. Prepare the concrete evidence and decision before asking. Silence is not approval. An available integration does not itself authorize external messages or unrelated writes.

## Start or resume

For an existing project, read CONTINUIDADE.md first, then the protocol, canonical tables, and latest frozen state. Preserve decided records and executed queries; do not reconstruct them from chat memory.

For a new project:
1. Resolve the storage gate before substantive research. Read [plugin onboarding](references/plugin-onboarding.md), [workspace](references/drive-workspace.md), [project state](references/project-state.md), and [storage mapping](references/storage-mapping.md). Google Drive is the canonical default, not an optional convenience.
2. Verify whether Google Drive is actually connected and writable. If it is not, surface the platform's connect/install flow and wait for the user's required authorization action. Re-check the connection; never claim it succeeded without verification.
3. If Google Drive is still unavailable after the connection attempt, ask one explicit fallback question before doing substantive work: whether the user wants to continue without Google Drive and use only the platform/Work/local artifacts for this project. Silence, topic continuation, or an unrelated answer is not consent.
4. Only after an explicit affirmative fallback authorization may the Skill initialize or treat Work/local/filesystem artifacts as the project's persistent workspace. Record the authorization, actor, date/time, storage mode, and limitation in PROJECT_CONFIG.json and CONTINUIDADE.md. If the user does not authorize fallback, remain blocked at storage onboarding and do not start novelty search, screening, synthesis, drafting, or local canonical project creation.
5. When Google Drive is connected, create or resume the Drive workspace first and persist every material artifact there. Temporary local/Work files may be used only as staging and must be uploaded/synchronized to the canonical Drive workspace before they are treated as project state.
6. Preserve the research input and identify the likely methodological track with [review design](references/review-design.md).
7. Ask whether a target journal and official author rules/template exist. Read [journal-aware](references/journal-aware.md). Use JOURNAL_NEUTRAL when none is selected, JOURNAL_AWARE_PENDING_PROFILE while rules are missing, and JOURNAL_AWARE only after reading the profile. Maintain JOURNAL_PROFILE.json.
8. Use the canonical spreadsheet in MATRIX_ONLY by default. Read [C.A.D.A.](references/cada-governance.md), [matrix](references/cada-matrix.md), [template](references/spreadsheet-template.md), and [storage mapping](references/storage-mapping.md) when setting it up. Prefer a native spreadsheet in the canonical Drive workspace, then the official generator with immediate synchronization, then CSV compatibility tables. Show 00_PAINEL.

For inexperienced users, apply [beginner mode](references/beginner-mode.md). A manager mirror is optional; use [work management](references/work-management.md) only when enabled. Keep one primary manager per article unless explicitly requested otherwise.

## Choose the scientific path

- Integrative/conceptual/theoretical: support synthesis of heterogeneous literature and explicit original contributions.
- Systematic: require comprehensive eligibility and appropriate appraisal; structured searches alone do not justify this label.
- Empirical: require actual design, data and analyses before reporting findings.
- Other review families: retrieve the appropriate methodological guidance; do not force an integrative design.

## Execute the current stage

Read only the relevant section of [detailed workflow](references/workflow-stages.md) and its references.

| Stage | Required output and control | Supporting reference |
|---|---|---|
| 1. Novelty | Compare nearest literature; narrow unsupported novelty claims | workflow-stages.md |
| 2–4. Protocol and search | Freeze eligibility and version executable queries; preserve and validate raw exports and counts | [search/screening](references/search-screening.md), [tool roles](references/tool-orchestration.md) |
| 5–7. Dedupe, screen, retrieve | Audit exclusions; preserve ambiguous duplicates; distinguish actual full text from abstracts | [search/screening](references/search-screening.md) |
| 8–9. Evidence and synthesis | Extract locators, limitations and evidence roles; compare sources; label inference | [evidence/synthesis](references/evidence-synthesis.md) |
| 10. Normative evidence | Separate institutional authority from scientific findings; omit when irrelevant | workflow-stages.md |
| 11–12. Journal and drafting | Draft from evidence and actual search logs; journal fit never changes findings | [journal-aware](references/journal-aware.md) |
| 12.5–13. Robustness and audit | Check Counter_Evidence_IDs, alternatives, boundaries, single-source dependence and Robustness_status | [scientific governance](references/scientific-governance.md) |
| 14. Submission | Verify rules, exact outgoing files and authorization; preserve submitted state and receipt | [anonymization](references/anonymization.md) |

Use scripts/dedupe_records.py for compatible exports. Conflicting DOIs must remain separate; title matches without corroborating author/year are review candidates. Lack of full-text access is pending access, not a scientific exclusion reason. Do not imply that purposive full-text sampling assessed every candidate.

Grounded Corpus Mode uses only validated eligible full text; give Record_IDs, Evidence_IDs and locators and disclose unsupported answers. Read [grounded corpus](references/grounded-corpus.md) when answering corpus questions. Corpus Map is optional exploration of real metadata, not a change of review design; read [corpus map](references/corpus-map.md).

In the evidence matrix, preserve conceptual lineage where relevant: distinguish foundational/canonical works, classic critiques, methodological foundations, contemporary updates, empirical support, and contrary evidence. Do not call a work “classic” merely because it is old or highly cited. For claims about who introduced/defined/proposed a concept, verify the primary source when reasonably accessible; otherwise mark the attribution as secondary-only rather than implying direct consultation. Read [evidence/synthesis](references/evidence-synthesis.md).

## C.A.D.A. contribution and scientific-method independence

C.A.D.A. captures, assigns, deadlines and follows up administrative research demands; it does not constitute a literature-review method, establish source validity or certify scientific results. Read [boundary and prospective comparison](docs/LIMITES-CADA-E-COMPARACAO.md) and use `scripts/audit_governance_boundary.py audit PROJECT` to distinguish task-completion records from scientific decisions and source/evidence checks. A CADA_ID or status DONE must never be the sole basis for approving a scientific gate. Always report management progress and scientific safeguards separately, and never claim reductions in retrabalho/time or improvements in research quality as established without independent, real-world comparison. A frozen comparison protocol is available but no results have been collected; preserve the same scientific methodology and human gates in both arms. No new worksheet, ID family or paid integration is needed.

## Evidence-backed process events

For local operations in the allowlist, use `scripts/trace_execution.py run` to capture the actual process exit, input/output hashes and receipt against the existing TRACE_ID. Read [event verification](docs/COMPROVACAO-EVENTOS.md). Do not label an externally performed search, export, upload or submission CONFIRMED on the basis of a model narrative or a manually written log. When there is no trusted tool receipt, preserve UNVERIFIED (a declaration is not proof). PARTIAL and FAILED outcomes remain visible. Existing C.A.D.A., decision/gate and TRACE tables stay canonical; no new ID family or worksheet is needed. Synchronize receipts and updated project state to Google Drive when Drive is canonical. Script execution does not prove a scientific conclusion.

## Researcher-controlled screening

Before writing eligibility decisions, read [screening audit](docs/SCREENING-AUDITAVEL.md). Run `scripts/screening_review.py propose` only when a real, cited AI recommendation exists; it cannot populate final decision cells. `scripts/screening_review.py decide` requires an actual human review with attributable evidence and a reason, including every EXCLUDE. Differences between an AI proposal and a human decision require a separate explanation. Do not treat a final cell without human evidence as approved or report a model as a second human screener. Reconcile screening before GATE-0004; new projects enforce this rule. No new sheet or management ID is created.

## Type-specific critical appraisal of cited evidence

Before relying on material evidence in a scientific claim, read [critical appraisal](docs/AVALIACAO-CRITICA-FONTES.md). DOI resolution and matched text cannot establish methodological quality. Use `scripts/appraise_evidence.py template` to generate an unanswered checklist for quantitative, qualitative, mixed-methods, review, conceptual, normative or other sources. Obtain a real researcher's review using `scripts/appraise_evidence.py record`; store criterion-level reasons, limitations, the reviewer and an actual response reference. A model cannot self-certify this assessment or substitute journal prestige for methodological rigor. In new projects GATE-0006 blocks reliance on missing, unsuitable or insufficiently appraised material evidence. Reuse existing Evidence_IDs and tabs; no paid service.

## Claim provenance and bounded originality

For material [L], [I] and [P] claims, use [claim integrity](docs/CONTROLE-CLAIMS-E-ORIGINALIDADE.md) and the offline standard-library script scripts/claim_integrity.py. Literature [L] needs traceable sources and locators; analytical [I] needs a reasoning warrant and explicit limits; author propositions [P] require nearest prior works, the difference contributed and a bounded novelty-search reference. Do not call a proposition 'first', 'unprecedented' or universally original merely because its specific keywords returned few results. A registered search cannot prove absence from all literature. Avoid automatically upgrading an LLM's inference to a source-supported finding. Use real researcher review evidence. These controls are structural, not semantic validation, originality certification or a substitute for human judgment. Keep existing claim IDs and worksheets.

## Scientific quality calibration

Use [quality evaluation](docs/AVALIACAO-QUALIDADE-CIENTIFICA.md) when benchmarking the Skill or comparing releases. A frozen public reference set and `scripts/quality_benchmark.py` evaluate actual submitted reference identities, documented selection counts, and local literal locators; unsubmitted evidence remains unscored. Public metadata pilot checks are not validation of LLM scientific quality. For source-supported claims and theoretical categories, require external, documented human adjudication rather than self-grading the model. Never manufacture screening exports, author decisions, published counts, expert labels, or a before/after evaluation. This evaluation is independent from routine project governance, introduces no extra spreadsheet tab or project ID, and requires no paid service.

## Source and locator verification

Before freezing literature-supported claims, read [source verification](references/source-verification.md). When a script runtime is available, run scripts/verify_sources.py against the canonical project state and persist the report. It uses public free Crossref/OpenAlex queries and local text checks; no paid subscription is required. An unavailable API, DOI, full text or runtime must remain unverified, never silently approved. A DOI match checks metadata; local passage matching checks textual presence; neither establishes semantic support. Human review remains necessary for material claims and alerts. Do not upload copyrighted PDFs to external verification services.

## Decisions, continuity, and release

Read [traceability](references/traceability.md) and [scientific governance](references/scientific-governance.md) for material events. Preserve CADA_ID, TRACE_ID, Evidence_ID and Claim_ID links. Use DEC_ID for material decisions, GATE_ID for actual human checkpoints and SNAP_ID for meaningful freezes. Proposals remain PROPOSED until explicit human judgment and evidence are recorded.

Default gates cover question, method, search, corpus, synthesis, claims and submission. For scientific gates GATE-0001 through GATE-0006, use the [formative validation](docs/VALIDACAO-FORMATIVA.md) workflow when enabled: explain the proposed decision and its boundaries, then obtain the researcher's own rationale and one limitation before recording approval. Do not invent, complete, or paraphrase a model-generated answer as the researcher's response. The submission gate retains its operational checks. Apply only relevant gates. Claims marked REVISE or REJECT block final freeze; QUALIFIED wording must carry its qualification into the manuscript.

At each material stage boundary update CONTINUIDADE.md, canonical tables, RASTREABILIDADE.md and applicable AI-use records with exact counts, changes, blockers, links, and the next valid action. When Google Drive is the canonical backend, perform these updates in Drive rather than leaving the current state only in Work/local outputs. Record real human review; do not infer it from a script's execution.

Before external artifacts, read [anonymization](references/anonymization.md). Keep ANONYMIZATION_PROFILE.json confidential; separate identified title pages from blinded manuscripts. For EXTERNAL_ANONYMIZED outputs, enforce `ZERO_NONESSENTIAL_METADATA`: no Author/Creator/Producer/Generator/Application, editing timestamps, XMP/EXIF/IPTC, document properties, archive comments, revision authorship, embedded paths or equivalent provenance metadata. A label such as “generated with Python”, “pypdf”, “ReportLab”, “Matplotlib”, “LibreOffice”, or another generator is a release-blocking metadata leak. Run `scripts/sanitize_metadata.py` on the exact outgoing files before `scripts/audit_anonymization.py`. Empty scope, unverified profiles, unsupported metadata inspection, or residual metadata cannot pass. Record actual manual review where needed. Approval is bound to file and profile hashes; any change requires a new audit. Scientific meaning and necessary self-citations must be preserved.

Run scripts/validate_project.py before release. Use scripts/governance_events.py for recorded decisions, scripts/create_snapshot.py and scripts/compare_snapshots.py for freezes, and scripts/generate_transparency_report.py for a report based solely on canonical data. These tools record/check state; they do not establish scientific validity.

For optional interoperable audit packages, read [provenance export](references/provenance-export.md): W3C PROV, RO-Crate and SHA-256 support provenance and fixity. Do not claim submission occurred without actual completion by the user or an authorized tool.
