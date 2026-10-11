"""Conservative cross-operation interlock for local research journals.

The three existing journals protect overlapping canonical registers. Their
presence blocks OTHER operations and recovery so two workflows cannot
silently clobber each other's scientific or bibliographic state. A journal
is not a multi-process mutex: independent direct file writers are outside
this protocol. No remote Drive or human authenticity guarantee is made.
"""
from __future__ import annotations

from pathlib import Path

MGMT = "00_Gestao_e_Continuidade"
JOURNALS = {
    "bibliographic": ".pending_bibliographic_import",
    "method_route": ".pending_method_route_change",
    "gate_snapshot": ".pending_gate_snapshot",
    "cada_continuity": ".pending_cada_continuity",
}


class ConflictingResearchTransaction(ValueError):
    """A distinct pending journal requires explicit reconciliation."""


def active_journals(root: Path) -> set[str]:
    mgmt = Path(root) / MGMT
    return {name for name, marker in JOURNALS.items()
            if (mgmt / marker).exists() or (mgmt / marker).is_symlink()}


def require_no_conflict(root: Path, *, allow: tuple[str, ...] = ()) -> None:
    active = active_journals(root) - set(allow)
    if active:
        raise ConflictingResearchTransaction(
            "OTHER_PENDING_RESEARCH_TRANSACTION_REQUIRES_RECOVERY: "
            + ", ".join(sorted(active)))
