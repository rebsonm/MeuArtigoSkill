# Meu Artigo — revisão documental dos PDFs públicos — etapa 2/5, lote 04/04

**Data:** 2026-11-22 (America/Fortaleza). **PR:** [#112](https://github.com/rebsonm/MeuArtigoSkill/pull/112), **Draft**. **Entrada congelada:** `db6a8e54f200f273bc756785b96ae1559a9271c7`. **Resultado:** `BATCH04_DOCUMENTARY_REVIEW_COMPLETE_WITH_CONDITIONS`; **não é autorização jurídica, científica ou de distribuição**. Sem merge, release ou alteração da allowlist.

## Escopo e sequência reproduzível

- Inventário público `knowledge/methodology/pdf_catalog.json`: 51 PDFs. Pacote TEST-ONLY: 29 documentos inalterados, listados em `knowledge/methodology/intake/PUBLIC-PDF-TEST-APPROVALS-2026-11-22.json`. Excluir os 29 e os dois `CC BY` sem versão do escopo desta ronda, selecionar os 20 restantes marcados `CC BY 4.0` e ordená-los pela posição original no catálogo; os lotes 1–3 documentaram os primeiros 15. **Este lote examina #45, #46, #47, #50 e #51**, completando a *cobertura documental dos vinte candidatos*, **não** uma liberação dos vinte para redistribuição.
- Verificação: fontes oficiais de editores e arXiv para título, autores, DOI, licença/versão, ano de publicação online vs edição; exame direcionado de texto editorial (gráficos, tabelas, fontes de dados e atribuições) e acesso ao PDF editorial do JMIR, do Springer e ao preprint do arXiv. As tentativas de captura visual de páginas desses PDFs pela ferramenta de web falharam com erro de cache; **não afirmar revisão visual completa dessas edições**. A fonte editorial HTML permitiu checar outros elementos. Materiais protegidos de terceiros não são automaticamente cobertos por licença do artigo quando excluídos expressamente.
- Integridade: a API GitHub forneceu os PDFs como Base64 no commit congelado; **4/5** retornaram bytes completos, foram decodificados em memória e re-hasheados SHA-256 (função validada com vetor conhecido de `abc`), tamanho em bytes e cabeçalho `%PDF-` conferidos. Para #50, a API **retornou 0 bytes**, ainda que tenha retornado Git blob SHA-1; portanto, nenhum SHA-256 independente foi calculado para #50. Como respaldo separado, a GitHub Actions [Release audit #44985054731](https://github.com/rebsonm/MeuArtigoSkill/actions/runs/44985054731) finalizou `success` na entrada congelada e marcou a etapa `Verify every catalogued public PDF against its SHA-256` como `success` para o catálogo. **Hash de cópia editorial não foi calculado para nenhum destes 5: identidade binária editor x GitHub NÃO VERIFICADA**.
- Os campos preexistentes do catálogo `rights=PUBLIC_REDISTRIBUTION_REVIEWED` e `original_file_unchanged=true` foram tratados como **declarações registradas no repositório, não como atestados independentes**. Fonte primária de licença favorável não é garantia da liberação de fotografias, datasets, elementos reproduzidos ou pessoas identificáveis.

## Registro por artigo: licença, edição, terceiros, atribuição e hash

### 16/20 — #45 Castellanos, Jiang, Gomes, Vander Meer & Castillo (2025)

**Caminho:** `knowledge/methodology/pdfs/castellanos-et-al-2025-llm-thematic-summarization.pdf`

**Atribuição completa:** Arturo Castellanos; Haoqiang Jiang; Paulo Gomes; Debra Vander Meer; Alfred Castillo. *Large Language Models for Thematic Summarization in Qualitative Health Care Research: Comparative Analysis of Model and Human Performance*. *JMIR AI* **4:e64447**, publicado em **04/04/2025**, DOI [10.2196/64447](https://doi.org/10.2196/64447). **Fonte e versão de registro:** [artigo JMIR AI](https://ai.jmir.org/2025/1/e64447/), [PDF editorial](https://ai.jmir.org/2025/1/e64447/PDF).

**Licença:** Nota de copyright específica no final do artigo do editor e na última página do PDF publicado: © cinco autores, Creative Commons Attribution [**CC BY 4.0**](https://creativecommons.org/licenses/by/4.0/). O editor exige **bibliografia completa, link ao trabalho publicado na JMIR AI e reprodução da nota de copyright/licença**; créditos são obrigatórios também no arquivo de atribuições da Skill. A página identifica um *preprint anterior* de 17/07/2024: **não confundir** com a versão definitiva de 2025.

**Terceiros/exceções:** Pesquisa analisa postagens textuais de fórum público para enfermeiros, coletadas ao longo de 28 períodos quinzenais (2020–2021), produz tabelas de temas e exemplos representativos de texto. Identificar por tabela/trecho se há reprodução literal de falas de terceiros ou nomes/dados pessoais; os termos do fórum não foram revisados como licença autônoma dos posts e o CC BY do artigo não implica permissão irrestrita para redistribuir corpus original. Tabelas 1–4 no PDF do editor; materiais e dados suplementares exigem escopo próprio. Nenhum indício de infração afirmado.

**Integridade:** **224375 bytes; SHA-256 recalculado MATCH** `afe781822e0637a1f1059ae2a8b538d2516ade299e0ee67c31ebeadd746562d0`; Git blob SHA-1 `67ef28f9ea9923ed0eaf53d714f239ab67ccbe35`, cabeçalho PDF OK. **Igualdade com o PDF editorial não comprovada.**

**Parecer:** `CONDITIONAL_JMIR_ATTRIBUTION_FORUM_TEXT_AND_EDITION`; **não incluir automaticamente**.

### 17/20 — #46 Messner, Smith & Richards (2025)

**Caminho:** `knowledge/methodology/pdfs/messner-smith-richards-2025-epistemological-incongruences.pdf`

**Atribuição:** Rudolf Messner; Samuel Smith; Carol Richards. *Artificial Intelligence and Qualitative Data Analysis: Epistemological Incongruences and the Future of the Human Experience*. *International Journal of Qualitative Methods*, **24 (2025)**, DOI [10.1177/16094069251371481](https://doi.org/10.1177/16094069251371481). Publicação online **26/08/2025**, edição jan.–dez. 2025.

**Licença:** [Página oficial SAGE](https://journals.sagepub.com/doi/full/10.1177/16094069251371481) declara copyright © autores 2025 e redistribuição sob **CC BY 4.0**, mediante crédito apropriado.

**Terceiros/exceções:** **Figura 1**: elaborada por autores, com fonte indicada como *Crotty (1998); Layder (1998, 2018)*; **Figura 2**: figura criada pelos autores. Conferir se a Fig.1 reproduz expressão gráfica externa ou apenas um modelo conceitualmente fundamentado, e preservar o crédito da legenda; referência acadêmica por si só não equivale a violação de copyright. A reprodução de dados primários externos não foi detectada no exame editorial dirigido, mas não há varredura de todo componente do PDF fornecido.

**Integridade:** **779818 bytes; SHA-256 recalculado MATCH** `af28adfce56d6ce33763a2538f5fd6e1e1d32fe4d39c10b8fe9d875fafdc20be`; Git blob SHA-1 `274762375d1c3b3810814867808766b765e08846`; `%PDF-` OK. **Cotejo binário com SAGE pendente**.

**Parecer:** `CONDITIONAL_FIGURE1_CREDITS_AND_EDITOR_EQUIVALENCE`; não incluir automaticamente.

### 18/20 — #47 Eschrich & Sterman (2024), arXiv v1 — preprint/workshop, não artigo de periódico

**Caminho:** `knowledge/methodology/pdfs/eschrich-sterman-2024-llm-qualitative-framework-arxiv-v1.pdf`

**Atribuição:** James Eschrich; Sarah Sterman. *A Framework For Discussing LLMs as Tools for Qualitative Analysis*. **arXiv:2407.11198v1**, submissão em **15/07/2024**, DOI do identificador arXiv [10.48550/arXiv.2407.11198](https://doi.org/10.48550/arXiv.2407.11198); apresentado como trabalho de **workshop CHI 2024**. [Página arXiv com histórico de versão e licença](https://arxiv.org/abs/2407.11198); [PDF v1](https://arxiv.org/pdf/2407.11198v1). **Não rotular como artigo certificado por revisão por pares ou proceedings do CHI 2025**.

**Licença:** a página de **v1** vincula expressamente à licença [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) e o PDF arXiv v1 também declara Creative Commons Attribution 4.0 International. Fonte aplicável à **versão v1**.

**Problema de edição/material:** o PDF do arXiv contém marcas não preenchidas do **template ACM** — referências como `Conference’17, July 2017`, `ACM ISBN 978-x-xxxx-xxxx-x/YY/MM` e instrução de classe LaTeX. Esse é um problema material de qualidade bibliográfica e identidade de edição, não prova de licença inválida. Na página PDF extraída, uma tabela intitulada *A Framework for Discussing LLMs for Qualitative Analysis* está associada ao conteúdo dos autores, com referência a conceitos teóricos de outros trabalhos, mas os créditos a cada possível componente devem ser checados. **A DOI arXiv não aparece na primeira página deste PDF** e não deve ser atribuída ficticiamente à capa. Evitar reproduzir marcadores ACM como dados de publicação reais.

**Integridade:** **112470 bytes; SHA-256 recalculado MATCH** `2c4e1e1e012a5fda2b8f153aff0f74b073b2c5e844483be9e74d20413d7b8850`; Git blob SHA-1 `ed9d620ed6035248799b64ac8d0500f0f61da7b6`; cabeçalho PDF OK. Cotejo da versão arXiv v1 baixada separadamente com GitHub ainda pendente.

**Parecer:** `CONDITIONAL_PREPRINT_TEMPLATE_AND_V1_BINARY_EQUIVALENCE`; manter indicação explícita de preprint/v1; não incluir automaticamente.

### 19/20 — #50 Atkinson (online 2023; periódico 2024)

**Caminho:** `knowledge/methodology/pdfs/atkinson-2023-mca-versus-catpca.pdf`

**Atribuição:** Will Atkinson. *Charting fields and spaces quantitatively: from multiple correspondence analysis to categorical principal components analysis*. *Quality & Quantity*, **58, 829–848 (2024)**, publicado online em **28/04/2023**, versão de registro na mesma data. DOI [10.1007/s11135-023-01669-w](https://doi.org/10.1007/s11135-023-01669-w). [Artigo Springer](https://link.springer.com/article/10.1007/s11135-023-01669-w); [PDF da editora](https://link.springer.com/content/pdf/10.1007/s11135-023-01669-w.pdf).

**Licença:** página Springer informa explicitamente **CC BY 4.0**, com dever de reconhecer autores, fonte, licença e modificações. Sua nota sobre terceiros esclarece que figuras e conteúdos externos participam da licença **salvo quando a legenda indicar exceção**; em caso de exceção, a permissão depende do titular. O texto padrão da página também menciona direitos reservados/licenciamento ao editor; não substituir a licença específica por essa declaração genérica, mas preservar para revisão caso surjam incongruências por versão.

**Terceiros/exceções:** artigo utiliza **dados European Social Survey (ESS 2016)** e repete/contrasta procedimento analítico de **Lindell & Ibrahim**; gráficos **Figuras 1 a pelo menos 6** e tabelas de MCA/CatPCA precisam ser atribuídos e checados quanto a fontes indicadas nas respectivas legendas. O processamento de dados de terceiros não é, por si, impedimento ao PDF publicado com CC BY; a eventual reutilização independente do dataset exige analisar sua licença/termos. **Não atestar ausência de exceções por falta de inspeção página a página**.

**Integridade:** **1.387.673 bytes**, SHA-256 **registrado no catálogo, NÃO recalculado pelo agente** `a31b1304cf1fa0e00182628553c415a169e2f48e16ee2df2edb86f7c519af101`; blob Git SHA-1 `a381ffe79ca0eb7890d748a2dcbbe0bec736a941`. A API de conteúdo **retornou zero bytes Base64** por limite de resposta. **Evidência de apoio independente de sessão:** [GitHub Actions Release audit #44985054731](https://github.com/rebsonm/MeuArtigoSkill/actions/runs/44985054731), `success` em commit congelado, etapa `Verify every catalogued public PDF against its SHA-256` `success`; **não substituir essa prova CI pela alegação de rehash nesta sessão**. Cotejo binário com Springer não realizado.

**Parecer:** `CONDITIONAL_ESS_FIGURES_AND_DIRECT_HASH_OR_PUBLISHER_COPY`; não incluir automaticamente.

### 20/20 — #51 Guedes-Neto (2026): survey experiments / Administração Pública

**Caminho:** `knowledge/methodology/pdfs/guedes-neto-2026-experimentos-survey-administracao.pdf`

**Atribuição:** João V. Guedes-Neto. *Experimentos de survey na administração pública brasileira: conceitos, métodos e exemplos*. *Revista de Administração Pública* (RAP/FGV), **60, e2025-0695 (2026)**, DOI [10.1590/0034-761220250695](https://doi.org/10.1590/0034-761220250695). [Página oficial do artigo](https://periodicos.fgv.br/rap/article/view/99745), [SciELO artigo HTML](https://new.scielo.br/j/rap/a/k4szTFchvXnvNGSQ4YJBnkv/?format=html&ilang=pt_BR&lang=pt), [PDF SciELO](https://new.scielo.br/j/rap/a/k4szTFchvXnvNGSQ4YJBnkv/?format=pdf&ilang=pt_BR&lang=pt). **Não confundir** o identificador editorial `e2025-0695` com ano real de publicação, 2026; [preprint SciELO](https://preprints.scielo.org/index.php/scielo/preprint/view/16950/version/17814) é outra edição.

**Licença:** [política de direitos autorais específica da RAP/FGV](https://periodicos.fgv.br/rap/copyright) e [página do artigo](https://periodicos.fgv.br/rap/article/view/99745) dizem que artigos da RAP são licenciados **CC BY 4.0**, com crédito da publicação original e link de licença. A natureza *não comercial da própria revista* na página institucional **não** é restrição `BY-NC` aos artigos; a mesma página autoriza expressamente até usos comerciais com atribuição. Essa distinção impede confundir a RAP com outra revista que use NC.

**Terceiros/exceções:** estudo apresenta exemplos experimentais e tabela de estimação de experimento de lista (tabela 1), utilizando fontes como **Guedes-Neto & Peters (2021, 2025)** e outros desenhos publicados. Validar nas legendas do PDF se são tabelas reconstruídas, adaptações ou reprodução de expressão alheia; **créditos aos estudos anteriores** e eventuais dados de respondentes devem ser preservados. O PDF de periódico não foi comparado byte a byte à cópia do GitHub.

**Integridade:** **371310 bytes; SHA-256 recalculado MATCH** `e0a3ae577c946ad4382f9e6cae1db24c2cf8bd5e8c402700e99dec1beb4535b8`; Git blob SHA-1 `0baf727256ec2138b108cd86ab91c65c684f127d`, cabeçalho PDF OK. **Equivalência binária com versão RAP/SciELO ainda não verificada**.

**Parecer:** `CONDITIONAL_PREVIOUS_EXPERIMENTS_CREDITS_AND_EDITION`; não incluir automaticamente.

## Quadro de fechamento e proveniência

| Índice | Documento e ano editorial | Licença efetiva indicada | Terceiros/edição: pendências principais | SHA-256 do GitHub nesta sessão | Status |
|---|---|---|---|---|---|
| #45 | Castellanos et al., JMIR AI 2025 | CC BY 4.0 (nota exigente de atribuição) | Conteúdo de fórum, tabelas/corpus, original de editor x preprint | **MATCH** | CONDICIONAL |
| #46 | Messner et al., IJQM 2025 | CC BY 4.0 (SAGE) | Figura 1 baseada em Crotty/Layder, cópia exata | **MATCH** | CONDICIONAL |
| #47 | Eschrich & Sterman, arXiv v1 2024 | CC BY 4.0 **na versão v1** | Template ACM com campos fictícios; classe de preprint; cópia original | **MATCH** | CONDICIONAL |
| #50 | Atkinson, Qual Quant online 2023 / ed. 2024 | CC BY 4.0 (Springer) | Figuras ESS/dados terceiros, crédito/editor x repositório | **SEM REHASH**; CI PASS | CONDICIONAL |
| #51 | Guedes-Neto, RAP 2026 | CC BY 4.0 (RAP, não NC) | Estudos/experimentos pré-existentes, tabela, cópia original | **MATCH** | CONDICIONAL |

**Fechamento quantitativo:** 20/20 PDFs CC BY 4.0 fora da allowlist **passaram por auditoria documental dirigida** entre os quatro relatórios, **zero PDFs adicionalmente liberados**, não significa 20/20 *juridicamente aptos*. O artigo Campos/Saidel 2022 (lote 02) continua **BLOQUEADO por conflito entre avisos de licença do mesmo periódico**, não pode ser revertido por inferência. Os dois registros `CC BY` sem versão (fora dos vinte) continuam sem decisão, não foram incorporados. Integridade do lote final: **4/5 recalculada e MATCH**, **1/5 verificada apenas por CI GitHub**. **Nenhuma comparação hash original de editora x hash da cópia GitHub**, ausência de varredura visual completa e nenhuma revisão jurídica/humana de direitos.

## Próximo ciclo — decisões necessárias, sem presunção

1. **Recomendado:** reconciliar o registro global de **20 auditorias, por item** com matrizes de pendências, prioridade e evidência faltante. Dar prioridade ao **bloqueio de licença da RPQ**; conferir licença e versão dos **dois `CC BY` genéricos** separadamente, sem os reclassificar. Comparar os bytes originais de editores com os PDF do GitHub quando permitido e revisar exclusões de figuras, datasets, tabelas e créditos. Recalcular diretamente SHA-256 das cópias >1MB por via que forneça os bytes, em vez de substituir evidência por CI.
2. Alternativa: testar tecnicamente apenas a Skill **TEST-ONLY atual com 29 PDFs**, mantendo direitos pendentes e sem publicar nova versão.
3. Alternativa: enfrentar primeiro o bloqueio da RPQ e a reconciliação das duas licenças genéricas, deixando a matriz 20/20 como pendência posterior.

**Não autorizado:** alteração automática de allowlist, arquivo PDF, catálogo, gates científicos, drive ACL, liberação de documentos do Drive privado, merge, tag, release, publicação da Skill ou reescrita de história Git. Issues [#102](https://github.com/rebsonm/MeuArtigoSkill/issues/102) e [#103](https://github.com/rebsonm/MeuArtigoSkill/issues/103) e atestação do host continuam temas separados. Este arquivo documenta evidência, não sign-off de liberação.
