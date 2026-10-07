#!/usr/bin/env python3
"""Build a data-driven Corpus Map from a canonical Meu Artigo project.

No network access and no third-party dependencies are required. The script uses
only metadata already present in the project. Optional bibliographic fields such
as journal/source title, keywords, OpenAlex ID, or citation links are used only
when they actually exist.

Outputs:
  04_Evidencias_e_Sintese/MAPA_CORPUS.json
  04_Evidencias_e_Sintese/MAPA_CORPUS.md
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

MGMT="00_Gestao_e_Continuidade"

def read_csv(path:Path)->list[dict[str,str]]:
    if not path.exists():
        return []
    with path.open("r",encoding="utf-8-sig",newline="") as f:
        return list(csv.DictReader(f))

def first_present(row:dict[str,str], names:list[str])->str:
    for name in names:
        v=(row.get(name) or "").strip()
        if v:
            return v
    return ""

def split_people(value:str)->list[str]:
    if not value:
        return []
    if ";" in value:
        parts=value.split(";")
    elif "|" in value:
        parts=value.split("|")
    elif " and " in value.lower():
        parts=re.split(r"\s+and\s+",value,flags=re.I)
    else:
        # Do not split on comma because many exports use "Family, Given".
        parts=[value]
    return [p.strip() for p in parts if p.strip()]

def split_terms(value:str)->list[str]:
    if not value:
        return []
    parts=re.split(r"[;|]",value)
    return [re.sub(r"\s+"," ",p).strip() for p in parts if p.strip()]

def eligible_record_ids(screen:list[dict[str,str]], fulltext:list[dict[str,str]])->set[str]:
    out=set()
    for r in screen:
        rid=(r.get("Record_ID") or "").strip()
        d=(r.get("Pass2_decision") or "").upper().strip()
        if rid and d in {"FULL TEXT — CORE","FULL TEXT — SUPPORT","FULL TEXT - CORE","FULL TEXT - SUPPORT"}:
            out.add(rid)
    for r in fulltext:
        rid=(r.get("Record_ID") or "").strip()
        decision=(r.get("Full_text_decision") or "").upper().strip()
        if rid and decision=="INCLUDE":
            out.add(rid)
    return out

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--output-dir",default="")
    a=ap.parse_args()

    root=Path(a.project).resolve()
    screen=read_csv(root/MGMT/"03_Screening.csv")
    fulltext=read_csv(root/MGMT/"04_FullText_Tracker.csv")
    evidence=read_csv(root/MGMT/"05_Evidence_Matrix.csv")
    eligible=eligible_record_ids(screen,fulltext)

    retained=[r for r in screen if (r.get("Record_ID") or "").strip() in eligible]
    by_id={(r.get("Record_ID") or "").strip():r for r in retained}

    years=Counter()
    authors=Counter()
    sources=Counter()
    keywords=Counter()
    concepts=Counter()
    openalex=0
    dois=0
    warnings=[]

    source_fields=["Source_title","Journal","Publication_name","Publication Name","Source title","SO"]
    keyword_fields=["Keywords","Author_Keywords","Author Keywords","DE","Index_Keywords","Indexed Keywords"]
    openalex_fields=["OpenAlex_ID","OpenAlex ID","openalex_id"]

    for r in retained:
        year=(r.get("Year") or "").strip()
        if year:
            years[year]+=1
        for person in split_people(r.get("Authors") or ""):
            authors[person]+=1
        src=first_present(r,source_fields)
        if src:
            sources[src]+=1
        for field in keyword_fields:
            for term in split_terms(r.get(field) or ""):
                keywords[term]+=1
        if first_present(r,openalex_fields):
            openalex+=1
        if (r.get("DOI") or "").strip():
            dois+=1

    evidence_record_links=0
    for e in evidence:
        concept=(e.get("Construct_or_concept") or "").strip()
        if concept:
            concepts[concept]+=1
        rid=first_present(e,["Record_ID","Canonical_record_id","Source_Record_ID"])
        if rid:
            evidence_record_links+=1

    years_sorted=sorted(years.items(),key=lambda kv:(int(kv[0]) if kv[0].isdigit() else 999999,kv[0]))
    numeric_years=[int(y) for y in years if y.isdigit()]
    year_range=[min(numeric_years),max(numeric_years)] if numeric_years else []

    coverage={
        "retained_records":len(retained),
        "doi_records":dois,
        "doi_coverage": round(dois/len(retained),4) if retained else 0,
        "openalex_records":openalex,
        "openalex_coverage": round(openalex/len(retained),4) if retained else 0,
        "source_title_records":sum(sources.values()),
        "source_title_coverage": round(sum(sources.values())/len(retained),4) if retained else 0,
        "records_with_author_data":sum(1 for r in retained if (r.get("Authors") or "").strip()),
        "author_coverage": round(sum(1 for r in retained if (r.get("Authors") or "").strip())/len(retained),4) if retained else 0,
    }

    if retained and not sources:
        warnings.append("No journal/source-title field was available in retained screening records.")
    if retained and not keywords:
        warnings.append("No keyword field was available in retained screening records.")
    if retained and not openalex:
        warnings.append("No OpenAlex identifier was available; no OpenAlex-based network analysis was performed.")
    if not retained:
        warnings.append("No retained FULL TEXT — CORE/SUPPORT or INCLUDE records were found.")

    # Network clustering is intentionally not fabricated. It remains unavailable
    # until a real edge model is supplied by citation/coauthorship/etc.
    map_data={
        "generated_at":datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "method":"Descriptive corpus map from canonical retained metadata.",
        "edge_definition":None,
        "cluster_method":None,
        "year_range":year_range,
        "coverage":coverage,
        "publications_by_year":[{"year":y,"count":n} for y,n in years_sorted],
        "top_authors":[{"author":k,"count":v} for k,v in authors.most_common(20)],
        "top_source_titles":[{"source_title":k,"count":v} for k,v in sources.most_common(20)],
        "top_keywords":[{"keyword":k,"count":v} for k,v in keywords.most_common(30)],
        "top_evidence_constructs":[{"construct":k,"count":v} for k,v in concepts.most_common(30)],
        "clusters":[],
        "bridge_records":[],
        "warnings":warnings,
        "record_ids":sorted(by_id),
    }

    outdir=Path(a.output_dir).resolve() if a.output_dir else root/"04_Evidencias_e_Sintese"
    outdir.mkdir(parents=True,exist_ok=True)
    json_path=outdir/"MAPA_CORPUS.json"
    md_path=outdir/"MAPA_CORPUS.md"
    json_path.write_text(json.dumps(map_data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

    lines=[
        "# Mapa do Corpus",
        "",
        f"Generated: {map_data['generated_at']}",
        "",
        "## Corpus overview",
        f"- Retained records: {coverage['retained_records']}",
        f"- Year range: {year_range[0]}–{year_range[1]}" if year_range else "- Year range: unavailable",
        f"- DOI coverage: {coverage['doi_records']}/{coverage['retained_records']} ({coverage['doi_coverage']:.1%})" if retained else "- DOI coverage: 0/0",
        f"- OpenAlex coverage: {coverage['openalex_records']}/{coverage['retained_records']} ({coverage['openalex_coverage']:.1%})" if retained else "- OpenAlex coverage: 0/0",
        f"- Source-title coverage: {coverage['source_title_records']}/{coverage['retained_records']} ({coverage['source_title_coverage']:.1%})" if retained else "- Source-title coverage: 0/0",
        "",
        "## Publications by year",
    ]
    lines += [f"- {x['year']}: {x['count']}" for x in map_data["publications_by_year"]] or ["- No year data available."]
    lines += ["","## Top authors"]
    lines += [f"- {x['author']}: {x['count']}" for x in map_data["top_authors"]] or ["- No author data available."]
    lines += ["","## Top source titles"]
    lines += [f"- {x['source_title']}: {x['count']}" for x in map_data["top_source_titles"]] or ["- No source-title data available."]
    lines += ["","## Top keywords"]
    lines += [f"- {x['keyword']}: {x['count']}" for x in map_data["top_keywords"]] or ["- No keyword data available."]
    lines += ["","## Evidence-matrix constructs"]
    lines += [f"- {x['construct']}: {x['count']}" for x in map_data["top_evidence_constructs"]] or ["- No evidence constructs available."]
    lines += [
        "",
        "## Network clusters / bridge records",
        "- Not generated unless a real network edge model is available (citation, coauthorship, bibliographic coupling, co-citation, or keyword co-occurrence).",
        "",
        "## Warnings",
    ]
    lines += [f"- {w}" for w in warnings] or ["- None."]
    lines += [
        "",
        "## Interpretation",
        "",
        "This map is exploratory unless the study design explicitly adopts bibliometric methods. Missing metadata is reported rather than inferred.",
    ]
    md_path.write_text("\n".join(lines)+"\n",encoding="utf-8")

    print(json_path)
    print(md_path)
    print(f"retained_records={len(retained)}")
    print(f"warnings={len(warnings)}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
