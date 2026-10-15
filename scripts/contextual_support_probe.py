#!/usr/bin/env python3
"""Experimental structured claim/excerpt discrepancy screening (REG-011).

Parallel to the lexical hints. Extracts limited contextual assertions,
qualifiers and contradictory limitations instead of matching an isolated
word anywhere. Advisory ONLY; not natural-language entailment or peer review.
Call ONLY on a verified literal source passage after source-hash verification.
No remote requests and no source content in returned observations.
"""
from __future__ import annotations

import re
import unicodedata

VERSION = "EXPERIMENTAL_CONTEXTUAL_SCREEN_V1"
MAX_CHARS = 12000

def plain(value: str) -> str:
    value = unicodedata.normalize("NFKD", str(value or "").casefold())
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", value).strip()

def present(s: str, pattern: str) -> bool:
    return re.search(pattern, s) is not None

def assertion(s: str, pattern: str, *, guarded_by: str) -> bool:
    """A lexical assertion is not positive if it is explicitly qualified.

    Clauses may still be ambiguously parsed; a signal remains advisory.
    """
    if not present(s, pattern):
        return False
    return not present(s, guarded_by)

def examine(claim: str, excerpt: str) -> dict:
    c, s = plain(claim), plain(excerpt)
    if not c or not s or max(len(c), len(s)) > MAX_CHARS:
        return {"status":"NOT_EVALUATED","signals":[],
                "reason":"EMPTY_OR_OVERSIZE",
                "entailment_proven":False,"human_review_required":True}
    found = []

    def flag(code, dimension, reason):
        if code not in {i["code"] for i in found}:
            found.append({"code":code,"dimension":dimension,
                          "reason":reason,"severity":"ADVISORY"})

    noncausal = present(s,
        r"\b(?:not randomi[sz]ed|nonrandom|not randomized|"
        r"assignment was not randomi[sz]ed|group composition.*differ|"
        r"groups differed|alternative explanations? (?:were )?not|"
        r"no alternative explanations?|"
        r"no causal|did not estimate causes|without causal|"
        r"observational|nao randomizad[oa]|sem inferencia causal)\b")
    causation = assertion(c,
        r"\b(?:caused|causou|was responsible for|resulted in|"
        r"attributable to|directly produced|led to|"
        r"proved effective|demonstrated (?:its )?effect|"
        r"was due to|resultou em|foi responsavel por)\b",
        guarded_by=r"\b(?:not establish|did not establish|cannot establish|"
        r"does not establish|not demonstrate|did not demonstrate|"
        r"did not prove|does not prove|cannot conclude|"
        r"nao estabelece|nao demonstrou|sem evidencia causal|"
        r"cannot be attributed)\b")
    if noncausal and causation:
        flag("CONTEXT_CAUSAL_ATTRIBUTION", "DESIGN",
             "Asserted causation despite source limits on causal attribution")

    is_narrow = present(s,
        r"\b(?:single (?:public |government )?(?:office|archive|department|unit)|"
        r"one (?:region|office|department)|only (?:two|one|six|eight)|"
        r"small (?:regional|convenience)|nonprobability|"
        r"five interviewees|six clerks|not (?:generaliz|represent)|"
        r"exploratory|no (?:population|prevalence) estimate|"
        r"one fictional region|em uma unica|apenas (?:uma|duas)|"
        r"amostra de conveniencia)\b")
    outside_scope = present(c,
        r"\b(?:throughout public administration|across (?:the |all )?(?:country|nation)|"
        r"throughout the (?:country|workforce)|all (?:government|public|national)|"
        r"most (?:administrators|employees|public servants)|"
        r"widespread (?:pattern|problem)|majority of administrators|"
        r"em toda (?:a administracao|a populacao)|"
        r"todos os servidores|maioria dos administradores)\b")
    bounded_claim = present(c,
        r"\b(?:in (?:this|the|a) (?:sample|survey|fictional|study)|"
        r"within (?:the|this) sample|only (?:in|among|for)|"
        r"two.office sample|among (?:respondents|interviewees)|"
        r"in the (?:participating|high.volume|low.volume) subgroup|"
        r"sem generalizar|na amostra|entre os respondentes)\b")
    if is_narrow and outside_scope and not bounded_claim:
        flag("CONTEXT_POPULATION_SCOPE", "POPULATION",
             "Broad target population exceeds the explicitly limited source population")

    if present(s,r"\b(?:nonrespondents|non.respondents|did not (?:answer|respond)|"
               r"invited but did not answer|respondents only)\b") and \
            present(c,r"\b(?:workforce|all employees|the department|"
                       r"three quarters of the|majority of employees)\b") and \
            not present(c,r"\b(?:among respondents|of respondents|"
                          r"in (?:the|this) survey sample)\b"):
        flag("CONTEXT_RESPONSE_DENOMINATOR", "SAMPLING",
             "Response fraction applied to a workforce not wholly observed")

    claims_positive_significance = assertion(c,
        r"\b(?:statistically significant|significantly (?:improv|increas|reduc)|"
        r"significancia estatistica|estatisticamente significativ)\w*",
        guarded_by=r"\b(?:not (?:statistically )?significant|"
        r"did not establish (?:a )?statistically significant|"
        r"no statistically significant|sem significancia|"
        r"nao foi estatisticamente significativ)\w*")
    if claims_positive_significance and present(s,
       r"\b(?:not statistically significant|no statistically significant|"
       r"no significant difference|sem significancia|"
       r"nao (?:foi|houve).{0,45}estatisticamente significativ)\w*"):
        flag("CONTEXT_SIGNIFICANCE_POLARITY", "STATISTICS",
             "Positive significance claim conflicts with reported null significance")

    no_outcome = present(s,
        r"\b(?:no results (?:were )?reported|data collection (?:had )?not started|"
        r"no (?:outcomes?|observations?|performance|satisfaction|competence)"
        r".{0,40}(?:available|collected|measured|recorded)|"
        r"did not measure (?:subsequent )?(?:job )?performance|"
        r"no earlier quarter.{0,35}(?:available|figures)|"
        r"no (?:unit [a-z]|subgroup).{0,20}(?:outcomes?|figures)|"
        r"results (?:were )?not reported|recruitment had yet to begin|"
        r"sem (?:dados|resultados|medicoes)|nao coletou resultados)\b")
    performance_claim = assertion(c,
        r"\b(?:proved effective|proven effective|"
        r"substantially more competent|higher competence|"
        r"more accurate than|better throughput|"
        r"eliminated its backlog|prevented incomplete|"
        r"produced better results|increased satisfaction|"
        r"achieved better|proven benefit|"
        r"demonstrou eficacia|comprovou melhora|eliminou a fila)\b",
        guarded_by=r"\b(?:cannot (?:be|establish)|"
        r"does not (?:establish|show)|did not (?:prove|establish)|"
        r"no improvement (?:could|can) be assessed|"
        r"not assessable|sem resultados comprovados|nao demonstra)\b")
    if no_outcome and performance_claim:
        flag("CONTEXT_UNOBSERVED_OUTCOME", "OUTCOME",
             "An outcome or effect is asserted where the source says it was not measured")

    unverified_deployment = present(s,
        r"\b(?:no operational deployment|unapproved software|"
        r"no (?:field trial|user training)|not (?:yet )?deployed|"
        r"had not (?:occurred|been launched)|"
        r"should not proceed to recruitment|"
        r"required substantial revision|"
        r"nao foi implantado|nao autorizado)\b")
    released = assertion(c,
        r"\b(?:already launched|had launched|trained administrative staff|"
        r"operational deployment|cleared.{0,50}recruitment|"
        r"authorized recruitment|without further revision|"
        r"ja lancou|autorizou (?:o inicio|recrutamento))\b",
        guarded_by=r"\b(?:not (?:yet )?launched|"
        r"not authorized|did not launch|not cleared|"
        r"nao (?:lancou|autorizou))\b")
    if unverified_deployment and released:
        flag("CONTEXT_STATUS_CONTRADICTION", "PROCESS_STATUS",
             "Claim asserts authorization or deployment denied by the source")

    private_missing=present(s,
        r"\b(?:excluded private companies|privately controlled firms were outside|"
        r"only (?:public|state.owned)|privat.{0,20}not represented|"
        r"sem empresas privadas|excluiu empresas privadas)\b")
    private_asserted=present(c,
        r"\b(?:private firms were|included private|private companies were|"
        r"private firms (?:formed|constituted)|"
        r"empresas privadas foram incluidas)\b")
    if private_missing and private_asserted:
        flag("CONTEXT_EXCLUDED_SAMPLE_ASSERTION", "SAMPLING",
             "Population explicitly excluded in source asserted to be sampled")

    contradictory_dates=present(s,
        r"\b(?:different approval dates|different dates|"
        r"discrepancy (?:was |remains? )?unresolved|"
        r"date was not confirmed|original signed.{0,30}unavailable|"
        r"datas divergentes|data nao confirmada)\b")
    fixed_date=present(c,
        r"\b(?:was formally (?:approved|transferred) on|"
        r"(?:formally )?(?:approved|transferred) on \d|"
        r"aprovado em \d|transferido em \d)\b")
    qualification=present(c,
        r"\b(?:does not establish|not confirmed|different dates|"
        r"not establish a final|discrepanc|nao confirmad)\b")
    if contradictory_dates and fixed_date and not qualification:
        flag("CONTEXT_DATE_UNCERTAINTY", "PROVENANCE",
             "Definite event date asserted despite unresolved documentary conflict")

    source_manual=present(s,
        r"\b(?:manually sorted|manual(?:ly)? (?:coding|grouping)|"
        r"neither predictive software nor machine.learning|"
        r"without (?:deploying )?(?:any )?(?:language model|ai)|"
        r"sem automatizacao|classificacao manual)\b")
    claim_auto=present(c,
        r"\b(?:automated classifier|ai system (?:performed|used)|"
        r"machine.learning classified|automatically (?:classified|sorted)|"
        r"classificador automatico|sistema de ia (?:classificou|usou))\b")
    if source_manual and claim_auto:
        flag("CONTEXT_MANUAL_AUTOMATED_METHOD", "METHOD",
             "Automated method asserted although source reports manual processing")

    if present(s,r"\b(?:no earlier quarter|earlier quarter.{0,20}not available|"
                  r"no (?:previous|baseline) (?:data|figures)|"
                  r"definition of completion had changed)\b") and \
          present(c,r"\b(?:better (?:than|throughput than)|"
                    r"than (?:in )?the preceding quarter|"
                    r"than (?:in )?the prior quarter)\b") and \
          not present(c,r"\b(?:cannot compare|no baseline|"
                        r"no (?:comparable|comparison) data)\b"):
        flag("CONTEXT_MISSING_COMPARATOR", "COMPARISON",
             "Comparative claim has no stable source comparator")

    # Two-term directional conflict: only when source describes one pair and
    # claim explicitly asserts the opposite, not multi-subgroup narratives.
    changes=re.findall(r"\b(?:fell|rose|increased|decreased|declined|dropped)"
                       r" from (\d+(?:[.,]\d+)?) to (\d+(?:[.,]\d+)?)\b",s)
    if len(changes)==1 and not present(c,
       r"\b(?:subgroup|opposite pattern|while.{0,40}other group)\b"):
        a,b=changes[0]
        try:
            delta=float(b.replace(",","."))-float(a.replace(",","."))
        except ValueError:
            delta=0
        up=present(c,r"\b(?:was higher after|increased|rose|went up|"
                     r"improved compared with before|aumentou|subiu)\b")
        down=present(c,r"\b(?:was lower after|decreased|fell|declined|"
                       r"reduced compared with before|diminuiu|caiu)\b")
        if (delta < 0 and up and not down) or (delta > 0 and down and not up):
            flag("CONTEXT_OPPOSITE_DIRECTION", "NUMERIC_DIRECTION",
                 "Claim's change direction conflicts with a single quoted before/after pair")

    return {
        "status":"SCREENED_EXPERIMENTAL_CONTEXT_ONLY",
        "version":VERSION,
        "signals":sorted(found,key=lambda x:(x["dimension"],x["code"])),
        "potential_review_needed":bool(found),
        "evaluated_dimensions":[
            "DESIGN","POPULATION","SAMPLING","STATISTICS","OUTCOME",
            "PROCESS_STATUS","PROVENANCE","METHOD","COMPARISON","NUMERIC_DIRECTION"],
        "severity":"ADVISORY",
        "can_block_scientific_workflow":False,
        "entailment_proven":False,
        "human_review_required":True,
        "independent_scientific_validation":False,
    }
