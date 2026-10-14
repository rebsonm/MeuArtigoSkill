# FAQ and troubleshooting

> **Publication status:** beta.5 is the current source candidate awaiting a separate manual release. The [published beta.4 release](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v0.9.0-beta.4) remains the verified installer until beta.5 assets are actually available. Existing installed Skills do not update automatically.

### Do I need to know Git or programming?

No. For supported platforms, install the prepared **release Skill ZIP** rather than the repository source archive. Development and local scripts require more technical setup.

### Which version should I download?

The recommended **experimental** distribution is [v0.9.0-beta.5](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v0.9.0-beta.5). Its publication has not yet been verified. There is no stable release.

### Why does the assistant ask to check Drive first?

Research continuity needs a real, writable source of truth. Seeing a connected app is not proof that files can be saved. A local fallback requires explicit authorization.

### I have access to Scopus or Web of Science. Does the Skill search them automatically?

Only when tools, permission and actual execution are available. Otherwise it can prepare search strategies, guide manual retrieval and process real exported metadata. A proposed string is **not an executed search**.

### Are AI-generated screening proposals considered human reviews?

No. The researcher must make consequential inclusion/exclusion decisions. An AI cannot count as an independent second human reviewer.

### Why does a gate remain pending after I say "next"?

"Next" can ask for a workflow step; it does not prove informed approval of consequential scientific content. The corresponding real decision and rationale must be recorded.

### Can it make my article original or guarantee acceptance?

No. The system helps **document bounded novelty searches, provenance, methods and journal rules**. It cannot establish universal originality, acceptance, causality or complete scientific validity.

### Does the assistant answer in Portuguese?

The Skill instructs the assistant to follow the researcher's actual conversation language. The source repository is in English; journal/manuscript language is independent. Real multilingual compatibility still needs field testing.

### Can I share research PDFs from the project's package?

The Apache-2.0 license applies to the Skill code and original content, **not** third-party journal PDFs or confidential research data. Verify rights and anonymization first.

### Why does the dashboard not show my exact current progress?

A dashboard must read authentic, authorized records. If the workspace is unavailable, the correct response is **not verified**, not simulated project data.

### How do I report a problem?

Use [GitHub Issues](https://github.com/rebsonm/MeuArtigoSkill/issues) and describe version, platform, reproduction steps, expected/observed behavior and sanitized evidence. **Do not upload credentials, protected full text or private participant information.**

See also [installation troubleshooting](https://github.com/rebsonm/MeuArtigoSkill/blob/main/docs/INSTALLATION.md) and [[Status and limitations|Status-and-Limitations]].
