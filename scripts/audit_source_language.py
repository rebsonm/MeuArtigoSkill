#!/usr/bin/env python3
"""Conservative signal for Portuguese prose still present in English-first source.

A heuristic language audit is an inventory, not a translator or evidence of
semantic equivalence. The default inspection does not print source excerpts.
Release strict mode fails when substantial untranslated prose remains.
Original bibliographic titles, proper names and deliberately multilingual
fixtures may need documented editorial handling before publication.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
# Prefer distinctive phrases to avoid confusing Latin-language bibliography,
# surnames, isolated technical tokens and the product's Portuguese proper name.
PORTUGUESE_WORDS=re.compile(
    r"\b(?:não|você|vocês|também|portanto|entretanto|pesquisador(?:es)?|"
    r"pesquisa(?:s)?|científic[oa]s?|bibliográfic[oa]s?|revisão|"
    r"arquivo(?:s)?|documentação|informações|orientações|"
    r"ferramenta(?:s)?|quando|somente|etapa(?:s)?|"
    r"fontes|fonte|análise|evidência(?:s)?|"
    r"utiliza(?:r|ção)|verificar|verificação|"
    r"responsabilidade|necessário|metodologia|"
    r"procedimento(?:s)?|perguntas|respostas|"
    r"conclusão|projeto(?:s)?|"
    r"atualização|alterações|realizada(?:s)?|"
    r"executada(?:s)?|construção|processo(?:s)?|"
    r"disponível|permitido|relatório(?:s)?|"
    r"instruções|autorização|resultado(?:s)?|"
    r"apresenta(?:r|ção)|criado(?:s)?|geração|"
    r"aprovad[oa]s?|pendente(?:s)?)\b",re.I
)
SUFFIXES={".md",".yaml",".yml",".py",".json",".cff"}
OMIT={"LICENSE","NOTICE"}


def scoped_files(root: Path) -> list[Path]:
    root=Path(root)
    files=[]
    for path in root.rglob("*"):
        if not path.is_file() or path.is_symlink() or path.name in OMIT:
            continue
        rel=path.relative_to(root)
        # The scanner stores Portuguese trigger words as DATA, not untranslated UI/source prose.
        if rel.as_posix() == "scripts/audit_source_language.py":
            continue
        if any(part.startswith(".") and part not in {".github"} for part in rel.parts):
            continue
        if any(part in {"dist","__pycache__",".git","assets","tests","benchmarks"} for part in rel.parts):
            # Test fixtures and benchmark scenarios may intentionally contain
            # user language examples, and are reviewed separately.
            continue
        if path.suffix.lower() not in SUFFIXES:
            continue
        files.append(path)
    return sorted(files)


def audit(root: Path) -> dict:
    root=Path(root).resolve()
    unresolved=[]
    unreadable=[]
    scanned=0
    for path in scoped_files(root):
        scanned+=1
        try:
            content=path.read_text(encoding="utf-8")
        except (OSError,UnicodeError):
            unreadable.append(path.relative_to(root).as_posix())
            continue
        # Preserve backwards-compatible anchor IDs as opaque technical keys.
        # They are URL identifiers from historical Portuguese headings,
        # not user-visible prose in the English documentation.
        if path.suffix.lower()==".md":
            content=re.sub(r'(?m)^\\s*<a\\s+id="[^"]+"></a>\\s*
        # A few Portuguese source titles or user-language examples are fine.
        threshold=7 if path.suffix.lower()==".md" else 12
        if len(words)>=threshold:
            unresolved.append({
                "path":path.relative_to(root).as_posix(),
                "portuguese_indicators":len(words),
            })
    return {
        "source_files_scanned":scanned,
        "source_files_requiring_editorial_language_review":len(unresolved),
        "unresolved":sorted(unresolved,key=lambda f:(-f["portuguese_indicators"],f["path"])),
        "unreadable":unreadable,
        "all_source_translated_verified":False,
        "method":"non-exhaustive Portuguese indicator scan; human editorial review also required",
    }


def main(argv=None) -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo",default=str(ROOT))
    p.add_argument("--strict",action="store_true")
    args=p.parse_args(argv)
    result=audit(Path(args.repo))
    print(json.dumps(result,indent=2,ensure_ascii=False))
    if result["unreadable"]:
        return 1
    if args.strict and result["unresolved"]:
        return 2
    return 0


if __name__=="__main__":
    raise SystemExit(main())
, "", content)
        words=PORTUGUESE_WORDS.findall(content)
        # A few Portuguese source titles or user-language examples are fine.
        threshold=7 if path.suffix.lower()==".md" else 12
        if len(words)>=threshold:
            unresolved.append({
                "path":path.relative_to(root).as_posix(),
                "portuguese_indicators":len(words),
            })
    return {
        "source_files_scanned":scanned,
        "source_files_requiring_editorial_language_review":len(unresolved),
        "unresolved":sorted(unresolved,key=lambda f:(-f["portuguese_indicators"],f["path"])),
        "unreadable":unreadable,
        "all_source_translated_verified":False,
        "method":"non-exhaustive Portuguese indicator scan; human editorial review also required",
    }


def main(argv=None) -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo",default=str(ROOT))
    p.add_argument("--strict",action="store_true")
    args=p.parse_args(argv)
    result=audit(Path(args.repo))
    print(json.dumps(result,indent=2,ensure_ascii=False))
    if result["unreadable"]:
        return 1
    if args.strict and result["unresolved"]:
        return 2
    return 0


if __name__=="__main__":
    raise SystemExit(main())
