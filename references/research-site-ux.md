# Approved blue website layout — optional research interface

## User's approved design, and assistant engineering

The researcher approved the website-style Meu Artigo interface (left
navigation, blue official logo, blue KPI/controls) and requested an
accessible, readable selected-method state. This visual direction and the
original Meu Artigo scientific workflow come from the researcher.

The assistant implemented \`assets/research_site.html\`,
\`scripts/build_research_site.py\` and \`tests/test_research_site.py\`.
This is assistant-created code, subject to review. The GitHub Actions audit
is a software test, not independent validation of UX, scientific quality or
a deployment of a ChatGPT-native application surface.

## User-visible layout

Ten navigable sections:
Overview, Steps, C.A.D.A. Tasks, Sources/Searches, Evidence,
Human Validations, Methods, Traceability, Submission and Sync.

The official SVG art from \`assets/icon.svg\` replaces the earlier "MA"
avatar in the website header. Official blue shades \`#0B57D0\` and
\`#2563EB\` lead the color system.

In Methods, selected options have a pale-blue fill, sufficiently dark
blue heading and description text, distinct blue outline, and a solid
blue exploration pill with white lettering. Keyboard users receive a
visible focus outline; selected options expose \`aria-pressed\`. Hover
is not the only selection indicator. Selected methods are **exploration
only** and are never automatically committed to scientific records.

The website adapts to a small/mobile screen without changing research
state or adding cloud permissions.

## Generate without an actual article

Run in the project repository's Python environment:

    python scripts/build_research_site.py --preview-route QUALITATIVE --output /tmp/meu-artigo-demo.html

Open the new HTML file in a regular browser. This preview retains
clearly fictional example numbers, sample gates and illustrative tasks.
It must not be sent to reviewers as evidence of a real article.

## Generate from an authorized existing LOCAL project

    python scripts/build_research_site.py --project /authorized/research/project --output /safe/private/project-site.html

The generator reuses the established, read-only
\`build_research_workspace.model\` projection. It produces a new
\`0600\` output, never overwrites one, and does not call cloud APIs.

A genuine authorized project displays only whitelisted fields from the
local projection:
- recorded tasks (not inferred task completion);
- gate approvals marked as **documented**, not authenticated;
- existing method route and next-action classification;
- observed data counts where source-backed.

The live local view always marks Drive sync, source audits, journal
submission and independent scientific validation as **unverified**,
unless those are separately established outside this view. It never
displays the fictional demo numbers as real results.

The output is an inert JSON data block with HTML-special characters
escaped, plus a strict policy that disallows outbound connections,
external scripts and form submissions. All dynamic UI strings are
HTML-escaped before insertion. Canonical files and gates stay unchanged.

The local HTML is a **snapshot**, not a persistent hosted application.
To refresh, re-run the generator to a new filename after rechecking the
authorized source; do not assume it is synchronized with Google Drive.
For actual Drive-canonical projects, validate authorization and read
the original records using the connected service rather than treating
a local mirror as authoritative.

## Integration and deployment limitations

This phase implements the approved web interface in the software
repository and tests the isolated HTML plus read-only model generator.
It does **not** automatically replace the installed private ChatGPT
entry-point with a hosted application, nor does it install an independent
external UI service or enable Drive writes. The ChatGPT conversation
dashboard and this optional website are distinct surfaces sharing
governance requirements.

The seven human scientific gates remain researcher-governed. Navigating,
exploring methods, filtering, reviewing draft text or opening a site
must never approve gates or create Drive folders.

Full host-native testing, actual authenticated Drive readback and
separate maintainer authorization for merge/release/installation are
still required.
