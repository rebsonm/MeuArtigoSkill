<a id="validação-formativa-de-decisões-científicas"></a>
# Formative validation of scientific decisions

Skill conducts operational steps autonomously, but requires that relevant scientific transitions be understood and deliberated by the researcher. The goal is not to create a long questionnaire or have the model produce justifications on the user's behalf.

<a id="onde-se-aplica"></a>
## Where it applies

In new projects, `formative_gates_required=true` in `PROJECT_CONFIG.json` enables control in approvals from `GATE-0001` to `GATE-0006`. The seven existing ghats are preserved. `GATE-0007`, dedicated to file release and submission, maintains its own safeguards, without mandatory additional training response.

Old projects, without this option, preserve their compatibility; Enabling the mode requires an explicit migration decision. The feature uses only standard Python and existing fields from `18_Human_Validation_Gates.csv` — it does not introduce spreadsheets, IDs, connectors, or costs.

<a id="como-apresentar-um-gate"></a>
## How to present a gate

1. The AI presents, in simple language, the proposed decision, the main alternatives, the evidence and limitations. Avoid jargon and a ready-made model answer.
2. Ask for two short answers **from the researcher himself**:
   - Why is this choice appropriate to the problem of the article?
   - What is a limitation, risk or possible alternative to this choice?
3. If the researcher has doubts, explain the concept and keep the gate pending. Ask again directly; do not produce a response and attribute it to the researcher.
4. Preserve the verifiable reference to the human response in `Validation_evidence` and record the justification and limitation in the `Notes` field in a structured format. Only after this can approval be registered. A "yes", "ok" or blank justification is not enough.

Command example **with demonstrative answers only in the documentation**:

```bash
python scripts/governance_events.py gate /caminho/do/projeto \
  --gate-id GATE-0002 \
  --decision APPROVED \
  --validated-by "Pesquisador" \
  --method "Revisão do protocolo metodológico" \
  --evidence "Referência à mensagem original do pesquisador" \
  --researcher-rationale "O desenho reúne perspectivas teóricas diferentes para esclarecer uma questão conceitual." \
  --researcher-limitation "A abrangência depende das fontes consultadas e das escolhas de seleção da literatura."
```

The texts above **do not represent real human response** and cannot be copied as evidence of an effective decision. In normal use, extract these arguments from the user's direct expression, not from text suggested by the agent.

<a id="auditoria-e-limites"></a>
## Audit and limits

The registrar blocks an approval without minimally substantive justification and limitation; `validate_project.py` also rejects completed scientific gates with missing, malformed, or discordant formative records from `Validation_evidence`/`Validated_by`/`Decision`.

Automatic checking detects filling gaps and structural incoherence; **does not measure real understanding**, does not authenticate the identity of who typed the text and does not prove human authorship. An extensive and plausible justification may still be incorrect or artificially generated. Preserving the original message and performing human review remains essential.

The Skill itself should avoid producing `researcher-rationale` or `researcher-limitation` as if they were researcher responses. If the answer is ambiguous, ask for clarification without issuing approval. Internal structured records may contain sensitive details and should not be included indiscriminately in blind assessment packages.

<a id="relação-com-o-método-de-pesquisa"></a>
## Relationship with the research method

Approval does not replace methodological evaluation, evidence, corpus integrity or independent audits. It merely demonstrates that a scientific choice was explicitly assumed and explained by the user, within the limitations of available controls.