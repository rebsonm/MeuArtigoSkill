# Using Meu Artigo with ChatGPT

Meu Artigo is a **Skill**, not a replacement for ChatGPT. Its research guidance works through the normal conversation, provided your ChatGPT account supports importing and running the Skill.

## Start using the Skill

1. Download the prepared [beta.6 Skill ZIP](https://github.com/rebsonm/MeuArtigoSkill/releases/download/v0.9.0-beta.6/MeuArtigoSkill-v0.9.0-beta.6.zip) from the [currently published release](INSTALLATION.md).
2. Import it using the **Skills** feature if it is available on your account.
3. Begin in your preferred language:
   > I want to use Meu Artigo to prepare a scientific article. Please check my available connections and storage before proposing methodological options.
4. Review the recommendations and decide what you want to adopt.

You do not need to open a technical dashboard to begin. The Skill is designed to offer a useful summary and next-step guidance in the conversation itself.

## When returning to an article

Say *"Meu Artigo, let's continue my article on [topic]"*. When an authorized saved project is accessible, the assistant should tell you where the recorded work stopped, what decision is pending and which step can safely follow. It should not assume that *"next"* means approval of a scientific choice.

If a file is unavailable, the research decisions are inconsistent or storage access has not been confirmed, the Skill should explain the blockage and suggest a safe check. It must not invent an approval, a restored file or a completed synchronization.

## What about my Google Drive and research services?

Installing the Skill does **not** grant access to Drive or databases. Connection status should be presented in a short, readable explanation rather than empty tables. A service is **NOT_VERIFIED** until actual access is checked; for saved files, an authorized write and, where possible, **read-after-write** confirmation are distinct from a successful read. ChatGPT can use only services actually connected and authorized for the current conversation. The assistant should distinguish accessible services from a successfully completed read, write or query.

Google Drive is preferred for long-term project continuity after a real writable-access check. When a project is saved there, expect actual folders and files that you can open individually, not only a ZIP or probe file. If folder creation fails or its outcome is uncertain, the Skill must inspect the actual Drive parent and consult the persistent creation journal. It must not automatically try the creation again. If complete folder listing or recovery of the saved operation history cannot be verified, creation should be paused safely. Optional API helpers require separately authorized secure execution; connecting Google Drive in ChatGPT does not activate them. The guard reduces duplication risk but cannot prevent creations by independent actors; pre-existing duplicates or inconsistent parent IDs must be reported and blocked for review rather than silently cleaned up. The assistant should provide a project link and tell you whether the structured delivery was fully verified or remains incomplete. Switching to another workspace requires your express agreement.

## Do I need an additional app or MCP connection?

**No additional connection is required just to use the standalone Skill's guidance.** If your ChatGPT session already exposes authorized MCP tools, the Skill may use them for specific tasks. Installing the Skill does not itself create an MCP connection, install a separate server or activate a visual MCP Apps interface.

If no MCP connection is available, **continue as a normal Skill** using already authorized tools or verifiable manual research materials. A separate interactive interface does not appear **when its Skill ZIP is installed**. The experimental project-owned connection and its interactive interface have **not** been confirmed in a live beta.6 installation. If a connected service is not available, the Skill can still explain alternatives and work with files or tools already accessible, without claiming that an external action took place.

## How do I know which Skill version is running?

An assistant may inspect the local Skill's VERSION and, when actually
accessible, verify the BUNDLE_MANIFEST.json file hashes. This identifies
the **local files inspected**, not necessarily which Skill package the host
activated. A repository release or path name must not be substituted for
actual installed-package evidence. If the host does not expose the
installed bundle, the correct answer is **installation not verified**,
with the observed source and its limitations.

When an optional XLSX visual dashboard is unavailable, the core protocol,
CSV tables and continuity may still be usable. Ask for a readable status
that distinguishes core readiness, optional visual status, and actual
remote Drive persistence, which is a separate operation.

## What remains your responsibility?

You choose the method, decide which materials to include, examine evidence, approve interpretations and review the manuscript before any submission. See [Getting started](COMECE-AQUI.md) and [scientific governance](GOVERNANCA-CIENTIFICA.md).

**Version note:** the [v0.9.0-beta.6](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v0.9.0-beta.6) installer is published. The corrections in open GitHub PRs must not be reported as installed or published until a separately authorized, verified build is actually loaded.
