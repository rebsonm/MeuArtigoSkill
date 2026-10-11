#!/usr/bin/env python3
"""Offline preflight for a prepared research Skill archive.

The check never installs software or accesses user projects.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path, PurePosixPath
from zipfile import ZipFile,BadZipFile

MAX_FILES=3000
MAX_TOTAL=100*1024*1024

def diagnose(path:Path)->dict:
    base={"valid":False,"kind":"INVALID","reason":"","next_step":""}
    if not path.is_file():
        return {**base,"reason":"FILE_NOT_FOUND","next_step":"Select a ZIP that exists on your computer."}
    try:
        with ZipFile(path) as z:
            members=z.infolist()
            names=[i.filename for i in members if not i.is_dir()]
            if len(members)>MAX_FILES or sum(i.file_size for i in members)>MAX_TOTAL:
                raise ValueError("Archive too large")
            if len(names)!=len(set(names)) or any(
                i.filename.startswith("/") or "\\" in i.filename
                or ".." in PurePosixPath(i.filename).parts
                or (i.external_attr >> 16)&0o170000 == 0o120000
                for i in members
            ):
                raise ValueError("Unsafe archive")
            if z.testzip() is not None:
                raise BadZipFile("CRC")
            if "SKILL.md" in names:
                if not z.read("SKILL.md").startswith(b"---\n"):
                    return {**base,"kind":"SKILL","reason":"INVALID_ENTRYPOINT",
                            "next_step":"Download the published, prepared Skill archive."}
                return {**base,"kind":"SKILL","valid":True,"reason":"SKILL_READY",
                        "next_step":"Upload through a supported Skills import. Other services must be authorized separately."}
            dirs={n.split("/",1)[0] for n in names if "/" in n}
            if any(f"{n}/SKILL.md" in names for n in dirs):
                return {**base,"kind":"SOURCE_CHECKOUT","reason":"SOURCE_NOT_INSTALLER",
                        "next_step":"You used a source archive. Choose the prepared Skill ZIP on the GitHub Releases page."}
            return {**base,"kind":"UNKNOWN","reason":"NO_SKILL_ENTRYPOINT",
                    "next_step":"This archive does not contain SKILL.md at its root."}
    except (BadZipFile,OSError,ValueError,RuntimeError):
        return {**base,"reason":"INVALID_OR_UNSAFE_ZIP",
                "next_step":"Check and download a complete ZIP under 100 MB."}

def main(argv=None)->int:
    p=argparse.ArgumentParser(description="Check the structure of a Skill ZIP before import.")
    p.add_argument("archive",type=Path)
    p.add_argument("--json",action="store_true")
    args=p.parse_args(argv)
    info=diagnose(args.archive)
    if args.json: print(json.dumps(info,ensure_ascii=False,sort_keys=True))
    else:
        print(("READY" if info["valid"] else "NOT READY")+": "+info["kind"]+" ("+info["reason"]+")")
        print(info["next_step"])
    return 0 if info["valid"] else 2
if __name__=="__main__":
    raise SystemExit(main())
