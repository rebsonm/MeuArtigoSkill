# V1-05/20 — auditoria editorial dos cards EC-019…EC-036

Data: 2026-11-21 (America/Fortaleza)
Branch exclusiva: `work/v1-05-20261121`.
Manifesto imutável: `7c92045310eb3b1474a9612a777fb0012a511592` em `knowledge/methodology/intake/v1_parallel/V1-WORKPACKAGES-MANIFEST.json`.
Corpus de leitura: `c5e0ca9abd98f824f1576c3ad94c6e9a5d18e9bf`.
**Estado da entrega:** ENTREGUE_PARA_AUDITORIA (documental); **não** AUDITADO, INTEGRADO, homologado nem autorizado a publicação.
**Estado científico:** 18 cards permanecem [I], DRAFT_NEEDS_INDEPENDENT_REVIEW; nenhuma promoção a [L].

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
