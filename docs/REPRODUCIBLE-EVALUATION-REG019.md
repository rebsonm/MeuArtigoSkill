# REG-019 — Privacy-reduced controlled-evaluation replay

This is an **incremental software-evaluation artifact**, not independent
scientific validation or a replacement for the established RO-Crate/PROV
exporter at scripts/export_provenance.py.

## Contents

- CASE_CATALOG.json: the actual frozen **synthetic** negative-case catalog.
- PROTOCOL.json: procedural steps, expected categories, input hashes and
  explicit nonvalidated-scope flags; optionally the SHA-256 of an authorized
  project's canonical research protocol (no raw protocol content).
- OBSERVATIONS.json: actual **supplied** evaluation-run actions when a valid
  REG-001 ledger is provided. Each evidence-reference string is replaced by
  its SHA-256; the file includes the exact source commit, case-set checksum,
  per-case state, recomputed observed/matched/missed counts and original ledger
  entry hashes. An empty ledger or omitted --ledger means NO_OBSERVED_RUNS.
- README.md: replay instructions and limits.
- MANIFEST.json: SHA-256 for each packaged member.

These artifacts form a reproducible **scoring demonstration**; they do not
prove the existence or truth of remote evidence. A reviewer needs separate
legally authorized evidence access to verify source content and the original
chain of observation logs.

## Offline commands

Build a neutral package with no observed research activity:

    python scripts/evaluation_package.py build \
      --catalog benchmarks/critical_cases_v1.json \
      --output /authorized/output/controlled-evaluation.zip

Build using actually recorded REG-001 runs (never fabricated):

    python scripts/evaluation_package.py build \
      --catalog benchmarks/critical_cases_v1.json \
      --ledger /authorized/secure/evaluation_runs.jsonl \
      --project /authorized/project \
      --output /authorized/output/controlled-evaluation.zip

Independently validate file hashes and recalculate every recorded outcome:

    python scripts/evaluation_package.py verify \
      /authorized/output/controlled-evaluation.zip

REG-001 can store an optional evidence reference on a NOT_EVALUATED case.
REG-019 preserves an optional *hash* of that reference without treating
it as execution. Both a null and a valid SHA-256 are accepted in this
unevaluated state, with observed count remaining zero.

The strict verifier rejects archive tampering, duplicate or unexpected
members, changed case IDs, inconsistent expected outcomes, missing source
revision IDs, altered result counts and invalid original ledger pointers.
It does not extract ZIP contents to disk and checks declared payload bounds.

The package is reproducible for identical inputs: archive member ordering,
serialization and ZIP timestamps are fixed. The converter does not modify
canonical project data or send anything over the network. It refuses to
overwrite an existing archive.

## Scientific, security and privacy boundaries

The default archive contains **no** raw protocol content, confidential
bibliographic metadata, DOI list, full texts, researcher identities,
review narratives, file paths or original evidence-reference strings.
Original ledger-entry SHA values are informational pointers only; the
complete external ledger hash chain cannot be independently verified from
this privacy-reduced export alone.

An entered result remains **self-reported software observation** until a
qualified reviewer accesses and independently evaluates its evidence.
The exporter never executes LLM evaluations, checks semantic entailment,
authenticates an evaluator, certifies results or approves any of the seven
human scientific gates.

For confidential or authorized source-level distribution, use the
existing PRIVATE or properly authorized COLLABORATIVE flows described in
docs/EXPORTACAO-SEGURA.md rather than weakening this export's boundaries.
External release, copying into a public Issue or reuse in a journal
supplement still requires human privacy, copyright and research-ethics
review. Even a hash list can reveal membership in a known private corpus.

## Work remaining for full REG-019 acceptance

A real research protocol and authorized corpus need independent audit;
replay must be tested by someone other than the developer; the environment
and model configuration should be captured in controlled evaluations;
negative controls, false positives, unrecognized failure types and case
coverage must be documented before any scientific performance claims.
