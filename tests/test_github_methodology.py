"""No-network checks for opt-in bounded, immutable GitHub methodology cards."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import consult_github_methodology as mod
REF = "a" * 40
BASE = ROOT / "knowledge" / "methodology"

class RemoteMethodologyTests(unittest.TestCase):
    def fixture(self, *, tamper=False):
        catalog=(BASE / "catalog.json").read_bytes()
        files={mod.INDEX_PATH:catalog}
        d=json.loads(catalog)
        for doc in d["documents"]:
            files[doc["path"]]=(ROOT / doc["path"]).read_bytes()
        if tamper:
            p=d["documents"][0]["path"]
            files[p] += b"bad"
        calls=[]
        def fetch(ref, path, limit):
            self.assertEqual(ref, REF)
            calls.append(path)
            return files[path]
        return fetch, calls

    def test_fetch_only_matching_cards_with_bounded_context(self):
        fetch,calls=self.fixture()
        result=mod.query("revisão integrativa da literatura",ref=REF,fetch=fetch,max_chars=900)
        self.assertEqual(result["status"],"RETRIEVED")
        self.assertEqual(result["hits"][0]["path"],"knowledge/methodology/cards/reviews.md")
        self.assertEqual(len(calls),2)
        self.assertLessEqual(result["returned_context_chars"],900)
        self.assertFalse(result["scientific_quality_validated"])

    def test_no_match_does_not_fetch_documents(self):
        fetch,calls=self.fixture()
        result=mod.query("meteorologia quasar elipse",ref=REF,fetch=fetch)
        self.assertEqual(result["status"],"NO_MATCH_IN_CATALOG")
        self.assertEqual(calls,[mod.INDEX_PATH])

    def test_reject_moving_branch(self):
        fetch,calls=self.fixture()
        with self.assertRaisesRegex(ValueError,"PINNED_40_HEX"):
            mod.query("revisão",ref="main",fetch=fetch)
        self.assertEqual(calls,[])

    def test_catalog_path_escape_blocked(self):
        fetch,calls=self.fixture()
        def evil(ref,path,limit):
            data=fetch(ref,path,limit)
            if path==mod.INDEX_PATH:
                v=json.loads(data)
                v["documents"][0]["path"]="../../credentials.md"
                return json.dumps(v).encode()
            return data
        with self.assertRaisesRegex(ValueError,"CATALOG_PATH_INVALID"):
            mod.query("revisão",ref=REF,fetch=evil)

    def test_remote_hash_mismatch_blocked(self):
        fetch,calls=self.fixture(tamper=True)
        with self.assertRaisesRegex(ValueError,"REMOTE_DIGEST_MISMATCH"):
            mod.query("revisão integrativa",ref=REF,fetch=fetch)

    def test_rights_not_approved_blocked(self):
        fetch,calls=self.fixture()
        def evil(ref,path,limit):
            data=fetch(ref,path,limit)
            if path==mod.INDEX_PATH:
                v=json.loads(data)
                v["documents"][0]["rights"]="PRIVATE_AUTHORIZED"
                return json.dumps(v).encode()
            return data
        with self.assertRaisesRegex(ValueError,"CATALOG_RIGHTS_NOT_REVIEWED"):
            mod.query("revisão",ref=REF,fetch=evil)

    def test_cache_reuse_and_tamper_detection(self):
        fetch,calls=self.fixture()
        h=hashlib.sha256((BASE / "catalog.json").read_bytes()).hexdigest()
        with tempfile.TemporaryDirectory() as temp:
            cache=Path(temp)
            mod.query("revisão integrativa",ref=REF,fetch=fetch,cache_dir=cache,catalog_sha256=h)
            calls.clear()
            mod.query("revisão integrativa",ref=REF,fetch=fetch,cache_dir=cache,catalog_sha256=h)
            self.assertEqual(calls,[])
            candidates=list(cache.glob("*.cache"))
            self.assertEqual(len(candidates),2)
            candidates[0].write_bytes(b"changed")
            with self.assertRaisesRegex(ValueError,"CACHE_DIGEST_MISMATCH"):
                mod.query("revisão integrativa",ref=REF,fetch=fetch,cache_dir=cache,catalog_sha256=h)

    def test_limits_and_original_public_cards_only(self):
        fetch,calls=self.fixture()
        with self.assertRaisesRegex(ValueError,"QUESTION_INVALID"):
            mod.query("a"*1000,ref=REF,fetch=fetch)
        with self.assertRaisesRegex(ValueError,"CONTEXT_BUDGET_INVALID"):
            mod.query("revisão",ref=REF,max_chars=10000,fetch=fetch)
        data=json.loads((BASE/"catalog.json").read_text())
        self.assertFalse(data["contains_third_party_full_text"])
        for x in (ROOT/"knowledge").rglob("*"):
            if x.is_file():
                self.assertIn(x.suffix,{".md",".json"})

if __name__=="__main__":
    unittest.main()
