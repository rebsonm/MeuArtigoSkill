# C.A.D.A. — research work management

**C.A.D.A.** organizes the operational side of an article: **Capture, Assign, Define a deadline, Accompany/Track** (*Capturar, Atribuir, Definir prazo, Acompanhar*). It is a **management method**, not a substitute for methodological validity.

## The four actions

1. **Capture:** register a verifiable task, dependency or issue (for example, review borderline records).
2. **Assign:** establish an execution owner and dependencies; distinguish technical preparation from consequential scientific judgment.
3. **Define a deadline:** differentiate an official external deadline from a researcher-defined target, an internal goal or a dependency.
4. **Accompany:** record progress and actual completion evidence; unresolved items remain visibly blocked.

A task such as "verify WoS export" may generate several provenance events. The task's `CADA_ID` organizes responsibility; the `TRACE_ID` events support what was actually done.

## Compact task view

| ID Tarefa | Tarefa | Responsável execução | Prazo |
| --- | --- | --- | --- |
| `CADA-0001` | Review original research question | Researcher | To define |
| `CADA-0002` | Check real search export | Researcher/authorized assistant | After export |

*Illustration only — not a record from a real research project.* The current native ChatGPT compact projection uses **exactly these four columns**. Details such as status, evidence and blocks remain in the canonical register, not additional columns of the compact view.

## Default organization

`MATRIX_ONLY` makes the canonical research spreadsheet and its C.A.D.A. register the default source of truth. ClickUp, Jira and Trello may optionally **mirror** tasks, but may not silently replace scientific records or human gate decisions.

An item marked `DONE` with no supporting work product does not establish completion of the corresponding science. The next-step router may surface a legitimate task and a blocker, but cannot authorize external actions or pass gates on its own.

**Reference:** [C.A.D.A. user guide](https://github.com/rebsonm/MeuArtigoSkill/blob/main/docs/CADA.md) · [Matrix](https://github.com/rebsonm/MeuArtigoSkill/blob/main/docs/MATRIZ-CADA.md) · [Limits](https://github.com/rebsonm/MeuArtigoSkill/blob/main/docs/LIMITES-CADA-E-COMPARACAO.md) · [[Storage and continuity|Storage-and-Continuity]].
