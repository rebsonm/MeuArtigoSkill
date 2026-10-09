# Operational research-method routes — Meu Artigo

The scientific design is a **researcher decision**, not something
automatically determined by the AI model's tools, database access
or favorite method. This document operationalizes the conditional
methodological foundations in
[methodology](../references/methodological-foundations.md)
and [article/review design](../references/review-design.md).
The rules are software **workflow policies**, not external
instruments claimed to be authored or validated by the cited
methodologists.

The repository's documents are in English. Explain these choices,
scientific gates and limitations to the **researcher in the language
of their actual conversation**. Journal/manuscript language is a
separate choice: [language policy](../references/language-policy.md).

## 1. Researcher decision and safe continuation

- During project initialization, preserve the researcher's original
  problem and article description. `--article-type` is a descriptive
  label, not confirmed scientific classification; ambiguous labels
  remain `UNDECIDED`. Optional `--method-route` selects a provisional
  method-specific scaffold.
- The canonical planning document is
  `00_Gestao_e_Continuidade/METHOD_PROFILE.json`. It does not
  introduce a new decision identifier, worksheet or scientific gate.
- The chosen route becomes confirmed **only by a real researcher**
  with an attributable rationale and a reference to the original
  declaration:

  ```bash
  python scripts/choose_method_route.py PROJECT \
    --route QUANTITATIVE \
    --decided-by "Real researcher" \
    --evidence "ACTUAL_DECISION_REFERENCE" \
    --rationale "The researcher's substantive original rationale"
  ```

  The uppercase placeholders above must be replaced with
  **actual information**. The script does not create a researcher's
  response or authenticate the claimed person. It uses existing
  `DEC_ID` and TRACE provenance structures and preserves
  previously recorded project materials.

- Once consequential method/evidence gates have been concluded,
  automatic route switching is blocked. A real researcher must
  review the prior protocol, decisions and evidence before any
  deliberate migration. Never delete or reconstruct prior science.
- Older projects without
  `method_route_governance_required` are kept compatible without
  retroactively filling gates, authorship or decisions.

## 2. Method-specific routes

| Route code | Scientific question | Appropriate evidence or activity | What must not be universally imposed |
| --- | --- | --- | --- |
| `INTEGRATIVE_REVIEW` | What explanatory understanding results from critical integration? | Documented bounded search, source appraisal, thematic tensions and contribution | Pretending complete coverage merely because indexed databases were searched |
| `SYSTEMATIC_REVIEW` | What conclusion follows from a genuinely defined eligibility protocol? | Proportionate comprehensive search, selection, risk-of-bias assessment and synthesis | Calling a search systematic just because PRISMA was mentioned |
| `PROBLEMATIZING_REVIEW` | Which underlying assumptions should be questioned? | Theoretically purposeful literature, counterpositions and revision of assumptions | Exhaustive screening as an automatic requirement |
| `CONCEPTUAL_THEORY` | What mechanism, framework, proposition or argument is defensible? | Nearby research, lineage of concepts, alternative explanations and boundaries | Mandatory fieldwork or statistical tests for purely conceptual research |
| `QUALITATIVE` | What meanings, practices or organizational processes occur in context? | Cases, interviews or documents legitimately obtained and analyzed, reflexivity | Treating statistical inter-rater reliability as universally required for interpretive work |
| `QUANTITATIVE` | What descriptive, associative, predictive or causal inference is supportable? | Defined units, sample, measures, real data, executed statistical analysis | Calling an association causal without valid identification |
| `MIXED_METHODS` | Why and how must substantive QUAL and QUAN strands be integrated? | Distinct strands, actual point of integration, discrepancies and meta-inference | Claiming methods are integrated merely because both appear in a paper |
| `DESIGN_SCIENCE` | What artefact addresses a problem, and how is its evaluation supported? | Requirements, justified construction, actual evaluation and traceable results | Claiming effectiveness solely from the existence of a prototype |

If the intended design is genuinely unclear, use `UNDECIDED` and
present alternatives to the researcher. Do not invent consent or
pretend that availability of a survey, LLM or corpus implies a route.

## 3. Research Onion as a coherence check

The planning profile records six commonly discussed layers of
Saunders' **Research Onion**:
philosophical position where relevant; theory development logic;
methodological choice; research strategy; time horizon; and
techniques/procedures. It also asks for the coherence rationale
connecting question, intended inference, data and method.

These layers do **not** map deterministically onto particular
tools, results or epistemologies. The assistant must not
automatically assign a philosophical worldview from a method.
For empirical routes, the software only checks that a strategy,
procedures and coherence explanation have been documented;
their adequacy requires the researcher's critical evaluation.
For conceptual/review routes, every layer need not be separately
filled if it does not serve the research argument.

The `MINIMAL` interface shows the next substantive decision
and material risk. `FULL` can expose detailed records. The
**underlying scientific controls are identical**, and neither
presentation mode constitutes scientific validation.

## 4. Controls by method family

**Quantitative:** distinguish `DESCRIPTIVE`,
`ASSOCIATIONAL`, `PREDICTIVE` and `CAUSAL` claims before
proposing analysis. Record population/units, sampling,
constructs/measures, source data, analysis plan and
inferential limitations. For causal claims, specify a defensible
identification strategy and assumptions appropriate to the
research design; a regression coefficient alone is not a
causal estimate. Do not report power calculations, tests,
uncertainty intervals or significance as performed unless
they were actually executed and are traceable.

**Qualitative:** declare the relevant tradition, such as
phenomenology, narrative, grounded theory or case research
where appropriate. Describe the phenomenon/case, setting,
participant or material selection, analysis and reflexivity.
Quality criteria are tradition-specific; do not demand Kappa
or saturation for every interpretive design.

**Mixed methods:** document one of
`CONVERGENT`, `EXPLANATORY_SEQUENTIAL`,
`EXPLORATORY_SEQUENTIAL` or `EMBEDDED`; substantial
QUAL and QUAN strands; and integration mechanism
`CONNECTING`, `BUILDING`, `MERGING` or
`EMBEDDING`. Explain why integration is essential, the
time/analytic point and how disagreement will be examined.
A proposed integration plan is **not evidence of integration
performed**. A final claim of integrated results requires
reference to the real integration output.

**Design science:** separate knowledge of the practical
problem, artefact requirements, actual construction choices
and evaluation genuinely performed. A versioned prototype
does not demonstrate adoption, utility or effectiveness.

**Theory and reviews:** choose literature selection and
synthesis rules appropriate to the review family.
Only a review genuinely using bibliographic eligibility
and a bounded review corpus passes through literature
corpus-freeze controls. Source identification and provenance
remain traceable whenever scientific literature is used.

## 5. Same seven human scientific gates; method-adapted meanings

`GATE-0001`: research question and intended contribution.

`GATE-0002`: scientific route, method choice and appropriate
protocol, based on a traceable real researcher decision.

`GATE-0003`: relevant literature/search strategy or theoretical
positioning; the exact purpose differs across methods.

`GATE-0004`: either a **bibliographic corpus** for an actual
review or real **empirical materials/data/artefact construction**
for the corresponding method.

`GATE-0005`: actual synthesis, statistical/qualitative
analysis, mixed-method integration or design-science
evaluation, depending on route.

`GATE-0006`: provenance, limits, scientific claim
integrity, contrary evidence and actual researcher review.

`GATE-0007`: verified journal rules, manuscript
files, submission readiness and evidence of external actions.

These are the **existing identifiers**, not a new gate family.
Filling a spreadsheet cell, completing a C.A.D.A. task
or drafting a plausible LLM explanation does not approve a gate.
For new route-aware projects, each approval checks the
required prior state and the relevant method-specific evidence.

At `GATE-0004`, empirical routes require an actual
materials/data/artefact reference and an explicit record
that they have been obtained or constructed.
At `GATE-0005`, the relevant analysis/evaluation must
have really occurred, with original evidence recorded.
Mixed-method research additionally needs evidence of the
actual integration, not only plans.

A declared evidence state is an **auditable claim made
in a record**, not independent proof of research execution.
Original artifacts, source quality and actual researcher
review must still be inspected.

Do not mark `NOT_APPLICABLE` merely to bypass
methodological planning, empirical materials, substantive
analysis or scientific-claim audit. A genuinely irrelevant
literature-positioning substage requires a substantive
human rationale and evidence reference. If no journal
submission is intended, the submission gate may
remain pending without pretending it was completed.

## 6. Source lineage and epistemic limitations

- **[L]**: assertion supported by actual consulted evidence.
- **[I]**: bounded author inference with a stated warrant.
- **[P]**: original proposal with nearest prior works,
  a contribution delta and limits.

A DOI match or the presence of a document file is not
proof that its text semantically supports a claim.
See [evidence levels](NIVEIS-DE-EVIDENCIA.md).

No code in this Skill should claim to have performed a
survey, interview, analysis, artifact evaluation,
human approval, ethics decision or causal assessment
solely by populating a profile. An `APPROVED` record
requires a real human decision, but recording a person's
name does not cryptographically authenticate them.

Workspace content, AI use, permissions, participant data
and source licenses must be handled under the authorized
storage and sharing policy. A local file is not a proven
Google Drive upload. Journal rules and third-party PDF
rights remain applicable.

Neither these routing rules nor the software tests
constitute independent scientific validation of the
Skill or the effect of C.A.D.A. Independent evaluations
are listed in [pending validations](VALIDACOES-PENDENTES.md).
