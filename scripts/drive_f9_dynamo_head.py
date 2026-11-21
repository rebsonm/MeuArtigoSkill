#!/usr/bin/env python3
"""F9 optional DynamoDB trusted-head adapter for F8's external CAS contract.

No table provisioning, IAM mutation or automatic initialization. An operator
must provision a *separate* DynamoDB table keyed by ProjectKey (string) and
preinitialize one trusted HeadSha256 (string) for an already provisioned F7
receipt before this adapter is usable. AWS boto3 is optional and imported
only by explicit authorized external host configuration.

No AWS credentials, endpoint URLs or account identifiers are stored in code.
"""
from __future__ import annotations

import hashlib
import json
import re
import drive_delivery as delivery
from drive_delivery import HASH

TABLE = re.compile(r"[A-Za-z0-9_.-]{3,255}\Z")
PROJECT_KEY = re.compile(r"[A-Za-z0-9_.:/#-]{10,256}\Z")


class DynamoTrustError(ValueError):
    """Fixed error only; never echo table details or provider exception bodies."""


def validate_sha(value: str) -> str:
    if not isinstance(value, str) or not HASH.fullmatch(value):
        raise DynamoTrustError("F9_TRUSTED_HEAD_INVALID")
    return value


def scoped_key(plan: dict, audit_parent_id: str, audit_file_id: str) -> str:
    """Stable identity for one exact plan and one provisioned journal file.

    A pre-provisioned trusted head must be created separately using the same
    digest. This helper itself never creates or modifies any AWS item.
    """
    delivery.check_plan(plan)
    parent = delivery.require_drive_id(audit_parent_id)
    file_id = delivery.require_drive_id(audit_file_id)
    payload = {
        "purpose": "MEU_ARTIGO_TRUSTED_HEAD_F9_V1",
        "drive_root_id": plan["drive_root_id"],
        "plan": hashlib.sha256(json.dumps(
            plan, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
        "audit_parent_id": parent, "audit_file_id": file_id,
    }
    return "ma-f9-" + hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


class DynamoHeadStore:
    """Single-scoped, strongly consistent read and conditional update.

    client is a boto3 DynamoDB low-level client (AttributeValue shape).
    The caller owns IAM, credentials, encryption and table provisioning.
    """

    def __init__(self, table: str, project_key: str, client):
        if not isinstance(table, str) or not TABLE.fullmatch(table):
            raise DynamoTrustError("F9_TRUST_TABLE_INVALID")
        if not isinstance(project_key, str) or not PROJECT_KEY.fullmatch(project_key):
            raise DynamoTrustError("F9_TRUST_SCOPE_INVALID")
        if client is None:
            raise DynamoTrustError("F9_CLIENT_REQUIRED")
        self.table = table
        self.project_key = project_key
        self.client = client

    def _key(self):
        return {"ProjectKey": {"S": self.project_key}}

    def read_head(self) -> str:
        try:
            res = self.client.get_item(
                TableName=self.table, Key=self._key(),
                ConsistentRead=True,
                ProjectionExpression="#head",
                ExpressionAttributeNames={"#head": "HeadSha256"})
        except Exception:
            raise DynamoTrustError("F9_TRUST_READ_UNVERIFIED") from None
        item = res.get("Item") if isinstance(res, dict) else None
        entry = item.get("HeadSha256") if isinstance(item, dict) else None
        head = entry.get("S") if isinstance(entry, dict) else None
        return validate_sha(head)

    def compare_and_set(self, previous_head: str, new_head: str) -> bool:
        validate_sha(previous_head)
        validate_sha(new_head)
        if previous_head == new_head:
            raise DynamoTrustError("F9_NOOP_HEAD_UPDATE_FORBIDDEN")
        try:
            result = self.client.update_item(
                TableName=self.table, Key=self._key(),
                UpdateExpression="SET #head = :next",
                ConditionExpression="attribute_exists(#pk) AND #head = :prev",
                ExpressionAttributeNames={
                    "#pk": "ProjectKey", "#head": "HeadSha256"},
                ExpressionAttributeValues={
                    ":prev": {"S": previous_head}, ":next": {"S": new_head}},
                ReturnValues="ALL_NEW",
            )
        except Exception as e:
            # Only the narrow conditional conflict code is a normal CAS false;
            # timeouts and transport failures are ambiguous and MUST stop.
            response = getattr(e, "response", None)
            err = response.get("Error", {}) if isinstance(response, dict) else {}
            if isinstance(err, dict) and err.get("Code") == "ConditionalCheckFailedException":
                return False
            raise DynamoTrustError("F9_TRUST_WRITE_UNVERIFIED") from None
        attrs = result.get("Attributes") if isinstance(result, dict) else None
        entry = attrs.get("HeadSha256") if isinstance(attrs, dict) else None
        reported = entry.get("S") if isinstance(entry, dict) else None
        if reported != new_head:
            raise DynamoTrustError("F9_TRUST_WRITE_RESPONSE_MISMATCH")
        # Do not infer global success from UpdateItem's response alone.
        # The F8 caller separately re-reads with ConsistentRead=True.
        return True


def authorized_client(*, region_name: str):
    """Explicit, separate operator initialization; never read from ChatGPT."""
    if not isinstance(region_name, str) or not re.fullmatch(r"[a-z]{2}-[a-z-]+-\d", region_name):
        raise DynamoTrustError("F9_REGION_REQUIRED")
    try:
        import boto3
    except ImportError:
        raise DynamoTrustError("F9_BOTO3_NOT_INSTALLED") from None
    return boto3.client("dynamodb", region_name=region_name)
