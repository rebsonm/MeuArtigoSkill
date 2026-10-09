"""Offline adversarial checks for lawful-document handling and public export.

Every document is a disposable binary software fixture, never a scientific
article or a demonstration of real publication rights.
"""
import csv
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import rights_audit as rights
from export_provenance import canonical_files


class RightsTests(unittest.TestCase):
    def setUp(self):
        ctx=tempfile.TemporaryDirectory()
        self.addCleanup(ctx.cleanup)
        self.root=Path(ctx.name)
        self.mgmt=self.root/rights.MGMT
        self.mgmt.mkdir()
        self.corpus=self.root/rights.CORPUS
        self.corpus.mkdir(parents=True)
        self.file=self.corpus/"sample.pdf"
        self.file.write_bytes(b"%PDF-1.4\nOffline rights-validation fixture only.\n")
        self.rel=self.file.relative_to(self.root).as_posix()
        self.cols=["Record_ID","File_or_URL","Access_basis","Rights_basis","License_URI",
                   "Rights_evidence","Permission_scope","Attribution_text","Source_sha256",
                   "Rights_reviewed_by","Rights_review_evidence"]
        self.row={
            "Record_ID":"REC-0001","File_or_URL":self.rel,
            "Access_basis":"OPEN_ACCESS","Rights_basis":"CC_BY_4_0",
            "License_URI":"https://creativecommons.org/licenses/by/4.0/",
            "Rights_evidence":"https://publisher.example.org/article/rights-and-license",
            "Permission_scope":"","Attribution_text":
                "Synthetic software fixture, original author, source, CC BY 4.0, no modifications.",
            "Source_sha256":hashlib.sha256(self.file.read_bytes()).hexdigest(),
            "Rights_reviewed_by":"Researcher","Rights_review_evidence":
                "document:2026-10-09 direct human check of source and license.",
        }
        self.write_tracker([self.row])

    def write_tracker(self,items):
        with (self.mgmt/"04_FullText_Tracker.csv").open("w",encoding="utf-8-sig",newline="") as f:
            writer=csv.DictWriter(f,fieldnames=self.cols)
            writer.writeheader()
            writer.writerows(items)

    def invoke_export(self,*args):
        return subprocess.run([sys.executable,str(ROOT/"scripts/export_provenance.py"),
                               str(self.root),*args],capture_output=True,text=True)

    def test_open_cc_by_requires_matching_file_and_evidence(self):
        result=rights.authorize_external_fulltext(self.root)
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]["sha256"],self.row["Source_sha256"])
        self.assertFalse(rights.audit_project(self.root)["rights_legally_verified"])

    def test_explicit_permission_needed_even_if_file_is_readable(self):
        r={**self.row,"Rights_basis":"INSTITUTIONAL_ACCESS","Access_basis":"INSTITUTIONAL_ACCESS"}
        self.write_tracker([r])
        with self.assertRaisesRegex(ValueError,"redistribution NOT authorized"):
            rights.authorize_external_fulltext(self.root)

    def test_personal_authorized_access_is_not_redistribution(self):
        self.write_tracker([{**self.row,"Rights_basis":"PERSONAL_ACCESS","Access_basis":"PERSONAL_AUTHORIZED"}])
        with self.assertRaises(ValueError): rights.authorize_external_fulltext(self.root)

    def test_unknown_license_cannot_be_inferred_from_pdf(self):
        self.write_tracker([{**self.row,"Rights_basis":"UNKNOWN"}])
        self.assertFalse(rights.audit_project(self.root)["errors"])
        with self.assertRaises(ValueError): rights.authorize_external_fulltext(self.root)

    def test_cc_by_nc_not_assumed_public_redistributable(self):
        self.write_tracker([{**self.row,"Rights_basis":"CC_BY_NC_4_0"}])
        with self.assertRaises(ValueError): rights.authorize_external_fulltext(self.root)

    def test_stale_sha_blocks_export(self):
        self.file.write_bytes(self.file.read_bytes()+b" altered")
        with self.assertRaisesRegex(ValueError,"digest"):
            rights.authorize_external_fulltext(self.root)

    def test_exact_license_uri_required(self):
        self.write_tracker([{**self.row,"License_URI":"https://creativecommons.org/licenses/by-nc/4.0/"}])
        with self.assertRaisesRegex(ValueError,"license URI"):
            rights.authorize_external_fulltext(self.root)

    def test_missing_source_specific_rights_evidence(self):
        self.write_tracker([{**self.row,"Rights_evidence":""}])
        with self.assertRaisesRegex(ValueError,"source-specific"):
            rights.authorize_external_fulltext(self.root)

    def test_generic_license_page_is_not_specific_article_rights_evidence(self):
        row={**self.row,"Rights_evidence":"https://creativecommons.org/licenses/by/4.0/"}
        self.write_tracker([row])
        with self.assertRaisesRegex(ValueError,"source-specific"):
            rights.authorize_external_fulltext(self.root)

    def test_missing_attribution_is_not_a_valid_export(self):
        self.write_tracker([{**self.row,"Attribution_text":""}])
        with self.assertRaisesRegex(ValueError,"attribution"):
            rights.authorize_external_fulltext(self.root)

    def test_missing_reviewer_reference_blocks_export(self):
        self.write_tracker([{**self.row,"Rights_review_evidence":"OK"}])
        with self.assertRaisesRegex(ValueError,"review"):
            rights.authorize_external_fulltext(self.root)

    def test_ai_cannot_certify_its_own_rights_record(self):
        self.write_tracker([{**self.row,"Rights_reviewed_by":"ChatGPT"}])
        with self.assertRaises(ValueError): rights.authorize_external_fulltext(self.root)

    def test_direct_permission_requires_public_scope(self):
        permitted={**self.row,"Rights_basis":"DIRECT_PERMISSION","License_URI":"",
                   "Access_basis":"DIRECT_PERMISSION","Permission_scope":"READ"}
        self.write_tracker([permitted])
        with self.assertRaises(ValueError): rights.authorize_external_fulltext(self.root)
        permitted["Permission_scope"]="PUBLIC_REDISTRIBUTION"
        self.write_tracker([permitted])
        self.assertEqual(len(rights.authorize_external_fulltext(self.root)),1)

    def test_fulltext_without_tracking_record_fails(self):
        self.write_tracker([])
        with self.assertRaisesRegex(ValueError,"exactly one"):
            rights.authorize_external_fulltext(self.root)

    def test_two_rows_for_one_source_fail(self):
        self.write_tracker([self.row,{**self.row,"Record_ID":"REC-0002"}])
        with self.assertRaises(ValueError): rights.authorize_external_fulltext(self.root)

    def test_path_outside_corpus_cannot_be_sneaked_in(self):
        with self.assertRaises(ValueError):
            rights.local_file(self.root,"../unauthorized.pdf")
        self.write_tracker([{**self.row,"File_or_URL":"../unauthorized.pdf"}])
        with self.assertRaises(ValueError): rights.authorize_external_fulltext(self.root)

    def test_undocumented_extra_fulltext_blocks_export(self):
        (self.corpus/"second.pdf").write_bytes(b"undocumented binary test fixture")
        with self.assertRaisesRegex(ValueError,"exactly one"):
            rights.authorize_external_fulltext(self.root)

    def test_nested_archive_in_corpus_is_not_exported(self):
        (self.corpus/"hidden.zip").write_bytes(b"not a true zip")
        with self.assertRaisesRegex(ValueError,"Unrecognized"):
            rights.authorize_external_fulltext(self.root)

    def test_source_symlink_cannot_bypass_checks(self):
        other=self.root/"outside.pdf"
        other.write_bytes(b"outside")
        (self.corpus/"linked.pdf").symlink_to(other)
        with self.assertRaisesRegex(ValueError,"Symlink"):
            rights.authorize_external_fulltext(self.root)

    def test_default_provenance_export_never_includes_fulltext(self):
        result=self.invoke_export("--no-record-export-event")
        self.assertEqual(result.returncode,0,result.stderr)
        packages=list((self.root/"06_Submissao/Arquivos_Finais").glob("RO_CRATE_*.zip"))
        self.assertEqual(len(packages),1)
        with zipfile.ZipFile(packages[0]) as z:
            self.assertFalse(any(n.endswith("sample.pdf") for n in z.namelist()))
            self.assertFalse(any(n.endswith("FULLTEXT_RIGHTS.json") for n in z.namelist()))

    def test_fulltext_flag_alone_is_not_legal_permission(self):
        result=self.invoke_export("--include-fulltext")
        self.assertNotEqual(result.returncode,0)
        self.assertFalse((self.mgmt/"13_Traceability_Log.csv").exists())
        self.assertFalse((self.root/"06_Submissao/Arquivos_Finais").exists())

    def test_refused_export_does_not_create_event_or_zip(self):
        self.write_tracker([{**self.row,"Rights_basis":"ALL_RIGHTS_RESERVED"}])
        result=self.invoke_export("--include-fulltext","--confirm-rights-review")
        self.assertNotEqual(result.returncode,0)
        self.assertFalse((self.mgmt/"13_Traceability_Log.csv").exists())
        self.assertFalse((self.root/"06_Submissao/Arquivos_Finais").exists())

    def test_permitted_export_contains_rights_manifest_and_hash(self):
        result=self.invoke_export("--include-fulltext","--confirm-rights-review",
                                  "--no-record-export-event")
        self.assertEqual(result.returncode,0,result.stderr)
        packages=list((self.root/"06_Submissao/Arquivos_Finais").glob("RO_CRATE_*.zip"))
        self.assertEqual(len(packages),1)
        with zipfile.ZipFile(packages[0]) as z:
            listing=z.namelist()
            self.assertTrue(any(n.endswith("sample.pdf") for n in listing))
            mf=next(n for n in listing if n.endswith("FULLTEXT_RIGHTS.json"))
            report=json.loads(z.read(mf))
            self.assertEqual(report["documents"][0]["sha256"],self.row["Source_sha256"])
            self.assertFalse(report["legal_rights_independently_verified"])

    def test_nested_snapshot_archive_skipped_in_default_export(self):
        (self.mgmt/"archived.zip").write_bytes(b"nested licensed PDF placeholder")
        included=canonical_files(self.root,include_fulltext=False)
        self.assertFalse(any(p.name=="archived.zip" for p in included))

    def test_rights_audit_does_not_claim_independent_legal_verification(self):
        audited=rights.audit_project(self.root,strict=True)
        self.assertEqual(audited["errors"],[])
        self.assertFalse(audited["rights_legally_verified"])
        self.assertEqual(audited["counts"]["exportable_documents"],1)


if __name__=="__main__":
    unittest.main()
