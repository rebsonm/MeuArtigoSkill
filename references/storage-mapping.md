# Canonical storage and workbook mapping

## Authority and synchronization

Resolve Google Drive first. The normal canonical backend is the Drive project workspace. Do not choose filesystem/Work storage merely because it is immediately available.

If Drive is not connected, request the connection and re-check it. If it is still unavailable, filesystem/Work may become canonical only after the user explicitly confirms that they want to continue without Drive. Record the authorization in PROJECT_CONFIG.json and CONTINUIDADE.md. Silence is not authorization.

Within the resolved storage backend, choose and record the canonical table representation: native spreadsheet or filesystem CSV tables. Never maintain two independent authorities.

When Drive is canonical, local CSV/JSON files are staging/processing copies unless explicitly synchronized back. A material change that exists only in Work/local output is not yet canonical. In an explicitly authorized `WORK_FALLBACK`, the local CSV/JSON files may be authoritative until migration. In native spreadsheet mode the mapped sheets hold canonical table data; export them to the exact CSV headers in scripts/init_project.py before running local scripts. Import script results back only after reconciling the export baseline.

The workbook generator creates a template; it does not implement bidirectional synchronization. The agent or an explicit adapter must map fields by name, preserve stable IDs and retain fields that have no visible counterpart. Never map columns by position.

| File in 00_Gestao_e_Continuidade | Workbook view | Key / main field correspondence |
|---|---|---|
| 00_Projeto.csv | 03_PROJETO | Field→Campo; Value→Valor; Updated→Última atualização |
| 01_Protocolo.csv | 05_PROTOCOLO | Item; Decision→Decisão; Rationale→Justificativa; Version→Versão |
| 02_Search_Log.csv | 06_BUSCAS | Search_ID; Literal_query→String literal; Records_found→Encontrados; Records_exported→Exportados |
| 03_Screening.csv | 07_SCREENING | Record_ID; Pass1_decision→Pass1; Pass2_decision→Pass2; Canonical_record_id→Canonical_ID |
| 04_FullText_Tracker.csv | 08_FULL_TEXT | Record_ID; Full_text_status→Status full text; Evidence_matrix_id→Evidence_ID |
| 05_Evidence_Matrix.csv | 09_MATRIZ_EVID | Evidence_ID; Citation→Citação; Supporting_locator→Locator; Epistemic_label→Rótulo epistêmico |
| 06_Journal_Dialogue.csv | No dedicated sheet | Preserve as auxiliary table; do not discard during export |
| 07_Normative_Corpus.csv | No dedicated sheet | Preserve as auxiliary table when applicable |
| 08_Synthesis_Log.csv | 10_SINTESE | Synthesis_ID; Category_or_theme→Tema / Categoria; Evidence_IDs |
| 09_Claims_Ledger.csv | 11_CLAIMS | Claim_ID; Claim_text→Claim / afirmação; Robustness_status→Robustez; Human_validation→Validação humana |
| 10_Submission_Checklist.csv | 13_SUBMISSAO | Item; Requirement→Requisito; Evidence_or_file→Evidência / arquivo |
| 11_CADA_Control.csv | 01_CADA | CADA_ID; Title→Tarefa; Assigned_to→Responsável; Next_action→Próxima ação; Deadline→Prazo; Status |
| 12_PM_Sync.csv | 14_PM_SYNC | CADA_ID + Provider; External_item_ID→External item ID |
| 13_Traceability_Log.csv | 02_LINHA_TEMPO | Trace_ID; Action_summary→Resumo da ação; Actor→Ator |
| 14_AI_Use_Log.csv | 12_USO_IA | AI_Use_ID; Human_review_method→Método de revisão humana; Human_decision→Decisão humana |
| 15_CADA_Dashboard.csv | 00_PAINEL | Metric/Value→derived dashboard indicators |
| 16_Interoperabilidade.csv | 16_INTEROPERABILIDADE | Export_ID; Package_SHA256→SHA-256 do pacote |
| 17_Decision_Log.csv | 17_DECISOES | DEC_ID; Decision→Decisão; Decided_by→Decidido por |
| 18_Human_Validation_Gates.csv | 18_VALIDACOES | GATE_ID; Validation_evidence→Evidência da validação |
| 19_Snapshots.csv | 19_SNAPSHOTS | SNAP_ID; Manifest_SHA256→SHA-256 do manifest |

04_EVIDENCIAS summarizes 09_MATRIZ_EVID and claims; do not edit it as an independent evidence source. 15_CONFIG contains controlled vocabularies. 20_MAPA_CORPUS is derived from validated corpus data, not an independent source of inclusion decisions.

Use scripts/init_project.py TABLES for complete machine headers and references/spreadsheet-template.md for complete visible labels. Additional scientific fields remain in the canonical backend and must survive a round trip even if the default workbook has no corresponding column. Ambiguous mappings require an explicit adapter decision, never silent field loss.

JOURNAL_PROFILE.json lives under 06_Submissao/Regras_da_Revista. ANONYMIZATION_PROFILE.json remains confidential in management storage. Project configuration is not inferred from decorative spreadsheet labels.

## Stage-boundary procedure

1. Record the storage policy/state, canonical backend, explicit fallback authorization when applicable, file/sheet links and baseline version or hash.
2. Read current state; update canonical rows by stable ID.
3. Refresh mapped views and verify row counts, IDs and critical fields.
4. Preserve unmapped fields and auxiliary tables; record last synchronized version in CONTINUIDADE.md.
5. On divergent edits, preserve both versions, stop synchronization of affected rows and record the conflict. Scientific conflicts need human judgment; never choose a winner solely by timestamp.
6. After reconciliation, record the material decision and new baseline. External task managers remain mirrors.

