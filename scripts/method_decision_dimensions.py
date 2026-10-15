#!/usr/bin/env python3
"""Epistemically bounded decision-dimension catalogue for the adaptive map.

Educational alternatives, not AI decisions or an exhaustive ontology.
Dimensions are optional lenses over EXISTING route_details; never new required
methodology fields, gates, scientific approvals, or source of truth.
"""
from __future__ import annotations

DIMENSIONS = ("sampling", "sources", "analysis", "inference", "reporting")

# None means an advisory conversation only: no canonical writable field.
# "Sampling" in a review means DOCUMENT ELIGIBILITY, never participants.
ROUTE_FIELDS = {
    "INTEGRATIVE_REVIEW": {
        "sampling":"selection_logic","sources":"appraisal_logic",
        "analysis":"synthesis_logic","inference":None,"reporting":None},
    "SYSTEMATIC_REVIEW": {
        "sampling":"eligibility_criteria","sources":"comprehensive_search_plan",
        "analysis":"synthesis_logic","inference":"risk_of_bias_plan","reporting":None},
    "PROBLEMATIZING_REVIEW": {
        "sampling":"selection_logic","sources":"counterpositions",
        "analysis":"interpretive_strategy","inference":None,"reporting":None},
    "CONCEPTUAL_THEORY": {
        "sampling":None,"sources":"closest_prior_work",
        "analysis":"argument_strategy","inference":"boundary_conditions",
        "reporting":None},
    "QUALITATIVE": {
        "sampling":"sampling_logic","sources":"material_sources",
        "analysis":"analysis_logic","inference":"reflexivity_or_positioning",
        "reporting":None},
    "QUANTITATIVE": {
        "sampling":"sampling_logic","sources":"data_sources",
        "analysis":"analysis_plan","inference":"inference_aim","reporting":None},
    "MIXED_METHODS": {
        "sampling":None,"sources":None,"analysis":"meta_inference_plan",
        "inference":"discordance_plan","reporting":None},
    "DESIGN_SCIENCE": {
        "sampling":None,"sources":"design_requirements",
        "analysis":"evaluation_plan","inference":"non_evaluated_claim_limits",
        "reporting":None},
}

def option(code, title, fit, value, caution, next_step):
    return (code, title, fit, value, caution, next_step)

# By *scientific approach*, not disciplinary label. Never rank by popularity.
CATALOG = {
 "INTEGRATIVE_REVIEW":{
  "sampling":[
   option("SELECT_BY_CONCEPT","Purposeful concept-based literature selection","When constructs or explanatory perspectives delimit the conversation.","Supports comparison of diverse but relevant studies.","Selection is bounded, not automatically exhaustive.","Justify definitions, inclusion and omitted traditions."),
   option("SELECT_BY_CONTEXT","Context/period-bounded literature selection","When settings or historical periods delimit interpretation.","Makes the review scope explicit.","A bounded literature set cannot establish universal prevalence.","Document period, setting, search limitations and exceptions.")],
  "sources":[
   option("APPRAISE_BY_RELEVANCE","Relevance and argumentative contribution","When diverse epistemic traditions contribute different kinds of claims.","Preserves conceptual diversity and tensions.","Relevance is not equivalent to study validity.","Define transparent criteria for contribution and source provenance."),
   option("APPRAISE_BY_TRUSTWORTHINESS","Design-sensitive quality appraisal","When the review contains empirical and nonempirical sources.","Makes limits of different evidence types visible.","Do not apply one appraisal scale to all epistemologies.","Choose design-appropriate appraisal and document exceptions.")],
  "analysis":[
   option("THEMATIC_INTEGRATION","Thematic or concept integration","When studies articulate shared concepts or tensions.","Supports a bounded synthesis across works.","Recurring themes alone do not prove effects.","Trace each theme to consulted primary texts."),
   option("EXPLANATORY_COMPARISON","Compare explanatory accounts","When competing interpretations matter.","May identify theoretical gaps and alternative mechanisms.","Conceptual integration is not a causal estimate.","Record agreements, counterpositions and scope of conclusions.")],
  "inference":[
   option("BOUND_INTERPRETATION","Bound interpretive synthesis","When claims come from heterogeneous studies.","Clarifies what the assembled evidence can sustain.","Avoid turning diversity into fabricated pooled certainty.","State limits and alternative interpretations."),
   option("PROPOSE_FRAMEWORK","Offer a new conceptual proposition","When synthesis motivates a provisional explanatory model.","Supports explicit theoretical contributions.","A proposed framework is not empirically confirmed.","Mark original propositions and identify disconfirming work.")],
  "reporting":[
   option("INTEGRATION_TABLE","Evidence-to-theme integration table","When comparing themes, sources and tensions helps readers.","Makes synthesis structure inspectable.","A table is not proof that a source supports the claim.","Show consulted sources, competing positions and limitations."),
   option("ARGUMENTATIVE_SYNTHESIS","Argument-led narrative synthesis","When interpretive links matter more than frequencies.","Makes reasoning and scope explicit.","Do not imply exhaustiveness without an exhaustive search.","Explain selection logic, warrants and unresolved contradictions.")],
 },
 "SYSTEMATIC_REVIEW":{
  "sampling":[
   option("DOCUMENT_ELIGIBILITY","Explicit eligibility criteria for documents","When studies must be included or excluded reproducibly.","Supports a traceable study-selection process.","This is study eligibility, not participant sampling.","Define designs, populations/concepts, exclusions and decisions."),
   option("PILOT_CRITERIA","Pilot the eligibility rules","When concepts or ambiguous abstracts risk inconsistent selection.","Surfaces ambiguous cases before full screening.","A pilot does not substitute recorded human study decisions.","Specify calibration examples, revisions and reviewer disagreement handling.")],
  "sources":[
   option("MULTISOURCE_RETRIEVAL","Planned retrieval across relevant sources","When important evidence spans multiple information resources.","May improve coverage within a defined scope.","No database set guarantees comprehensiveness.","Document search syntax, sources, dates and updates."),
   option("ADDITIONAL_TRACING","Backward/forward citation tracing","When eligible studies are poorly indexed.","May find relevant material missed by keyword search.","Citation tracing alone is not an exhaustive strategy.","Define tracing rules and provenance.")],
  "analysis":[
   option("NARRATIVE_SYNTHESIS","Structured synthesis without pooling","When heterogeneous designs or outcomes preclude meaningful pooling.","Preserves design-specific findings and contradictions.","Do not present narrative findings as a pooled effect.","Plan grouping, appraisal, uncertainty and evidence links."),
   option("QUANTITATIVE_SYNTHESIS","Quantitative synthesis where justified","When comparable estimands and outcome measures support pooling.","May estimate combined effects with uncertainty.","Meta-analysis is not mandatory or appropriate for all systematic reviews.","Check compatibility, heterogeneity, bias and sensitivity.")],
  "inference":[
   option("DESIGN_AWARE_BIAS","Design-specific risk-of-bias assessment","When evidence includes distinct quantitative study designs.","Explains which inferences are threatened by bias.","One universal scale is not suitable for every design.","Choose appraisal methods appropriate to eligible study types."),
   option("CONFIDENCE_AND_UNCERTAINTY","Certainty or confidence in synthesis","When conclusions require calibrated strength-of-evidence claims.","Communicates uncertainty transparently.","A method name alone does not imply high certainty.","Document domain-specific appraisal and reasons for confidence.")],
  "reporting":[
   option("SELECTION_ACCOUNTING","Selection-flow and eligibility account","When transparent retrieval and screening are important.","Makes recorded exclusions and corpus boundaries visible.","A flow diagram cannot authenticate screening or complete retrieval.","Reconcile executed searches and study-level decisions."),
   option("OUTCOME_GROUPED_REPORT","Results grouped by question and design","When outcomes vary by study type.","Keeps distinct estimates and uncertainty interpretable.","Avoid merging incomparable outcomes.","Report study-specific contributions, bias and heterogeneity.")],
 },
 "PROBLEMATIZING_REVIEW":{
  "sampling":[
   option("PURPOSEFUL_THEORY_SELECTION","Purposeful source selection","When the aim is to challenge assumed theoretical premises.","Can expose neglected or dominant positions.","Selection is not a claim of exhaustive retrieval.","Justify inclusion, opposing works and limitations."),
   option("COUNTEREXAMPLE_SELECTION","Select theoretically challenging cases","When counterexamples illuminate a premise.","Can sharpen alternatives to accepted framing.","Cherry-picking risks a distorted conversation.","Document competing evidence and why it challenges the premise.")],
  "sources":[
   option("FOUNDATIONAL_AND_CRITICAL","Foundational and critical works","When an assumption has an identifiable intellectual lineage.","Preserves the debate's origin and revisions.","Commentary alone may misrepresent original arguments.","Inspect primary works and relevant critique."),
   option("CROSS_TRADITION_COMPARISON","Compare distinct theoretical traditions","When an assumption changes across scholarly conversations.","Supports alternative conceptual framing.","Different vocabularies need not mean substantive disagreement.","Clarify shared concepts and real divergences.")],
  "analysis":[
   option("ASSUMPTION_CRITIQUE","Explicit assumption critique","When premises are the focal analytical object.","Makes conceptual shifts auditable.","Rejecting a premise is not proof of an alternative.","Present assumption, warrant, critique and rival accounts."),
   option("REFRAMING_ARGUMENT","Reframe the original problem","When theoretical tension merits a new question.","Can generate testable or interpretive future work.","The reframe is a proposal, not an empirical finding.","State what changes, why and which questions remain.")],
  "inference":[
   option("BOUNDED_CRITIQUE","Bounded critique without universal novelty","When critique is based on a purposefully selected corpus.","Reduces unwarranted priority or coverage claims.","A selective reading cannot prove no prior similar argument exists.","Mark unresolved counterarguments and literature gaps."),
   option("CONDITIONAL_PROPOSITION","Conditional theoretical propositions","When reformulation yields possible mechanisms.","Makes assumptions and boundaries inspectable.","A proposition is not demonstrated by its elegance.","Differentiate premises, inference and original proposal.")],
  "reporting":[
   option("ASSUMPTION_MAP","Map assumptions and counterpositions","When intellectual disagreements drive the contribution.","Shows how the theoretical argument changes.","Mapping citations does not prove source agreement.","Present each position with provenance and disconfirming views."),
   option("CRITICAL_ESSAY","Critical argumentative essay","When the contribution is a defensible reinterpretation.","Keeps reasoning central.","Do not imply experimental validation.","Separate source claims, inference and proposal.")],
 },
 "CONCEPTUAL_THEORY":{
  "sources":[
   option("PRIMARY_THEORETICAL_WORKS","Trace primary intellectual sources","When construct meanings depend on original arguments.","Keeps conceptual lineage explicit.","Secondary summaries can distort an original position.","Compare key definitions and their contexts."),
   option("CLOSEST_ALTERNATIVE_MODELS","Compare closest rival frameworks","When proposing a new construct or mechanism.","Supports careful differentiation and boundary conditions.","Novel terminology alone is not theoretical novelty.","Identify prior mechanisms and rival explanations.")],
  "analysis":[
   option("LOGICAL_ARGUMENT","Premise-to-conclusion argument","When the thesis is established through theoretical reasoning.","Makes conceptual inference open to criticism.","An internally consistent argument does not establish empirical truth.","Lay out premises, counterexamples and scope."),
   option("CONCEPTUAL_RECONSTRUCTION","Reconstruct or refine concepts","When terms are contradictory or underspecified.","May improve explanatory clarity.","Do not present definitional changes as empirical observations.","Explain competing definitions, choices and tradeoffs.")],
  "inference":[
   option("SCOPE_BOUNDARIES","Specify conceptual boundary conditions","When a model applies only under stated assumptions.","Prevents universal extrapolation.","Scope assertions require a defensible conceptual warrant.","Define boundary cases and rival predictions."),
   option("TESTABLE_IMPLICATIONS","Develop conditional implications","When theoretical claims can lead to future empirical questions.","Separates proposed test implications from known results.","A future test is not a completed experiment.","Label untested implications and how they could be challenged.")],
  "reporting":[
   option("ARGUMENT_MAP","Structured theoretical argument","When premises and challenges need to be made explicit.","Helps trace claims and counterarguments.","A diagram is not evidence of correctness.","Show assumptions, citations, inferences and proposals."),
   option("CONCEPT_COMPARISON","Comparative conceptual table","When neighboring concepts risk conflation.","Clarifies overlap, distinctions and application limits.","Tabulation does not validate a concept.","Cite original meanings and unresolved problems.")],
 },
 "QUALITATIVE":{
  "sampling":[
   option("PURPOSIVE","Purposive selection","When information-rich cases illuminate the phenomenon.","Enables depth within an explicit scope.","Does not justify statistical representativeness.","Define selection rationale, access and adequacy criteria."),
   option("THEORETICAL_ITERATIVE","Iterative/theoretical selection","When an appropriate interpretive tradition uses emerging analysis to direct further material.","Can deepen and challenge developing categories.","Not every qualitative tradition uses theoretical sampling.","Explain iteration, negative cases and adequacy."),
   option("MAX_VARIATION","Maximum-variation selection","When contrasts across experiences or settings matter.","Makes important heterogeneity inspectable.","Variation sampling does not estimate population proportions.","Specify relevant variation, access and limits.")],
  "sources":[
   option("INTERVIEWS","Interview/conversational material","When participant accounts help answer the question.","Can provide detailed perspectives.","Accounts are situated and require ethics and interpretation.","Define access, consent as applicable and analytical treatment."),
   option("DOCUMENTS","Documentary/archival materials","When records or texts directly inform the phenomenon.","Can allow inquiry without direct interviews.","Provenance, selection and source criticism remain necessary.","Define the corpus, legal access and critique."),
   option("OBSERVATIONS","Observational/field material","When practices in context are central.","May capture situated action and variation.","Positioning and consent/privacy obligations vary.","Plan ethically appropriate field records and reflexivity.")],
  "analysis":[
   option("REFLEXIVE_THEMATIC","Reflexive thematic interpretation","When patterned meanings across material are central.","Supports explicit interpretive themes.","Not automatically compatible with all epistemological traditions.","Justify theme development, reflexivity and interpretation."),
   option("NARRATIVE_INTERPRETATION","Narrative analysis","When temporality, plot and voice are part of the research object.","Preserves sequencing and perspective.","Fragmentary coding can lose narrative context.","Justify narrative units and mode of interpretation."),
   option("CASE_COMPARISON","Within/across-case comparison","When clearly bounded cases are the unit of understanding.","Makes similarities and differences interpretable.","Case comparison alone does not support population prevalence.","Plan case descriptions, contrasts and exceptions.")],
  "inference":[
   option("INTERPRETIVE_WARRANT","Interpretive warrants and reflexivity","When meanings depend on interpretation in context.","Exposes how claims follow from analyzed material.","There is no universal agreement about a single credibility metric.","Document positionality, competing readings and limits."),
   option("ANALYTIC_TRANSFER","Analytical transferability","When findings may be meaningful in other comparable contexts.","Clarifies contextual resonance without numerical generalization.","Transferability is not statistical representativeness.","Specify case features and conditions of potential transfer.")],
  "reporting":[
   option("THEMATIC_EVIDENCE","Themes grounded in legitimate excerpts","When thematic analysis was actually conducted.","Makes interpretations inspectable.","Excerpts must respect consent, anonymity and reuse rights.","Connect claims to permitted material and alternative readings."),
   option("CASE_OR_NARRATIVE_REPORT","Case-based or narrative account","When context or temporal sequence is essential.","Retains situated meaning.","Detailed context can reidentify people or organizations.","Explain anonymization, interpretive scope and source limits.")],
 },
 "QUANTITATIVE":{
  "sampling":[
   option("PROBABILITY","Probability sampling","When population-level estimation is an aim and a viable sampling frame exists.","Can support appropriately designed population estimates.","Sampling frame, nonresponse and design effects still matter.","Specify frame, inclusion probabilities, planned precision and missingness."),
   option("NONPROBABILITY","Nonprobability sampling","When a defined accessible group or exploratory setting is necessary.","Allows bounded studies with transparent recruitment.","Does not justify automatic population prevalence claims.","Define access, selection bias and inferential boundaries."),
   option("COMPLETE_FRAME","Census of defined eligible units","When all units of a realistic bounded frame can be observed.","May avoid sampling within the defined frame.","Missing records and coverage error remain possible.","Specify eligibility, completeness and exclusions.")],
  "sources":[
   option("ORIGINAL_MEASUREMENTS","Original measured observations","When defined constructs require dedicated data collection.","Can align instruments to the research question.","Instrument quality and ethics must be assessed.","Define variables, recruitment, instruments and measurement quality."),
   option("EXISTING_DATA","Existing datasets/administrative records","When valid accessible data address the question.","May permit analyses without new recruitment.","Provenance, permissions, construct validity and missing data matter.","Document access, linkage, definitions and data quality.")],
  "analysis":[
   option("DESCRIPTIVE_COMPARISON","Descriptive estimation/comparison","When the aim concerns observed quantities or subgroups.","Can communicate differences and uncertainty.","Descriptive contrasts do not establish causality.","Define denominator, uncertainty and missingness."),
   option("REGRESSION_OR_MODELLING","Regression or other statistical modelling","When assumptions and measured relationships warrant a model.","May examine association or prediction in a bounded setting.","Model fit is not a causal identification strategy.","Predefine estimands, assumptions, diagnostics and sensitivity."),
   option("CAUSAL_DESIGN","Identification-focused causal analysis","When causal effects are the central question and assumptions are defensible.","Makes counterfactual assumptions explicit.","Causal claims cannot be derived from an arbitrary model.","Specify identification, confounding, robustness and ethical constraints.")],
  "inference":[
   option("DESCRIPTIVE","Description","When the aim is a frequency, parameter or distribution.","Provides bounded estimates.","Estimation outside the sampling frame may be invalid.","Define target quantity and uncertainty."),
   option("ASSOCIATIONAL","Association","When the aim concerns a relation between measures.","Supports explicit statistical comparisons.","Association alone is not causation.","Clarify controls, assumptions and multiple testing."),
   option("PREDICTIVE","Prediction","When generalization to unseen cases is the target.","Makes validation and calibration testable.","High accuracy alone does not prove safety or mechanism.","Define holdout, leakage control and drift."),
   option("CAUSAL","Causal effect","When treatment or exposure effect is the research target.","Makes counterfactual reasoning explicit.","Identification assumptions must be defended.","Define intervention, comparison and identification.")],
  "reporting":[
   option("ESTIMATES_WITH_UNCERTAINTY","Estimates and uncertainty intervals","When numerical inference was actually executed.","Shows magnitude and precision.","A small p-value alone does not establish practical relevance.","Report effect size, uncertainty, assumptions and limitations."),
   option("DIAGNOSTIC_SENSITIVITY","Diagnostics and sensitivity report","When model assumptions and robustness matter.","Makes inference limits inspectable.","Robustness exercises do not eliminate all bias.","Report missingness, sensitivity, alternative models and assumptions.")],
 },
 "MIXED_METHODS":{
  "sampling":[
   option("STRAND_SPECIFIC_SAMPLING","Distinct sampling for each strand","When QUAN and QUAL answer complementary questions.","Preserves appropriate designs for each strand.","There is no single universally correct mixed-method sampling rule.","Specify both selections and the intended connection."),
   option("CONNECTED_SAMPLING","Connected sequential sampling","When later participants or cases follow earlier findings.","Creates an explicit explanatory or exploratory link.","The second sample cannot be justified by convenience alone.","Explain how the first results inform the next strand.")],
  "sources":[
   option("DISTINCT_STRAND_SOURCES","Separate QUAN and QUAL material plans","When each strand needs different data.","Clarifies which source answers which part of the question.","Parallel streams alone do not constitute integration.","Document access, alignment and integration purpose."),
   option("LINKED_MATERIALS","Linked records, cases or participants","When integration requires connecting the strands.","Can support within-case explanatory comparison.","Privacy, linkage error and ethics may constrain the design.","Define permissible linkage, integration points and risks.")],
  "analysis":[
   option("JOINT_DISPLAY","Joint displays and explicit meta-inference","When different forms of evidence need structured comparison.","Makes convergence and disagreement visible.","A display does not automatically create justified integration.","Specify connection, explanation and discrepant patterns."),
   option("SEQUENTIAL_INTEGRATION","Sequential building or explanation","When one strand informs the next.","Preserves sequence and explanatory intent.","Requires actual integration, not a simple collection of both data types.","Document strand order, adaptation and meta-inference.")],
  "inference":[
   option("DISCORDANCE_PLAN","Analyse disagreement between strands","When QUAL and QUAN evidence may diverge.","Avoids treating discordance as a failure to be hidden.","Cannot assume one strand is always correct.","Define cases of divergence and interpretive procedure."),
   option("COMPLEMENTARY_INFERENCE","Identify complementary insights","When strands answer related but nonidentical questions.","Distinguishes convergence from complementarity.","Different constructs may be incomparable.","Specify interpretive scope and which claims each strand supports.")],
  "reporting":[
   option("INTEGRATED_DISPLAY","Integrated results with joint display","When meta-inferences depend on linked results.","Makes integration visible to readers.","Juxtaposed tables alone are not integrated inference.","Report convergence, divergence and limitations."),
   option("SEQUENTIAL_RESULTS","Stage-ordered reporting with integration","When a sequential design drives interpretation.","Clarifies what each phase changed.","Results chronology must not replace integration.","Explain how one phase informs the next and the final inference.")],
 },
 "DESIGN_SCIENCE":{
  "sampling":[
   option("EVALUATION_CASE_SELECTION","Choose evaluation cases or scenarios","When the artifact must be examined in bounded use conditions.","Makes scenario coverage and variation explicit.","Synthetic case tests do not demonstrate real-world uptake.","Define scenario provenance, coverage and blind evaluation if applicable."),
   option("EXPERT_OR_USER_EVALUATION","Consider expert/user assessment","When usability or field relevance is itself a research question.","Can provide additional situated feedback.","Requires ethical and operational care; not mandatory for every design-science study.","Define participants or experts, rights, criteria and study approvals where applicable.")],
  "sources":[
   option("DESIGN_REQUIREMENTS","Literature- and task-grounded requirements","When a problem and intended artifact behavior can be specified.","Creates traceable design rationale.","A requirement is not evidence that the feature works.","Link each requirement to rationale and test evidence."),
   option("STAKEHOLDER_CONSTRAINTS","Stakeholder and deployment constraints","When different intended users or institutions impose limits.","Surfaces trade-offs in validity, safety and feasibility.","Do not imply stakeholder input occurred if it has not.","Specify actual provenance of constraints and unresolved assumptions.")],
  "analysis":[
   option("CONTROLLED_ARTIFACT_TEST","Controlled artifact evaluation","When predefined technical behavior can be tested without participants.","Enables reproducible technical observations.","Software passing tests does not establish scientific utility.","Specify cases, thresholds, evidence and failure analysis."),
   option("REAL_CONTEXT_EVALUATION","Real-context evaluation","When effectiveness or adoption in actual use is at issue.","Can test situated performance and unintended effects.","Requires access, appropriate ethics and careful attribution.","Specify deployment scope, participants if any and observation criteria.")],
  "inference":[
   option("FUNCTIONAL_ONLY","Restrict claims to verified functionality","When only software tests or prototypes exist.","Prevents performance and productivity overclaims.","Functionality does not prove adoption or scientific validity.","List outcomes not evaluated and required future evidence."),
   option("BOUNDED_EFFECTIVENESS","Make explicitly bounded evaluation claims","When an actual appropriate evaluation has been executed.","Links outcomes to predefined criteria.","External validity remains limited by design and observed cases.","Document evaluation design, limitations and counterevidence.")],
  "reporting":[
   option("REQUIREMENTS_TRACE","Requirements-to-test trace","When readers must verify why each design choice was made.","Links claimed features to executable evidence.","Traceability alone does not prove research quality.","Report requirements, execution results, failures and limitations."),
   option("DESIGN_AND_EVALUATION","Design decisions and evaluation narrative","When the research contribution includes an artifact and its assessment.","Makes design iteration and evidence legible.","Do not infer user benefit from implementation alone.","Separate constructed features, tested effects and future hypotheses.")],
 },
}

NOT_UNIVERSAL = {
 "CONCEPTUAL_THEORY":{"sampling"},
}

def eligible(route: str, dimension: str) -> bool:
    return route in ROUTE_FIELDS and dimension in DIMENSIONS and \
           dimension not in NOT_UNIVERSAL.get(route,set())

def candidates(route: str, dimension: str):
    """Return author-curated illustrative options, not a forced classification."""
    if not eligible(route,dimension):
        return []
    return CATALOG.get(route,{}).get(dimension,[])

def existing_field(route: str, dimension: str):
    if route not in ROUTE_FIELDS or dimension not in DIMENSIONS:
        raise ValueError("Unsupported research decision dimension")
    return ROUTE_FIELDS[route][dimension]
