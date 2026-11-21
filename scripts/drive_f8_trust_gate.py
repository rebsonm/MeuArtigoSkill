#!/usr/bin/env python3
"""F8 host trust gate between F7 signed receipts and F5 synthetic create.

No Drive mutations here. TrustedHeadBackend must be furnished by an
INDEPENDENT authorized executor providing a durable, atomic compare-and-set
high-watermark with readback. A local file or in-memory fake is NOT such an
authority; tests may use fakes, but the real CLI has no enabled backend.
Without the head backend this module always blocks before CREATE.
"""
from __future__ import annotations

from pathlib import Path
from typing import Protocol

import drive_delivery as delivery
import drive_f7_anchor as anchor
import drive_journal_checkpoint as checkpoint


class TrustGateError(ValueError):
    """Fixed error codes safe for logging; never echo secret or token."""


class TrustedHeadBackend(Protocol):
    def read_head(self) -> str:
        """Read the latest committed receipt hash from durable external store."""
        ...

    def compare_and_set(self, previous_head: str, new_head: str) -> bool:
        """Atomically persist the next head iff current equals previous."""
        ...


def head_from_backend(store: TrustedHeadBackend) -> str:
    if store is None:
        raise TrustGateError("F8_TRUSTED_HEAD_BACKEND_REQUIRED")
    try:
        head = store.read_head()
    except Exception:
        raise TrustGateError("F8_TRUSTED_HEAD_READ_FAILED") from None
    if not isinstance(head, str) or not delivery.HASH.fullmatch(head):
        raise TrustGateError("F8_TRUSTED_HEAD_INVALID")
    return head


def require_configuration(store: TrustedHeadBackend, archive: Path,
                          key: bytes) -> None:
    """Reject missing credentials/anchor config BEFORE any remote writes."""
    if store is None:
        raise TrustGateError("F8_TRUSTED_HEAD_BACKEND_REQUIRED")
    if archive is None:
        raise TrustGateError("F8_SIGNED_ARCHIVE_REQUIRED")
    if not isinstance(key, bytes) or len(key) < 32:
        raise TrustGateError("F8_HMAC_KEY_REQUIRED")
    if not isinstance(archive, Path):
        raise TrustGateError("F8_SIGNED_ARCHIVE_REQUIRED")


def verify_current(store: TrustedHeadBackend, archive: Path, key: bytes,
                   project_root: Path, plan: dict, audit_parent: str,
                   audit_file: str, token: str, expected_journal_sha: str, *,
                   sender=checkpoint.request) -> str:
    """Check trusted latest head, full signed chain AND current remote bytes."""
    require_configuration(store, archive, key)
    head = head_from_backend(store)
    verified = anchor.verify_remote_against_anchor(
        archive, project_root, plan, audit_parent, audit_file,
        token, head, key, sender=sender)
    if verified["journal_sha256"] != expected_journal_sha:
        raise TrustGateError("F8_ANCHORED_REMOTE_SHA_MISMATCH")
    return head


def pin_checkpoint(store: TrustedHeadBackend, archive: Path, key: bytes,
                   project_root: Path, plan: dict, audit_parent: str,
                   audit_file: str, token: str, previous_head: str,
                   next_journal_sha: str, *, sender=checkpoint.request) -> str:
    """Seal a fetched remote journal; require CAS and exact head readback.

    If a receipt is sealed but CAS fails, the chain is intentionally left
    ahead of the external head. This blocks recovery and all future creates
    until the operator reconciles the event safely (never blind rollback).
    """
    require_configuration(store, archive, key)
    if head_from_backend(store) != previous_head:
        raise TrustGateError("F8_TRUSTED_HEAD_CHANGED")
    sealed = anchor.seal_remote_checkpoint(
        archive, project_root, plan, audit_parent, audit_file, token,
        next_journal_sha, key, previous_head, sender=sender)
    new_head = sealed["head_sha256"]
    try:
        accepted = store.compare_and_set(previous_head, new_head)
    except Exception:
        raise TrustGateError("F8_TRUSTED_HEAD_CAS_FAILED") from None
    if accepted is not True:
        raise TrustGateError("F8_TRUSTED_HEAD_CAS_REJECTED")
    if head_from_backend(store) != new_head:
        raise TrustGateError("F8_TRUSTED_HEAD_READBACK_MISMATCH")
    confirmed = anchor.verify_remote_against_anchor(
        archive, project_root, plan, audit_parent, audit_file,
        token, new_head, key, sender=sender)
    if confirmed["journal_sha256"] != next_journal_sha:
        raise TrustGateError("F8_ANCHORED_REMOTE_SHA_MISMATCH")
    return new_head
