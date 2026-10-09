#!/usr/bin/env python3
"""Language settings for a project; actual conversational detection is model-side.

The source repository and schema are English. This module validates optional
persistent preferences but NEVER attempts to infer a researcher's language
from their country, name, publications or a pasted text.
"""
from __future__ import annotations

import re
from typing import Any

LANGUAGE_TAG = re.compile(r"^[a-zA-Z]{2,3}(?:-[a-zA-Z]{4})?(?:-(?:[a-zA-Z]{2}|\d{3}))?$")
MODES = {"AUTO", "EXPLICIT"}
AUTO = "auto"
UNDECIDED = "undecided"


def normalized_tag(value: str, *, allow_auto: bool = False, allow_undecided: bool = False) -> str:
    text = str(value or "").strip()
    if allow_auto and text.lower() == AUTO:
        return AUTO
    if allow_undecided and text.lower() == UNDECIDED:
        return UNDECIDED
    if not LANGUAGE_TAG.fullmatch(text):
        raise ValueError("Expected a simple BCP-47 language tag (for example pt-BR, en, es)")
    chunks = text.split("-")
    normalized = [chunks[0].lower()]
    for chunk in chunks[1:]:
        if len(chunk) == 4:
            normalized.append(chunk.title())
        elif len(chunk) == 2:
            normalized.append(chunk.upper())
        else:
            normalized.append(chunk)
    return "-".join(normalized)


def project_language_settings(interaction_language: str = AUTO,
                              manuscript_language: str = UNDECIDED,
                              *, explicitly_selected: bool = False) -> dict[str, str]:
    interaction = normalized_tag(interaction_language, allow_auto=True)
    manuscript = normalized_tag(manuscript_language, allow_undecided=True)
    if interaction != AUTO and not explicitly_selected:
        raise ValueError("Persistent interaction language requires the researcher's explicit choice")
    return {
        "interaction_language_mode": "EXPLICIT" if interaction != AUTO else "AUTO",
        "interaction_language": interaction,
        "manuscript_language": manuscript,
    }


def settings_issues(config: dict[str, Any]) -> list[str]:
    """Check only settings shape, never claim that the actual LLM replied in this language."""
    if not any(key in config for key in
               ("interaction_language_mode", "interaction_language", "manuscript_language")):
        # Backward compatibility: old workspaces default to AUTO without mutation.
        return []
    issues = []
    mode = config.get("interaction_language_mode")
    if mode not in MODES:
        issues.append("Invalid interaction language mode")
    try:
        interaction = normalized_tag(config.get("interaction_language", ""), allow_auto=True)
    except ValueError:
        interaction = ""
        issues.append("Invalid interaction language tag")
    try:
        normalized_tag(config.get("manuscript_language", ""), allow_undecided=True)
    except ValueError:
        issues.append("Invalid manuscript language tag")
    if mode == "AUTO" and interaction != AUTO:
        issues.append("AUTO interaction mode requires interaction_language=auto")
    if mode == "EXPLICIT" and interaction == AUTO:
        issues.append("EXPLICIT interaction mode requires a concrete language tag")
    return issues
