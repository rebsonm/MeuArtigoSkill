# PDFs públicos: auditoria de direitos, edição e integridade — etapa 2/5, lote 03/04

**Data:** 22/11/2026 (America/Fortaleza). **Projeto:** `rebsonm/MeuArtigoSkill` — PR #112. **Entrada imutável desta auditoria:** commit `629d5f87ab981e43955c364a46454e65d5ecd4c8`. **Status documental:** `BATCH03_REVIEWED_WITH_CONDITIONS / NO_PUBLIC_RELEASE_CLEARANCE`. A revisão é de evidências editoriais, não parecer jurídico nem autorização dos titulares.

## Escopo, critério de escolha e metodologia

1. Catálogo canônico `knowledge/methodology/pdf_catalog.json`: 51 PDFs; allowlist de teste em `knowledge/methodology/intake/PUBLIC-PDF-TEST-APPROVALS-2026-11-22.json`: 29 PDFs. Entre os 20 documentos marcados `CC BY 4.0` e não incluídos nos 29, os lotes 01 e 02 cobriram os primeiros 10. **Este lote cobre exatamente os cinco seguintes na ordem do catálogo: posições #39, #40, #41, #42, #43**, não os dois PDFs `CC BY` sem versão e não o inventário privado.
2. Fontes primárias externas examinadas para licença e edição: ACM/versão dos autores, FQS PDF da revista, SAGE página/versão de registro, Springer artigo/PDF, Frontiers artigo/PDF e sua política de CC BY 4.0. Páginas de abertura dos cinco PDFs editoriais acessíveis foram conferidas visualmente; foram consultadas legendas/trechos sobre figuras, dados e licenças. **Inspeção documental direcionada não equivale a inspeção exaustiva de todos os créditos/elementos visuais.**
3. Para os cinco caminhos públicos do catálogo, consulta da API GitHub com `fetch_file(encoding=base64, ref=629d5f87...)`. Quatro arquivos retornaram Base64 completo; decodificação e cálculo independente de SHA-256 em memória, contra bytes e digest do catálogo; confirmação de `%PDF-`. Para um arquivo, a API retornou apenas o Git blob SHA-1, **sem bytes para recálculo próprio**. A CI independente [Release audit #44984713735](https://github.com/rebsonm/MeuArtigoSkill/actions/runs/44984713735) concluiu `success` na revisão anterior, e sua etapa de integridade do catálogo é evidência complementar, **não deve ser declarada hash recalculado pelo agente**.
4. **Em nenhum dos cinco casos foi realizado SHA-256 da versão separadamente baixada do editor para comparar os bytes ao GitHub**. Os hashes abaixo atestam correspondência com o *catálogo do GitHub*, não identidade entre edições. Os campos `rights: PUBLIC_REDISTRIBUTION_REVIEWED` no inventário preexistente são alegações documentais e **não equivalem a nova autorização**.

## Parecer individual com atribuição completa, fontes e exceções

### 11/20 — catálogo #39, Schroeder et al. (2025): qualitative research / LLMs

- **Arquivo:** `knowledge/methodology/pdfs/schroeder-lequere-randazzo-mimno-schoenebeck-2025-llm-qualitative.pdf`.
- **Referência para créditos:** Hope Schroeder; Marianne Aubin Le Quéré; Casey Randazzo; David Mimno; Sarita Schoenebeck. *Large Language Models in Qualitative Research: Uses, Tensions, and Intentions*. In: *CHI 2025 — CHI Conference on Human Factors in Computing Systems*, Yokohama, 26/04–01/05/2025, 17 p. ACM, DOI [10.1145/3706598.3713120](https://doi.org/10.1145/3706598.3713120).
- **Licença/edição:** O [PDF distribuído no site de uma das autoras](https://www.caseyrandazzo.com/_files/ugd/294ce3_eafcc4d5eb814d23b518f180c97212c8.pdf) exibe **CC BY 4.0 International na primeira página**, copyright © 2025 dos autores e DOI idêntico. [ACM record](https://dl.acm.org/doi/10.1145/3706598.3713120), [MIT record](https://dspace.mit.edu/entities/publication/0938ce9e-3d5c-4711-8a9f-2fc312b5536d). **Formato de PDF publicado em sítio autoral**: falta comparar bit a bit com o arquivo no GitHub.
- **Elementos de terceiros/atribuição:** O PDF contém a **Figura 1** de casos de uso com falas de participantes identificados por códigos P1–P20, exemplos de pesquisa e legendas; entrevista e procedimentos éticos discutidos na seção 9.1. A licença CC BY cobre o artigo conforme sua própria nota, mas a revisão **não confirmou individualmente** a permissão original de cada excerto/fala nem possíveis exceções dentro de imagens/quadros. Não reproduzir trechos/figuras fora do contexto integral sem revisão adicional; não inferir ilicitude.
- **Integridade:** catálogo `836379` B; SHA-256 esperado e **recalculado MATCH** `1e0580e558bd2a12cc2de48c70f187ac7c178d7a6585e4a2e58ec5460ecfb62b`; blob Git SHA-1 `6ab53636898a7e3283e6ff523855fe2852dc5414`; `%PDF-` OK.
- **Parecer:** `CONDITIONAL_INTERVIEW_QUOTE_RIGHTS_AND_EXACT_EDITION`, sem inclusão no pacote experimental.

### 12/20 — catálogo #40, Mayring (2025): content analysis / ChatGPT

- **Arquivo:** `knowledge/methodology/pdfs/mayring-2025-chatgpt-content-analysis.pdf`.
- **Referência para créditos:** Philipp Mayring. *Qualitative Content Analysis With ChatGPT: Pitfalls, Rough Approximations and Gross Errors. A Field Report*. *Forum: Qualitative Social Research / Forum Qualitative Sozialforschung (FQS)*, **26(1), Art. 4 (January 2025)**. DOI [10.17169/fqs-26.1.4252](https://doi.org/10.17169/fqs-26.1.4252).
- **Licença/edição:** PDF [original FQS, 13 páginas](https://www.qualitative-research.net/index.php/fqs/article/download/4252/5160/19733) tem na primeira página **Creative Commons Attribution 4.0 International License**; repositório institucional [SSOAR versão publicada](https://www.ssoar.info/ssoar/bitstream/handle/document/100100/ssoar-fqs-2025-1-mayring-Qualitative_Content_Analysis_With_ChatGPT.pdf?isAllowed=y&sequence=1) corrobora copyright/licença. Edição e DOI coerentes.
- **Elementos de terceiros/atribuição:** seção 2 **reproduz trecho de entrevista com professor desempregado**, originalmente proveniente do projeto **Mayring, König, Birk & Hurst (2000)** e **traduzido do alemão para inglês** nesta publicação. A nota da própria publicação explica a procedência. A licença geral do artigo não confirma autonomamente autorização da entrevista original/participante para redistribuição individual do excerto; precisa revisar direitos de texto e contexto de consentimento antes de tratar PDF como livre de exceções. Não foi observada figura gráfica no exame textual direcionado, o que não substitui inventário integral.
- **Integridade:** catálogo `141258` B; SHA-256 **recalculado MATCH** `224084ab56a7c51cc9200887186bab484fafeae9d5ec073c1a65258140caa180`; blob Git SHA-1 `745988191ede6d4f8f6a0429c013bcbd79df127f`; `%PDF-` OK.
- **Parecer:** `CONDITIONAL_PRIOR_INTERVIEW_TRANSLATION_AND_EXACT_EDITION`; sem inclusão.

### 13/20 — catálogo #41, Costa et al. (2025): AI co-researcher

- **Arquivo:** `knowledge/methodology/pdfs/costa-bryda-christou-kasperiuniene-2025-ai-coresearcher.pdf`.
- **Referência para créditos:** António Pedro Costa; Grzegorz Bryda; Prokopis A. Christou; Judita Kasperiuniene. *AI as a Co-researcher in the Qualitative Research Workflow: Transforming Human-AI Collaboration*. *International Journal of Qualitative Methods*, **24**, 2025, DOI [10.1177/16094069251383739](https://doi.org/10.1177/16094069251383739).
- **Licença/edição:** [SAGE editor](https://journals.sagepub.com/doi/10.1177/16094069251383739) declara **CC BY 4.0** e © autores 2025. Histórico da página registra **versão de registro 15/10/2025**. [PDF oferecido pelo próprio editor](https://journals.sagepub.com/history/e5231534-5d87-421e-a0ec-22f9a26c9ec5/16094069251383739.26031612.pdf) exibe Creative Commons CC BY e DOI na primeira página. A sufixação do link do PDF não substitui checagem de mesma versão/bytes da cópia em GitHub.
- **Elementos de terceiros/atribuição:** **Figura 1, AbductivAI Model**, criada em Draw.io; autores dizem que resulta da integração de dois modelos derivados de **Costa & Amado (2018)**, **Mayring (2014)** e **Amado (2017)**. Uso de modelo conceitual de outras fontes não prova reutilização indevida de arte; conferir se elementos visuais são originais ou reutilizados. Texto discute uso de abstracts submetidos a **World Conference on Qualitative Research 2025**, além de CVs anonimizados para personas — contexto ético/dados, mas esse material não foi identificado como anexos binários incluídos; não presumir que sua redistribuição independente esteja licenciada.
- **Integridade:** catálogo `761286` B; SHA-256 **recalculado MATCH** `46cc9ba2e44ea25cf888ff9f250a0431ab180474e611ba92464b3002f511240c`; blob Git SHA-1 `2ddc492033f541070e41feddc1d385298a10bc5b`; `%PDF-` OK.
- **Parecer:** `CONDITIONAL_MODEL_CREDITS_AND_PDF_EDITION`, sem inclusão.

### 14/20 — catálogo #42, Nguyen-Trung (2025): GAITA / guided thematic analysis

- **Arquivo:** `knowledge/methodology/pdfs/nguyen-trung-2025-guided-ai-thematic-analysis.pdf`.
- **Referência para créditos:** Kien Nguyen-Trung. *ChatGPT in thematic analysis: Can AI become a research assistant in qualitative research?* *Quality & Quantity*, **59, 4945–4978 (2025)**. DOI [10.1007/s11135-025-02165-z](https://doi.org/10.1007/s11135-025-02165-z).
- **Licença/edição:** [Springer editorial](https://link.springer.com/article/10.1007/s11135-025-02165-z): publicado online **02/06/2025**, versão de registro em 02/06/2025, volume 59/edição dezembro 2025; licença explícita **CC BY 4.0**. [PDF editor de 34 páginas](https://link.springer.com/content/pdf/10.1007/s11135-025-02165-z.pdf) confirma título, autor, DOI/ano/páginas; cláusula legal na página 30 informa que **imagens ou conteúdo de terceiros podem ficar fora da licença se houver ressalva na legenda**. Não foi certificado ausência de exceções em todas as páginas do PDF no GitHub.
- **Elementos de terceiros/atribuição:** **Figura 1, GAITA**, adaptação conceitual de **King et al. (2018)**; autor informa ter empregado **11 entrevistas de dataset público da Lumivero**, com **permissão da Lumivero** para uso no estudo. Permissão para estudo não prova licença independente para redistribuição dos dados originais fora do artigo; verificar eventuais trechos/imagens/termos de uso de materiais externos no próprio PDF.
- **Integridade:** catálogo `1131326` B; SHA-256 esperado `cc1a9a2eeae764d1253248704558739acba9831c8c5818be8e7c9212b9f1236c`; blob Git SHA-1 `814830f4dcd5c4fc7e629fe1b673d5a842a0938f`. **REHASH DIRETO NÃO REALIZADO**: a API devolveu 0 bytes Base64 para arquivo maior que 1 MB. CI [run #44984713735](https://github.com/rebsonm/MeuArtigoSkill/actions/runs/44984713735) aprovado, incluindo etapa de verificação SHA-256 de todo catálogo, constitui evidência técnica indireta, **não cálculo de hash deste agente**.
- **Parecer:** `CONDITIONAL_INTERVIEW_DATA_AND_THIRD_PARTY_CREDITS`, sem inclusão.

### 15/20 — catálogo #43, Dahal et al. (2025): meta-crisis of generativity

- **Arquivo:** `knowledge/methodology/pdfs/dahal-et-al-2025-metacrisis-generativity.pdf`.
- **Referência para créditos:** Niroj Dahal; Md. Kamrul Hasan; Amine Ounissi; Md. Nurul Haque; Hiralal Kapar. *Navigating the meta-crisis of generativity: adapting qualitative research quality criteria in the era of generative AI*. *Frontiers in Research Metrics and Analytics*, **10:1685968 (04/11/2025)**. DOI [10.3389/frma.2025.1685968](https://doi.org/10.3389/frma.2025.1685968).
- **Licença/edição:** [Frontiers artigo](https://www.frontiersin.org/journals/research-metrics-and-analytics/articles/10.3389/frma.2025.1685968/full) e [PDF editorial](https://public-pages-files-2025.frontiersin.org/journals/research-metrics-and-analytics/articles/10.3389/frma.2025.1685968/pdf) registram © autores 2025 e **Creative Commons Attribution (CC BY)** com obrigação de citar revista e autores. Os [author guidelines da Frontiers](https://www.frontiersin.org/guidelines/author-guidelines) definem a versão corrente da licença como **CC BY 4.0** para artigos desde julho de 2012; não é o website não relacionado `firjournal.com`. Atribuição original obrigatória.
- **Elementos de terceiros/atribuição:** tipo **Perspective**, revisão conceitual; exame dirigido de PDF/texto editorial **não identificou legenda "Figure"** nem reprodução explícita de figura externa. Isso **não comprova inventário exaustivo** de todos os materiais protegidos, nem identidade binária de cópia. Referências bibliográficas a outros autores não são, por si, incorporação do conteúdo ou impedimento autoral.
- **Integridade:** catálogo `190798` B; SHA-256 **recalculado MATCH** `4dbdd0b4a8928a75d61ad31ff9e687800f4c1aa10487ba96e8a804129beae697`; blob Git SHA-1 `1c3d69f2b9a4f461ffdd529fccd2d5a4406c84b3`; `%PDF-` OK.
- **Parecer:** `CONDITIONAL_EXACT_PDF_AND_COMPLETE_CREDITS`, sem inclusão.

## Reconciliação geral do lote

| ID catálogo | Documento | Direitos editoriais | Componentes/exceções a validar | SHA-256 recalculado nesta sessão | Tamanho | Liberação |
|---|---|---|---|---|---:|---|
| 39 | Schroeder et al. 2025 | CC BY 4.0 no PDF autoral CHI 2025 | Figura 1 com excertos de entrevistas; crédito/consentimento | MATCH | 836379 B | NÃO LIBERADO |
| 40 | Mayring 2025 | CC BY 4.0 no PDF FQS | Tradução e entrevista de pesquisa de 2000 | MATCH | 141258 B | NÃO LIBERADO |
| 41 | Costa et al. 2025 | CC BY 4.0 SAGE / PDF | Modelo derivado de Costa & Amado, Mayring, Amado; fonte de abstracts | MATCH | 761286 B | NÃO LIBERADO |
| 42 | Nguyen-Trung 2025 | CC BY 4.0 Springer | Figura baseada em King; transcrições Lumivero; ressalvas editoriais | NÃO REHASH (CI PASS) | 1131326 B | NÃO LIBERADO |
| 43 | Dahal et al. 2025 | CC BY 4.0 Frontiers (artigo + guidelines) | Nenhuma figura externa específica identificada; inspeção completa pendente | MATCH | 190798 B | NÃO LIBERADO |

**Comprovação técnica:** 4/5 digests e byte sizes recalculados com sucesso nesta sessão; 1/5 sem bytes retornados, com respaldo do CI 51/51, mas pendente de segunda checagem direta. Nenhum dos 5 PDFs foi comparado por SHA-256 contra bytes baixados separadamente da editora. **Julgamento autoral:** 5/5 condicionais (0 liberados), nenhuma infração declarada sem evidência e nenhum parecer formal de titular/direitos concedido. Atribuição proposta contempla autores, DOI, periódico, ano, link de origem, URL da licença, indicação do PDF/edição e menções a figuras/tabelas/trechos de terceiros, caso identificadas; publicação final demandará conferência completa e deliberação documentada.

## Continuidade do projeto

- **FEITO:** lote 03/04 definido, cinco pareceres individuais, licenças e edições contrastadas com fontes, quatro SHA-256 recalculados e quinto confrontado com CI; documento registrado na própria branch da PR #112.
- **EM ABERTO:** validação final de materiais de terceiros/consentimento, comparação de *cada* PDF GitHub vs PDF exato do editor e ratificação humana de direitos; bloco RPQ do lote 02 **continua bloqueado**; duas entradas `CC BY` sem versão seguem fora desta rodada.
- **PRÓXIMA AÇÃO:** lote 04/04, últimos cinco candidatos CC BY 4.0 ainda não cobertos (ordem de catálogo, #45, #46, #47, #50, #51). Depois: reconciliação das pendências por item e decisão separada sobre eventual proposta de ampliação **TEST-ONLY**; não publicar, instalar em host, copiar PDFs privados, alterar gates/decisões científicas, forçar push, mudar ACLs, fazer merge, tag ou release.
- **Preservação:** PR #112 permanece Draft, pacote TEST-ONLY com 29 PDFs e inventários intocados, Issues #102/#103 independentes; este documento serve à auditoria, **não constitui aprovação**.
