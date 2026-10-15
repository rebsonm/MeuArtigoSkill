"""REG-019 synthetic replay archive integrity and privacy tests (offline)."""
from __future__ import annotations
import json
import hashlib
from pathlib import Path
import sys
import tempfile
import unittest
from zipfile import ZipFile,ZipInfo,ZIP_DEFLATED

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import evaluation_package as ep
import evaluation_registry as er

CATALOG=ROOT/"benchmarks/critical_cases_v1.json"
FIXTURES_DO_NOT_INCLUDE_REAL_OBSERVATIONS=True

class ReplayPackageTests(unittest.TestCase):
    def setUp(self):
        td=tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        self.dir=Path(td.name)
        self.archive=self.dir/"evaluation.zip"
        self.ledger=self.dir/"runs.jsonl"
        self.catalog=json.loads(CATALOG.read_text(encoding="utf-8"))
        self.cases=er.validate_catalog(self.catalog)

    def observed(self):
        # This is a synthetic unit-test fixture, not an empirical researcher observation.
        first=next(iter(self.cases))
        p=self.dir/"sample_observed.json"
        p.write_text(json.dumps({
            "schema_version":1,"cases":[{
                "case_id":first,
                "observed_action":self.cases[first]["expected_action"],
                "evidence_reference":"PRIVATE_TEST_OUTPUT_LOCATION_SECRET_774"
            }]}),encoding="utf-8")
        er.record(CATALOG,p,self.ledger,"fixture-001","a"*40)

    def payload(self):
        with ZipFile(self.archive) as f:
            return {name:f.read(name) for name in f.namelist()}

    def repack(self,members):
        with ZipFile(self.archive,"w",compression=ZIP_DEFLATED) as z:
            for name,data in members.items():
                z.writestr(name,data)

    def test_empty_package_is_explicitly_not_an_executed_study(self):
        b=ep.build(self.archive,CATALOG)
        summary=ep.validate(self.archive)
        self.assertEqual(summary["run_count"],0)
        self.assertEqual(summary["case_count"],12)
        self.assertEqual(summary["observed_total"],0)
        self.assertFalse(summary["scientific_validity_proven"])
        self.assertFalse(b["scientific_quality_validated"])
        self.assertEqual(json.loads(self.payload()["OBSERVATIONS.json"])["status"],"NO_OBSERVED_RUNS")

    def test_identical_inputs_produce_identical_archive_sha(self):
        a=ep.build(self.archive,CATALOG)
        other=self.dir/"other.zip"
        b=ep.build(other,CATALOG)
        self.assertEqual(a["archive_sha256"],b["archive_sha256"])
        self.assertEqual(self.archive.read_bytes(),other.read_bytes())

    def test_self_reported_run_is_recomputed_and_private_refs_redacted(self):
        self.observed()
        ep.build(self.archive,CATALOG,ledger=self.ledger)
        report=ep.validate(self.archive)
        self.assertEqual(report["run_count"],1)
        self.assertEqual(report["observed_total"],1)
        entries=self.payload()
        text="".join(v.decode("utf-8") for v in entries.values())
        self.assertNotIn("PRIVATE_TEST_OUTPUT_LOCATION_SECRET_774",text)
        self.assertNotIn(str(self.dir),text)
        self.assertNotIn('"evidence_reference":',text)
        self.assertIn("evidence_reference_sha256",text)
        result=json.loads(entries["OBSERVATIONS.json"])
        self.assertFalse(result["original_ledger_chain_reverifiable_from_this_redacted_package"])
        self.assertFalse(result["independent_scientific_validation"])
        self.assertEqual(result["runs"][0]["score"]["matches_expected"],1)
        self.assertEqual(result["runs"][0]["score"]["not_evaluated"],11)

    def test_project_protocol_contents_never_copied(self):
        p=self.dir/"research"/"00_Gestao_e_Continuidade"
        p.mkdir(parents=True)
        f=p/"01_Protocolo.csv"
        f.write_text("PRIVATE_UNPUBLISHED_PROTOCOL_SOURCE_TEXT_963",encoding="utf-8")
        ep.build(self.archive,CATALOG,project=p.parent)
        all_text="".join(v.decode("utf-8") for v in self.payload().values())
        self.assertNotIn("PRIVATE_UNPUBLISHED_PROTOCOL_SOURCE_TEXT_963",all_text)
        obj=json.loads(self.payload()["PROTOCOL.json"])
        self.assertEqual(obj["canonical_project_protocol_sha256"],
                         hashlib.sha256(f.read_bytes()).hexdigest())
        self.assertFalse(obj["canonical_project_protocol_contents_included"])

    def test_changed_archive_member_rejected_by_hash(self):
        ep.build(self.archive,CATALOG)
        members=self.payload()
        members["README.md"]+=b"\ncorrupted"
        self.repack(members)
        with self.assertRaisesRegex(ValueError,"SHA-256 mismatch"):
            ep.validate(self.archive)

    def test_tampered_scores_rejected_even_if_checksum_recomputed(self):
        self.observed()
        ep.build(self.archive,CATALOG,ledger=self.ledger)
        members=self.payload()
        obs=json.loads(members["OBSERVATIONS.json"])
        obs["runs"][0]["score"]["matches_expected"]=999
        members["OBSERVATIONS.json"]=ep.json_bytes(obs)
        manifest=json.loads(members["MANIFEST.json"])
        manifest["files"]["OBSERVATIONS.json"]=ep.hashed(members["OBSERVATIONS.json"])
        members["MANIFEST.json"]=ep.json_bytes(manifest)
        self.repack(members)
        with self.assertRaisesRegex(ValueError,"metrics disagree"):
            ep.validate(self.archive)

    def test_changed_catalog_in_ledger_fails_closed(self):
        self.observed()
        changed=json.loads(CATALOG.read_text(encoding="utf-8"))
        changed["cases"][0]["scenario"]="Changed scenario invalidates frozen evaluation"
        path=self.dir/"changed.json"
        path.write_text(json.dumps(changed),encoding="utf-8")
        with self.assertRaisesRegex(ValueError,"different frozen case catalog"):
            ep.build(self.archive,path,ledger=self.ledger)
        self.assertFalse(self.archive.exists())

    def test_existing_output_cannot_be_overwritten(self):
        ep.build(self.archive,CATALOG)
        before=self.archive.read_bytes()
        with self.assertRaisesRegex(ValueError,"non-existing"):
            ep.build(self.archive,CATALOG)
        self.assertEqual(before,self.archive.read_bytes())

    def test_missing_ledger_is_not_called_zero_real_failures(self):
        with self.assertRaisesRegex(ValueError,"ledger unavailable"):
            ep.build(self.archive,CATALOG,ledger=self.dir/"not-found.jsonl")
        self.assertFalse(self.archive.exists())

    def test_modified_ledger_fails_on_original_chain(self):
        self.observed()
        self.ledger.write_text(self.ledger.read_text(encoding="utf-8").replace(
            "fixture-001","fixture-999"),encoding="utf-8")
        with self.assertRaisesRegex(ValueError,"integrity"):
            ep.build(self.archive,CATALOG,ledger=self.ledger)

    def test_unknown_zip_member_and_traversal_rejected(self):
        ep.build(self.archive,CATALOG)
        members=self.payload()
        members["../private.txt"]=b"NOT_ALLOWED"
        self.repack(members)
        with self.assertRaisesRegex(ValueError,"archive members"):
            ep.validate(self.archive)

    def test_duplicate_zip_members_rejected(self):
        ep.build(self.archive,CATALOG)
        entries=self.payload()
        with ZipFile(self.archive,"w") as z:
            for name,data in entries.items():
                z.writestr(name,data)
            import warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore",UserWarning)
                z.writestr("README.md",b"duplicate")
        with self.assertRaisesRegex(ValueError,"duplicate archive members"):
            ep.validate(self.archive)

    def test_no_source_bundle_or_sensitive_canonical_project_tables(self):
        ep.build(self.archive,CATALOG)
        blob="".join(v.decode("utf-8") for v in self.payload().values())
        for absent in ("PROJECT_CONFIG.json","09_Claims_Ledger.csv",
                       "05_Evidence_Matrix.csv","GATE-0006 APPROVED",
                       "independent peer review passed"):
            self.assertNotIn(absent,blob)
        self.assertEqual(set(self.payload()),ep.ALL)

if __name__=="__main__":
    unittest.main()
