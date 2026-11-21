#!/usr/bin/env python3
"""Offline, local-only experimental conceptual RAG index for a private Drive mirror.

SQLite FTS5 lexical retrieval is always available. Vector retrieval is enabled
ONLY when an already installed, local-only sentence-transformer model is supplied.
No Drive SDK/API, keys, downloads, sync, remote embedding calls or gate writes.
Never infer semantic validity from embedding similarity.
"""
from __future__ import annotations
import argparse
from array import array
from contextlib import closing
import hashlib
import json
import math
import os
from pathlib import Path
import re
import sqlite3
import sys

SCHEMA = 'MEU_ARTIGO_CONCEPTUAL_RAG_PILOT_V1'
PAGE = re.compile(r'<!--\s*source_page:\s*(\d+)\s*-->')
WORDS = re.compile(r'\w+', re.UNICODE)
MAX_MD_BYTES = 5_000_000
ALLOWED_RIGHTS = {'PRIVATE_AUTHORIZED', 'PUBLIC_DOMAIN'}


def digest(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def source_chunks(root: Path, *, size=1000, overlap=100):
    if not (150 <= size <= 5000 and 0 <= overlap < size//2):
        raise ValueError('INVALID_CHUNK_BOUNDS')
    if not root.is_dir() or root.is_symlink():
        raise ValueError('LIBRARY_DIRECTORY_REQUIRED')
    out=[]
    seen=set()
    for path in sorted(root.rglob('*.md')):
        if path.is_symlink() or any(x.is_symlink() for x in path.parents if x != root and root in x.parents):
            raise ValueError('SYMLINK_SOURCE_BLOCKED')
        if path.stat().st_size > MAX_MD_BYTES:
            raise ValueError('SOURCE_TOO_LARGE')
        raw=path.read_bytes()
        try: content=raw.decode('utf-8')
        except UnicodeDecodeError as e: raise ValueError('SOURCE_NOT_UTF8') from e
        meta_path=path.with_name(path.name+'.meta.json')
        if not meta_path.is_file() or meta_path.is_symlink():
            raise ValueError('SOURCE_METADATA_REQUIRED')
        m=json.loads(meta_path.read_text(encoding='utf-8'))
        if m.get('schema') != 'MEU_ARTIGO_MD_SOURCE_V1':
            raise ValueError('SOURCE_METADATA_SCHEMA_INVALID')
        if m.get('rights_status') not in ALLOWED_RIGHTS or m.get('extraction_status') != 'HUMAN_REVIEWED':
            raise ValueError('SOURCE_NOT_AUTHORIZED_OR_REVIEWED')
        if m.get('md_sha256') != digest(raw):
            raise ValueError('SOURCE_HASH_MISMATCH')
        sid=m.get('source_id')
        if not isinstance(sid,str) or not re.fullmatch(r'[A-Za-z0-9_-]{3,80}',sid) or sid in seen:
            raise ValueError('DUPLICATE_OR_INVALID_SOURCE_ID')
        seen.add(sid)
        matches=list(PAGE.finditer(content))
        if not matches:
            raise ValueError('SOURCE_PAGE_MARKERS_REQUIRED')
        if [int(x.group(1)) for x in matches] != list(range(1,len(matches)+1)):
            raise ValueError('SOURCE_PAGE_MARKERS_INCOMPLETE')
        if m.get('page_count') != len(matches):
            raise ValueError('SOURCE_PAGE_COUNT_MISMATCH')
        for i,mat in enumerate(matches):
            block=content[mat.end():matches[i+1].start() if i+1 < len(matches) else len(content)].strip()
            if not block:continue
            cursor=0;seq=0
            while cursor < len(block):
                end=min(cursor+size,len(block))
                if end < len(block):
                    boundary=block.rfind(' ',max(cursor+100,end-130),end)
                    if boundary > cursor+100:end=boundary
                excerpt=block[cursor:end].strip()
                if not excerpt:break
                key=f'{sid}:p{int(mat.group(1))}:c{seq}'
                out.append({'id':key,'source_id':sid,'title':str(m.get('title') or sid)[:200],
                            'source_file':path.relative_to(root).as_posix(),
                            'page':int(mat.group(1)),'text':excerpt,
                            'rights_status':m['rights_status']})
                if end >= len(block):break
                cursor=max(cursor+1,end-overlap);seq+=1
    if not out:raise ValueError('NO_ELIGIBLE_SOURCE_CHUNKS')
    if len(out)>100000:raise ValueError('TOO_MANY_CHUNKS')
    return out


def local_encoder(model_dir: Path):
    """Only load an explicitly provisioned on-disk model; never download."""
    model_dir=Path(model_dir).resolve()
    if not model_dir.is_dir() or not (model_dir/'modules.json').exists():
        raise ValueError('LOCAL_SENTENCE_TRANSFORMER_MODEL_REQUIRED')
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise ValueError('SENTENCE_TRANSFORMERS_NOT_INSTALLED') from exc
    try:
        return SentenceTransformer(str(model_dir),local_files_only=True)
    except TypeError as exc:
        raise ValueError('LOCAL_ONLY_MODEL_LOADING_UNSUPPORTED') from exc


def vectors_for(items, encoder):
    data=encoder.encode([x['text'] for x in items],normalize_embeddings=True)
    vectors=[]
    dim=None
    for row in data:
        vals=[float(v) for v in row]
        if not vals or any(not math.isfinite(v) for v in vals):
            raise ValueError('EMBEDDING_INVALID')
        if dim is None:dim=len(vals)
        if len(vals)!=dim:raise ValueError('EMBEDDING_DIMENSION_INCONSISTENT')
        norm=math.sqrt(sum(x*x for x in vals))
        if norm <= 0:raise ValueError('EMBEDDING_ZERO_VECTOR')
        vectors.extend(x/norm for x in vals)
    return dim,vectors


def create_index(library: Path, index: Path, *, model_dir:Path|None=None, encoder=None):
    library,index=Path(library).resolve(),Path(index).absolute()
    if index.exists() or index.is_symlink() or not index.parent.is_dir():
        raise ValueError('CREATE_NEW_INDEX_DIRECTORY_REQUIRED')
    if index == library or library in index.parents:
        raise ValueError('INDEX_OUTSIDE_LIBRARY_REQUIRED')
    rows=source_chunks(library)
    vector_enabled=encoder is not None or model_dir is not None
    if model_dir is not None and encoder is None:encoder=local_encoder(model_dir)
    dim,values=(vectors_for(rows,encoder) if vector_enabled else (None,None))
    index.mkdir(mode=0o700)
    try:
        chunk_path=index/'chunks.jsonl'
        chunk_path.write_text(''.join(json.dumps(x,ensure_ascii=False,sort_keys=True)+'\n' for x in rows),encoding='utf-8')
        db=index/'lexical.sqlite3'
        connection=sqlite3.connect(str(db))
        try:
            connection.execute('CREATE VIRTUAL TABLE passages USING fts5(text, tokenize="unicode61")')
            connection.executemany('INSERT INTO passages(rowid,text) VALUES(?,?)',[(i+1,x['text']) for i,x in enumerate(rows)])
            connection.commit()
        finally:connection.close()
        if vector_enabled:
            vec=array('f',values)
            if sys.byteorder!='little':vec.byteswap()
            (index/'vectors.f32').write_bytes(vec.tobytes())
        tracked=['chunks.jsonl','lexical.sqlite3']+(['vectors.f32'] if vector_enabled else [])
        manifest={'schema':SCHEMA,'chunk_count':len(rows),'source_count':len(set(x['source_id'] for x in rows)),
                  'retrieval': 'HYBRID_LOCAL' if vector_enabled else 'LEXICAL_ONLY',
                  'vector_dim':dim,'model_identity':str(Path(model_dir).name) if model_dir is not None else ('TEST_ENCODER' if encoder else None),
                  'files':{f:digest((index/f).read_bytes()) for f in tracked},
                  'external_network_used':False,'public_distribution_allowed':False,
                  'semantic_support_proven':False,'scientific_gate_approved':False,
                  'note':'Copy only into authorized private storage after review; index contains source excerpts.'}
        (index/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        for p in index.iterdir():p.chmod(0o600)
        return manifest
    except Exception:
        for p in index.iterdir():p.unlink()
        index.rmdir()
        raise


def verify(index: Path):
    index=Path(index).resolve()
    man=json.loads((index/'manifest.json').read_text(encoding='utf-8'))
    if man.get('schema')!=SCHEMA:raise ValueError('INDEX_SCHEMA_MISMATCH')
    expected={'chunks.jsonl','lexical.sqlite3'}|({'vectors.f32'} if man.get('retrieval')=='HYBRID_LOCAL' else set())
    if set(man.get('files',{}))!=expected:raise ValueError('INDEX_FILES_INVALID')
    for fn,sha in man['files'].items():
        f=index/fn
        if f.is_symlink() or digest(f.read_bytes())!=sha:raise ValueError('INDEX_DIGEST_MISMATCH')
    rows=[json.loads(line) for line in (index/'chunks.jsonl').read_text(encoding='utf-8').splitlines()]
    if len(rows)!=man.get('chunk_count'):raise ValueError('INDEX_CHUNK_COUNT_MISMATCH')
    return man,rows


def search(index: Path, question: str, *, top=5, encoder=None, model_dir:Path|None=None):
    if not isinstance(question,str) or not question.strip() or len(question)>1000 or not 1<=top<=20:
        raise ValueError('QUERY_INVALID')
    man,rows=verify(index)
    terms=[w for w in WORDS.findall(question.casefold()) if len(w)>1][:16]
    if not terms:raise ValueError('QUERY_EMPTY_TERMS')
    with closing(sqlite3.connect(f'file:{(Path(index)/"lexical.sqlite3").resolve()}?mode=ro',uri=True)) as con:
        match=' OR '.join('"'+s.replace('"','')+'"' for s in terms)
        lexical=con.execute('SELECT rowid FROM passages WHERE passages MATCH ? ORDER BY bm25(passages) LIMIT 40',(match,)).fetchall()
    scores={int(v[0])-1:1/(60+rank) for rank,v in enumerate(lexical,1)}
    mode='LEXICAL_ONLY';warnings=[]
    if man.get('retrieval')=='HYBRID_LOCAL':
        if encoder is None and model_dir is not None:encoder=local_encoder(model_dir)
        if encoder is None:
            warnings.append('VECTOR_INDEX_PRESENT_BUT_NO_LOCAL_QUERY_ENCODER')
        else:
            if man.get('model_identity') != (str(Path(model_dir).name) if model_dir is not None else 'TEST_ENCODER'):
                raise ValueError('EMBEDDING_MODEL_IDENTITY_MISMATCH')
            dim=man['vector_dim'];values=array('f')
            values.frombytes((Path(index)/'vectors.f32').read_bytes())
            if sys.byteorder!='little':values.byteswap()
            if len(values)!=len(rows)*dim:raise ValueError('VECTOR_SHAPE_MISMATCH')
            query=list(encoder.encode([question],normalize_embeddings=True)[0]); qnorm=math.sqrt(sum(float(v)**2 for v in query))
            if len(query)!=dim or not math.isfinite(qnorm) or qnorm<=0:raise ValueError('QUERY_VECTOR_INVALID')
            q=[float(v)/qnorm for v in query]
            similarity=[]
            for i in range(len(rows)):
                sim=sum(values[i*dim+j]*q[j] for j in range(dim))
                similarity.append((i,sim))
            similarity.sort(key=lambda z:z[1],reverse=True)
            for rank,(i,_) in enumerate(similarity[:40],1):scores[i]=scores.get(i,0)+1/(60+rank)
            mode='HYBRID_LOCAL'
    winners=sorted(scores,key=lambda i:(-scores[i],rows[i]['id']))[:top]
    return {'schema':SCHEMA,'retrieval_mode':mode,'warnings':warnings,
            'sources_consulted_by_this_query':len({rows[i]['source_id'] for i in winners}),
            'hits':[{'source_id':rows[i]['source_id'],'title':rows[i]['title'],'page':rows[i]['page'],
                     'chunk_id':rows[i]['id'],'excerpt':rows[i]['text'][:360],
                     'evidence_type':'RETRIEVED_TEXT_NOT_SEMANTICALLY_VALIDATED'} for i in winners],
            'scientific_quality_validated':False,'researcher_decision_recorded':False,
            'read_only':True,'external_network_used':False}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    sub=ap.add_subparsers(dest='command',required=True)
    build=sub.add_parser('build');build.add_argument('--library',required=True,type=Path);build.add_argument('--index',required=True,type=Path);build.add_argument('--local-model',type=Path)
    query=sub.add_parser('query');query.add_argument('--index',required=True,type=Path);query.add_argument('--text',required=True);query.add_argument('--top',type=int,default=5);query.add_argument('--local-model',type=Path)
    a=ap.parse_args()
    try:
        out=create_index(a.library,a.index,model_dir=a.local_model) if a.command=='build' else search(a.index,a.text,top=a.top,model_dir=a.local_model)
        print(json.dumps(out,ensure_ascii=False))
        return 0
    except (OSError,ValueError,sqlite3.Error,ImportError) as e:
        print(json.dumps({'status':'BLOCKED','reason':str(e)}))
        return 2
if __name__=='__main__':sys.exit(main())
