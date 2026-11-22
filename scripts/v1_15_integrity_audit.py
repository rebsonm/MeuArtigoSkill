#!/usr/bin/env python3
"""V1-15: auditoria SOMENTE LEITURA de hashes, duplicatas e aliases.
Uso: python scripts/v1_15_integrity_audit.py --repo . --output /tmp/v1-15-audit.json
Antes, obtenha no clone local as refs work/ib-01-20261121 ... work/ib-20-20261121.
O script NUNCA lê PDFs privados, altera o repositório, resolve direitos ou certifica ciência.
O JSON de saída NÃO inclui nomes de pastas; nenhuma relação Unicode autoriza fusão de caminhos.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

REPO = "rebsonm/MeuArtigoSkill"
PLAN_SHA = "7c92045310eb3b1474a9612a777fb0012a511592"
READ_SHA = "c5e0ca9abd98f824f1576c3ad94c6e9a5d18e9bf"
ROOT = "knowledge/methodology"
HEX64 = re.compile(r"^[a-f0-9]{64}$")
HASH_FIELDS = (
    "novo_hash_sha256_da_ficha", "novo_hash_da_ficha",
    "sha256_da_ficha", "card_sha256",
)


def unicode_relation(ledger_value: str, alias_value: str) -> str:
    """Triagem de Unicode; nunca transforma isto em identidade de pastas."""
    if ledger_value == alias_value:
        return "EXACT_STRING"
    if unicodedata.normalize("NFC", ledger_value) == unicodedata.normalize("NFC", alias_value):
        return "CANONICAL_UNICODE_EQUIVALENT_NOT_PHYSICAL_PATH_PROOF"
    if unicodedata.normalize("NFKC", ledger_value) == unicodedata.normalize("NFKC", alias_value):
        return "COMPATIBILITY_UNICODE_EQUIVALENT_NOT_PHYSICAL_PATH_PROOF"
    return "DIFFERENT_STRING_NO_AUTO_EQUIVALENCE"


def git_bytes(repo: Path, ref: str, path: str) -> bytes:
    p = subprocess.run(
        ["git", "-C", str(repo), "show", f"{ref}:{path}"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if p.returncode:
        raise RuntimeError(f"Não foi possível ler {ref}:{path}; confirme a ref e a permissão")
    return p.stdout


def git_json(repo: Path, ref: str, path: str) -> dict:
    return json.loads(git_bytes(repo, ref, path).decode("utf-8"))


def card_hash(repo: Path, ref: str, path: str) -> str:
    return hashlib.sha256(git_bytes(repo, ref, path)).hexdigest()


def delta_records(delta: dict) -> list:
    matches = [(k, delta[k]) for k in ("records", "files", "documents", "source_records")
               if isinstance(delta.get(k), list)]
    if len(matches) != 1:
        raise ValueError("Delta deve conter exatamente uma lista de registros entre records/files/documents/source_records")
    return matches[0][1]


def summarize(repo: Path) -> dict:
    manifest = git_json(repo, PLAN_SHA, f"{ROOT}/intake/v1_parallel/V1-WORKPACKAGES-MANIFEST.json")
    ticket = next(t for t in manifest["tasks"] if t["batch_id"] == "V1-15/20")
    if ticket["dependencies"] or ticket["write_scope"].find("V1-15") < 0:
        raise RuntimeError("Escopo/dependências da V1-15 inesperados")
    src = git_json(repo, READ_SHA, f"{ROOT}/source_registry_catalog.json")["documents"]
    editorial = git_json(repo, READ_SHA, f"{ROOT}/catalog.json")["documents"]
    ledger = []
    for part in range(1, 6):
        name = f"{ROOT}/intake/rights-ledger-part-{part:02d}.json"
        ledger.extend(git_json(repo, READ_SHA, name)["records"])
    registry = {r["source_id"]: r for r in src}
    ledger_by_id = {r["id"]: r for r in ledger}
    if len(registry) != 475 or len(ledger_by_id) != 475 or len(editorial) != 174:
        raise RuntimeError("Contadores congelados não coincidem com o manifesto")
    planned = {r["source_id"] for r in src if r["bibliography_match_status"] != "SOURCE_PDF_WORK_VERIFIED"}
    source_mismatches, source_missing_hash, aliases, mapping_errors = [], [], [], []
    observed = []
    for i in range(1, 21):
        batch = f"{i:02d}"
        branch = f"work/ib-{batch}-20261121"
        path = f"{ROOT}/intake/parallel/IB-{batch}-DELTA.json"
        delta = git_json(repo, branch, path)
        for entry in delta_records(delta):
            sid = entry.get("source_id")
            if not sid or sid not in registry or sid not in ledger_by_id:
                mapping_errors.append({"batch": batch, "source_id": sid, "type": "ID_INEXISTENTE"})
                continue
            observed.append(sid)
            original = ledger_by_id[sid]
            folder = entry.get("folder_do_ledger") or entry.get("folder")
            filename = entry.get("filename_esperado") or entry.get("filename")
            size = entry.get("size_bytes_esperados", entry.get("size_bytes"))
            if filename is not None and filename != original["filename"]:
                mapping_errors.append({"batch": batch, "source_id": sid, "type": "FILENAME"})
            if size is not None and int(size) != int(original["size_bytes"]):
                mapping_errors.append({"batch": batch, "source_id": sid, "type": "SIZE_BYTES"})
            if folder is not None and folder != original["folder"]:
                aliases.append({
                    "batch": batch, "source_id": sid,
                    "unicode_relation": unicode_relation(original["folder"], folder),
                    "status": "ALIAS_CANDIDATE_NOT_DRIVE_VALIDATED",
                    # Não imprimir nomes físicos nem URLs privados no JSON de auditoria.
                })
            expected = next((entry[k] for k in HASH_FIELDS if entry.get(k)), None)
            path_card = f"{ROOT}/source_cards/{sid.lower()}.md"
            if not expected or not HEX64.fullmatch(str(expected)):
                source_missing_hash.append({"batch": batch, "source_id": sid, "reason": "NO_VALID_SHA256"})
                continue
            try:
                actual = card_hash(repo, branch, path_card)
                if actual != expected:
                    source_mismatches.append({
                        "batch": batch, "source_id": sid, "path": path_card,
                        "expected_sha256": expected, "actual_sha256": actual,
                    })
            except RuntimeError:
                source_missing_hash.append({"batch": batch, "source_id": sid, "reason": "CARD_UNREADABLE"})
    dup = [sid for sid, count in Counter(observed).items() if count > 1]
    missing_ids = sorted(planned - set(observed))
    unexpected_ids = sorted(set(observed) - planned)
    editorial_mismatches, editorial_missing_hash = [], []
    statuses = Counter()
    seen_paths = set()
    for card in editorial:
        path = card["path"]
        statuses[card.get("editorial_status") or "NO_EXPLICIT_STATUS"] += 1
        if path in seen_paths:
            editorial_missing_hash.append({"path": path, "reason": "DUPLICATE_PATH"})
            continue
        seen_paths.add(path)
        expected = card.get("sha256")
        if not expected or not HEX64.fullmatch(str(expected)):
            editorial_missing_hash.append({"path": path, "reason": "NO_VALID_SHA256"})
            continue
        try:
            actual = card_hash(repo, READ_SHA, path)
            if actual != expected:
                editorial_mismatches.append({
                    "path": path, "expected_sha256": expected, "actual_sha256": actual,
                })
        except RuntimeError:
            editorial_missing_hash.append({"path": path, "reason": "CARD_UNREADABLE"})
    by_size = defaultdict(list)
    for entry in ledger:
        by_size[int(entry["size_bytes"])].append(entry["id"])
    duplicate_candidates = [
        {"size_bytes": size, "source_ids": sorted(ids),
         "status": "SAME_SIZE_ONLY_NOT_PDF_SHA256_PROOF"}
        for size, ids in sorted(by_size.items()) if len(ids) > 1
    ]
    rights = Counter(r.get("rights_review") or "UNSET" for r in src)
    issues = (source_mismatches + source_missing_hash + mapping_errors
              + editorial_mismatches + editorial_missing_hash)
    return {
        "stage": "V1-15/20", "status": "AUDITORIA_TECNICA_SEM_ACEITE_CIENTIFICO",
        "manifest_ref": PLAN_SHA, "snapshot_ref": READ_SHA,
        "source_records_total": len(src), "source_delta_expected": len(planned),
        "source_delta_observed": len(observed), "source_delta_unique": len(set(observed)),
        "source_delta_duplicate_ids": dup, "source_delta_missing_ids": missing_ids,
        "source_delta_unexpected_ids": unexpected_ids,
        "source_sha256_recomputed": len(observed) - len(source_missing_hash),
        "source_sha256_mismatch": source_mismatches,
        "source_sha256_unverifiable": source_missing_hash,
        "editorial_cards_total": len(editorial),
        "editorial_sha256_recomputed": len(editorial) - len(editorial_missing_hash),
        "editorial_sha256_mismatch": editorial_mismatches,
        "editorial_sha256_unverifiable": editorial_missing_hash,
        "editorial_status": dict(statuses),
        "folder_alias_candidates": aliases, "folder_alias_count": len(aliases),
        "filename_or_size_or_id_errors": mapping_errors,
        "duplicate_size_groups": duplicate_candidates,
        "duplicate_size_groups_count": len(duplicate_candidates),
        "rights_registry_status": dict(rights),
        "original_pdf_sha256_verified": 0,
        "independent_scientific_reviews_verified": 0,
        "global_file_modified": False,
        "technical_discrepancy_count": len(issues) + len(dup) + len(missing_ids) + len(unexpected_ids),
        "limitations": [
            "Apenas hashes de Markdown em refs Git; não hashes dos PDFs privados",
            "Tamanho igual não comprova cópia nem obra intelectual idêntica",
            "Aliases requerem cotejo autorizado no Drive privado",
            "Ausência de status editorial não equivale a aprovação",
            "Direitos de cada edição/cópia e revisão científica continuam independentes",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, help="JSON local sanitizado, fora dos catálogos")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        assert hashlib.sha256(b"abc").hexdigest() == (
            "ba7816bf8f01cfea414140de5dae2223"
            "b00361a396177a9cb410ff61f20015ad"
        )
        assert unicode_relation("á", "á") == "CANONICAL_UNICODE_EQUIVALENT_NOT_PHYSICAL_PATH_PROOF"
        assert unicode_relation("Ａ", "A") == "COMPATIBILITY_UNICODE_EQUIVALENT_NOT_PHYSICAL_PATH_PROOF"
        assert unicode_relation("TÃ­tulo", "Título") == "DIFFERENT_STRING_NO_AUTO_EQUIVALENCE"
        assert unicode_relation("caminho", "caminho") == "EXACT_STRING"
        print("SELF_TEST_OK: SHA-256 e relações Unicode, sem equivalência automática de pasta")
        return 0
    result = summarize(args.repo)
    encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded)
    return int(bool(result["technical_discrepancy_count"]))


if __name__ == "__main__":
    raise SystemExit(main())
