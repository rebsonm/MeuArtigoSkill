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
