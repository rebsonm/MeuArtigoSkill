# RT-10 — Declaração editorial de uso de IA

O Meu Artigo usa exclusivamente os eventos registrados em `14_AI_Use_Log.csv` para preparar a declaração editorial. A Skill não pode reconstruir um histórico imaginado, inventar ferramentas, atribuir revisão humana sem resposta real ou apresentar o texto como aprovado pela revista.

## Política específica do periódico

Em `06_Submissao/Regras_da_Revista/JOURNAL_PROFILE.json`, o objeto `ai_disclosure_policy` registra: `status=VERIFIED`, `source` oficial, `verified_at`, `statement_location`, `category_rules` por categoria e, quando aplicável, `require_model_version`. As decisões permitidas são `ALLOWED`, `PROHIBITED` e `EDITORIAL_REVIEW`. Qualquer regra ausente ou proibitiva bloqueia a declaração final. O campo antigo `ai_policy` não equivale a uma política conferida.

O objeto `ai_disclosure_attestation` exige manifestação real do pesquisador sobre a completude do log, data, autoria, referência da resposta e SHA-256 exato do CSV. Um log vazio não prova por si que nenhuma IA foi utilizada.

## Uso da tabela existente

A aba `12_USO_IA` e o arquivo `14_AI_Use_Log.csv` acrescentam três colunas sem criar novas abas ou IDs: `Disclosure_category`, `Human_review_evidence` e `Confidentiality_review`. As categorias: ADMIN_SUPPORT, LITERATURE_SEARCH, SCREENING, EVIDENCE_EXTRACTION, DATA_ANALYSIS, DRAFTING_EDITING, FIGURES e OTHER.

Para eventos substantivos, informe a revisão humana e sua referência real. Um `Disclosure_required=NO` não supera a política do periódico. Não inclua prompts completos, textos restritos ou dados pessoais na declaração pública.

## Comandos

```bash
python scripts/editorial_ai_disclosure.py audit /projeto
python scripts/editorial_ai_disclosure.py draft /projeto
python scripts/editorial_ai_disclosure.py final /projeto
python scripts/editorial_ai_disclosure.py verify-final /projeto
```

A minuta pode ter pendências; a final só é emitida após reconciliação e política verificada. Ela fica em `06_Submissao/Regras_da_Revista/AI_DISCLOSURE_FINAL.md`, associada ao relatório com hashes `00_Gestao_e_Continuidade/AI_DISCLOSURE_AUDIT.json`. O `GATE-0007` revalida ambos.

O texto final é uma proposta para conferência de colocação no manuscrito e na carta, não evidência de submissão. A Skill não consegue autenticar pessoas, confirmar automaticamente que todo uso de IA foi registrado nem garantir aceitação editorial.

## Referências gerais

- ICMJE, `https://www.icmje.org/recommendations/browse/artificial-intelligence/`
- COPE, `https://doi.org/10.24318/cCVRZBms`

Essas orientações não substituem as regras oficiais de cada revista. Não se deve atribuir autoria a uma IA, nem supor que revisão humana foi efetiva por existir uma coluna preenchida. Permanecem obrigatórios os controles de anonimização e uso lícito de PDFs. Não se requer serviço pago.
