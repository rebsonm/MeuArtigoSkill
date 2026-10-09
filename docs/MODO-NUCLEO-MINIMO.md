# Progressive presentation — minimal core and full view

The **minimal presentation** reduces the amount of operational detail
shown to the researcher. It does **not remove** registers, checks,
human scientific gates or evidence requirements; the two presentation
modes share the same canonical data and safeguards.

Stage 4 also introduced a **progressive reference router** in
`SKILL.md`: only instructions relevant to the current scientific
problem, research route and gate should be loaded. Selecting references
is distinct from choosing MINIMAL/FULL presentation. See
[context routing by stage](../references/CONTEXTO-POR-ETAPA.md).

| Feature | MINIMAL | FULL |
| --- | --- | --- |
| Conversation | Next actionable step, decision and salient risk | Detailed trace, documents and open issues |
| Article screening | Consequential decisions and contradictions | Existing screening registers |
| Sources and claims | Material problems and required human review | Fine-grained evidence provenance |
| Human scientific review | Always required when applicable | Same requirements |
| Independent audit | No reduction in safeguards | Same safeguards |
| Data, tables and identifiers | Existing canonical schema | Same canonical schema |
| **Response language** | User's conversational language | Same conversational language |

New projects use `presentation_mode=MINIMAL` by default. Older
projects missing that configuration stay in FULL until a genuine
authorized choice is recorded. Mode selection never changes a
project's review family, search protocol, access rights or research
autonomy. The repository's English authoring language does not
change the researcher's conversational language.

For Python 3.10+ and an authorized local project:

```bash
python scripts/presentation_mode.py /project
python scripts/presentation_mode.py /project --mode FULL --confirmed-by "reference to the researcher's real request"
python scripts/presentation_mode.py /project --mode MINIMAL --confirmed-by "reference to the researcher's real request"
```

Mode updates affect only preferences in `PROJECT_CONFIG.json`.
They do not rebuild, alter or erase scientific documents, counts,
decisions or evidence. The text identifying the requester is an
audit statement, **not identity authentication**.

The prospective MINIMAL/FULL evaluation is specified in
`benchmarks/minimal_full_comparison_protocol_v1.json`;
no participant observations or actual benefits are asserted.
