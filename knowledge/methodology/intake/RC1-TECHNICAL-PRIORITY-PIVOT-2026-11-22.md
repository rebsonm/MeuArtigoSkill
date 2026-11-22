# Meu Artigo RC.1 — retomada do desenvolvimento, prioridade técnica

**Data:** 2026-11-22. **PR:** [#112](https://github.com/rebsonm/MeuArtigoSkill/pull/112). **HEAD anterior ao registro:** `f21991d0f8de6a5e29e68eb68ca27adb63cb86a4` (Draft, não mesclada). **Natureza:** deliberação gerencial de sequência de trabalho + reconciliação de evidências técnicas existentes. Não instala, não libera nem publica artefatos.

## 1. Decisão expressa do mantenedor

Na conversa de 22/11/2026, o mantenedor do projeto `rebsonm` esclareceu: **assume ele próprio a decisão de publicação e pretende resolver as questões de direitos autorais posteriormente**. Também determinou: **não elaborar, enviar ou voltar a sugerir e-mails editoriais** sobre essas questões. A decisão interna de responsabilidade pelas escolhas de publicação e a preferência de adiar o saneamento jurídico ficam documentadas, sem necessidade de nova consulta de prioridade.

**Consequência operacional:** interromper a proposta repetitiva de consultas autorais; não criar novos rascunhos, não enviar mensagens e não colocar o saneamento de RPQ/UFF/BPSR como "próximo passo recomendado" do trabalho técnico. Rascunhos existentes ficam não enviados e não serão acionados automaticamente. O mantenedor decide se, quando e sob que condições fará a publicação. Esta decisão **não significa** que possua direitos autorais de terceiros, não prova licença, nem modifica silenciosamente declarações de direitos do `pdf_catalog.json`. Não afirmar liberação jurídica, não alterar `exact_pdf_licence_certified_by_human` ou o escopo da allowlist como se um titular tivesse assinado; os fatos jurídicos/documentais ficam disponíveis apenas para referência futura.

## 2. Última CI do HEAD de entrada — evidência verificável, sem repetir auditorias

- GitHub Actions [run `45030949812`](https://github.com/rebsonm/MeuArtigoSkill/actions/runs/45030949812), workflow **Release audit** do commit `f21991d0f8de6a5e29e68eb68ca27adb63cb86a4`: `completed/success`, job `audit` `success`. É um PASS **de CI**, não homologação do host.
- O log da CI reportou `release_metadata=READY_FOR_CANDIDATE_TESTING`, **não** pronto para release pública; o build de PDFs declara `public_release_authorized=false`.
- Artefato de CI padrão `MeuArtigoSkill-rc-test-only` (ID `14758015698`, digest SHA-256 do **artefato externo** `5f5de3dc451806c737f0175b504d7a0c5bc0de8dc563934c67e2ff392c22c09b`).
- Artefato de testes sintéticos `meu-artigo-integrated-skill-acceptance-synthetic` (ID `14757448679`, SHA-256 do **artefato externo** `3221d28307223e7ee6251deb1dc615cc0e9335f41a263a2701ed0ded22f95477`); ZIP foi recuperado e seu JSON aberto nesta execução. **11/11 cenários PASS**, `all_cases_without_canonical_writes=true`, `all_cases_without_private_prose_export=true`, `all_cases_without_scientific_approval=true`.
- O conjunto sintético validou resposta de preparo local autorizado e bloqueios por: decisão ausente, TRACE órfã, divergência de rota/metodologia, mirror Drive não autenticado, fallback local revogado, continuidade desatualizada, transação pendente, gates científicos ausentes, dependência de tarefa desconhecida e próximo passo não registrado.
- **LIMITES DO PRÓPRIO JSON:** `host_mcp_connection_exercised=false`, `real_drive_access_or_sync_verified=false`, `mcp_apps_ui_verified=false`, `project_owned_mcp_server_connected=false`, `updated_skill_installed_in_chatgpt=false`; fontes eram `DISPOSABLE_SYNTHETIC_LOCAL_RECORDS_ONLY`. Logo, PASS 11/11 **não** autoriza alegar funcionamento integrado real do host.
- Outros artefatos CI vistos: `meu-artigo-interactive-research-map-fictional` (ID `14757960900`), `synthetic-research-journey-exercise` (ID `14757776688`), `public-pdf-rights-preflight-not-release` (ID `14757781643`) e `MeuArtigoSkill-PDFs-TEST-ONLY-NOT-RELEASE` (ID `14757568252`). São artefatos de CI/teste, não releases e não foram publicados por esta etapa.

## 3. O que já está resolvido no escopo adequado

O [relatório T01–T34](./RC1-T01-T34-CONSOLIDATED-MATRIX-2026-11-22.md) possui 34/34 IDs documentados, sem afirmar 34 passes na candidata host; T05/T06/T33 tiveram PASS_LOCAL, T32 PASS parser local com LLM host NOT_RUN, T34 PASS leitura documental Drive com motor host NOT_RUN. T01/T02 reais no host ainda `NOT_RUN` por inexistir readback autenticado. O teste de segurança não transforma texto recuperado em ordem aprovada; sete gates científicos continuam `PENDING`. Evitar repetição desses testes apenas para gerar status verde.

## 4. Próximo trabalho de engenharia — decisões A/B/C

### A — RECOMENDADO: piloto de retomada funcional com o projeto fictício no Drive

**Objetivo concreto:** completar a lacuna entre 11 PASS sintéticos locais e o fluxo de retomada do projeto `TESTE_MEU_ARTIGO_RC1` usando ferramentas conectadas reais, **somente em ambiente fictício**, sem alterar decisões/gates. **Sequência:** (i) ler configuração/continuidade/CSV/gates/DEC/TRACE atuais via Drive; (ii) verificar correspondência de versões e dependências na candidata da PR; (iii) executar smoke test do fluxo disponível com permissões verificadas; (iv) emitir recibo claro `PASS / FAIL / NOT_RUN` para integração efetiva do conector, sem inferir que o host ChatGPT foi testado. **Responsável proposto:** QA integração + operador Drive. **Condição de aceite:** seis arquivos canônicos intactos, zero DEC/gates aprovados, rastreabilidade real sem falso sincronismo.

### B — preparação de candidata técnica RC.1 para publicação pelo mantenedor

**Objetivo concreto:** fixar o **ZIP exato** da versão executável e seu manifesto/assinatura SHA, executar smoke do pacote, documentar diferenças de instalação e um checklist de distribuição. A CI atual passou, mas `public_release_authorized=false` e host Save/readback ainda `NOT_RUN`; não contornar essas limitações por atestado fictício. **Responsável proposto:** mantenedor + QA release. **Aceite:** recibo de hash, hash do manifesto e URL do artefato de origem, distinção clara entre ZIP padrão e PDF TEST-ONLY, nenhuma publicação automática.

### C — avaliar interface de mapa interativo fictício

**Objetivo concreto:** revisar o artefato `meu-artigo-interactive-research-map-fictional` gerado pela CI para transformar o protótipo visual em plano de interface integrado às ações que já existem na Skill, sem expandir gates. **Responsável proposto:** UX + engenharia. **Aceite:** inventário das ações que funcionam em preview, requisitos faltantes de autenticação, conexão Drive, states e revisão de segurança; não chamar demo local de interface de produção.

## 5. Regras de execução e continuidade

**FEITO:** inspecionados CI e 11 cenários sintéticos e fixada prioridade técnica sem nova discussão autoral. **EM EXECUÇÃO:** transição de validação isolada para piloto funcional. **PRÓXIMO:** executar A, B ou C conforme escolha expressa do mantenedor, apresentando sempre opções com vantagens e limites. O usuário não deseja ser instado a rediscutir a publicação ou contatar editoras.

**Restrições conservadas por esta etapa:** nenhuma alteração de código, PDFs, catálogo, allowlist, autoria de terceiros, ACLs, gates, decisão científica, manifesto, instalação host, merge, tag, release ou histórico Git. Issues [#102](https://github.com/rebsonm/MeuArtigoSkill/issues/102) e [#103](https://github.com/rebsonm/MeuArtigoSkill/issues/103) continuam fatos de risco documentados, sem transformar tais assuntos em bloqueio para todo e qualquer próximo teste técnico.
