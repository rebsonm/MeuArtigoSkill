#!/usr/bin/env python3
"""One-time translation of Portuguese prose in maintained Python program text.

Do not translate machine schemas, immutable IDs, user data, paths, regexes,
test fixtures or nonliteral expressions. Translation is an editorial first
pass. The existing regression tests must run after the resulting commit.
"""
from __future__ import annotations
import ast
import io
import json
import re
import sys
import time
import tokenize
import urllib.parse
import urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from audit_source_language import PORTUGUESE_WORDS

FILES=[
    "scripts/build_matrix_template.py",
    "scripts/method_routes.py",
    "scripts/init_project.py",
    "scripts/editorial_ai_disclosure.py",
    "scripts/release_audit.py",
]
MORE_PT=re.compile(r"\b(?:título|revista|motivo|fonte|etapa|prazo|resumo|avaliação|"
                   r"observações|revisão|análise|evidências|evidência|pesquisa|"
                   r"autor(?:es)?|artigo|desenho|método|registro|dados|"
                   r"citação|conclusão|problema|pessoa|projeto|definição|"
                   r"documento|requisito|critérios|sim|não|verificação|"
                   r"justificativa|limitações|human[ao]s?|periódico)\b",re.I)
MACHINE_PATH=re.compile(r"(?:[/\\]|\.[a-z]{2,6}\b|https?://|[A-Z_]{4,}|^[A-Z0-9_-]+$)")


def translate(value):
    if not MORE_PT.search(value):
        return value
    params=urllib.parse.urlencode({"client":"gtx","sl":"pt","tl":"en","dt":"t","q":value})
    url="https://translate.googleapis.com/translate_a/single?"+params
    for attempt in range(5):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
            with urllib.request.urlopen(req,timeout=30) as r:
                decoded=json.loads(r.read().decode("utf-8"))
            out="".join(str(s[0] or "") for s in decoded[0])
            if out: return out
        except Exception:
            if attempt==4:raise
            time.sleep(1.5*(attempt+1))
    raise RuntimeError("translation unavailable")


def replace_spans(source,spans):
    lines=source.splitlines(keepends=True)
    # Apply in reverse order so token positions refer to the original code.
    for (start,end),new_text in sorted(spans,key=lambda x:x[0],reverse=True):
        line1,col1=start
        line2,col2=end
        if line1!=line2:
            raise ValueError("Unexpected multiline token; conservative skip")
        line=lines[line1-1]
        lines[line1-1]=line[:col1]+new_text+line[col2:]
    return "".join(lines)


def convert_source(path):
    original=path.read_text(encoding="utf-8")
    line_tokens=list(tokenize.generate_tokens(io.StringIO(original).readline))
    fixes=[]
    cache={}
    substitutions={}
    for token in line_tokens:
        if token.type!=tokenize.STRING:
            continue
        literal=token.string
        if literal.lower().startswith(("r'",'r"','b"', "b'", "f'",'f"')):
            continue
        try:value=ast.literal_eval(literal)
        except (ValueError,SyntaxError):
            continue
        if not isinstance(value,str) or len(value)<4:
            continue
        if value.startswith("=") or not MORE_PT.search(value):
            continue
        if (len(value)<25 and MACHINE_PATH.search(value)
                and "/" in value and MORE_PT.search(value)):
            # Slash-delimited column labels ARE user-facing; preserve
            # command paths, actual source paths and URLs only.
            if ".py" in value or ".md" in value or "http" in value:continue
        if (re.fullmatch(r"[A-Za-z0-9_-]+",value)
                or value.startswith(("http:","https:","--","scripts/"))):
            continue
        # Avoid fixed user-language words in route inference that remain
        # legitimate Portuguese synonyms even in English source code.
        if path.name=="method_routes.py" and token.start[0]>90 and token.start[0]<110:
            continue
        if value in cache:
            after=cache[value]
        else:
            after=translate(value)
            cache[value]=after
            time.sleep(0.08)
        if after!=value:
            fixes.append(((token.start,token.end),repr(after)))
            substitutions[value]=after
    new=replace_spans(original,fixes)
    # Keep downstream formula lookups coupled to translated display labels
    # without translating Excel expression/function syntax.
    for old,new_text in sorted(substitutions.items(),key=lambda kv:-len(kv[0])):
        if len(old)>80:continue
        if old in new and old!=new_text:
            # Only replace literal label text inside string delimiters,
            # not arbitrary identifier names in source lines.
            quoted='"'+old+'"'
            if quoted in new:
                new=new.replace(quoted,'"'+new_text+'"')
    ast.parse(new,filename=str(path))
    path.write_text(new,encoding="utf-8")
    print("PYTHON_TRANSLATED",path.relative_to(ROOT).as_posix(),"literal_values",len(fixes),flush=True)
    return len(fixes)


def main():
    total=0
    for relative in FILES:
        p=ROOT/relative
        try:
            total+=convert_source(p)
        except Exception as exc:
            print("PYTHON_FAILED",relative,type(exc).__name__,str(exc)[:150],flush=True)
            return 1
    print("PYTHON_SUMMARY",total,flush=True)
    return 0


if __name__=="__main__":
    sys.exit(main())
