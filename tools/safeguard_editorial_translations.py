#!/usr/bin/env python3
"""Correct scientific-status corruption in machine-translated editorial cards.

Do NOT infer that editorial translation validates any source, license or claim.
Restore six previously verified translations from the main commit unchanged.
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]
LIB=ROOT/"knowledge/methodology"
ORIGINAL="9cf5b9ee91c0c0ade6c6d66316b26bde67cbe413"
PUBLISHED="fef0fe391b76709005c6b1ae6f64dcca7011e2f9"
SIX={"source-review-0259.md","source-review-0298.md",
     "yin-2018-case-study-design.md","suddaby-2006-grounded-theory-not.md",
     "zupic-cater-2015-bibliometric-methods.md",
     "donthu-2021-bibliometric-how-to.md"}
LEGACY="REVISÃO_CIENTÍFICA_INDEPENDENTE_PENDENTE"
BAD="== sync, corrected by elderman == @elder man"

def gitfile(revision,path):
    return subprocess.check_output(["git","show",f"{revision}:{path}"])

def hash_bytes(data):
    return hashlib.sha256(data).hexdigest()

def main():
    cat_path=LIB/"catalog.json"
    ledger_path=LIB/"intake/operational-validation.json"
    cat=json.loads(cat_path.read_text(encoding="utf-8"))
    ledger=json.loads(ledger_path.read_text(encoding="utf-8"))
    card_receipts={x["path"]:x for x in ledger["cards"]}
    repaired=0
    six_restored=0
    edits=[]
    for row in cat["documents"]:
        path=row["path"]
        file=ROOT/path
        if Path(path).name in SIX:
            new=gitfile(PUBLISHED,path).decode("utf-8")
            six_restored+=1
        elif row.get("translation_fidelity_status")=="MACHINE_TRANSLATED_REVIEW_PENDING":
            content=file.read_text(encoding="utf-8")
            baseline=gitfile(ORIGINAL,path).decode("utf-8")
            if BAD in content:
                content=content.replace(BAD,"DRAFT_NEEDS_INDEPENDENT_REVIEW — "+LEGACY)
                repaired+=1
            content=content.replace("before playing it","before reproducing or redistributing the work")
            content=content.replace("without playing it","without redistributing the work")
            content=content.replace("independent scientific opinion","independent scientific review")
            content=content.replace("not a card-tested procedure","not a scientifically validated procedure")
            # The exact inherited technical label is immutable documentation
            # of pending review, not a prose string for machine translation.
            if row.get("source_registry_id"):
                if LEGACY not in content:
                    content=content.rstrip()+f"\n\n- Technical pending-review identifier: {LEGACY}\n"
            if "DRAFT_NEEDS_INDEPENDENT_REVIEW" not in content:
                content=content.rstrip()+"\n\nEditorial status: DRAFT_NEEDS_INDEPENDENT_REVIEW\n"
            rights=row.get("underlying_source_rights_status","UNVERIFIED_FOR_PUBLICATION")
            status=f"Rights status: {rights}"
            if status not in content and rights=="UNVERIFIED_FOR_PUBLICATION":
                content=content.rstrip()+"\n\n"+status+"\n"
            if "## Translation and source-of-truth notice" not in content:
                content=content.rstrip()+"\n\n## Translation and source-of-truth notice\n\n"
                content+=(
                    "**MACHINE_TRANSLATED_REVIEW_PENDING:** This English editorial "
                    "draft is **not independently scientifically reviewed**. It "
                    "is NOT primary evidence [L], does not reproduce or authorize "
                    "the source PDF, and cannot approve a scientific gate. The "
                    "original Portuguese record prevails in any discrepancy, "
                    "including limitations, negation, methodological scope and rights.\n\n"
                    f"Original preserved editorial record: https://github.com/rebsonm/MeuArtigoSkill/blob/{ORIGINAL}/{path}\n\n"
                    f"Catalogue underlying-source rights: \x60{rights}\x60. "
                    "No republication rights or scientific validation are "
                    "established by this translation.\n"
                )
            old_doi=set(re.findall(r"10\.\d{4,9}/[A-Za-z0-9._;()/:-]+",baseline))
            new_doi=set(re.findall(r"10\.\d{4,9}/[A-Za-z0-9._;()/:-]+",content))
            if old_doi-new_doi:
                content=content.rstrip()+"\n\nSource DOI(s) as recorded in the original: "+", ".join(sorted(old_doi-new_doi))+"\n"
            new=content
        else:
            continue
        data=new.encode("utf-8")
        if len(data)>14000:
            raise ValueError("OVERSIZE: "+path)
        if Path(path).name in SIX:
            if row.get("translation_fidelity_status"):
                row.pop("translation_fidelity_status",None)
        else:
            if "[L]" not in new or not any(x in new for x in ("NOT primary evidence","NOT [L]","not independently")):
                raise ValueError("EVIDENCE_BOUNDARY_LOST: "+path)
        file.write_bytes(data)
        row["sha256"]=hash_bytes(data)
        card_receipts[path]["sha256"]=hash_bytes(data)
        edits.append(path)
    assert six_restored==6
    assert repaired>0
    cat_path.write_text(json.dumps(cat,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    ledger_path.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    info={"source_language":"pt","target_language":"en",
          "machine_translations_without_independent_review":len(edits)-6,
          "corrupted_status_markers_repaired":repaired,
          "six_reviewed_translations_preserved":six_restored,
          "scientific_approvals":0,"pdfs_published":0}
    Path("/tmp/editorial-safeguard.json").write_text(json.dumps(info,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(info))
if __name__=="__main__":
    main()
