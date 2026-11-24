#!/usr/bin/env python3
"""Read-only candidate retrieval and conservative matching; no corpus or gate writes."""
from __future__ import annotations
import argparse, json, re, os
from bibliographic_connectors import search
from verify_sources import norm, doi_of

def rank_candidates(record, rows):
    """Exact normalized title plus author token/year/venue checks; no auto-verification."""
    title=norm(record.get('title')); author=norm(record.get('author'))
    year=str(record.get('year') or '').strip(); journal=norm(record.get('journal'))
    candidates=[]
    for row in rows:
        doi=doi_of(row.get('doi'))
        if not doi or not title or norm(row.get('title'))!=title: continue
        authors=set(norm(row.get('authors')).split()); tokens=set(author.split())
        author_match=bool(tokens and tokens.issubset(authors)); year_match=bool(year and str(row.get('year'))==year)
        venue_match=bool(journal and norm(row.get('journal'))==journal)
        candidates.append({'doi':doi,'source':row.get('source'),'title':row.get('title'),'authors':row.get('authors'),'year':row.get('year'),'journal':row.get('journal'),'author_match':author_match,'year_match':year_match,'venue_match':venue_match,'candidate_only':True})
    exact=[c for c in candidates if c['author_match'] and c['year_match'] and (not journal or c['venue_match'])]
    ids={c['doi'] for c in candidates}; strong={c['doi'] for c in exact}
    status='MATCH_CANDIDATE' if len(ids)==len(strong)==1 else 'AMBIGUOUS' if len(ids)>1 else 'CONFLICT' if candidates else 'NOT_FOUND'
    return {'status':status,'candidates':candidates,'verified_identity':False,'human_gate_approved':False,'canonical_write':False}

def recover(record, *, allow_network=False, lookup=search):
    if not str(record.get('title') or '').strip(): raise ValueError('title required')
    if not allow_network: return {'status':'NOT_EXECUTED','verified_identity':False,'canonical_write':False,'attempts':[]}
    query=' '.join(str(record.get(k) or '') for k in ('title','author','year'))[:600]
    all_rows=[]; attempts=[]
    for provider in ('crossref','openalex','semantic_scholar'):
        out=lookup(provider,query,limit=10,execute=True,api_key=os.environ.get({'openalex':'OPENALEX_API_KEY','semantic_scholar':'SEMANTIC_SCHOLAR_API_KEY'}.get(provider,''),''))
        attempts.append({'provider':provider,'query':query,'status':out.status,'retrieved':len(out.rows),'executed_at':out.executed_at})
        all_rows.extend(out.rows)
        if rank_candidates(record,all_rows)['status']=='MATCH_CANDIDATE': break
    result=rank_candidates(record,all_rows)
    if result['status']=='NOT_FOUND' and any(a['status'] not in ('COMPLETE','PARTIAL') for a in attempts): result['status']='UNVERIFIED'
    result['attempts']=attempts; return result

def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--title',required=True);p.add_argument('--author',default='');p.add_argument('--year',default='');p.add_argument('--journal',default='');p.add_argument('--allow-network',action='store_true');a=p.parse_args()
    print(json.dumps(recover(vars(a),allow_network=a.allow_network),ensure_ascii=False,indent=2))
if __name__=='__main__': main()
