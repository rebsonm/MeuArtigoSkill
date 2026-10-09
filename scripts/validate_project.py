#!/usr/bin/env python3
"""Validate the canonical local mirror of a Meu Artigo project."""
from __future__ import annotations
import argparse,csv,json,hashlib
from pathlib import Path
from formative_gates import gate_issues
from screening_review import audit_rows as audit_screening_rows
from appraise_evidence import audit as audit_appraisals
from claim_integrity import audit as audit_claim_integrity
from audit_governance_boundary import audit as audit_cada_boundary
from rights_audit import audit_project as audit_fulltext_rights

REQUIRED=[
"00_Gestao_e_Continuidade/CONTINUIDADE.md",
"00_Gestao_e_Continuidade/PROTOCOLO.md",
"00_Gestao_e_Continuidade/02_Search_Log.csv",
"00_Gestao_e_Continuidade/03_Screening.csv",
"00_Gestao_e_Continuidade/04_FullText_Tracker.csv",
"00_Gestao_e_Continuidade/05_Evidence_Matrix.csv",
"00_Gestao_e_Continuidade/11_CADA_Control.csv",
"00_Gestao_e_Continuidade/12_PM_Sync.csv",
"00_Gestao_e_Continuidade/13_Traceability_Log.csv",
"00_Gestao_e_Continuidade/14_AI_Use_Log.csv",
"00_Gestao_e_Continuidade/15_CADA_Dashboard.csv",
"00_Gestao_e_Continuidade/RASTREABILIDADE.md",
"00_Gestao_e_Continuidade/16_Interoperabilidade.csv",
"00_Gestao_e_Continuidade/17_Decision_Log.csv",
"00_Gestao_e_Continuidade/18_Human_Validation_Gates.csv",
"00_Gestao_e_Continuidade/19_Snapshots.csv",
"00_Gestao_e_Continuidade/ANONYMIZATION_PROFILE.json",
]
PASS1={"","INCLUDE","BORDERLINE","EXCLUDE"}
PASS2={"","FULL TEXT — CORE","FULL TEXT — SUPPORT","EXCLUDE","FULL TEXT - CORE","FULL TEXT - SUPPORT"}
EPI={"","L","I","P","[L]","[I]","[P]"}
CADA_STATUS={"CAPTURED","ASSIGNED","READY","IN_PROGRESS","WAITING","BLOCKED","DONE","CANCELLED","SUPERSEDED"}
CADA_TERMINAL={"DONE","CANCELLED","SUPERSEDED"}
DEADLINE_TYPES={"EXTERNAL","USER_SET","INTERNAL_TARGET","DEPENDENCY","TO_DEFINE"}
TRACE_STATUS={"PLANNED","IN_PROGRESS","COMPLETE","CONFIRMED","UNVERIFIED","PARTIAL","FAILED","INVALID","SUPERSEDED"}
AI_MATERIALITY={"ASSISTIVE","SUBSTANTIVE","ADMINISTRATIVE","NOT_APPLICABLE"}
AI_DECISION={"","ACCEPTED","MODIFIED","REJECTED","PENDING"}
JOURNAL_MODES={"JOURNAL_NEUTRAL","JOURNAL_AWARE_PENDING_PROFILE","JOURNAL_AWARE"}
JOURNAL_PROFILE_STATUS={"TO_DEFINE","PENDING_RULES","LOADED","VERIFIED","SUPERSEDED"}
CLAIM_ROBUSTNESS={"","NOT_AUDITED","ROBUST","QUALIFIED","REVISE","REJECT","NOT_APPLICABLE"}
HUMAN_VALIDATION={"","PENDING","VALIDATED","REVISED","REJECTED","NOT_APPLICABLE"}
ANON_STATUS={"TO_CONFIGURE","CONFIGURED","VERIFIED","NOT_REQUIRED"}
EXTERNAL_ARTIFACT_MODE={"EXTERNAL_ANONYMIZED","EXTERNAL_IDENTIFIED","INTERNAL_IDENTIFIED"}
STORAGE_MODES={"GOOGLE_DRIVE_STAGING","GOOGLE_DRIVE","WORK_FALLBACK"}
STORAGE_STATES={"DRIVE_WORKSPACE_READY","DRIVE_STAGING_PENDING_UPLOAD","WORK_FALLBACK_AUTHORIZED"}

def rows(path):
    with path.open("r",encoding="utf-8-sig",newline="") as f:
        yield from csv.DictReader(f)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("project_path")
    a=ap.parse_args()
    root=Path(a.project_path).resolve()
    errors=[];warnings=[]
    cfg_data={}

    for rel in REQUIRED:
        if not (root/rel).exists():
            errors.append(f"missing required artifact: {rel}")

    cfg=root/"00_Gestao_e_Continuidade/PROJECT_CONFIG.json"
    if cfg.exists():
        try:
            cfg_data=json.loads(cfg.read_text(encoding="utf-8"))
            if not str(cfg_data.get("research_input","")).strip():
                warnings.append("PROJECT_CONFIG research_input is empty")
            if cfg_data.get("cada_governance") is not True:
                warnings.append("PROJECT_CONFIG cada_governance is not true")
            if cfg_data.get("traceability_enabled") is not True:
                warnings.append("PROJECT_CONFIG traceability_enabled is not true")
            storage_policy=str(cfg_data.get("storage_policy") or "").strip().upper()
            storage_mode=str(cfg_data.get("storage_mode") or "").strip().upper()
            storage_state=str(cfg_data.get("storage_state") or "").strip().upper()
            if storage_policy:
                if storage_policy!="GOOGLE_DRIVE_FIRST":
                    errors.append(f"PROJECT_CONFIG unexpected storage_policy={storage_policy!r}")
                if storage_mode not in STORAGE_MODES:
                    errors.append(f"PROJECT_CONFIG unexpected storage_mode={storage_mode!r}")
                if storage_state not in STORAGE_STATES:
                    errors.append(f"PROJECT_CONFIG unexpected storage_state={storage_state!r}")
                if storage_mode=="WORK_FALLBACK":
                    if cfg_data.get("fallback_authorized") is not True:
                        errors.append("WORK_FALLBACK is active without explicit fallback_authorized=true")
                    if not str(cfg_data.get("fallback_authorized_by") or "").strip():
                        errors.append("WORK_FALLBACK lacks fallback_authorized_by")
                    if not str(cfg_data.get("fallback_authorized_at") or "").strip():
                        errors.append("WORK_FALLBACK lacks fallback_authorized_at")
                if storage_state=="DRIVE_WORKSPACE_READY" and not str(cfg_data.get("google_drive_workspace_url") or "").strip():
                    errors.append("DRIVE_WORKSPACE_READY lacks google_drive_workspace_url")
                if storage_state=="DRIVE_STAGING_PENDING_UPLOAD":
                    warnings.append("Google Drive is canonical but current scaffold is still pending upload/synchronization; local/Work output is not canonical project state")
            else:
                warnings.append("PROJECT_CONFIG has no GOOGLE_DRIVE_FIRST storage decision; migrate legacy project state before substantive continuation")

            mode=cfg_data.get("work_management_mode")
            if mode not in {"MATRIX_ONLY","MATRIX_PLUS_EXTERNAL"}:
                warnings.append(f"PROJECT_CONFIG unexpected work_management_mode={mode!r}")
            jmode=cfg_data.get("journal_construction_mode")
            if jmode and jmode not in JOURNAL_MODES:
                errors.append(f"PROJECT_CONFIG unexpected journal_construction_mode={jmode!r}")
            jpstatus=cfg_data.get("journal_profile_status")
            if jpstatus and jpstatus not in JOURNAL_PROFILE_STATUS:
                errors.append(f"PROJECT_CONFIG unexpected journal_profile_status={jpstatus!r}")
        except Exception as e:
            errors.append(f"invalid PROJECT_CONFIG.json: {e}")

    anonymization_profile=root/"00_Gestao_e_Continuidade/ANONYMIZATION_PROFILE.json"
    anonymization_data={}
    if anonymization_profile.exists():
        try:
            anonymization_data=json.loads(anonymization_profile.read_text(encoding="utf-8"))
            astatus=str(anonymization_data.get("status","")).strip().upper()
            if astatus not in ANON_STATUS:
                errors.append(f"ANONYMIZATION_PROFILE unexpected status={astatus!r}")
            amode=str(anonymization_data.get("default_external_artifact_mode","")).strip().upper()
            if amode and amode not in EXTERNAL_ARTIFACT_MODE:
                errors.append(f"ANONYMIZATION_PROFILE unexpected default_external_artifact_mode={amode!r}")
            groups=anonymization_data.get("sensitive_terms")
            if not isinstance(groups,dict):
                errors.append("ANONYMIZATION_PROFILE sensitive_terms must be an object")
            elif any(not isinstance(v,list) for v in groups.values()):
                errors.append("ANONYMIZATION_PROFILE sensitive_terms values must be arrays")
            if astatus=="NOT_REQUIRED" and not str(anonymization_data.get("notes") or "").strip():
                errors.append("ANONYMIZATION_PROFILE is NOT_REQUIRED without rationale in notes")
        except Exception as e:
            errors.append(f"invalid ANONYMIZATION_PROFILE.json: {e}")
    else:
        errors.append("ANONYMIZATION_PROFILE.json is missing")

    journal_profile=root/"06_Submissao/Regras_da_Revista/JOURNAL_PROFILE.json"
    journal_data={}
    if journal_profile.exists():
        try:
            journal_data=json.loads(journal_profile.read_text(encoding="utf-8"))
            jstatus=str(journal_data.get("status","")).strip()
            jmode=str(journal_data.get("construction_mode","")).strip()
            if jstatus and jstatus not in JOURNAL_PROFILE_STATUS:
                errors.append(f"JOURNAL_PROFILE unexpected status={jstatus!r}")
            if jmode and jmode not in JOURNAL_MODES:
                errors.append(f"JOURNAL_PROFILE unexpected construction_mode={jmode!r}")
            if journal_data.get("official_rules_verified") and not str(journal_data.get("rules_verified_at","")).strip():
                warnings.append("JOURNAL_PROFILE marks official rules verified but rules_verified_at is empty")
            if jmode=="JOURNAL_AWARE" and not str(journal_data.get("journal_name","")).strip():
                errors.append("JOURNAL_PROFILE is JOURNAL_AWARE but journal_name is empty")
        except Exception as e:
            errors.append(f"invalid JOURNAL_PROFILE.json: {e}")
    else:
        if str(cfg_data.get("target_journal") or "").strip():
            errors.append("target journal is defined but JOURNAL_PROFILE.json is missing")
        else:
            warnings.append("JOURNAL_PROFILE.json not found; journal-neutral projects should still preserve the canonical profile scaffold")

    log=root/"00_Gestao_e_Continuidade/02_Search_Log.csv"
    if log.exists():
        for i,r in enumerate(rows(log),2):
            st=(r.get("Status") or "").upper()
            if st and st not in {"PLANNED","INVALID","SUPERSEDED"} and not (r.get("Literal_query") or "").strip():
                errors.append(f"search row {i}: executed search lacks Literal_query")

    scr=root/"00_Gestao_e_Continuidade/03_Screening.csv"
    if scr.exists():
        ids=set()
        for i,r in enumerate(rows(scr),2):
            rid=(r.get("Record_ID") or "").strip()
            if rid and rid in ids:
                errors.append(f"screening row {i}: duplicate Record_ID {rid}")
            if rid: ids.add(rid)
            p1=(r.get("Pass1_decision") or "").strip().upper()
            p2=(r.get("Pass2_decision") or "").strip().upper()
            if p1 not in PASS1:
                warnings.append(f"screening row {i}: nonstandard Pass1_decision {p1!r}")
            if p2 not in {x.upper() for x in PASS2}:
                warnings.append(f"screening row {i}: nonstandard Pass2_decision {p2!r}")

    # Human review and AI proposal are independent facts.  Prevent an AI-only
    # proposal or a bare decision cell from counting as validated screening.
    if scr.exists():
        with scr.open("r", encoding="utf-8-sig", newline="") as stream:
            screening_headers=csv.DictReader(stream).fieldnames or []
        gate_path=root/"00_Gestao_e_Continuidade/18_Human_Validation_Gates.csv"
        g4_approved=False
        if gate_path.is_file():
            g4_approved=any(
                (r.get("GATE_ID") or "").strip()=="GATE-0004"
                and (r.get("Status") or "").upper()=="COMPLETED"
                and (r.get("Decision") or "").upper() in {"APPROVED","APPROVED_WITH_CHANGES"}
                for r in rows(gate_path)
            )
        require_human=cfg_data.get("screening_human_decisions_required") is True
        checked=audit_screening_rows(
            list(rows(scr)),enforce=require_human,
            freeze=require_human and g4_approved,headers=screening_headers,
        )
        for problem in checked["errors"]:
            errors.append("screening audit: "+problem)
        for problem in checked["warnings"]:
            warnings.append("screening audit: "+problem)

    ev=root/"00_Gestao_e_Continuidade/05_Evidence_Matrix.csv"
    if ev.exists():
        ids=set()
        for i,r in enumerate(rows(ev),2):
            eid=(r.get("Evidence_ID") or "").strip()
            lab=(r.get("Epistemic_label") or "").strip().upper()
            if eid and eid in ids:
                errors.append(f"evidence row {i}: duplicate Evidence_ID {eid}")
            if eid: ids.add(eid)
            if lab not in EPI:
                warnings.append(f"evidence row {i}: unexpected Epistemic_label {lab!r}")

    cada=root/"00_Gestao_e_Continuidade/11_CADA_Control.csv"
    cada_ids=set()
    if cada.exists():
        for i,r in enumerate(rows(cada),2):
            cid=(r.get("CADA_ID") or "").strip()
            status=(r.get("Status") or "").strip().upper()
            next_action=(r.get("Next_action") or "").strip()
            deadline_type=(r.get("Deadline_type") or "").strip().upper()
            completion=(r.get("Completion_evidence") or "").strip()
            if not cid:
                errors.append(f"CADA row {i}: missing CADA_ID")
                continue
            if cid in cada_ids:
                errors.append(f"CADA row {i}: duplicate CADA_ID {cid}")
            cada_ids.add(cid)
            if not cid.startswith("CADA-"):
                warnings.append(f"CADA row {i}: nonstandard ID {cid!r}")
            if status not in CADA_STATUS:
                warnings.append(f"CADA row {i}: unexpected Status {status!r}")
            if status not in CADA_TERMINAL and not next_action:
                errors.append(f"CADA row {i}: active item {cid} lacks Next_action")
            if status not in CADA_TERMINAL and deadline_type not in DEADLINE_TYPES:
                errors.append(f"CADA row {i}: active item {cid} lacks valid Deadline_type")
            if status=="DONE" and not completion:
                warnings.append(f"CADA row {i}: DONE item {cid} lacks Completion_evidence")

    sync=root/"00_Gestao_e_Continuidade/12_PM_Sync.csv"
    if sync.exists():
        keys=set()
        for i,r in enumerate(rows(sync),2):
            cid=(r.get("CADA_ID") or "").strip()
            provider=(r.get("Provider") or "").strip().lower()
            if not cid and not provider:
                continue
            key=(cid,provider)
            if key in keys:
                errors.append(f"PM sync row {i}: duplicate CADA_ID/provider pair {key}")
            keys.add(key)
            if cid and cada_ids and cid not in cada_ids:
                warnings.append(f"PM sync row {i}: CADA_ID {cid} not found in 11_CADA_Control")

    pm=(cfg_data.get("work_management_provider") if cfg_data else None)
    if pm and sync.exists():
        sync_rows=list(rows(sync))
        if not sync_rows:
            warnings.append(f"PROJECT_CONFIG selects work_management_provider={pm!r} but 12_PM_Sync has no rows yet")

    trace=root/"00_Gestao_e_Continuidade/13_Traceability_Log.csv"
    trace_ids=set()
    if trace.exists():
        for i,r in enumerate(rows(trace),2):
            tid=(r.get("Trace_ID") or "").strip()
            status=(r.get("Status") or "").strip().upper()
            action=(r.get("Action_summary") or "").strip()
            if not tid:
                errors.append(f"trace row {i}: missing Trace_ID")
                continue
            if tid in trace_ids:
                errors.append(f"trace row {i}: duplicate Trace_ID {tid}")
            trace_ids.add(tid)
            if not tid.startswith("TRACE-"):
                warnings.append(f"trace row {i}: nonstandard Trace_ID {tid!r}")
            if not action:
                errors.append(f"trace row {i}: {tid} lacks Action_summary")
            if status and status not in TRACE_STATUS:
                warnings.append(f"trace row {i}: unexpected Status {status!r}")
            cid=(r.get("CADA_ID") or "").strip()
            if cid and cada_ids and cid not in cada_ids:
                warnings.append(f"trace row {i}: CADA_ID {cid} not found in 11_CADA_Control")

    # Independently reconcile confirmed TRACE events with machine-created receipts.
    # Legacy records remain visible but cannot be silently promoted to proof.
    from trace_execution import audit_receipts
    receipt_audit = audit_receipts(root, strict=cfg_data.get("trace_receipts_required") is True)
    errors.extend(receipt_audit["errors"])
    warnings.extend(receipt_audit["warnings"])
    if receipt_audit["counts"]["unverified"]:
        warnings.append(
            f'TRACE contains {receipt_audit["counts"]["unverified"]} unverified event(s); '
            'do not report these as confirmed executions'
        )

    ai=root/"00_Gestao_e_Continuidade/14_AI_Use_Log.csv"
    ai_ids=set()
    if ai.exists():
        for i,r in enumerate(rows(ai),2):
            aid=(r.get("AI_Use_ID") or "").strip()
            if not aid:
                continue
            if aid in ai_ids:
                errors.append(f"AI-use row {i}: duplicate AI_Use_ID {aid}")
            ai_ids.add(aid)
            if not aid.startswith("AIUSE-"):
                warnings.append(f"AI-use row {i}: nonstandard AI_Use_ID {aid!r}")
            materiality=(r.get("Materiality") or "").strip().upper()
            if materiality and materiality not in AI_MATERIALITY:
                warnings.append(f"AI-use row {i}: unexpected Materiality {materiality!r}")
            decision=(r.get("Accepted_modified_or_rejected") or "").strip().upper()
            if decision not in AI_DECISION:
                warnings.append(f"AI-use row {i}: unexpected decision {decision!r}")
            trace_id=(r.get("Trace_ID") or "").strip()
            if trace_id and trace_ids and trace_id not in trace_ids:
                warnings.append(f"AI-use row {i}: Trace_ID {trace_id} not found in 13_Traceability_Log")
            review=(r.get("Human_review_method") or "").strip()
            if materiality=="SUBSTANTIVE" and not review:
                errors.append(f"AI-use row {i}: substantive AI use {aid} lacks Human_review_method")
            if materiality=="SUBSTANTIVE" and decision in {"","PENDING"}:
                warnings.append(f"AI-use row {i}: substantive AI use {aid} has no final human decision")

    claims_path=root/"00_Gestao_e_Continuidade/09_Claims_Ledger.csv"
    claim_rows=[]
    if claims_path.exists():
        for i,r in enumerate(rows(claims_path),2):
            claim_rows.append(r)
            cid=(r.get("Claim_ID") or "").strip()
            if not cid:
                continue
            robustness=(r.get("Robustness_status") or "").upper().strip()
            human=(r.get("Human_validation") or "").upper().strip()
            draft=(r.get("Draft_status") or "").upper().strip()
            if robustness not in CLAIM_ROBUSTNESS:
                errors.append(f"claim row {i}: {cid} has invalid Robustness_status={robustness!r}")
            if human not in HUMAN_VALIDATION:
                errors.append(f"claim row {i}: {cid} has invalid Human_validation={human!r}")
            if draft in {"VERIFIED","FROZEN","FINAL","READY"} and robustness in {"","NOT_AUDITED","REVISE","REJECT"}:
                errors.append(f"claim row {i}: {cid} is {draft} but robustness status is {robustness or 'empty'}")
            if robustness in {"ROBUST","QUALIFIED"} and human in {"","PENDING"}:
                warnings.append(f"claim row {i}: {cid} is {robustness} but human validation is pending")
            if robustness=="QUALIFIED" and not (r.get("Boundary_conditions") or "").strip() and not (r.get("Robustness_notes") or "").strip():
                warnings.append(f"claim row {i}: {cid} is QUALIFIED without an explicit boundary/robustness note")

    # Provenance integrity and bounded originality are required at final claim freeze.
    if cfg_data.get("claim_integrity_required") is True:
        source_claims=root/"00_Gestao_e_Continuidade/09_Claims_Ledger.csv"
        with source_claims.open("r",encoding="utf-8-sig",newline="") as f:
            claim_headers=csv.DictReader(f).fieldnames or []
        evidence_rows=list(rows(root/"00_Gestao_e_Continuidade/05_Evidence_Matrix.csv"))
        search_rows=list(rows(root/"00_Gestao_e_Continuidade/02_Search_Log.csv"))
        gate_file=root/"00_Gestao_e_Continuidade/18_Human_Validation_Gates.csv"
        g6_final=gate_file.exists() and any(
            (g.get("GATE_ID") or "").strip()=="GATE-0006"
            and (g.get("Status") or "").upper()=="COMPLETED"
            and (g.get("Decision") or "").upper() in {"APPROVED","APPROVED_WITH_CHANGES"}
            for g in rows(gate_file)
        )
        claim_audit=audit_claim_integrity(
            claim_rows,evidence_rows,search_rows,strict=True,
            freeze=g6_final,headers=claim_headers)
        errors.extend("claim integrity: "+p for p in claim_audit["errors"])
        warnings.extend("claim integrity: "+p for p in claim_audit["warnings"])

    dashboard=root/"00_Gestao_e_Continuidade/15_CADA_Dashboard.csv"
    if dashboard.exists():
        metrics={(r.get("Metric") or "").strip():(r.get("Value") or "").strip() for r in rows(dashboard)}
        for metric in ["Management_mode","Current_scientific_stage","Next_CADA_ID","Next_action","Traceability_gaps"]:
            if metric not in metrics:
                warnings.append(f"CADA dashboard lacks metric {metric!r}")

    rast=root/"00_Gestao_e_Continuidade/RASTREABILIDADE.md"
    if rast.exists():
        rs=rast.read_text(encoding="utf-8",errors="replace")
        for heading in ["## Process provenance","## AI use","## Human validation checkpoints","## Provenance gaps"]:
            if heading not in rs:
                warnings.append(f"RASTREABILIDADE.md lacks {heading!r}")

    interop=root/"00_Gestao_e_Continuidade/16_Interoperabilidade.csv"
    if interop.exists():
        export_ids=set()
        for i,r in enumerate(rows(interop),2):
            eid=(r.get("Export_ID") or "").strip()
            if not eid:
                continue
            if eid in export_ids:
                errors.append(f"interoperability row {i}: duplicate Export_ID {eid}")
            export_ids.add(eid)
            if not eid.startswith("EXPORT-"):
                warnings.append(f"interoperability row {i}: nonstandard Export_ID {eid!r}")
            if (r.get("Validation_status") or "").upper().startswith("INVALID"):
                warnings.append(f"interoperability row {i}: provenance package {eid} is INVALID")

    decisions=root/"00_Gestao_e_Continuidade/17_Decision_Log.csv"
    if decisions.exists():
        seen=set()
        for i,r in enumerate(rows(decisions),2):
            did=(r.get("DEC_ID") or "").strip()
            if not did: continue
            if did in seen: errors.append(f"decision row {i}: duplicate DEC_ID {did}")
            seen.add(did)
            if not did.startswith("DEC-"): warnings.append(f"decision row {i}: nonstandard DEC_ID {did!r}")
            status=(r.get("Status") or "").upper()
            if status in {"APPROVED","FROZEN"} and not (r.get("Rationale") or "").strip():
                errors.append(f"decision row {i}: {did} is {status} without rationale")

    gates=root/"00_Gestao_e_Continuidade/18_Human_Validation_Gates.csv"
    if gates.exists():
        seen=set()
        for i,r in enumerate(rows(gates),2):
            gid=(r.get("GATE_ID") or "").strip()
            if not gid: continue
            if gid in seen: errors.append(f"gate row {i}: duplicate GATE_ID {gid}")
            seen.add(gid)
            if not gid.startswith("GATE-"): warnings.append(f"gate row {i}: nonstandard GATE_ID {gid!r}")
            status=(r.get("Status") or "").upper()
            decision=(r.get("Decision") or "").upper()
            if status=="COMPLETED" and decision not in {"APPROVED","APPROVED_WITH_CHANGES","REJECTED"}:
                errors.append(f"gate row {i}: completed {gid} lacks valid decision")
            if status=="COMPLETED" and not (r.get("Validated_by") or "").strip():
                errors.append(f"gate row {i}: completed {gid} lacks validator")
            if status=="COMPLETED" and not (r.get("Validation_method") or "").strip():
                errors.append(f"gate row {i}: completed {gid} lacks validation method")
            if cfg_data.get("formative_gates_required") is True and status=="COMPLETED":
                for issue in gate_issues(r):
                    errors.append(f"gate row {i}: {gid} {issue}")

    gate_state={}
    if gates.exists():
        for r in rows(gates):
            gid=(r.get("GATE_ID") or "").strip()
            if gid:
                gate_state[gid]=r

    g6=gate_state.get("GATE-0006",{})
    if (g6.get("Status") or "").upper()=="COMPLETED" and (g6.get("Decision") or "").upper() in {"APPROVED","APPROVED_WITH_CHANGES"}:
        for i,r in enumerate(claim_rows,2):
            cid=(r.get("Claim_ID") or "").strip()
            if not cid:
                continue
            robustness=(r.get("Robustness_status") or "").upper().strip()
            if robustness in {"","NOT_AUDITED","REVISE","REJECT"}:
                errors.append(f"GATE-0006 approved while claim {cid} remains {robustness or 'not audited'}")

    # Methodological suitability is separate from DOI identity and literal locators.
    # Require documented human appraisal only for the material evidence linked
    # to claims when GATE-0006 is approved; keep historic projects compatible.
    if ev.exists():
        evidence_items=list(rows(ev))
        quality_required=cfg_data.get("critical_appraisal_required") is True
        approved=(g6.get("Status") or "").upper()=="COMPLETED" and (g6.get("Decision") or "").upper() in {"APPROVED","APPROVED_WITH_CHANGES"}
        used=set()
        if approved and quality_required:
            import re
            for claim in claim_rows:
                if not (claim.get("Claim_ID") or "").strip():
                    continue
                for field in ("Evidence_IDs","Counter_Evidence_IDs"):
                    used.update(x for x in re.split(r"[;,\s]+",(claim.get(field) or "")) if x)
        with ev.open("r",encoding="utf-8-sig",newline="") as stream:
            ev_columns=csv.DictReader(stream).fieldnames or []
        appraisal=audit_appraisals(evidence_items,required_ids=used,
                                  enforce=approved and quality_required,headers=ev_columns)
        errors.extend("critical appraisal: "+x for x in appraisal["errors"])

    # Newly initialized projects require independently checkable source records.
    if (g6.get("Status") or "").upper()=="COMPLETED" and (g6.get("Decision") or "").upper() in {"APPROVED","APPROVED_WITH_CHANGES"} and cfg_data.get("source_verification_required") is True:
        report_path=root/"00_Gestao_e_Continuidade/SOURCE_VERIFICATION.json"
        evidence_file=root/"00_Gestao_e_Continuidade/05_Evidence_Matrix.csv"
        if not report_path.is_file():
            errors.append("GATE-0006 approved without source-verification report")
        else:
            try:
                source_report=json.loads(report_path.read_text(encoding="utf-8"))
                if source_report.get("schema_version")!=1:
                    errors.append("GATE-0006 source-verification report has unsupported schema")
                if source_report.get("input_sha256")!=hashlib.sha256(evidence_file.read_bytes()).hexdigest():
                    errors.append("GATE-0006 source-verification report is stale")
                entries=source_report.get("checks")
                if not isinstance(entries,list) or len(entries)!=sum(1 for _ in rows(evidence_file)):
                    errors.append("GATE-0006 source-verification report is incomplete")
                else:
                    if any(x.get("result")=="FAIL" for x in entries):
                        errors.append("GATE-0006 source-verification report contains conflicting source evidence")
                    if any(x.get("result")!="METADATA_AND_LOCATOR_CHECKED" for x in entries):
                        warnings.append("GATE-0006 unresolved source checks require documented human examination")
                    for x in entries:
                        rel=x.get("source_path")
                        sha=x.get("source_sha256")
                        if not rel or not sha:
                            continue
                        file_path=(root/rel).resolve()
                        if not file_path.is_relative_to(root) or not file_path.is_file():
                            errors.append("GATE-0006 verified source file is inaccessible or outside workspace")
                        elif hashlib.sha256(file_path.read_bytes()).hexdigest()!=sha:
                            errors.append("GATE-0006 verified source file changed after source check")
            except (OSError,ValueError,TypeError,KeyError) as exc:
                errors.append(f"GATE-0006 cannot validate source-verification report: {type(exc).__name__}")

    # Local PDF availability never implies export/redistribution permission.
    if cfg_data.get("fulltext_rights_audit_required") is True:
        try:
            rights_report=audit_fulltext_rights(root,strict=False)
            errors.extend("full-text rights: "+m for m in rights_report["errors"])
            warnings.extend("full-text rights: "+m for m in rights_report["warnings"])
        except (OSError,ValueError) as exc:
            errors.append(f"full-text rights audit could not run: {type(exc).__name__}")

    # Keep the editorial AI declaration tied to the actual log and policy.
    if cfg_data.get("editorial_ai_disclosure_required") is True:
        from editorial_ai_disclosure import assess,verify_final
        try:
            disclosure=assess(root)
            if disclosure["errors"]:
                warnings.extend("editorial AI disclosure: "+e for e in disclosure["errors"])
            gate7=gate_state.get("GATE-0007",{})
            if (gate7.get("Status") or "").upper()=="COMPLETED" and (
                gate7.get("Decision") or "").upper() in {"APPROVED","APPROVED_WITH_CHANGES"}:
                errors.extend("editorial AI disclosure: "+e for e in verify_final(root))
        except (ValueError,OSError) as exc:
            pending=gate_state.get("GATE-0007",{})
            final=(pending.get("Status") or "").upper()=="COMPLETED" and (
                pending.get("Decision") or "").upper() in {"APPROVED","APPROVED_WITH_CHANGES"}
            (errors if final else warnings).append(
                f"editorial AI disclosure unresolved: {type(exc).__name__}")

    g7=gate_state.get("GATE-0007",{})
    if (g7.get("Status") or "").upper()=="COMPLETED" and (g7.get("Decision") or "").upper() in {"APPROVED","APPROVED_WITH_CHANGES"}:
        target=str((journal_data or {}).get("journal_name") or cfg_data.get("target_journal") or "").strip()
        if target:
            if (journal_data or {}).get("status")!="VERIFIED" or (journal_data or {}).get("official_rules_verified") is not True:
                errors.append("GATE-0007 approved for a defined target journal without VERIFIED official journal rules")
        astatus=str((anonymization_data or {}).get("status") or "").upper()
        if astatus not in {"VERIFIED","NOT_REQUIRED"}:
            errors.append("GATE-0007 approved without VERIFIED anonymization profile or explicit NOT_REQUIRED rationale")
        if astatus=="VERIFIED":
            audit_dir=root/"06_Submissao/Anonimizacao"
            valid_results={"PASS","PASS_WITH_HUMAN_REVIEW"}
            valid_audits=[]
            for p in sorted(audit_dir.glob("ANONYMIZATION_AUDIT_*.json")) if audit_dir.exists() else []:
                try:
                    ad=json.loads(p.read_text(encoding="utf-8"))
                    if str(ad.get("result") or "").upper() not in valid_results:
                        continue
                    final_dir = root / "06_Submissao/Arquivos_Finais"
                    outgoing = {
                        f.relative_to(root).as_posix(): hashlib.sha256(f.read_bytes()).hexdigest()
                        for f in final_dir.rglob("*") if f.is_file()
                    }
                    manifest = ad.get("file_manifest") or []
                    audited = {item["path"]: item["sha256"] for item in manifest}
                    profile_hash = hashlib.sha256(anonymization_profile.read_bytes()).hexdigest()
                    if (outgoing and audited == outgoing and len(manifest) == len(outgoing)
                            and ad.get("profile_sha256") == profile_hash
                            and not ad.get("blocking_errors")):
                        valid_audits.append(p)
                except Exception:
                    continue
            if not valid_audits:
                errors.append("GATE-0007 approved without a passing ANONYMIZATION_AUDIT bound to the current outgoing files and profile")

    snaps=root/"00_Gestao_e_Continuidade/19_Snapshots.csv"
    if snaps.exists():
        seen=set()
        for i,r in enumerate(rows(snaps),2):
            sid=(r.get("SNAP_ID") or "").strip()
            if not sid: continue
            if sid in seen: errors.append(f"snapshot row {i}: duplicate SNAP_ID {sid}")
            seen.add(sid)
            if not sid.startswith("SNAP-"): warnings.append(f"snapshot row {i}: nonstandard SNAP_ID {sid!r}")
            if (r.get("Validation_status") or "").upper()=="VALID" and not (r.get("Manifest_SHA256") or "").strip():
                warnings.append(f"snapshot row {i}: VALID {sid} lacks manifest SHA-256")

    matrix_files=list((root/"00_Gestao_e_Continuidade").glob("MATRIZ_MESTRA_*.xlsx"))
    if not matrix_files:
        warnings.append("visual MATRIZ_MESTRA_*.xlsx not found; project is using compatibility tables only")

    cont=root/"00_Gestao_e_Continuidade/CONTINUIDADE.md"
    if cont.exists():
        s=cont.read_text(encoding="utf-8",errors="replace")
        for heading in [
            "## 14. Next valid action",
            "## 15. Change log",
            "## 16. C.A.D.A. dashboard",
            "## 3. Tool and plugin status",
        ]:
            if heading not in s:
                warnings.append(f"CONTINUIDADE.md lacks {heading!r}")

    # Distinguish administrative task completion from science-method quality.
    if cfg_data.get("cada_science_boundary_required") is True:
        boundary=audit_cada_boundary(root,strict=True)
        errors.extend("management/science boundary: "+item for item in boundary["integrity"]["errors"])
        warnings.extend("management/science boundary: "+item for item in boundary["integrity"]["warnings"])

    for w in warnings: print("WARNING:",w)
    for e in errors: print("ERROR:",e)
    print(f"validation_errors={len(errors)}")
    print(f"validation_warnings={len(warnings)}")
    return 1 if errors else 0

if __name__=="__main__":
    raise SystemExit(main())
