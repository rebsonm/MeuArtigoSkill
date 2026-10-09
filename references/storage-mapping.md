<a id="canonical-storage-and-workbook-mapping"></a>
# Canonical storage and workbook mapping

<a id="authority-and-synchronization"></a>
## Authority and synchronization

Resolve Google Drive first. The normal canonical backend is the Drive project workspace. Do not choose filesystem/Work storage merely because it is immediately available.

If Drive is not connected, request the connection and re-check it. If it is still unavailable, filesystem/Work may become canonical only after the user explicitly confirms that they want to continue without Drive. Record the authorization in PROJECT_CONFIG.json and CONTINUIDADE.md. Silence is not authorization.

Within the resolved storage backend, choose and record the canonical table representation: native spreadsheet or filesystem CSV tables. Never maintain two independent authorities.

When Drive is canonical, local CSV/JSON files are staging/processing copies unless explicitly synchronized back. A material change that exists only in Work/local output is not yet canonical. In an explicitly authorized `WORK_FALLBACK`, the local CSV/JSON files may be authoritative until migration. In native spreadsheet mode the mapped sheets hold canonical table data; export them to the exact CSV headers in scripts/init_project.py before running local scripts. Import script results back only after reconciling the export baseline.

The workbook generator creates a template; it does not implement bidirectional synchronization. The agent or an explicit adapter must map fields by name, preserve stable IDs and retain fields that have no visible counterpart. Never map columns by position.

| File in 00_Gestao_e_Continuidade | Workbook view | Key / main field correspondence |
|---|---|---|
| 00_Projeto.csv | 03_PROJECT | Field→Field; Value→Value; Updated→Last updated |
| 01_Protocol.csv | 05_PROTOCOL | Item; Decision→Decision; Rationale→Justification; Version→Version |
| 02_Search_Log.csv | 06_SEARCH | Search_ID; Literal_query→String literal; Records_found→Found; Records_exported→Exported |
| 03_Screening.csv | 07_SCREENING | Record_ID; Pass1_decision→Pass1; Pass2_decision→Pass2; Canonical_record_id→Canonical_ID |
| 04_FullText_Tracker.csv | 08_FULL_TEXT | Record_ID; Full_text_status→Status full text; Evidence_matrix_id→Evidence_ID; Access_basis→Access base; Rights_basis→Rights base; License_URI→license URI; Rights_evidence→Evidence of rights; Source_sha256→SHA-256 source; Rights_reviewed_by→Rights Reviewer |
| 05_Evidence_Matrix.csv | 09_MATRIZ_EVID | Evidence_ID; Citation→Quote; Supporting_locator→Locator; Epistemic_label→Epistemic label |
| 06_Journal_Dialogue.csv | No dedicated sheet | Preserve the auxiliary tables; do not discard during export |
| 07_Normative_Corpus.csv | No dedicated sheet | Preserve the auxiliary table when applicable |
| 08_Synthesis_Log.csv | 10_SYNTHESIS | Synthesis_ID; Category_or_theme→Theme / Category; Evidence_IDs |
| 09_Claims_Ledger.csv | 11_CLAIMS | claim_ID; claim_text→Claim / assertion; Robustness_status→Robustness; Human_validation→Human validation |
| 10_Submission_Checklist.csv | 13_SUBMISSION | Item; Requirement→Requirement; Evidence_or_file→Evidence/file |
| 11_CADA_Control.csv | 01_EACH | EACH_ID; Title→Task; Assigned_to→Responsible; Next_action→Next action; Deadline→Deadline; Status |
| 12_PM_Sync.csv | 14_PM_SYNC | EACH_ID + Provider; External_item_ID→External item ID |
| 13_Traceability_Log.csv | 02_TIME_LINE | Trace_ID; Action_summary→Action summary; Actor→Actor |
| 14_AI_Use_Log.csv | 12_USO_IA | AI_Use_ID; Human_review_method→Human review method; Human_decision→Human decision |
| 15_CADA_Dashboard.csv | 00_PAINEL | Metric/Value→derived dashboard indicators |
| 16_Interoperability.csv | 16_INTEROPERABILITY | Export_ID; Package_SHA256→SHA-256 from package |
| 17_Decision_Log.csv | 17_DECISIONS | DEC_ID; Decision→Decision; Decided_by→Decided by |
| 18_Human_Validation_Gates.csv | 18_VALIDATIONS | GATE_ID; Validation_evidence→Validation evidence |
| 19_Snapshots.csv | 19_SNAPSHOTS | SNAP_ID; Manifest_SHA256→SHA-256 from manifest |

04_EVIDENCIAS summarizes 09_MATRIZ_EVID and claims; do not edit it as an independent evidence source. 15_CONFIG contains controlled vocabularies. 20_MAPA_CORPUS is derived from validated corpus data, not an independent source of inclusion decisions.

Use scripts/init_project.py TABLES for complete machine headers and references/spreadsheet-template.md for complete visible labels. Additional scientific fields remain in the canonical backend and must survive a round trip even if the default workbook has no corresponding column. Ambiguous mappings require an explicit adapter decision, never silent field loss.

JOURNAL_PROFILE.json lives under 06_Submissao/Regras_da_Revista. ANONYMIZATION_PROFILE.json remains confidential in management storage. Project configuration is not inferred from decorative spreadsheet labels.

<a id="stage-boundary-procedure"></a>
## Stage-boundary procedure1. Record the storage policy/state, canonical backend, explicit fallback authorization when applicable, file/sheet links and baseline version or hash.
2. Read current state; update canonical rows by stable ID.
3. Refresh mapped views and verify row counts, IDs and critical fields.
4. Preserve unmapped fields and auxiliary tables; record last synchronized version in CONTINUIDADE.md.
5. On divergent edits, preserve both versions, stop synchronization of affected rows and record the conflict. Scientific conflicts need human judgment; never choose a winner solely by timestamp.
6. After reconciliation, record the material decision and new baseline. External task managers remain mirrors.

