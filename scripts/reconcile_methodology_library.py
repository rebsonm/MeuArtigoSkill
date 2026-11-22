#!/usr/bin/env python3
"""Reconcile operational dispositions; never certify science or source rights.

Run on the isolated integration branch. Historical receipts are attributed,
not re-labelled as primary-source work performed in the current cycle.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
LIB = Path('knowledge/methodology')
OUT = LIB / 'intake/operational-validation.json'
STATUSES = {'VALIDADO_POR_IA_E_CODIGO', 'CORRIGIDO_E_REVALIDADO',
            'VALIDADO_COM_RESTRICOES', 'BLOQUEADO_POR_EVIDENCIA',
            'EXCLUIDO_COM_JUSTIFICATIVA'}
BLOCKED = {'BLOQUEADO_POR_EVIDENCIA', 'EXCLUIDO_COM_JUSTIFICATIVA'}


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def digest(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def rows(obj, keys):
    for key in keys:
        if isinstance(obj.get(key), list):
            return obj[key]
    raise ValueError('RECEIPT_RECORD_LIST_MISSING')


def write(path, obj):
    (ROOT / path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def reconcile():
    refs = read(LIB / 'intake/v1_parallel/INTEGRATION-REFS.json')
    source_receipts = {}
    for i in range(1, 21):
        path = LIB / f'intake/parallel/IB-{i:02d}-DELTA.json'
        for row in rows(read(path), ('records', 'files', 'documents', 'source_records')):
            sid = row['source_id']
            if sid in source_receipts:
                raise ValueError('DUPLICATE_IB_SOURCE')
            source_receipts[sid] = (str(path), row)
    if len(source_receipts) != 343:
        raise ValueError('EXPECTED_343_IB_RECEIPTS')
    residuals = {}
    editorial = {}
    for i in range(1, 14):
        path = LIB / f'intake/v1_parallel/V1-{i:02d}-DELTA.json'
        obj = read(path)
        items = rows(obj, ('patch_intents', 'findings', 'items', 'cards', 'records', 'receipts', 'evidence'))
        for row in items:
            if i <= 3:
                residuals[row['source_id']] = (str(path), row)
            else:
                key = row.get('path') or row.get('card_path')
                if not key:
                    raise ValueError(f'EDITORIAL_PATH_MISSING_{i}')
                if key in editorial:
                    raise ValueError('DUPLICATE_EDITORIAL_RECEIPT')
                editorial[key] = (str(path), row)
    if len(residuals) != 15 or len(editorial) != 174:
        raise ValueError(f'INCOMPLETE_V1_RECEIPTS_{len(residuals)}_{len(editorial)}')
    independent_path = LIB / 'intake/independent-editorial-review.json'
    independent = read(independent_path)
    independent_rows = independent.get('cards', independent.get('records', []))
    by_path = {r['path']: r for r in independent_rows}
    if len(by_path) != 174 or set(by_path) != set(editorial):
        raise ValueError('INDEPENDENT_REVIEW_INCOMPLETE')
    ledgers = {}
    for i in range(1, 6):
        path = LIB / f'intake/rights-ledger-part-{i:02d}.json'
        obj = read(path)
        for row in obj['records']:
            if row['id'] in ledgers:
                raise ValueError('DUPLICATE_RIGHTS_SOURCE')
            ledgers[row['id']] = (path, row)
    registry_path = LIB / 'source_registry_catalog.json'
    registry = read(registry_path)
    catalog_path = LIB / 'catalog.json'
    catalog = read(catalog_path)
    corrections_path = LIB / 'intake/editorial-corrections.json'
    corrections = {r['path']: r for r in read(corrections_path)}
    amendment_path = LIB / 'intake/operational-scope-amendment.json'
    amendment = read(amendment_path)
    if (amendment.get('schema') != 'MEU_ARTIGO_OPERATIONAL_SCOPE_AMENDMENT_V1'
            or amendment.get('scientific_use_validated') is not False
            or amendment.get('pdf_redistribution_authorized') is not False
            or amendment.get('strictly_blocked_ids') != ['SRC-0385']):
        raise ValueError('UNSAFE_OPERATIONAL_SCOPE_AMENDMENT')
    lead_ids = set(amendment['source_lead_ids'])
    if len(lead_ids) != 14 or 'SRC-0385' in lead_ids or not lead_ids.issubset(residuals):
        raise ValueError('SOURCE_AMENDMENT_SCOPE_INVALID')
    editorial_amendments = {r['path']: r for r in amendment['editorial_card_amendments']}
    if len(editorial_amendments) != 4 or not set(editorial_amendments).issubset(editorial):
        raise ValueError('EDITORIAL_AMENDMENT_SCOPE_INVALID')
    for path, entry in editorial_amendments.items():
        if entry.get('sha') != digest(path):
            raise ValueError('EDITORIAL_AMENDMENT_CARD_HASH_MISMATCH')
    dispositions = []
    for item in registry['documents']:
        sid, path = item['source_id'], item['path']
        card = (ROOT / path).read_text(encoding='utf-8')
        # Normalize the consultation contract without changing prior findings.
        legacy_header = ('FICHA_DE_PROSPECÇÃO_NÃO_REVISADA — [P] metadados para consulta.\n'
                         'NÃO é [I] síntese de leitura nem [L] evidência científica.\n'
                         'Esta orientação é redação editorial original; não atribuir perguntas aos autores.\n\n')
        english_header = ('UNREVIEWED_PROSPECTING_CARD — [P] bibliographic metadata for consultation.\n'
                          'This is NOT an [I] synthesis of a source reading or [L] scientific evidence.\n'
                          'The guidance is original editorial text; do not attribute its questions to the source authors.\n\n')
        # Recognize both the preserved historical header and the current English
        # form; do not reintroduce Portuguese into translated source cards.
        if english_header not in card and legacy_header not in card:
            (ROOT / path).write_text(english_header + card, encoding='utf-8')
        status = 'BLOQUEADO_POR_EVIDENCIA' if sid in residuals else 'VALIDADO_COM_RESTRICOES'
        evidence = [str(ledgers[sid][0])]
        if sid in source_receipts:
            receipt_path, receipt = source_receipts[sid]
            evidence.append(receipt_path)
            item['documentary_receipt'] = receipt_path
            item['documentary_identity_claim'] = receipt.get('identidade_confirmada_boolean') is True
            # Receipt claims do not change the stronger baseline verification class.
            ledgers[sid][1]['documentary_receipt'] = receipt_path
            ledgers[sid][1]['identity_claim_in_receipt'] = item['documentary_identity_claim']
        if sid in residuals:
            receipt_path, receipt = residuals[sid]
            evidence.append(receipt_path)
            item['pending_bibliographic_findings'] = receipt_path
        if sid in lead_ids:
            # Prospecting-only access, NEVER a resolution of copy identity or rights.
            status = 'VALIDADO_COM_RESTRICOES'
            evidence.append(str(amendment_path))
        if sid == 'SRC-0385':
            excluded = amendment.get('editorial_exclusion', {})
            if (excluded.get('id') != sid
                    or excluded.get('status') != 'EXCLUIDO_COM_JUSTIFICATIVA'
                    or excluded.get('source_card_sha256') != digest(path)):
                raise ValueError('QUARANTINE_EXCLUSION_PROVENANCE_INVALID')
            status = 'EXCLUIDO_COM_JUSTIFICATIVA'
            evidence.append(str(amendment_path))
        item['sha256'] = digest(path)
        item['operational_disposition'] = status
        item['scientific_use_validated'] = False
        ledgers[sid][1]['operational_disposition'] = status
        dispositions.append({'id': sid, 'path': path, 'kind': 'BIBLIOGRAPHIC_METADATA',
            'disposition': status, 'sha256': item['sha256'], 'evidence': evidence,
            'primary_source_rechecked_this_cycle': False,
            'reason': ('Editorial exclusion: Smith/OEconomia private attribution uncorroborated; distinct Dacombe source confirmed. Not a claim of fraud or nonexistence.'
                       if sid == 'SRC-0385' else
                       'Unresolved edition/authenticity or copy provenance; bibliography prospecting [P] only.'
                       if sid in residuals else 'Integrity and receipt linkage checked; usable only as a bibliographic lead, not scientific evidence.'),
            'limits': ['No new private PDF reading', 'No primary claim support verified',
                       'No new redistribution permission', 'No scientific gate approval']})
    for item in catalog['documents']:
        path = item['path']
        receipt_path, prior = editorial[path]
        review = by_path[path]
        # Explicit blockers remain excluded; a previous receipt is never an acceptance.
        historical = str(prior.get('decision', prior.get('disposition', prior.get('triage', prior.get('editorial_verdict', prior.get('status', '')))))).upper()
        new = str(review.get('recommendation', review.get('disposition', ''))).upper()
        blocked = any(token in new for token in ('BLOQUEAD', 'BLOCKED', 'EXCLUI')) or historical == 'BLOQUEADO'
        status = 'BLOQUEADO_POR_EVIDENCIA' if blocked else 'VALIDADO_COM_RESTRICOES'
        if path in corrections and not blocked:
            if digest(path) != corrections[path]['after_sha256'] or review['sha256_reviewed'] != digest(path):
                raise ValueError('CORRECTED_CARD_NOT_REVALIDATED')
            status = 'CORRIGIDO_E_REVALIDADO'
        if path in editorial_amendments:
            # Original prompts [I]/[P] may be used as guidance with limitations.
            # This does not erase historical blockers or validate underlying PDFs.
            status = 'VALIDADO_COM_RESTRICOES'
        item['sha256'] = digest(path)
        item['operational_disposition'] = status
        item['scientific_use_validated'] = False
        dispositions.append({'id': 'EC-' + str(len(dispositions) - 474).zfill(4),
            'path': path, 'kind': 'EDITORIAL_GUIDANCE', 'disposition': status,
            'sha256': item['sha256'], 'evidence': [receipt_path, str(independent_path)] + ([str(corrections_path)] if path in corrections else []) + ([str(amendment_path)] if path in editorial_amendments else []),
            'reason': 'Individual IA content review and deterministic integrity check; restrictions/blockers from review retained.',
            'review_record': str(independent_path) + '#' + path,
            'primary_source_rechecked_this_cycle': bool(review.get('primary_evidence')),
            'limits': ['Editorial orientation only', 'Not independently validated science',
                       'Read exact source passages before [L]', 'No scientific gate approval']})
    if len(dispositions) != 649 or len({x['path'] for x in dispositions}) != 649:
        raise ValueError('EXPECTED_649_UNIQUE_CARDS')
    for i in range(1, 6):
        path = LIB / f'intake/rights-ledger-part-{i:02d}.json'
        obj = read(path)
        obj['records'] = [ledgers[r['id']][1] for r in obj['records']]
        write(path, obj)
    # Report metadata checks separately from original-copy identity verification.
    registry['operational_dispositions'] = dict(Counter(d['operational_disposition'] for d in registry['documents']))
    registry['ib_documentary_receipt_count'] = len(source_receipts)
    registry['version'] = 'integration-operational-2026-11-21'
    write(registry_path, registry)
    write(catalog_path, catalog)
    manifest_path = LIB / 'intake/rights-ledger-manifest.json'
    manifest = read(manifest_path)
    manifest['operational_validation'] = str(OUT)
    manifest['ib_receipts_integrated'] = 343
    manifest['unresolved_residuals_excluded_from_recommendations'] = sorted(set(residuals) - lead_ids)
    manifest['unresolved_copy_identities_accessible_as_leads_only'] = sorted(lead_ids)
    manifest['next'] = 'All 649 records have operational dispositions; exact copy identity, rights and primary claim support remain pending before scientific L use.'
    write(manifest_path, manifest)
    result = {'schema': 'MEU_ARTIGO_OPERATIONAL_VALIDATION_V1', 'date': '2026-11-21',
        'actor': 'IA_CODEX', 'review_policy': 'MAINTAINER_AUTHORIZED_AI_AND_CODE_OPERATIONAL_ONLY',
        'scientific_validation': False, 'human_review': False,
        'source_baseline_sha': 'c5e0ca9abd98f824f1576c3ad94c6e9a5d18e9bf',
        'version': (ROOT / 'VERSION').read_text().strip(),
        'procedure': 'scripts/reconcile_methodology_library.py',
        'ref_evidence': str(LIB / 'intake/v1_parallel/INTEGRATION-REFS.json'),
        'counts': dict(Counter(d['disposition'] for d in dispositions)),
        'card_count': 649, 'operational_scope_amendment': str(amendment_path),
        'scientific_primary_claims_validated': 0,
        'cards': dispositions}
    write(OUT, result)
    print(json.dumps({'cards': 649, 'counts': result['counts']}, ensure_ascii=False))


def check():
    report = read(OUT)
    entries = report['cards']
    expected = {str(p.relative_to(ROOT)) for folder in ('cards', 'source_cards')
                for p in (ROOT / LIB / folder).glob('*.md') if p.name != 'README.md'}
    if len(entries) != 649 or {r['path'] for r in entries} != expected:
        raise ValueError('DISPOSITION_COVERAGE_MISMATCH')
    if len({r['id'] for r in entries}) != 649:
        raise ValueError('DISPOSITION_DUPLICATE_ID')
    if report['counts'] != dict(Counter(r['disposition'] for r in entries)):
        raise ValueError('DISPOSITION_COUNT_MISMATCH')
    for row in entries:
        if row['disposition'] not in STATUSES or row['sha256'] != digest(row['path']):
            raise ValueError('DISPOSITION_STALE_OR_INVALID')
        for evidence in row['evidence']:
            if not (ROOT / evidence).is_file():
                raise ValueError('DISPOSITION_EVIDENCE_MISSING')
    for catalog in ('catalog.json', 'source_registry_catalog.json'):
        for doc in read(LIB / catalog)['documents']:
            row = next(r for r in entries if r['path'] == doc['path'])
            if doc['sha256'] != row['sha256'] or doc.get('operational_disposition') != row['disposition']:
                raise ValueError('CATALOG_DISPOSITION_MISMATCH')
    quarantine = next(r for r in entries if r['id'] == 'SRC-0385')
    if quarantine['disposition'] != 'EXCLUIDO_COM_JUSTIFICATIVA':
        raise ValueError('QUARANTINE_BREACH')
    amendment = read(LIB / 'intake/operational-scope-amendment.json')
    if report.get('operational_scope_amendment') != str(LIB / 'intake/operational-scope-amendment.json'):
        raise ValueError('OPERATIONAL_AMENDMENT_NOT_RECORDED')
    if quarantine['sha256'] != amendment.get('editorial_exclusion', {}).get('source_card_sha256'):
        raise ValueError('QUARANTINE_EXCLUSION_HASH_MISMATCH')
    for sid in amendment['source_lead_ids']:
        entry = next(r for r in entries if r['id'] == sid)
        if entry['disposition'] != 'VALIDADO_COM_RESTRICOES':
            raise ValueError('PROSPECTING_SCOPE_NOT_RECONCILED')
    for x in amendment['editorial_card_amendments']:
        entry = next(r for r in entries if r['id'] == x['id'])
        if (entry['sha256'] != x['sha'] or entry['disposition'] != 'VALIDADO_COM_RESTRICOES'):
            raise ValueError('EDITORIAL_SCOPE_NOT_RECONCILED')
    print('649 dispositions: coverage, hashes, evidence, catalogues and quarantine OK')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    check() if args.check else reconcile()
