#!/usr/bin/env python3
"""Small deterministic checks for researcher explanations at scientific gates.

These checks establish that a recorded response is substantive enough to
require actual review. They cannot prove understanding or human authorship.
"""
from __future__ import annotations

import json
import re
import unicodedata

SCIENTIFIC_GATES = {f"GATE-{number:04d}" for number in range(1, 7)}
FORMATIVE_MARKER = "FORMATIVE_REVIEW_V1:"
APPROVALS = {"APPROVED", "APPROVED_WITH_CHANGES"}
PLACEHOLDERS = {
    "sim", "ok", "okay", "aprovado", "aprovo", "concordo", "de acordo",
    "confirmo", "sem ressalvas", "nao sei", "não sei", "n a",
    "n/a", "none", "approved", "yes", "agree", "agreed",
}


def clean(value: str) -> str:
    return " ".join(str(value or "").split())


def normalized(value: str) -> str:
    value = unicodedata.normalize("NFKD", clean(value).casefold())
    return "".join(ch for ch in value if not unicodedata.combining(ch))


def response_issues(rationale: str, limitation: str) -> list[str]:
    """Detect empty, placeholder and clearly insufficient answers, not meaning."""
    issues = []
    for label, content in (("rationale", rationale), ("limitation", limitation)):
        value = clean(content)
        words = re.findall(r"\b[\wÀ-ÿ]+\b", value, flags=re.UNICODE)
        if not value or normalized(value) in PLACEHOLDERS or len(words) < 5 or len(value) < 25:
            issues.append(f"{label} needs a substantive explanation in the researcher's own words")
    if clean(rationale) and normalized(rationale) == normalized(limitation):
        issues.append("rationale and limitation must describe different aspects of the decision")
    return issues


def encode_formative(*, rationale: str, limitation: str, source: str,
                    validated_by: str, decision: str) -> str:
    payload = {
        "schema": 1,
        "researcher_rationale": clean(rationale),
        "researcher_limitation": clean(limitation),
        "source": clean(source),
        "validated_by": clean(validated_by),
        "decision": clean(decision).upper(),
    }
    return FORMATIVE_MARKER + json.dumps(payload, ensure_ascii=False, sort_keys=True)


def extract_formative(notes: str) -> dict | None:
    """Read a single structured record at end of Notes, preserving old text."""
    value = str(notes or "")
    location = value.rfind(FORMATIVE_MARKER)
    if location < 0:
        return None
    prefix = value[:location]
    if prefix and not prefix.endswith("\n"):
        return None
    try:
        data = json.loads(value[location + len(FORMATIVE_MARKER):])
    except (json.JSONDecodeError, TypeError):
        return None
    return data if isinstance(data, dict) and data.get("schema") == 1 else None


def gate_issues(row: dict[str, str]) -> list[str]:
    """Check the form and internal consistency of an approved gate record."""
    gid = clean(row.get("GATE_ID"))
    decision = clean(row.get("Decision")).upper()
    if gid not in SCIENTIFIC_GATES or decision not in APPROVALS:
        return []
    data = extract_formative(row.get("Notes", ""))
    if data is None:
        return ["completed scientific gate has no structured researcher explanation"]
    issues = response_issues(data.get("researcher_rationale", ""), data.get("researcher_limitation", ""))
    for key, field in (
        ("source", "Validation_evidence"),
        ("validated_by", "Validated_by"),
        ("decision", "Decision"),
    ):
        expected, actual = clean(data.get(key, "")), clean(row.get(field, ""))
        if not expected or expected != actual:
            issues.append(f"formative {key} does not correspond to the gate record")
    return issues
