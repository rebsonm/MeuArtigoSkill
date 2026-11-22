#!/usr/bin/env python3
"""Offline English translation of public bibliography prospecting cards.

Academic titles, DOI, technical tokens, and rights are preserved. The output
requires human fidelity review and never approves scientific [L]/[I] or gates.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "knowledge/methodology"
PT = re.compile(r"\b(?:não|pesquisa|revisão|análise|metodologia|fontes?|"
                r"evidência|conferir|verificar|pesquisador|direitos|edição|escopo|"
                r"leitura|proposta|estudo|dados|orientação|limites?|resultados?|"
                r"publicação|documental|contribuição|identidade|observada|"
                r"condições|perguntas?|trabalho|nenhum|nenhuma|aprovada|"
                r"pendente|científic[ao]|autoria|título|autores|antes|qualquer|como|sem|com|para|da|dos|das|na|por|seu|suas|seus|uma|quando|que|ainda|fonte|provas)\b", re.I)
KEEP = re.compile(r"(\x60[^\x60]+\x60|\[[LIP]\]|\b(?:SRC|EC|GATE|TRACE|DEC|IB)-\d+\b|"
                  r"https?://[^\s)\]>]+|\b10\.\d{4,9}/[^\s)]+|"
                  r"\[[^\]]+\]\([^)]+\))")
TITLES = re.compile(r"^(\s*[-*]\s*)(?:Título[^:]*|Obra|Fonte bibliográfica|"
                    r"Bibliographic source)\s*:\s*(.*)$", re.I)
HEADER = ("UNREVIEWED_PROSPECTING_CARD — [P] bibliographic metadata for consultation.\n"
          "This is NOT an [I] synthesis of a source reading or [L] scientific evidence.\n"
          "The guidance is original editorial text; do not attribute its questions "
          "to the source authors.\n\n")

def read(p):
    return json.loads(p.read_text(encoding="utf-8"))

def sha(data):
    return hashlib.sha256(data).hexdigest()

def translate_piece(s, model):
    t = s.strip()
    if len(t) < 4 or not any(c.isalpha() for c in t):
        return s
    flagged = bool(PT.search(t))
    if not flagged and len(t) > 32:
        import langid
        language, confidence = langid.classify(t)
        flagged = language == "pt" and confidence > 0
    if not flagged:
        return s
    translated = model.translate(t)
    if not translated or len(translated) < max(2, len(t)//6):
        return s
    left = s[:len(s)-len(s.lstrip())]
    right = s[len(s.rstrip()):]
    return left + translated + right

def translate_line(line, model):
    if not line.strip() or line.lstrip().startswith(("<", "~" * 3, chr(96) * 3)):
        return line
    m = TITLES.match(line)
    if m:
        return m.group(1) + "Original published title: " + m.group(2)
    head = re.match(r"^(\s*(?:#{1,6}\s+|[-*>]\s+|\d+\.\s+)?)(.*)$", line)
    prefix, body = head.groups()
    # Preserve exact source values, but translate short recurring metadata labels.
    for old, new in (
        ("Ano:", "Year:"), ("Autor:", "Author:"), ("Autoria:", "Authorship:"),
        ("Autores:", "Authors:"), ("Tipo de material:", "Material type:"),
        ("DOI:", "DOI:"), ("Localizador editorial:", "Publisher locator:"),
        ("Conferência efetiva:", "Verification performed:"),
        ("Status científico:", "Scientific status:"),
        ("Natureza:", "Nature:"), ("Registro:", "Record:"),
        ("Grau de evidência:", "Evidence grade:"),
    ):
        if body.startswith(old):
            body = new + body[len(old):]
            break
    pieces = KEEP.split(body)
    for i in range(0, len(pieces), 2):
        pieces[i] = translate_piece(pieces[i], model)
    outcome = prefix + "".join(pieces)
    if sorted(KEEP.findall(line)) != sorted(KEEP.findall(outcome)):
        return line
    return outcome

def translate_card(original, model):
    if original.startswith(("FICHA_DE_PROSPECÇÃO_NÃO_REVISADA",
                            "UNREVIEWED_PROSPECTING_CARD")):
        parts = original.split("\n\n", 1)
        if len(parts) == 2:
            original = parts[1]
    output, code = [], False
    for raw in original.splitlines(keepends=True):
        end = "\n" if raw.endswith("\n") else ""
        line = raw[:-1] if end else raw
        if line.lstrip().startswith((chr(96)*3, "~"*3)):
            code = not code
        output.append((line if code else translate_line(line, model)) + end)
    return HEADER + "".join(output).replace(
        "FICHA_DE_PROSPECÇÃO_NÃO_REVISADA", "UNREVIEWED_PROSPECTING_CARD")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--limit", type=int, default=12)
    p.add_argument("--report", required=True)
    a = p.parse_args()
    if not 1 <= a.limit <= 475:
        raise ValueError("INVALID_LIMIT")
    registry_path = LIB / "source_registry_catalog.json"
    report_path = LIB / "intake/operational-validation.json"
    registry, ledger = read(registry_path), read(report_path)
    index = {x["path"]: x for x in registry["documents"]}
    state = {x["path"]: x for x in ledger["cards"]}
    banned = {next(x["path"] for x in registry["documents"]
                   if x["source_id"] == "SRC-0385")}
    candidates = [p for p in sorted((LIB/"source_cards").glob("*.md"))
                  if p.relative_to(ROOT).as_posix() not in banned
                  and p.relative_to(ROOT).as_posix() in index
                  and index[p.relative_to(ROOT).as_posix()].get("translation_fidelity_status") != "MACHINE_TRANSLATED_REVIEW_PENDING"
                  and PT.search(p.read_text(encoding="utf-8"))]
    from argostranslate import package, translate
    package.update_package_index()
    models = [x for x in package.get_available_packages()
              if x.from_code in ("pt", "pb") and x.to_code == "en"]
    if not models:
        raise RuntimeError("OFFLINE_PORTUGUESE_TO_ENGLISH_MODEL_UNAVAILABLE")
    models.sort(key=lambda x: x.from_code != "pt")
    selected = models[0]
    package.install_from_path(selected.download())
    engine = translate.get_translation_from_codes(selected.from_code, "en")
    changes = []
    for item in candidates[:a.limit]:
        path = item.relative_to(ROOT).as_posix()
        old = item.read_bytes()
        new = translate_card(old.decode("utf-8"), engine).encode("utf-8")
        ids = re.findall(r"\b(?:SRC|EC|GATE|TRACE)-\d+\b", old.decode("utf-8"))
        if new == old or len(new)>14000 or not all(i.encode() in new for i in ids):
            continue
        if b"[P]" not in new:
            continue
        if path not in index or path not in state:
            raise ValueError("MISSING_CARD_LEDGER_ENTRY")
        item.write_bytes(new)
        index[path]["sha256"] = sha(new)
        state[path]["sha256"] = sha(new)
        index[path]["translation_fidelity_status"] = "MACHINE_TRANSLATED_REVIEW_PENDING"
        changes.append({"path":path,"before":sha(old),"after":sha(new)})
        print("TRANSLATED", path, flush=True)
    if changes:
        for target, data in ((registry_path, registry),(report_path,ledger)):
            target.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",
                              encoding="utf-8")
    result = {"mode":"OFFLINE_MACHINE_TRANSLATION_NOT_SCIENTIFIC_REVIEW",
              "model_from":selected.from_code,"model_to":"en",
              "selected":min(len(candidates),a.limit),"changed":changes,
              "human_fidelity_review":False,"scientific_gates_changed":False}
    Path(a.report).write_text(json.dumps(result,ensure_ascii=False,indent=2),
                              encoding="utf-8")
    print(json.dumps({"changed":len(changes)}))
    if not changes:
        raise SystemExit("NO_TRANSLATION_CHANGE")

if __name__ == "__main__":
    main()
