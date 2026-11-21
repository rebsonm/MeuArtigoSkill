# V1-09/20 — RESULTADOS DA AUDITORIA EDITORIAL DE 17 CARDS

- Data: 2026-11-21 (America/Fortaleza); branch: `work/v1-09-20261121`.
- Manifesto congelado: `7c92045310eb3b1474a9612a777fb0012a511592`; snapshot dos cards: `c5e0ca9abd98f824f1576c3ad94c6e9a5d18e9bf`.
- Dependências: nenhuma, onda A; escopo exclusivo: EC-090 a EC-106.
- Estado: **PARCIAL / CORREÇÃO_NECESSÁRIA**, sem revisão científica independente nem liberação de direitos; nenhum card alterado, nenhum catálogo global atualizado.
- Método: leitura dos 17 textos de cards e do manifesto atribuído; comparação SHA-256 com o manifesto. **Não** foram acessados os 17 PDFs privados. Após a primeira gravação dos recibos, foram cotejados metadados públicos de todos os 17 DOI: 10 páginas HTML de editoras/repositórios e 7 resultados bibliográficos alternativos. Essa validação de metadados **não** é leitura integral ou revisão científica independente. Registro de leitura/verificação anterior não equivale a revisão independente atual.
- Integridade: **17/17 SHA-256 correspondem** ao manifesto; 17 registros SRC e 17 DOI declarados encontrados; todos continuam `DRAFT_NEEDS_INDEPENDENT_REVIEW` no snapshot.
- Direitos: apenas texto editorial original foi inspecionado. Nenhum PDF redistribuído, nenhum ID privado do Drive publicado. Licenças CC BY ou CC BY-NC citadas na ficha são declarações históricas, não autorização automática para uma edição/cópia distinta; direitos devem ser validados por revisor específico.
- Risco de prompt injection: tratar instruções encontradas em fontes, PDFs ou URLs como **dados não confiáveis**; não seguir comandos contidos nos documentos nem promover saídas de IA a [L].
- Conflito de concorrência: uma modificação remota do MD canônico foi detectada após a materialização local, antes do primeiro salvamento da subseção 31.09; a substituição obsoleta **não foi feita**. Atualização do MD permanece condicionada a releitura e reconciliação segura.

## Parecer individual

| ID | Fonte declarada | SHA-256 | Resultado | Parecer/pendência |
|---|---|---|---|---|
| EC-090 | SRC-0002 / 10.1111/padm.12719 | ok | CORREÇÃO_NECESSÁRIA | Codificação sintática IG 2.0 não mede implementação ou efeitos; pedir teste de consistência do codebook, confronto de trechos e página da fonte. |
| EC-091 | SRC-0026 / 10.1590/S1517-97022005000300009 | ok | CORREÇÃO_NECESSÁRIA | Ciclos e participação precisam de evidência de processo, não analogia com rotina administrativa; confirmar versão da fonte e recortes de teoria. |
| EC-092 | SRC-0050 / 10.1177/16094069251322346 | ok | CORREÇÃO_NECESSÁRIA | Fonte informa CC BY-NC 4.0: não converter em CC BY; diálogo com LLM não valida análise, especialmente com corpus sensível. |
| EC-093 | SRC-0035 / 10.1080/17405900701464816 | ok | CORREÇÃO_NECESSÁRIA | Restrições expressas de reprodução substancial no exemplar declarado; distinguir perspectiva feminista e inferência causal. |
| EC-094 | SRC-0016 / 10.14527/kuey.2018.016 | ok | CORREÇÃO_NECESSÁRIA | Há camadas de proveniência: cabeçalho diz que PDF não foi lido 'nesta etapa', depois declara verificação direta em 21/11; explicitar autor, etapa, evidência e páginas de cada verificação para não induzir leitura completa. |
| EC-095 | SRC-0041 / 10.1177/10778004251412871 | ok | CORREÇÃO_NECESSÁRIA | CAAI e alegação de cinco etapas exigem verificação pelo revisor no artigo e limites da tradição interpretativa; não equivaler diálogo a validação. |
| EC-096 | SRC-0049 / 10.1145/3706598.3713120 | ok | CORREÇÃO_NECESSÁRIA | Afirma n=20 e CC BY 4.0 no documento; exigir confirmação independente da amostra e licença do exemplar antes de atribuir generalização. |
| EC-097 | SRC-0054 / 10.1177/10497323241244669 | ok | CORREÇÃO_NECESSÁRIA | Distinguir publicação online 2024 da referência final 2025; cotejar comparação restrita a transcrição e não tratar concordância temática como validade. |
| EC-098 | SRC-0055 / 10.1177/10497323251401503 | ok | CORREÇÃO_NECESSÁRIA | ARC e suas cinco dimensões são descritos pelo card; confirmar nome, categorias e edição online 2025/volume 2026 antes de uso [L]. |
| EC-099 | SRC-0063 / 10.1177/10778004251401851 | ok | CORREÇÃO_NECESSÁRIA | 419 signatários/32 países é afirmação apresentada no card e requer conferência; manifesto argumentativo não é experimento; evitar prescrição universal. |
| EC-100 | SRC-0069 / 10.17169/fqs-26.1.4252 | ok | CORREÇÃO_NECESSÁRIA | Ensaios com GPT-3.5/4 não justificam extrapolação para outros modelos; observar CC BY 4.0 somente se edição/cópia confirmada. |
| EC-101 | SRC-0037 / 10.1177/14687941251390794 | ok | CORREÇÃO_NECESSÁRIA | Reflexividade tecnológica proposta como orientação [I], não validação empírica; confirmar obra e licença da cópia de origem. |
| EC-102 | SRC-0038 / 10.1177/16094069261426100 | ok | CORREÇÃO_NECESSÁRIA | Citações sobre 34 entrevistas clínicas e Gemma2/Llama3.1 dependem de cotejo; não expor corpus sensível e não equiparar maior número de códigos à acurácia. |
| EC-103 | SRC-0039 / 10.1177/10944281251377154 | ok | CORREÇÃO_NECESSÁRIA | Crítica epistemológica é argumento, não demonstração causal de impossibilidade de assistência computacional; preservar dissenso metodológico. |
| EC-104 | SRC-0042 / 10.3102/0013189X251314821 | ok | CORREÇÃO_NECESSÁRIA | Comparação GPT-3/humanos em contexto de equidade requer análise contextual; não inferir sensibilidade estrutural da semelhança das categorias. |
| EC-105 | SRC-0043 / 10.1177/10497323251365211 | ok | CORREÇÃO_NECESSÁRIA | Uso offline não prova confidencialidade ou equivalência epistemológica da RTA; verificação técnica e ética pendente. |
| EC-106 | SRC-0045 / 10.1177/16094069251383739 | ok | CORREÇÃO_NECESSÁRIA | Exploração de 323 resumos não valida entrevista, etnografia, causalidade nem autonomia inferencial; autoria das inferências humana. |

## Interpretação de [L]/[I]/[P] e parecer

- [L]: referências e descrições existentes **na fonte declarada**, não evidência científica independentemente homologada neste ticket.
- [I]: orientações metodológicas inferenciais próprias do card, sujeitas a validação contextual.
- [P]: perguntas/decisões propostas, não fatos empíricos nem comandos executáveis.
- Parecer provisório: os 17 cards possuem proveniência e cautelas editoriais; **nenhum atende ainda às duas revisões independentes de direitos/originalidade e fidelidade científica**. A classificação CORREÇÃO_NECESSÁRIA indica documentação/validação adicional antes de qualquer aceite, não que todas as proposições sejam falsas.
- Originalidade: redação breve e advertências presentes, mas originalidade não auditada contra texto integral das obras; nenhuma certificação de ausência de plágio.
- Contraprovas: procurar material divergente dentro de cada fonte e, nos cards LLM, testes de falha, vieses, codificação não concordante e limitações da tradição qualitativa. Não criar conclusões novas sem leitura da fonte.

## Testes e limites

- Conferência: todos os 17 caminhos exatamente atribuídos; 17/17 hashes SHA-256 compatíveis; 17/17 DOI e SRC declarados; sem arquivos de terceiros alterados.
- Não executado: comparação de hashes dos PDFs privados; revisão por segundo avaliador; validação de licenças por edição, detector de plágio, comparação contextual de páginas, CI de branch/host, integração V1-16.

## Próximos passos

1. Revisor humano 1: checagem independente de originalidade, citação, licença por exemplar e risco de reprodução.
2. Revisor humano 2: cotejo substantivo do artigo e página para cada claim, limites de inferência e [I]/[L]/[P].
3. Corrigir proveniência/camadas históricas especialmente em EC-094; manter cuidado quanto a diferença online 2024/2025 e volume.
4. Atualizar somente subseção 31.09 do MD canônico após releitura sem conflito; seguir para auditoria/integrador apenas quando pré-requisitos globais permitirem.

## Referência de artefatos

- `V1-09-DELTA.json`: um objeto auditável para cada card com fonte/DOI declarado, hash, direitos, decisão e bloqueios.
- Nenhum PDF protegido, hash de conteúdo privado ou identificador privado está presente nesses recibos.

## Complemento de verificação pública dos mesmos 17 documentos

Esta rodada confirmou metadados de identidade dos artigos atribuídos, sem consultar cards de outros lotes nem baixar PDFs. Páginas indisponíveis (403, timeout, DOI inacessível) foram substituídas somente por informações bibliográficas de fontes alternativas, sem simular acesso ao texto completo.

| Card | Forma de consulta pública | Evidência/limitação |
|---|---|---|
| EC-090 | HTML editora; [link](https://onlinelibrary.wiley.com/doi/abs/10.1111/padm.12719) | Frantz e Siddiki (2021) e IG 2.0 confirmados em página editorial |
| EC-091 | HTML publicação; [link](https://www.scielo.br/j/ep/a/3DkbXnqBQqyq5bV4TCL9NSH/?format=html) | Tripp (2005), texto HTML SciELO acessível |
| EC-092 | HTML editora; [link](https://journals.sagepub.com/doi/10.1177/16094069251322346) | Hayes (2025); direitos da página indicam CC BY-NC 4.0 |
| EC-093 | Metadados alternativos; [link](https://www.scienceopen.com/document?vid=c969f169-9c94-45c9-995a-c099c0241a90) | DOI/Lazar (2007) em fonte indexadora; editora retornou 403 |
| EC-094 | Metadados alternativos; [link](https://www.scilit.com/publications/5aba961cb4f78c5045da36f0711e70b8) | Cardno (2018) e DOI identificados em índice; ERIC retornou timeout |
| EC-095 | HTML editora; [link](https://journals.sagepub.com/doi/10.1177/10778004251412871) | Friese (2026), acesso restrito e pedido de permissão explícitos |
| EC-096 | Metadados alternativos; [link](https://dspace.mit.edu/entities/publication/0938ce9e-3d5c-4711-8a9f-2fc312b5536d) | Schroeder et al., CHI 2025 e estudo com 20 entrevistas; ACM retornou 403 |
| EC-097 | HTML repositório público; [link](https://pmc.ncbi.nlm.nih.gov/articles/PMC12202826/) | Wachinger: online 22/05/2024; volume 35(9) de 2025 |
| EC-098 | HTML editora; [link](https://journals.sagepub.com/doi/10.1177/10497323251401503) | Prahl: online 24/12/2025; fascículo 36(2–3) de 2026; solicitação de permissão |
| EC-099 | HTML editora; [link](https://journals.sagepub.com/doi/10.1177/10778004251401851) | Jowsey et al.: online 17/12/2025; issue 12/2026; 419 de 32 países; CC BY 4.0 |
| EC-100 | Metadados alternativos; [link](https://doaj.org/article/00be4819aded4a7ebc37e917a54a0b9f) | Mayring (2025), DOI e testes ChatGPT 3.5/4 confirmados por DOAJ; página FQS retornou timeout |
| EC-101 | HTML editora; [link](https://journals.sagepub.com/doi/10.1177/14687941251390794) | Ibrahim/Voyer: online 05/11/2025, volume 26(1) de 2026; CC BY 4.0 |
| EC-102 | Metadados de editora via pesquisa; [link](https://journals.sagepub.com/doi/full/10.1177/16094069261426100) | Misra et al. (2026), artigo e DOI confirmados no índice editorial; acesso direto DOI falhou |
| EC-103 | HTML editora; [link](https://journals.sagepub.com/doi/10.1177/10944281251377154) | Nguyen/Welch: online 30/09/2025, volume 29(1) de 2026; CC BY-NC 4.0 |
| EC-104 | Metadados de editora via pesquisa; [link](https://journals.sagepub.com/doi/abs/10.3102/0013189X251314821) | Jiang et al. (2025) e DOI confirmados; acesso DOI direto falhou |
| EC-105 | HTML editora; [link](https://journals.sagepub.com/doi/10.1177/10497323251365211) | Vikan et al.: online 08/09/2025, volume 36(2–3) de 2026; CC BY 4.0 |
| EC-106 | Metadados alternativos institucionais; [link](https://cidtff.web.ua.pt/blog/?p=78974) | Costa et al. e DOI AbductivAI em blog institucional; DOI direto falhou |

**Direitos conferidos diretamente em páginas editoriais:** EC-092 e EC-103 — **CC BY-NC 4.0**; EC-095 — acesso restrito e permissão; EC-098 — acesso gratuito, mas pedido de permissão; EC-099, EC-101, EC-105 — **CC BY 4.0**, condicionada à atribuição e versão. Para EC-100 a licença CC BY foi declarada historicamente e pode ser corroborada por índice público, mas a conferência de exemplar privado/versão continua pendente. Nenhum direito de redistribuição dos PDFs armazenados foi promovido.

**Datas editoriais a preservar:** EC-097 publicação online em 2024 e volume em 2025; EC-098 e EC-099 online em 2025 e fascículos 2026; EC-101, EC-103 e EC-105 igualmente online em 2025 e fascículos 2026. Não confundir ano de DOI com data da edição final.

## Revalidação de continuidade — auditoria estrutural nova (21/11/2026)

Este adendo **não refaz** os 17 pareceres nem a pesquisa de metadados públicos já concluídos. Foi feita nova leitura direta dos 17 caminhos na branch `work/v1-09-20261121` e comparação dos **17 Git blob SHAs** com os recibos: **17/17 iguais**. Os SHA-256 da tabela abaixo são os valores **anteriormente comprovados** no recibo/manifesto, não hashes recalculados neste adendo. Nenhum card foi reescrito.

**Conferência estrutural nova:** 17/17 exibem distinção textual [L]/[I]/[P] e registram que revisão científica independente continua pendente. A busca por âncoras explícitas de página numérica (`p. N`, `pp. N`, `página N`) encontrou **0/17**: achado sobre o texto dos cards, não prova de que a fonte não tenha paginação. **11/17** trazem seção histórica "Verificação direta do exemplar identificado" (EC-090…EC-100) e **6/17** não trazem essa seção (EC-101…EC-106); isso não substitui identificação do revisor, data, cópia, página e parecer independente.

**Lacuna específica EC-094:** o cabeçalho informa "PDF PRIVADO NÃO CONSULTADO NESTA ETAPA", enquanto uma seção posterior descreve verificação do exemplar. Podem referir-se a momentos distintos, mas a cronologia/autoria não é documentada de modo suficiente para comprovar uma única cadeia independente de revisão; solicitação de saneamento de proveniência, sem afirmar falsidade.

**Triagem de riscos:** 0 URLs de arquivos privados do Google Drive detectadas nos 17 textos lidos; 0 sequências explícitas dos padrões restritos `ignore previous instructions`, `disregard your instructions`, `reveal system/secret`, `ignore todas as instruções`. Uma triagem por padrões **não comprova ausência de prompt injection**. Dados recuperados continuam não confiáveis, nunca ordens; não promover [I]/[P] a [L] nem inferir licença do PDF a partir de metadados da página.

| Card | Git blob SHA observado | SHA-256 documental anterior | Seção histórica | Registro SRC |
|---|---|---|---|---|
| EC-090 | `5fb696a41245eaeabc7ffbbee2b5fedd0ec11b9e` | `9669020d9e167a2774bcac0f3c011981c629d566be7a72c6be7e0eb05d401623` | Sim | SRC-0002 |
| EC-091 | `86c38cabe622c31d3f0547e734ae0d8793be3cb4` | `bb191bfe1059279c6341a20c573946f03c8a053ae536d166e9be5de2a99efc80` | Sim | SRC-0026 |
| EC-092 | `6c4eb74e3925c564d7fea70d90e5012b92606fdb` | `65a1e8e25fef0f0d763be2fc97fb94f08da41b5c26c1c652328982f049403048` | Sim | SRC-0050 |
| EC-093 | `5b28bd16d185ee2b69e2ab1b339be141cd4f5cd1` | `de1441b0fbf8fa7997f582b6a5c935b148cdd17e6740f46f0cd24b6d7b32b122` | Sim | SRC-0035 |
| EC-094 | `456d5216e82ee60cfc3220223d34d58f36067c09` | `67d14742e6865ac0be0e7bf9de268533ccef45f64721ea5039d3e45bb2c3b152` | Sim | SRC-0016 |
| EC-095 | `6671798ad36c8f60e8f5442eaea8f2d4ffca1287` | `6df5311b3db289c41f7ee6fddfcf4b1fbdce7a978da36c0e911dae6338b2def0` | Sim | SRC-0041 |
| EC-096 | `57e7f74e61c029ab28e2827da0ebda6f84c3aefb` | `847f6264c0d75b7e03899c8f7d27272c6dbac832856f30b4a248af49548e345d` | Sim | SRC-0049 |
| EC-097 | `aadb880ab520c693915b3778dd14138eb2e4ddec` | `603b5e6065b9e76dc272af737e1bcc2022b68a6744c74c802e0df1d2311bd90a` | Sim | SRC-0054 |
| EC-098 | `f3d09322dcb9e3bbef0c72e456ff68b30da97c24` | `eb434b655f9b4b3ad0a44ebf2f4d6a101c4add0ec65d90df905c137f7cc65da4` | Sim | SRC-0055 |
| EC-099 | `31c488b2a13d521774a7badfb91caa8c1fd4e12a` | `699b23bae748da48eed369c0c8df7b169f2b9ac855b40cd1e50ccf46e3889092` | Sim | SRC-0063 |
| EC-100 | `5cf14235a68052dc51ba13b373bed6e829ffbd83` | `9d3f763f20b601420f575c8021ea6ac7c665de3321ba298fe6e28e0e309a6854` | Sim | SRC-0069 |
| EC-101 | `5871e4fb76d51680b539968c646c0317e6e515db` | `eba4afdcb42beb58fe8b0949a509d4d4955406f92177376692aefda184483291` | Não | SRC-0037 |
| EC-102 | `aef588d66cc5da2343a923064834d922026cb46d` | `794178b00be3844852e2136c2b2785e7b3a13bdd60cfd3f0b69f76075e4e519f` | Não | SRC-0038 |
| EC-103 | `44dda34ec3a43a4093d818bd053eefc3c38b0e71` | `23425b7cc3d014b6e07cc75c2716160483f79ec89bf8cdaa068fe446d70cdd81` | Não | SRC-0039 |
| EC-104 | `67cbf7f851cb0c2a1f2b970984b75d7a88f8646f` | `36c2d5d52b50d9394fa97fdff06cc458befcf853ea11fce107981ade0d31a471` | Não | SRC-0042 |
| EC-105 | `fd8f88f4d2a2ce49c26cf0150a6002aeacb6e3f2` | `dedf8976bc59a4b9c9c074db9fd4fb4ce103f44e15cf5b70aa8437b0adaac1ca` | Não | SRC-0043 |
| EC-106 | `b88a50bd5611da4549d810db34faa12b64dceb3c` | `376785000ca038fb1527df2ff1ad832ef41ee48a235a80b6a38fb73a5fef5ba3` | Não | SRC-0045 |

**Controle de execução pré-adendo:** comparação da branch com `7c92045310eb3b1474a9612a777fb0012a511592`: 6 commits à frente, 0 atrás, somente dois caminhos exclusivos; PR da V1-09 não localizada, statuses=[] e workflow_runs=[] no HEAD `0a0ef10ddf7d104a6f97b73e5a08cd1a81846c87`. Não confundir ausência de resultado com sucesso de CI.

**Canônico Drive:** a seção 31.09 do corpo ainda contém o planejamento inicial. Sem revisão atômica ou janela exclusiva, **não sobrescrever** o Markdown bruto; um comentário ancorado na 31.09 foi criado para FEITO/EM EXECUÇÃO/PRÓXIMA AÇÃO. Nenhum byte do corpo do MD foi alterado por esta etapa.

**Decisão editorial:** preservar `CORREÇÃO_NECESSÁRIA` para 17/17 e `PARCIAL` como estado da etapa. Faltam cotejo de trecho/página/edição/cópia, direitos por exemplar, revisão científica independente, avaliação independente de originalidade/direitos e conclusão segura do acompanhamento no MD. Sem merge, tag, release, MCP, PDF protegido ou aprovação de gate.

## Substituição proposta exclusivamente para a subseção 31.09 do MD canônico — NÃO APLICADA

A seguir consta a substituição exata para integração controlada. Ela não foi gravada no Drive, pois o arquivo Markdown mudou durante a preparação e o endpoint de edição por trechos retornou `FAILED_PRECONDITION`; a API de substituição bruta não oferece trava otimista de versão. Em caso de janela de edição exclusiva, reler o MD integral mais recente, substituir somente o trecho entre 31.09 e 31.10 e conferir os demais blocos após a escrita.

### 31.09 — V1-09/20 — Curadoria editorial de cards 090–106

- **Estado:** `PARCIAL` — a revisão documental e os recibos próprios foram entregues à auditoria no GitHub; gravação no MD canônico não realizada por conflito concorrente e falta de edição transacional de Markdown.
- **Onda e dependências:** A; nenhuma. Escopo exclusivo: 17 cards EC-090…EC-106, conforme manifesto `7c92045310eb3b1474a9612a777fb0012a511592`.
- **Branch exclusiva:** `work/v1-09-20261121`, derivada do commit-base; nenhum merge em `main`, tag, release, force-push ou implementação MCP.
- **Início:** 21/11/2026, os 17 cards do snapshot `c5e0ca9abd98f824f1576c3ad94c6e9a5d18e9bf` foram lidos. 17/17 SHA-256 dos conteúdos corresponderam ao manifesto. Tentativa de registro inicial foi abortada quando o MD mudou em outra aba antes da gravação.
- **Evolução:** metadados dos 17 trabalhos corroborados (10 páginas HTML acessíveis de editoras/repositórios e 7 verificações bibliográficas alternativas). Dois recibos exclusivos produzidos; 17 pareceres `CORREÇÃO_NECESSÁRIA`, sem alteração de cards globais ou de outras etapas. A API Docs recusou edição por trecho por se tratar de Markdown; operação não aplicada.
- **Direitos:** EC-092 e EC-103 com CC BY-NC 4.0; EC-095 com acesso restrito; EC-098 com aviso de solicitação de permissão; EC-099, EC-101 e EC-105 com CC BY 4.0 nas páginas editoriais, sempre condicionadas a versão e atribuição. Nenhum PDF privado redistribuído, nenhum ID privado do Drive exposto.
- **Decisão científica:** revisão científica independente e checagem independente de direitos/originalidade seguem pendentes; não promover [P]/[I] a [L] nem interpretar hash como aprovação.
- **Commits confirmados:** `a514976fb48bd1561ced4eace33385796ff99588` (RESULTS inicial), `d936263030a794eb8a3ba64db759386ba64323b3` (DELTA inicial), `a5e4488605b073920c2dc21033b967c223784a69` e `5850041847fe499008c6f6ddfeac19b6d16aa2cd` (verificação bibliográfica/direitos).
- **Testes:** 17 caminhos e hashes conferidos, 17 IDs únicos, comparação do GitHub limitada aos 2 arquivos do próprio lote; nenhum status CI publicado (não declarar CI aprovado).
- **Bloqueios:** falta de revisão humana independente por obra/página, licença do exemplar privado, conflito de concorrência do Markdown e ausência de API com compare-and-swap para edição de subseção `31.09`.
- **Próximos passos:** só reconciliar este bloco do MD em janela exclusiva e conferir preservação das outras seções; após isso, encaminhar revisão científica/direitos. Etapas V1-16…V1-20 somente após pré-requisitos globais, sem GO antecipado.

