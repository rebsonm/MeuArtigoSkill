#!/usr/bin/env python3
"""Cautious lexical red flags for claim/passage scope or polarity conflicts.

Advisory, language-limited, deterministic, explicitly NOT semantic entailment.
Only run after the passage was literally located and its hash was checked.
Absence of flags is NOT evidence of support. No source passages are exported.
"""
from __future__ import annotations

import re
import unicodedata

VERSION = "EXPLORATORY_LEXICAL_RISK_V1"
LIMIT_CHARS = 12000
LIMIT_FLAGS = 8

def norm(text: str) -> str:
    s = unicodedata.normalize("NFKD", str(text or "").casefold())
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", s).strip()

def has(text: str, expression: str) -> bool:
    return re.search(expression, text, flags=re.I) is not None

def signals(claim: str, passage: str) -> dict:
    """Return review *possibilities*, never a truth, support or gate verdict.

    Signals are deliberately selective. Each one needs textual evidence on
    BOTH sides of the comparison. They can miss paraphrases and languages.
    Caller must verify quoted passage against a real local source first.
    """
    c, p = norm(claim), norm(passage)
    if not c or not p or len(c)>LIMIT_CHARS or len(p)>LIMIT_CHARS:
        return {
            "status":"NOT_EVALUATED","codes":[],
            "reason":"EMPTY_OR_OVERSIZE",
            "is_scientific_verification":False,"semantic_entailment_proven":False,
        }
    codes = []

    def add(code, claim_pattern, source_pattern):
        if has(c,claim_pattern) and has(p,source_pattern):
            codes.append(code)

    # Diagnostic contradictions, not universal rules for causal inference.
    add("CAUSALITY_FROM_NONCAUSAL_EVIDENCE",
        r"\b(?:caus(?:e[ds]?|al)|led to|resulted in|redu(?:c(?:e[ds]?|tion))|improv(?:ed|es?|ement)|"
        r"causou|provocou|resultou em|reduziu|melhorou|comprovou impacto)\b",
        r"\b(?:not randomi[sz]ed|assignment was not randomi[sz]ed|nonrandom|"
        r"did not estimate causes|without causal|no causal|observational association|"
        r"nao randomizad[ao]s?|sem randomizac[aã]o|nao estimou causas|sem inferencia causal)\b")

    add("POPULATION_EXTRAPOLATION",
        r"\b(?:throughout [a-z]+|across all|all (?:public|municipal|government|private|teams|"
        r"employees|organizations)|every (?:worker|employee|team|organization)|"
        r"most employees across|all public organizations|"
        r"todos os|todas as|em todo o brasil|em todas as|servidores de todo)\b",
        r"\b(?:only|two|one region|one department|eight|interview study|"
        r"nonprobability|non-probability|convenience sample|"
        r"twenty respondents|25 artificially|synthetic|fictional|"
        r"apenas|somente|duas unidades|uma regiao|amostra de conveniencia)\b")

    add("SIGNIFICANCE_POLARITY_CONFLICT",
        r"\b(?:significantly (?:improv\w*|reduc\w*|increas\w*)|statistically significant|"
        r"melhora estatisticamente significativa|reduziu significativamente)\b",
        r"\b(?:no statistically significant|not statistically significant|"
        r"no significant difference|nao houve diferenca estatisticamente significativa|"
        r"sem significancia estatistica)\b")

    add("DIRECTION_OF_CHANGE_CONFLICT",
        r"\b(?:decreas(?:ed|e)|declin(?:ed|e)|fell|dropped|reduziu|diminuiu)\b",
        r"\b(?:rose from \d+|increased from \d+|went up from \d+|"
        r"subiu de \d+|aumentou de \d+)\b")
    add("DIRECTION_OF_CHANGE_CONFLICT",
        r"\b(?:increas(?:ed|e)|rose|went up|aumentou|subiu)\b",
        r"\b(?:decreased from \d+|declined from \d+|fell from \d+|"
        r"diminuiu de \d+|reduziu de \d+)\b")

    add("METHOD_CONTRADICTS_SOURCE",
        r"\b(?:ai system|language model|automatically classif(?:ied|ies|y)|"
        r"sistema de ia|modelo de linguagem|classificou automaticamente)\b",
        r"\b(?:without deploying any language model|no language model|coding was performed manually|"
        r"without any ai|sem modelo de linguagem|codificacao manual|sem inteligencia artificial)\b")

    add("EXCLUDED_POPULATION_ASSERTED_PRESENT",
        r"\b(?:both public-sector units and private companies|"
        r"(?:included|contained) private companies|incluiu empresas privadas|"
        r"incluiu setor privado)\b",
        r"\b(?:excluded private companies|private companies were excluded|"
        r"no private companies|excluiu empresas privadas|sem empresas privadas)\b")

    add("OUTCOME_WITHOUT_COLLECTED_RESULTS",
        r"\b(?:reduc(?:ed|tion)|improv(?:ed|ement)|increas(?:ed|e)|higher compliance|"
        r"reduced its backlog|significantly|reduziu|melhorou|aumentou|"
        r"comprovou|demonstrou resultado)\b",
        r"\b(?:data collection had not started|no results were reported|"
        r"results were not reported|no outcomes? (?:were )?(?:collected|reported|available)|"
        r"nao houve coleta de dados|resultados nao foram reportados|sem resultados)\b")

    add("MISSING_SUBGROUP_OUTCOME",
        r"\b(?:unit\s+[a-z]\s+(?:reduc|improv|increas)|"
        r"unidade\s+[a-z]\s+(?:reduz|melhor|aument))",
        r"\b(?:records for unit [a-z] were missing|unit [a-z] outcomes? (?:were )?(?:missing|unavailable)|"
        r"dados da unidade [a-z] indisponiveis)\b")

    add("CONFLICTING_DATE_REPORTED_AS_FINAL",
        r"\b(?:formally approved on \d{1,2}|officially decided on \d{1,2}|"
        r"formalmente aprovad[ao] em \d{1,2})\b",
        r"\b(?:different dates|dates remain unresolved|discrepancy remains unresolved|"
        r"datas divergentes|divergencia de datas nao resolvida)\b")

    add("UNOBSERVED_GROUP_COMPARISON",
        r"\b(?:nonrespondents had|non[- ]respondents (?:were|showed)|"
        r"nao respondentes tinham|nao respondentes apresentaram)\b",
        r"\b(?:no (?:compliance )?observations were collected for nonrespondents|"
        r"no data (?:on|for) nonrespondents|sem dados de nao respondentes)\b")

    # Require both a number/percentage unaccounted for in the passage AND a
    # statement of missing measurements. This reduces naive numeric false
    # alarms. This is only a possible review signal.
    claim_numbers = set(re.findall(r"\b\d+(?:[.,]\d+)?\b",c))
    source_numbers = set(re.findall(r"\b\d+(?:[.,]\d+)?\b",p))
    if claim_numbers-source_numbers and has(p,
        r"\b(?:missing|unavailable|no (?:data|results)|not collected|"
        r"not available|no outcomes|dados ausentes|indisponiveis|sem dados)\b"):
        codes.append("UNACCOUNTED_QUANTITY_WITH_MISSING_DATA")

    codes = sorted(set(codes))[:LIMIT_FLAGS]
    return {
        "status":"SCREENED_HEURISTIC_ONLY","codes":codes,
        "potential_review_needed":bool(codes),
        "rule_set":VERSION,
        "languages_targeted":["en","pt"],
        "is_scientific_verification":False,
        "semantic_entailment_proven":False,
    }
