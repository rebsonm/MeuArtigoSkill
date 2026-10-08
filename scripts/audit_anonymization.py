#!/usr/bin/env python3
"""Audit generated/shareable artifacts for anonymization leaks.

This is a release-control audit, not a guarantee of irreversible anonymity.
It scans visible text where readable, common OOXML metadata, filenames and
configured identity terms. PDF/image outputs always require explicit human
visual review because automated inspection can miss rasterized or embedded
content.
"""
from __future__ import annotations

import hashlib
import argparse
import json
import re
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

MGMT = "00_Gestao_e_Continuidade"
PROFILE_REL = Path(MGMT) / "ANONYMIZATION_PROFILE.json"
DEFAULT_OUT_REL = Path("06_Submissao") / "Anonimizacao"

TEXT_EXTS = {".md", ".txt", ".csv", ".json", ".yaml", ".yml", ".xml", ".html", ".htm", ".tex", ".rst"}
OOXML_EXTS = {".docx", ".xlsx", ".pptx", ".docm", ".xlsm", ".pptm"}
VISUAL_EXTS = {".pdf", ".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff", ".svg"}

GENERIC_PATTERNS = [
    ("EMAIL", re.compile(r"(?<![\w.+-])[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}(?![\w.-])", re.I), "HIGH"),
    ("ORCID", re.compile(r"\b\d{4}-\d{4}-\d{4}-\d{3}[\dX]\b", re.I), "HIGH"),
    ("CPF_LIKE", re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b"), "HIGH"),
    ("PHONE_BR", re.compile(r"(?<!\d)(?:\+?55\s*)?(?:\(?\d{2}\)?\s*)?9?\d{4}[-\s]?\d{4}(?!\d)"), "MEDIUM"),
    ("LOCAL_PATH_WINDOWS", re.compile(r"\b[A-Z]:\\(?:Users|Documents and Settings)\\[^\s<>\"']+", re.I), "HIGH"),
    ("LOCAL_PATH_MAC", re.compile(r"/Users/[^/\s]+/"), "HIGH"),
    ("LOCAL_PATH_LINUX", re.compile(r"/home/[^/\s]+/"), "HIGH"),
    ("PRIVATE_CLOUD_LINK", re.compile(r"https?://(?:drive|docs)\.google\.com/[^\s)\]>]+", re.I), "MEDIUM"),
]

PROFILE_SEVERITY = {
    "author_names": "MEDIUM",
    "name_variants": "MEDIUM",
    "emails": "HIGH",
    "orcids": "HIGH",
    "affiliations": "HIGH",
    "departments_units": "HIGH",
    "institutional_identifiers": "HIGH",
    "case_site_names": "MEDIUM",
    "participant_identifiers": "HIGH",
    "account_usernames": "HIGH",
    "local_path_tokens": "HIGH",
    "custom_terms": "MEDIUM",
}

def load_profile(root: Path) -> dict:
    path = root / PROFILE_REL
    if not path.exists():
        raise SystemExit(f"missing anonymization profile: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(f"invalid anonymization profile: {exc}")
    return data

def configured_terms(profile: dict) -> list[tuple[str, int, str, str]]:
    out = []
    groups = profile.get("sensitive_terms") or {}
    if not isinstance(groups, dict):
        return out
    for category, values in groups.items():
        if not isinstance(values, list):
            continue
        sev = PROFILE_SEVERITY.get(category, "MEDIUM")
        for idx, value in enumerate(values, 1):
            value = str(value or "").strip()
            if len(value) >= 3:
                out.append((category, idx, value, sev))
    return out

def add_finding(findings: list[dict], *, file: Path, kind: str, severity: str, location: str, token_label: str = ""):
    findings.append({
        "file": file.as_posix(),
        "kind": kind,
        "severity": severity,
        "location": location,
        "token_label": token_label,
    })

def scan_text(text: str, file: Path, findings: list[dict], terms, location: str = "content"):
    for kind, pattern, severity in GENERIC_PATTERNS:
        for _ in pattern.finditer(text):
            add_finding(findings, file=file, kind=kind, severity=severity, location=location)
    lowered = text.casefold()
    for category, idx, value, severity in terms:
        if value.casefold() in lowered:
            add_finding(
                findings,
                file=file,
                kind="PROFILE_TERM",
                severity=severity,
                location=location,
                token_label=f"{category}[{idx}]",
            )

def scan_filename(file: Path, findings: list[dict], terms):
    scan_text(file.name, file, findings, terms, location="filename")

def scan_ooxml(file: Path, findings: list[dict], terms, manual: list[dict]):
    try:
        with zipfile.ZipFile(file) as z:
            for name in z.namelist():
                if not (name.endswith(".xml") or name.endswith(".rels")):
                    continue
                raw = z.read(name)
                text = raw.decode("utf-8", errors="replace")
                scan_text(text, file, findings, terms, location=f"package:{name}")
                if name == "docProps/core.xml":
                    for tag in ("dc:creator", "cp:lastModifiedBy"):
                        m = re.search(rf"<{re.escape(tag)}[^>]*>(.*?)</{re.escape(tag)}>", text, re.I | re.S)
                        if m and re.sub(r"<[^>]+>", "", m.group(1)).strip():
                            add_finding(findings, file=file, kind="DOCUMENT_CREATOR_METADATA", severity="HIGH", location=name)
                if "comments" in name.lower():
                    if re.search(r"(?:w:author|author)=\"[^\"]+\"", text, re.I):
                        add_finding(findings, file=file, kind="COMMENT_AUTHOR_METADATA", severity="HIGH", location=name)
                if re.search(r"file://|target=\"(?:[A-Z]:\\|/Users/|/home/)", text, re.I):
                    add_finding(findings, file=file, kind="EMBEDDED_LOCAL_PATH", severity="HIGH", location=name)
    except Exception as exc:
        manual.append({"file": file.as_posix(), "reason": f"OOXML package could not be fully inspected: {exc}"})

def scan_pdf(file: Path, findings: list[dict], terms, manual: list[dict]):
    inspected = False
    try:
        from pypdf import PdfReader  # optional
        reader = PdfReader(str(file))
        metadata = reader.metadata or {}
        meta_text = "\n".join(f"{k}: {v}" for k, v in metadata.items() if v)
        if meta_text:
            scan_text(meta_text, file, findings, terms, location="pdf_metadata")
            for key in ("/Author", "/Creator"):
                if metadata.get(key):
                    add_finding(findings, file=file, kind="PDF_IDENTITY_METADATA", severity="HIGH", location=f"metadata:{key}")
        for i, page in enumerate(reader.pages, 1):
            text = page.extract_text() or ""
            scan_text(text, file, findings, terms, location=f"pdf_page:{i}")
        inspected = True
    except Exception:
        try:
            raw = file.read_bytes().decode("latin-1", errors="ignore")
            scan_text(raw, file, findings, terms, location="pdf_raw_bytes")
        except Exception:
            pass
    manual.append({
        "file": file.as_posix(),
        "reason": "PDF requires human visual review for rasterized/embedded identifiers even after automated inspection." if inspected else "PDF could not be fully text-extracted; human visual/metadata review is required.",
    })

def collect_targets(targets: list[str]) -> list[Path]:
    out = []
    for raw in targets:
        p = Path(raw).resolve()
        if p.is_file():
            out.append(p)
        elif p.is_dir():
            out.extend(x for x in p.rglob("*") if x.is_file())
    seen = set()
    unique = []
    for p in sorted(out):
        rp = p.resolve()
        if rp not in seen:
            seen.add(rp)
            unique.append(p)
    return unique

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("project", help="Canonical project root")
    ap.add_argument("targets", nargs="*", help="Files/directories to audit; defaults to 06_Submissao/Arquivos_Finais")
    ap.add_argument("--output-dir", default="", help="Audit report directory")
    ap.add_argument("--acknowledge-human-review", action="store_true", help="Record that required visual/medium-risk review was completed by a human")
    args = ap.parse_args()

    root = Path(args.project).resolve()
    profile = load_profile(root)
    terms = configured_terms(profile)
    targets = args.targets or [str(root / "06_Submissao" / "Arquivos_Finais")]
    files = collect_targets(targets)
    findings: list[dict] = []
    manual: list[dict] = []

    blocking_errors = []
    status = profile.get("status")
    if status not in {"VERIFIED", "NOT_REQUIRED"}:
        blocking_errors.append("Anonymization profile must be VERIFIED or NOT_REQUIRED.")
    if status == "NOT_REQUIRED" and not str(profile.get("notes") or "").strip():
        blocking_errors.append("NOT_REQUIRED requires a rationale.")
    if not files:
        blocking_errors.append("No outgoing files found.")
        manual.append({"file": "", "reason": "No outgoing files found in the requested audit scope."})

    fingerprints = []
    for file in files:
        try:
            relative = file.relative_to(root).as_posix()
            fingerprints.append({"path": relative, "sha256": hashlib.sha256(file.read_bytes()).hexdigest()})
        except (ValueError, OSError):
            blocking_errors.append("Audit files must be readable and inside the project.")
        scan_filename(file, findings, terms)
        ext = file.suffix.lower()
        if ext in TEXT_EXTS:
            try:
                scan_text(file.read_text(encoding="utf-8", errors="replace"), file, findings, terms)
            except Exception as exc:
                manual.append({"file": file.as_posix(), "reason": f"Text file could not be read: {exc}"})
        elif ext in OOXML_EXTS:
            scan_ooxml(file, findings, terms, manual)
        elif ext == ".pdf":
            scan_pdf(file, findings, terms, manual)
        elif ext in VISUAL_EXTS:
            manual.append({"file": file.as_posix(), "reason": "Visual/image artifact requires human inspection for visible identifiers and embedded metadata."})
        else:
            manual.append({"file": file.as_posix(), "reason": "Unsupported/binary format requires human inspection."})

    high = [f for f in findings if f["severity"] == "HIGH"]
    medium = [f for f in findings if f["severity"] == "MEDIUM"]

    if high or blocking_errors:
        result = "FAIL"
    elif (medium or manual) and not args.acknowledge_human_review:
        result = "REVIEW_REQUIRED"
    elif medium or manual:
        result = "PASS_WITH_HUMAN_REVIEW"
    else:
        result = "PASS"

    report = {
        "schema_version": "2.0",
        "blocking_errors": blocking_errors,
        "file_manifest": fingerprints,
        "profile_sha256": hashlib.sha256((root / PROFILE_REL).read_bytes()).hexdigest(),
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "project": root.name,
        "profile_status": profile.get("status", "TO_CONFIGURE"),
        "default_external_artifact_mode": profile.get("default_external_artifact_mode", "ANONYMIZED"),
        "audit_scope": [str(Path(t)) for t in targets],
        "files_scanned": len(files),
        "high_risk_findings": len(high),
        "medium_risk_findings": len(medium),
        "manual_review_items": len(manual),
        "human_review_acknowledged": bool(args.acknowledge_human_review),
        "result": result,
        "findings": findings,
        "manual_review": manual,
        "note": "Sensitive literal values are intentionally omitted from this report.",
    }

    outdir = Path(args.output_dir).resolve() if args.output_dir else root / DEFAULT_OUT_REL
    outdir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    out = outdir / f"ANONYMIZATION_AUDIT_{stamp}.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"anonymization_result={result}")
    print(f"files_scanned={len(files)}")
    print(f"high_risk_findings={len(high)}")
    print(f"medium_risk_findings={len(medium)}")
    print(f"manual_review_items={len(manual)}")
    print(f"report={out}")
    return 0 if result in {"PASS", "PASS_WITH_HUMAN_REVIEW"} else 1

if __name__ == "__main__":
    raise SystemExit(main())
