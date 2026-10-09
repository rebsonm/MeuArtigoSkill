#!/usr/bin/env python3
"""One-time translation of PUBLIC repository Markdown from Portuguese to English.

Never run on workspaces, uploads, external literature or private documents.
Preserve code, citations, existing identifiers, links and old section anchors.
Machine translation is an editorial first pass, not scientific verification.
"""
from __future__ import annotations
import argparse
import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from audit_source_language import PORTUGUESE_WORDS
from check_documentation_links import slugify

EXCLUDED={"SKILL.md","README.md","docs/ENGLISH-SOURCE-MIGRATION.md",
          "docs/RELEASE-CANDIDATE-v0.9.0-beta.1.md"}
PRESERVE=[
    re.compile(r'(?ms)^\x60{3}.*?^\x60{3}[^\n]*(?:\n|$)'),
    re.compile(r'(?ms)^~~~.*?^~~~[^\n]*(?:\n|$)'),
    re.compile(r'(?m)^ {4,}.*$'),
    re.compile(r'\x60[^\x60\n]+\x60'),
    re.compile(r'(?m)^ *- [A-Z][A-ZÁ-ÚÀ-Ü0-9 ,.;&()\-]+(?:et al\.)? .*https?://(?:doi\.org/|www\.)[^\n]*$'),
    re.compile(r'\]\((?:https?://|\.?\.?/|#)[^)\s]+\)'),
    re.compile(r'https?://[^\s)<>"\x60]+'),
    re.compile(r'<a\s+id="[^"]+"></a>'),
    re.compile(r'\$[^$\n]+\$'),
]


def protect(text):
    locked=[]
    for patt in PRESERVE:
        def callback(m):
            token=f"ZXQLOCK{len(locked):05d}ZXQ"
            locked.append(m.group(0))
            return token
        text=patt.sub(callback,text)
    return text,locked


def restore(text,locked):
    for i,content in enumerate(locked):
        token=f"ZXQLOCK{i:05d}ZXQ"
        if text.count(token)!=1:
            raise RuntimeError(f"source token was damaged: {i}")
        text=text.replace(token,content)
    if re.search(r'ZXQLOCK\d+ZXQ',text):
        raise RuntimeError("unexpected translation sentinel")
    return text


def legacy_heading_anchors(text):
    used={}
    out=[]
    in_fence=False
    for line in text.splitlines(keepends=True):
        if re.match(r'^\s*(\x60{3}|~~~)',line):
            in_fence=not in_fence
        m=re.match(r'^(#{1,6})\s+(.+?)\s*#*\s*$',line.rstrip("\r\n"))
        if not in_fence and m:
            slug=slugify(m.group(2))
            idx=used.get(slug,0)
            used[slug]=idx+1
            original_slug=slug if idx==0 else f"{slug}-{idx}"
            if original_slug:
                out.append(f'<a id="{html.escape(original_slug,quote=True)}"></a>\n')
        out.append(line)
    return "".join(out)


def chunks(text,limit=3900):
    paragraphs=re.split(r'(\n\n+)',text)
    pieces=[]
    for part in paragraphs:
        if len(part)<=limit:
            pieces.append(part)
        else:
            lines=part.splitlines(keepends=True)
            piece=""
            for line in lines:
                if len(piece)+len(line)>limit and piece:
                    pieces.append(piece);piece=""
                if len(line)>limit:
                    while len(line)>limit:
                        pos=line.rfind(" ",0,limit)
                        if pos<limit//2:pos=limit
                        pieces.append(line[:pos])
                        line=line[pos:]
                piece+=line
            if piece:pieces.append(piece)
    result=[]
    current=""
    for part in pieces:
        if len(current)+len(part)>limit and current:
            result.append(current);current=""
        current+=part
    if current:result.append(current)
    return result


def google_translate(text,retries=5):
    if not text.strip() or not PORTUGUESE_WORDS.search(text):
        return text
    params=urllib.parse.urlencode({"client":"gtx","sl":"pt","tl":"en","dt":"t","q":text})
    url="https://translate.googleapis.com/translate_a/single?"+params
    for attempt in range(retries):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
            with urllib.request.urlopen(req,timeout=45) as response:
                raw=json.loads(response.read().decode("utf-8"))
            output="".join(str(i[0] or "") for i in raw[0])
            if not output.strip():
                raise ValueError("empty translation")
            return output
        except Exception:
            if attempt==retries-1:raise
            time.sleep(min(14,1.5*(attempt+1)**2))
    raise RuntimeError("unavailable translation endpoint")


def run(max_files=0):
    files=[p for p in sorted(ROOT.rglob("*.md"))
           if not any(s in {".git","dist","__pycache__","tests","benchmarks"} for s in p.parts)
           and p.relative_to(ROOT).as_posix() not in EXCLUDED]
    edited=[];failed=[];skipped=[]
    for file in files:
        original=file.read_text(encoding="utf-8")
        hits=len(PORTUGUESE_WORDS.findall(original))
        if hits<4:
            skipped.append(file.relative_to(ROOT).as_posix());continue
        try:
            masked,locked=protect(legacy_heading_anchors(original))
            translated=[]
            for part in chunks(masked):
                translated.append(google_translate(part))
                time.sleep(0.12)
            result=restore("".join(translated),locked)
            if result.count(chr(96)*3)!=original.count(chr(96)*3):
                raise RuntimeError("fenced code delimiters were altered")
            if not result.strip():
                raise RuntimeError("empty translated document")
            if result!=original:
                file.write_text(result,encoding="utf-8")
                edited.append(file.relative_to(ROOT).as_posix())
            print("TRANSLATED",file.relative_to(ROOT).as_posix(),"original_indicators",hits,flush=True)
        except Exception as exc:
            failed.append({"file":file.relative_to(ROOT).as_posix(),"reason":str(exc)[:150]})
            print("FAILED",file.relative_to(ROOT).as_posix(),str(exc)[:100],flush=True)
        if max_files and len(edited)>=max_files:break
    print("TRANSLATION_SUMMARY",json.dumps({"translated":len(edited),"skipped":len(skipped),"failed":failed},ensure_ascii=False),flush=True)
    return 1 if failed else 0


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--max-files",type=int,default=0)
    args=p.parse_args()
    sys.exit(run(args.max_files))
