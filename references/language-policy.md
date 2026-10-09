# Language policy — English source, user-language interaction

## Scope and precedence

The canonical repository, Skill instructions, developer documentation, tool
descriptions and human-maintained configuration text are authored in **English**.
"Meu Artigo" and "C.A.D.A." are proper names and must not be silently renamed.
Existing machine-readable identifiers, legacy paths, DOI strings and bibliographic
titles are stable identifiers, **not language preferences**.

**The repository's authoring language is NOT the assistant's response language.**
A researcher using the installed Skill does not need to install a translation
pack, select Portuguese, change account language or edit `SKILL.md`.

When answering the researcher, use this priority:

1. Explicit language instruction in the user's current message.
2. Otherwise, the language of the user's latest **substantive direct message**
   (not quoted source text, pasted paper, code, sample prompts or tool output).
3. Otherwise, an explicit interaction-language preference already established
   in the current project or conversation.
4. Otherwise, the language clearly established in prior substantive dialogue.
5. Otherwise, use a supported user-interface/account language where actually
   available; if no reliable signal exists, start in English and allow a change
   with a simple user message.

Follow the user's language changes during the conversation. For example,
a direct question written in Brazilian Portuguese receives a Brazilian
Portuguese answer; a later direct English question normally receives English,
unless the user explicitly asked to keep Portuguese. If the user mixes
languages, use the dominant request language or their explicit preference.
Do not infer a language from nationality, name, location, institution,
repository language, citation titles, journal language or the Skill's
English installation prompt.

**Every user-visible conversational element** follows the interaction language
where possible: onboarding, clarifying questions, scientific decisions,
C.A.D.A. next-action summaries, warnings, errors explained by the assistant,
progress reports, final replies and ordinary user-facing drafts. Localize
explanations of command output without pretending its underlying structured
values were translated or modified. Preserve user-provided text verbatim
when it functions as original evidence. A researcher may always say
"Responda em português", "Answer in English" or an equivalent instruction.

## Manuscript, evidence and tool data: independent languages

The **manuscript language** is a separate decision based on the selected
journal's official author instructions or the researcher's explicit request.
A researcher can speak Portuguese while writing an English manuscript, or
speak English while drafting a Portuguese manuscript. Never silently
translate the manuscript, questionnaire, participant statements, search
queries or direct quotations merely to match the conversation language.

If a translation is specifically necessary, preserve the original,
mark translations transparently and retain source/locator provenance.
Respect confidentiality and the legal right to process/translate documents.

Machine-readable fields, enums, paths, API names, DOIs, command-line options,
SHA-256 digests and existing scientific IDs remain exactly as defined in the
schema (e.g., `GATE-0006`, `HUMAN_CONFIRMED`, `UNVERIFIED`).
These are stable protocol tokens, not text to be localized.

## Configuration contract

Projects may store these independent, non-identifying settings:

- `interaction_language_mode: "AUTO"` (default). The assistant follows
  the language of the researcher's substantive requests as described above.
- `interaction_language: "auto"` (default). A valid BCP-47 language tag
  such as `pt-BR`, `en`, `es` is allowed only when the researcher
  explicitly selects a persistent preference.
- `manuscript_language: "undecided"` (default). Use a BCP-47 tag only
  when the researcher or journal has specified the manuscript language.

No language auto-detector is falsely claimed to have run; the assistant's
recognition of conversational language is an LLM interaction behavior, not
a deterministic script result. Any manually specified preference must be
traceable to the user's actual choice. For existing projects missing these
settings, behave as AUTO; do not rewrite historical project decisions.

## User-visible examples (illustrative, not empirical tests)

| Researcher's direct message | Conversational reply | Manuscript language |
| --- | --- | --- |
| "Quero começar um artigo científico." | Portuguese | Undecided until the journal/researcher chooses |
| "I want to design a qualitative article." | English | Undecided |
| "Quiero revisar la literatura científica." | Spanish | Undecided |
| "Responda em português; o artigo será em inglês." | Portuguese | English |
| "Please keep replying in Spanish." | Spanish until superseded | Unchanged |

These rows illustrate the instruction; they are not evidence of model
accuracy in live multilingual sessions. Future functional evaluation should
use legitimate researcher interactions and record observed deviations.

## Security and scientific integrity

Language adaptation must not change gate decisions, source facts, citations,
research scope or evidence statuses. A translated answer with plausible
claims is not stronger evidence than the original. Keep the required
human gates and the storage authorization flow unchanged.
