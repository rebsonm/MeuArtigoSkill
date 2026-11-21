# Optional methodological consultation — Skill-only route

**SKILL_ONLY_NO_SERVER_REQUIRED.** This is an instruction/reference module inside the installable **Meu Artigo Skill** ZIP. It does not define or require a remote protocol server, endpoint, daemon, tokens, OAuth, hosted backend, vector DB service, background sync, private Drive access or any action outside the user's host capabilities.

## Activation

Use this guide only when the researcher's actual question involves selecting, comparing, justifying, correcting or critically assessing research methods; do not inject a 100-card library into every interaction. Preserve the user's language, research question and researcher's own consequential choices. Consult the bundled methodological index first.

## Capability-aware procedure

1. Identify the research decision: research philosophy/design, integrative versus systematic versus scoping review, qualitative coding, sampling, causal identification, mixed-method integration, DSR, evidence synthesis or integrity.
2. **If reliable Python + HTTPS are both available and explicitly permitted**, an optional read-only bundled script may retrieve a maximum of a few relevant records from the pinned public GitHub commit:
   - `python scripts/consult_public_methodology.py --question "..."` for original editorial [I] guidance and separately licensed public PDFs. This does NOT silently download the complete library.
   - `python scripts/consult_source_registry.py --question "..."` for 475 bibliographic **[P] prospects only**, not author conclusions.
3. **If Python/HTTPS is unavailable**, use only the packaged `references/INDICE-METODOLOGICO.md`, `references/methodological-foundations.md` and relevant method-route docs. If the host has an authorized native web/document reader, it may consult publisher webpages without pretending to have executed Python; never treat native browsing as proof of the private corpus.
4. Select **at most three pertinent leads by default**, justify relevance to the user's real design, and explicitly label each result: [P] unverified prospect; [I] original editorial analytical guidance; [L] primary source actually inspected with the relevant claim and page/location verified. A DOI/hash/abstract or publicly visible metadata alone cannot upgrade to [L].
5. Present one best-supported methodological option, competing interpretations where material, concrete limitations and the researcher's decision point. Consult actual primary sources before supporting manuscript claims.
6. A missing relevant item, unavailable connection, mismatched hash, unsupported parser, license uncertainty or contrary evidence is a **stop/fallback state**, never a reason to hallucinate a citation or fetch a private PDF.

## Selection integrity

- Do not equate PRISMA with a review method; it is primarily a reporting guideline. Match chosen review approach to the research aim, corpus and inference.
- A technical test suite verifies software behavior, not scientific correctness. Do not approve gates, infer method validity or claim a researcher review.
- Some works oppose GenAI in reflexive qualitative traditions while others discuss assisted analysis; show the relevant methodological disagreement rather than silently imposing the Skill author's preference.
- Use only publicly licensed exact PDFs in the public catalog when host extraction is authorized. Copyrighted literature cannot be redistributed as full-text PDF or substituted by serial derivative MD cards.
- GitHub is public storage of allowed editorial material and separately licensed PDFs, not a remotely hosted service or live research execution backend.

## Evidence and acceptance boundary

The external bibliography audit under `knowledge/methodology/intake/PUBLIC-WORK-BIBLIOGRAPHY-AUDIT-12.json` tracks 12 publicly corroborated works without claiming the privately inventoried editions were read. It is **source-development evidence**, not installed source data: the installable ZIP intentionally excludes `knowledge/`. Any genuine scientific review must separately inspect the relevant source and record a human reviewer, decision and limitation.
