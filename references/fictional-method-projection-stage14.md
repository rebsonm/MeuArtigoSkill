# Stage 14 — Fictional method projection from historical #66

The exclusive old preview was reconciled as
`scripts/fictional_method_projection.py`, an isolated local-only
adapter sharing the current canonical `build_research_workspace.model`,
`adaptive_method_guide.preview` and `method_choice_dialogue.dialogue`.
It neither reimplements methodological rules in JavaScript nor adds
another server or registered remote tool.

It accepts fixed routes, MINIMAL/FULL, five optional decision dimensions
and five read-only catalogue actions: suggest, explore, compare, all,
decision. A decision result is only a prompt for attributable researcher
choice, NEVER a selection, approval, gate transition or persistence.

The eight operational routes and UNDECIDED remain from the one authority.
OTHER_NOT_LISTED is always a possible researcher-defined alternative,
not a compulsory ninth family. No semantic method ranking is claimed.

Examples:
```sh
python scripts/fictional_method_projection.py --route QUALITATIVE --dimension sampling --action suggest
python scripts/fictional_method_projection.py --route QUALITATIVE --dimension sampling --action explore --option-id PURPOSIVE
python scripts/fictional_method_projection.py --route QUANTITATIVE --dimension sampling --action compare --compare PROBABILITY NONPROBABILITY
python scripts/fictional_method_projection.py --route CONCEPTUAL_THEORY --dimension reporting --action all
python scripts/fictional_method_projection.py --route MIXED_METHODS --action decision
```

The existing protected optional server remains the sole host-facing
service; this script is NOT wired into it or exposed to network callers.
The historical second server, standalone widget and Node workflow from
#66 have been deliberately rejected as duplicate/obsolete distribution.
The tested data are synthetic; neither a real research project nor its
private material is accessed. External methodology validation, DEC/TRACE,
C.A.D.A., seven human gates, current scientific triage, Drive F1–F9 and
authorization rules remain separate and authoritative.
