# F8 — mandatory F5/F7 signed high-watermark integration

Status: **IMPLEMENTED AS EXPERIMENTAL HOST CODE; OFFLINE TESTED ONLY.**
Live Google Drive create remains **disabled in the repository CLI**.

## Contribution provenance

- **Researcher / repository maintainer (user):** owns the original Meu Artigo
  initiative, the research questions, scientific methods, decision gates and
  authority for permitted Drive projects, independent review, merge/release.
- **Assistant-authored work in F8:** \`scripts/drive_f8_trust_gate.py\`,
  changes to \`scripts/drive_f5_operator.py\`, new failure-mode regression
  tests and this design record. These are proposed software engineering
  contributions, not researcher-written experimental evidence.
- **GitHub Actions:** executes offline tests; it neither authorizes scientific
  decisions nor establishes that a separate trusted store or real OAuth
  connection exists.
- **Google Drive:** a previous F6 read-only metadata observation of a
  disposable folder is independent real-provider evidence, but it is NOT
  F8 end-to-end remote journal/cross-session acceptance.

## Mandatory gate

A new F8 \`TrustedHeadBackend\` protocol declares:

    read_head() -> str
    compare_and_set(previous_head: str, new_head: str) -> bool

The executor must supply **an independent durable, access-controlled store**
whose compare-and-set is genuinely atomic among **all active writers** and
whose reads are independently verifiable. An in-memory test double, ordinary
local JSON file, unsigned file on the same host as the receipt chain, or
arbitrary caller-supplied hash is NOT adequate. The code cannot prove from
method names that a backend implements the contract.

Under the experiment-only host lock, an authorized *single* folder create
now requires this sequence:

1. Provider check of exact synthetic root ID/name, current remote journal
   and all-MIME folder inventory with complete official Drive pagination.
2. Verify the trusted-head backend's committed head against F7's complete
   HMAC receipt chain **and** the exact downloaded remote journal SHA.
3. Write a single OUTCOME_UNKNOWN intent locally; PATCH **existing** private
   remote journal file once, read back exact bytes, check SHA-256.
4. Seal a new F7 HMAC receipt of the verified remote intent.
5. Call backend CAS(previous_head,new_head), read the committed head back,
   revalidate signed chain and remote journal bytes. **Only then** allow
   exactly one Drive folder-create POST for the synthetic test item.
6. Regardless of ambiguous POST outcome, freshly inspect the parent (all
   types). Reconcile exact remote folder ID without repeating create.
7. If uniquely resolved, write RESOLVED journal remotely, download/check
   its bytes, seal another signed receipt, CAS the new head and revalidate
   head/chain/remote journal. **Only then** report VERIFIED_SINGLE_SYNTHETIC_CREATE.
8. If the response is ambiguous without an observed folder, leave
   OUTCOME_UNKNOWN and report blocking. Never attempt a second POST.
9. If CAS or readback fails, preserve all artifacts and stop. A newer signed
   receipt ahead of the trusted head indicates an interrupted/unresolved
   checkpoint. **Do not** silently delete or rewrite receipts to recover.

F5 now requires \`trusted_head\`, \`anchor_archive\` and \`anchor_key\`
for every \`execute=True\` invocation. The ordinary CLI intentionally
**does not construct or accept** an independent CAS backend yet. Therefore
using \`--execute-synthetic-create\` on that CLI **blocks before issuing any
Google Drive write**, rather than falling back to an insecure mock. The
read-only default remains available.

## Synthetic acceptance and interruption coverage

The tests use a fake remote Drive client and an in-memory atomic-store
double only as behavior simulators. These do NOT provide real secret
management, independent persistence, distributed concurrency guarantees
or Google OAuth authentication.

The F8-augmented suite exercises:
- success with **three** chain receipts (initial, OUTCOME_UNKNOWN, RESOLVED)
  and exactly **two** successful trusted-head compare-and-set transitions;
- a single create when the simulated POST reports an ambiguous error after
  its effect, with no retry;
- no create and a preserved pending intent when the POST has no effect;
- refusal to create with missing backend, missing archive, invalid key,
  wrong/stale trusted head or a failed remote journal checkpoint;
- no create after CAS rejection or stale CAS readback, even though remote
  journal content was written and the new receipt file may exist;
- failure to claim finished when the final RESOLVED head CAS is rejected
  after a simulated create; a second invocation must not POST again.

The original scientific gates are not edited or approved by these tests.

## Unresolved prerequisites for real acceptance

- Implement, review and provision a real trusted high-watermark CAS service
  isolated from the receipt archive, with persistent verified state across
  independent executor sessions. Persist the initial F7 head *before* enabling
  the F5 flow.
- Integrate an authenticated Google Drive v3 executor with only necessary
  OAuth scopes. ChatGPT Drive tool credentials are not exported to Python.
- Demonstrate complete all-MIME paginated root scan; the connected
  folder-only search result is insufficient for any create authorization.
- Perform a single authorized, disposable Google Drive test with remote
  journal readback, trusted-head CAS and actual process interruption/resume.
- Review that cross-host writers cannot evade the shared high-watermark.
  Google Drive does not by itself offer a global transaction for a folder
  creation plus audit journal write.
- Obtain the researcher's explicit approval for any merge, publication,
  deployment or modification of real research projects.

**Go/no-go: NO-GO for merge/live create.** F8 closes the previous
unconditional host-path gap at source level, but does not constitute real
authenticated cross-session acceptance.
