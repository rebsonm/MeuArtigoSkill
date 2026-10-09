<a id="avaliação-crítica-da-qualidade-das-fontes"></a>
# Critical assessment of font quality

This component checks whether the source is methodologically suitable for the purpose for which it is being used in the article. **True DOI does not mean robust evidence.** Skill does not automatically issue a quality score or replace the researcher's judgment.

<a id="abrangência-gratuita"></a>
## Free coverage

Requires Python 3.10+ and the standard library only. The procedure uses the same Evidence_ID, the canonical matrix 05_Evidence_Matrix.csv and the existing tab 09_MATRIZ_EVID. No new ID, new tab or paid service.

Criteria families — adjustable to article design and protocol:
- QUANTITATIVE: adequacy of design, sampling/bias, measurement and analysis;
- QUALITATIVE: adequacy of design, sampling/context, traceability of analysis and reflexivity/limits;
- MIXED_METHODS: quantitative and qualitative components, integration of results and limitations of the combination;
- REVIEW: question and scope, search coverage, selection/extraction and synthesis/appreciation methods;
- CONCEPTUAL: precision of concepts, coherence of arguments, dialogue with alternatives and limits of scope;
- NORMATIVE: authority/version, jurisdiction/validity, interpretation and distinction between norm and empirical finding;
- OTHER: nature of the source, origin, suitability for the claim and uncertainty.

This is **our own operational checklist**, not a reproduction or official certification of JBI, CASP, MMAT or other scale. When the research or magazine requires a specific validated instrument, follow its rules and register the original version; do not pretend to be equivalent to the general checklist.

<a id="procedimento"></a>
## Procedure

1. Classify the font by actual design, not by the magazine's prestige or impact factor. Works of different nature are not comparable using a universal score.
2. Generate a structural form without auto-filling responses:

       python scripts/appraise_evidence.py template --family QUALITATIVE

   Save the JSON to a temporary file in the project workspace and fill each item with:
   - rating: YES, NO, UNCLEAR or NOT_APPLICABLE;
   - basis: explanation based on the text actually consulted, with section/page indication if available.

3. Skill can prepare an information board for easy reading. **Cannot claim to have performed human review** nor generate responses attributed to the user.
4. After an actual evaluation by the researcher, record it in the canonical CSV, for example:

       python scripts/appraise_evidence.py record "/path/to/project" \
         --evidence-id "EVID-0001" --family QUALITATIVE \
         --checklist "/path/to/project/appraised_criteria.json" \
         --judgement USE_WITH_CAVEATS \
         --rationale "The analysis addresses the question, but participant selection limits transferability." \
         --limitations "These findings are context-specific and do not justify statistical generalization to other populations." \
         --reviewer "Pesquisador" \
         --review-evidence "Referência à manifestação humana original"

   The texts above are just examples of **format**. They do not represent an examined source or actual human decision.

5. To audit documentation:

       python scripts/appraise_evidence.py audit "/path/to/project" --strict

<a id="julgamento-científico-registrado"></a>
## Registered scientific judgment

- SUITABLE_FOR_CLAIM: human assessment registered without reservations on applicable items. It is only allowed when the checklist items are YES. Still, it is not an automatic certification of the source.
- USE_WITH_CAVEATS: the source can be used with explicit restrictions, maintaining the qualification in the claims.
- INSUFFICIENT_INFORMATION: the available material is insufficient to support the intended claim.
- DO_NOT_USE_FOR_CLAIM: the researcher judged that the proposed statement should not be substantiated.

The choice of these states remains human. The code rejects objective inconsistencies, such as asserting SUITABLE_FOR_CLAIM when there is a NO or UNCLEAR item, or registering criteria without basis. **Does not conclude**, based on how many items were marked YES, that the source is valid.

<a id="integração-da-avaliação-crítica-com-a-verificação-das-fontes-e-das-evidências"></a>
## Integration of critical appraisal with source and evidence verification

New projects have critical_appraisal_required=true. When approving GATE-0006, the validator requires critical evaluation of the Evidence_IDs effectively linked to material claims (including contrary evidence). Evidence used with the INSUFFICIENT_INFORMATION or DO_NOT_USE_FOR_CLAIM judgment blocks the gate while substantiating the claim. Qualified evidence requires scientific justification and correctly limited claims.

In older designs, the mode is not retroactively enabled. The Appraisal_criteria field stores structured JSON and the other six fields are on the same line in the source. Subsequent updates require versioning and new decision recording: do not silently overwrite evaluations already carried out.

A change to the evidence matrix modifies its SHA-256; therefore, source verification reports will need to be **regenerated** after evaluations are completed before final freezing.

<a id="limitações"></a>
## Limitations

- A name entered as a reviewer does not authenticate the person's identity.
- Completion does not prove real quality, correct interpretation or access to the full text.
- Information obtained only by summary must continue to be marked as such; Do not extrapolate the criticism beyond the material accessed.
- Do not automatically exclude fonts with reservations. The relevance and argumentative weight depend on the question and the type of statement.
- Conceptual books, standards and empirical studies have distinct epistemological functions. Do not mix normative authority and empirical demonstration.
- In projects with canonical Drive, synchronize the CSVs, human manifestations and completed checklist before stating that the official workspace is updated.

The tool is an auditable record of critical assessment, **not an independent peer review**.