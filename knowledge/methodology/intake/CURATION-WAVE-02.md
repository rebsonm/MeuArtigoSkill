# Source curation roadmap — archive coverage, not automatic full-text ingestion

Status: DRAFT / POST-v1 / SOURCE-ONLY. Last reviewed: 2026-11-21.

## What is in this draft branch

- Five public metadata-inventory parts enumerate **475 archive PDF records** across
  **75 top-level/nested categories**. There are **466 distinct filenames**.
  Filenames are not reliable work identifiers: identical names need not have
  identical content, and different filenames may refer to the same work.
- The separate public methodology library lists **23 original editorial cards**
  (19 explicitly marked as pending independent review, four earlier pilot
  summaries without an independent acceptance receipt) and **12 individually
  attributed CC BY 4.0 source PDFs**. These public sources can overlap the
  archive, so coverage must not be calculated by naïve subtraction.
- No evidence supports a claim that all 475 private/publicly shared PDFs were
  lawfully parsed, read, licensed, scientifically assessed or carded.
- Run the source-only `experimental/conceptual_rag/curation_progress.py`
  to regenerate the read-only inventory summary; no output modifies Drive,
  GitHub source documents, scientific gates or researchers' projects.

## Source review sequence (one source at a time)

| Priority | Archive theme | Proposed editorial outcome | Review boundary |
| --- | --- | --- | --- |
| 1 | Research design; epistemology; scientific writing | Method comparison/decision cards | Verify edition, actual method claim and primary bibliographic record |
| 1 | Literature review; content analysis; thematic analysis | Review and coding-practice cards | Keep named source boundaries; do not reprint copyrighted checklists |
| 1 | Case study; interviews; focus groups; qualitative sampling | Decision criteria and counterexample cards | Clarify analytic tradition, limits, participant and ethics constraints |
| 2 | Survey; measurement; factorial analysis; regression | Design diagnostics and assumptions cards | Prevent inferential overreach and preserve computational conditions |
| 2 | Difference-in-differences; RDD; instrumental variables; synthetic control | Causal design choice/assumption cards | Verify estimand, identification conditions and limitations |
| 2 | QCA; process tracing; mixed methods; longitudinal data | Comparative methodological routing cards | Differentiate logics of inference and quality criteria |
| 3 | Bibliometrics; text as data; network analysis; machine learning | Reproducibility and corpus-selection cards | Keep software behavior distinct from validated research claims |
| 3 | Digital ethnography; digital methods; AI-assisted qualitative analysis | Digital ethics and reflexivity cards | Do not expose private data or fabricate source consultation |

## Publication gate for every newly proposed source or card

1. Resolve a DOI or an authoritative original bibliographic record, including
   edition/version. Identify the actual text permitted for consultation.
2. **Binary PDF:** separately verify public redistribution rights for that
   exact file and retain publisher/repository evidence; a free DOI page or
   accessible personal-cloud file alone is insufficient. Prefer canonical PDFs.
3. **Protected work:** create a short, genuinely independent original editorial
   card without extended extracts, replicated original tables, translated
   passages, copyrighted diagrams or serial chapter-by-chapter substitutes.
   Do not present bibliography-only metadata as a read primary source.
4. Check semantic and epistemic fidelity against the original work actually
   inspected. Record limitations, counterexamples and reviewer evidence.
5. Separate rights/originality sign-off from scientific/fidelity sign-off. Only
   then promote card `editorial_status` to `ACCEPTED` in an approved review.
   Until then, return explicit provisional [I] guidance, never [L] evidence.
6. Test Portuguese, English and Spanish lexical retrieval, negative queries,
   page labels, checksum failures and access-denied fallback in a real
   authorized host. A CI result does not validate expert methodology judgment.

## Download failures requiring an authorized source route

The previous trial could not obtain PDFs for some openly described journal
articles because the publisher redirected to an identity portal or returned
HTTP 403. **Do not retry by bypassing authentication or weakening network
checks.** Keep their DOI/source links and original editorial cards; publish
an original PDF only after confirming the exact downloadable version and
applicable redistribution permission.

## Out-of-scope without further approval

Bulk copying the private archive, publishing copyrighted book PDF/Markdown
derivatives, uploading raw evidence to a third-party index, adding embedded
credentials, writing to researchers' Drive projects, scientific gate
approval, merge to main, tag, or release.
