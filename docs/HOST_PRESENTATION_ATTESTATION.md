# T02 acceptance: immutable release bytes and host-managed presentation

The RC.1 package contains an immutable `BUNDLE_MANIFEST.json`. Upon saving a
Skill, ChatGPT can modify **two** platform-managed presentation files:

- `agents/openai.yaml`: YAML reserialization and host policy injection
- `assets/icon.svg`: replacement by the platform's default icon

This does not by itself prove malicious tampering. It also must never justify
silently modifying the source manifest, ignoring two hashes, or approving
unrelated payload modifications.

## Acceptance policy

**Strict default:** `verify_installed_bundle.py` checks the original SHA-256
of every installed file. Any mismatch remains `FAIL`.

**Reviewed host presentation:** the verifier may report `status=PASS` and
`integrity_mode=CORE_EXACT_HOST_PRESENTATION_ATTESTED` only if:

1. Installed `VERSION`, manifest version, and build identity are correct.
2. The installed manifest SHA-256 is identical to a checksum independently
   obtained from the release ZIP and supplied as a CLI argument.
3. **Every other** program file, reference, document, and script matches the
   original manifest byte for byte.
4. The ONLY mismatches are the two allowlisted presentation paths above.
5. An external operator-reviewed receipt records the original SHA-256 and the
   exact post-save SHA-256 for each transformed asset, ChatGPT host identity,
   actual save/readback evidence, and substantive review of the transformed
   content. The receipt must match the **currently installed** bytes.
6. The observed SVG passes a conservative XML safety check; the YAML remains
   UTF-8 and contains a recognizable interface. These structural checks are
   insufficient alone: the operator must review the actual policy changes.
7. The receipt does not imply review of scientific content, authorization to
   redistribute PDFs, identity of the actual host through cryptographic
   attestation, or approval of research gates.

This receipt is an explicit, auditable *operator review* of observed bytes,
not a signature supplied by the ChatGPT platform. High-risk installations
require independent authenticated evidence, such as a signed release or
external attestation. Without sufficient evidence, retain `NO-GO`.

## Host procedure

1. Download the ZIP produced by CI for the **exact SHA of the candidate PR**
   and independently verify its origin.
2. From a terminal outside the Skill installation, calculate the original
   manifest SHA-256 directly from that ZIP:

   `python -c "import hashlib,zipfile; z=zipfile.ZipFile('MeuArtigoSkill-v1.0.0-rc.1.zip'); print(hashlib.sha256(z.read('BUNDLE_MANIFEST.json')).hexdigest())"`

3. Install and SAVE the Skill. Identify the **actual persisted executable
   directory**, then run:

   `python scripts/verify_installed_bundle.py --root /ACTUAL/INSTALLED/SKILL`

   Under the strict default the verifier MUST return `FAIL` if the host
   modified the two presentation files.
4. Generate a draft receipt, never an automatic approval:

   `python scripts/verify_installed_bundle.py --root /ACTUAL/INSTALLED/SKILL --emit-host-receipt-draft > /SEPARATE/SECURE/host-receipt.json`

   The draft command intentionally exits with status 2. Initially,
   `reviewed=false` everywhere.
5. Inspect the **post-save** YAML and SVG against the exact source files.
   Review the host's added policies, default-prompt changes, external
   references, and SVG safety. Verify independently that the observed files
   were saved and reloaded by the host. Name the reviewing operator. Record
   `review_evidence` (at least 30 characters) and
   `host_save_readback_evidence` (at least 20 characters). Only after this
   actual review, mark `reviewed=true` for the receipt and each transformed
   file. No instruction can substitute a simulated host review.
6. Verify with the original manifest checksum from step 2:

   `python scripts/verify_installed_bundle.py --root /ACTUAL/INSTALLED/SKILL --expected-version 1.0.0-rc.1 --expected-manifest-sha256 ORIGINAL_MANIFEST_SHA256 --host-receipt /SEPARATE/SECURE/host-receipt.json`

7. Accept T02 only when `status=PASS`,
   `integrity_mode=CORE_EXACT_HOST_PRESENTATION_ATTESTED`, and the output
   explicitly names both host-managed assets while reporting zero unresolved
   payload mismatches. Keep the receipt outside the installed Skill. Avoid
   placing private installed policy contents in a public Pull Request.

**Mandatory failure:** any other altered payload, missing or incomplete
receipt, incorrect manifest pin, unknown host, executable SVG content,
beta-version executable, or modification after the operator's review.

## Other acceptance tests

- T06 XLSX: if `artifact_tool` is unavailable, keep canonical CSV files
  functional and record the XLSX visualization as an optional dependency
  limitation.
- T05/T33/T32/T34 retain their individual behavioral tests and evidence.
  A presentation receipt does not replace those acceptance cases.
- Never merge, force-push, publish a release, approve scientific gates,
  disclose private files, or distribute protected PDFs to manufacture a PASS.
