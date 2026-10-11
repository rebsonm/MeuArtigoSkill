#!/usr/bin/env python3
"""Reproducible scientific-quality calibration with real published sources.

Two separate paths:
  pilot: live, public metadata checks of factual references (not LLM quality);
  evaluate: compare *actual* candidate outputs with independently frozen
            reference facts and optional separately adjudicated claim labels.
Never infer semantic validity from metadata, a text match, or a publication.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path

from verify_sources import check_locator, doi_of, match_metadata, norm, provider_query

DEFAULT_REFERENCE = Path(__file__).resolve().parents[1] / "benchmarks/public_review_reference_v1.json"
DEFAULT_METHOD_REFERENCE = Path(__file__).resolve().parents[1] / "benchmarks/methodological_response_reference_v1.json"
COUNT_NAMES = {
    "database_records", "other_records", "identified", "duplicates_removed",
    "screened", "screened_excluded", "full_text_reviewed",
    "full_text_excluded", "included",
}
LABELS = {"SUPPORTED", "NOT_SUPPORTED", "UNCERTAIN"}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, content):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(content, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def ratio(numerator, denominator):
    return round(numerator / denominator, 5) if denominator else None


def reference_cases(reference):
    if reference.get("schema_version") != 1 or not isinstance(reference.get("cases"), list):
        raise ValueError("Unsupported public reference set")
    cases = {}
    for row in reference["cases"]:
        case = row.get("case")
        if not case or case in cases:
            raise ValueError("Each reference case requires a unique identifier")
        if not doi_of(row.get("doi", "")) or not row.get("source", "").startswith("https://"):
            raise ValueError(f"{case}: DOI and official source are mandatory")
        for key, n in {**row.get("reported_counts", {}), **row.get("derived_counts", {})}.items():
            if key not in COUNT_NAMES or type(n) is not int or n < 0:
                raise ValueError(f"{case}: invalid count {key}")
        # Check only equalities whose inputs are all present.
        flow = {**row.get("reported_counts", {}), **row.get("derived_counts", {})}
        for lhs, terms in [
            ("identified", ["database_records", "other_records"]),
            ("screened", ["identified", "-duplicates_removed"]),
            ("full_text_reviewed", ["screened", "-screened_excluded"]),
            ("included", ["full_text_reviewed", "-full_text_excluded"]),
        ]:
            if lhs in flow and all(t.lstrip("-") in flow for t in terms):
                calculated = sum((-1 if t.startswith("-") else 1) * flow[t.lstrip("-")] for t in terms)
                if flow[lhs] != calculated:
                    raise ValueError(f"{case}: inconsistent published/derived count {lhs}")
        cases[case] = row
    return cases


def pilot(reference_path=DEFAULT_REFERENCE, *, offline=False, fetcher=provider_query):
    reference_path = Path(reference_path)
    cases = reference_cases(read_json(reference_path))
    results = []
    for case_id, source in cases.items():
        doi = doi_of(source["doi"])
        response = {
            p: ({"status": "OFFLINE"} if offline else fetcher(p, doi, ""))
            for p in ("crossref", "openalex")
        }
        outcome, checks, retracted, corrected, updated, notices, provider_warnings = match_metadata(
            doi, source["title"], str(source["published_year"]), source.get("authors", ""), response
        )
        results.append({
            "case": case_id, "doi": doi,
            "metadata_status": outcome, "provider_checks": checks,
            "retraction_alert": retracted, "correction_alert": corrected,
            "update_alert": updated, "editorial_notices": notices,
            "provider_warnings": provider_warnings,
            "interpretation": "BIBLIOGRAPHIC_IDENTITY_ONLY",
            "full_text_evaluated": False,
            "claims_scientifically_adjudicated": False,
        })
    return {
        "schema_version": 1, "mode": "public_metadata_pilot",
        "reference_sha256": digest(reference_path),
        "observed_at": timestamp(), "offline": offline,
        "case_count": len(results),
        "verified_metadata": sum(x["metadata_status"] == "VERIFIED" for x in results),
        "unverified_metadata": sum(x["metadata_status"] != "VERIFIED" for x in results),
        "results": results,
        "limitation": "Checks open bibliographic providers, not manuscript creation, claim support, or review replication.",
    }


def prediction_cases(candidate):
    if candidate.get("schema_version") != 1:
        raise ValueError("Candidate file must use schema_version=1")
    items = candidate.get("cases") or []
    if not isinstance(items, list):
        raise ValueError("Candidate cases must be a list")
    out = {}
    for row in items:
        case = row.get("case")
        if not isinstance(case, str) or not case or case in out:
            raise ValueError("Candidate case identifiers must be distinct and nonempty")
        out[case] = row
    return out


def field_scores(reference, candidates, workspace):
    result = {
        "identity": {"eligible": len(reference), "observed": 0, "doi_exact": 0, "title_corresponds": 0},
        "stage_counts": {"eligible": 0, "observed": 0, "correct": 0, "inconsistent_cases": []},
        "locators": {"observed": 0, "matched": 0, "pending": 0, "mismatch": 0},
    }
    detail = []
    for key, gold in reference.items():
        pred = candidates.get(key)
        if pred is None:
            detail.append({"case": key, "status": "NOT_SUBMITTED"})
            result["stage_counts"]["eligible"] += len(gold.get("reported_counts", {})) + len(gold.get("derived_counts", {}))
            continue
        row = {"case": key, "status": "SUBMITTED"}
        doi_pred = doi_of(pred.get("doi") or "")
        title_pred = pred.get("title") or ""
        identity_observed = bool(doi_pred or title_pred)
        if identity_observed:
            result["identity"]["observed"] += 1
            result["identity"]["doi_exact"] += int(doi_pred == doi_of(gold["doi"]))
            result["identity"]["title_corresponds"] += int(bool(title_pred) and
                SequenceMatcher(None, norm(title_pred), norm(gold["title"])).ratio() >= 0.86)
            row["doi_exact"] = doi_pred == doi_of(gold["doi"])
            row["title_corresponds"] = bool(title_pred) and (
                SequenceMatcher(None, norm(title_pred), norm(gold["title"])).ratio() >= 0.86)
        gold_counts = {**gold.get("reported_counts", {}), **gold.get("derived_counts", {})}
        pred_counts = pred.get("stage_counts") or {}
        if not isinstance(pred_counts, dict):
            raise ValueError(f"{key}: stage_counts must be a dictionary")
        result["stage_counts"]["eligible"] += len(gold_counts)
        row["count_errors"] = {}
        for name, expected in gold_counts.items():
            if name not in pred_counts or pred_counts[name] is None:
                continue
            value = pred_counts[name]
            if type(value) is not int or value < 0:
                raise ValueError(f"{key}: invalid submitted count {name}")
            result["stage_counts"]["observed"] += 1
            result["stage_counts"]["correct"] += int(value == expected)
            if value != expected:
                row["count_errors"][name] = {"reported_or_derived": expected, "candidate": value}
        # Candidate arithmetic is checked separately from agreement with published figures.
        algebra = [
            ("identified", ["database_records", "other_records"]),
            ("screened", ["identified", "-duplicates_removed"]),
            ("full_text_reviewed", ["screened", "-screened_excluded"]),
            ("included", ["full_text_reviewed", "-full_text_excluded"]),
        ]
        for lhs, terms in algebra:
            if lhs in pred_counts and all(t.lstrip("-") in pred_counts for t in terms):
                value = sum((-1 if t.startswith("-") else 1)*pred_counts[t.lstrip("-")] for t in terms)
                if pred_counts[lhs] != value:
                    result["stage_counts"]["inconsistent_cases"].append({"case": key, "equation": lhs})
        locators = pred.get("locators") or []
        if not isinstance(locators, list):
            raise ValueError(f"{key}: locators must be a list")
        row["locators"] = []
        for locator in locators:
            # The cited file must be held inside the workspace. No online download.
            path = locator.get("source_path", "")
            snippet = locator.get("supporting_locator", "")
            checked = check_locator(workspace, path, snippet)
            status = checked["status"]
            bucket = "matched" if status == "MATCHED" else "mismatch" if status in {
                "PASSAGE_NOT_FOUND", "PAGE_MISMATCH", "OUTSIDE_WORKSPACE"
            } else "pending"
            result["locators"]["observed"] += 1
            result["locators"][bucket] += 1
            row["locators"].append({
                "claim_id": locator.get("claim_id"), "locator_status": status,
                "textual_match_only": True, "semantic_support": "NOT_ADJUDICATED",
                "source_sha256": checked.get("source_sha256"),
            })
        detail.append(row)
    result["identity"]["doi_exact_rate_on_observed"] = ratio(
        result["identity"]["doi_exact"], result["identity"]["observed"])
    result["identity"]["coverage"] = ratio(result["identity"]["observed"], result["identity"]["eligible"])
    result["stage_counts"]["correct_rate_on_observed"] = ratio(
        result["stage_counts"]["correct"], result["stage_counts"]["observed"])
    result["stage_counts"]["coverage"] = ratio(
        result["stage_counts"]["observed"], result["stage_counts"]["eligible"])
    result["locators"]["text_match_rate_on_observed"] = ratio(
        result["locators"]["matched"], result["locators"]["observed"])
    return result, detail


def adjudication_scores(candidate, annotations=None):
    submitted = candidate.get("claims") or []
    predicted = {str(r.get("claim_id")): r for r in submitted}
    if len(predicted) != len(submitted):
        raise ValueError("Claim identifiers must be unique")
    if annotations is None:
        return {
            "status": "NOT_EVALUATED", "reason": "No independently prepared claim annotations were supplied",
            "submitted_claims": len(submitted), "adjudicated": 0, "accuracy": None,
            "category_assessment": "PENDING_INDEPENDENT_REVIEW",
        }
    if annotations.get("schema_version") != 1 or not annotations.get("reviewer_reference"):
        raise ValueError("Adjudication requires a documented independent review reference")
    gold_items = annotations.get("claims") or []
    gold = {str(r.get("claim_id")): r for r in gold_items}
    if len(gold) != len(gold_items):
        raise ValueError("Adjudication claim identifiers must be unique")
    eligible = [key for key in predicted if key in gold and
                predicted[key].get("label") in LABELS and gold[key].get("label") in LABELS]
    correct = sum(predicted[key]["label"] == gold[key]["label"] for key in eligible)
    return {
        "status": "ANNOTATIONS_PROVIDED_UNAUTHENTICATED", "reviewer_reference": annotations["reviewer_reference"],
        "submitted_claims": len(submitted), "adjudicated": len(eligible), "correct": correct,
        "accuracy": ratio(correct, len(eligible)),
        "category_assessment": "REQUIRES_DOCUMENTED_HUMAN_ADJUDICATION",
        "note": "A JSON annotation and reviewer field do not authenticate independence or scientific correctness.",
    }


def evaluate(reference_path, candidate_path, *, workspace, adjudications=None, baseline=None):
    reference_path = Path(reference_path)
    candidate_path = Path(candidate_path)
    reference = reference_cases(read_json(reference_path))
    candidate = read_json(candidate_path)
    if "reference_sha256" in candidate and candidate["reference_sha256"] != digest(reference_path):
        raise ValueError("Candidate was generated for a different frozen reference file")
    candidates = prediction_cases(candidate)
    unknown = sorted(set(candidates) - set(reference))
    if unknown:
        raise ValueError("Unknown cases not present in frozen reference: " + ", ".join(unknown))
    scored, details = field_scores(reference, candidates, Path(workspace).resolve())
    review = read_json(adjudications) if adjudications else None
    semantic = adjudication_scores(candidate, review)
    result = {
        "schema_version": 1, "mode": "candidate_evaluation",
        "reference_sha256": digest(reference_path),
        "candidate_sha256": digest(candidate_path),
        "observed_at": timestamp(), "submitted_cases": len(candidates),
        "metrics": scored, "semantic_adjudication": semantic, "cases": details,
        "limitations": [
            "Scores describe the submitted cases, not an exhaustive independent replication of the original review.",
            "Absent predictions are coverage gaps, never interpreted as correct answers.",
            "Quoted-text matching does not establish whether a claim is scientifically supported.",
            "Published theme labels are not automatic gold standard categories. Any coding comparison needs independent adjudication.",
            "Claim reviewers and their independence cannot be authenticated by a JSON field alone.",
        ],
    }
    if baseline:
        base = evaluate(reference_path, baseline, workspace=workspace)
        comparison = {}
        for group, metric in [
            ("identity", "doi_exact_rate_on_observed"),
            ("stage_counts", "correct_rate_on_observed"),
            ("locators", "text_match_rate_on_observed"),
        ]:
            before = base["metrics"][group][metric]
            after = scored[group][metric]
            comparison[group] = {"baseline": before, "candidate": after,
                                 "change": round(after - before, 5) if before is not None and after is not None else None}
        result["baseline_comparison"] = comparison
        result["comparison_limit"] = "Interpret changes only when task, source set, denominators and judging process are equivalent."
    return result



def methodology_reference_cases(reference):
    """Validate frozen *synthetic software* checks, never a scientific gold set."""
    if (not isinstance(reference, dict)
            or reference.get("schema_version") != 1
            or reference.get("source_kind") != "SYNTHETIC_SOFTWARE_REGRESSION_FIXTURE"
            or reference.get("independent_scientific_gold") is not False
            or not isinstance(reference.get("cases"), list)
            or not 1 <= len(reference["cases"]) <= 40):
        raise ValueError("Not a bounded synthetic methodological reference")
    cases = {}
    for row in reference["cases"]:
        if not isinstance(row, dict):
            raise ValueError("Malformed methodological reference case")
        case = row.get("case")
        expected = row.get("expected")
        required = row.get("required_nonempty")
        if (not isinstance(case, str) or not re.fullmatch(r"[a-z][a-z0-9_]{3,79}", case)
                or case in cases or not isinstance(expected, dict)
                or not expected or not isinstance(required, list)
                or len(required) != len(set(map(str, required)))):
            raise ValueError("Malformed or repeated methodological case")
        if any(not isinstance(key, str) or not key or
               type(value) not in (str, int, bool)
               for key, value in expected.items()):
            raise ValueError("Methodological expectations must use primitive fields")
        if (any(not isinstance(key, str) or not key
                or key in expected for key in required)
                or len(expected) + len(required) > 30):
            raise ValueError("Invalid or excessive required methodological fields")
        if expected.get("approved_by_automation") is True or expected.get("human_reviewer_confirmed") is True:
            raise ValueError("Synthetic checklist cannot claim AI approved a human decision")
        cases[case] = row
    return cases


def methodology_candidate_cases(candidate, reference_sha):
    """Only user-supplied recorded outputs; never infer missing candidates."""
    if (not isinstance(candidate, dict) or candidate.get("schema_version") != 1
            or candidate.get("reference_sha256") != reference_sha
            or not isinstance(candidate.get("cases"), list)):
        raise ValueError("Methodology candidate requires matching frozen reference SHA-256")
    output = {}
    for row in candidate["cases"]:
        if not isinstance(row, dict) or not isinstance(row.get("case"), str):
            raise ValueError("Malformed methodological candidate case")
        key = row["case"]
        fields = row.get("fields")
        if key in output or not isinstance(fields, dict):
            raise ValueError("Repeated case or missing candidate fields object")
        if any(not isinstance(k, str) for k in fields):
            raise ValueError("Candidate field names must be strings")
        output[key] = fields
    return output


def evaluate_methodology(reference_path=DEFAULT_METHOD_REFERENCE, candidate_path=None,
                         *, baseline=None):
    """Score fixed structural expectations; never self-adjudicate meaning.

    Reports contain case IDs, field names and mismatch reasons, never raw
    candidate prose or source excerpts. Equal fields are not evidence that
    a real literature review, screening or human approval took place.
    """
    reference_path = Path(reference_path)
    if candidate_path is None:
        raise ValueError("Recorded candidate file is required")
    reference = methodology_reference_cases(read_json(reference_path))
    reference_sha = digest(reference_path)
    candidate_path = Path(candidate_path)
    candidates = methodology_candidate_cases(read_json(candidate_path), reference_sha)
    unknown = sorted(set(candidates) - set(reference))
    if unknown:
        raise ValueError("Candidate includes unknown methodological cases")
    summary = {"eligible_cases": len(reference), "submitted_cases": len(candidates),
               "criterion_count": 0, "observed_criteria": 0,
               "matched_criteria": 0, "missing_criteria": 0,
               "mismatched_criteria": 0, "structurally_matching_cases": 0}
    details = []
    for case_id, case in reference.items():
        expected = case["expected"]
        required = case["required_nonempty"]
        count = len(expected) + len(required)
        summary["criterion_count"] += count
        if case_id not in candidates:
            summary["missing_criteria"] += count
            details.append({"case": case_id, "status": "NOT_SUBMITTED",
                            "missing_fields": sorted([*expected, *required]),
                            "mismatched_fields": [], "matched_criteria": 0})
            continue
        fields = candidates[case_id]
        missing, mismatch, matched = [], [], 0
        for field, value in expected.items():
            if field not in fields:
                missing.append(field)
                continue
            if type(fields[field]) is type(value) and fields[field] == value:
                matched += 1
            else:
                mismatch.append(field)
        for field in required:
            if field not in fields:
                missing.append(field)
            elif isinstance(fields[field], str) and fields[field].strip():
                matched += 1
            else:
                mismatch.append(field)
        summary["matched_criteria"] += matched
        summary["missing_criteria"] += len(missing)
        summary["mismatched_criteria"] += len(mismatch)
        summary["observed_criteria"] += count - len(missing)
        ok = not missing and not mismatch
        summary["structurally_matching_cases"] += int(ok)
        details.append({"case": case_id,
                        "status": "STRUCTURAL_MATCH" if ok else "STRUCTURAL_MISMATCH",
                        "matched_criteria": matched,
                        "missing_fields": sorted(missing),
                        "mismatched_fields": sorted(mismatch)})
    summary["case_coverage"] = ratio(summary["submitted_cases"], summary["eligible_cases"])
    summary["criterion_coverage"] = ratio(summary["observed_criteria"], summary["criterion_count"])
    summary["fixed_rule_conformance_all_criteria"] = ratio(
        summary["matched_criteria"], summary["criterion_count"])
    summary["fixed_rule_conformance_observed_only"] = ratio(
        summary["matched_criteria"], summary["observed_criteria"])
    result = {
        "schema_version": 1, "mode": "methodological_response_calibration",
        "reference_sha256": reference_sha,
        "candidate_sha256": digest(candidate_path),
        "observed_at": timestamp(),
        "reference_kind": "SYNTHETIC_SOFTWARE_REGRESSION_FIXTURE",
        "human_semantic_review": "NOT_PERFORMED",
        "scientific_validity_proven": False,
        "source_access_verified": False,
        "reviewer_identity_authenticated": False,
        "metrics": summary,
        "cases": details,
        "limitations": [
            "Comparison is limited to frozen expected field values and nonempty documentation markers.",
            "A matching text field does not mean that its evidence, interpretation or research justification is correct.",
            "Reference cases are synthetic developer-authored policy examples, not independently adjudicated scientific gold.",
            "No researcher identity, human gate approval, source access or real model behavior is authenticated by this report.",
            "Do not interpret structural conformance as scientific quality, a successful research article or validated productivity.",
        ],
    }
    if baseline is not None:
        prior = evaluate_methodology(reference_path, baseline)
        b = prior["metrics"]
        result["baseline_comparison"] = {
            "reference_sha256": reference_sha,
            "comparable_rule_set": True,
            "baseline_matched_criteria": b["matched_criteria"],
            "candidate_matched_criteria": summary["matched_criteria"],
            "change_matched_criteria": summary["matched_criteria"] - b["matched_criteria"],
            "baseline_case_coverage": b["case_coverage"],
            "candidate_case_coverage": summary["case_coverage"],
            "interpretation": "Structural compliance only; distinct model tasks, sources, and human checks cannot be inferred equivalent.",
        }
    return result


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)
    p = sub.add_parser("pilot", help="Query real public DOI metadata; not LLM evaluation")
    p.add_argument("--reference", default=str(DEFAULT_REFERENCE))
    p.add_argument("--offline", action="store_true")
    p.add_argument("--output", required=True)
    e = sub.add_parser("evaluate", help="Score actual recorded outputs against frozen public references")
    e.add_argument("--reference", default=str(DEFAULT_REFERENCE))
    e.add_argument("--candidate", required=True)
    e.add_argument("--workspace", required=True)
    e.add_argument("--adjudications", default="")
    e.add_argument("--baseline", default="")
    e.add_argument("--output", required=True)
    m = sub.add_parser("evaluate-methodology",
                       help="Compare recorded responses to frozen synthetic structural checks, not scientific truth")
    m.add_argument("--reference", default=str(DEFAULT_METHOD_REFERENCE))
    m.add_argument("--candidate", required=True)
    m.add_argument("--baseline", default="")
    m.add_argument("--output", required=True)
    a = ap.parse_args(argv)
    try:
        if a.command == "pilot":
            report = pilot(a.reference, offline=a.offline)
        elif a.command == "evaluate":
            report = evaluate(a.reference, a.candidate, workspace=a.workspace,
                              adjudications=a.adjudications or None, baseline=a.baseline or None)
        else:
            report = evaluate_methodology(a.reference, a.candidate,
                                          baseline=a.baseline or None)
        write_json(a.output, report)
        print(json.dumps({"mode": report["mode"], "output": str(a.output),
                          "verified_metadata": report.get("verified_metadata"),
                          "submitted_cases": report.get("submitted_cases"),
                          "semantic_status": (report.get("semantic_adjudication") or {}).get("status"),
                          "human_semantic_review": report.get("human_semantic_review"),
                          "scientific_validity_proven": report.get("scientific_validity_proven")}, ensure_ascii=False))
        return 0
    except (ValueError, OSError, KeyError, TypeError) as ex:
        print("ERROR: " + str(ex), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
