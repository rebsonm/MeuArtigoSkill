#!/usr/bin/env python3
"""Check local Markdown links and headings without external network access."""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

MD_LINK = re.compile(r'!?\[[^\]]*\]\(\s*(<[^>]*>|[^\s)]+)(?:\s+["\'][^"\']*["\'])?\s*\)')
REF_LINK = re.compile(r'^\s*\[[^\]]+\]:\s*(<[^>]*>|\S+)',re.M)
HEADING = re.compile(r'^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$')
INLINE_CODE = re.compile(r'(?<!\x60)\x60[^\x60\n]+\x60')
HTML_LINK = re.compile(r'<(?:img|a)\b[^>]*(?:src|href)=["\']([^"\']+)["\']',re.I)
FENCE = re.compile(r'^\s*(\x60{3}|~~~)')


def slugify(value):
    value=re.sub(r'<[^>]*>', '', value)
    value=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',value)
    value=value.replace(chr(96),'').lower()
    value=re.sub(r'[^\w \t-]', '',value,flags=re.U)
    return re.sub(r'[ \t]+','-',value.strip())


def anchors(markdown):
    used={}
    result=set()
    fenced=False
    for line in markdown.splitlines():
        if FENCE.match(line):
            fenced=not fenced
            continue
        if fenced: continue
        m=HEADING.match(line)
        if m:
            title=slugify(m.group(1))
            idx=used.get(title,0)
            result.add(title if idx==0 else f"{title}-{idx}")
            used[title]=idx+1
        for a in re.findall(r'<a\s+[^>]*id=["\']([^"\']+)["\']',line,re.I):
            result.add(a)
    return result


def targets(content):
    fenced=False
    for line_no,line in enumerate(content.splitlines(),1):
        if FENCE.match(line):
            fenced=not fenced
            continue
        if fenced: continue
        line=INLINE_CODE.sub('',line)
        for m in MD_LINK.finditer(line):
            yield line_no,m.group(1).strip('<>')
        m=REF_LINK.match(line)
        if m: yield line_no,m.group(1).strip('<>')
        for m in HTML_LINK.finditer(line):
            yield line_no,m.group(1)


def inspect(root,scopes=("README.md","docs","references","SKILL.md",
                         "CONTRIBUTING.md","SECURITY.md","CHANGELOG.md")):
    root=Path(root).resolve()
    docs=[]
    problems=[]
    checked=0
    for scope in scopes:
        where=root/scope
        if where.is_file(): docs.append(where)
        elif where.is_dir(): docs.extend(sorted(where.rglob("*.md")))
    heading_cache={}
    for file in sorted(set(docs)):
        if file.is_symlink():
            problems.append(f"{file.relative_to(root)}: symlinked source document")
            continue
        for line,link_text in targets(file.read_text(encoding="utf-8")):
            if not link_text or link_text.startswith(("mailto:","tel:","data:","//")):
                continue
            item=urlsplit(link_text)
            if item.scheme:
                continue
            checked+=1
            path=unquote(item.path).replace(chr(92),'/')
            if not path and item.fragment:
                dest=file
            elif path.startswith('/'):
                dest=root/path.lstrip('/')
            else:
                dest=file.parent/path
            dest=dest.resolve()
            where=f"{file.relative_to(root)}:{line} {link_text}"
            if not dest.is_relative_to(root):
                problems.append(f"{where}: link escapes repository")
            elif not dest.exists():
                problems.append(f"{where}: destination missing")
            elif item.fragment and dest.suffix.lower()==".md":
                if dest not in heading_cache:
                    heading_cache[dest]=anchors(dest.read_text(encoding="utf-8"))
                if unquote(item.fragment) not in heading_cache[dest]:
                    problems.append(f"{where}: heading not found")
    return {"checked":checked,"errors":problems,"documents":len(set(docs))}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo",default=str(Path(__file__).resolve().parents[1]))
    args=p.parse_args(argv)
    result=inspect(Path(args.repo))
    print(f"documentation_files={result['documents']}")
    print(f"local_links_checked={result['checked']}")
    for error in result["errors"]: print("ERROR:",error)
    print(f"link_errors={len(result['errors'])}")
    return 1 if result["errors"] else 0


if __name__=="__main__":
    raise SystemExit(main())
