# Meu Artigo — saneamento autoral aprofundado: PDF-35, PDF-48 e PDF-49

**Data:** 22/11/2026 (America/Fortaleza). **PR #112** Draft. **Escopo:** investigar edições específicas, licenças editoriais e exceções de terceiros; **não alterar** catálogo, allowlist, PDFs, código, sete gates, ACL, histórico Git, merge ou release. **Status global:** `NO_GO`, sem licença/sublicença humana presumida. [Delta auditável JSON](./PDF-35-48-49-EDITORIAL-RIGHTS-DEEP-REVIEW-2026-11-22.json).

## Decisões técnicas e autorais — separadas

| PDF | Prova da licença da edição | Componentes protegidos/edição | SHA-256 no GitHub (recalculado agora) | Disposição para distribuição |
|---|---|---|---|---|
| **35 — Campos/Saidel** | Aviso específico CC BY 4.0, mas a frase genérica da revista declara não comercial; contradição persiste | Quadro 1 creditado aos autores; nenhuma evidência positiva de figura externa; varredura integral de exceções pendente | **MATCH**, 223.205 bytes | **BLOCKED** aguardando esclarecimento escrito |
| **48 — Silva/Barbosa/Lima** | CC BY e permissões comerciais expressas; **sem versão CC numérica** na página da edição | Figuras 1–5 dos autores, Quadro 1 e duas pesquisas anteriores; confirmar proveniência/consentimento | **MATCH**, 631.240 bytes | **CONDITIONAL** sem versão da licença |
| **49 — Figueiredo Filho et al.** | **CC BY 4.0 confirmado na própria página do artigo de 2019**: link de licença remete à URI /by/4.0/ | Figuras 1, 2, 4 e 5 com fontes externas nomeadas; Figura 3 dados externos; Tabela 2 adapta guideline TOP; errata Review Essay | **MATCH**, 693.693 bytes | **CONDITIONAL** por terceiros/cópia exata, embora a versão CC do artigo HTML esteja demonstrada |

Os três SHA-256 foram **calculados diretamente sobre bytes Base64 de PDFs do GitHub** no commit de entrada `99e232ca4c61430e915160f3c22e55e58c19539d` (implementação SHA-256 testada com vetor `abc`), com tamanho e cabeçalho `%PDF-` coincidentes com o catálogo. **Isto não é SHA do PDF da editora**. Tentativas de baixar a cópia editorial via runtime falharam por DNS; inspeção documental por web foi efetuada para as edições. Portanto, `publisher_vs_git_binary_equal=NOT_VERIFIED` para 3/3. O PDF BPSR foi inspecionado como texto editorial (37 páginas); a captura visual adicional falhou por cache, não se declara inventário visual completo. Outras capturas confirmaram a primeira página RPQ e UFF.

## PDF-35 — Revista Pesquisa Qualitativa, 2022

- **Referência:** Claudinei José Gomes Campos e Maria Giovana Borges Saidel, *Amostragem em investigações qualitativas: conceitos e aplicações ao campo da saúde*, RPQ **10(25), 404–424 (2022)**, DOI [`10.33361/RPQ.2022.v.10.n.25.545`](https://doi.org/10.33361/RPQ.2022.v.10.n.25.545). [Página oficial](https://editora.sepq.org.br/rpq/article/view/545); [PDF 21 páginas](https://editora.sepq.org.br/rpq/article/download/545/337).
- **Evidência de licença:** a página individual informa **Creative Commons Attribution 4.0 International**; já uma frase genérica diz que a revista é “4.0, não-comercial”. O **mesmo par de avisos conflitantes**, incluindo a mesma frase genérica, está presente em [página de 2021](https://editora.sepq.org.br/rpq/article/view/484) e em [página de 2026](https://editora.sepq.org.br/rpq/article/view/1787). Isto torna plausível uma inconsistência duradoura de template, **sem provar** qual aviso prevalece juridicamente para esta obra. O texto pesquisável do PDF do artigo não apresenta aviso de licença que resolva a contradição.
- **Terceiros:** no PDF, o **Quadro 1** resume técnicas de amostragem e tem fonte expressa **“Elaborado pelos autores (2022)”** (página impressa 417). A ausência de figura externa destacada no exame dirigido não é certificação integral de todos os elementos, imagens, dados e permissões.
- **Hash e identidade de arquivo:** `b3e78db1e163a787ec0ac08c44fca1cbb2c664f53564581128779c65a8ddd1a8` / 223205 B, Git blob SHA-1 `3507ba7c143cd295e752bca55feeb061255dce00`, MATCH apenas ao catálogo.
- **Decisão:** `BLOCKED_LICENSE_CONFLICT_PENDING_PUBLISHER_CLARIFICATION`. Solicitar resposta da RPQ com **URI da licença aplicável ao artigo e ao PDF de 2022**, se permite usos comerciais, eventuais exceções por componentes e sentido do texto genérico. Sem enviar nem presumir resposta. Papel proposto: editor-chefe RPQ (página de contato identifica **Tiago Emanuel Klüber**), curadoria de direitos, mantenedor. [Contato editorial oficial](https://editora.sepq.org.br/rpq/about/contact).

## PDF-48 — Revista Pensamento Contemporâneo em Administração/UFF, 2020

- **Referência:** Manuela Ramos da Silva; Marcos Antônio de Souza Barbosa; Lucas Gabriel Bezerra Lima. *Usos e possibilidades metodológicas para os estudos qualitativos em Administração: explorando a análise temática*. RPCA **14(1), 2020**. DOI [`10.12712/rpca.v14i1.38405`](https://doi.org/10.12712/rpca.v14i1.38405). [Página oficial (publicada 31/03/2020)](https://periodicos.uff.br/pca/article/view/38405), [PDF da edição](https://periodicos.uff.br/pca/article/download/38405/pdf/138387).
- **Evidência de licença:** o artigo e as [condições de submissão da própria revista](https://periodicos.uff.br/pca/about/submissions) declaram **CC BY**, com permissão de distribuição, remix, adaptações e uso **comercial** mediante crédito. A página visível não fornece hiperlink/URI específico identificando a **versão numérica**, e a extração do PDF da edição não mostra aviso CC. Não inferir CC BY 4.0 só por se tratar da licença CC BY em 2020.
- **Componentes e proveniência:** o PDF contém **Figuras 1–5** creditadas, no texto acessível, como **“Elaborado pelos autores (2020)”**, além de **Quadro 1** e exemplos das **Pesquisas A e B**, envolvendo entrevistas e materiais de estudos anteriores (inclusive menção a Silva 2017). É necessário identificar se os gráficos são criações originais, adaptações ou reproduções, e se há restrições de citação/proteção de falas, imagens ou dados de participantes. Fontes acadêmicas citadas como ideias não significam reutilização não autorizada de arte.
- **Hash:** `ba56e9b7fff572af066706ddbe0d886f36eff0ecf8916227c1ff0ec7798a5870` / 631240 B, Git blob `83a1140fa939436a187f4773e60c116efed4caa9`, MATCH ao catálogo.
- **Decisão:** `CONDITIONAL_VERSION_UNSPECIFIED_AND_COMPONENTS`. Solicitar ao corpo editorial **URI/versão da licença vigente para o PDF de 2020**, confirmação de alcance à cópia publicada e eventuais ressalvas. A [página de contato do RPCA/UFF](https://periodicos.uff.br/pca/about/contact) mostrou mensagem de manutenção nesta consulta; **não utilizar o endereço técnico do portal como se fosse o editor da revista**.

## PDF-49 — Brazilian Political Science Review, 2019

- **Referência:** Dalson Figueiredo Filho; Rodrigo Lins; Amanda Domingos; Nicole Janz; Lucas Silva. *Seven Reasons Why: A User’s Guide to Transparency and Reproducibility*. BPSR **13(2), e0001 (2019)**, DOI [`10.1590/1981-3821201900020001`](https://doi.org/10.1590/1981-3821201900020001). [Artigo SciELO em HTML](https://www.scielo.br/j/bpsr/a/sytyL4L63976XCHfK3d7Qjh/?format=html&ilang=en&lang=en); [PDF SciELO](https://www.scielo.br/j/bpsr/a/sytyL4L63976XCHfK3d7Qjh/?format=pdf&lang=en).
- **Prova substancialmente NOVA e mais forte:** o aviso de licença do **próprio artigo de 2019** é hiperlink no rodapé do HTML (link `205`), e o destino foi seguido: **`https://creativecommons.org/licenses/by/4.0/`**. Portanto **CC BY 4.0 do artigo HTML de 2019 está diretamente documentada**, não apenas deduzida da [política atual de 2026](https://new.scielo.br/journal/bpsr/about/). A política atual é evidência corroborativa. **Não atualizar metadados no GitHub automaticamente**: o arquivo específico e terceiros continuam não reconciliados.
- **Correção bibliográfica:** a própria página contém **ERRATUM** que substitui classificação **“Article” por “Review Essay”**; manter a nomenclatura corrigida em créditos/descritivos, sem confundir categoria com copyright.
- **Terceiros, PRIORIDADE:** a página original fornece lista de Figuras **1–5** e tabelas **1–4**. Fig. 1 cita blog externo *shadowtolight*; Fig. 2 cita **Imai et al. (2016)**; Fig. 3 é figura elaborada pelos autores com dados de fonte externa de biologia; Fig. 4 cita **TIER (2017)**; Fig. 5 cita **r4stats.com/articles/popularity**. Tabela 2 resume padrões **TOP/Nosek et al. (2015)**; Tabela 3 compila dados da BITSS. **A licença CC BY do artigo não atesta, por si, autorização autônoma para relicenciar imagens externas.** É preciso verificar se são figuras reproduzidas, adaptadas, autorizadas/licenciadas independentemente ou abrangidas pela publicação; o simples crédito não comprova permissão nem violação.
- **Hash:** `c2dc25fc39a0782be735e723e5613eacf90562aadb4cfe00e51442cce056a7e8` / 693693 B, Git blob `4e7d3eeb61dbb45b10f67c48add78d1187d5e6c3`, MATCH ao catálogo.
- **Decisão:** `ARTICLE_CC_BY_4_0_LICENSE_CONFIRMED_HTML; THIRD_PARTY_RIGHTS_AND_EXACT_PDF_BLOCKED`. **Não é mais necessário pedir à BPSR a geração da licença do artigo HTML**, pois o hiperlink original confirma 4.0; uma consulta editorial **é opcional e dirigida à abrangência de figuras 1/2/4/5, PDF exato e exceções**. [Contato BPSR](https://brazilianpoliticalsciencereview.org/about-the-journal/) (página oficial informa `bpsr@brazilianpoliticalsciencereview.org`); nenhuma mensagem foi enviada.

## Solicitações editoriais preparadas — rascunhos NÃO ENVIADOS

### RPQ — consulta necessária (P0)

**Assunto:** Esclarecimento da licença do artigo 10.33361/RPQ.2022.v.10.n.25.545 (edição PDF de 2022)

Prezada equipe editorial da Revista Pesquisa Qualitativa,

Estou realizando uma conferência documental de direitos de reutilização de artigos científicos em um recurso de apoio à pesquisa. Sobre o artigo de Campos e Saidel (2022), DOI 10.33361/RPQ.2022.v.10.n.25.545, verifiquei que sua página específica identifica Creative Commons Attribution 4.0 International, enquanto aviso geral do periódico menciona Creative Commons 4.0 “não-comercial”.

Poderiam confirmar, por gentileza: (1) qual licença, com URL exata, governa o texto e o PDF publicado no volume 10, número 25, páginas 404–424; (2) se o artigo pode ser redistribuído com atribuição também em contextos comerciais; (3) se existem exceções para o Quadro 1 ou outros materiais de terceiros; e (4) se há algum requisito adicional de crédito ou identificação da versão?

Esta solicitação não pressupõe autorização nem a redistribuição do arquivo. Agradeço a orientação oficial, idealmente por escrito e vinculada ao DOI acima.

Atenciosamente,

[Responsável pelo projeto Meu Artigo]

### RPCA/UFF — consulta necessária para versão da CC BY (P1)

**Assunto:** Confirmação da versão Creative Commons — artigo RPCA 14(1), DOI 10.12712/rpca.v14i1.38405

Prezada equipe editorial da Revista Pensamento Contemporâneo em Administração,

Para uma auditoria documental de reutilização, consultamos o artigo de Silva, Barbosa e Lima (2020), DOI 10.12712/rpca.v14i1.38405. A página oficial declara CC BY e admite uso comercial mediante atribuição, mas não conseguimos localizar o número da versão/URI aplicável ao PDF de 2020.

Solicitamos informar: (1) a URL da licença Creative Commons vigente para essa obra e edição específica; (2) se a licença alcança a versão PDF disponibilizada pelo periódico; (3) se figuras, quadros e exemplos das pesquisas A/B têm alguma exceção ou crédito adicional; e (4) a forma correta de atribuição para redistribuição integral sem modificações.

Não houve redistribuição em razão desta consulta. Agradecemos uma resposta formal que permita atualizar a documentação de direitos com segurança.

Atenciosamente,

[Responsável pelo projeto Meu Artigo]

### BPSR — consulta complementar OPCIONAL, restrita a figuras (P1)

**Subject:** Third-party figure permissions and PDF edition — DOI 10.1590/1981-3821201900020001

Dear Brazilian Political Science Review editorial team,

We are auditing the reuse conditions of *Seven Reasons Why: A User’s Guide to Transparency and Reproducibility* (2019), DOI 10.1590/1981-3821201900020001. We verified that the copyright/license link on the SciELO article page points to CC BY 4.0.

Could you please clarify whether Figures 1, 2, 4 and 5, which credit external sources, are included in the article-level CC BY 4.0 license or require separate permission from the respective rightsholders? Please also confirm whether the linked PDF of the original 2019 Review Essay, as corrected by its erratum, is the version covered and whether any additional attribution statements apply.

We have not assumed any permissions for third-party figures or redistributed the file based on this inquiry.

Kind regards,

[Meu Artigo project representative]

## Rastreabilidade e limites

**FEITO:** páginas editoriais exatas examinadas, links de licença e errata consultados, componentes identificados e **SHA-256 recalculado 3/3** sobre os arquivos do GitHub. **NÃO FEITO:** prova de correspondência bit a bit com PDF da editora, inspeção exaustiva de todas as figuras pelos arquivos binários das editoras, resposta do editor, envio de e-mail, decisão jurídica ou clearance do titular.

**PRÓXIMA AÇÃO RECOMENDADA:** manter bloqueio RPQ e receber esclarecimento editorial específico, confirmar versão UFF, aprofundar exceções das Figuras 1/2/4/5 da BPSR. Solicitações acima estão somente preparadas em texto; qualquer envio requer autorização explícita. Prioridades de release também incluem issues #102/#103 e leitura real da Skill no host (T02 NOT_RUN). Sete gates continuam `PENDING`. **Nenhuma licença em `pdf_catalog.json`, nenhum PDF, allowlist, política YAML/SVG, PR status ou Git history foi modificado.**
