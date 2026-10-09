#!/usr/bin/env python3
"""Generate a deterministic reviewer/editor transparency report from canonical project state."""
from __future__ import annotations

import argparse, csv, json
from datetime import datetime, timezone
from pathlib import Path

from audit_governance_boundary import audit as audit_cada_boundary

MGMT="00_Gestao_e_Continuidade"

def rows(root:Path, name:str)->list[dict[str,str]]:
    p=root/MGMT/name
    if not p.exists(): return []
    with p.open("r",encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

def kv_project(root:Path)->dict[str,str]:
    p=root/MGMT/"00_Projeto.csv"
    out={}
    if p.exists():
        for r in rows(root,"00_Projeto.csv"):
            k=(r.get("Field") or "").strip()
            if k: out[k]=(r.get("Value") or "").strip()
    cfg=root/MGMT/"PROJECT_CONFIG.json"
    if cfg.exists():
        try:
            data=json.loads(cfg.read_text(encoding="utf-8"))
            for k,v in data.items():
                if k not in out and isinstance(v,(str,int,float,bool)):
                    out[k]=str(v)
        except Exception:
            pass
    return out

def count_nonempty(rs:list[dict[str,str]], field:str)->int:
    return sum(1 for r in rs if (r.get(field) or "").strip())

def report_data(root:Path)->dict:
    project=kv_project(root)
    protocol=rows(root,"01_Protocolo.csv")
    searches=rows(root,"02_Search_Log.csv")
    screening=rows(root,"03_Screening.csv")
    fulltext=rows(root,"04_FullText_Tracker.csv")
    evidence=rows(root,"05_Evidence_Matrix.csv")
    synthesis=rows(root,"08_Synthesis_Log.csv")
    claims=rows(root,"09_Claims_Ledger.csv")
    cada=rows(root,"11_CADA_Control.csv")
    trace=rows(root,"13_Traceability_Log.csv")
    ai=rows(root,"14_AI_Use_Log.csv")
    interop=rows(root,"16_Interoperabilidade.csv")
    decisions=rows(root,"17_Decision_Log.csv")
    gates=rows(root,"18_Human_Validation_Gates.csv")
    snaps=rows(root,"19_Snapshots.csv")
    submission=rows(root,"10_Submission_Checklist.csv")
    journal_profile_path=root/"06_Submissao/Regras_da_Revista/JOURNAL_PROFILE.json"
    journal_profile=None
    if journal_profile_path.exists():
        try:
            journal_profile=json.loads(journal_profile_path.read_text(encoding="utf-8"))
        except Exception:
            journal_profile={"status":"INVALID","notes":"JOURNAL_PROFILE.json exists but could not be parsed."}
    corpus_map_path=root/"04_Evidencias_e_Sintese/MAPA_CORPUS.json"
    corpus_map=None
    if corpus_map_path.exists():
        try:
            corpus_map=json.loads(corpus_map_path.read_text(encoding="utf-8"))
        except Exception:
            corpus_map={"warnings":["MAPA_CORPUS.json exists but could not be parsed."]}

    executed_searches=[
        r for r in searches
        if (r.get("Status") or "").upper() not in {"","PLANNED","INVALID","SUPERSEDED"}
    ]
    included=sum(1 for r in screening if (r.get("Pass1_decision") or "").upper()=="INCLUDE")
    borderline=sum(1 for r in screening if (r.get("Pass1_decision") or "").upper()=="BORDERLINE")
    excluded=sum(1 for r in screening if (r.get("Pass1_decision") or "").upper()=="EXCLUDE")
    from screening_review import audit_rows as audit_screening_rows
    screening_checks=audit_screening_rows(screening,enforce=True)

    from appraise_evidence import audit as audit_critical_appraisals
    quality=audit_critical_appraisals(evidence)
    substantive=[r for r in ai if (r.get("Materiality") or "").upper()=="SUBSTANTIVE"]
    substantive_pending=[
        r for r in substantive
        if not (r.get("Human_review_method") or "").strip()
        or (r.get("Accepted_modified_or_rejected") or "").upper() in {"","PENDING"}
    ]
    claims_without_evidence=[
        r for r in claims if (r.get("Claim_ID") or "").strip() and not (r.get("Evidence_IDs") or "").strip()
    ]
    claims_not_audited=[
        r for r in claims
        if (r.get("Claim_ID") or "").strip()
        and (r.get("Robustness_status") or "").upper().strip() in {"","NOT_AUDITED"}
    ]
    claims_revise_or_reject=[
        r for r in claims
        if (r.get("Claim_ID") or "").strip()
        and (r.get("Robustness_status") or "").upper().strip() in {"REVISE","REJECT"}
    ]
    claims_qualified=[
        r for r in claims
        if (r.get("Claim_ID") or "").strip()
        and (r.get("Robustness_status") or "").upper().strip()=="QUALIFIED"
    ]
    claims_robust=[
        r for r in claims
        if (r.get("Claim_ID") or "").strip()
        and (r.get("Robustness_status") or "").upper().strip()=="ROBUST"
    ]
    done_without_evidence=[
        r for r in cada
        if (r.get("Status") or "").upper()=="DONE" and not (r.get("Completion_evidence") or "").strip()
    ]
    gates_pending=[
        r for r in gates
        if (r.get("Status") or "").upper() not in {"COMPLETED","NOT_APPLICABLE"}
    ]

    boundary=audit_cada_boundary(root,strict=False)

    return {
        "generated_at":datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "project":project,
        "counts":{
            "protocol_rows":len(protocol),
            "search_runs":len(searches),
            "executed_searches":len(executed_searches),
            "screening_records":len(screening),
            "screening_include":included,
            "screening_borderline":borderline,
            "screening_exclude":excluded,
            "screening_ai_suggestions":screening_checks["counts"]["ai_suggestions"],
            "screening_unreviewed_suggestions":screening_checks["counts"]["unreviewed_suggestions"],
            "screening_recorded_pass1":screening_checks["counts"]["recorded_pass1"],
            "screening_recorded_pass2":screening_checks["counts"]["recorded_pass2"],
            "screening_documentation_errors":len(screening_checks["errors"]),
            "fulltext_records":len(fulltext),
            "evidence_items":len(evidence),
            "appraised_evidence_items":quality["counts"]["assessed"],
            "unappraised_evidence_items":quality["counts"]["unassessed"],
            "appraisal_items_with_caveats":quality["counts"]["with_caveats"],
            "appraisal_documentation_errors":len(quality["errors"]),
            "synthesis_items":len(synthesis),
            "claims":len([r for r in claims if (r.get("Claim_ID") or "").strip()]),
            "claims_robust":len(claims_robust),
            "claims_qualified":len(claims_qualified),
            "claims_not_audited":len(claims_not_audited),
            "claims_revise_or_reject":len(claims_revise_or_reject),
            "trace_events":len([r for r in trace if (r.get("Trace_ID") or "").strip()]),
            "trace_confirmed":sum(1 for r in trace if (r.get("Status") or "").upper()=="CONFIRMED"),
            "trace_unverified":sum(1 for r in trace if (r.get("Status") or "").upper()=="UNVERIFIED"),
            "trace_legacy_complete":sum(1 for r in trace if (r.get("Status") or "").upper()=="COMPLETE"),
            "material_decisions":len([r for r in decisions if (r.get("DEC_ID") or "").strip()]),
            "human_gates":len([r for r in gates if (r.get("GATE_ID") or "").strip()]),
            "snapshots":len([r for r in snaps if (r.get("SNAP_ID") or "").strip()]),
            "substantive_ai_uses":len(substantive),
            "interop_exports":len([r for r in interop if (r.get("Export_ID") or "").strip()]),
            "corpus_map_generated":1 if corpus_map else 0,
        },
        "governance_boundary":boundary,
        "executed_searches":executed_searches,
        "decisions":decisions,
        "gates":gates,
        "snapshots":snaps,
        "substantive_ai":substantive,
        "interop":interop,
        "corpus_map":corpus_map,
        "journal_profile":journal_profile,
        "submission_checklist":submission,
        "gaps":{
            "claims_without_evidence":[r.get("Claim_ID") for r in claims_without_evidence],
            "claims_not_robustness_audited":[r.get("Claim_ID") for r in claims_not_audited],
            "claims_revise_or_reject":[r.get("Claim_ID") for r in claims_revise_or_reject],
            "done_cada_without_completion_evidence":[r.get("CADA_ID") for r in done_without_evidence],
            "substantive_ai_pending_validation":[r.get("AI_Use_ID") for r in substantive_pending],
            "gates_not_completed":[r.get("GATE_ID") for r in gates_pending],
            "executed_search_without_literal_query":[r.get("Search_ID") for r in executed_searches if not (r.get("Literal_query") or "").strip()],
        }
    }

def md_list(vals):
    vals=[v for v in vals if v]
    return "\n".join(f"- {v}" for v in vals) if vals else "- None detected"

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--output-dir",default="")
    a=ap.parse_args()

    root=Path(a.project).resolve()
    data=report_data(root)
    stamp=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    outdir=Path(a.output_dir).resolve() if a.output_dir else root/"06_Submissao/Arquivos_Finais"
    outdir.mkdir(parents=True,exist_ok=True)
    base=outdir/f"RELATORIO_TRANSPARENCIA_{stamp}"
    json_path=base.with_suffix(".json")
    md_path=base.with_suffix(".md")
    json_path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

    p=data["project"]; c=data["counts"]; gaps=data["gaps"]
    lines=[
        "# Relatório de Transparência e Rastreabilidade",
        "",
        f"Generated: {data['generated_at']}",
        "",
        "## 1. Project identity and research object",
        f"- Project: {p.get('project_name') or p.get('Título curto do projeto') or root.name}",
        f"- Original research input: {p.get('research_input') or p.get('Problema original') or 'Not available in canonical project metadata'}",
        f"- Article/review design: {p.get('article_type') or p.get('Desenho metodológico') or 'Not yet frozen'}",
        f"- Management mode: {p.get('work_management_mode') or p.get('Modo de gestão') or 'Not recorded'}",
        "",
        "## 1.1. Operational management versus scientific evidence",
        f"- C.A.D.A. recorded tasks: {data['governance_boundary']['management_activity']['recorded_tasks']}",
        f"- C.A.D.A. tasks marked DONE: {data['governance_boundary']['management_activity']['tasks_marked_done']}",
        f"- C.A.D.A. DONE entries with no independent completion proof: {data['governance_boundary']['management_activity']['done_without_meaningful_completion_evidence']}",
        "- DONE denotes an operational status only; it is not proof of scientific rigor.",
        f"- Recorded scientific gate approvals: {data['governance_boundary']['scientific_registers']['gate_approvals_recorded']}",
        f"- Recorded Evidence_IDs and claims: {data['governance_boundary']['scientific_registers']['evidence_records']} / {data['governance_boundary']['scientific_registers']['claims_registered']}",
        "- Scientific entries are reported separately; their counts do not certify methodological quality.",
        "- Causal efficiency improvement from C.A.D.A.: NOT_MEASURED (prospective comparison pending).",
        "",
        "## 1.5. Journal-aware construction",
        f"- Target journal: {(data.get('journal_profile') or {}).get('journal_name') or p.get('target_journal') or 'TO_DEFINE'}",
        f"- Construction mode: {(data.get('journal_profile') or {}).get('construction_mode') or p.get('journal_construction_mode') or 'JOURNAL_NEUTRAL'}",
        f"- Journal profile status: {(data.get('journal_profile') or {}).get('status') or p.get('journal_profile_status') or 'TO_DEFINE'}",
        f"- Official rules verified: {(data.get('journal_profile') or {}).get('official_rules_verified') if data.get('journal_profile') is not None else 'not recorded'}",
        f"- Rules verified at: {(data.get('journal_profile') or {}).get('rules_verified_at') or '—'}",
        f"- Submission checklist items: {len(data.get('submission_checklist') or [])}",
        "",
        "## 2. Methodological design and protocol status",
        f"- Protocol records: {c['protocol_rows']}",
        f"- Material decisions recorded: {c['material_decisions']}",
        "",
        "### Material scientific decisions",
    ]
    if data["decisions"]:
        for r in data["decisions"]:
            did=(r.get("DEC_ID") or "").strip()
            if not did: continue
            lines.append(
                f"- {did} [{r.get('Status') or '—'}] {r.get('Decision_type') or 'OTHER'} — "
                f"{r.get('Decision') or 'No decision text'}"
                + (f" — rationale: {r.get('Rationale')}" if (r.get("Rationale") or "").strip() else "")
            )
    else:
        lines.append("- No material decisions recorded.")

    lines += [
        "",
        "## 3. Search provenance and corpus status",
        f"- Search runs logged: {c['search_runs']}",
        f"- Locally confirmed TRACE executions: {c['trace_confirmed']}",
        f"- Unverified TRACE declarations/records: {c['trace_unverified']}",
        f"- Legacy TRACE COMPLETE records (not proof): {c['trace_legacy_complete']}",
        "- Search-log statuses are not independent proof of a provider query; compare actual exports and provider receipts.",
        f"- Executed/active search runs: {c['executed_searches']}",
        f"- Screening records: {c['screening_records']}",
        f"- Pass-1 INCLUDE: {c['screening_include']}",
        f"- Pass-1 BORDERLINE: {c['screening_borderline']}",
        f"- Pass-1 EXCLUDE: {c['screening_exclude']}",
        f"- AI screening suggestions (not final decisions): {c['screening_ai_suggestions']}",
        f"- Suggestions awaiting human review: {c['screening_unreviewed_suggestions']}",
        f"- Recorded Pass-1/Pass-2 final decisions: {c['screening_recorded_pass1']} / {c['screening_recorded_pass2']}",
        f"- Screening provenance problems: {c['screening_documentation_errors']}",
        "- Recorded reviewer fields are attestations, not independent authentication of human identity.",
        f"- Full-text tracker records: {c['fulltext_records']}",
        f"- Evidence items with documented appraisal: {c['appraised_evidence_items']}",
        f"- Evidence items without appraisal: {c['unappraised_evidence_items']}",
        f"- Appraisals requiring caveats: {c['appraisal_items_with_caveats']}",
        f"- Appraisal documentation problems: {c['appraisal_documentation_errors']}",
        "- Appraisal records are attributed judgments; they do not independently certify scientific quality or reviewer identity.",
        "",
        "### Executed searches",
    ]
    if data["executed_searches"]:
        for r in data["executed_searches"]:
            lines.append(
                f"- {r.get('Search_ID') or 'unnamed search'} — {r.get('Database_or_source') or 'source not recorded'}"
                f" — found={r.get('Records_found') or '—'} — exported={r.get('Records_exported') or '—'}"
            )
    else:
        lines.append("- No executed searches recorded.")

    lines += [
        "",
        "### Corpus Map / grounded corpus status",
        f"- Corpus Map generated: {'yes' if data.get('corpus_map') else 'no'}",
        f"- Grounded Corpus Mode enabled in project configuration: {p.get('grounded_corpus_mode_enabled') or 'not recorded'}",
    ]
    if data.get("corpus_map"):
        cm=data["corpus_map"] or {}
        coverage=cm.get("coverage") or {}
        lines += [
            f"- Retained records represented: {coverage.get('retained_records','—')}",
            f"- DOI coverage: {coverage.get('doi_coverage','—')}",
            f"- OpenAlex coverage: {coverage.get('openalex_coverage','—')}",
            f"- Edge definition: {cm.get('edge_definition') or 'none / not available'}",
            f"- Clusters generated: {len(cm.get('clusters') or [])}",
            f"- Bridge records generated: {len(cm.get('bridge_records') or [])}",
        ]
        for warning in (cm.get("warnings") or []):
            lines.append(f"- Corpus Map warning: {warning}")

    lines += [
        "",
        "## 4. Evidence and claim coverage",
        f"- Evidence items: {c['evidence_items']}",
        f"- Synthesis items: {c['synthesis_items']}",
        f"- Claims: {c['claims']}",
        f"- Claims ROBUST: {c['claims_robust']}",
        f"- Claims QUALIFIED: {c['claims_qualified']}",
        f"- Claims not robustness-audited: {c['claims_not_audited']}",
        f"- Claims pending REVISE/REJECT: {c['claims_revise_or_reject']}",
        "",
        "## 5. Human validation gates",
    ]
    if data["gates"]:
        for r in data["gates"]:
            gid=(r.get("GATE_ID") or "").strip()
            if not gid: continue
            lines.append(
                f"- {gid} — {r.get('Name') or r.get('Gate_type') or 'gate'}"
                f" — status={r.get('Status') or '—'}"
                f" — decision={r.get('Decision') or 'PENDING'}"
                + (f" — validated_by={r.get('Validated_by')}" if (r.get("Validated_by") or "").strip() else "")
            )
    else:
        lines.append("- No validation gates recorded.")

    lines += [
        "",
        "## 6. Frozen snapshots",
    ]
    if data["snapshots"]:
        for r in data["snapshots"]:
            sid=(r.get("SNAP_ID") or "").strip()
            if sid:
                lines.append(
                    f"- {sid} — {r.get('Milestone') or 'snapshot'}"
                    f" — validation={r.get('Validation_status') or '—'}"
                    + (f" — SHA-256={r.get('Manifest_SHA256')}" if (r.get("Manifest_SHA256") or "").strip() else "")
                )
    else:
        lines.append("- No snapshots recorded.")

    lines += [
        "",
        "## 7. AI use and human review",
        f"- Substantive AI-use records: {c['substantive_ai_uses']}",
    ]
    if data["substantive_ai"]:
        for r in data["substantive_ai"]:
            lines.append(
                f"- {r.get('AI_Use_ID') or 'AI use'} — {r.get('Platform_or_tool') or 'tool not recorded'}"
                f" — purpose={r.get('Purpose') or '—'}"
                f" — review={r.get('Human_review_method') or 'PENDING'}"
                f" — decision={r.get('Accepted_modified_or_rejected') or 'PENDING'}"
            )
    else:
        lines.append("- No substantive AI use recorded.")

    lines += [
        "",
        "## 8. Interoperability / provenance exports",
        f"- W3C PROV / RO-Crate exports: {c['interop_exports']}",
    ]
    if data["interop"]:
        for r in data["interop"]:
            eid=(r.get("Export_ID") or "").strip()
            if eid:
                lines.append(
                    f"- {eid} — validation={r.get('Validation_status') or '—'}"
                    + (f" — SHA-256={r.get('Package_SHA256')}" if (r.get("Package_SHA256") or "").strip() else "")
                )
    else:
        lines.append("- No interoperability export recorded.")

    lines += [
        "",
        "## 9. Unresolved traceability gaps",
        "",
        "### Claims without Evidence_ID",
        md_list(gaps["claims_without_evidence"]),
        "",
        "### Claims without robustness audit",
        md_list(gaps["claims_not_robustness_audited"]),
        "",
        "### Claims still marked REVISE/REJECT",
        md_list(gaps["claims_revise_or_reject"]),
        "",
        "### DONE C.A.D.A. items without completion evidence",
        md_list(gaps["done_cada_without_completion_evidence"]),
        "",
        "### Substantive AI uses pending human validation",
        md_list(gaps["substantive_ai_pending_validation"]),
        "",
        "### Human gates not completed",
        md_list(gaps["gates_not_completed"]),
        "",
        "### Executed searches without literal query",
        md_list(gaps["executed_search_without_literal_query"]),
        "",
        "## 10. Interpretation and limits",
        "",
        "This report exposes the documented construction process. It does not by itself establish scientific validity, reproducibility, or absence of error. Those require evaluation of the underlying method, evidence, analysis, reasoning, and human responsibility.",
    ]
    md_path.write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(md_path)
    print(json_path)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
