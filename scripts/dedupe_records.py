#!/usr/bin/env python3
"""Conservatively consolidate bibliographic exports.

Exact DOI/title duplicates are consolidated. Fuzzy title matches are only flagged
for manual/agent audit and are never removed automatically.

Supported input: CSV, TSV/TXT, XLSX (XLSX requires openpyxl).
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

ALIASES = {
    "title": ["title", "article title", "document title", "ti", "paper title", "work title", "dc.title"],
    "doi": ["doi", "digital object identifier", "di", "doi url", "doi_url"],
    "authors": ["authors", "author", "author full names", "au", "author names", "creators", "creator"],
    "year": ["year", "publication year", "publication_year", "py", "published year", "publication date", "date"],
    "stable_id": ["openalex_id", "openalex id", "pmid", "pubmed id", "arxiv_id", "arxiv id"],
    "version": ["version", "version id", "version_id", "edition", "publication version"],
    "record_id": ["record_id", "record id"],
    "search_id": ["search_id", "search id"],
}
DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$", re.I)
# Preserve results from earlier attempts: require a new output folder for each run.
# Never overwrite or leave stale canonical files looking like the latest import.
GENERATED_OUTPUT_FILES = (
    "import_diagnostics.json", "rejected_records.csv",
    "consolidated_exact_dedup.csv", "exact_duplicate_audit.csv",
    "near_duplicate_review.csv", "import_sources_manifest.json",
)


def sha256_stream(path: Path) -> str:
    """Content fingerprint for a *single invocation*, not a persistent source ID."""
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


class HeaderValidationError(ValueError):
    """Ambiguous input headers, with untouched positional rows for quarantine."""

    def __init__(self, reason: str, columns: list[str]):
        super().__init__(reason)
        self.reason = reason
        self.columns = columns
        self.rows: list[list] = []


def validate_headers(headers: list[str]) -> None:
    """Check all column headings before any dict can discard repeated keys."""
    normalized = [norm_header(h) for h in headers]
    if any(not h for h in normalized):
        raise HeaderValidationError(
            "EMPTY_HEADER", [f"column_{i + 1}" for i, h in enumerate(normalized) if not h]
        )

    by_name: dict[str, list[str]] = {}
    for original, key in zip(headers, normalized):
        by_name.setdefault(key, []).append(original)
    repeated = [value for names in by_name.values() if len(names) > 1 for value in names]
    if repeated:
        raise HeaderValidationError("DUPLICATE_HEADER", repeated)

    for aliases in ALIASES.values():
        matching = [h for h, normalized_h in zip(headers, normalized)
                    if normalized_h in aliases]
        if len(matching) > 1:
            raise HeaderValidationError("AMBIGUOUS_BIBLIOGRAPHIC_HEADERS", matching)


def norm_header(s: str) -> str:
    return re.sub(r"\s+", " ", str(s or "").strip().lower())


def pick(row: dict[str, str], key: str) -> str:
    mapped = {norm_header(k): (v or "") for k, v in row.items()}
    for alias in ALIASES[key]:
        if alias in mapped and str(mapped[alias]).strip():
            return str(mapped[alias]).strip()
    return ""


def norm_doi(value: str) -> str:
    s = str(value or "").strip().lower()
    s = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", s)
    s = re.sub(r"^doi:\s*", "", s)
    s = s.strip().rstrip(".,;)")
    return s if DOI_RE.match(s) else ""


def norm_title(value: str) -> str:
    s = unicodedata.normalize("NFKC", str(value or "")).casefold()
    s = "".join(c if c.isalnum() else " " for c in s)
    return re.sub(r"\s+", " ", s).strip()


def first_author(value: str) -> str:
    s = unicodedata.normalize("NFKC", str(value or "")).casefold()
    s = re.split(r";|\band\b|\|", s)[0]
    return "".join(c for c in s if c.isalpha())


def normal_year(value: str) -> str:
    m = re.search(r"(?<!\d)((?:19|20)\d{2})(?!\d)", str(value or ""))
    return m.group(1) if m else ""


def normal_stable_id(value: str) -> str:
    """Only clearly recognizable persistent identifiers establish identity."""
    raw = str(value or "").strip()
    if re.fullmatch(r"W\d{5,}", raw, re.I):
        return "openalex:" + raw.upper()
    if re.fullmatch(r"\d{4,10}", raw):
        return "pmid:" + raw
    if re.fullmatch(r"\d{4}\.\d{4,5}(?:v\d+)?", raw):
        return "arxiv:" + raw.lower()
    return ""


def identity_reason(row: dict[str, str]) -> str:
    """Return empty on reliable bibliographic identity, otherwise a reason."""
    doi = norm_doi(pick(row, "doi"))
    title = norm_title(pick(row, "title"))
    author = first_author(pick(row, "authors"))
    year = normal_year(pick(row, "year"))
    stable_id = normal_stable_id(pick(row, "stable_id"))
    if doi or (title and author and year) or (title and stable_id):
        return ""
    return "MISSING_BIBLIOGRAPHIC_IDENTITY"


def available_schema(headers: list[str]) -> bool:
    found = {norm_header(h) for h in headers}
    has = lambda field: bool(found.intersection(ALIASES[field]))
    return has("doi") or (has("title") and has("authors") and has("year")) or (has("title") and has("stable_id"))


def identifier_list(row: dict[str, str], key: str) -> str:
    return pick(row, key)


def append_distinct(previous: str, new: str) -> str:
    values = [x for x in previous.split(";") if x]
    for v in new.split(";"):
        v = v.strip()
        if v and v not in values:
            values.append(v)
    return ";".join(values)


def read_tabular(path: Path) -> list[dict[str, str]]:
    suffix = path.suffix.lower()
    if suffix == ".xlsx":
        try:
            from openpyxl import load_workbook
        except ImportError as e:
            raise SystemExit("XLSX input requires openpyxl; convert to CSV or install openpyxl.") from e
        wb = load_workbook(path, read_only=True, data_only=True)
        try:
            ws = wb.active
            rows = ws.iter_rows(values_only=True)
            headers = [str(x) if x is not None else "" for x in next(rows)]
            try:
                validate_headers(headers)
            except HeaderValidationError as exc:
                exc.rows = [list(vals) for vals in rows]
                raise
            return [{headers[i]: "" if v is None else str(v)
                     for i, v in enumerate(vals)} for vals in rows]
        finally:
            wb.close()

    delimiter = "\t" if suffix in {".tsv", ".txt"} else ","
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        sample = f.read(4096); f.seek(0)
        try:
            delimiter = csv.Sniffer().sniff(sample, delimiters=",\t;").delimiter
        except csv.Error:
            pass
        reader = csv.DictReader(f, delimiter=delimiter)
        if reader.fieldnames is not None:
            try:
                validate_headers(reader.fieldnames)
            except HeaderValidationError as exc:
                # DictReader silently overwrites repeated keys; re-read
                # positional cells to retain every original column.
                f.seek(0)
                positional = csv.reader(f, delimiter=delimiter)
                next(positional, None)
                exc.rows = list(positional)
                raise
        return list(reader)


def safe_spreadsheet_cell(value: str) -> str:
    """Prevent imported metadata from becoming an Excel/Calc formula.

    Use only when writing user-facing CSV; normalization and comparisons retain
    the original content. Keep original inputs as the audit source of truth.
    """
    text = str(value or "")
    if text.lstrip()[:1] in ("=", "+", "-", "@", "\t", "\r", "\n"):
        return "'" + text
    return text


def write_safe_rows(writer: csv.DictWriter, records: list[dict[str, str]]) -> None:
    writer.writerows([
        {field: safe_spreadsheet_cell(row.get(field, "")) for field in writer.fieldnames}
        for row in records
    ])


def main() -> int:
    ap = argparse.ArgumentParser(description="Conservative, schema-validated bibliographic consolidation.")
    ap.add_argument("inputs", nargs="+", help="Bibliographic CSV/TSV/XLSX exports")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--fuzzy-threshold", type=float, default=0.94)
    args = ap.parse_args()

    if not (0 < args.fuzzy_threshold <= 1):
        ap.error("--fuzzy-threshold must be between 0 and 1")
    out = Path(args.out_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    # Exclusive directory creation is atomic across competing processes.
    # If the process is interrupted, the marker remains as a fail-closed signal.
    lock = out / ".dedupe_import_in_progress"
    try:
        lock.mkdir()
    except FileExistsError:
        print(
            "ERROR: OUTPUT_DIRECTORY_LOCKED; another import is running or "
            "an earlier attempt was interrupted. Inspect its outputs and "
            "choose a new --out-dir.",
            file=__import__("sys").stderr,
        )
        return 2
    try:
        return run_import(out, args)
    finally:
        lock.rmdir()


def run_import(out: Path, args: argparse.Namespace) -> int:
    if any((out / name).exists() or (out / name).is_symlink()
           for name in GENERATED_OUTPUT_FILES):
        print(
            "ERROR: OUTPUT_DIRECTORY_ALREADY_HAS_RESULTS; choose a new "
            "--out-dir to preserve the earlier attempt and avoid stale files.",
            file=__import__("sys").stderr,
        )
        return 2
    records, rejected, diagnostics = [], [], []
    source_manifest = []
    all_fields = set()

    for input_index, filename in enumerate(args.inputs, 1):
        p = Path(filename).resolve()
        source_input_id = f"INPUT-{input_index:04d}"
        file_entry = {
            "source_input_id": source_input_id,
            "source_file": p.name,
            "content_sha256": None,
            "size_bytes": None,
            "read_status": "UNREADABLE_EXPORT",
            "rows_observed": 0,
        }
        source_manifest.append(file_entry)
        try:
            source = read_tabular(p)
            file_entry["content_sha256"] = sha256_stream(p)
            file_entry["size_bytes"] = p.stat().st_size
            file_entry["rows_observed"] = len(source)
            file_entry["read_status"] = "READABLE"
        except HeaderValidationError as exc:
            # Entire export is untrusted because a dict can hide conflicting
            # columns. The original remains untouched; quarantine by row.
            file_entry["read_status"] = exc.reason
            file_entry["rows_observed"] = len(exc.rows)
            try:
                file_entry["content_sha256"] = sha256_stream(p)
                file_entry["size_bytes"] = p.stat().st_size
            except OSError:
                pass
            diagnostics.append({
                "source_file": p.name, "source_input_id": source_input_id,
                "reason": exc.reason, "affected_records": len(exc.rows),
                "conflicting_headers": exc.columns,
            })
            for row_idx, original_cells in enumerate(exc.rows, 2):
                rejected.append({
                    "_source_file": p.name, "_source_input_id": source_input_id,
                    "_source_row": str(row_idx), "_reject_reason": exc.reason,
                    "_raw_record": repr(original_cells)[:3000],
                })
            continue
        except (OSError, ValueError, StopIteration, csv.Error) as exc:
            diagnostics.append({"source_file": p.name, "source_input_id": source_input_id, "reason": "UNREADABLE_EXPORT",
                                "affected_records": 0, "error_type": type(exc).__name__})
            continue
        if not source:
            file_entry["read_status"] = "EMPTY_EXPORT"
            diagnostics.append({"source_file": p.name, "source_input_id": source_input_id, "reason": "EMPTY_EXPORT",
                                "affected_records": 0})
            continue
        header = list(source[0].keys())
        if not available_schema([str(h) for h in header if h is not None]):
            diagnostics.append({"source_file": p.name, "source_input_id": source_input_id, "reason": "MISSING_BIBLIOGRAPHIC_SCHEMA",
                                "affected_records": len(source),
                                "available_headers": [str(h) for h in header if h is not None]})
            for idx, raw in enumerate(source, 2):
                rejected.append({"_source_file": p.name, "_source_input_id": source_input_id, "_source_row": str(idx),
                                 "_reject_reason": "MISSING_BIBLIOGRAPHIC_SCHEMA",
                                 "_raw_record": repr(raw)[:3000]})
            continue

        for idx, raw in enumerate(source, 2):
            if None in raw or any(isinstance(v, (list, dict, tuple)) for v in raw.values()):
                rejected.append({"_source_file": p.name, "_source_input_id": source_input_id, "_source_row": str(idx),
                                 "_reject_reason": "MALFORMED_ROW",
                                 "_raw_record": repr(raw)[:3000]})
                continue
            row = {str(k): "" if v is None else str(v) for k, v in raw.items()}
            reason = identity_reason(row)
            if reason:
                rejected.append({"_source_file": p.name, "_source_input_id": source_input_id, "_source_row": str(idx),
                                 "_reject_reason": reason, "_raw_record": repr(row)[:3000]})
                continue
            row["_source_file"] = p.name
            row["_source_input_id"] = source_input_id
            row["_source_row"] = str(idx)
            row["_norm_doi"] = norm_doi(pick(row, "doi"))
            row["_norm_title"] = norm_title(pick(row, "title"))
            row["_first_author"] = first_author(pick(row, "authors"))
            row["_year"] = normal_year(pick(row, "year"))
            row["_stable_id"] = normal_stable_id(pick(row, "stable_id"))
            row["_version"] = pick(row, "version").strip().casefold()
            row["_merged_Record_IDs"] = identifier_list(row, "record_id")
            row["_merged_Search_IDs"] = identifier_list(row, "search_id")
            row["_source_locations"] = f"{source_input_id}:{p.name}:{idx}"
            records.append(row)
            all_fields.update(row.keys())

    canonical, exact_audit, doi_index, title_index = [], [], {}, {}
    for rec in records:
        match, reason = None, ""
        if rec["_norm_doi"]:
            for candidate in doi_index.get(rec["_norm_doi"], []):
                prior = canonical[candidate]
                versions_conflict = bool(rec["_version"] and prior["_version"]
                                         and rec["_version"] != prior["_version"])
                if not versions_conflict:
                    match, reason = candidate, "exact_doi"
                    break
        if match is None and rec["_norm_title"]:
            for candidate in title_index.get(rec["_norm_title"], []):
                prior = canonical[candidate]
                conflicting_doi = bool(rec["_norm_doi"] and prior["_norm_doi"]
                                       and rec["_norm_doi"] != prior["_norm_doi"])
                versions_conflict = bool(rec["_version"] and prior["_version"]
                                         and rec["_version"] != prior["_version"])
                if (not conflicting_doi and not versions_conflict
                        and rec["_first_author"] and rec["_year"]
                        and rec["_first_author"] == prior["_first_author"]
                        and rec["_year"] == prior["_year"]):
                    match, reason = candidate, "exact_title_author_year"
                    break
        if match is None:
            ci = len(canonical)
            canonical.append(rec)
            if rec["_norm_doi"]:
                doi_index.setdefault(rec["_norm_doi"], []).append(ci)
            if rec["_norm_title"]:
                title_index.setdefault(rec["_norm_title"], []).append(ci)
        else:
            prior = canonical[match]
            if rec["_norm_doi"]:
                existing = doi_index.setdefault(rec["_norm_doi"], [])
                if match not in existing:
                    existing.append(match)
                if not prior["_norm_doi"]:
                    prior["_norm_doi"] = rec["_norm_doi"]
            for field in ("_merged_Record_IDs", "_merged_Search_IDs", "_source_locations"):
                prior[field] = append_distinct(prior[field], rec[field])
            exact_audit.append({
                "duplicate_source_file": rec["_source_file"],
                "duplicate_source_input_id": rec["_source_input_id"],
                "duplicate_source_row": rec["_source_row"],
                "canonical_source_file": prior["_source_file"],
                "canonical_source_input_id": prior["_source_input_id"],
                "canonical_source_row": prior["_source_row"],
                "duplicate_Record_ID": identifier_list(rec, "record_id"),
                "duplicate_Search_ID": identifier_list(rec, "search_id"),
                "canonical_Record_ID": identifier_list(prior, "record_id"),
                "canonical_Search_ID": identifier_list(prior, "search_id"),
                "reason": reason,
                "doi": rec["_norm_doi"], "title": pick(rec, "title"),
            })

    fuzzy = []
    for i, a in enumerate(canonical):
        ta = a["_norm_title"]
        if not ta:
            continue
        for b in canonical[i+1:]:
            tb = b["_norm_title"]
            if not tb:
                continue
            author_ok = bool(a["_first_author"] and a["_first_author"] == b["_first_author"])
            year_ok = bool(a["_year"] and b["_year"] and a["_year"] == b["_year"])
            if ta != tb and not (author_ok or year_ok):
                continue
            score = SequenceMatcher(None, ta, tb).ratio()
            if score >= args.fuzzy_threshold:
                fuzzy.append({
                    "source_file_a": a["_source_file"], "source_input_id_a": a["_source_input_id"], "source_row_a": a["_source_row"],
                    "title_a": pick(a, "title"), "doi_a": a["_norm_doi"],
                    "source_file_b": b["_source_file"], "source_input_id_b": b["_source_input_id"], "source_row_b": b["_source_row"],
                    "title_b": pick(b, "title"), "doi_b": b["_norm_doi"],
                    "title_similarity": f"{score:.4f}",
                    "author_overlap_signal": "yes" if author_ok else "no",
                    "same_year_signal": "yes" if year_ok else "no",
                    "decision": "REVIEW_REQUIRED",
                    "notes": "Do not remove automatically.",
                })

    for reason, count in sorted(__import__("collections").Counter(
            item["_reject_reason"] for item in rejected).items()):
        diagnostics.append({"source_file": "MULTIPLE", "reason": reason,
                            "affected_records": count})
    out.mkdir(parents=True, exist_ok=True)
    summary = {"input_records": len(records) + len(rejected),
               "valid_records": len(records),
               "rejected_records": len(rejected),
               "canonical_after_exact_dedup": len(canonical),
               "exact_duplicates": len(exact_audit),
               "near_duplicate_pairs_to_review": len(fuzzy),
               "diagnostics": diagnostics}
    # Preserve a privacy-conscious, content-addressed map from this run's
    # positional IDs to their inputs. Never record absolute paths or credentials.
    (out / "import_sources_manifest.json").write_text(
        __import__("json").dumps({
            "schema_version": 1,
            "id_scope": "SINGLE_IMPORT_INVOCATION",
            "inputs": source_manifest,
            "limitations": "Hashes describe files observed during this invocation; "
                           "they do not identify scientific works or verify source validity.",
        }, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (out / "import_diagnostics.json").write_text(
        __import__("json").dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    with (out / "rejected_records.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["_source_file", "_source_input_id", "_source_row",
                                          "_reject_reason", "_raw_record"])
        w.writeheader()
        write_safe_rows(w, rejected)

    if not canonical:
        print("ERROR: no valid bibliographic records; see import_diagnostics.json", file=__import__("sys").stderr)
        return 2

    with (out / "consolidated_exact_dedup.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=sorted(all_fields))
        w.writeheader()
        write_safe_rows(w, canonical)
    with (out / "exact_duplicate_audit.csv").open("w", newline="", encoding="utf-8-sig") as f:
        fields = ["duplicate_source_file", "duplicate_source_input_id", "duplicate_source_row", "canonical_source_file", "canonical_source_input_id",
                  "canonical_source_row", "duplicate_Record_ID", "duplicate_Search_ID",
                  "canonical_Record_ID", "canonical_Search_ID", "reason", "doi", "title"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        write_safe_rows(w, exact_audit)
    with (out / "near_duplicate_review.csv").open("w", newline="", encoding="utf-8-sig") as f:
        fields = ["source_file_a", "source_input_id_a", "source_row_a", "title_a", "doi_a", "source_file_b", "source_input_id_b",
                  "source_row_b", "title_b", "doi_b", "title_similarity",
                  "author_overlap_signal", "same_year_signal", "decision", "notes"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        write_safe_rows(w, fuzzy)

    print(f"input_records={summary['input_records']}")
    print(f"canonical_after_exact_dedup={len(canonical)}")
    print(f"exact_duplicates={len(exact_audit)}")
    print(f"near_duplicate_pairs_to_review={len(fuzzy)}")
    print(f"rejected_records={len(rejected)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
