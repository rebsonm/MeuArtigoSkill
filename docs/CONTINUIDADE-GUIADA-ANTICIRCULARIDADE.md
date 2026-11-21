# Guided research continuation and anti-loop evidence signal

**Status:** Read-only development candidate stacked on earlier methodology
consistency proposals. This is neither a published release nor part of the
scientifically frozen historical reference `v0.9.0-beta.6`.

## Verifiable baseline

- One authoritative route/task resolver already exists: `scripts/next_step_router.py`.
- One read-only restart projection exists: `scripts/research_resume_brief.py`.
- A separate presentation helper for recorded blockers already exists:
  `scripts/research_blocker_guide.py`.
- The prior restart text presents technical identifiers but has no explicit
  user-facing task exit criterion within its compact summary.
- TRACE already records some local execution attempts with hash-linked
  receipts. It cannot prove the semantics of every proposed research action.
- The preceding development branch passed 815 software tests; no real-user
  time, workload, confusion or productivity measure was available.

## Integration decision: presentation, not a new authority

The improvement remains in the existing restart projection; it does not
create another task register, another gate system or a second source of
truth. The existing router and panel still determine the next action.
Use the local CLI only for an expressly authorized local fallback:

```bash
python scripts/research_resume_brief.py PROJECT --format guided
python scripts/research_resume_brief.py PROJECT --format guided-json
python scripts/research_resume_brief.py PROJECT --format json
```

The guided response reports the observed state, recorded operational work
(not scientific validation), outstanding items, exactly one next action,
its reason and an exit criterion. The described criterion is not evidence
that it has been met. A completed manuscript is never inferred from an
absent task or structurally filled method fields.

All repository source instructions and CLI labels remain English-first.
The conversational Skill adapts its user-visible explanation to the
researcher's current language. Translating a message does not alter its
data source, permissions, gate status or scientific authority.

## Narrow anti-loop heuristic

The optional read-only warning reuses existing TRACE receipts and only
examines explicitly authorized, reconciled local fallback workspaces.
It considers the two latest TRACE entries for the *same current task*.
An anti-loop signal is possible only if all conditions hold:

1. Both local attempts have a `FAILED` or `PARTIAL` status, with
   a hash-linked receipt at the established TRACE receipt path.
2. Both attempts used the same allowlisted script, recorded script
   fingerprint, arguments fingerprint and recorded input state.
3. No output change occurred in either attempt and the recorded output
   state matches between attempts.
4. The task has not been classified as periodic/recurring/monitoring.
   Standard local validation and verification scripts are also exempt.
5. The original task remains active and no canonical reconciliation
   problem is present.

An exact match causes only a diagnostic suggestion: investigate the
obstacle before a third identical action, document new evidence or
change the approach through existing human authorization. It never
executes an action, alters the task, marks a gate approved, or prevents
a legitimate later attempt.

**Missing proof is not proof of circularity.** A changed input, script
version, declared arguments or relevant output remains eligible for
independent review. Local hash integrity does not authenticate the
actor, externally collected evidence, scientific suitability or real
cloud synchronization. Drive-canonical states require an actual
authorized connected read before any such conclusion.

## Proposed verification metrics

| Metric | Grounded prior state | Technical acceptance criterion |
| --- | --- | --- |
| One next action | Existing restart did not contain an explicit exit criterion | Exactly one action and one exit criterion per guided response |
| Duplicate researcher choices | Not empirically measured | A ready task must not be replaced by a redundant new method-choice prompt |
| Repeated unproductive attempts | No diagnostic in restart view | Warn only for two equivalent validated receipt-linked attempts |
| False positive after changed input | Not measured | New input fingerprint does not trigger a loop warning |
| False positive for recurring actions | Not measured | Skip declared recurring work and routine validation |
| Canonical Drive uncertainty | Local project alone is insufficient | No fake connected access or synchronization success |
| Parallel registers | Existing task/decision/TRACE ledgers | Zero additional canonical tables or gate families |
| Governance preservation | Human-reviewed gates already required | Zero automatic approvals or project writes |
| Regression | 815 tests in the previous branch | Full existing suite plus new synthetic tests must pass on final SHA |

No percentage reduction in friction, actual researcher productivity gain,
validated usability or improved paper quality is claimed by these tests.
CI test counts are factual only when a successful run is linked.

## Exit conditions and deliberately open work

The new view does not automatically award `COMPLETED` or
`COMPLETED_WITH_RESERVATIONS` to an entire study: this would require
actual deliverables and researcher decisions, including any mandatory
scientific gates. `BLOCKED` reflects real documented impediments only.

Later stages must address the following separately, without spawning
unnecessary authoritative subprojects:

- Extend repetition diagnostics beyond local scripts only where
  trustworthy equivalently scoped evidence is actually available.
- Support bounded completion with disclosed reservations, preserving
  all non-waivable scientific and ethical requirements.
- Trace documented dependencies among METHOD_PROFILE, DEC, TRACE,
  evidence, claims and explicitly versioned sources; explore hypothetical
  source removal without mutating the project.
- Exercise the full A–L acceptance matrix, then evaluate the
  experience with real researchers under appropriate study controls.

**Limit:** software tests do not constitute scientific validation,
user research or independent evidence of improved cognitive effort.
