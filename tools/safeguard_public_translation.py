#!/usr/bin/env python3
"""Repair machine-generated Markdown provenance without promoting scientific evidence.

The original Git commit is the authority for source-identifying and copyright
strings. Translation remains a draft, even if mechanical regression passes.
"""
import hashlib
import json
import re
import subprocess
from pathlib import Path

BASE_SHA = "9cf5b9ee91c0c0ade6c6d66316b26bde67cbe413"
ROOT=Path(__file__).resolve().parents[1]
LIB=ROOT/"knowledge/methodology"
CAT=LIB/"source_registry_catalog.json"
LEDGER=LIB/"intake/operational-validation.json"
GUARD="UNREVIEWED_PROSPECTING_CARD — [P] bibliographic metadata for consultation."
PROBLEM="== sync, corrected by elderman == @elder man"

def original(path):
    return subprocess.check_output(["git","show",f"{BASE_SHA}:{path}"],text=True)

def digest(body):
    return hashlib.sha256(body.encode("utf-8")).hexdigest()

def doi_tokens(text):
    return set(re.findall(r"10\.\d{4,9}/[A-Za-z0-9._;()/:-]+",text))

def run():
    reg=json.loads(CAT.read_text(encoding="utf-8"))
    op=json.loads(LEDGER.read_text(encoding="utf-8"))
    operational={x["path"]:x for x in op["cards"]}
    changed=[]
    flagged=[]
    corrections=0
    for row in reg["documents"]:
        if row.get("translation_fidelity_status") != "MACHINE_TRANSLATED_REVIEW_PENDING":
            continue
        path=row["path"]
        file=ROOT/path
        english=file.read_text(encoding="utf-8")
        baseline=original(path)
        assert GUARD in english, path
        assert row["source_id"] in english, path
        if PROBLEM in english:
            # Model output is not a scientific status or an authorised editor.
            english=english.replace(PROBLEM,"NOT_INDEPENDENTLY_SCIENTIFICALLY_REVIEWED")
            corrections+=1
        english=english.replace("before playing it","before reproducing or redistributing it")
        english=english.replace("permission to play it","permission to redistribute it")
        english=english.replace("without playing it","without redistributing it")
        english=english.replace("independent scientific opinion","independent scientific assessment")
        # Strong, unambiguous notices override any incorrect machine inference.
        if "## Translation and source-of-truth notice" not in english:
            english=english.rstrip()+"\n\n## Translation and source-of-truth notice\n\n"
            english+=(
                "**Status: MACHINE_TRANSLATED_REVIEW_PENDING.** "
                "This English text is an unreviewed machine-generated editorial aid. "
                "It is **not** a verified translation, independent critical appraisal, "
                "direct source evidence [L], or scientific approval. "
                "The bibliographic metadata and original Portuguese card prevail "
                "in any discrepancy. The author's published title is deliberately "
                "preserved in its original language.\n\n"
                f"Original preserved record: https://github.com/rebsonm/MeuArtigoSkill/blob/{BASE_SHA}/{path}\n\n"
                f"Authoritative rights-review state: \x60{row['rights_review']}\x60; "
                f"authorised open PDF in this catalogue: \x60{str(row['has_original_public_pdf']).lower()}\x60. "
                "No rights or approval are conferred by this machine translation.\n"
            )
        if "UNREVIEWED_PROSPECTING_CARD" not in english or "[P]" not in english:
            raise ValueError("BIBLIOGRAPHY_GRADE_LOST: "+path)
        if row["source_id"] not in english:
            raise ValueError("SOURCE_ID_LOST: "+path)
        # Do not conceal loss of explicit DOI in a machine-generated draft.
        missing=doi_tokens(baseline)-doi_tokens(english)
        if missing:
            flagged.append({"path":path,"missing_doi":sorted(missing)})
            english=english.rstrip()+"\n\nDOI(s) transcribed from authoritative original record: "+", ".join(sorted(missing))+"\n"
        if english!=file.read_text(encoding="utf-8"):
            file.write_text(english,encoding="utf-8")
        if len(english.encode("utf-8"))>14000:
            raise ValueError("MAX_CARD_SIZE_EXCEEDED: "+path)
        row["sha256"]=digest(english)
        operational[path]["sha256"]=row["sha256"]
        changed.append(path)
    assert len(changed)>=400, f"UNEXPECTED_TRANSLATED_CARD_COUNT:{len(changed)}"
    CAT.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    LEDGER.write_text(json.dumps(op,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    report={"batch":"machine-translated bibliographic cards","updated":len(changed),
            "machine_status_repairs":corrections,"missing_original_doi_restored":flagged,
            "fidelity_independently_verified":False,"scientific_gates_changed":0,
            "original_source_commit":BASE_SHA}
    Path("/tmp/source-card-translation-sanitization.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({"updated":len(changed),"machine_status_repairs":corrections,"missing_doi_restored":len(flagged)}))

if __name__=="__main__":
    run()
