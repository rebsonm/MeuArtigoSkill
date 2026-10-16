"""Etapa 08 — falhas adversariais F5–F9, exclusivamente sintéticas.

Nenhuma credencial, operação Drive ou AWS real é utilizada nestes testes.
"""
from __future__ import annotations
import hashlib
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import drive_create_guard as guard
import drive_f5_operator as operator
import drive_f7_anchor as anchor
import drive_f8_trust_gate as gate
import drive_f9_dynamo_head as dynamo
from test_drive_f5_operator import F5HostTests
from test_drive_f9_dynamo_head import (
    FakeDynamoClient, FakeAwsError, INITIAL, NEXT, TABLE, PROJECT_KEY
)


class Stage08AdversarialTests(unittest.TestCase):
    def harness(self):
        case = F5HostTests("test_default_read_only_no_intent_or_external_create")
        case.setUp()
        self.addCleanup(case.doCleanups)
        return case

    def test_unexpected_creator_exception_after_effect_resolves_once(self):
        case = self.harness()
        original = case.drive.creator
        def unexpected(*args, **kwargs):
            original(*args, **kwargs)
            raise RuntimeError("fictional sensitive exception, do not leak")
        case.drive.creator = unexpected
        result = case.run_flow(execute=True)
        self.assertEqual(result["action"], "VERIFIED_SINGLE_SYNTHETIC_CREATE")
        self.assertTrue(result["create_return_was_ambiguous"])
        self.assertEqual(case.drive.posts, 1)
        self.assertEqual(case.trusted_head.cas_calls, 2)

    def test_unexpected_creator_exception_without_effect_blocks_retry(self):
        case = self.harness()
        case.drive.create_effect = False
        original = case.drive.creator
        def unexpected(*args, **kwargs):
            original(*args, **kwargs)
            raise RuntimeError("fictional transport timeout")
        case.drive.creator = unexpected
        result = case.run_flow(execute=True)
        self.assertEqual(result["action"], "BLOCKED_AMBIGUOUS_OUTCOME")
        self.assertEqual(case.drive.posts, 1)
        again = case.run_flow(execute=True)
        self.assertEqual(again["action"],
                         "BLOCKED_PREVIOUS_CREATE_INTENT_REQUIRES_RECONCILIATION")
        self.assertEqual(case.drive.posts, 1)

    def test_foreign_lock_replacement_is_never_unlinked(self):
        case = self.harness()
        original = case.drive.creator
        lock = case.journal_path.with_name(case.journal_path.name + ".f5-host.lock")
        def replaced(*args, **kwargs):
            result = original(*args, **kwargs)
            # A separately allocated inode is renamed over the current lock.
            # unlink()+create could reuse the same inode and invalidate the test.
            replacement = lock.with_name(lock.name + ".foreign")
            replacement.write_text("foreign-worker-ownership", encoding="utf-8")
            replacement.replace(lock)
            return result
        case.drive.creator = replaced
        with self.assertRaisesRegex(operator.HostBlock, "HOST_LOCK_OWNERSHIP_LOST"):
            case.run_flow(execute=True)
        self.assertEqual(lock.read_text(encoding="utf-8"), "foreign-worker-ownership")
        self.assertEqual(case.drive.posts, 1)
        self.assertEqual(guard.read_journal(case.plan,case.journal_path)
                         ["operations"]["01_Dados"]["state"], "OUTCOME_UNKNOWN")

    def test_post_create_scan_unexpected_failure_is_sanitized_and_no_retry(self):
        case = self.harness()
        fetch = case.drive.fetch_page
        calls = []
        def broken(*args, **kwargs):
            calls.append(1)
            if len(calls) == 3:
                raise RuntimeError("fictional private response details")
            return fetch(*args, **kwargs)
        case.drive.fetch_page = broken
        with self.assertRaisesRegex(operator.HostBlock,
                                    "POST_CREATE_RECONCILIATION_BLOCKED"):
            case.run_flow(execute=True)
        self.assertEqual(case.drive.posts, 1)
        self.assertEqual(guard.read_journal(case.plan,case.journal_path)
                         ["operations"]["01_Dados"]["state"], "OUTCOME_UNKNOWN")

    def test_cas_timeout_after_remote_write_still_blocks_external_create(self):
        case = self.harness()
        def ambiguous(previous, next_head):
            case.trusted_head.current = next_head
            case.trusted_head.cas_calls += 1
            raise TimeoutError("fictional Dynamo response lost after write")
        case.trusted_head.compare_and_set = ambiguous
        with self.assertRaisesRegex(gate.TrustGateError, "CAS_FAILED"):
            case.run_flow(execute=True)
        self.assertEqual(case.drive.posts, 0)
        self.assertEqual(case.drive.patch_count, 1)
        self.assertEqual(len(list(case.anchor_archive.iterdir())), 2)
        result = case.run_flow(execute=True)
        self.assertEqual(result["action"],
                         "BLOCKED_PREVIOUS_CREATE_INTENT_REQUIRES_RECONCILIATION")
        self.assertEqual(case.drive.posts, 0)

    def test_old_hmac_receipt_replay_with_new_trusted_head_fails(self):
        case = self.harness()
        case.run_flow(execute=True)
        old_head = hashlib.sha256((case.anchor_archive / "00000001.json").read_bytes()).hexdigest()
        with self.assertRaisesRegex(anchor.AnchorError, "TRUSTED_HEAD_MISMATCH"):
            anchor.read_verified_chain(case.anchor_archive,case.plan,
                case.AUDIT_PARENT if hasattr(case,"AUDIT_PARENT") else "synthetic-audit-0001",
                "synthetic-file-00001",bytes(range(32)),case.project,old_head)
        self.assertEqual(case.drive.posts,1)

    def test_f9_two_writers_observing_same_head_only_one_cas_wins(self):
        shared=FakeDynamoClient()
        first=dynamo.DynamoHeadStore(TABLE,PROJECT_KEY,shared)
        second=dynamo.DynamoHeadStore(TABLE,PROJECT_KEY,shared)
        head_a=first.read_head()
        head_b=second.read_head()
        self.assertEqual(head_a,head_b)
        self.assertTrue(first.compare_and_set(head_a,NEXT))
        self.assertFalse(second.compare_and_set(head_b,"c"*64))
        self.assertEqual(second.read_head(),NEXT)
        self.assertEqual(len(shared.writes),2)

    def test_f9_cas_timeout_after_remote_effect_is_ambiguous(self):
        class Ambiguous(FakeDynamoClient):
            def update_item(self,**kwargs):
                super().update_item(**kwargs)
                raise FakeAwsError("ProvisionedThroughputExceededException")
        shared=Ambiguous()
        store=dynamo.DynamoHeadStore(TABLE,PROJECT_KEY,shared)
        with self.assertRaisesRegex(dynamo.DynamoTrustError,"F9_TRUST_WRITE_UNVERIFIED"):
            store.compare_and_set(INITIAL,NEXT)
        self.assertEqual(store.read_head(),NEXT)

    def test_f9_nonmapping_attribute_value_does_not_crash_or_pass(self):
        class Broken(FakeDynamoClient):
            def get_item(self,**kwargs):
                return {"Item":{"HeadSha256":"not-an-attribute-map"}}
        store=dynamo.DynamoHeadStore(TABLE,PROJECT_KEY,Broken())
        with self.assertRaisesRegex(dynamo.DynamoTrustError,"F9_TRUSTED_HEAD_INVALID"):
            store.read_head()

    def test_f9_nonmapping_write_response_blocks(self):
        class Broken(FakeDynamoClient):
            def update_item(self,**kwargs):
                super().update_item(**kwargs)
                return {"Attributes":{"HeadSha256":"not-a-map"}}
        store=dynamo.DynamoHeadStore(TABLE,PROJECT_KEY,Broken())
        with self.assertRaisesRegex(dynamo.DynamoTrustError,"F9_TRUST_WRITE_RESPONSE_MISMATCH"):
            store.compare_and_set(INITIAL,NEXT)

    def test_f9_nonmapping_error_envelope_is_sanitized(self):
        class Malformed(Exception):
            def __init__(self):
                self.response={"Error":"not-a-map"}
        class Broken(FakeDynamoClient):
            def update_item(self,**kwargs):
                raise Malformed()
        store=dynamo.DynamoHeadStore(TABLE,PROJECT_KEY,Broken())
        with self.assertRaisesRegex(dynamo.DynamoTrustError,"F9_TRUST_WRITE_UNVERIFIED"):
            store.compare_and_set(INITIAL,NEXT)

    def test_f9_missing_item_does_not_bootstrap_it(self):
        client=FakeDynamoClient()
        client.head=None
        store=dynamo.DynamoHeadStore(TABLE,PROJECT_KEY,client)
        with self.assertRaisesRegex(dynamo.DynamoTrustError,"F9_TRUSTED_HEAD_INVALID"):
            store.read_head()
        self.assertFalse(store.compare_and_set(INITIAL,NEXT))
        self.assertIsNone(client.head)

    def test_f5_read_only_never_reserves_intent(self):
        case=self.harness()
        result=case.run_flow(execute=False)
        self.assertEqual(result["action"],"PRECHECK_ONLY_NO_CREATE")
        self.assertEqual(case.drive.posts,0)
        self.assertEqual(case.drive.patch_count,0)
        self.assertEqual(guard.read_journal(case.plan,case.journal_path)
                        ["operations"],{})

    def test_f8_without_backend_fails_before_any_drive_io(self):
        case=self.harness()
        with self.assertRaisesRegex(gate.TrustGateError,
                                    "F8_TRUSTED_HEAD_BACKEND_REQUIRED"):
            operator.guarded_synthetic_create(
                case.plan,case.journal_path,case.project,"01_Dados",
                "synthetic-audit-0001","synthetic-file-00001",
                "fake-credential-is-not-real",
                hashlib.sha256(case.drive.journal).hexdigest(),
                execute=True,
                trusted_head=None,anchor_archive=case.anchor_archive,
                anchor_key=bytes(range(32)),
                fetch_page=case.drive.fetch_page,
                sender=case.drive.sender,creator=case.drive.creator)
        self.assertEqual(case.drive.posts,0)
        self.assertEqual(case.drive.patch_count,0)

if __name__ == "__main__":
    unittest.main()
