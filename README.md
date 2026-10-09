# Meu Artigo — Skill para pesquisa e construção de artigos científicos

**Versão atual:** `0.7.0-beta.1`

**Status de distribuição:** repositório público · versão beta em desenvolvimento · código e documentação disponíveis para consulta e instalação · veja [CHANGELOG.md](./CHANGELOG.md) · metadados de citação em [CITATION.cff](./CITATION.cff)

**Meu Artigo** é uma Skill **multiplataforma** para pesquisa e construção de artigos científicos. Ela transforma um problema, pergunta ou ideia de pesquisa fornecida pelo usuário em um **processo científico rastreável, persistente, orientado por evidências e auditável quanto à sua própria construção**. O núcleo metodológico vive em `SKILL.md`; diferenças entre ChatGPT, Claude e Gemini ficam isoladas em adapters/documentação de plataforma.

Ela não entrega um “artigo pronto por mágica” e não reutiliza o conteúdo de um projeto anterior. O que a Skill reutiliza é um **método de trabalho**: organização do projeto, auditoria de novidade, protocolo, buscas bibliográficas, registro das decisões, deduplicação, screening, full text, matriz de evidências, síntese, redação e auditoria final. Todo esse fluxo é acompanhado por uma camada de gestão **C.A.D.A.**, para tornar o passo a passo visível e rastreável.

> O tema, a pergunta de pesquisa, os conceitos, as strings de busca, as fontes, as categorias analíticas e as conclusões pertencem sempre ao projeto do novo usuário.

## 🚀 Nunca usou GitHub? Comece aqui

> **Acesso público:** o código e a documentação podem ser consultados ou obtidos neste repositório sem convite. A versão continua beta, e controles técnicos aprovados não significam que seus resultados científicos foram validados empiricamente.

Você **não precisa saber Git, programação nem terminal** para testar o Meu Artigo.

Se esta é sua primeira vez no GitHub, abra o guia:

### 👉 [COMECE AQUI — passo a passo para quem nunca usou GitHub](./docs/COMECE-AQUI.md)

O caminho básico é:

```text
GitHub → botão Code → Download ZIP
       → no ChatGPT, importar o ZIP completo
       → seguir o guia da sua IA
```

Depois escolha:

- [ChatGPT / Codex](./docs/CHATGPT.md)
- [Claude](./docs/CLAUDE.md)
- [Gemini](./docs/GEMINI.md)

Você não precisa clonar o repositório, criar branch, fazer commit ou instalar Git para usar a Skill.

### Disponibilidade das Skills

A instalação nativa depende da plataforma e do plano atual:

| Plataforma | Situação atual resumida |
|---|---|
| **ChatGPT** | A disponibilidade pode variar por conta e rollout. Em teste direto em 07/10/2026, a criação/importação de Skills estava ativa também em uma conta Plus. Verifique a presença de **Plugins → Habilidades** na própria interface. |
| **Claude.ai** | Skills personalizadas podem ser enviadas em planos Pro, Max, Team e Enterprise quando a execução de código está habilitada. |
| **Gemini** | Skills dependem dos requisitos atuais da conta/assinatura Google; confira o guia antes do teste. |

Se o menu de Skills não aparecer, abra o guia da plataforma antes de concluir que houve erro no repositório.

## Screening com revisão humana rastreável

A triagem diferencia **sugestões da IA** de **decisões finais atribuídas à revisão humana**. O mecanismo gratuito em Python exige motivo, identificação do revisor, referência à manifestação original e registro das divergências. Projetos novos não podem congelar o corpus com decisões incompletas. A implementação reaproveita a aba 07_SCREENING e o CSV canônico, sem nova aba ou ID. Consulte [Screening auditável](./docs/SCREENING-AUDITAVEL.md). A presença dos campos não autentica, sozinha, a identidade do revisor.

## Avaliação crítica da qualidade metodológica das fontes

A Skill acrescenta avaliação por tipo de fonte — quantitativa, qualitativa, métodos mistos, revisão, conceitual, normativa ou outra — sem confundir existência de DOI, prestígio do periódico ou popularidade com rigor do estudo. O código fornece checklists adaptáveis, exige justificativa, limitações e referência à avaliação do pesquisador e bloqueia o uso de evidências materialmente inadequadas no congelamento final. Não atribui notas universais automáticas nem inventa pareceristas. Leia [Avaliação crítica de fontes](./docs/AVALIACAO-CRITICA-FONTES.md).

## Avaliação de qualidade científica

O repositório inclui um benchmark reproduzível, com referências reais e contagens publicadas, para comparar saídas **efetivamente produzidas** pela Skill. O verificador aponta divergências, cobertura e aspectos não avaliados; confirmação de DOI não substitui avaliação de claims ou categorias teóricas. Uma etapa opcional consulta metadados públicos gratuitos e publica o relatório observado no GitHub Actions. Veja [Avaliação de qualidade científica](./docs/AVALIACAO-QUALIDADE-CIENTIFICA.md).

## Controle de originalidade, inferências e apoio das fontes

O Meu Artigo distingue afirmações baseadas na literatura [L], inferências analíticas [I] e propostas próprias [P]. Antes de finalizar um claim, o verificador gratuito em Python exige vínculos com fontes, justificativa da inferência ou comparação explícita com os trabalhos anteriores, conforme o tipo. Afirmações absolutas de ineditismo são sinalizadas e impedem o congelamento do manuscrito enquanto não forem delimitadas. O mecanismo mantém os mesmos IDs e a planilha existente. Isso não demonstra originalidade real nem substitui exame humano. Consulte [Controle de claims](./docs/CONTROLE-CLAIMS-E-ORIGINALIDADE.md).

## Decisões científicas com compreensão explícita

Nos novos projetos, os gates científicos existentes pedem ao pesquisador que explique brevemente, com suas próprias palavras, por que aprovou uma escolha e qual limitação reconhece. O modo iniciante apresenta explicações acessíveis e mantém a autonomia entre os gates. Os textos humanos são registrados no controle atual, sem novas abas, identificadores ou serviços pagos. Isso reforça a responsabilidade decisória, mas não equivale a atestar compreensão profunda. Consulte [Validação formativa](./docs/VALIDACAO-FORMATIVA.md).

## Comprovação de eventos e rastreabilidade

A Skill diferencia execução comprovada de ação apenas declarada. Operações locais permitidas podem produzir recibos técnicos com resultado da execução e hashes dos artefatos. Buscas externas e ações não observadas permanecem como não verificadas, sem inventar comprovantes. Isso não exige planos pagos, novos identificadores ou novas abas. Consulte [Comprovação de eventos](./docs/COMPROVACAO-EVENTOS.md).

## Verificação de fontes e passagens

A Skill inclui verificação bibliográfica independente do texto produzido pela IA: consultas gratuitas ao Crossref/OpenAlex, reconciliação de DOI e metadados, avisos de atualização editorial e localização de passagens em arquivos disponíveis localmente. Não exige serviços pagos e não envia PDFs inteiros a essas APIs. Divergências e resultados inconclusivos permanecem visíveis para revisão humana; metadados corretos não equivalem a comprovação do conteúdo de um argumento. Consulte [Verificação de fontes](./docs/VERIFICACAO-FONTES.md).

## O que a Skill faz

A Skill conduz o pesquisador por um fluxo completo:

1. recebe o problema, pergunta, fenômeno ou ideia de artigo do usuário;
2. verifica primeiro o Google Drive; se não estiver conectado, orienta a conexão e verifica novamente;
3. se o Drive continuar indisponível, pergunta explicitamente se o usuário quer continuar sem ele; somente uma resposta afirmativa autoriza o uso de arquivos/resultados do Work ou armazenamento local;
4. cria ou retoma o workspace persistente no Google Drive; quando Drive é canônico, resultados locais/Work são apenas staging até serem sincronizados;
5. registra o problema original e cria `CONTINUIDADE.md`, protocolo e matriz-mestra;
5. faz uma auditoria inicial de novidade e de terminologia;
6. ajuda a refinar pergunta, objetivo e contribuição;
7. identifica o desenho metodológico adequado, sem chamar toda busca estruturada de “revisão sistemática”;
8. constrói e versiona estratégias de busca;
9. usa fontes acadêmicas e bibliográficas de acordo com o papel de cada uma;
10. valida exports de Scopus/Web of Science quando essas bases forem usadas;
11. consolida e deduplica registros sem excluir automaticamente casos duvidosos;
12. conduz screening em passes explícitos;
13. acompanha obtenção e leitura de textos completos;
14. extrai evidências para uma matriz estruturada;
15. sintetiza evidências entre fontes em vez de apenas resumir artigo por artigo;
16. mantém um *claims ledger* para ligar afirmações do manuscrito às evidências;
17. redige o artigo a partir dos artefatos canônicos do projeto;
18. audita método, contagens, evidências, citações e requisitos da revista antes da submissão;
19. mantém o projeto retomável por outro chat ou agente sem depender da memória da conversa;
20. governa o passo a passo pelo C.A.D.A. — Capturar, Atribuir, Definir prazo e Acompanhar;
21. usa a própria planilha/matriz como gerenciador C.A.D.A. universal;
22. quando disponível e desejado, espelha as tarefas C.A.D.A. em ClickUp, Jira/Atlassian ou Trello;
23. mantém uma trilha de rastreabilidade do processo de construção do artigo;
24. registra usos materiais de IA, finalidade, ferramenta/modelo quando conhecido e validação humana;
25. registra decisões científicas materiais com `DEC_ID`;
26. usa gates humanos críticos e snapshots verificáveis com `GATE_ID` e `SNAP_ID`;
27. gera o Mapa do Corpus somente com metadados reais do corpus retido;
28. oferece Grounded Corpus Mode para perguntas limitadas ao full text validado;
29. gera relatório de transparência para revisor/editor;
30. exporta proveniência interoperável em W3C PROV/RO-Crate com SHA-256;
31. aplica anonimização de alto rigor aos arquivos externos, incluindo conteúdo visível, metadados ocultos, comentários, revisões, nomes de arquivo, caminhos, links e inspeção final antes da liberação.

## Direitos autorais e PDFs do corpus

O código do Meu Artigo é público, mas **os PDFs de terceiros não se tornam públicos por isso**. A autorização para ler e analisar um texto é diferente da autorização para redistribuí-lo. O controle RT-09 registra a origem, licença ou permissão, evidências, atribuição e hash do arquivo na tabela de full text existente. O exportador RO-Crate exclui textos integrais por padrão e bloqueia a inclusão de documentos sem direitos de redistribuição documentados. Sem novas abas, identificadores ou serviços pagos. Consulte [Direitos dos PDFs e full text](./docs/DIREITOS-FULLTEXT-E-PDFS.md).

## C.A.D.A.: gestão operacional não é validação científica

O C.A.D.A. organiza demandas, responsáveis, prazos e comprovação de providências administrativas. A qualidade metodológica depende dos procedimentos científicos e da revisão humana, nunca do percentual de tarefas concluídas. O novo controle separa indicadores de gestão, registros científicos e recibos de execução no relatório de transparência; bloqueia aprovações que usam apenas `CADA-0001` ou `DONE` como suposta prova científica. Há um [protocolo comparativo com e sem C.A.D.A.](./docs/LIMITES-CADA-E-COMPARACAO.md), **ainda sem dados coletados nem efeitos demonstrados**. Python padrão, sem novas abas ou serviços pagos.

## Gestão do passo a passo com C.A.D.A.

O **C.A.D.A. não substitui a metodologia científica**. Ele governa o trabalho necessário para executá-la.

| C.A.D.A. | No Meu Artigo |
|---|---|
| **Capturar** | registrar uma ação, decisão, dependência, prazo ou bloqueio relevante |
| **Atribuir** | definir responsável, etapa científica, prioridade e artefato relacionado |
| **Definir prazo** | registrar prazo externo, prazo do usuário, meta interna ou dependência |
| **Acompanhar** | atualizar status até existir evidência de avanço ou conclusão |

Cada unidade operacional recebe um identificador como `CADA-0042`.

Assim, a Skill consegue responder com clareza:

- onde o artigo está;
- o que já foi concluído;
- o que está em andamento;
- o que está bloqueado;
- quem é responsável;
- qual é o próximo passo;
- qual é o prazo;
- qual evidência comprova o avanço.

A documentação completa está em [docs/CADA.md](./docs/CADA.md).

### A planilha já é um gerenciador completo

O usuário **não precisa conhecer ClickUp, Jira ou Trello**.

O modo padrão é `MATRIX_ONLY`: a própria matriz-mestra gerencia o projeto por meio de:

- `11_CADA_Control` — tarefas, responsáveis, próxima ação, prazos, status e evidências;
- `15_CADA_Dashboard` — visão resumida do andamento;
- `16_INTEROPERABILIDADE` — exports PROV/RO-Crate e fixidade;
- `17_DECISOES` — decisões científicas materiais;
- `18_VALIDACOES` — gates humanos críticos;
- `19_SNAPSHOTS` — estados congelados;
- `20_MAPA_CORPUS` — estrutura exploratória do corpus validado.

Quem já usa uma ferramenta de gestão pode ativar `MATRIX_PLUS_EXTERNAL`.

### ClickUp, Jira e Trello

O usuário pode conectar um gerenciador de trabalho para visualizar o C.A.D.A. fora da conversa.

A Skill pode usar:

- **ClickUp**;
- **Jira**, via Atlassian;
- **Trello**;
- ou um gerenciador equivalente com capacidade de leitura e escrita.

Por padrão, usa **um único gerenciador principal por artigo**. A matriz científica continua sendo a fonte de verdade; o card/ticket é um espelho operacional.

O vínculo entre cada item C.A.D.A. e a tarefa externa fica registrado em `12_PM_Sync`.

## Template oficial da matriz C.A.D.A.

A planilha que gerencia o projeto tem agora um **template canônico de 21 abas**, com dashboard, C.A.D.A., linha do tempo, protocolo, buscas, screening, full text, matriz de evidências, síntese, claims, uso de IA, submissão e sincronização opcional.

O modo padrão é `MATRIX_ONLY`: a pessoa consegue conduzir todo o projeto sem conhecer software de gestão.

A Skill deve tentar criar essa matriz **antes das buscas em escala**:

1. como planilha nativa quando houver integração de planilhas;
2. pelo gerador oficial `scripts/build_matrix_template.py` quando `artifact_tool` estiver disponível;
3. pelos CSVs somente como compatibilidade final.

Documentação: [docs/MATRIZ-CADA.md](./docs/MATRIZ-CADA.md)

Especificação técnica: [references/spreadsheet-template.md](./references/spreadsheet-template.md)

## Construção orientada à revista

No início de um projeto, o Meu Artigo pergunta se o pesquisador já possui uma revista-alvo e solicita as **diretrizes oficiais para autores e o template/layout**, quando existirem.

Se esses materiais forem fornecidos, a Skill cria um `JOURNAL_PROFILE` e passa a construir o manuscrito considerando desde cedo estrutura, extensão, resumo, referências, anonimização, declarações, política de IA e demais requisitos do periódico.

Se ainda não houver revista definida, o projeto segue normalmente em `JOURNAL_NEUTRAL`.

A revista orienta a **apresentação e arquitetura do manuscrito**, nunca os resultados ou a força das evidências.

Veja [docs/JOURNAL-AWARE.md](./docs/JOURNAL-AWARE.md).

## Anonimização de alto rigor

O Meu Artigo trata anonimização como uma etapa de liberação, não como simples remoção do nome da primeira página.

Arquivos internos podem permanecer identificados quando isso é necessário para a gestão do projeto. Já arquivos destinados a circulação externa usam, por padrão, o modo `EXTERNAL_ANONYMIZED` quando a identidade não é necessária ou quando as regras da revista ainda não estão definidas.

A verificação considera conteúdo visível e também possíveis vazamentos em propriedades do documento, comentários, controle de alterações, notas, planilhas ocultas, nomes de arquivos, caminhos locais, links privados, afiliações, ORCID, contatos, agradecimentos, financiamento e metadados de PDF/imagens. Para arquivos `EXTERNAL_ANONYMIZED`, a política é `ZERO_NONESSENTIAL_METADATA`: também são removidos metadados neutros de geração, como Creator, Producer, Generator, Application, datas de criação/modificação, XMP/EXIF/IPTC e identificadores equivalentes. Portanto, um PDF que ainda informe “gerado com Python”, `pypdf`, ReportLab, Matplotlib, LibreOffice ou outro gerador não passa na liberação.

Cada projeto mantém um `ANONYMIZATION_PROFILE.json` confidencial. Esse arquivo nunca deve ser incluído em pacotes externos, snapshots compartilháveis ou submissões cegas.

Antes da liberação externa, a sequência obrigatória é `scripts/sanitize_metadata.py` → `scripts/audit_anonymization.py`. O primeiro remove metadados descritivos/proveniência que não são necessários para a integridade do arquivo; o segundo audita os arquivos exatos de saída e gera um `ANONYMIZATION_AUDIT`. O GATE-0007 não deve ser aprovado enquanto houver qualquer metadado residual bloqueante, achado de alto risco ou revisão pendente.

Veja [docs/ANONIMIZACAO.md](./docs/ANONIMIZACAO.md).

## Auditoria de robustez dos claims

Antes de congelar os claims principais, o Meu Artigo verifica não apenas se existe evidência favorável, mas também evidência contrária, explicações alternativas, condições de contorno e dependência excessiva de uma única fonte.

Essa auditoria acontece dentro do `GATE-0006`, sem criar nova camada de gestão.

Veja [docs/ROBUSTEZ-CLAIMS.md](./docs/ROBUSTEZ-CLAIMS.md).

## Exportação interoperável da proveniência

O Meu Artigo consegue transformar a trilha interna de rastreabilidade em um **pacote auditável e legível por máquinas**.

A exportação usa:

- **W3C PROV-O** para entidades, atividades, agentes e relações de proveniência;
- **RO-Crate 1.3** para empacotar o objeto de pesquisa;
- **SHA-256** para verificar se os arquivos do pacote permaneceram inalterados.

O pesquisador não precisa conhecer esses padrões para usar a Skill. Eles funcionam como camada de interoperabilidade.

Cada export recebe um `EXPORT-####` e é registrado em `16_INTEROPERABILIDADE`.

Veja [docs/INTEROPERABILIDADE.md](./docs/INTEROPERABILIDADE.md).

## Mapa do Corpus e consulta grounded

Depois que existe um corpus retido real, o Meu Artigo pode gerar uma visão exploratória da sua estrutura em `20_MAPA_CORPUS`.

O mapa usa somente metadados disponíveis e não inventa periódicos, keywords, citações, clusters ou cobertura de OpenAlex.

O **Grounded Corpus Mode** permite consultar analiticamente apenas o full text validado, com Record_ID, Evidence_ID e locator quando disponíveis. Se o corpus não sustenta a resposta, a Skill deve dizer isso em vez de completar com memória do modelo.

Veja [docs/MAPA-CORPUS.md](./docs/MAPA-CORPUS.md).

## Cadeia de custódia científica

Além de tarefas e eventos, o Meu Artigo distingue três objetos de governança:

- **DEC_ID** — registra o que foi decidido, alternativas, justificativa e impacto;
- **GATE_ID** — registra a validação humana em poucos pontos críticos;
- **SNAP_ID** — congela o estado oficial do projeto com SHA-256.

A cadeia, quando aplicável, fica:

```text
DEC_ID → CADA_ID → TRACE_ID → Evidence/Claim → GATE_ID → SNAP_ID → EXPORT_ID
```

A Skill trabalha autonomamente entre os gates. Ela só pede julgamento humano quando uma transição científica crítica está pronta para validação.

Também pode gerar um **Relatório de Transparência e Rastreabilidade para Revisor/Editor**, sem expor o workspace privado inteiro.

## Rastreabilidade da construção do artigo

Um objetivo central do Meu Artigo é permitir que o pesquisador responda:

> **Como este artigo foi construído?**

Para isso, gestão e rastreabilidade são separadas:

- **C.A.D.A.** mostra onde estamos e o que precisa acontecer;
- **rastreabilidade** mostra como chegamos até aqui.

O projeto mantém:

- `RASTREABILIDADE.md` — síntese legível da proveniência do processo;
- `13_Traceability_Log` — registro estruturado dos eventos científicos materiais;
- `14_AI_Use_Log` — registro específico de uso de IA e validação humana.

A trilha permite ligar, quando aplicável:

```text
Claim_ID
  ↓
Evidence_ID
  ↓
Record_ID / fonte
  ↓
Search_ID / origem
  ↓
Trace_ID
  ↓
CADA_ID / decisão de protocolo
```

Isso aproxima a construção do artigo de um processo auditável, especialmente importante em pesquisa assistida por IA.

Essa preocupação é consistente com diretrizes editoriais recentes. A Revista de Ciências da Administração, por exemplo, determina que usos substantivos de IA sejam descritos nos métodos e que ferramenta, versão, finalidade e procedimentos de validação humana sejam explicitados para assegurar rastreabilidade.

Veja [docs/RASTREABILIDADE.md](./docs/RASTREABILIDADE.md) e [docs/GOVERNANCA-CIENTIFICA.md](./docs/GOVERNANCA-CIENTIFICA.md).

## Exemplo de ponta a ponta

Veja o [exemplo ilustrativo](docs/EXEMPLO-FLUXO.md): da pergunta inicial à evidência, à afirmação e à decisão humana. Os conteúdos são didáticos e não representam uma pesquisa executada.

A relação entre arquivos de controle e abas visuais está no [mapa de armazenamento](references/storage-mapping.md). O gerador de planilha cria a estrutura; não deve ser confundido com sincronização automática.

## O que o usuário precisa trazer

No mínimo, um destes elementos:

- um problema de pesquisa;
- uma pergunta de pesquisa;
- um fenômeno que deseja estudar;
- uma lacuna teórica percebida;
- uma ideia de artigo suficientemente específica.

Exemplo:

> “Quero estudar por que pequenos municípios têm dificuldade para adotar inteligência artificial em processos de compras públicas.”

A Skill não deve importar tema, constructos, artigos, strings ou resultados de projetos anteriores. Ela constrói o projeto científico a partir da entrada do novo usuário.

## Portabilidade entre IAs

O projeto separa **método** de **plataforma**.

| Camada | Portável? | Papel |
|---|---|---|
| `SKILL.md` | Sim | Metodologia e workflow científico |
| `references/` | Sim | Regras de busca, evidência, síntese, persistência e rigor |
| `scripts/` | Em geral | Operações determinísticas quando a plataforma permite execução |
| `agents/openai.yaml` | Não | Adapter específico para ambientes OpenAI |
| `docs/CHATGPT.md` | Plataforma | Instalação/comportamento no ChatGPT/Codex |
| `docs/CLAUDE.md` | Plataforma | Instalação/comportamento no Claude |
| `docs/GEMINI.md` | Plataforma | Instalação/comportamento no Gemini |

A Skill não exige que todas as IAs tenham os mesmos plugins. O núcleo resolve **capacidades por função**: armazenamento persistente, descoberta acadêmica, contexto de citação, busca em web/editoras/repositórios, bases bibliográficas indexadas e execução de scripts. Produtos específicos são implementações possíveis dessas funções.

Guias:

- [ChatGPT / Codex](./docs/CHATGPT.md)
- [Claude](./docs/CLAUDE.md)
- [Gemini](./docs/GEMINI.md)

## Integrações de pesquisa

O núcleo não depende de marcas específicas. Ele procura capacidades:

- **armazenamento persistente** — workspace, PDFs, documentos, matrizes, exports e manuscrito;
- **descoberta acadêmica** — calibração de termos, auditoria de novidade e literatura próxima;
- **contexto/grafo de citação** — verificação bibliográfica e apoio à leitura quando disponível;
- **web/editoras/repositórios/fontes oficiais** — metadados, full text legal, normas e instruções;
- **bases indexadas** — busca bibliográfica estruturada e reproduzível;
- **execução local** — scaffolding, validação e deduplicação determinística.

No ChatGPT, a configuração preferencial declara Google Drive, Consensus, Scite e Firecrawl em `agents/openai.yaml`. Em outras plataformas, a Skill mapeia ferramentas equivalentes conforme o que realmente estiver disponível.

Scopus e Web of Science não são tratados como “plugins imaginários”. Quando não há conector direto, a Skill prepara a busca, orienta a execução/autenticação, especifica o export e depois valida e processa o arquivo recebido.

## Workspace canônico persistente

Google Drive é o backend canônico padrão. A Skill deve tentar e verificar sua conexão antes de qualquer trabalho substantivo. Se a conexão não existir, deve orientar a configuração e verificar novamente. Apenas se o Drive continuar indisponível e o usuário confirmar explicitamente que quer prosseguir sem ele, a Skill pode usar `WORK_FALLBACK`/armazenamento local. Resultados do Work não substituem silenciosamente o Drive.

Quando o Drive está conectado, a Skill cria ou retoma uma estrutura como esta:

```text
ARTIGO_<titulo>_<ano>/
├── 00_Gestao_e_Continuidade/
│   ├── CONTINUIDADE.md
│   ├── PROTOCOLO.md
│   ├── PROJECT_CONFIG.json
│   └── MATRIZ_MESTRA_<titulo>
├── 01_Auditoria_de_Novidade/
│   ├── Notas_de_Auditoria/
│   └── Artigos_Semente/
├── 02_Buscas_e_Exports/
│   ├── Scopus/
│   ├── Web_of_Science/
│   ├── Outras_Bases/
│   └── Snapshots/
├── 03_Screening_e_FullText/
│   ├── FullText_Corpus/
│   ├── Pendentes_de_Acesso/
│   └── Excluidos_com_Justificativa/
├── 04_Evidencias_e_Sintese/
│   ├── Notas_de_Sintese/
│   ├── Figuras_e_Modelos/
│   └── Claims_Ledger/
├── 05_Manuscrito/
│   ├── Rascunhos/
│   └── Versao_Canonica/
├── 06_Submissao/
│   ├── Regras_da_Revista/
│   ├── Arquivos_Finais/
│   └── Comprovantes/
└── 99_Arquivo_Historico/
```

O chat não é a fonte de verdade do projeto. O workspace persistente é. No fluxo normal, esse workspace é o Google Drive.

## Matriz-mestra

A Skill cria uma planilha-mestra com abas lógicas para:

- `00_Projeto`
- `01_Protocolo`
- `02_Search_Log`
- `03_Screening`
- `04_FullText_Tracker`
- `05_Evidence_Matrix`
- `06_Journal_Dialogue`
- `07_Normative_Corpus`
- `08_Synthesis_Log`
- `09_Claims_Ledger`
- `10_Submission_Checklist`
- `11_CADA_Control`
- `12_PM_Sync`
- `13_Traceability_Log`
- `14_AI_Use_Log`
- `15_CADA_Dashboard`
- `16_INTEROPERABILIDADE`
- `17_DECISOES`
- `18_VALIDACOES`
- `19_SNAPSHOTS`
- `20_MAPA_CORPUS`

Essas tabelas separam descoberta, decisão metodológica, evidência e redação. Também permitem reconstruir de onde vieram as contagens e afirmações utilizadas no manuscrito.

## `CONTINUIDADE.md`

O `CONTINUIDADE.md` funciona como a memória operacional do artigo. Toda sessão retomada deve lê-lo primeiro.

Ele registra, entre outros pontos:

- entrada original do usuário;
- pergunta e objetivo atuais;
- desenho metodológico;
- decisões congeladas;
- status das integrações;
- links canônicos do Drive;
- famílias e versões de busca;
- contagens de registros;
- rodadas inválidas ou substituídas;
- estado da deduplicação e do screening;
- full texts obtidos e pendentes;
- estado da matriz de evidências;
- síntese em andamento;
- estado do manuscrito;
- pendências de revista/submissão;
- bloqueios;
- **próxima ação válida**.

Assim, outro chat ou agente consegue continuar o projeto sem depender do histórico da conversa anterior.

## Revisão integrativa não é automaticamente revisão sistemática

A Skill diferencia o desenho metodológico antes de rotular o artigo.

Uma revisão com busca estruturada, strings reproduzíveis, deduplicação e screening pode continuar sendo **integrativa** quando o objetivo é integrar literatura heterogênea e construir/refinar conceitos, mecanismos, proposições, modelos ou frameworks.

A Skill só utiliza o rótulo **revisão sistemática** quando o projeto atende às exigências metodológicas correspondentes. Para artigos empíricos, ela pode organizar a auditoria de novidade, literatura, evidências e manuscrito, mas não inventa desenho amostral, coleta, análise ou resultados.

## Princípios de segurança científica

A Skill deve:

- preservar a entrada original do pesquisador;
- não inventar acesso a bases;
- não inventar artigos ou citações;
- não alegar leitura integral quando só teve acesso ao resumo;
- não inventar números de registros;
- nunca alterar silenciosamente uma string de busca já executada;
- preservar exports brutos;
- registrar rodadas inválidas em vez de apagá-las;
- separar literatura `[L]`, inferência analítica `[I]` e proposição original `[P]`;
- não remover near-duplicates apenas por similaridade automática;
- não tratar falta de acesso ao full text como critério científico de exclusão;
- não apresentar amostragem teórica/intencional como se todos os candidatos tivessem sido avaliados em full text;
- escrever afirmações importantes somente quando houver evidência rastreável ou indicação explícita de contribuição original.

## Estrutura do repositório

```text
MeuArtigoSkill/
├── README.md
├── VERSION
├── CHANGELOG.md
├── CITATION.cff
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   └── ... documentação operacional da Skill
├── scripts/
│   └── ... automações determinísticas
├── docs/
│   └── ... guias de uso e distribuição
└── .github/
    └── workflows/
        └── release-audit.yml
```

## Instalação

Se você nunca usou GitHub, comece pelo [guia para iniciantes](./docs/COMECE-AQUI.md).

A Skill instalável está na **raiz do repositório**: `SKILL.md`, `references/`, `scripts/` e `agents/` formam um único bundle.

**Para o ChatGPT, o método validado neste projeto é importar diretamente o ZIP completo baixado em `Code → Download ZIP`.** No teste de 07/10/2026, essa forma preservou corretamente os arquivos auxiliares da Skill; tentativas de reconstruir ou selecionar apenas parte do pacote resultaram em importação incompleta.

### ChatGPT / Codex

Siga [docs/CHATGPT.md](./docs/CHATGPT.md). O adapter OpenAI está em `agents/openai.yaml`.

### Claude

Siga [docs/CLAUDE.md](./docs/CLAUDE.md). O mesmo `SKILL.md`, referências e scripts constituem o núcleo portável; MCPs e ferramentas são mapeados conforme a instalação do Claude.

### Gemini

Siga [docs/GEMINI.md](./docs/GEMINI.md). Envie a pasta raiz do projeto ou um ZIP em que `SKILL.md` esteja na raiz da Skill.

### Prompt inicial

> “Use a Skill Meu Artigo. Meu problema de pesquisa é: [descreva o problema]. Quero desenvolver um artigo científico, acompanhar o passo a passo pelo C.A.D.A. e ainda não defini a revista.”

A própria Skill deve verificar as capacidades disponíveis, orientar conexões quando a plataforma permitir, criar o workspace e **começar a pesquisa**, não apenas explicar o método.

## Scripts incluídos

Os scripts são auxiliares determinísticos para etapas frágeis/repetitivas:

- `init_project.py` — cria um espelho local do workspace canônico;
- `dedupe_records.py` — normaliza identificadores e títulos, remove duplicatas exatas e **sinaliza** near-duplicates para revisão;
- `validate_project.py` — verifica a presença e consistência mínima dos artefatos canônicos do projeto;
- `governance_events.py` — registra DEC_ID e validações GATE_ID;
- `create_snapshot.py` / `compare_snapshots.py` — congela e compara estados SNAP_ID;
- `generate_transparency_report.py` — gera a visão de transparência para revisor/editor;
- `build_corpus_map.py` — gera o mapa exploratório do corpus usando somente metadados reais disponíveis;
- `export_provenance.py` / `validate_provenance_package.py` — gera e valida o pacote W3C PROV/RO-Crate;
- `release_audit.py` — audita estrutura, versão, sintaxe e consistência antes de uma release.

Eles não substituem julgamento científico.

## Idioma

O nome e a documentação principal estão em português, mas a Skill deve responder no idioma do usuário e adaptar estratégias de busca às línguas relevantes para o campo científico.

## Sugestões e relatos de uso

O repositório não contém formulário de percepção, escala de avaliação, amostra de participantes ou protocolo de coleta de dados com usuários.

Comentários externos são tratados apenas como sugestões espontâneas de desenvolvimento, relatos de erro ou críticas metodológicas livres. Eles não fazem parte de um instrumento padronizado de pesquisa.

Qualquer eventual estudo científico com participantes deverá ser planejado separadamente do funcionamento da Skill e seguir, antes de qualquer coleta, as exigências éticas e institucionais aplicáveis.

## Estado do projeto

Esta é uma Skill de pesquisa em evolução, atualmente em `0.7.0-beta.1`. Seu objetivo é transformar o uso de IA na escrita científica de uma sequência de conversas isoladas em um **pipeline de pesquisa auditável, persistente, retomável e portável entre agentes**.
