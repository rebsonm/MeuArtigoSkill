#!/usr/bin/env python3
"""Record a researcher's method-route decision without rebuilding a project.

Does not authenticate identity or claim that research was performed.
Canonical existing DEC/TRACE records are retained; no new ID family.
Only projects initialized with route governance can use this command.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from method_routes import GATE_VARIANTS, MGMT, ROUTES, new_profile


def _load_csv(path: Path) -> tuple[list[str], list[dict]]:
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return reader.fieldnames or [], list(reader)


def choose(root: Path, route: str, reviewer: str, evidence: str, rationale: str) -> str:
    root = Path(root).resolve()
    if route not in ROUTES or route == "UNDECIDED":
        raise ValueError("Choose one explicitly named scientific route")
    if len(reviewer.strip()) < 3 or len(evidence.strip()) < 5 or len(rationale.split()) < 6:
        raise ValueError("Real researcher, human-decision reference and substantive rationale required")
    config_path = root / MGMT / "PROJECT_CONFIG.json"
    method_path = root / MGMT / "METHOD_PROFILE.json"
    gate_path = root / MGMT / "18_Human_Validation_Gates.csv"
    cfg = json.loads(config_path.read_text(encoding="utf-8"))
    if cfg.get("method_route_governance_required") is not True:
        raise ValueError("Legacy project: do not silently migrate historical scientific decisions")
    previous = cfg.get("method_route")
    if previous not in ROUTES:
        raise ValueError("Unknown existing route; review project configuration")
    current = json.loads(method_path.read_text(encoding="utf-8"))
    if current.get("route") != previous:
        raise ValueError("Current route and method profile disagree")
    header, gates = _load_csv(gate_path)
    if route != previous:
        for row in gates:
            if row.get("GATE_ID") in {"GATE-0002","GATE-0003","GATE-0004","GATE-0005","GATE-0006","GATE-0007"} and (
                (row.get("Status") or "").upper() in {"COMPLETED","NOT_APPLICABLE"}
            ):
                raise ValueError("Cannot change route after method/data/scientific approval: review and migrate manually")
    if current.get("route_confirmation") == "HUMAN_CONFIRMED" and route == previous:
        raise ValueError("Route already confirmed; revise through a documented superseding decision")
    updated_method = dict(current) if previous == route else new_profile(route,cfg.get("article_type") or "")
    updated_method["route_confirmation"] = "HUMAN_CONFIRMED"
    updated_method["human_route_reviewer"] = reviewer.strip()
    updated_method["human_route_decision_evidence"] = evidence.strip()
    updated_method["human_route_rationale"] = rationale.strip()
    cfg["method_route"] = route

    for row in gates:
        gid=row.get("GATE_ID")
        if gid == "GATE-0002":
            row["Entry_condition"]="Perfil metodológico preparado e escolhas justificadas pelo pesquisador."
            row["Items_to_validate"]="Pergunta, inferência visada, abordagem, decisão humana e limites."
            row["Blocking_transition"]="Etapa pertinente ao desenho escolhido"
        if gid in GATE_VARIANTS[route]:
            typ, name, entry, checks = GATE_VARIANTS[route][gid]
            row.update({"Gate_type":typ,"Name":name,"Entry_condition":entry,"Items_to_validate":checks})

    # Preserve real human-decision provenance in existing tables first.
    script = Path(__file__).with_name("governance_events.py")
    result = subprocess.run([
        sys.executable, str(script), "decision", str(root),
        "--type", "METHOD", "--stage", "02-03",
        "--question", "Qual desenho científico orientará este projeto?",
        "--decision", route, "--status", "APPROVED",
        "--decided-by", reviewer.strip(),
        "--evidence", evidence.strip(), "--rationale", rationale.strip(),
        "--alternatives", f"Previous proposed route: {previous}",
        "--artifacts", "00_Gestao_e_Continuidade/METHOD_PROFILE.json; 00_Gestao_e_Continuidade/PROJECT_CONFIG.json; 00_Gestao_e_Continuidade/18_Human_Validation_Gates.csv",
    ], capture_output=True, text=True)
    if result.returncode:
        raise ValueError("Could not preserve human route decision: " + (result.stderr or result.stdout)[:300])
    did = next((line.split("=",1)[1].strip() for line in result.stdout.splitlines()
                if line.startswith("decision_id=")), "")
    if not did:
        raise ValueError("Human method decision was logged but lacked a returned DEC_ID")
    updated_method["route_decision_id"]=did

    # Inputs have already been validated and the decision written. No scientific
    # data/evidence/screening tables are reconstructed or deleted.
    config_path.write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    method_path.write_text(json.dumps(updated_method,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    with gate_path.open("w",newline="",encoding="utf-8-sig") as f:
        writer=csv.DictWriter(f,fieldnames=header)
        writer.writeheader()
        writer.writerows([{key:row.get(key,"") for key in header} for row in gates])
    return did


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("project")
    ap.add_argument("--route", choices=[x for x in ROUTES if x!="UNDECIDED"],required=True)
    ap.add_argument("--decided-by",required=True,help="Real researcher who made this choice")
    ap.add_argument("--evidence",required=True,help="Actual human decision/message reference")
    ap.add_argument("--rationale",required=True,help="Researcher's genuine reason for selecting this design")
    a = ap.parse_args(argv)
    try:
        did = choose(Path(a.project),a.route,a.decided_by,a.evidence,a.rationale)
    except (ValueError,OSError,KeyError,TypeError,json.JSONDecodeError) as exc:
        ap.error(str(exc))
    print(f"route_confirmed={a.route}")
    print(f"decision_id={did}")
    print("scientific_method_validated=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
