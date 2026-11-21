#!/usr/bin/env python3
"""Private, local-only PDF -> page-addressable Markdown candidate.

No OCR, cloud upload, overwrite, publication, or claim of verified reading.
The output is NOT index-eligible until a human reviews extraction and rights.
"""
import argparse
import os
import hashlib
import json
from pathlib import Path
import re
import sys


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def convert(pdf: Path, md: Path, *, source_id: str, title: str):
    raw_pdf = Path(pdf)
    if raw_pdf.is_symlink():
        raise ValueError('SOURCE_PDF_SYMLINK_BLOCKED')
    pdf, md = raw_pdf.resolve(), Path(md).absolute()
    if not pdf.is_file() or pdf.suffix.lower() != '.pdf':
        raise ValueError('SOURCE_PDF_REQUIRED')
    if not re.fullmatch(r'[A-Za-z0-9_-]{3,80}', source_id):
        raise ValueError('INVALID_SOURCE_ID')
    meta = md.with_name(md.name + '.meta.json')
    if md.exists() or md.is_symlink() or meta.exists() or meta.is_symlink():
        raise ValueError('CREATE_ONLY_NO_OVERWRITE')
    if not md.parent.is_dir() or md.parent == pdf.parent and md.name == pdf.name:
        raise ValueError('OUTPUT_PARENT_REQUIRED')
    try:
        import fitz
    except ImportError as exc:
        raise ValueError('PYMUPDF_REQUIRED_LOCAL') from exc
    pages = []
    warnings = []
    with fitz.open(str(pdf)) as document:
        if document.is_encrypted:
            raise ValueError('ENCRYPTED_PDF_NOT_SUPPORTED')
        for n, page in enumerate(document, 1):
            text = page.get_text('text', sort=True).strip()
            if len(text) < 50:
                warnings.append({'page': n, 'code': 'LOW_TEXT_OCR_OR_MANUAL_REVIEW'})
            pages.append(f'<!-- source_page: {n} -->\n\n{text}\n')
    if not pages:
        raise ValueError('EMPTY_PDF')
    body = '\n'.join([f'# {title}', ''] + pages).rstrip() + '\n'
    metadata = {'schema':'MEU_ARTIGO_MD_SOURCE_V1', 'source_id':source_id,
                'title':title,'original_pdf_name':pdf.name,
                'original_pdf_sha256':sha256(pdf), 'page_count':len(pages),
                'md_sha256':hashlib.sha256(body.encode('utf-8')).hexdigest(),
                'extraction_status':'REVIEW_REQUIRED',
                'rights_status':'NOT_REVIEWED',
                'warnings':warnings,
                'provenance_notice':'This extraction is not a verified scholarly reading or redistribution license.'}
    # Create only. Files are intentionally private (0600) and retain source PDF.
    created=[]
    try:
        for path, data in ((md, body), (meta, json.dumps(metadata, ensure_ascii=False, indent=2)+'\n')):
            with open(path, 'x', encoding='utf-8', opener=lambda name, flags: os.open(name, flags, 0o600)) as f:
                f.write(data)
            created.append(path)
    except Exception:
        for path in created:
            path.unlink()
        raise
    return {'status':'REVIEW_REQUIRED','source_id':source_id,'pages':len(pages),
            'md':str(md),'metadata':str(meta),'warnings':len(warnings),
            'source_unchanged':True,'shared_or_uploaded':False}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('pdf',type=Path)
    p.add_argument('md',type=Path)
    p.add_argument('--source-id',required=True)
    p.add_argument('--title',required=True)
    a=p.parse_args()
    try:
        print(json.dumps(convert(a.pdf,a.md,source_id=a.source_id,title=a.title), ensure_ascii=False))
        return 0
    except (OSError,ValueError,RuntimeError) as e:
        print(json.dumps({'status':'BLOCKED','reason':str(e)}))
        return 2
if __name__=='__main__':sys.exit(main())
