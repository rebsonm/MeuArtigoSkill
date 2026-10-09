#!/usr/bin/env python3
"""Static release audit for MeuArtigoSkill.

This audit intentionally does not require artifact_tool, network access, or a
fictitious project. It checks repository structure, Python syntax, version
consistency, key documentation references, and absence of placeholder demo
content in the canonical distribution.
"""
from __future__ import annotations

import ast
import re
from pathlib import Path
from version_info import read_version, release_notes_path

ROOT=Path(__file__).resolve().parents[1]

REQUIRED=[
    "VERSION",
    "LICENSE",
    "NOTICE",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "docs/IMPLANTACAO-BETA.md",
    "docs/CHECKLIST-PRIMEIRO-USO.md",
    "docs/PROTOCOLO-BETA-USUARIOS.md",
    "docs/VALIDACOES-PENDENTES.md",
    "docs/NOTAS-DA-VERSAO-0.8.0-beta.1.md",
    "docs/NOTAS-DA-VERSAO-0.8.0-beta.2.md",
    "docs/NOTAS-DA-VERSAO-0.8.0-beta.3.md",
    "docs/NOTAS-DA-VERSAO-0.8.0-beta.6.md",
    "docs/NOTAS-DA-VERSAO-0.8.0-beta.7.md",
    "docs/MODO-NUCLEO-MINIMO.md",
    "docs/REPRODUCAO-REVISAO-INTEGRATIVA.md",
    "references/methodological-foundations.md",
    "references/language-policy.md",
    "scripts/language_config.py",
    "scripts/audit_source_language.py",
    "tests/test_language_policy.py",
    "docs/ENGLISH-SOURCE-MIGRATION.md",
    "references/INDICE-METODOLOGICO.md",
    "references/CONTEXTO-POR-ETAPA.md",
    "references/fluxo-essencial.md",
    "references/platform-capability-preflight.md",
    "tests/test_stage4_routing.py",
    "scripts/presentation_mode.py",
    "tests/test_a2_controls.py",
    "benchmarks/minimal_full_comparison_protocol_v1.json",
    "benchmarks/integrative_replication_protocol_v1.json",
    "docs/COMPATIBILIDADE-PLATAFORMAS.md",
    "scripts/check_documentation_links.py",
    "tests/test_documentation_links.py",
    "tests/test_public_communication.py",
    "scripts/build_skill_bundle.py",
    "tests/test_bundle_release.py",
    "tests/test_external_export_privacy.py",
    "docs/EXPORTACAO-SEGURA.md",
    "CHANGELOG.md",
    "CITATION.cff",
    ".github/workflows/release-audit.yml",
    ".github/workflows/publish-beta.yml",
    "scripts/version_info.py",
    "scripts/audit_public_docs.py",
    "tests/test_version_info.py",
    "scripts/sync_version.py",
    "tests/test_sync_version.py",
    "tests/test_ci_workflows.py",
    "docs/GUIA-DE-RELEASES.md",
    "tests/test_public_documentation_audit.py",
    "README.md",
    "docs/COMECE-AQUI.md",
    "docs/MATRIZ-CADA.md",
    "docs/RASTREABILIDADE.md",
    "docs/GOVERNANCA-CIENTIFICA.md",
    "docs/INTEROPERABILIDADE.md",
    "docs/MAPA-CORPUS.md",
    "docs/JOURNAL-AWARE.md",
    "docs/ROBUSTEZ-CLAIMS.md",
    "docs/ANONIMIZACAO.md",
    "SKILL.md",
    "references/corpus-map.md",
    "references/grounded-corpus.md",
    "references/journal-aware.md",
    "references/scientific-governance.md",
    "references/provenance-export.md",
    "references/anonymization.md",
    "scripts/build_matrix_template.py",
    "scripts/build_corpus_map.py",
    "scripts/governance_events.py",
    "scripts/formative_gates.py",
    "docs/VALIDACAO-FORMATIVA.md",
    "scripts/create_snapshot.py",
    "scripts/compare_snapshots.py",
    "scripts/generate_transparency_report.py",
    "scripts/export_provenance.py",
    "scripts/validate_provenance_package.py",
    "scripts/validate_project.py",
    "scripts/method_routes.py",
    "scripts/choose_method_route.py",
    "scripts/scientific_evidence_tiers.py",
    "docs/NIVEIS-DE-EVIDENCIA.md",
    "tests/test_scientific_evidence_tiers.py",
    "tests/test_method_routes.py",
    "docs/ROTAS-METODOLOGICAS.md",
    "scripts/verify_sources.py",
    "scripts/appraise_evidence.py",
    "docs/AVALIACAO-CRITICA-FONTES.md",
    "scripts/trace_execution.py",
    "scripts/screening_review.py",
    "docs/SCREENING-AUDITAVEL.md",
    "scripts/editorial_ai_disclosure.py",
    "docs/DECLARACAO-EDITORIAL-IA.md",
    "scripts/rights_audit.py",
    "docs/DIREITOS-FULLTEXT-E-PDFS.md",
    "scripts/audit_governance_boundary.py",
    "benchmarks/cada_comparison_protocol_v1.json",
    "docs/LIMITES-CADA-E-COMPARACAO.md",
    "scripts/claim_integrity.py",
    "docs/CONTROLE-CLAIMS-E-ORIGINALIDADE.md",
    "scripts/quality_benchmark.py",
    "benchmarks/public_review_reference_v1.json",
    "docs/AVALIACAO-QUALIDADE-CIENTIFICA.md",
    ".github/workflows/scientific-quality-calibration.yml",
    "docs/COMPROVACAO-EVENTOS.md",
    "references/source-verification.md",
    "docs/VERIFICACAO-FONTES.md",
    "scripts/audit_anonymization.py",
    "scripts/sanitize_metadata.py",
]

def main()->int:
    errors=[]
    warnings=[]

    for rel in REQUIRED:
        if not (ROOT/rel).exists():
            errors.append(f"missing required file: {rel}")

    try:
        version=read_version(ROOT)
    except ValueError as exc:
        version=""
        errors.append(str(exc))
    if version and not release_notes_path(ROOT).is_file():
        errors.append(f"missing current release notes: {release_notes_path(ROOT).relative_to(ROOT)}")
    citation=(ROOT/"CITATION.cff").read_text(encoding="utf-8") if (ROOT/"CITATION.cff").exists() else ""
    changelog=(ROOT/"CHANGELOG.md").read_text(encoding="utf-8") if (ROOT/"CHANGELOG.md").exists() else ""
    readme=(ROOT/"README.md").read_text(encoding="utf-8") if (ROOT/"README.md").exists() else ""
    skill=(ROOT/"SKILL.md").read_text(encoding="utf-8") if (ROOT/"SKILL.md").exists() else ""

    if version:
        if f'version: "{version}"' not in citation and f"version: {version}" not in citation:
            errors.append("CITATION.cff version does not match VERSION")
        if not re.search(r"(?m)^## "+re.escape(version)+r"\s+[—-]", changelog):
            errors.append("CHANGELOG.md lacks a headed section for current VERSION")
    else:
        errors.append("VERSION is empty")

    # Public beta release consistency. The code is Apache-2.0, but third-party
    # article PDFs are NOT relicensed or distributable as software.
    license_text=(ROOT/"LICENSE").read_text(encoding="utf-8") if (ROOT/"LICENSE").exists() else ""
    onboarding=(ROOT/"docs/COMECE-AQUI.md").read_text(encoding="utf-8") if (ROOT/"docs/COMECE-AQUI.md").exists() else ""
    workflow=(ROOT/".github/workflows/release-audit.yml").read_text(encoding="utf-8") if (ROOT/".github/workflows/release-audit.yml").exists() else ""
    if not license_text.lstrip().startswith("Apache License") or "END OF TERMS AND CONDITIONS" not in license_text:
        errors.append("Repository source license must contain Apache License 2.0 terms")
    if 'license: "Apache-2.0"' not in citation and "license: Apache-2.0" not in citation:
        errors.append("CITATION.cff must identify Apache-2.0")
    if "Rebson de Morais Mendes" not in (ROOT/"NOTICE").read_text(encoding="utf-8"):
        errors.append("NOTICE must preserve original author attribution")
    if f"**Current version:** `{version}`" not in readme:
        errors.append("README does not display current VERSION")
    if "Enquanto o acesso não for aberto pelo autor" in onboarding:
        errors.append("Onboarding still falsely describes public repository as restricted")
    if "beta pública" not in onboarding.lower():
        errors.append("Public-beta access is not described in onboarding")
    publisher=(ROOT/".github/workflows/publish-beta.yml").read_text(encoding="utf-8") if (ROOT/".github/workflows/publish-beta.yml").exists() else ""
    if not all(name in workflow for name in [
        "pull_request:", "push:", "branches: [main]", "audit:",
        "build_skill_bundle.py", "check_documentation_links.py",
        "audit_public_docs.py", "contents: read"
    ]):
        errors.append("CI workflow lacks mandatory checks and read-only permission")
    if "gh release create" in workflow or "contents: write" in workflow:
        errors.append("CI audit workflow must not publish releases or grant write privileges")
    if not all(name in publisher for name in [
        "workflow_dispatch:", "refs/heads/main", "contents: write",
        "gh release create", "--prerelease", "VERSION", "SHA256SUMS.txt",
        "NOTAS-DA-VERSAO-", "build_skill_bundle.py"
    ]):
        errors.append("Manual beta release workflow is incomplete")
    if re.search(r"0\\.8\\.0-beta\\.\\d+", publisher + workflow):
        errors.append("Workflows must derive version dynamically from VERSION")
    if "PENDENTE" not in (ROOT/"docs/VALIDACOES-PENDENTES.md").read_text(encoding="utf-8"):
        errors.append("Pending empirical validations must remain explicitly documented")

    # Avoid internal implementation notes in the public landing page.
    for exposed in [r"\bRT-\d{2}\b", r"\bGATE-\d{4}\b", r"\bDEC_ID\b",
                    r"\bSNAP_ID\b", r"\bscripts/[A-Za-z0-9_]+\.py\b",
                    r"\bCADA-\d{4}\b", r"\bGATE_ID\b", r"\bTRACE_ID\b"]:
        if re.search(exposed, readme, flags=re.IGNORECASE):
            errors.append(f"README contains an internal control reference: {exposed}")

    # Python syntax audit without importing optional dependencies.
    for p in sorted((ROOT/"scripts").glob("*.py")):
        try:
            ast.parse(p.read_text(encoding="utf-8"),filename=str(p))
        except SyntaxError as exc:
            errors.append(f"syntax error in {p.relative_to(ROOT)}: {exc}")

    # Core feature references.
    required_terms={
        "SKILL.md":["DEC_ID","GATE_ID","SNAP_ID","W3C PROV","RO-Crate","Grounded Corpus","Corpus Map","JOURNAL_PROFILE","JOURNAL_NEUTRAL","Counter_Evidence_IDs","Robustness_status","ANONYMIZATION_PROFILE","audit_anonymization.py","sanitize_metadata.py","ZERO_NONESSENTIAL_METADATA","GOOGLE_DRIVE_FIRST","WORK_FALLBACK"],
        "README.md":["Meu Artigo","C.A.D.A.","Getting started","researcher","sources","beta"],
    }
    for label,terms in required_terms.items():
        text=skill if label=="SKILL.md" else readme
        for term in terms:
            if term.lower() not in text.lower():
                warnings.append(f"{label} does not mention expected term: {term}")

    # Ensure the canonical workbook generator exposes all currently defined views.
    matrix=(ROOT/"scripts/build_matrix_template.py").read_text(encoding="utf-8") if (ROOT/"scripts/build_matrix_template.py").exists() else ""
    for sheet in ["16_INTEROPERABILIDADE","17_DECISOES","18_VALIDACOES","19_SNAPSHOTS","20_MAPA_CORPUS"]:
        if sheet not in matrix:
            errors.append(f"workbook generator missing sheet: {sheet}")
    for term in ["Counter_Evidence_IDs","Explicações alternativas","Dependência de fonte única","Robustez","Revista-alvo","Modo de construção editorial","Anonimização: auditoria final","Modo padrão de arquivo externo","Papel na literatura","Base da classificação","Fonte primária","Linhagem conceitual / relação","FOUNDATIONAL","CLASSIC_CRITIQUE","CONTEMPORARY_UPDATE"]:
        if term not in matrix:
            errors.append(f"workbook generator missing journal/robustness field: {term}")

    init_script=(ROOT/"scripts/init_project.py").read_text(encoding="utf-8") if (ROOT/"scripts/init_project.py").exists() else ""
    for term in ["JOURNAL_PROFILE.json","JOURNAL_NEUTRAL","claim_robustness_audit_enabled","Counter_Evidence_IDs","ANONYMIZATION_PROFILE.json","anonymization_policy_enabled","ZERO_NONESSENTIAL_METADATA","GOOGLE_DRIVE_FIRST","fallback_authorized","WORK_FALLBACK"]:
        if term not in init_script:
            errors.append(f"project initializer missing journal/robustness capability: {term}")

    # Do not ship a fake project/corpus as part of the canonical repository.
    forbidden_paths=[]
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        rel=p.relative_to(ROOT).as_posix().lower()
        if any(tok in rel for tok in ["demo_project","projeto_demo","fictitious_project","synthetic_corpus"]):
            forbidden_paths.append(rel)
    for rel in forbidden_paths:
        errors.append(f"unexpected demo/fictitious artifact in canonical repository: {rel}")

    print(f"version={version}")
    print(f"errors={len(errors)}")
    print(f"warnings={len(warnings)}")
    for e in errors:
        print("ERROR:",e)
    for w in warnings:
        print("WARNING:",w)
    return 1 if errors else 0

if __name__=="__main__":
    raise SystemExit(main())
