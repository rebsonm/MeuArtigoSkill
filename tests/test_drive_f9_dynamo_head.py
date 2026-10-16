"""F9 DynamoDB CAS contract tests with a simulated in-memory wire client."""
from __future__ import annotations

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import drive_f9_dynamo_head as dynamo

INITIAL = "a" * 64
NEXT = "b" * 64
TABLE = "MeuArtigoTrustedHeads"
PROJECT_KEY = "synthetic-project-audit-root"


class FakeAwsError(Exception):
    def __init__(self, code):
        super().__init__("synthetic error not for logs")
        self.response = {"Error": {"Code": code}}


class FakeDynamoClient:
    def __init__(self):
        self.head = INITIAL
        self.reads = []
        self.writes = []
        self.fail_read = False
        self.fail_write = None
        self.bad_return = False

    def get_item(self, **kw):
        self.reads.append(kw)
        if self.fail_read:
            raise FakeAwsError("ThrottlingException")
        if self.head is None:
            return {}
        return {"Item": {"HeadSha256": {"S": self.head}}}

    def update_item(self, **kw):
        self.writes.append(kw)
        if self.fail_write:
            raise FakeAwsError(self.fail_write)
        old = kw["ExpressionAttributeValues"][":prev"]["S"]
        new = kw["ExpressionAttributeValues"][":next"]["S"]
        if old != self.head:
            raise FakeAwsError("ConditionalCheckFailedException")
        self.head = new
        return {"Attributes": {"HeadSha256": {"S": "f" * 64 if self.bad_return else new}}}


class DynamoBackendTests(unittest.TestCase):
    def setUp(self):
        self.client = FakeDynamoClient()
        self.store = dynamo.DynamoHeadStore(TABLE, PROJECT_KEY, self.client)

    def test_strongly_consistent_read(self):
        self.assertEqual(self.store.read_head(), INITIAL)
        self.assertTrue(self.client.reads[0]["ConsistentRead"])
        self.assertEqual(self.client.reads[0]["TableName"], TABLE)
        self.assertEqual(self.client.reads[0]["Key"]["ProjectKey"]["S"], PROJECT_KEY)

    def test_conditional_cas_succeeds_and_reads_new_head(self):
        self.assertTrue(self.store.compare_and_set(INITIAL, NEXT))
        self.assertEqual(self.store.read_head(), NEXT)
        call = self.client.writes[0]
        self.assertIn("attribute_exists", call["ConditionExpression"])
        self.assertIn("#head = :prev", call["ConditionExpression"])
        self.assertEqual(call["ReturnValues"], "ALL_NEW")

    def test_stale_concurrent_writer_is_rejected(self):
        self.assertTrue(self.store.compare_and_set(INITIAL, NEXT))
        self.assertFalse(self.store.compare_and_set(INITIAL, "c"*64))
        self.assertEqual(self.client.head, NEXT)

    def test_missing_item_does_not_create_it(self):
        self.client.head = None
        with self.assertRaisesRegex(dynamo.DynamoTrustError, "F9_TRUSTED_HEAD_INVALID"):
            self.store.read_head()
        self.assertFalse(self.store.compare_and_set(INITIAL, NEXT))
        self.assertIsNone(self.client.head)

    def test_transport_timeout_does_not_claim_cas_false(self):
        self.client.fail_write = "ProvisionedThroughputExceededException"
        with self.assertRaisesRegex(dynamo.DynamoTrustError, "F9_TRUST_WRITE_UNVERIFIED"):
            self.store.compare_and_set(INITIAL, NEXT)

    def test_permission_denied_refuses(self):
        self.client.fail_read = True
        with self.assertRaisesRegex(dynamo.DynamoTrustError, "F9_TRUST_READ_UNVERIFIED"):
            self.store.read_head()

    def test_post_update_response_mismatch_refuses(self):
        self.client.bad_return = True
        with self.assertRaisesRegex(dynamo.DynamoTrustError, "F9_TRUST_WRITE_RESPONSE_MISMATCH"):
            self.store.compare_and_set(INITIAL, NEXT)

    def test_noop_cas_forbidden(self):
        with self.assertRaisesRegex(dynamo.DynamoTrustError, "F9_NOOP_HEAD_UPDATE_FORBIDDEN"):
            self.store.compare_and_set(INITIAL, INITIAL)
        self.assertEqual(len(self.client.writes), 0)

    def test_invalid_head_rejected_before_request(self):
        with self.assertRaisesRegex(dynamo.DynamoTrustError, "F9_TRUSTED_HEAD_INVALID"):
            self.store.compare_and_set("untrusted", NEXT)
        self.assertFalse(self.client.writes)

    def test_bad_scope_cannot_contact_dynamo(self):
        with self.assertRaisesRegex(dynamo.DynamoTrustError, "F9_TRUST_SCOPE_INVALID"):
            dynamo.DynamoHeadStore(TABLE, "too short", self.client)
        self.assertFalse(self.client.reads)

    def test_bad_table_name_refused(self):
        with self.assertRaisesRegex(dynamo.DynamoTrustError, "F9_TRUST_TABLE_INVALID"):
            dynamo.DynamoHeadStore("weird table", PROJECT_KEY, self.client)

    def test_absent_client_refused(self):
        with self.assertRaisesRegex(dynamo.DynamoTrustError, "F9_CLIENT_REQUIRED"):
            dynamo.DynamoHeadStore(TABLE, PROJECT_KEY, None)

    def test_region_syntax_does_not_infer_credentials(self):
        with self.assertRaisesRegex(dynamo.DynamoTrustError, "F9_REGION_REQUIRED"):
            dynamo.authorized_client(region_name="invalid region!")

if __name__ == "__main__":
    unittest.main()
