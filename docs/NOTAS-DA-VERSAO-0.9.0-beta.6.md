# Meu Artigo — v0.9.0-beta.6

**Last planned experimental beta for researchers, prepared 2026-10-15.** This is a **pre-release**, not a stable version, and does not establish independent scientific validation or proven improvements in article quality. The publishing workflow is manual; successful engineering tests do not by themselves make a GitHub release.

## Changes from beta.5

- **Scientific continuity and safer provenance:** the Skill checks actual DEC/TRACE links and methodological conflicts before offering to resume research. A technical C.A.D.A. task cannot override missing or inconsistent canonical scientific records.
- **Research continuation in conversation:** authorized local projects can produce a read-only summary of the latest recorded decision, existing responsible person, next task and blocking conditions. No scientific judgment or task is automatically approved or executed.
- **Explain impediments:** a bounded, safe catalogue explains known blockers and which original records to inspect, while protecting private research text and unknown untrusted codes.
- **Storage safeguards:** method writers require explicitly authorized local `WORK_FALLBACK`; Drive-canonical work cannot be silently treated as writable or synchronized through a local copy.
- **Optional host-tool use:** a Skill may coordinate tools that the user's host already exposes and authorizes. The standalone ZIP does not include, install, connect or authenticate the project-owned MCP server or expose MCP Apps interactive UI.
- **Integrated engineering checks:** candidate PR #70 at commit `200e1d1e0b5bb0664daf0e4427959c58c7ba5114` passed 758 automated tests, 11 fictional integrated continuation scenarios and eight fictional research journeys. Publication requires a new passing audit on the final versioned commit.

## Required scientific and product limitations

- **No independent scientific validation.** The seven human-controlled gates, original researcher decisions, evidence provenance and [L] consulted literature / [I] inference / [P] original proposition distinctions remain mandatory.
- **MCP Apps remains unverified:** no authenticated end-to-end test of our custom MCP server, OAuth, visual app or scoped Google Drive operations in this integrated beta. Importing the Skill alone cannot activate these features. The Skill can still be used without MCP, subject to actual platform tool availability and permission checks.
- **Real ChatGPT beta.6 installation not yet accepted:** the integrated code was tested in CI with synthetic fixtures, not in a live researcher installation. A host test should verify the installed version, no-MCP fallback and a truly authorized tool read before claiming real compatibility.
- **Cloud claims must be evidenced:** repository CI, a local receipt, or a copied project folder does not prove live Google Drive write or synchronization. No academic source access, authorship, human gate approval or journal submission is presumed.
- **No automatic update:** an installed beta.4/beta.5 stays installed until the researcher intentionally updates in a supported host.

## Install and report defects

After the manual tagged release is available, use the versioned `MeuArtigoSkill-v0.9.0-beta.6.zip` plus its release-specific `SHA256SUMS.txt` from [the beta.6 release page](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v0.9.0-beta.6), rather than GitHub's generic source-code ZIP. Until then, the [published beta.5](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v0.9.0-beta.5) remains available. Report sanitized steps, actual installed version and environment through [GitHub Issues](https://github.com/rebsonm/MeuArtigoSkill/issues), without sharing confidential manuscripts, restricted PDFs, private Drive links or credentials.

**Scope of 'last beta':** a *release plan*, not a guarantee that urgent security fixes will never be needed or that stable v1.0.0 has been approved. A stable release requires a separately authorized and evidenced decision.
