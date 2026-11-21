# V1-06/20 — RESULTADOS da auditoria editorial (EC-037…EC-054)

- Branch exclusiva: `work/v1-06-20261121` — base de planejamento `7c92045310eb3b1474a9612a777fb0012a511592`.
- Manifesto: `knowledge/methodology/intake/v1_parallel/V1-WORKPACKAGES-MANIFEST.json` no commit acima.
- Snapshot **lido**: `c5e0ca9abd98f824f1576c3ad94c6e9a5d18e9bf` (PR #101, não integrado nesta branch).
- Trabalho: leitura integral dos **18 cards atribuídos**, SHA-256 calculado sobre seu texto UTF-8, 18/18 iguais aos hashes do manifesto. Nenhum documento fora do lote foi objeto de auditoria de conteúdo.
- Método/limite: auditoria de **cards**, não dos PDFs originais. Declarações de origem e de licença nos cards NÃO constituem verificação autônoma. Nenhum PDF foi copiado, publicado ou distribuído; não há conclusão científica humana independente.
- Taxonomia: CORREÇÃO_NECESSÁRIA = metadado/inferência a corrigir ou conferir; APROVÁVEL_COM_EVIDÊNCIA = potencialmente publicável **apenas após** duas verificações humanas independentes, de direitos/originalidade e de fidelidade científica. Nenhum status significa aceitação.
- Direitos: EC-037…043 sem licença exata corroborada; EC-044…054 declaram CC BY 4.0 (11 registros), mas falta conferir o exemplar/edição, escopo e atribuição. A existência de um DOI ou PDF privado não autoriza redistribuição.
- Segurança: leitura textual não identificou instrução explícita de prompt injection nos cards; conteúdo de fontes externas permanece não confiável. Não foram executadas instruções externas nem testes de ataque sobre PDFs.
- **Conflito do MD canônico:** um snapshot bruto de 312041 bytes, modificado 22:17:12.560Z, foi substituído remotamente por versão de 312644 bytes, modificada 22:18:31.685Z, antes do envio. A escrita foi **abortada**, sem modificar o Drive. Uma cópia local de proposta não equivale a atualização do arquivo canônico.

## Recibo individual e decisão editorial

### EC-037 — Survey questionnaire quality: response wording is a measurement decision
- **Arquivo único:** `knowledge/methodology/cards/lietz-2009-survey-questionnaire.md`.
- **Integridade:** SHA-256 `61736b7c519202e35f93d2ed883ec21530a01019aed63f4875f3de56b6f953f4` — **igual ao manifesto**; blob Git `2ae6aa6f6596b041ce420e84389bbd4574e5da7a`.
- **Fonte:** DOI não verificado/ausente no card; obra original **não aberta nesta execução**. SHA da cópia original não conferido.
- **Direitos:** LICENÇA DA EDIÇÃO/CÓPIA NÃO DEMONSTRADA. Não reproduzir original sem licença específica demonstrada.
- **Parecer provisório:** `CORREÇÃO_NECESSÁRIA`; classe **[I]**. Ano 2009/2010 ambíguo e DOI apontado, mas não verificado para a edição; cotejar ficha primária e redação bibliográfica.
- **Contraprova/limite:** Reformulações do questionário podem produzir efeitos distintos por idioma, contexto e população.
- **Revisores:** identificação e datas de revisão humana editorial/autorais e científica: **não demonstradas**.

### EC-038 — Meta-analysis with R: effect sizes and dependence before code
- **Arquivo único:** `knowledge/methodology/cards/harrer-etal-2022-meta-analysis-r.md`.
- **Integridade:** SHA-256 `8006030e79250b8eeb2e544c45d95e50800abe9fea95dbe8fc70d84a42eb8a9c` — **igual ao manifesto**; blob Git `6ae9a331063cc310d7f7e2d0098a10675040303a`.
- **Fonte:** https://doi.org/10.1201/9781003107347; obra original **não aberta nesta execução**. SHA da cópia original não conferido.
- **Direitos:** LICENÇA DA EDIÇÃO/CÓPIA NÃO DEMONSTRADA. Não reproduzir original sem licença específica demonstrada.
- **Parecer provisório:** `APROVÁVEL_COM_EVIDÊNCIA`; classe **[I]**. Conferir edição, licença do livro e páginas sobre dependência e conversão de efeitos; não atribuir procedimento numérico específico ao livro sem passagem.
- **Contraprova/limite:** Dependência entre efeitos pode invalidar inferências ainda com código reproduzível.
- **Revisores:** identificação e datas de revisão humana editorial/autorais e científica: **não demonstradas**.

### EC-039 — Systematic reviews: searching, screening and synthesis are separate decisions
- **Arquivo único:** `knowledge/methodology/cards/sampaio-mancini-2007-systematic-review.md`.
- **Integridade:** SHA-256 `a8b93433d1b2cd5742e3a303cca663ace914e681b096177207a643632777a974` — **igual ao manifesto**; blob Git `d3803196f118dc09e4489ed46eae3594e341d2db`.
- **Fonte:** DOI não verificado/ausente no card; obra original **não aberta nesta execução**. SHA da cópia original não conferido.
- **Direitos:** LICENÇA DA EDIÇÃO/CÓPIA NÃO DEMONSTRADA. Não reproduzir original sem licença específica demonstrada.
- **Parecer provisório:** `CORREÇÃO_NECESSÁRIA`; classe **[I]**. Link de editora aponta apenas à raiz SciELO; corrigir URL específica e verificar DOI, título acentuado e edição.
- **Contraprova/limite:** Fluxograma da revisão não substitui critérios de busca e elegibilidade replicáveis.
- **Revisores:** identificação e datas de revisão humana editorial/autorais e científica: **não demonstradas**.

### EC-040 — LLM-assisted qualitative inquiry: technological reflexivity as an audit obligation
- **Arquivo único:** `knowledge/methodology/cards/ibrahim-voyer-2025-llm-reflexivity.md`.
- **Integridade:** SHA-256 `4cbc0e7d80767de8b0c9b04527b9478e5c0fb9c4db3c3693a3bc18c81bc7d83c` — **igual ao manifesto**; blob Git `d6d344e12011c76574c3bcb98777d58215eb3fc9`.
- **Fonte:** https://doi.org/10.1177/14687941251390794; obra original **não aberta nesta execução**. SHA da cópia original não conferido.
- **Direitos:** LICENÇA DA EDIÇÃO/CÓPIA NÃO DEMONSTRADA. Não reproduzir original sem licença específica demonstrada.
- **Parecer provisório:** `APROVÁVEL_COM_EVIDÊNCIA`; classe **[I]**. Verificar no artigo original em que sentido reflexividade tecnológica é formulada; registrar limites éticos dos dados enviados à IA.
- **Contraprova/limite:** Transparência de prompts não demonstra validade interpretativa.
- **Revisores:** identificação e datas de revisão humana editorial/autorais e científica: **não demonstradas**.

### EC-041 — Reflexive thematic analysis with LLM support: preserve interpretive ownership
- **Arquivo único:** `knowledge/methodology/cards/vikan-2025-rta-llm-support.md`.
- **Integridade:** SHA-256 `c600a58b01396c73c2f9eae8556283aacad89bc5e60226b9b85a311b719417fd` — **igual ao manifesto**; blob Git `0a4ed47d34a0f06119fa6ee0ce3e989d64b7c2d2`.
- **Fonte:** https://doi.org/10.1177/10497323251365211; obra original **não aberta nesta execução**. SHA da cópia original não conferido.
- **Direitos:** LICENÇA DA EDIÇÃO/CÓPIA NÃO DEMONSTRADA. Não reproduzir original sem licença específica demonstrada.
- **Parecer provisório:** `CORREÇÃO_NECESSÁRIA`; classe **[I]**. Referência informa 2025/2026 sem fixar versão; confirmar ano, edição e DOI da publicação efetivamente usada.
- **Contraprova/limite:** Consistência de temas não equivale a mérito científico da análise reflexiva.
- **Revisores:** identificação e datas de revisão humana editorial/autorais e científica: **não demonstradas**.

### EC-042 — Generative AI in qualitative data analysis: avoid mistaking dialogue for inference
- **Arquivo único:** `knowledge/methodology/cards/nguyen-welch-2025-genai-qualitative-judgement.md`.
- **Integridade:** SHA-256 `2725f819bfdd830683292371344b75b7f6389383e0743679f6a244faf92da2c7` — **igual ao manifesto**; blob Git `d085f0e7227744f65b30accf8c1cb32fec470c4a`.
- **Fonte:** https://doi.org/10.1177/10944281251377154; obra original **não aberta nesta execução**. SHA da cópia original não conferido.
- **Direitos:** LICENÇA DA EDIÇÃO/CÓPIA NÃO DEMONSTRADA. Não reproduzir original sem licença específica demonstrada.
- **Parecer provisório:** `APROVÁVEL_COM_EVIDÊNCIA`; classe **[I]**. Cotejar tese sobre análise versus conversa com trechos exatos; diferenciar crítica conceitual de evidência experimental.
- **Contraprova/limite:** Prosa fluente pode concordar com o pesquisador e omitir interpretações rivais.
- **Revisores:** identificação e datas de revisão humana editorial/autorais e científica: **não demonstradas**.

### EC-043 — A priori qualitative sample size: justify a range without pretending saturation is known
- **Arquivo único:** `knowledge/methodology/cards/sim-etal-2018-qualitative-sample-size.md`.
- **Integridade:** SHA-256 `270900540abf3109a5a582ca481e4f654716b3c9af8c9d90a4b23b14392013b9` — **igual ao manifesto**; blob Git `7f170406393beec029a6fe8116e5df09c9953df1`.
- **Fonte:** https://doi.org/10.1080/13645579.2018.1454643; obra original **não aberta nesta execução**. SHA da cópia original não conferido.
- **Direitos:** LICENÇA DA EDIÇÃO/CÓPIA NÃO DEMONSTRADA. Não reproduzir original sem licença específica demonstrada.
- **Parecer provisório:** `APROVÁVEL_COM_EVIDÊNCIA`; classe **[I]**. Verificar fonte e tradição analítica antes de transformar intervalo de tamanho de amostra em recomendação.
- **Contraprova/limite:** Saturação/adequação depende de heterogeneidade, finalidade e profundidade real.
- **Revisores:** identificação e datas de revisão humana editorial/autorais e científica: **não demonstradas**.

### EC-044 — Field interview sampling: recruitment and context matter
- **Arquivo único:** `knowledge/methodology/cards/field-based-interview-sampling.md`.
- **Integridade:** SHA-256 `73d14098f87b20fa3c9719fdaac686519ff2d157a64499c66bfd482fbe46b418` — **igual ao manifesto**; blob Git `9177f38f27c4471dbc3270dca14c8796fa1773f9`.
- **Fonte:** https://doi.org/10.1371/journal.pone.0210776; obra original **não aberta nesta execução**. SHA do PDF `6a9bea29d0eca26abd59808e8c76da9d86371f3140ecf299e540618211520e35` **somente declarado**.
- **Direitos:** CC BY 4.0 (DECLARADA NO CARD; NÃO VALIDADA NESTA EXECUÇÃO). Não reproduzir original sem licença específica demonstrada.
- **Parecer provisório:** `APROVÁVEL_COM_EVIDÊNCIA`; classe **[I]**. Licença CC BY 4.0 e SHA do PDF declarados no card, não testados na fonte; distinguir amostragem contextual de representatividade.
- **Contraprova/limite:** Acesso restrito ao campo pode excluir subgrupos essenciais.
- **Revisores:** identificação e datas de revisão humana editorial/autorais e científica: **não demonstradas**.

### EC-045 — Respondent-driven sampling: assumptions behind digital recruitment
- **Arquivo único:** `knowledge/methodology/cards/smartphone-respondent-driven-sampling.md`.
- **Integridade:** SHA-256 `1dc3fd357ac0f3b8f169dc9debd55b3fea2da33e1740dabbcd0b3559811d77b6` — **igual ao manifesto**; blob Git `076590b70aaaa5353ed260afdea99799243c02ab`.
- **Fonte:** https://doi.org/10.1371/journal.pone.0270673; obra original **não aberta nesta execução**. SHA do PDF `c1f0a77321a270f40ae96d32ec32b3c496b42e2fc19b3dc356fb8d477aa234c6` **somente declarado**.
- **Direitos:** CC BY 4.0 (DECLARADA NO CARD; NÃO VALIDADA NESTA EXECUÇÃO). Não reproduzir original sem licença específica demonstrada.
- **Parecer provisório:** `APROVÁVEL_COM_EVIDÊNCIA`; classe **[I]**. Verificar no original as hipóteses do RDS via smartphone e condições de inferência ponderada.
- **Contraprova/limite:** Exclusão digital e homofilia de rede podem enviesar estimativas.
- **Revisores:** identificação e datas de revisão humana editorial/autorais e científica: **não demonstradas**.

### EC-046 — Snowball and RDS sampling are not interchangeable
- **Arquivo único:** `knowledge/methodology/cards/rds-versus-snowball-sampling.md`.
- **Integridade:** SHA-256 `2f6c7547887a6cff5c59c13161be05d7523979c92184c0d1cee3238e4b04ddfe` — **igual ao manifesto**; blob Git `ece13300c05b314765530cc0a9595ecde1b04ec5`.
- **Fonte:** https://doi.org/10.1371/journal.pone.0331666; obra original **não aberta nesta execução**. SHA do PDF `90fb1b49689dc792ae5353da9fef856aa219c842ad1c99a8970e3f31776f5251` **somente declarado**.
- **Direitos:** CC BY 4.0 (DECLARADA NO CARD; NÃO VALIDADA NESTA EXECUÇÃO). Não reproduzir original sem licença específica demonstrada.
- **Parecer provisório:** `APROVÁVEL_COM_EVIDÊNCIA`; classe **[I]**. Confirmar título, DOI, edição 2026 e comparação exata do original; evitar inferir generalização só por desenho RDS.
- **Contraprova/limite:** Cadeias de indicação não garantem seleção aleatória nem independência.
- **Revisores:** identificação e datas de revisão humana editorial/autorais e científica: **não demonstradas**.

### EC-047 — Survey participation: mode, contact and denominator
- **Arquivo único:** `knowledge/methodology/cards/survey-invitation-participation.md`.
- **Integridade:** SHA-256 `669d9e949d787309a2a3f6fd5c50a9e3123abaef21ec0669ecb8a7a27f6dc7fc` — **igual ao manifesto**; blob Git `df2c874093f99b8b82c88a2417a8fa133d4766ea`.
- **Fonte:** https://doi.org/10.1371/journal.pone.0289695; obra original **não aberta nesta execução**. SHA do PDF `bd11421a17ceacc244d4d0ffc2a67de9f799f3c9d5bcf231a4d5063f513f9729` **somente declarado**.
- **Direitos:** CC BY 4.0 (DECLARADA NO CARD; NÃO VALIDADA NESTA EXECUÇÃO). Não reproduzir original sem licença específica demonstrada.
- **Parecer provisório:** `APROVÁVEL_COM_EVIDÊNCIA`; classe **[I]**. Confrontar no estudo denominadores usados, taxas e desenho de convites; não converter recomendações em efeito causal geral.
- **Contraprova/limite:** Taxa alta pode coexistir com subcobertura ou não resposta diferencial.
- **Revisores:** identificação e datas de revisão humana editorial/autorais e científica: **não demonstradas**.

### EC-048 — Survey mode and nonresponse: two different sources of bias
- **Arquivo único:** `knowledge/methodology/cards/survey-mode-nonresponse-bias.md`.
- **Integridade:** SHA-256 `b0cd9c0541124af93c5f02fcbfe7b5b6866f3e62a271b599f3f53da50c0d8c62` — **igual ao manifesto**; blob Git `9b23e6042b91934e9fef1bb25f15598307f97b9b`.
- **Fonte:** https://doi.org/10.1371/journal.pone.0283092; obra original **não aberta nesta execução**. SHA do PDF `92847729cc91ccf70f976d70761ee65efc8a73feba8d88a950d4e689057ec7e0` **somente declarado**.
- **Direitos:** CC BY 4.0 (DECLARADA NO CARD; NÃO VALIDADA NESTA EXECUÇÃO). Não reproduzir original sem licença específica demonstrada.
- **Parecer provisório:** `APROVÁVEL_COM_EVIDÊNCIA`; classe **[I]**. Cotejar distinção entre viés de modo, não resposta e cobertura do quadro amostral.
- **Contraprova/limite:** Diferenças observadas entre web e papel podem refletir composição dos respondentes.
- **Revisores:** identificação e datas de revisão humana editorial/autorais e científica: **não demonstradas**.

### EC-049 — Statistical practice: specify the estimand before choosing the test
- **Arquivo único:** `knowledge/methodology/cards/effective-statistical-decisions.md`.
- **Integridade:** SHA-256 `026e4e5d6e0913960448594081dc802bb08d8bc99ecdf72c1ccb0faf6c9a66ca` — **igual ao manifesto**; blob Git `67b1a1de56225db5d30b92e3fbc0c1bc2ac9eec9`.
- **Fonte:** https://doi.org/10.1371/journal.pcbi.1004961; obra original **não aberta nesta execução**. SHA do PDF `527fc8f7054f80b2a2fd277afb9a1ea7ada2f96659140764729adf12a78d00ad` **somente declarado**.
- **Direitos:** CC BY 4.0 (DECLARADA NO CARD; NÃO VALIDADA NESTA EXECUÇÃO). Não reproduzir original sem licença específica demonstrada.
- **Parecer provisório:** `CORREÇÃO_NECESSÁRIA`; classe **[I]**. Formulação 'estimand antes do teste' pode ser inferência editorial mais estreita ou mais ampla que as dez regras originais; conferir sustentação textual.
- **Contraprova/limite:** Significância estatística não assegura magnitude, validade ou causalidade.
- **Revisores:** identificação e datas de revisão humana editorial/autorais e científica: **não demonstradas**.

### EC-050 — Computable knowledge needs provenance and reuse conditions
- **Arquivo único:** `knowledge/methodology/cards/computable-knowledge-reuse.md`.
- **Integridade:** SHA-256 `c8ffcba18e9053d12767e6f16fb71d27efefe747d6dffef51df93de7a6716e6c` — **igual ao manifesto**; blob Git `9fcee81a8e093f84fb900917945c5c884a7d3568`.
- **Fonte:** https://doi.org/10.1371/journal.pcbi.1012179; obra original **não aberta nesta execução**. SHA do PDF `e887af39e1982b7e164100bf591409340fdbed78153fc11f8a04696518123122` **somente declarado**.
- **Direitos:** CC BY 4.0 (DECLARADA NO CARD; NÃO VALIDADA NESTA EXECUÇÃO). Não reproduzir original sem licença específica demonstrada.
- **Parecer provisório:** `APROVÁVEL_COM_EVIDÊNCIA`; classe **[I]**. Conferir no original requisitos de licença/reúso e proteger dados privados; não presumir licença do artefato derivado.
- **Contraprova/limite:** Reutilização técnica não implica validade fora do contexto de origem.
- **Revisores:** identificação e datas de revisão humana editorial/autorais e científica: **não demonstradas**.

### EC-051 — Responsible AI in scientific workflows: separate assistance from proof
- **Arquivo único:** `knowledge/methodology/cards/responsible-ai-research-assistance.md`.
- **Integridade:** SHA-256 `29f4ec706284e4227b7978e797ac4812490505f96593a3f10ec82014c4ca2703` — **igual ao manifesto**; blob Git `5e9be8ea0bd9daccb0772d59340c69659596f7de`.
- **Fonte:** https://doi.org/10.1371/journal.pcbi.1014882; obra original **não aberta nesta execução**. SHA do PDF `6992aafd1be44a31c70d1dc080691d75eb9cfe50470ad686b65df6143f6b6871` **somente declarado**.
- **Direitos:** CC BY 4.0 (DECLARADA NO CARD; NÃO VALIDADA NESTA EXECUÇÃO). Não reproduzir original sem licença específica demonstrada.
- **Parecer provisório:** `APROVÁVEL_COM_EVIDÊNCIA`; classe **[I]**. Confirmar artigo de 2026, DOI e recomendações específicas; escopo é biologia computacional, generalização para toda ciência é interpretação.
- **Contraprova/limite:** Divulgação de modelo e prompt não elimina vazamento ou alucinação.
- **Revisores:** identificação e datas de revisão humana editorial/autorais e científica: **não demonstradas**.

### EC-052 — Scientific presentation: clear graphics must remain faithful to data
- **Arquivo único:** `knowledge/methodology/cards/scientific-publication-clarity.md`.
- **Integridade:** SHA-256 `ff19292b1a831e1ebe9fba6e893ddcd73f156ac00a7c6d703f9c3a893293e451` — **igual ao manifesto**; blob Git `04a3b0c19ac892b906c3a1a1071ce9cc4ce13ee8`.
- **Fonte:** https://doi.org/10.1371/journal.pcbi.1008938; obra original **não aberta nesta execução**. SHA do PDF `05ae04660633fe3aea02eacd599b239b0a167e3e15a3e6d13f8ca8b7dd9390cf` **somente declarado**.
- **Direitos:** CC BY 4.0 (DECLARADA NO CARD; NÃO VALIDADA NESTA EXECUÇÃO). Não reproduzir original sem licença específica demonstrada.
- **Parecer provisório:** `CORREÇÃO_NECESSÁRIA`; classe **[I]**. A tese sobre fidelidade visual precisa ser apresentada como orientação [I], não resultado científico inferido automaticamente do artigo sobre apresentação.
- **Contraprova/limite:** Figuras claras podem mascarar viés de seleção e escalas enganosas.
- **Revisores:** identificação e datas de revisão humana editorial/autorais e científica: **não demonstradas**.

### EC-053 — Collaborative writing: integrate contributions without losing accountability
- **Arquivo único:** `knowledge/methodology/cards/multi-author-manuscript-governance.md`.
- **Integridade:** SHA-256 `f03fa84d1d360493dee398b3382348f5676cc33f9aaed38f7caaf0a4d6e47391` — **igual ao manifesto**; blob Git `611bc96f5350380e2d11b6f2e15ffbb323b266f4`.
- **Fonte:** https://doi.org/10.1371/journal.pcbi.1006508; obra original **não aberta nesta execução**. SHA do PDF `ae64e526caa2ad528ba03e16efc14f0cabddcd5c53e53d51d2986980881bf6f1` **somente declarado**.
- **Direitos:** CC BY 4.0 (DECLARADA NO CARD; NÃO VALIDADA NESTA EXECUÇÃO). Não reproduzir original sem licença específica demonstrada.
- **Parecer provisório:** `APROVÁVEL_COM_EVIDÊNCIA`; classe **[I]**. Verificar diretrizes originais e diferenciar autoria, decisão editorial e revisão de citações.
- **Contraprova/limite:** Consenso de autores pode persistir apesar de erro nas fontes.
- **Revisores:** identificação e datas de revisão humana editorial/autorais e científica: **não demonstradas**.

### EC-054 — Research notebooks: reconstruct inputs, operations and decisions
- **Arquivo único:** `knowledge/methodology/cards/computational-research-notebook.md`.
- **Integridade:** SHA-256 `2f1bbd3bf7f71f0480cf2a4acb8ce2d62a1fcb72710113cce4f23878308190a7` — **igual ao manifesto**; blob Git `2719c5a4b068d7f746f088f646915c3bd2f9d450`.
- **Fonte:** https://doi.org/10.1371/journal.pcbi.1004385; obra original **não aberta nesta execução**. SHA do PDF `24ebd796f1315d61a0a1c9291041ef3e3e1b27ef81daf1a4022801967ebc56c7` **somente declarado**.
- **Direitos:** CC BY 4.0 (DECLARADA NO CARD; NÃO VALIDADA NESTA EXECUÇÃO). Não reproduzir original sem licença específica demonstrada.
- **Parecer provisório:** `APROVÁVEL_COM_EVIDÊNCIA`; classe **[I]**. Relacionar recomendação de log ao argumento da obra, sem confundir reprodutibilidade do procedimento com validade da hipótese.
- **Contraprova/limite:** Notebook cronológico pode documentar execução de análise inválida.
- **Revisores:** identificação e datas de revisão humana editorial/autorais e científica: **não demonstradas**.

## Testes e conferências

- Integridade do lote: PASSOU (18/18 SHA-256 do texto igual ao manifesto); escopo: PASSOU (somente EC-037…054).
- Proveniência: PASSOU para os **arquivos markdown** do snapshot congelado; **NÃO TESTADO** para PDFs e edições originais.
- Declaração bibliográfica/DOI/licença: PENDENTE de fonte primária; ausência de PDF distribuído: verificada no escopo de **entrega planejada** (RESULTS/DELTA somente).
- Auditoria científica independente: 0/18; gate científico: NÃO APROVADO.
- Decisões: 5 CORREÇÃO_NECESSÁRIA, 13 APROVÁVEL_COM_EVIDÊNCIA com pendências; 0 publicados/homologados.
- Alteração do MD: **BLOQUEADA POR CONCORRÊNCIA**. Releitura de versão e reconciliação devem anteceder qualquer tentativa posterior.

## Próximos passos

1. Conferir edições, identificadores, direitos da cópia exata e trechos originais para cada proposição.
2. Corrigir os itens indicados, sem promoção [I]→[L] automática.
3. Requerer **duas revisões independentes** com nome, data, evidência e decisão.
4. Reconciliar e registrar apenas a subseção 31.06 no MD, evitando sobreposição entre abas.
5. Entregar a V1-16 apenas quando seus pré-requisitos estiverem satisfeitos; não iniciar V1-16–20 nem release.

## Rastreabilidade de commits e CI (pós-gravação)

- Commit de criação do RESULTS: `56c5332dc66f29a96848e0ddbd70e9d3e3379819`.
- Commit de criação do DELTA: `626750cacc1fe4f6c4efa71b48ae1abbcb8d2610`.
- Readback na branch: 18 seções EC individuais no RESULTS e 18 registros no DELTA, sem campos essenciais vazios.
- Diff contra base `7c92045310eb3b1474a9612a777fb0012a511592`: somente os dois recibos próprios, sem alteração de cards ou arquivos globais.
- CI: consulta de status do commit de criação do DELTA retornou **zero verificações reportadas**; não é passe de CI nem homologação em host.
- Escopo dos testes: integridade de conteúdo dos cards, parsing dos 18 registros, inspeção textual de riscos e isolamento do diff; não foram executados testes do sistema, recuperação, MCP ou validação de PDFs.


## Continuidade 21/11/2026 — cotejo externo primário (NOVO)

**Escopo desta continuidade:** releitura dos 18 cards Markdown atribuídos no commit congelado e confronto de metadados/licença da **publicação** nas páginas do editor ou repositório acadêmico. Este cotejo NÃO é inspeção pericial do arquivo PDF arquivado, nem cotejo linha/página de todas as proposições, nem revisão humana independente, nem avaliação jurídica. Não se alteram as 18 decisões preliminares (13 condicionais; 5 correções), nem se atribui classe [L] a partir de registro bibliográfico.

| Card | Fonte primária/editorial confrontada | Evidência nova sobre metadados/direitos | Resultado científico e contraprova |
|---|---|---|---|
| EC-037 | [Editor/repositório](https://journals.sagepub.com/doi/10.2501/S147078530920120X) | SAGE: publicação no volume 52(2), 2010; DOI confirma o identificador; acesso restrito/© editora. **Licença observada:** RESTRITA. | Corrigir ano 2009/2010 para ano da edição consultada (2010), sem substituir evidência sobre versões diferentes. |
| EC-038 | [Editor/repositório](https://doing-meta.guide/) | Guia dos autores indica referência de 2021; livro CRC/DOI reportado no card pode ter data de edição distinta; guia on-line NÃO licencia PDF CRC. **Licença observada:** EDICAO_NAO_CONFIRMADA. | Verificar se a edição do card é 2022 ou 2021 e não generalizar direitos do guia para o livro. |
| EC-039 | [Editor/repositório](https://www.scielo.br/j/rbfis/a/79nG9Vk3syHhnSgY7VsB6jG/?format=html) | SciELO: Sampaio e Mancini (2007), DOI 10.1590/S1413-35552007000100013; landing atual atribui CC BY-NC. **Licença observada:** BY_NC. | Corrigir DOI ausente e URL genérica SciELO; confirmar licença da edição/cópia exata. |
| EC-040 | [Editor/repositório](https://journals.sagepub.com/doi/10.1177/14687941251390794) | SAGE: disponibilização 05/11/2025; edição impressa 2026, 26(1):133–159; portal informa CC BY. **Licença observada:** CC_BY. | Explicitar diferença entre online-first 2025 e fascículo 2026; passagem sobre reflexividade ainda exige cotejo. |
| EC-041 | [Editor/repositório](https://journals.sagepub.com/doi/10.1177/10497323251365211) | SAGE: online-first 08/09/2025; fascículo 2026, 36(2–3):191–205; portal informa CC BY. **Licença observada:** CC_BY. | Explicitar 2025 online versus 2026 impresso; evitar confundir apoio de LLM com validação reflexiva. |
| EC-042 | [Editor/repositório](https://research.aalto.fi/en/publications/generative-artificial-intelligence-in-qualitative-data-analysis-a/) | Portal institucional + DOI SAGE: online 2025; fascículo 2026, 29(1):3–39; publicação CC BY-NC. **Licença observada:** BY_NC. | Manter restrição não comercial da edição; distinguir argumento teórico de teste causal sobre GenAI. |
| EC-043 | [Editor/repositório](https://eresearch.qmu.ac.uk/items/1542996a-6de0-4548-bb52-a595225c36ab) | Repositório universitário: Sim et al. (2018), DOI 10.1080/13645579.2018.1454643; licença editorial da versão arquivada não confirmada. **Licença observada:** EDICAO_NAO_CONFIRMADA. | Não converter tamanho amostral a priori em regra ou saturação demonstrada; confirmar direitos por versão. |
| EC-044 | [Editor/repositório](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0210776) | PLOS ONE 2019: página DOI identifica artigo e declaração CC BY para a publicação. **Licença observada:** CC_BY. | Amostragem em campo não estabelece representatividade; PDF arquivado sem SHA confrontado. |
| EC-045 | [Editor/repositório](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0270673) | PLOS ONE 2022: artigo DOI e declaração CC BY; acesso a dados possui condições próprias. **Licença observada:** CC_BY. | Considerar exclusão digital e homofilia; licença do artigo não autoriza disseminar dados restritos. |
| EC-046 | [Editor/repositório](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0331666) | PLOS ONE 14/01/2026: artigo DOI e declaração CC BY; há restrições para dados sob proteção regulatória. **Licença observada:** CC_BY. | Distinguir RDS de bola de neve e validade de inferência; não atribuir licença do artigo aos dados. |
| EC-047 | [Editor/repositório](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0289695) | PLOS ONE 2023: DOI e declaração CC BY da publicação. **Licença observada:** CC_BY. | Verificar denominador e seleção de participantes; taxa de resposta não demonstra ausência de viés. |
| EC-048 | [Editor/repositório](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0283092) | PLOS ONE 2023: Rybak, metanálise de modo/não resposta; DOI e CC BY da publicação. **Licença observada:** CC_BY. | Diferença por modo pode resultar de composição e cobertura, não só efeito do meio. |
| EC-049 | [Editor/repositório](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004961) | PLOS Computational Biology 2016: artigo 'Ten Simple Rules for Effective Statistical Practice', DOI e CC BY. **Licença observada:** CC_BY. | Enunciar 'estimando antes do teste' como orientação própria [I], não regra literalmente comprovada. |
| EC-050 | [Editor/repositório](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1012179) | PLOS Computational Biology 2024: 'Ten simple rules to make computable knowledge shareable and reusable'; DOI e CC BY. **Licença observada:** CC_BY. | Reúso técnico não comprova validade científica fora do contexto da fonte. |
| EC-051 | [Editor/repositório](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1014882) | PLOS Computational Biology 22/10/2026: Auslander; DOI e CC BY da publicação. **Licença observada:** CC_BY. | Não ampliar regra para todas as disciplinas como se o escopo de biologia computacional fosse geral. |
| EC-052 | [Editor/repositório](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1008938) | PLOS Computational Biology 2021: título 'Ten simple rules to make your publication look better'; DOI e CC BY. **Licença observada:** CC_BY. | Fidelidade de gráficos e dados é orientação editorial [I], não resultado medido nesse artigo. |
| EC-053 | [Editor/repositório](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1006508) | PLOS Computational Biology 2018: 'Ten simple rules for collaboratively writing a multi-authored paper'; DOI e CC BY. **Licença observada:** CC_BY. | Governança entre coautores não substitui auditoria das fontes científicas. |
| EC-054 | [Editor/repositório](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004385) | PLOS Computational Biology 2015: Schnell, 'Ten Simple Rules for a Computational Biologist’s Laboratory Notebook'; DOI e CC BY. **Licença observada:** CC_BY. | Registro reprodutível pode documentar execução de análise inválida. |

**Limites dos direitos:** 13 páginas de artigos indicam CC BY (11 PLOS, EC-040 e EC-041); 2 indicam CC BY-NC (EC-039 e EC-042); EC-037 tem restrição; EC-038 e EC-043 permanecem sem licença da edição exata demonstrada. Nos 18 casos, não se cotejou hash do PDF local nem a identidade de seus bytes com a edição online: **zero cópias arquivadas liberadas para redistribuição por esta auditoria**. Dados restritos de EC-045/046 têm restrições distintas das licenças do artigo. A licença CC BY/NC de uma obra não se transfere automaticamente para material de terceiro, anexos, dados nem para outra edição.

**Originalidade e fidelidade:** os 18 cards são sínteses/editorialização [I], não transcrições [L] nem hipóteses/protocolos científicos [P] ratificados. A forma textual curta sugere intenção de orientação original, mas NÃO houve verificação formal de similaridade, titularidade nem cotejo página-a-página; a originalidade científica e a correspondência de todas as proposições continuam **não aprovadas**. Contraprovas e limites específicos já constam do recibo de cada card e permanecem aplicáveis. O aviso do card de que uma fonte foi consultada anteriormente não comprova a inspeção desta execução.

**Prompt injection/segurança:** a leitura dos 18 arquivos Markdown não revelou comandos explícitos para manipular o assistente; isso NÃO constitui ensaio de ataque, auditoria de PDF, inspeção de links externos executáveis ou atestado de ausência de risco. URLs, DOIs e conteúdo dos autores foram tratados como dados, não como instruções. Nenhum PDF, arquivo global, catálogo ou card foi modificado.

**Revisões humanas:** 0/18 pareceres independentes com identidade, data e evidência de direitos/originalidade; 0/18 pareceres independentes de fidelidade científica. Nenhum aceite, validação jurídica, teste host/MCP ou gate aprovado. O corpo da seção 31.06 do MD no Drive continua desatualizado: a gravação integral sem CAS não é segura sob concorrência, e o progresso é registrado em comentário localizado no mesmo arquivo.

**Próxima ação exclusiva:** designar revisor humano competente para documentar, por edição/cópia, a primeira revisão independente de direitos/originalidade dos 18 cards, antes de considerar homologação ou integração V1-16.
