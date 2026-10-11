#!/usr/bin/env python3
"""Read-only next-action resolver for an authorized Meu Artigo project.

This is a conservative navigation aid, not an autonomous scientific decision
engine. Only canonical project records are considered; no chat assumptions,
human-approval writes, network calls, or Drive sync claims are made.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

from transaction_coordinator import active_journals

MGMT = "00_Gestao_e_Continuidade"
GATES = f"{MGMT}/18_Human_Validation_Gates.csv"
TASKS = f"{MGMT}/11_CADA_Control.csv"
CONTINUITY = "CONTINUIDADE.md"
EXPECTED_GATES = tuple(f"GATE-{i:04d}" for i in range(1, 8))
APPROVALS = {"APPROVED", "APPROVED_WITH_CHANGES"}
TERMINAL = {"DONE", "COMPLETED", "CANCELLED", "CANCELED", "SUPERSEDED"}
EXECUTABLE = {"READY", "IN_PROGRESS"}
DECISION_EXECUTION = {"DECISION_REQUIRED", "HUMAN_ONLY", "RESEARCHER_ONLY"}
SPLIT = re.compile(r"[;,\s]+")


def clean(value: object) -> str:
    return str(value or "").strip()


def upper(value: object) -> str:
    return clean(value).upper()


def ids(value: object) -> list[str]:
    return [part for part in SPLIT.split(clean(value)) if part]


def recorded_next_ids(markdown: str) -> list[str]:
    """Extract only explicit CADA_ID markers in Next valid action sections.

    The free-form content is untrusted task metadata, never executable
    instructions. Do not expose text or presume that absence means DONE.
    """
    stored = []
    in_section = False
    for line in markdown.splitlines():
        if re.match(r"^#{2,3}\s+", line):
            in_section = bool(re.search(
                r"(?:next valid action|pr[oó]xima a[cç][aã]o v[aá]lida)",
                line, flags=re.IGNORECASE))
        if in_section:
            match = re.search(r"^\s*-\s*CADA_ID:\s*(CADA-\d{4,})\s*$", line)
            if match:
                stored.append(match.group(1))
    # Also support lightweight continuity notes with an unambiguous inline ID.
    if not stored:
        for line in markdown.splitlines():
            match = re.search(
                r"(?:next valid action|pr[oó]xima a[cç][aã]o v[aá]lida):\s*(CADA-\d{4,})",
                line, flags=re.IGNORECASE)
            if match:
                stored.append(match.group(1))
    return stored


def read_csv(root: Path, relative: str, id_key: str) -> tuple[list[dict], list[str]]:
    file = root / relative
    if file.is_symlink() or not file.is_file():
        return [], [f"MISSING_OR_UNSAFE_{id_key}_REGISTER"]
    try:
        with file.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            if reader.fieldnames is None or id_key not in reader.fieldnames:
                return [], [f"INVALID_{id_key}_HEADERS"]
            rows = list(reader)
        if any(None in r for r in rows):
            return [], [f"MALFORMED_{id_key}_ROWS"]
        keys = [clean(row.get(id_key)) for row in rows]
        if any(not key for key in keys) or len(keys) != len(set(keys)):
            return rows, [f"MISSING_OR_DUPLICATE_{id_key}"]
        return rows, []
    except (UnicodeError, OSError, csv.Error):
        return [], [f"UNREADABLE_{id_key}_REGISTER"]


def stage_num(value: object) -> int | None:
    match = re.match(r"^\s*(\d+)", clean(value))
    return int(match.group(1)) if match else None


def documented_gate(row: dict) -> bool:
    """Structural record of approval only; never authenticate the researcher."""
    return (upper(row.get("Status")) == "COMPLETED"
            and upper(row.get("Decision")) in APPROVALS
            and bool(clean(row.get("Validated_by")))
            and bool(clean(row.get("Validation_evidence"))))


def task_dependencies_met(task: dict, by_id: dict[str, dict]) -> tuple[bool, str | None]:
    for dependent_id in ids(task.get("Dependency_IDs")):
        dependency = by_id.get(dependent_id)
        if dependency is None:
            return False, "UNKNOWN_TASK_DEPENDENCY"
        if upper(dependency.get("Status")) not in {"DONE", "COMPLETED"}:
            return False, "UNFINISHED_TASK_DEPENDENCY"
        if not clean(dependency.get("Completion_evidence")):
            return False, "UNVERIFIED_TASK_DEPENDENCY_COMPLETION"
    return True, None


def resolve(project: Path) -> dict:
    """Classify next permitted work without modifying canonical artifacts."""
    root = Path(project).resolve()
    result = {
        "schema": "MEU_ARTIGO_NEXT_STEP_V1",
        "status": "BLOCKED",
        "next_task_id": None,
        "next_gate_id": None,
        "requires_human_decision": False,
        "technical_preparation_possible": False,
        "action_recorded": False,
        "blockers": [],
        "continuity_document_read": False,
        "storage_verified_in_this_session": False,
        "scientific_gate_approved_by_this_command": False,
        "canonical_state_modified": False,
        "method_or_science_independently_validated": False,
    }
    config_file = root / MGMT / "PROJECT_CONFIG.json"
    if config_file.is_symlink() or not config_file.is_file():
        result["blockers"].append("MISSING_OR_UNSAFE_PROJECT_CONFIG")
        return result
    try:
        config = json.loads(config_file.read_text(encoding="utf-8"))
        if not isinstance(config, dict):
            raise ValueError()
    except (OSError, UnicodeError, ValueError):
        result["blockers"].append("INVALID_PROJECT_CONFIG")
        return result

    # A chat is not durable project memory. Inspect the continuity artifact
    # before trusting operational rows, without obeying arbitrary Markdown
    # text as executable instructions or exporting its confidential contents.
    continuity = root / CONTINUITY
    if continuity.is_symlink() or not continuity.is_file():
        result["blockers"].append("CONTINUITY_MISSING_OR_UNSAFE")
        return result
    try:
        saved_text = continuity.read_text(encoding="utf-8")
        if not saved_text.strip():
            result["blockers"].append("CONTINUITY_EMPTY")
            return result
    except (OSError, UnicodeError):
        result["blockers"].append("CONTINUITY_UNREADABLE")
        return result
    result["continuity_document_read"] = True
    continuity_candidates = recorded_next_ids(saved_text)
    if len(set(continuity_candidates)) > 1:
        result["blockers"].append("CONTINUITY_CONFLICTING_NEXT_ACTIONS")
        return result
    recorded_next = continuity_candidates[0] if continuity_candidates else None

    pending = sorted(active_journals(root))
    if pending:
        result["blockers"].append("PENDING_RESEARCH_TRANSACTION_RECOVERY")
        result["pending_journals"] = pending
        return result

    gates, gate_problems = read_csv(root, GATES, "GATE_ID")
    tasks, task_problems = read_csv(root, TASKS, "CADA_ID")
    result["blockers"].extend(gate_problems + task_problems)
    if result["blockers"]:
        return result
    gate_by_id = {clean(row.get("GATE_ID")): row for row in gates}
    if set(gate_by_id) != set(EXPECTED_GATES):
        result["blockers"].append("SEVEN_GATES_NOT_PRESENT_OR_UNEXPECTED")
        return result
    next_gate = next(
        (gate_by_id[gid] for gid in EXPECTED_GATES
         if not documented_gate(gate_by_id[gid])), None)
    if next_gate is not None:
        result["next_gate_id"] = clean(next_gate.get("GATE_ID"))

    # A recorded DONE without completion evidence does not satisfy an
    # operational dependency. Never promote C.A.D.A. DONE to gate approval.
    by_id = {clean(row.get("CADA_ID")): row for row in tasks}
    first_blocked = None
    candidate = None
    gate_stage = stage_num(next_gate.get("Scientific_stage")) if next_gate else None
    for task in tasks:
        status = upper(task.get("Status"))
        if status in TERMINAL:
            continue
        tid = clean(task.get("CADA_ID"))
        if status not in EXECUTABLE:
            if first_blocked is None:
                first_blocked = (tid, "TASK_NOT_READY")
            continue
        if not clean(task.get("Next_action")):
            if first_blocked is None:
                first_blocked = (tid, "MISSING_RECORDED_NEXT_ACTION")
            continue
        ok, why = task_dependencies_met(task, by_id)
        if not ok:
            if first_blocked is None:
                first_blocked = (tid, why)
            continue
        task_stage = stage_num(task.get("Scientific_stage"))
        if (gate_stage is not None and task_stage is not None
                and task_stage > gate_stage):
            if first_blocked is None:
                first_blocked = (tid, "PRIOR_HUMAN_GATE_NOT_DOCUMENTED")
            continue
        candidate = task
        break

    if candidate:
        result["next_task_id"] = clean(candidate.get("CADA_ID"))
        result["action_recorded"] = True
        execution = upper(candidate.get("Execution_mode"))
        owner = upper(candidate.get("Assigned_to"))
        if execution in DECISION_EXECUTION or (
                "RESEARCHER" in owner and "AGENT" not in owner):
            result["status"] = "HUMAN_TASK_DECISION_REQUIRED"
            result["requires_human_decision"] = True
        elif execution in {"AUTONOMOUS", "AUTONOMOUS_WITH_USER_DECISIONS"}:
            result["status"] = "TECHNICAL_PREPARATION_AVAILABLE"
            result["technical_preparation_possible"] = True
        else:
            # Unknown execution permission does not grant autonomy.
            result["status"] = "TASK_EXECUTION_PERMISSION_REVIEW"
            result["requires_human_decision"] = True
    elif next_gate is not None:
        result["status"] = "HUMAN_GATE_DECISION_REQUIRED"
        result["requires_human_decision"] = True
        if first_blocked:
            result["blocked_task_id"] = first_blocked[0]
            result["blockers"].append(first_blocked[1])
    elif first_blocked:
        result["status"] = "BLOCKED_TASK"
        result["blocked_task_id"] = first_blocked[0]
        result["blockers"].append(first_blocked[1])
    else:
        result["status"] = "NO_RECORDED_NEXT_ACTION"
        # Seven recorded approvals do not prove that a manuscript was sent.
        result["requires_human_decision"] = True

    # The continuity record and C.A.D.A. are both durable source records.
    # A stale next-action ID cannot authorize an unrelated technical task.
    if recorded_next:
        if result["next_task_id"] and recorded_next != result["next_task_id"]:
            result["status"] = "CONTINUITY_RECONCILIATION_REQUIRED"
            result["technical_preparation_possible"] = False
            result["requires_human_decision"] = True
            result["blockers"].append("CONTINUITY_NEXT_ACTION_MISMATCH")
        elif not result["next_task_id"] and next_gate is not None:
            # A completed operational task commonly leaves a stale markdown
            # note: retain the real pending human gate, but flag reconciliation.
            result["blockers"].append("CONTINUITY_NEXT_ACTION_NOT_CURRENT")

    # A local copy is not evidence of a writable, synchronized Drive.
    # Only an explicitly authorized WORK_FALLBACK permits local navigation
    # without separately consulting the connected canonical Drive.
    storage = clean(config.get("storage_mode"))
    if not (storage == "WORK_FALLBACK"
            and config.get("fallback_authorized") is True):
        result["status"] = "CANONICAL_STORAGE_RECHECK_REQUIRED"
        result["technical_preparation_possible"] = False
        result["blockers"].append("CANONICAL_STORAGE_NOT_VERIFIED")
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project")
    parser.add_argument("--intent", choices=["next", "proximo", "próximo", "resume"],
                        default="next", help="Read-only routing, never gate approval")
    args = parser.parse_args(argv)
    try:
        outcome = resolve(Path(args.project))
    except (OSError, ValueError, TypeError, csv.Error):
        print("ERROR: UNREADABLE_PROJECT_CONTINUITY", file=sys.stderr)
        return 1
    print(json.dumps(outcome, ensure_ascii=False, indent=2))
    return 0 if not outcome["blockers"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
