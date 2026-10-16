# Adaptive Research Map — methodological alternatives (experimental)

This read-only orientation prototype **does not replace** existing
methodological governance, source evidence, the canonical project profile,
C.A.D.A. control, researcher decisions or the seven human scientific gates.
It is not a new universal research methodology, a copied research canvas,
an AI-chosen "best method" or a validated teaching intervention.

## Rationale

A researcher can benefit from seeing **several defensible alternatives**
when documenting a methodological choice, with:
* what question each route might suit;
* what it can and cannot justify;
* changes to materials, evidence and analysis after the choice;
* whether human choice or independent scientific judgment is required.

The guide draws method families from the existing METHOD_PROFILE schema and
REQUIRED_DESIGN fields. It has 8 current operational routes; `UNDECIDED`
and `OTHER_NOT_LISTED` remain first-class possibilities.
A philosophical argument, mathematical proof, historical inquiry, normative
study or a hybrid design must **not** be forced into a limited menu.
An unlisted route needs deliberate methodological mapping rather than
automatic casting into an existing gate.

## Demonstrate without a project

    python scripts/adaptive_method_guide.py
    python scripts/adaptive_method_guide.py --preview-route QUALITATIVE
    python scripts/adaptive_method_guide.py --preview-route QUANTITATIVE
    python scripts/adaptive_method_guide.py --preview-route MIXED_METHODS

## Inspect an authorized project without changing it

    python scripts/adaptive_method_guide.py /path/to/project
    python scripts/adaptive_method_guide.py /path/to/project --field material_sources

The router reads only the already recorded methodological route and
the field-completion state. It does **not** expose question text, source
passages, interview material, human rationale or private paths. If a
PROFILE is missing, unsafe or contradicts config it fails closed.

The native dashboard's `method_guidance` view shows up to
three unranked options plus "Another approach" in MINIMAL mode, with
an explicit incomplete-view flag and option total. FULL returns all.

No candidate is automatically ranked, selected, committed or allowed to
change a gate. Filled fields are not proof of scientific adequacy. A human
researcher must make an attributable, documented choice through the existing
method-route decision workflow. The model must not invent a human's
answer to fill `METHOD_PROFILE.json`.

## Operation and remaining limitations

This is **static epistemic orientation**, not a scientific
recommendation model: a request's substantive question is not automatically
parsed and no scholarly databases or external sources are consulted.
Method descriptions and examples need review by specialists across
disciplines, and user research is needed to know whether this experience
actually reduces confusion or work. The model is optional and
progressive: experienced researchers may ignore it or state a preferred
method from the start.

Human work is not required to browse examples or run the engineering
tests. Human researcher choice is mandatory to **confirm** a real method.
Future independent method validation requires external specialists.
Merge/public release require the maintainer's explicit authorization.

## Expanded route-aware decision choices

Researchers can now explore **five optional decision dimensions** without
being required to complete a generic methodological questionnaire:

    python scripts/adaptive_method_guide.py --preview-route QUALITATIVE --dimension sampling
    python scripts/adaptive_method_guide.py --preview-route SYSTEMATIC_REVIEW --dimension sources
    python scripts/adaptive_method_guide.py --preview-route QUANTITATIVE --dimension analysis
    python scripts/adaptive_method_guide.py --preview-route MIXED_METHODS --dimension inference
    python scripts/adaptive_method_guide.py --preview-route DESIGN_SCIENCE --dimension reporting
    python scripts/adaptive_method_guide.py /authorized/project --dimension sources

The available dimensions are `sampling`, `sources`, `analysis`,
`inference`, and `reporting`. Meaning depends on the declared research
route. For systematic reviews, source eligibility is **not participant
sampling**; in qualitative studies selection can be purposeful or
iterative; mixed-method strands may require different sampling plans.
Pure conceptual theory is **not forced into empirical participant sampling**.

Each option explains when it can be considered, what it may enable, its
limitations and implications for the next step, including appropriate
researcher judgment. Alternatives are **not ranked** or recommended on
the basis of a private question or a claim of computational expertise.
There is always a researcher-defined `OTHER_NOT_LISTED` route.

Where a dimension corresponds to an **existing** method-profile field,
it returns the canonical field name and whether a value is recorded,
without exposing the value itself or overwriting it. Dimensions without
a canonical field (especially results `reporting`) explicitly return
`ADVISORY_DIMENSION_NOT_CANONICAL_FIELD`. An inappropriate empirical
requirement reports `NOT_UNIVERSALLY_APPLICABLE`. Neither is silently
written into a canonical project.

Exploration and technical checks need **no human action now**. Confirming
the actual scientific method, sampling, analysis, inferential claims and
presentation is a **researcher decision**. Cross-disciplinary scientific
validation requires independent experts later; a maintainer must
separately authorize integration, merge and release.

## Conversational guidance (experimental, read-only)

The guide also exposes an ephemeral dialogue projection, integrated as
`method_conversation` in the existing native research dashboard.
The default `suggest` action displays up to **three unranked contextual
catalogue choices** plus `OTHER_NOT_LISTED`. This is a selection by
documented method route and requested decision dimension, **not** an
AI-generated semantic ranking of the private research question.

Researchers may request:
- `suggest`: short initial route-specific possibilities and their limitations;
- `explore`: details of one option, practical consequences and reflective questions;
- `compare`: side-by-side explanation of two explicitly selected alternatives;
- `all`: the complete route-specific catalogue, including unlisted traditions;
- `decision`: a request for the researcher's own attributable, justified choice,
  **without writing or approving** the chosen approach.

Examples, without changing any project:

    python scripts/method_choice_dialogue.py --preview-route QUALITATIVE --dimension sampling
    python scripts/method_choice_dialogue.py --preview-route QUALITATIVE --dimension sampling --action explore --option-id PURPOSIVE
    python scripts/method_choice_dialogue.py --preview-route QUANTITATIVE --dimension sampling --action compare --compare PROBABILITY NONPROBABILITY
    python scripts/method_choice_dialogue.py --preview-route CONCEPTUAL_THEORY --dimension sampling
    python scripts/method_choice_dialogue.py /authorized/project --action decision

Unknown option identifiers and incompatible fields fail closed. Neither the
dialogue nor the read-only dashboard export private research-question text
or original scientific reasons. A missing/contradictory method profile
produces reconciliation status rather than an invented decision. No
scientific gate, canonical register or Google Drive state is mutated.

**Human involvement:** suggestions, comparisons and technical tests need
no manual intervention. **A real researcher must decide** the actual
method and justify it; independent disciplinary experts are needed later
to claim scientifically validated guidance. **Merge and release** still
require explicit maintainer authorization. The current prototype is not
an interactive deployment to an end-user host; it is a tested dialogue
data contract and CLI plus native-panel projection.

## Synthetic end-to-end researcher journeys

The optional journey evaluator rehearses eight different **fictional**
routes from a synthetic research question through method-family discovery,
route-specific alternatives, explanation, comparison, an explicitly
**simulated researcher-like fixture choice**, a field-entry suggestion, and
the conservative human handoff.

    python scripts/simulate_research_journeys.py
    python scripts/simulate_research_journeys.py --output /fresh/temp/synthetic-journeys.json

The example cases are software fixtures, not a participant sample,
authoritative domain labels, external research papers, or a study of user
experience. All examples are marked `SYNTHETIC_FIXTURE_NOT_A_REAL_RESEARCHER`.
A fixture choice is **not passed** to
`scripts/choose_method_route.py`, so no researcher declaration, DEC/TRACE
entry, method-route confirmation or scientific-gate approval can be
forged. The output includes only route identifiers, scripted steps, labels,
hashed fictional questions, generic field suggestions and explicit
nonapproval flags. No raw questions or researcher rationale are exported.

A simulated field suggestion points only to an existing
`METHOD_PROFILE.json` route_detail if such a canonical field exists;
otherwise it is exploratory only. **No field is written.**
`next_step_router.py` is not claimed to have run, because its actual
decisions require a valid canonical project, continuity records and
authorized storage. The journey reports the *researcher action* still
required before a real method can be confirmed.

The evaluator can emit a report to an **existing directory under a new
filename**, refusing to overwrite an existing file. CI runs the script
without real providers and keeps the synthetic observation report as an
artifact. The route cases are **not** a scientific benchmark of method
appropriateness; results report engineering flow coverage, not scientific
success rates or real researcher productivity.

**Manual responsibilities:** No user action is needed to run this
synthetic rehearsal. A real researcher must select and justify the method,
approve substantive design decisions and comply with ethical requirements
where applicable. External disciplinary experts must independently assess
the guidance before claims of universal scientific adequacy. The maintainer
must explicitly authorize integrating PR #65, merging PR #66 or releasing.

## Preventive methodological field preflight (experimental)

The adaptive guide now includes `method_fill_preflight.py`, a **read-only
inspection step** before any existing methodological field is updated.
It is intentionally **not an automatic form-filler** or a new pathway
around real scientific decisions.

For an authorized existing project:

    python scripts/method_fill_preflight.py /authorized/project
    python scripts/method_fill_preflight.py /authorized/project --field sampling_logic
    python scripts/method_fill_preflight.py /authorized/project --dimension analysis
    python scripts/method_fill_preflight.py /authorized/project --field analysis_logic --option-id REFLEXIVE_THEMATIC --draft-file /authorized/local/draft.txt

The user supplies or revises the actual proposal. The guide identifies the
**existing** canonical method field when one exists, lists suggested content
elements and relevant option limitations, and checks the draft's technical
compatibility with the chosen route and field. The script never claims that
it wrote a decision, inferred scientific adequacy, validated evidence or
authenticated the person supplying the draft.

### Preventive checks

- Exact placeholder/workflow-status values such as `PENDING`,
  `NOT_EXECUTED`, `APPROVED` or `N/A` are blocked as field content;
  an ordinary discussion of an unfinished study is not automatically
  treated as a placeholder.
- An invalid field or an alternative from a different route is refused.
- Existing canonical choices are not overwritten merely because an
  assistant proposes new text; revision requires a separately documented
  researcher decision.
- Existing controlled vocabulary fields use the **current canonical
  enums**, such as quantitative inference aim or mixed-methods design.
- Unlisted methods and optional, noncanonical orientations (such as
  results reporting) require deliberate researcher mapping rather than
  inventing a new required field.
- Very short descriptions and unsupported declarations of "validated
  effectiveness" produce **cautions**, not fabricated semantic judgments.
- When input is a **preview**, the output always blocks canonical writing
  with `PREVIEW_NOT_CANONICAL_AUTHORIZATION`, even if the synthetic text
  looks structurally reasonable.

The confidential UTF-8 input is read locally with a size limit; reports
contain **only its hash, bounded status codes and generic explanations**,
not the raw proposal or any source text. The native chat panel includes
`method_fill_guidance`, a guidance-only projection with no write action.

`DRAFT_REQUIRES_HUMAN_REVIEW` means *only* that a supplied proposal did not
trigger the implemented structural blockers. It must **never** be translated
into "scientifically valid", "approved by the researcher" or "safe to
write automatically". The validated method, human authorization,
canonical-source reconciliation and any transaction/Drive synchronization
remain separate requirements. No direct field-writing method is introduced
here.

Eight fictional end-to-end routes now exercise this preflight and verify
that no preview document can be saved or counted as human approval.
Software regressions do not establish the scientific suitability or
cross-disciplinary validity of the written suggestions.

**Human responsibility:** None for producing explanations or running these
checks. **Real researcher approval is always necessary** before accepting
a particular field value; an independent expert review remains necessary
to claim validated methodological instruction across disciplines. The
maintainer must explicitly approve merging or releasing this experiment.


## Supported canonical method-field write path (human-authorized)

The opt-in \`scripts/commit_method_field.py\` command is the **supported**
methodological-detail write path for new route-aware projects. It integrates
the structural field preflight **before** a local canonical write, and
repeats the validation **inside** an existing recoverable method journal.
It does not silently migrate legacy or undecided projects, does not use
test-generated decisions as real consent and cannot authenticate the
researcher behind the evidence reference.

Usage **only after the real researcher has independently made and
documented the actual methodological decision**:

    python scripts/commit_method_field.py /authorized/project \
      --field material_sources \
      --draft-file /authorized/local/researcher-reviewed-proposal.txt \
      --decided-by "Actual researcher name" \
      --evidence "Real original decision message/reference" \
      --rationale "Researcher's genuine substantive justification with limitations" \
      --option-id DOCUMENTS \
      --researcher-reviewed

The command is allowed only in an **explicitly authorized WORK_FALLBACK**
local project (both `storage_mode=WORK_FALLBACK` and
`fallback_authorized=true`). A Drive-canonical local mirror is not a
writable authority for this CLI; it must use a separately verified
canonical Drive workflow. No automatic conversion to fallback occurs.
The command requires an already confirmed method route whose original
DEC record matches the canonical profile; a field from that route; a
genuine researcher-declared decision, reference and rationale; safe
unmodified canonical files; and no already closed/approved scientific
gate 2–7. Controlled enums and exact placeholders are blocked. A
previously populated field cannot be overwritten by an assistant
suggestion. Advisory warnings require explicit
\`--acknowledge-warnings\` **from the authorized researcher**, and this
acknowledgment never means semantic validation.

After accepted human declarations, the command writes only the approved
method \`route_details\` field and appends a new METHOD DEC record and TRACE
event under the existing five-file recoverable transaction. The project
method route, seven scientific gate records and project configuration
are not modified. A handled failure rolls back the five correlated
files; abrupt interruptions require explicit recovery via:

    python scripts/commit_method_field.py /authorized/project --recover-pending

The command does not echo confidential draft text, and its result is
\`DECLARED_RESEARCHER_METHOD_FIELD_RECORDED_NOT_AUTHENTICATED\`. This is
a **declared recorded decision**, not independent authentication or
scientific approval. It does not make Google Drive writes, and local
transaction success does not prove Drive synchronization.

### Independent defensive check at gate 2

The method gate validator now independently rejects exact placeholder
tokens within the required method-profile fields, even if someone edited
the JSON directly without using the authorized writer. Existing
controlled-vocabulary, method-coherence and declared prior-gate checks
remain enforced.

This is a **defense in depth, not a universal filesystem interceptor**:
direct editing of files or unsupported external write tools can bypass
the supported writer. Such edits are not guaranteed to be blocked at
write time, and the gate validator's structural checks do **not**
establish scientific validity. Real research may require other review
procedures before any actual method decision is recorded.

### Human responsibilities

- **Now, during engineering tests:** no action from the maintainer or
  research participants. Synthetic fixture actors are never real people.
- **For a real method-field commit:** an actual researcher must decide,
  review the exact field text and affirm the evidence reference and
  rationale. A CLI flag alone does not authenticate the person.
- **For disciplinary coverage/accuracy claims:** independent human
  methodologists and an appropriate evaluation protocol are required.
- **For integration, merge or release:** explicit maintainer authorization
  is still required. PR #65 remains separate.


## Intelligent continuity from the last declared scientific decision

The native research panel now includes a read-only
\`decision_continuity\` view, built from the **existing**
\`17_Decision_Log.csv\`, \`13_Traceability_Log.csv\`,
\`METHOD_PROFILE.json\`, \`11_CADA_Control.csv\`, canonical
\`CONTINUIDADE.md\` and the established \`next_step_router.py\`.
No additional tracking register or second C.A.D.A. task board exists.

It shows:
- the last **append-recorded** decision ID, type and recorded status,
  without reproducing a private research question, original decision
  text, reasoning, personal name, source material or task instructions;
- whether the latest recorded methodological-field change matches the
  currently stored text's original SHA-256 fingerprint, and whether a
  referenced TRACE identifier appears in the trace register;
- structural method progress: route, confirmed-in-record status, number
  of fields filled and **next missing required canonical field**;
- the next step decided by the existing C.A.D.A./gate router, identified
  by CADA_ID and/or GATE_ID, with technical versus researcher ownership;
- conservative blockers, including unverified canonical Drive storage,
  interrupted journals, conflicting method decisions and inconsistent
  C.A.D.A. continuity.

The view never marks a filled field as scientifically adequate. Logged
human-approval fields remain declarations requiring independent
verification where appropriate. The most recent decision means the
**last CSV append row**, not independently established chronological
ordering. A missing, malformed or conflicting log must be reconciled:
the assistant must not reconstruct a fictional human decision.

**Action responsibility and blocking rule:** where the authorized router
explicitly permits technical preparation, the panel points to the
existing CADA_ID without duplicating private Next_action text. If
authoritative storage, integrity, methods or decision records require
reconciliation, it must show that blocker instead of declaring any
scientific task automatically executable. A pending scientific gate or
unconfirmed method always requires a real researcher decision.

### Fail-closed resumption when decision provenance is incomplete

The Skill-only `decision_continuity.compose` refuses to advertise an
authorized technical C.A.D.A. preparation if the decision ledger is missing,
malformed or contains duplicate identifiers, or if a last recorded decision
cannot be linked to an existing TRACE row. A separate method profile blocker
also takes priority over otherwise eligible technical preparation. The
read-only `native_chat_dashboard.panel` now reconciles its outward
continuation status with these blockers so plain-text and native views do not
contradict the method/provenance checks.

A **readable but empty** DEC ledger remains a legitimate no-decision-yet
state and cannot be confused with missing evidence. The response only
reports technical identifiers and conservative blocker codes, not original
human rationale, task instructions or source text. No register is rebuilt
or written; seven gates remain governed by the existing human workflow.

**Human involvement:**
- Engineering and fixture checks: no user action.
- Actual method choices, field approval, decisions at the seven gates:
  real researcher action and evidence.
- Independent scientific/disciplinary validation: human experts later.
- Integration with PR #65, merge, publication: separate maintainer approval.


## Offline interactive research workspace — local UI prototype

A **self-contained, responsive HTML interface** is available to exercise
the adaptive map without deploying a server or changing the scientific
workflow. This prototype is an optional read-only presentation based on
the same \`native_chat_dashboard.panel\` / canonical method guides /
\`decision_continuity\` records. The source UI template is allowlisted
**by exact filename** in the Skill ZIP; arbitrary HTML documents remain
rejected by the public bundle allowlist.

To generate a **fictional example** (safe to share):

    python scripts/build_research_workspace.py \
      --preview-route QUALITATIVE \
      --output /existing/local/directory/fictional-research-workspace.html

To generate a **private read-only snapshot** of an authorized project:

    python scripts/build_research_workspace.py /authorized/project \
      --mode MINIMAL \
      --output /secure/local/directory/my-research-workspace.html

The output HTML is created **only under a new name**, with filesystem
permission 0600, and never overwrites an existing file or symlink.
Do not upload or publish private snapshots: the optional C.A.D.A. table
contains legitimate **task titles** from the authorized local project,
even though raw research questions, original DEC rationales and source
passages are excluded.

### What the researcher can do on screen

- See recorded research-method route, unvalidated field counts,
  latest declared DEC entry, the next responsible action and the
  **exact four-column** C.A.D.A. table;
- Switch among design/route, sampling, sources, analysis, inference
  and reporting views, with no forced empirical requirements;
- Explore a curated alternative, compare **two** selected paths side
  by side and use \`OTHER_NOT_LISTED\` to retain noncatalogued traditions;
- Type a draft and trigger **ephemeral local browser hints** for
  placeholders, controlled-vocabulary values, existing-field status
  and unconfirmed routes. The browser code is **not authoritative**:
  the Python \`method_fill_preflight.py\` and human-authorization
  procedures must be executed again before any canonical write;
- See the specific responsible human or technical action but **not**
  execute it from the browser or silently advance a scientific gate.

The HTML has **no network requests, external dependencies, local
persistent storage, background services, live host callbacks, or
write/approve controls**. A restrictive CSP and text-only rendering
are used; embedded JSON escapes \`<\` and other dangerous script-tag
characters. The model is a **point-in-time offline snapshot**; the
researcher must regenerate it after legitimate project changes.

The experimental UI is **not** an installed ChatGPT application, a
completed integration with a visual host, a Drive sync mechanism or
a researcher-usability validation. Its narrative alternatives still
come from the authored catalog: these are **not personalized semantic
recommendations** or peer-reviewed methodological advice.

**Human actions:** none to generate/run fictional previews or engineering
tests. A real researcher must still decide and authorize a method and
any canonical field; scientific coverage claims require independent
experts. The maintainer separately authorizes merge, distribution and
any later connected-host integration.


## Opt-in local read bridge (experimental)

The offline visual research workspace can now run as an **explicitly
started local web interface**. It is a step toward a versioned host
contract; it is **not a remotely connected ChatGPT application**, a
deployed service or an installed account feature.

Start a **fictional example**, without a real research project:

    python scripts/local_research_bridge.py --preview-route QUALITATIVE

Start an authorized existing local project only when its owner has
approved local processing of the canonical files:

    python scripts/local_research_bridge.py /authorized/project --mode MINIMAL

The command binds only to `127.0.0.1`, on an OS-chosen port
by default. It prints only the constant status
`LOCAL_READ_ONLY_BRIDGE_READY` — no bearer credential, URL, project
metadata, port or filesystem path appears in stdout.

A session-specific URL is written temporarily to
`~/.meu-artigo-session-*/launch-url.txt` in the local user's home
directory. Locate the active file privately with your shell
(for example `ls -t ~/.meu-artigo-session-*/launch-url.txt`)
and open its contents only on the same computer. The temporary directory
has mode 0700 and its file mode 0600; they are deleted on normal exit
or handled SIGTERM. The URL is itself a credential: never share,
screenshot, archive or upload the file, its contents or related terminal
output.

The browser removes the session fragment from the address bar after
bootstrap. Stop the process to end the session. A forced kill or
machine crash may leave local artifacts: delete any stale
`~/.meu-artigo-session-*` directories only after verifying the
process has stopped. Never expose the port through a public proxy,
tunnel, shared network or cloud host.

### Actions and restrictions

| Route | Purpose | Permission |
| --- | --- | --- |
| \`GET /\` | Public fictional shell, **no project contents or token** | Loopback only |
| \`GET /api/snapshot\` | Re-read current local canonical projections | Read-only; session required |
| \`POST /api/preflight\` | Run the existing Python method-field draft checks | Read-only; session required |
| All other methods/paths | No support for writes, gates, decisions or Drive changes | Rejected |

The visual screen exposes **Atualizar dados locais**. This action fetches
fresh read-only C.A.D.A., DEC/TRACE, method, gate and continuity
projections; it clears drafts and selections to prevent stale bindings.
\`Conferir rascunho\` sends only the researcher's current field/dimension,
catalogue option and draft to the Python checker **on loopback**.
Response data include only structural finding codes, a fingerprint and
safe generic explanations, not the private text.

Security boundaries of the local prototype:

- Read API requests require an unpredictable, process-scoped token and
  the exact loopback origin; other origins, hosts and browser cross-site
  requests are rejected, with **no CORS access**.
- Browser responses require \`Cache-Control: no-store\`; requests are
  not logged by the service and transport runs on the local computer.
- The served HTML starts as a **fictional shell** with no project data or
  token. The browser reads the session fragment, clears the URL, then
  requests the private model via the authenticated API. A token-less
  browser cannot read actual project details. Same-origin API requests
  are permitted only in the served session; saved offline HTML retains
  \`connect-src 'none'\` and has no session token.
- No write/update/delete API exists. The existing controlled Python
  \`commit_method_field.py\` remains a separate tool, never callable
  from these endpoints. Human decisions and original evidence cannot be
  synthesized by an API call.
- Neither researcher authentication nor independent scientific validity
  is supplied by the session token. The user's OS account and local
  computer security remain relevant.

The bridge cannot read a connected cloud Drive directly, prove cloud
synchronization, install itself into the ChatGPT interface or safely
offer remote collaboration. A future ChatGPT-host adapter would require
an explicit trust model, external access policy, permission review
and separate authorization before any service is exposed.

**Human actions:** None to run the fictional engineering tests. A user
must deliberately start/stop the local process to view a live project;
all actual scientific choices and their authorized recording remain
human responsibilities. Independent evaluation, integrating PR #65,
merging PR #66 and publishing remain separately authorized tasks.
