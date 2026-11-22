#!/usr/bin/env python3
"""Offline machine translation of original editorial methodology cards.

No source-rights, evidence or scientific approvals are inferred. Historic
hash-bound corrections and operational amendments are left untouched.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
LIB=ROOT/"knowledge/methodology"
PORTUGUESE=re.compile(
    r"\b(?:não|pesquisa|revisão|análise|metodologia|fonte|fontes|"
    r"científic[ao]s?|autor(?:es|a)?|pergunta|decisão|contribuição|"
    r"verificar|evidências?|dados|método|analisar|condições|"
    r"limitações?|etapa|resultados?|direitos|texto|somente|"
    r"nenhum|nenhuma|artigo|estudo|qual|como|também|para|"
    r"trabalho|com|sem|ainda|do|da|dos|das|que)\b", re.I
)
PRESERVE=re.compile(
    r"(\x60[^\x60]+\x60|\[[LIP]\]|\b(?:SRC|EC|GATE|DEC|TRACE|IB)-\d+\b|"
    r"https?://[^\s)\]>]+|\b10\.\d{4,9}/[^\s)]+|"
    r"\[[^\]]+\]\([^)]+\))"
)

def load(p):
    return json.loads(p.read_text(encoding="utf-8"))

def digest(data):
    return hashlib.sha256(data).hexdigest()

def should_translate(s):
    t=s.strip()
    if len(t)<4 or not any(c.isalpha() for c in t):
        return False
    if PORTUGUESE.search(t):
        return True
    if len(t)<32:
        return t.lower() in {"resumo","introdução","métodos","limites",
                              "conclusão","referências","síntese","orientação"}
    import langid
    language, score=langid.classify(t)
    return language=="pt" and score>0

def fragment(s, engine):
    if not should_translate(s):
        return s
    value=s.strip()
    out=engine.translate(value)
    if not out or len(out)<max(2,len(value)//6):
        return s
    return s[:len(s)-len(s.lstrip())]+out+s[len(s.rstrip()):]

def translate_line(line,engine):
    if not line.strip() or line.lstrip().startswith(("<",chr(96)*3,"~~~")):
        return line
    match=re.match(r"^(\s*(?:#{1,6}\s+|[-*>]\s+|\d+\.\s+)?)(.*)$",line)
    prefix,body=match.groups()
    parts=PRESERVE.split(body)
    for i in range(0,len(parts),2):
        parts[i]=fragment(parts[i],engine)
    out=prefix+"".join(parts)
    return out if sorted(PRESERVE.findall(line))==sorted(PRESERVE.findall(out)) else line

def translate_content(s,engine):
    lines=[]
    in_code=False
    in_original_bibliography=False
    for raw in s.splitlines(keepends=True):
        e="\n" if raw.endswith("\n") else ""
        line=raw[:-1] if e else raw
        if line.lstrip().startswith((chr(96)*3,"~~~")):
            in_code=not in_code
        # Leave published reference lines as written, especially original titles.
        if re.search(r"(?i)^##\s+(?:fonte|referência|referências|bibliografia|source|bibliographic)",line):
            in_original_bibliography=True
        elif line.startswith("## "):
            in_original_bibliography=False
        protected_citation=in_original_bibliography and (
            bool(re.search(r"\b\d{4}\b",line)) and
            (line.count(".")>=2 or "doi" in line.lower()))
        lines.append((line if in_code or protected_citation else translate_line(line,engine))+e)
    return "".join(lines)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--limit",type=int,default=174)
    parser.add_argument("--report",required=True)
    a=parser.parse_args()
    if a.limit<1 or a.limit>174:
        raise ValueError("INVALID_LIMIT")
    catpath=LIB/"catalog.json"
    ledgerpath=LIB/"intake/operational-validation.json"
    cat,ledger=load(catpath),load(ledgerpath)
    rows={x["path"]:x for x in cat["documents"]}
    receipts={x["path"]:x for x in ledger["cards"]}
    corrections={x["path"] for x in load(LIB/"intake/editorial-corrections.json")}
    amend=load(LIB/"intake/operational-scope-amendment.json")
    protected=corrections|{x["path"] for x in amend["editorial_card_amendments"]}
    candidates=[p for p in sorted((LIB/"cards").glob("*.md"))
                if p.relative_to(ROOT).as_posix() in rows
                and p.relative_to(ROOT).as_posix() not in protected
                and PORTUGUESE.search(p.read_text(encoding="utf-8"))]
    from argostranslate import package,translate
    package.update_package_index()
    models=[x for x in package.get_available_packages()
            if x.from_code in ("pt","pb") and x.to_code=="en"]
    if not models:
        raise RuntimeError("NO_OFFLINE_PORTUGUESE_ENGLISH_MODEL")
    models.sort(key=lambda x:x.from_code!="pt")
    selected=models[0]
    package.install_from_path(selected.download())
    engine=translate.get_translation_from_codes(selected.from_code,"en")
    changed=[]
    skipped=[]
    for p in candidates[:a.limit]:
        key=p.relative_to(ROOT).as_posix()
        old=p.read_bytes()
        new=translate_content(old.decode("utf-8"),engine).encode("utf-8")
        identifiers=re.findall(r"\b(?:SRC|EC|GATE|DEC)-\d+\b",old.decode("utf-8"))
        if (new==old or len(new)>14000 or
            not all(x.encode("utf-8") in new for x in identifiers)):
            skipped.append(key)
            continue
        if "[I]" in old.decode("utf-8") and b"[I]" not in new:
            skipped.append(key)
            continue
        p.write_bytes(new)
        rows[key]["sha256"]=digest(new)
        receipts[key]["sha256"]=digest(new)
        rows[key]["translation_fidelity_status"]="MACHINE_TRANSLATED_REVIEW_PENDING"
        changed.append({"path":key,"previous":digest(old),"translated":digest(new)})
        print("TRANSLATED",key,flush=True)
    if changed:
        for path,obj in ((catpath,cat),(ledgerpath,ledger)):
            path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",
                            encoding="utf-8")
    result={"mode":"OFFLINE_EDITORIAL_TRANSLATION_NOT_SCIENTIFIC_APPROVAL",
            "model":selected.from_code+"->en","changed":changed,
            "skipped":skipped,"human_fidelity_review":False,
            "approved_gates":0,"historical_corrections_unchanged":True}
    Path(a.report).write_text(json.dumps(result,ensure_ascii=False,indent=2),
                              encoding="utf-8")
    print(json.dumps({"translated":len(changed),"skipped":len(skipped)}))
    if not changed:
        raise SystemExit("NO_ELIGIBLE_EDITORIAL_CHANGES")

if __name__=="__main__":
    main()
