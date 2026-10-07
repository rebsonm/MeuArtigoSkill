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

ROOT=Path(__file__).resolve().parents[2]

REQUIRED=[
    "VERSION",
    "CHANGELOG.md",
    "CITATION.cff",
    ".github/workflows/release-audit.yml",
    "README.md",
    "docs/COMECE-AQUI.md",
    "docs/MATRIZ-CADA.md",
    "docs/RASTREABILIDADE.md",
    "docs/GOVERNANCA-CIENTIFICA.md",
    "docs/INTEROPERABILIDADE.md",
    "docs/MAPA-CORPUS.md",
    "docs/JOURNAL-AWARE.md",
    "docs/ROBUSTEZ-CLAIMS.md",
    "meu-artigo/SKILL.md",
    "meu-artigo/references/corpus-map.md",
    "meu-artigo/references/grounded-corpus.md",
    "meu-artigo/references/journal-aware.md",
    "meu-artigo/references/scientific-governance.md",
    "meu-artigo/references/provenance-export.md",
    "meu-artigo/scripts/build_matrix_template.py",
    "meu-artigo/scripts/build_corpus_map.py",
    "meu-artigo/scripts/governance_events.py",
    "meu-artigo/scripts/create_snapshot.py",
    "meu-artigo/scripts/compare_snapshots.py",
    "meu-artigo/scripts/generate_transparency_report.py",
    "meu-artigo/scripts/export_provenance.py",
    "meu-artigo/scripts/validate_provenance_package.py",
    "meu-artigo/scripts/validate_project.py",
]

def main()->int:
    errors=[]
    warnings=[]

    for rel in REQUIRED:
        if not (ROOT/rel).exists():
            errors.append(f"missing required file: {rel}")

    version=(ROOT/"VERSION").read_text(encoding="utf-8").strip() if (ROOT/"VERSION").exists() else ""
    citation=(ROOT/"CITATION.cff").read_text(encoding="utf-8") if (ROOT/"CITATION.cff").exists() else ""
    changelog=(ROOT/"CHANGELOG.md").read_text(encoding="utf-8") if (ROOT/"CHANGELOG.md").exists() else ""
    readme=(ROOT/"README.md").read_text(encoding="utf-8") if (ROOT/"README.md").exists() else ""
    skill=(ROOT/"meu-artigo/SKILL.md").read_text(encoding="utf-8") if (ROOT/"meu-artigo/SKILL.md").exists() else ""

    if version:
        if f'version: "{version}"' not in citation and f"version: {version}" not in citation:
            errors.append("CITATION.cff version does not match VERSION")
        if version not in changelog:
            errors.append("CHANGELOG.md does not contain current VERSION")
    else:
        errors.append("VERSION is empty")

    # Python syntax audit without importing optional dependencies.
    for p in sorted((ROOT/"meu-artigo/scripts").glob("*.py")):
        try:
            ast.parse(p.read_text(encoding="utf-8"),filename=str(p))
        except SyntaxError as exc:
            errors.append(f"syntax error in {p.relative_to(ROOT)}: {exc}")

    # Core feature references.
    required_terms={
        "SKILL.md":["DEC_ID","GATE_ID","SNAP_ID","W3C PROV","RO-Crate","Grounded Corpus","Corpus Map","JOURNAL_PROFILE","JOURNAL_NEUTRAL","Counter_Evidence_IDs","Robustness_status"],
        "README.md":["DEC_ID","GATE_ID","SNAP_ID","RO-Crate","Mapa do Corpus","JOURNAL_PROFILE","robustez dos claims"],
    }
    for label,terms in required_terms.items():
        text=skill if label=="SKILL.md" else readme
        for term in terms:
            if term.lower() not in text.lower():
                warnings.append(f"{label} does not mention expected term: {term}")

    # Ensure the canonical workbook generator exposes all currently defined views.
    matrix=(ROOT/"meu-artigo/scripts/build_matrix_template.py").read_text(encoding="utf-8") if (ROOT/"meu-artigo/scripts/build_matrix_template.py").exists() else ""
    for sheet in ["16_INTEROPERABILIDADE","17_DECISOES","18_VALIDACOES","19_SNAPSHOTS","20_MAPA_CORPUS"]:
        if sheet not in matrix:
            errors.append(f"workbook generator missing sheet: {sheet}")
    for term in ["Counter_Evidence_IDs","Explicações alternativas","Dependência de fonte única","Robustez","Revista-alvo","Modo de construção editorial"]:
        if term not in matrix:
            errors.append(f"workbook generator missing journal/robustness field: {term}")

    init_script=(ROOT/"meu-artigo/scripts/init_project.py").read_text(encoding="utf-8") if (ROOT/"meu-artigo/scripts/init_project.py").exists() else ""
    for term in ["JOURNAL_PROFILE.json","JOURNAL_NEUTRAL","claim_robustness_audit_enabled","Counter_Evidence_IDs"]:
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
