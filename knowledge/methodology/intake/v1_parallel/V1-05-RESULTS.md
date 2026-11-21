# V1-05/20 — auditoria editorial dos cards EC-019…EC-036

Data: 2026-11-21 (America/Fortaleza)
Branch exclusiva: `work/v1-05-20261121`.
Manifesto imutável: `7c92045310eb3b1474a9612a777fb0012a511592` em `knowledge/methodology/intake/v1_parallel/V1-WORKPACKAGES-MANIFEST.json`.
Corpus de leitura: `c5e0ca9abd98f824f1576c3ad94c6e9a5d18e9bf`.
**Estado da entrega:** ENTREGUE_PARA_AUDITORIA (documental); **não** AUDITADO, INTEGRADO, homologado nem autorizado a publicação.
**Estado científico:** 18 cards permanecem [I], DRAFT_NEEDS_INDEPENDENT_REVIEW; nenhuma promoção a [L].

## Decisão expressa do mantenedor — 21/11/2026
- **Aprovação declarada pelo mantenedor nesta conversa:** “Aprovado os cards.” Escopo: 18 cards EC-019…EC-036 da etapa V1-05; decisão registrada como `APROVADO_PELO_MANTENEDOR`, sem presumir que as duas revisões independentes exigidas por `CARD-POLICY.md` ocorreram.
- **Consequência imediata:** autorização de continuidade editorial dos 18 cards, conservando classificação `[I]`, triagem documental e a PR #104 em Draft. Este registro **não** converte 0/18 revisões independentes comprovadas em 18/18, **não** concede licença sobre obras de terceiros, **não** promove `[I]` a `[L]` e **não** autoriza merge, publicação, release ou alteração dos arquivos de card.
- **Em execução / próximo passo:** verificar originais e licenças dos oito cards prioritários (EC-021, 024, 028, 030, 032, 033, 034 e 036); documentar riscos por edição; obter as duas checagens independentes para promoção a `ACCEPTED` e conciliar com segurança a subseção 31.05 do Markdown canônico.

## O que foi concluído
- Checados 18/18 caminhos exatos do manifesto, todos únicos, sem inspecionar/editar cards de lotes alheios.
- SHA-256 computado sobre bytes UTF-8 dos 18 cards retornados pelo GitHub no snapshot e confrontado com `catalog_blob_sha256` do manifesto: **18/18 MATCH**, 0 divergências.
- Os 18 cards apresentam orientação metodológica, limites/contraprovas, bibliografia e links. Todos permanecem explicitamente [I]/rascunho; **0/18 apresentam comprovação de duas revisões humanas independentes**.
- 13/18 contêm autodeclaração de consulta a PDF apenas para identificação/abstract/escopo; a presente etapa **não teve acesso nem refez esse cotejo**. Outros 5 são sínteses editoriais com leads bibliográficos. 14/18 possuem DOI textual e 4 não confirmam DOI para a edição.
- Triagem textual limitada não identificou padrões óbvios de prompt injection, mas isso não prova ausência de risco. Nenhum PDF de terceiro foi anexado, extraído, modificado ou publicado.
- Permanece pendente conferir direitos por edição/cópia, especialmente licenças NC/ND, artigos protegidos, working papers e capítulo com link ResearchGate. Não inferir autorização pelo link.
- GitHub: PR #101 continua Draft; Issues #102 e #103 permanecem abertas. V1-16 não liberada.

## Pareceres por card
Critério transversal: **CORREÇÃO NECESSÁRIA** = falta de avaliação independente de direitos/originalidade e fidelidade científica; não significa que o texto esteja comprovadamente incorreto.

| ID | Arquivo atribuído | Verificação e pendência individual | Encaminhamento |
|---|---|---|---|
| EC-019 | `sampling-saturation-compatibility.md` | Confirmar fidelidade aos diferentes critérios de adequação/saturação; distinguir análise temática reflexiva, contagem de códigos e grounded theory. Sem leitura independente das fontes primárias. | CORREÇÃO NECESSÁRIA |
| EC-020 | `literature-review-writing-practice.md` | Confrontar Pautasso (2013) com limites da revisão narrativa; não inferir cobertura sistemática a partir de orientações de redação. | CORREÇÃO NECESSÁRIA |
| EC-021 | `manuscript-argument-structure.md` | Conferir aviso de correção editorial associado ao artigo de Mensh e Kording e a edição efetivamente usada antes da aceitação. | CORREÇÃO NECESSÁRIA |
| EC-022 | `reproducible-computational-workflow.md` | Verificar o artigo de Sandve et al. quanto à reprodutibilidade computacional; não confundir rerun técnico com validação científica. | CORREÇÃO NECESSÁRIA |
| EC-023 | `meta-analysis-design-and-reporting.md` | Validar conceitos de estimando, comparabilidade e heterogeneidade contra a edição primária; não propor pooling sem estudos e protocolo. | CORREÇÃO NECESSÁRIA |
| EC-024 | `sa-silva-2009-documentary-research.md` | DOI pendente; Conferir edição, identidade bibliográfica e eventuais direitos da fonte Sá-Silva et al.; DOI não confirmado nesta edição. Consulta ao PDF é apenas autodeclarada no card. | CORREÇÃO NECESSÁRIA |
| EC-025 | `morgan-2022-qualitative-document-analysis.md` | Conferir edição/paginação e fidelidade ao artigo de Morgan; consulta ao PDF é autodeclarada, sem cotejo de cada afirmação. | CORREÇÃO NECESSÁRIA |
| EC-026 | `byrne-2022-reflexive-thematic-worked-example.md` | Conferir aderência a Byrne e pressupostos da análise temática reflexiva; não converter reflexividade em teste de concordância. | CORREÇÃO NECESSÁRIA |
| EC-027 | `kiger-varpio-2020-thematic-analysis.md` | Confirmar tipologia e edição do AMEE Guide de Kiger e Varpio; registrar diferenças entre abordagens de análise temática. | CORREÇÃO NECESSÁRIA |
| EC-028 | `nowell-2017-trustworthy-analysis.md` | direitos explícitos; Verificar a licença exata CC BY-NC indicada para Nowell et al., sem promover PDF para catálogo irrestrito; revisar critérios de rigor sem reduzir qualidade a checklist. | CORREÇÃO NECESSÁRIA |
| EC-029 | `rijnsoever-2017-saturation-simulation.md` | Confrontar condições da simulação de van Rijnsoever; rejeitar extrapolação para quota universal de entrevistas. | CORREÇÃO NECESSÁRIA |
| EC-030 | `hennink-kaiser-2022-saturation-review.md` | direitos explícitos; Verificar a licença CC BY-NC-ND indicada no card de Hennink e Kaiser; não redistribuir derivativos/PDF em regime irrestrito. Distinguir saturação de códigos e de significados. | CORREÇÃO NECESSÁRIA |
| EC-031 | `roth-etal-2023-did-identification.md` | Conferir texto e edição de Roth et al. para pressupostos de tendências paralelas, tratamentos escalonados e efeitos heterogêneos. | CORREÇÃO NECESSÁRIA |
| EC-032 | `cattaneo-titiunik-2022-rdd.md` | direitos explícitos; A publicação Cattaneo/Titiunik é descrita como protegida; revisar metadados/licença da edição e não reproduzir tabelas/figuras. | CORREÇÃO NECESSÁRIA |
| EC-033 | `imbens-lemieux-2007-rdd-practice.md` | DOI pendente; direitos explícitos; O working paper NBER indica reserva de direitos; conferir edição e DOI (não confirmado no card), vedada redistribuição do PDF por mera acessibilidade. | CORREÇÃO NECESSÁRIA |
| EC-034 | `bennett-fairfield-soifer-2019-process-tracing.md` | DOI pendente; direitos explícitos; Confirmar autoria/edição do relatório SSRN do grupo QTD e condições de reutilização; DOI não confirmado e PDF não liberado. | CORREÇÃO NECESSÁRIA |
| EC-035 | `thiem-2017-qca.md` | Validar distinções necessidade/suficiência, calibração e contraexemplos contra Thiem (2017) e sua edição. | CORREÇÃO NECESSÁRIA |
| EC-036 | `couto-albala-2022-public-policy-qca.md` | DOI pendente; direitos explícitos; Confirmar identificação e edição do capítulo Couto/Albala; ResearchGate não é licença e DOI não consta confirmado. Não publicar PDF. | CORREÇÃO NECESSÁRIA |

## Verificação bibliográfica externa focalizada — 21/11/2026

A pesquisa abaixo confronta **metadados de páginas identificadas** dos oito cards de maior risco (EC-021/024/028/030/032/033/034/036). Não equivale a ler integralmente as fontes originais, verificar página a página as afirmações, revisar originalidade nem emitir parecer jurídico ou qualquer uma das duas revisões independentes obrigatórias.

| Card | Achado verificável e URL | Situação após pré-verificação |
|---|---|---|
| EC-021 | O editor PLOS identifica o artigo original (DOI [10.1371/journal.pcbi.1005619](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005619)) e a correção (DOI [10.1371/journal.pcbi.1005830](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005830)). | Correção bibliográfica confirmada; detalhes alterados devem ser cotejados antes de citação científica. |
| EC-024 | A página oficial do periódico apresenta [10.63595/rbhcs.v1i1.10351](https://periodicos.furg.br/rbhcs/article/view/10351/0) para o artigo de 2009; o DOI não constava no card. | DOI **localizado na página atual do periódico**; confirmar metadados e eventuais alterações de registro, sem supor que existia em 2009. |
| EC-028 | A página DOI do artigo da SAGE é [10.1177/1609406917733847](https://doi.org/10.1177/1609406917733847); o PDF de origem indicado pelo próprio card menciona CC BY-NC. | DOI e identidade bibliográfica identificados; licença aplicável por edição e direitos do uso pretendido requerem checagem independente. |
| EC-030 | O editor identifica Hennink/Kaiser 2022 com DOI [10.1016/j.socscimed.2021.114523](https://www.sciencedirect.com/science/article/pii/S0277953621008558). | Metadados compatíveis; **licença CC BY-NC-ND ainda não confirmada independentemente na cópia exata**. |
| EC-032 | O editor Annual Reviews identifica Cattaneo/Titiunik 2022, vol. 14, pp. 821–851, DOI [10.1146/annurev-economics-051520-021409](https://www.annualreviews.org/content/journals/10.1146/annurev-economics-051520-021409), com copyright/reserva de direitos no portal. | Identidade/DOI confirmados; não redistribuir a obra original. |
| EC-033 | O NBER identifica o *Working Paper* 13039 de 2007 com DOI [10.3386/w13039](https://www.nber.org/papers/w13039). Existe **outra identificação, Technical Working Paper t0337**, com DOI [10.3386/t0337](https://www.nber.org/papers/t0337). | DOI confirmado **para edição w13039 citada no card**, não confundir com t0337 ou artigo de periódico posterior; direitos não liberados. |
| EC-034 | O SSRN identifica o relatório *Comparative Methods and Process Tracing* (2019), Bennett/Fairfield/Soifer, com DOI [10.2139/ssrn.3333405](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3333405). | DOI de depósito SSRN identificado; confirmar edição/autorizações da versão exata e não presumir licença do PDF. |
| EC-036 | Produção institucional do autor vinculada ao livro *Política Comparada: Teoria e Método* (ABCP/EduERJ, 2022): [registro UnB](https://sigaa.unb.br/sigaa/public/docente/producao.jsf?siape=1421282). | Capítulo bibliográfico localizado de modo preliminar; **DOI e direitos não confirmados**; ResearchGate não autoriza redistribuição. |

**Saldo deste pré-check:** oito referências examinadas em fontes externas; dentre os quatro cards originalmente sem DOI textual (EC-024/033/034/036), três ganharam identificador externo plausível ligado à edição declarada (EC-024/033/034), e um continua sem DOI verificado (EC-036). **Os cards originais não foram alterados; os quatro ainda não exibem DOI no corpo.** Nenhuma licença de redistribuição foi aprovada, nenhum card passou pelas duas checagens independentes e nenhuma fonte foi promovida a [L].

**Próxima ação concreta:** cotejar licença/edição e originalidade dos oito itens com documentação primária e pareceres independentes; depois, sob coordenação, conciliar os recibos com as demais etapas para avaliar V1-16, mantendo #102/#103 P0 pendentes.

## Testes, CI e readback
- Controle de integridade: SHA-256 dos 18 cards conferidos (18/18 MATCH) e verificação de leitura dos dois recibos no GitHub.
- Comparação de escopo com o manifesto-base: 0 commits atrás e somente RESULTS.md e DELTA.json alterados; a contagem de commits varia com cada atualização do diário.
- Commit verificado 063c3221522c1ae65cbfaa4f6e307eeca43e1fdb: 0 status checks combinados e 0 workflow runs do tipo PR consultados. CI automatizada NÃO COMPROVADA para o lote; não alegar verde.

## O que ficou em execução e limitações
- A revisão de conteúdo aqui foi de primeira triagem documental. Não se comprovou que fonte primária, versão ou página respaldam individualmente os enunciados dos 18 cards.
- Não foram colhidas assinaturas nem atribuídos nomes de revisores. A qualidade editorial e a originalidade frente aos textos originais não estão comprovadas; permanecem sujeitas a dois controles independentes previstos no CARD-POLICY.md.
- Hash de card é verificação de integridade, **não** prova de adequação metodológica, legalidade ou veracidade.
- A tentativa de editar apenas a subseção 31.05 do Markdown no Google Drive por `documents.batchUpdate` foi recusada (arquivo MIME `text/markdown`, HTTP 400 FAILED_PRECONDITION). A alternativa `files.update` sobrescreve bytes completos sem CAS documentado. Como há sessões concorrentes, **não foi alterado o MD do Drive**; a conciliação exclusiva de 31.05 está pendente e deve ocorrer por mecanismo que preserve todos os registros simultâneos.

## Próximos passos
1. Dois revisores independentes (direitos/originalidade; fidelidade científica) decidem para cada card: aceitar, corrigir ou excluir, com datas e evidências. **Não tomar esta triagem automática como aceite**.
2. Verificar contra fontes primárias e licença por edição, com atenção a EC-021, EC-024, EC-028, EC-030, EC-032, EC-033, EC-034 e EC-036.
3. Conciliar somente a subseção 31.05 no MD canônico, com leitura da versão atual e preservação das outras 19 abas; verificar por readback e registrar SHA/revision se ferramenta permitir.
4. Integrador verificar este delta/recibo, sanear P0 #102/#103 e os bloqueios das outras etapas antes de liberar V1-16. Nenhum merge, release, tag, mudança global ou publicação de PDF protegido foi realizado.

## Controle de escopo
A escrita GitHub desta etapa limita-se exclusivamente a `V1-05-RESULTS.md` e `V1-05-DELTA.json`. Os 18 cards consultados foram preservados sem edição; nenhum registry, ledger, catálogo, manifesto, main ou branch de terceiro foi modificado.

## Pacotes individuais para duas revisões independentes — continuidade 21/11/2026

**Natureza desta entrega:** PACOTES DE REVISÃO preparados com base nos 18 cards do snapshot imutável `c5e0ca9abd98f824f1576c3ad94c6e9a5d18e9bf` e nos resultados de triagem já registrados. Isto **não** constitui parecer independente, verificação de plágio/similaridade, certificação de licença, revisão jurídica ou aceite científico.

**Controle de independência:** para cada card devem existir **dois pareceres assinados e distintos**, com identificação interna controlada (sem expor IDs privados), data, edição/cópia exata, links autorizados, trecho/localização de evidência, decisão, objeções e resolução. O revisor A examina **direitos e originalidade**; o revisor B examina **fidelidade científica e editorial**. Os autores da triagem e o mantenedor não são contados automaticamente como esses revisores. Ambos permanecem **NÃO RECEBIDOS (0/18 em cada trilha)**.

| Card | Revisor A — direitos/originalidade: achado preliminar e prova a exigir | Revisor B — fidelidade: confronto obrigatório | Estado A/B |
|---|---|---|---|
| EC-019 | Síntese editorial declarada; direitos das edições Guest/Byrne e similaridade textual ainda não atestados | Confrontar a diferença entre saturação temática operacional, reflexividade e amostragem teórica; apontar passagens correspondentes nos originais | PENDENTE / PENDENTE |
| EC-020 | Síntese declarada de Pautasso/PLOS; licença da edição e confronto de originalidade pendentes | Distinguir regras de redação narrativa de protocolo de revisão sistemática; marcar o que é inferência editorial | PENDENTE / PENDENTE |
| EC-021 | PLOS informa CC BY no artigo e na correção; atribuição e versão corrigida devem ser verificadas (https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005619 ; https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005830) | Confrontar texto/alcance da correção de 09/11/2017 com a orientação sobre estrutura e distinguir regras prescritivas de evidência empírica | PENDENTE / PENDENTE |
| EC-022 | Síntese declarada de Sandve/PLOS; autorias e termos de reutilização da edição ainda sem revisão formal | Confrontar dez regras e separar rerun reprodutível de replicação/validade de afirmações | PENDENTE / PENDENTE |
| EC-023 | Síntese declarada de Forero/PLOS; verificar originalidade e termos da versão exata | Conferir estimando, compatibilidade de efeitos, dependência entre estimativas e heterogeneidade: distinguir proposta editorial do conteúdo citado | PENDENTE / PENDENTE |
| EC-024 | Página atual do periódico FURG exibe CC BY 4.0, mas licença da cópia arquivada/histórico de edição e autorização concreta pendentes (https://periodicos.furg.br/rbhcs/article/view/10351/0) | Confrontar autoria/edição, natureza de pesquisa documental, crítica de fonte e distinção de revisão bibliográfica; registrar seção/página | PENDENTE / PENDENTE |
| EC-025 | Card informa PDF consultado apenas para escopo; termos exatos do PDF Morgan não verificados | Confrontar seleção amostral de documentos, unidades de análise e processo de interpretação no original | PENDENTE / PENDENTE |
| EC-026 | Card informa consulta preliminar ao PDF Byrne; checar licença exata e possível dependência expressiva | Confrontar análise temática reflexiva, construção de temas e inadequação de concordância intercodificador universal | PENDENTE / PENDENTE |
| EC-027 | Card informa consulta preliminar ao PDF Kiger/Varpio; direitos do AMEE Guide pendentes | Conferir variantes da análise temática, etapas descritas e condições de aplicação dos critérios | PENDENTE / PENDENTE |
| EC-028 | PDF hospedado pela editora SAGE exibe CC BY-NC 4.0 na primeira página; a restrição NC impede assumir uso comercial irrestrito (https://journals.sagepub.com/doi/pdf/10.1177/1609406917733847) | Confrontar trilha de decisões, trustworthiness e limites da mera auditabilidade com a argumentação da fonte; registrar páginas | PENDENTE / PENDENTE |
| EC-029 | PDF van Rijnsoever consultado apenas em identificação declarada; direitos e originalidade ainda não comparados | Verificar hipóteses/simulações e impedir extrapolação de tamanho universal de amostra | PENDENTE / PENDENTE |
| EC-030 | Card declara CC BY-NC-ND, sem certificação independente da licença da cópia (https://www.sciencedirect.com/science/article/pii/S0277953621008558) | Verificar revisão sistemática, variabilidade dos contextos e diferença entre saturação de códigos e de significados; confirmar condições empíricas | PENDENTE / PENDENTE |
| EC-031 | Síntese Roth et al. sem validação independente do regime de direitos da edição citada | Conferir tendências paralelas, heterogeneidade temporal, efeitos de tratamento e críticas a TWFE | PENDENTE / PENDENTE |
| EC-032 | Portal da Annual Reviews declara copyright © 2022 e 'All rights reserved'; nenhuma autorização de redistribuição identificada (https://www.annualreviews.org/content/journals/10.1146/annurev-economics-051520-021409) | Verificar validade local, manipulação do running variable, largura da janela, inferência e extrapolação | PENDENTE / PENDENTE |
| EC-033 | NBER w13039 identificado; não assumir autorização pela acessibilidade; distinção entre w13039 e t0337 necessária (https://www.nber.org/papers/w13039) | Confrontar sharp/fuzzy, continuidades e opções práticas na edição exata; não misturar versões posteriores | PENDENTE / PENDENTE |
| EC-034 | Depósito SSRN DOI identificado, mas uma licença do SSRN para hospedar não concede licença de redistribuição a terceiros (https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3333405) | Conferir autoria/versão do relatório QTD e diferença entre inferência de mecanismo, evidência diagnóstica e sequência narrativa | PENDENTE / PENDENTE |
| EC-035 | Síntese editorial de Thiem; regime de direitos/semelhança do original ainda não verificados | Conferir necessidade, suficiência, calibragem, contradições e limites de interpretações causais de solução QCA | PENDENTE / PENDENTE |
| EC-036 | Somente rastro bibliográfico de capítulo; ResearchGate não concede direito de redistribuição, DOI não confirmado (https://www.researchgate.net/publication/358594522) | Conferir capítulo/edição e exemplos de política pública, calibragem e inferência configuracional; requer exemplar primário | PENDENTE / PENDENTE |

### Evidências novas e cautelas específicas
- EC-021: a página da PLOS registra CC BY para o artigo e para a correção, além da correção publicada em 09/11/2017. A licença do artigo não prova que todo material de terceiros ou figura seja livre de ressalvas; atribuição e versão exata continuam no roteiro do revisor A.
- EC-024: a página contemporânea do periódico FURG anuncia CC BY 4.0. **Isto não comprova que a cópia armazenada foi obtida dessa edição/versão, nem configura homologação jurídica**. Não modificar automaticamente `doi_status` ou `rights_approved` do card.
- EC-028: a primeira página do PDF disponibilizado pela SAGE traz CC BY-NC 4.0. O texto do card já alertava NC; o novo ganho é a localização da declaração na cópia do editor. Não promover redistribuição comercial.
- EC-032: o portal da Annual Reviews registra 'All rights reserved'. Não publicar figura, tabela, PDF ou extenso excerto; usar apenas síntese independente enquanto direitos permanecem não aprovados.
- EC-030, EC-033, EC-034 e EC-036: persistem bloqueios para concluir os termos de direitos da **cópia exata**, mesmo com DOI ou localizador bibliográfico. EC-036 não tem DOI verificado.

### Critério de aceite verificável por card
1. **A/rights-originality:** registro assinado de um revisor independente com fonte oficial para titular/termos/edição da cópia, comparação editorial de originalidade e decisão `ACEITAR_COM_LIMITE` / `CORRIGIR` / `REJEITAR`; sem publicar o material protegido.
2. **B/scientific-fidelity:** registro assinado por segundo revisor distinto, com cotejo item a item de afirmações vs. fonte primária, localizador de seção/página e contraexemplo, decisão e justificativa; vedada promoção automática [I]→[L].
3. **Conciliação:** se há ressalva, correção e revisão das partes pertinentes com evidência, mantendo o card em Draft até ambas as decisões documentadas; os pareceres **não** substituem o controle dos bloqueios #102/#103 nem a decisão de integração por V1-16.

### Teste e rastreabilidade desta continuidade
- Manifesto fixo: `7c92045310eb3b1474a9612a777fb0012a511592`, apenas EC-019…EC-036; nenhuma outra etapa ou card editado.
- HEAD precedente da PR Draft #104: `01d8ea7cab5988583d5e79cb24495ff5157a7298`; comparação antes desta escrita: 11 commits à frente, 0 atrás, somente dois recibos alterados.
- CI observada nesse HEAD: workflow `Release audit` ID 44959898288 concluiu `success`; status checks combinados retornaram lista vazia. **Esse teste não certifica revisão de direitos nem fidelidade**. Após novos commits, CI precisa ser revalidada no novo HEAD.
- Google Drive: somente comentários de 31.05 são elegíveis nesta janela; o corpo `text/markdown` bruto permanece sem edição transacional/CAS garantida e não será substituído.

**Próxima ação única:** solicitar e receber o **primeiro parecer independente de direitos/originalidade (revisor A)** para EC-019…EC-036 com o pacote acima, preservando a segunda trilha científica pendente. Nenhum merge/publicação.
