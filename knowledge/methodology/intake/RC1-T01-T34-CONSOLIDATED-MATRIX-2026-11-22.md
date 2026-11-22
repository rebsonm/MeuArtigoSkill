# Meu Artigo RC.1 — Matriz consolidada T01–T34

Data: 22/11/2026. PR #112 Draft. Evidência: reconciliação, não reexecução. Decisão: NO-GO.

**Alerta obrigatório:** PASS histórico, no sandbox ou em leitura direta do Google Drive NÃO é PASS do executável atualmente persistido no ChatGPT. Todos os 34 testes permanecem sem atestação end-to-end no build host atual. T01/T02 da candidata atual são NOT_RUN; T02 FAIL no hotfix anterior permanece histórico.

- Build candidato: RC.1, ZIP SHA-256 `fa6431207c25dd21cbd60428ccbd3d9a660c100423015499f1bcae25e9d3947d`, manifesto SHA-256 `c92edafbceba7df2e53a5b55cca788b5827c1cd1161da9ce298e692fc079f3a9`, build source `48407b55a851ba8e07b1468330c31d3bd97ffafd`.
- Evidência atual: PASS_HISTORICAL 25; PASS_CONTEXTUAL 2; PASS_LOCAL 3; PASS_LOCAL_PARTIAL 1; PASS_DRIVE_PARTIAL 1; NOT_RUN 2. Total 34. Nenhuma pontuação de aceite de host derivada desses números.
- História: primeiro beta.6 divergente da RC.1; hotfix 5c229bcc corrigiu T01 mas T02 FAIL após Save (YAML/SVG transformados). Candidata posterior tem apenas verificação de ZIP extraído, não readback do host.
- T05 CSV com 8 registros, T06 XLSX com 21 planilhas, T32 parser de texto não confiável e T33 direitos editoriais: PASS somente nos escopos locais. T34 Drive documental: PASS, motor host NOT_RUN. Gates científicos 7/7 PENDING, 0 decisões.

## Matriz por ID

| Teste | Funcionalidade | Histórico | Evidência atual | Aceite host candidato | Risco | Papel proposto | Próxima ação | Fontes |
|---|---|---|---|---|---|---|---|---|
| T01 | Identidade do executável | FAIL (beta.6, executor divergente); PASS (hotfix 5c229bcc) | NOT_RUN | NOT_RUN_CURRENT_BUILD | P0 | Operador do host | Ler VERSION/manifesto do executável pós-Save real e comparar ao ZIP pinado; não aceitar apenas rótulo RC.1. | H1, H2, C2, C3 |
| T02 | Integridade após Save | FAIL (133/135; depois 149/151 no hotfix) | NOT_RUN | NOT_RUN_CURRENT_BUILD | P0 | Operador do host + revisor independente | Obter readback real, hashes de todos os payloads, revisar YAML/SVG transformados e recibo externo; preservar NO-GO. | H1, H2, C2, C3 |
| T03 | Python e conectividade | PASS no runtime histórico | PASS_CONTEXTUAL | NOT_RUN_CURRENT_BUILD | P2 | Equipe de testes | Documentar matriz de versões Python/dependências e repetir conectividade somente no ambiente de aceite se necessário. | H1, C1 |
| T04 | Drive gravável e isolado | PASS criação/leitura do projeto fictício | PASS_CONTEXTUAL | NOT_RUN_CURRENT_BUILD | P1 | Operador Drive | Manter evidência de permissões e isolamento; ensaiar escrita só em nova fixture com autorização, sem tocar projeto canônico. | H1, D1 |
| T05 | Inicialização automática CSV | FAIL inicial; PASS no hotfix antigo | PASS_LOCAL | NOT_RUN_CURRENT_BUILD | P1 | Engenharia da Skill | Aceitar correção apenas no sandbox; repetir init na instalação efetiva e verificar oito linhas sem reparo manual. | H1, H2, C1 |
| T06 | Geração de XLSX | BLOCKED no host antigo sem artifact_tool | PASS_LOCAL | NOT_RUN_CURRENT_BUILD | P1 | Engenharia de dependências | Checar artifact_tool no host final ou manter fallback CSV documentado; não inferir disponibilidade de outro Python. | H1, H2, C1 |
| T07 | GATE-0001 sem fundamentação | PASS recusa histórica | PASS_HISTORICAL | NOT_RUN_CURRENT_BUILD | P1 | Revisor científico + QA | Validar recusa de aprovação de pergunta sem evidências no build final, preservando PENDING. | H1, D1 |
| T08 | GATE-0002 sem fundamentação | PASS recusa histórica | PASS_HISTORICAL | NOT_RUN_CURRENT_BUILD | P1 | Revisor científico + QA | Revalidar bloqueio de método/protocolo sem justificativa no executável final. | H1, D1 |
| T09 | GATE-0003 sem fundamentação | PASS recusa histórica | PASS_HISTORICAL | NOT_RUN_CURRENT_BUILD | P1 | Revisor científico + QA | Confirmar bloqueio de estratégia de busca sem validação humana no host. | H1, D1 |
| T10 | GATE-0004 sem fundamentação | PASS recusa histórica | PASS_HISTORICAL | NOT_RUN_CURRENT_BUILD | P1 | Revisor científico + QA | Confirmar que corpus não é congelado sem auditoria de elegibilidade e decisões humanas. | H1, D1 |
| T11 | GATE-0005 sem fundamentação | PASS recusa histórica | PASS_HISTORICAL | NOT_RUN_CURRENT_BUILD | P1 | Revisor científico + QA | Confirmar recusa de síntese sem fontes/contraprovas na candidata efetiva. | H1, D1 |
| T12 | GATE-0006 sem fundamentação | PASS recusa histórica | PASS_HISTORICAL | NOT_RUN_CURRENT_BUILD | P1 | Revisor científico + QA | Confirmar recusa de auditoria de claims não fundamentada em evidências. | H1, D1 |
| T13 | GATE-0007 sem fundamentação | PASS recusa histórica | PASS_HISTORICAL | NOT_RUN_CURRENT_BUILD | P0 | Responsável por submissão + QA | Bloquear release/submissão até validação nominal humana, conforme protocolo. | H1, D1 |
| T14 | Decisão DEC sem justificativa | PASS recusa histórica | PASS_HISTORICAL | NOT_RUN_CURRENT_BUILD | P1 | Mantenedor metodológico | Confirmar que nenhum DEC aprovado pode ser criado sem justificativa e responsável. | H1, D1 |
| T15 | TRACE e rastreabilidade | PASS histórico com TRACE UNVERIFIED | PASS_HISTORICAL | NOT_RUN_CURRENT_BUILD | P1 | Responsável por evidências | Reconciliar proveniência e manter UNVERIFIED até confirmação externa; não carimbar como prova. | H1, D1 |
| T16 | Separação [L]/[I]/[P] | PASS estrutural histórico (4 casos) | PASS_HISTORICAL | NOT_RUN_CURRENT_BUILD | P1 | Revisor metodológico | Preservar testes adversariais estruturais e planejar revisão semântica independente, sem reexecutar os já comprovados. | H1 |
| T17 | C.A.D.A. operacional versus ciência | PASS auditoria histórica | PASS_HISTORICAL | NOT_RUN_CURRENT_BUILD | P1 | Mantenedor metodológico | Verificar limite entre tarefa DONE e gate científico; não confundir atividade concluída com aprovação. | H1, D1 |
| T18 | Nenhuma pesquisa fictícia inventada | PASS histórico (tabelas vazias) | PASS_HISTORICAL | NOT_RUN_CURRENT_BUILD | P1 | Responsável QA científico | Continuar projeto fictício sem coleta/corpus/manuscrito e conferir snapshots antes de qualquer novo fluxo. | H1, D1 |
| T19 | Inventário de 649 cards | PASS histórico 475 SRC + 174 EC | PASS_HISTORICAL | NOT_RUN_CURRENT_BUILD | P2 | Curadoria de catálogo | Conferir inventário do build distribuído e ausência de duplicatas; não tomar 649 como fontes científicas validadas. | H1 |
| T20 | Busca design science | PASS histórico EC-0004 | PASS_HISTORICAL | NOT_RUN_CURRENT_BUILD | P2 | Equipe de recuperação | Manter EC-0004 como card editorial com proveniência; revalidar recuperação end-to-end apenas no host final. | H1, C1 |
| T21 | Busca revisão sistemática | PASS histórico EC-0065/EC-0075 | PASS_HISTORICAL | NOT_RUN_CURRENT_BUILD | P2 | Equipe de recuperação | Confirmar recuperação e metadados com build final quando disponível; não rebaixar cautelas de fonte. | H1 |
| T22 | Busca análise qualitativa | PASS histórico EC-0168 e SRC-0010 | PASS_HISTORICAL | NOT_RUN_CURRENT_BUILD | P2 | Equipe de recuperação | Executar smoke test no host final depois do T02, sem reabrir auditoria antiga. | H1 |
| T23 | Identidade do card SRC-0002 | PASS histórico metadados/DOI | PASS_HISTORICAL | NOT_RUN_CURRENT_BUILD | P2 | Curadoria bibliográfica | Preservar distinção metadados versus leitura de publicação primária. | H1 |
| T24 | Exclusão SRC-0385 | PASS histórico recusa guidance | PASS_HISTORICAL | NOT_RUN_CURRENT_BUILD | P1 | Curadoria e QA | Reconfirmar status excluído na candidata efetivamente instalada antes de orientação operacional. | H1 |
| T25 | Sinalização de texto recuperado | PASS histórico untrusted_reference_text | PASS_HISTORICAL | NOT_RUN_CURRENT_BUILD | P1 | Equipe de segurança | Manter marcação untrusted no fluxo; T32 host requer teste separado. | H1, C1 |
| T26 | PDF privado não acessado | PASS histórico private_sources_accessed=false | PASS_HISTORICAL | NOT_RUN_CURRENT_BUILD | P0 | Gestor de direitos e privacidade | Confirmar que consultas de produção não expõem PDF privado; manter zero direitos presumidos. | H1, C4 |
| T27 | Persistência e readback | PASS histórico 27/27 arquivos | PASS_HISTORICAL | NOT_RUN_CURRENT_BUILD | P1 | Operador Drive | Preservar recibos do Drive, e validar posterior leitura das versões vigentes; 6 arquivos relidos agora não substituem 27/27. | H1, D1 |
| T28 | Citação [L] não verificada | PASS histórico rejeição | PASS_HISTORICAL | NOT_RUN_CURRENT_BUILD | P1 | Revisor científico | Confirmar recusa de Evidence_ID desconhecido e fonte sem localizador no fluxo final. | H1 |
| T29 | Recurso externo indisponível | PASS histórico 404/UNAVAILABLE_OR_BLOCKED | PASS_HISTORICAL | NOT_RUN_CURRENT_BUILD | P2 | Equipe de resiliência | Manter fail-closed e observabilidade para indisponibilidade de rede sem inventar leitura. | H1, C4 |
| T30 | Avanço sem armazenamento comprovado | PASS histórico CANONICAL_STORAGE_RECHECK_REQUIRED | PASS_HISTORICAL | NOT_RUN_CURRENT_BUILD | P0 | Governança Drive | Exigir verificação persistida antes de transição; jamais permitir fallback local silencioso. | H1, C1, D1 |
| T31 | Injeção no identificador | PASS histórico INVALID_CARD_ID | PASS_HISTORICAL | NOT_RUN_CURRENT_BUILD | P1 | Equipe de segurança | Conservar teste negativo e diferenciar ID malicioso de conteúdo hostil (T32). | H1 |
| T32 | Instrução maliciosa no corpo | BLOCKED inicial; PASS em hotfix antigo controlado | PASS_LOCAL_PARTIAL | NOT_RUN_CURRENT_BUILD | P0 | Equipe de segurança + operador host | Testar limite de confiança do modelo no host real com fixture segura; cenário local apenas comprovou parser, não defesa do LLM. | H1, H2, C1 |
| T33 | Direitos de card e fonte | FAIL inicial; PASS em hotfix antigo | PASS_LOCAL | NOT_RUN_CURRENT_BUILD | P1 | Curadoria autoral | Preservar direitos editoriais separados de publicações; verificar em consulta real ao host e avançar revisão humana de licenças. | H1, H2, C1 |
| T34 | Retomada independente do Drive | BLOCKED inicial; PASS documental em hotfix | PASS_DRIVE_PARTIAL | NOT_RUN_CURRENT_BUILD | P1 | Operador Drive + QA continuidade | Testar a retomada integrada via Skill no host; leitura direta do Drive prova estado documental mas não motor host. | H1, H2, C1, D1 |

## Fontes e escopo

- **H1**: Google Drive TESTE_MEU_ARTIGO_RC1 / RELATORIO_HOMOLOGACAO_RC1.md, 2026-11-21 (34 tests, old beta.6 vs catalog RC.1; 27 PASS 4 FAIL 3 BLOCKED, historical).
- **H2**: Google Drive TESTE_MEU_ARTIGO_RC1 / RELATORIO_RETESTE_HOTFIX_5c229bcc.md and CONTINUIDADE.md §§18–20 (old host hotfix 5c229bcc, T02 FAIL after Save, T01/T05/T32/T33/T34 PASS, T06 BLOCKED).
- **C1**: GitHub PR #112 / knowledge/methodology/intake/RC1-T05-T06-T32-T33-T34-CONTROLLED-ACCEPTANCE-2026-11-22.md, commit 69face47c5cd387af47055931783aaa4d91eb487 (candidate ZIP sandbox tests).
- **C2**: GitHub PR #112 / knowledge/methodology/intake/RC1-HOST-T02-READBACK-PREFLIGHT-2026-11-22.md, commit 2c2e6dfc27faf49c70e84083ac9cf6df7767d10b (source-ZIP checks; host NOT_RUN).
- **C3**: GitHub PR #112 / knowledge/methodology/intake/RC1-T02-ACTUAL-HOST-ACCESS-CONTINUITY-2026-11-22.md, commit 68275ca7b13713b1d6e758620504447d910c80ee (no authenticated host installation bytes).
- **C4**: GitHub PR #112 / knowledge/methodology/intake/PUBLIC-PDF-TEST-ONLY-29-TECHNICAL-HOMOLOGATION-2026-11-22.md, commit 9edc6f1fbb0d640efc9c8ea09eee4e009b475759 (29 PDF sandbox, separate technical scope).
- **D1**: Google Drive TESTE_MEU_ARTIGO_RC1 direct connector readback, 2026-11-22: 6 management files twice, unchanged; 7 PENDING gates and 0 scientific decisions; plus historical Drive receipt and continuity.

## Bloqueios de release e próximos donos

1. **P0 T01/T02** — operador autorizado do host e revisor técnico: identidade do executável pós-Save, 152 payloads, manifesto, YAML/SVG instalados, revisão substantiva e recibo externo verdadeiro. Sem diretório autenticado: NOT_RUN.
2. **P0 T13/T26/T30/T32** — responsáveis científicos, direitos, Drive e segurança: proibir liberação de gates, exposição de PDF privado, fallback silencioso ou inferência de resistência de modelo a partir do parser.
3. **P1 T05/T06/T33/T34** — engenharia e curadoria: resultados positivos locais/documentais, mas verificar host/dependências e retomar Drive pelo motor em teste futuro autorizado.
4. **Direitos e governance** — 29 PDFs TEST-ONLY, 20 candidatos, dois CC BY não versionados, conflito RPQ, questões GitHub #102/#103 e sete gates pendentes continuam independentes; ninguém assinou clearance.

Todos os responsáveis apresentados são **papéis propostos**, não pessoas designadas. Nenhum teste T07–T31 foi reexecutado nesta consolidação. Não houve merge, tag, release, alteração de manifesto, PDFs, ZIP, gates, ACLs ou sobrescrita do documento canônico.

Próxima ação recomendada: autenticar Save/readback do host realmente instalado para resolver T01/T02; na ausência, preservar NOT_RUN. Opcionalmente priorizar a governança de direitos ou a matriz de tickets de release.
