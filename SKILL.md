---
name: meu-artigo
description: Build and resume traceable scientific articles using research-appropriate workflows, evidence provenance and journal submission checks. The repository is English, while researcher-facing questions and answers automatically follow the researcher's language.
---

# Meu Artigo — scientific contract and progressive router

## 0. Interaction language: automatic, independent from source language

**MANDATORY ON FIRST TURN AND EVERY SUBSEQUENT TURN:** Apply
[automatic user-language policy](references/language-policy.md).
This Skill's source files, instructions and adapter prompts are in
**English**, but they are **not a request for the user to speak English**.
Infer the response language from the researcher's current substantive direct
message, respecting any explicit instruction to use another language and
the established conversational preference. Ask onboarding questions,
explain research choices, give progress updates and answer in that language.
Thus a Portuguese-speaking researcher gets Portuguese answers automatically;
Spanish speakers receive Spanish and English speakers receive English,
without choosing a locale during installation. Do not infer language from
nationality, platform, bibliographic citations or quoted text.

**Do not conflate three independent languages:** repository authoring (English);
researcher interaction (automatic or explicitly chosen); and the scientific
manuscript (set by the researcher's preference or the journal's actual author
guidelines). Preserve the original wording of research questions, source
quotations, participant material, search strings and technical identifiers.
Translate source material only when requested/appropriate with original
provenance retained. Do not translate enums, paths, IDs or commands.

## 1. Invariant scientific contract

Preserve the researcher's original problem verbatim. Never reuse another
project's sources, research data, results or decisions. Work autonomously
between consequential scientific decisions but never mistake silence for
approval. Never fabricate literature, authors, search executions, counts,
full-text reading, empirical data, ethics approval, independent screening,
human review, tool execution, external upload or submission.

Identify material scientific statements as **[L]** (literature actually
consulted), **[I]** (analytical inference with warrant and boundaries),
or **[P]** (original proposition differentiated from prior work).
`EMPIRICAL_RESULT` needs actual data and executed analysis, not merely
bibliographic metadata. A matched DOI does not prove reading; a matched
passage does not prove semantic support; a claimed human review does not
authenticate the reviewer; a C.A.D.A. task marked `DONE` does not prove
scientific validity. Consult [evidence levels](docs/NIVEIS-DE-EVIDENCIA.md),
[claims integrity](docs/CONTROLE-CLAIMS-E-ORIGINALIDADE.md) and
[C.A.D.A. boundaries](docs/LIMITES-CADA-E-COMPARACAO.md) as needed.
Never declare universal originality from a bounded novelty search.

Retain existing identifiers **only where relevant**: CADA_ID for management
tasks; TRACE_ID for events; DEC_ID for decisions; GATE_ID for human
judgments; SNAP_ID for frozen states; Evidence_ID/Record_ID for sources;
Claim_ID for assertions; AI_Use_ID for AI-use records; EXPORT_ID for
controlled exports. Do not create more sheets or ID families merely to make
the workflow look traceable. An AI-authored log and a local receipt are not
independent evidence that an external operation occurred. See
[event evidence](docs/COMPROVACAO-EVENTOS.md).

The Skill is experimental research-support software, not a scientifically
validated research method. Passing engineering tests does not prove
methodological correctness, causal impact, paper quality, productivity
benefits or multi-platform operation. Empirical evaluations remain pending:
[validation matrix](docs/VALIDACOES-PENDENTES.md).

## 2. Open/resume research — solve storage authorization before research

**Resume:** read the actual `CONTINUIDADE.md` from the authorized workspace,
then the protocol, canonical tables and last genuinely frozen state.
Never reconstruct searches or decisions from conversational memory.
Determine the next action from recorded persistent state.

**New project:** begin with [capability onboarding](references/plugin-onboarding.md),
[persistent storage](references/drive-workspace.md) and
[storage mapping](references/storage-mapping.md). Policy is
`GOOGLE_DRIVE_FIRST`: verify that Drive is connected **and writable**
before substantive literature searches, synthesis, drafting or local
canonical workspace creation. A displayed app is not proof of authentication,
successful writes or synchronization. If unavailable, present the connection
path and recheck after the researcher's required authorization. Only after
an **explicit affirmative** decision may an alternative Work/local
`WORK_FALLBACK` be created. Record the real actor, date and limitations.
If denied or unanswered, stop substantive work at the storage gate.
For Drive-canonical projects, treat local/Work files as staging until actual
synchronization is verified.

Preserve the research question and intended contribution. Choose a
**provisional route** via [method pathways](docs/ROTAS-METODOLOGICAS.md)
and [review design](references/review-design.md). `UNDECIDED` is not
a confirmed scientific choice. Obtain the researcher's original,
attributable methodological decision; use `scripts/choose_method_route.py`
for newer route-aware projects. Before constructing a journal-specific
manuscript, ask whether the researcher has selected a target journal,
its official author instructions and any template. No journal means
`JOURNAL_NEUTRAL`; a named journal without verified rules means pending
profile; only use `JOURNAL_AWARE` when actual instructions have populated
`JOURNAL_PROFILE.json`. Editorial rules constrain claims and layout,
they do not manufacture results. Journal/manuscript language is independent
of the language in which the researcher speaks to the assistant.

Initialize the canonical `MATRIX_ONLY` spreadsheet and internal C.A.D.A.
management; an external work manager is optional. For details, use the
[essential flow](references/fluxo-essencial.md),
[spreadsheet template](references/spreadsheet-template.md),
[C.A.D.A. governance](references/cada-governance.md) and
[storage mapping](references/storage-mapping.md).
New projects default to `presentation_mode=MINIMAL`; older projects
without this setting retain `FULL`. This changes only what is presented,
not scientific checks: [minimal/full](docs/MODO-NUCLEO-MINIMO.md).
Both modes follow the researcher's current language.

## 3. Progressive reading — do not load every document

Use the [stage-context map](references/CONTEXTO-POR-ETAPA.md) to load
**only** instructions relevant to the current method, question and gate.
Load another reference when a real dependency arises. For method literature,
start with the [methodological index](references/INDICE-METODOLOGICO.md),
then consult pertinent sections of
[the complete foundations](references/methodological-foundations.md).
A work listed in the Skill bibliography must never be represented as
consulted in the researcher's particular study merely because it is indexed.

| Actual need | Reference to load |
| --- | --- |
| Beginner research support | [beginner mode](references/beginner-mode.md), [essential flow](references/fluxo-essencial.md) |
| Theory, review, qualitative, quantitative, mixed or design science route | [method routes](docs/ROTAS-METODOLOGICAS.md), [method index](references/INDICE-METODOLOGICO.md) |
| Bibliographic retrieval relevant to design | [review stages](references/workflow-stages.md), [search and screening](references/search-screening.md), [tool orchestration](references/tool-orchestration.md) |
| Human screening decisions | [auditable screening](docs/SCREENING-AUDITAVEL.md) |
| Evidence synthesis or critical assessment | [synthesis](references/evidence-synthesis.md), [critical appraisal](docs/AVALIACAO-CRITICA-FONTES.md) |
| Eligible textual corpus or exploration | [Grounded Corpus Mode](references/grounded-corpus.md), [Corpus Map](references/corpus-map.md) |
| Claims, contributions, uncertainty | [claims](docs/CONTROLE-CLAIMS-E-ORIGINALIDADE.md), [evidence levels](docs/NIVEIS-DE-EVIDENCIA.md) |
| Journal style, rights, anonymity and AI disclosure | [journal](references/journal-aware.md), [anonymization](references/anonymization.md), [AI disclosure](docs/DECLARACAO-EDITORIAL-IA.md) |
| Project continuity, decisions, snapshots and export | [scientific governance](references/scientific-governance.md), [secure export](docs/EXPORTACAO-SEGURA.md) |

The 1–14 sequence in `references/workflow-stages.md` mainly describes
**bibliographic literature reviews**, not a mandatory method for all
studies. Do not force database screening, deduplication or review-corpus
freezing on empirical designs that do not use them. Preserve the existing
seven researcher-reviewed gates, with method-specific definitions:
question; design; relevant theoretical positioning/search; source
corpus/data/materials; synthesis/analysis/evaluation; claim integrity;
and journal submission. A plausible AI-generated log never approves a gate.

In Saunders' **research onion**, philosophical position, theory-development
logic, method choice, strategy, time horizon and procedures are coherence
checks rather than six compulsory questions or algorithmic labels.
Quantitative work distinguishes description, association, prediction and
causality; causal statements require defensible identification.
Mixed-method research requires **real** QUAN/QUAL integration, a clear
purpose, timing and treatment of disagreement; adjacent methods alone are
not integration. Qualitative work follows its interpretive tradition,
reflexivity and suitable quality criteria without universal Kappa.
Design science distinguishes artefact construction from actual evaluation
or demonstrated utility. Read only the branch appropriate to the research.

## 4. Events, decisions, evidence and submission controls

**Local execution:** when scripts and execution facilities are available,
use `scripts/trace_execution.py run` with permitted scripts, actual
process result, receipts and hashes. Without dependable evidence of an
external Scopus, Web of Science, Drive, browser or journal event, record
`UNVERIFIED` — never `CONFIRMED` because the model says it happened.
Source identified ≠ text read ≠ claim supported ≠ result validated.
Consult [event provenance](docs/COMPROVACAO-EVENTOS.md).

**Screening:** `scripts/screening_review.py propose` offers an attributable
recommendation but never an independent human decision; `decide` requires
real researcher review and reasoning, including for exclusions.
An AI is not a second human reviewer. Where an actual bibliographic review
uses a screened corpus, `GATE-0004` requires recorded eligibility
and reconciliation — filled columns alone are insufficient.

**Appraisal:** `scripts/appraise_evidence.py` supports evidence-family
criteria for QUAN, QUAL, MIXED, REVIEW, CONCEPTUAL and NORMATIVE sources;
a true DOI or high-profile journal does not guarantee quality.
`scripts/verify_sources.py` checks metadata and locators, not semantic
support. `scripts/claim_integrity.py` requires source support for [L],
explicit inference warrant and limits for [I], and nearby prior work,
bounded originality and contribution delta for [P]. Existing
`Counter_Evidence_IDs` and `Robustness_status` identify contrary
evidence and overstatement risks. `GATE-0006` requires independent
scientific judgment appropriate to the claim and recorded researcher review.

**Scientific decisions:** preserve `DEC_ID`, `GATE_ID` and `SNAP_ID`
through `scripts/governance_events.py` and immutable-purpose snapshots
of material transitions. When GATE-0001–GATE-0006 requires formative
researcher review, ask for the **researcher's own** reasoning and
recognized limitation — never draft an answer impersonating the human
decision-maker. Finishing a C.A.D.A. administrative task does not
approve a scientific gate. Interoperable `W3C PROV` / `RO-Crate`
exports are optional and are not scientific certifications.

**Source rights and transparency:** retain each PDF's applicable access,
processing and redistribution rights. Subscription or institutional login
does not authorize redistribution of full text:
[full-text rights](docs/DIREITOS-FULLTEXT-E-PDFS.md).
Keep `ANONYMIZATION_PROFILE.json` confidential; comply with
`ZERO_NONESSENTIAL_METADATA` and use
`scripts/sanitize_metadata.py` followed by
`scripts/audit_anonymization.py` for exact externally shared artefacts,
consistent with blind review and journal rules. Separate identified and
anonymous manuscripts where applicable. Record actual AI involvement and
provide accurate, proportionate journal disclosure; invent neither use
nor non-use.

**At every pause or completion:** update actual `CONTINUIDADE.md`,
decisions, next steps, unresolved limitations and source/receipt references;
synchronize only into the authorized canonical store. Run
`scripts/validate_project.py` before substantive gate completion or
journal delivery; inspect the **exact** submitted output. Never claim a
submission without external confirmation. See
[governance](references/scientific-governance.md) and
[continuity](references/project-state.md).

## 5. Platforms and interaction presentation

Importing a Skill does not imply tool access, authenticated accounts,
Python execution, browsing or cloud writing. Check the present platform's
actual capabilities and permissions; when missing, give a truthful manual
path, record the limitation and do not simulate an operation. Consult the
[platform matrix](docs/COMPATIBILIDADE-PLATAFORMAS.md) and guides for
[ChatGPT](docs/CHATGPT.md), [Claude](docs/CLAUDE.md) and
[Gemini](docs/GEMINI.md). Adapters never relax scientific or ethical controls.

For **each response**, in the researcher's active conversational language:
state confirmed facts, material uncertainty and the next valid action.
Avoid flooding an inexperienced researcher with internal record names
when the MINIMAL view suffices. Neither a ZIP, release badge, citation
metadata nor a successful engineering CI job validates research quality.
Apache-2.0 for the software does not grant rights over third-party PDFs.
