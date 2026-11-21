# V1-14/20 — RESULTADOS: direitos, histórico Git e privacidade (21/11/2026)

**Situação do ticket:** ENTREGUE_PARA_AUDITORIA, com P0 remanescentes e sem aceite jurídico/editorial final.
**Base de planejamento:** manifesto `knowledge/methodology/intake/v1_parallel/V1-WORKPACKAGES-MANIFEST.json` no commit `7c92045310eb3b1474a9612a777fb0012a511592` (Git blob `2f85dc6c4283376b9fc3c312668f0a1f25a0a301`).
**Branch exclusiva:** `work/v1-14-20261121`; somente este relatório e `V1-14-DELTA.json` são entregas de escrita.
**Escopo:** Issue #102 (licença e objeto PDF histórico); Issue #103 (IDs de Drive em histórico público); metadados de ACL do acervo. Sem alterações de permissões, sem rewrite/force-push e sem leitura/republicação de PDFs protegidos.
**Estado científico:** NÃO AVALIADO — nenhuma validação independente de card, nenhuma promoção de [P]/[I] a [L].

## 1. RESULTADOS verificáveis

### R14-01 — Issue #102, direitos e histórico de SRC-0367

- [Issue #102](https://github.com/rebsonm/MeuArtigoSkill/issues/102): aberta na consulta. O registro do mantenedor informa que o PDF de Silva & Hernández (2020), DOI `10.1590/0103-3352.2020.33.218584`, foi equivocadamente classificado como CC BY irrestrita; a licença indicada pela página editorial é **CC BY-NC 4.0**. Não houve nesta etapa nova verificação independente da edição no portal do periódico.
- A [Creative Commons BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) permite compartilhar e adaptar **nas condições de atribuição e uso não comercial**. A classificação equivocada como licença irrestrita é erro de curadoria e incompatibilidade com a política vigente do catálogo público; a presença histórica, por si, não prova infração autoral. Exigível parecer jurídico/editorial sobre condições do uso efetivamente ocorrido.
- Verificação das árvores Git, **sem buscar os bytes do PDF**: no commit anterior `115ba34f168f9efc78da3ff4a79bf61cb608e2d7`, o objeto binário Git `36de02c67d14754ac77c8f6681a5427820763d0e` consta no diretório público de PDFs. No commit corretivo `feaf1908008c3ae6e2e554c4c45b6cc25f89b468` e no snapshot `c5e0ca9abd98f824f1576c3ad94c6e9a5d18e9bf`, esse objeto não consta das árvores. As três árvores estavam completas (`truncated=false`).
- A comparação Git da revisão antiga até o snapshot `c5e0ca9...` retornou `status=ahead`, 139 commits à frente, 0 atrás. Portanto, a exclusão do HEAD **não eliminou o commit histórico da ancestralidade da linha examinada**. Não foi feita auditoria exaustiva de todos os outros refs e clones.
- O repositório é público; a API retornou **1 fork** e **13 refs de tags** na consulta. Não se verificou conteúdo/alcance desse fork nem de todos os caches/refs. Não interpretar esses contadores como prova de divulgação de arquivo específico em forks/tags.

**Decisão necessária:** opção A, documentar licença NC e uso histórico, manter histórico com controles; ou opção B, elaborar e aprovar plano de reescrita coordenada. Ambas condicionadas a análise jurídica/editorial, avaliação dos efeitos sobre SHA pinados, PRs, CI, clonagens e suporte da plataforma; **nenhuma** foi executada ou aprovada aqui.

### R14-02 — Issue #103, exposição de IDs em recibos IB

- [Issue #103](https://github.com/rebsonm/MeuArtigoSkill/issues/103): aberta. Auditoria conservadora de **14 recibos** `knowledge/methodology/intake/parallel/IB-XX-DELTA.json` em branches próprias: IB-01, 03, 05–11, 13, 15, 16, 19 e 20.
- Conferidos os recibos *HEAD* de cada branch por leitura de JSON: o campo `drive_file_id_confirmado_ou_null` estava `null` nos 240 registros examinados (18 + 18 + 12×17). Os recibos possuem indicação de redação de IDs. Isso prova o estado desses arquivos atuais, não a ausência de IDs em qualquer outro arquivo público.
- Conferidos os **commits anteriores à redação** de cada um dos 14 recibos, sem copiar valores para este relatório: **240 valores não nulos de identificadores privados** foram detectados no mesmo campo (18 + 18 + 12×17). A evidência é histórica, não mera hipótese. Verificação feita por contagem de campos após leitura de commits por SHA, com nenhum valor exportado ao relatório.
- Prefixos dos commits históricos consultados, apenas para reconciliação sem revelar identificadores: IB-01 `334886e32422`, IB-03 `6e132d1cbdbd`, IB-05 `a65850de0d64`, IB-06 `7b87579d812c`, IB-07 `0b16b58c4c9d`, IB-08 `75b53a4399b9`, IB-09 `6346df7244a1`, IB-10 `2ec297fbd928`, IB-11 `f5471e65c7b2`, IB-13 `79a6ce7dc540`, IB-15 `12e45e17c35d`, IB-16 `a2c2736c4d32`, IB-19 `cff41a9f9232`, IB-20 `bbb008637db1`.
- A sanitização dos HEADs **não limpa Git history, forks, clones, caches, refs de PRs**. Nenhum mapeamento particular ou URL de arquivo do Drive deve ser acrescentado a GitHub, issues ou artefatos públicos.

### R14-03 — Permissões efetivas reportadas pelo Drive, evidência minimizada

- Pela API autenticada de metadados do Google Drive, a pasta-raiz do acervo **`PPGA - LIVROS`** retornou `shared=true`, permissão `anyone:reader` e `allowFileDiscovery=false`. Isto significa **visualização para qualquer pessoa que disponha do link**, ainda que sem descoberta em pesquisa pública; não significa que o conteúdo já foi acessado por terceiros.
- Amostra em duas profundidades: **1 PDF diretamente na raiz, 6 subpastas e 4 PDFs aninhados em subpastas distintas**. Para os 11 objetos amostrados, a API também reportou `anyone:reader` (e permissão de proprietário). Não se reproduziram nomes ou IDs de PDFs, links ou nomes pessoais.
- Portanto, **há risco P0 de acesso não pretendido ao acervo privado por link**; não é seguro classificar a coleção como privada apenas por estar fora de um pacote ZIP ou por suprimir os identificadores das branches HEAD. A amostra **não** estabelece a ACL de todos os documentos do inventário, de outros drives, backups, versões ou contas; também não constitui teste anônimo de download.
- Nenhuma ACL foi alterada, conforme `write_scope` do manifesto. A ação recomendada é o **mantenedor revisar e restringir o compartilhamento da pasta/acervo**, após avaliar heranças e necessidades legítimas de colaboração, confirmar acesso efetivo com conta não autorizada, registrar decisão, e auditar todos os PDFs sob a árvore. O executor V1-14 não foi autorizado a efetuar essa alteração.

## 2. Riscos, mitigação proposta e decisões pendentes

| Risco | Severidade | Mitigação proposta (NÃO executada) | Quem decide / evidência de saída |
| --- | --- | --- | --- |
| P0-ACL — acervo por link `anyone:reader` | Crítico/P0 | Revisar herança, limitar compartilhamento de pasta e filhos conforme necessidade, testar conta externa, registrar varredura item-a-item | Proprietário do Drive / ACL e teste de acesso documentados |
| P0-HIST — 240 IDs em versões históricas de 14 arquivos | Alto/P0 | Inventário privado de refs/históricos/PRs/forks, contenção de acesso, política de não inclusão de IDs e eventual plano supervisionado de rewrite | Mantenedor + responsável de segurança / plano aprovado e reauditoria |
| P0-LIC — PDF CC BY-NC anteriormente classificado como irrestrito | Alto/P0 | Parecer sobre a cópia exata, termos NC, atribuição e uso histórico; decidir preservação de histórico vs. rewrite | Jurídico/editorial + mantenedor / decisão assinada |
| REGR-IMP — SHA pinado e PR após rewrite | Alto | Simular impactos em branches, tags, pull requests, leitores, CI, cópias e suporte; backup privado antes de qualquer mudança destrutiva | Mantenedor + responsáveis técnicos / rollback e revalidação |
| ED-CI — inferir aceite científico de uma auditoria de ACL | Alto | Exigir revisões editoriais/científicas independentes por card | Revisores distintos / atas/checklists |

**Opções para decisão humana:**
- **Opção A (contenção preservando histórico)** — reclassificação NC, notas, controle de acesso do Drive, política preventiva e documentação pública sanitizada. Preserva SHAs e evita quebra imediata de integrações; **não apaga evidências de exposição histórica**.
- **Opção B (reescrita de histórico planejada)** — somente com decisão expressa após mapa de refs, fork/clones/PRs, backup privado, coordenação e plano de recuperação; pode reduzir acesso por refs controlados mas não garante remoção de clones/caches e altera SHAs. **Não autorizada nesta etapa.**
- **Decisão provisória da V1-14:** **BLOQUEADO para GO/publicação** até decisão formal das Issues #102/#103 e revisão de ACL do acervo. Não emitir parecer jurídico conclusivo nem declaração de saneamento completo.

## 3. Critérios de aceite deste ticket

1. **Relatório risco/refs/histórico:** atendido como **mapeamento delimitado**, com commits de evidência, 14 branches e ressalva expressa de não exaustividade (sem clone completo, fork/PR/caches integrais).
2. **Permissões efetivas com minimização:** atendido **em amostra autenticada de metadados** (pasta principal + 11 objetos); ACL P0 detectada e comunicada, sem expor identificadores.
3. **Riscos e decisões pendentes:** atendido, com alternativas A/B, responsabilidades e critérios para auditoria complementar.

**Status:** `ENTREGUE_PARA_AUDITORIA` refere-se ao **relatório**; **P0#102, P0#103 e P0-ACL permanecem abertos**, sem afirmar resolução técnica, legal, científica ou aceite da publicação.

## 4. Testes e evidências de integridade

- Leitura e parse do manifesto congelado (20 tarefas), com V1-14 `dependencies=[]`, `write_scope` exclusivamente para dois relatórios.
- Árvores Git históricas consultadas por SHA com `truncated=false`; confirmação de presença/ausência de blob sem transferência de binário.
- Parse de 14 JSONs do HEAD e 14 JSONs históricos; verificação estrutural de campo privado `null` vs. não `null` (240 em cada condição).
- Consultas de metadados Drive (12 objetos, incluindo pasta raiz), sem consulta a conteúdo/bytes do acervo.
- **Não houve execução de pytest/CI** para a Skill neste ticket documental. Nenhum teste de host real nem verificação independente científica.
- Valores de SHA detalhados dos **dois relatórios** devem ser preenchidos por readback após seus commits; hash SHA-256 de PDF privado não foi calculado nem divulgado.

## 5. Próximos passos e fronteira

- Solicitar decisão explícita do mantenedor sobre mitigação imediata de ACL e avaliação jurídica/editorial de NC e histórico.
- Fazer auditoria read-only controlada e mais ampla de refs, forks, clones e permissões (inclusive testes externos autorizados) sem exportar IDs privados; documentar inventário completo em local privado.
- V1-16 poderá integrar **após** auditoria e entrega de V1-01 a V1-15, sem assumir que estes bloqueios estejam resolvidos. V1-17…V1-20 continuam condicionadas às dependências do manifesto.
- **Proibido**: merge em `main`, tag, release, force-push, reescrita do histórico, MCP, distribuição do PDF CC BY-NC no catálogo irrestrito, alteração global de ledger/registry/catalog ou qualquer aprovação científica independente sem evidência.

**Fontes delimitadas:** manifesto V1 fixado; Issues #102/#103; árvores e commits Git mencionados; metadados de ACL da pasta do acervo (valores minimizados); termos oficiais CC BY-NC; documentação GitHub sobre consequências da reescrita de histórico. Não foram lidos materiais atribuídos a tickets de cards ou identificações residuais.


## 6. Continuidade V1-14 — verificação complementar independente (21/11/2026)

**Natureza:** adendo verificável à auditoria previamente entregue, sem reexecutar a contagem dos 240 campos/14 recibos IB nem alterar direitos, ACL ou histórico. Referências e evidências sanitizadas.

### C14-01 — Licença da edição oficial confirmada por fonte primária (NOVO)

- A página pública da SciELO referente **exatamente** ao DOI `10.1590/0103-3352.2020.33.218584`, *Aplicação metodológica da análise de conteúdo em pesquisas de análise de política externa*, informa publicação na coleção em **30/11/2020**. O link de licença associado ao próprio artigo (âncora "Este é um artigo publicado em acesso aberto sob uma licença Creative Commons", link #124 do HTML) foi seguido em modo somente leitura e levou diretamente a `https://creativecommons.org/licenses/by-nc/4.0/` (**CC BY-NC 4.0**).
- Fonte da **edição oficial**, sem acesso ao PDF: https://www.scielo.br/j/rbcpol/a/QFmq77JnT468fcBKCdh99ms/?format=html ; termo oficial: https://creativecommons.org/licenses/by-nc/4.0/legalcode.en .
- **Interpretação delimitada:** BY-NC permite reproduzir/compartilhar sob atribuição e finalidade não comercial, sujeito aos demais termos; não licencia reutilização comercial irrestrita. A licença da edição está confirmada por redirecionamento da editora; **identidade, condições de atribuição e histórico de disponibilização do exato binário Git ainda exigem conferência editorial/jurídica**. Uma política de catálogo irrestrito não pode reclassificar BY-NC como BY. Isso não constitui, por si, parecer de infração.

### C14-02 — Alcance de refs públicas de tags (NOVO)

- API GitHub `git/matching-refs/tags` retornou **13 referências de tags**, todas com objeto do tipo commit. Foram feitas **13 comparações de ancestralidade** entre cada tag e o commit histórico `115ba34f168f9efc78da3ff4a79bf61cb608e2d7` (marco em que o blob do PDF já constava da árvore).
- Resultado verificável: **13/13 tags são ancestrais do referido commit histórico** (`status=behind`, `ahead_by=0`, `behind_by>0` em todas as comparações). Portanto, **nenhuma dessas 13 refs de tag contém o commit histórico na própria ancestralidade**. Isso NÃO comprova ausência de cópias do PDF em outros commits, tags externas, branches ou forks; não foram inspecionados blobs nem PDF.
- Consulta adicional `git/matching-refs/heads` retornou **139 referências de branches**. Foi inventariado apenas o universo de refs HEAD; **a análise de alcance histórico dessas 139 branches não foi executada individualmente**. Esse levantamento não é uma varredura completa de conteúdo nem do fork.
- API GitHub `git/ref/heads/work/v1-14-20261121` confirmou HEAD inicial desta continuidade `a13a52be77e818567e8d3123e14ca0a96875d4fb`; PR #101 permanece **Draft**, aberta, não mesclada e seu HEAD é o snapshot congelado `c5e0ca9abd98f824f1576c3ad94c6e9a5d18e9bf`. Issues #102/#103 continuavam **OPEN** na leitura.

### C14-03 — ACL da raiz revalidada agora (NOVO)

- Busca nominal exata da pasta `PPGA - LIVROS` no Drive retornou um único objeto. Nova consulta autenticada de **metadados**, sem baixar PDF ou expor URL/ID, confirmou `shared=true`, `canShare=true`, `source_visibility_status=permission_metadata_available`, permissão `anyone:reader` e `allowFileDiscovery=false`.
- O risco P0-ACL **permanece ativo**: pessoas que detenham um link podem potencialmente ler conteúdo permitido pela ACL; não foi feito teste anônimo, verificação integral da árvore nem prova de acesso efetivamente realizado. As 11 amostras de descendentes são evidência da rodada anterior, **não** novas verificações deste adendo.

### C14-04 — Alternativas, riscos e decisão pendente

- **A (preservação com contenção):** manter SHAs/histórico e registrar aviso NC, verificação de atribuição/uso histórico, tratamento de ACL pelo proprietário e política de não exposição de IDs. Não elimina commits acessíveis, forks ou caches.
- **B (plano de expurgo):** preparar inventário privado de refs/PRs/forks, cópia de segurança privada, parecer jurídico/editorial, coordenação de clones, janela de manutenção e avaliação de impactos em SHAs assinados/pinados antes de qualquer possível rewrite. Nenhum rewrite ou autorização foi concedido; GitHub alerta que clones/forks/caches podem permanecer.
- Fonte técnica: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository .
- **Evidência mínima para decisão humana:** (1) permissão atual e herança de cada objeto relevante, teste externo autorizado e registro assinado do proprietário; (2) parecer específico da edição/licença/uso histórico SRC-0367, atribuição e destino do binário; (3) matriz privada de alcance em branches, refs de PR e fork, mantendo zeros IDs privados em recibos públicos; (4) alternativa A/B deliberada pelo mantenedor e plano verificável de reteste.
- **Estado final deste adendo:** `ENTREGUE_PARA_AUDITORIA`, `release_gate=BLOQUEADO`, P0#102/#103/P0-ACL sem aceite jurídico, científico ou de segurança. Não houve CI/pytest/host nesta continuidade; apenas testes de leitura, 13 comparações de ancestralidade e metadados de ACL. Nenhum PDF distribuído, ACL modificada, branch/PR de terceiros alterada, merge/tag/release/MCP ou rewrite executado.

**Próxima ação única:** o proprietário do Drive deve registrar decisão de contenção da permissão `anyone:reader` na pasta `PPGA - LIVROS` e descendentes e autorizar teste externo de acesso, com comprovante anonimizado do resultado. Sem essa evidência, P0-ACL permanece bloqueado. Questões #102/#103 exigem deliberações adicionais separadas.
