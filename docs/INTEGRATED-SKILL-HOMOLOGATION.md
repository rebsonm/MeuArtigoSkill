# Integrated Skill acceptance — single candidate line

**Candidate basis:** PR #67 (science-safe continuation), PR #68 (conversation
resume) and PR #69 (guided blocker review), in precisely that ancestry.
This integration branch is based on PR #69's reviewed head. The three
original PRs remain independent Draft reviews. The branch is **not** a
public release, not installed automatically, and not a merge to `main`.

## One source of truth

The stack reuses existing canonical `CONTINUIDADE.md`, DEC/TRACE,
seven scientific gates and C.A.D.A. The user-facing resume and blocker
guidance are read-only projections. They never make a scientific choice,
mark a task done, rewrite an original decision, consent to local storage,
or claim external Drive synchronization. The project must be selected
and its canonical location authorized before any real continuation.

No code from the separately experimental project-owned MCP Apps bridge
PR #66 is deployed or required. The installed Skill may use authorized,
already-connected host tools, where supported, but **importing the ZIP
does not connect, authenticate, host or expose an MCP server**.

## Reproducible local engineering homologation

The integration runs `python scripts/homologate_integrated_skill.py`
against disposable fictional project registers. Each scenario exercises
the **actual** `native_chat_dashboard.panel`,
`research_resume_brief.from_panel`, and
`research_blocker_guide.explain` in sequence. It compares the complete
synthetic file snapshot before and after the read-only workflow and
refuses any manuscript/private fixture prose in the exported report.

| Scenario | Required acceptance |
| --- | --- |
| Authorized local research ready | Suggest technical *candidate*, never execute |
| Missing DEC register | Report decision-provenance reconciliation |
| DEC with absent TRACE | Block unverified decision provenance |
| Method route/profile mismatch | Require method-profile reconciliation |
| Local copy of Drive-canonical project | Require actual authorized Drive access |
| Revoked local fallback | Refuse unauthorized local continuation |
| Stale recorded CADA_ID | Require comparison with original continuity |
| Pending method transaction | Require explicit human/operator recovery review |
| Missing scientific gate | Protect the seven-gate contract |
| Unknown task dependency | Block execution until dependency evidence checked |
| C.A.D.A. task lacks Next_action | Ask to inspect missing task step |

The GitHub release audit additionally runs the existing
software regressions, eight fictional research journeys, source-language,
package-integrity, documentation and provenance checks. The
integration JSON is uploaded only as a CI artifact explicitly labeled
`synthetic`. The acceptance harness itself is **excluded** from the
installable user Skill ZIP, which still contains its operational scripts
and trusted references.

### Execute locally (development only)

```bash
python -m unittest discover -s tests -v
python scripts/homologate_integrated_skill.py --output /tmp/integrated-skill-acceptance-synthetic.json
python scripts/build_skill_bundle.py
python scripts/build_skill_bundle.py --verify "dist/MeuArtigoSkill-v$(cat VERSION).zip"
```

Do not publish the generated build as a release without a separate
manual maintainer decision and version/tag procedure.

## MCP interoperability: narrow truthfulness levels

- **Static optional-tool contract:** verified in source/tests: no
  forced server dependency, discovery of actually exposed tools,
  permission checking, safe no-connection fallback and preservation
  of seven scientific gates.
- **Existing host tool smoke:** a prior ChatGPT session reported an
  installed Meu Artigo beta.4 Skill and a connected GitHub public-read
  tool operating in the same conversation; see
  [host acceptance](CHATGPT-MCP-HOST-ACCEPTANCE.md).
- **Not verified in this homologation:** installation of this candidate
  in ChatGPT, the *project-owned* MCP server, OAuth/user isolation,
  MCP Apps visual UI, runtime tool-to-Skill causality, real canonical
  Drive read/write/sync, or end-to-end research operation with actual
  participating researchers.

A successful mock/documentation test **must not be relabeled as a
working custom MCP connection**.

## Review gates to be satisfied before release

1. All local/software/packaging checks green on the **final candidate SHA**.
2. Review the cumulative Git diff from `main`, including permission,
   provenance, privacy and dependency paths. All changes still require
   an actual merge review.
3. Install that exact candidate package in a supported ChatGPT test
   environment; confirm its `VERSION` and instruction content.
4. Verify no-MCP fallback in the host with an unauthorized/unavailable
   tool; the Skill must remain usable and never claim tool success.
5. Verify a real read using a supported previously authorized tool,
   without promoting it to evidence of custom MCP Apps support.
6. If deciding to ship **our own** MCP service, separately connect the
   HTTPS server, test OAuth and per-researcher isolation, project-scoped
   read-only methods, and UI rendering. Those are *not* release
   prerequisites for a purely independent Skill.
7. Validate methodological breadth and usability through independent
   reviewers before claiming scientifically demonstrated reliability.

Until these conditions are satisfied, classify the candidate as
`ENGINEERING_HOMOLOGATION_ONLY`. Neither an approved software test nor
a human-authored fixture authenticates scientific judgments or real users.

## Merge and publication policy

This integration PR is a consolidated *review vehicle* against `main`,
not an instruction to merge. The three stacked Draft PRs are preserved,
and neither their branch history nor PR #65/#66 is rewritten. Decide
**one** merge strategy after final review to avoid merging the same work
twice; do not merge #67/#68/#69 and the consolidated candidate
independently into `main`. No installed Skill upgrade, tag, release
asset or remote server deployment is performed here.
