# Meu Artigo — Skill para pesquisa e construção de artigos científicos

**Meu Artigo** é uma Skill **multiplataforma** para pesquisa e construção de artigos científicos. Ela transforma um problema, pergunta ou ideia de pesquisa fornecida pelo usuário em um **processo científico rastreável, persistente, orientado por evidências e auditável quanto à sua própria construção**. O núcleo metodológico vive em `meu-artigo/SKILL.md`; diferenças entre ChatGPT, Claude e Gemini ficam isoladas em adapters/documentação de plataforma.

Ela não entrega um “artigo pronto por mágica” e não reutiliza o conteúdo de um projeto anterior. O que a Skill reutiliza é um **método de trabalho**: organização do projeto, auditoria de novidade, protocolo, buscas bibliográficas, registro das decisões, deduplicação, screening, full text, matriz de evidências, síntese, redação e auditoria final. Todo esse fluxo é acompanhado por uma camada de gestão **C.A.D.A.**, para tornar o passo a passo visível e rastreável.

> O tema, a pergunta de pesquisa, os conceitos, as strings de busca, as fontes, as categorias analíticas e as conclusões pertencem sempre ao projeto do novo usuário.

## 🚀 Nunca usou GitHub? Comece aqui

Você **não precisa saber Git, programação nem terminal** para testar o Meu Artigo.

Se esta é sua primeira vez no GitHub, abra o guia:

### 👉 [COMECE AQUI — passo a passo para quem nunca usou GitHub](./docs/COMECE-AQUI.md)

O caminho básico é:

```text
GitHub → botão Code → Download ZIP → descompactar
       → abrir a pasta meu-artigo/
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
| **ChatGPT** | Skills nativas aparecem em contas/workspaces elegíveis; a documentação atual cita Business, Enterprise, Healthcare e Edu. |
| **Claude.ai** | Skills personalizadas podem ser enviadas em planos Pro, Max, Team e Enterprise quando a execução de código está habilitada. |
| **Gemini** | Skills dependem dos requisitos atuais da conta/assinatura Google; confira o guia antes do teste. |

Se o menu de Skills não aparecer, abra o guia da plataforma antes de concluir que houve erro no repositório.

## O que a Skill faz

A Skill conduz o pesquisador por um fluxo completo:

1. recebe o problema, pergunta, fenômeno ou ideia de artigo do usuário;
2. verifica as integrações de pesquisa disponíveis e orienta a conexão das que estiverem faltando;
3. cria um workspace persistente e padronizado — com Google Drive como implementação de referência;
4. registra o problema original e cria `CONTINUIDADE.md`, protocolo e matriz-mestra;
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
24. registra usos materiais de IA, finalidade, ferramenta/modelo quando conhecido e validação humana.

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
- `15_CADA_Dashboard` — visão resumida do andamento.

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

A planilha que gerencia o projeto tem agora um **template canônico de 16 abas**, com dashboard, C.A.D.A., linha do tempo, protocolo, buscas, screening, full text, matriz de evidências, síntese, claims, uso de IA, submissão e sincronização opcional.

O modo padrão é `MATRIX_ONLY`: a pessoa consegue conduzir todo o projeto sem conhecer software de gestão.

A Skill deve tentar criar essa matriz **antes das buscas em escala**:

1. como planilha nativa quando houver integração de planilhas;
2. pelo gerador oficial `scripts/build_matrix_template.py` quando `artifact_tool` estiver disponível;
3. pelos CSVs somente como compatibilidade final.

Documentação: [docs/MATRIZ-CADA.md](./docs/MATRIZ-CADA.md)

Especificação técnica: [meu-artigo/references/spreadsheet-template.md](./meu-artigo/references/spreadsheet-template.md)

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

Essa preocupação é consistente com diretrizes editoriais recentes. A Revista de Ciências da Administração, por exemplo, determina que usos substantivos de IA sejam descritos nos métodos e que ferramenta, versão, finalidade e procedimentos de validação humana sejam explicitados para assegurar rastreabilidade. Ricardo Limongi também possui trabalhos publicados sobre IA, integridade científica e transparência algorítmica.

Veja [docs/RASTREABILIDADE.md](./docs/RASTREABILIDADE.md).

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
| `meu-artigo/SKILL.md` | Sim | Metodologia e workflow científico |
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
- [Protocolo de teste com usuários](./docs/TESTE-DE-USABILIDADE.md)

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

Google Drive é a implementação de referência. Quando ele está conectado, a Skill cria ou retoma uma estrutura como esta. Em outra plataforma, um armazenamento persistente equivalente pode reproduzir a mesma estrutura lógica:

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

O chat não é a fonte de verdade do projeto. O **workspace persistente** é.

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
├── docs/
│   ├── COMECE-AQUI.md
│   ├── CADA.md
│   ├── MATRIZ-CADA.md
│   ├── RASTREABILIDADE.md
│   ├── CHATGPT.md
│   ├── CLAUDE.md
│   ├── GEMINI.md
│   └── TESTE-DE-USABILIDADE.md
└── meu-artigo/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    ├── references/
    │   ├── beginner-mode.md
    │   ├── drive-workspace.md
    │   ├── evidence-synthesis.md
    │   ├── plugin-onboarding.md
    │   ├── project-state.md
    │   ├── review-design.md
    │   ├── search-screening.md
    │   └── tool-orchestration.md
    └── scripts/
        ├── dedupe_records.py
        ├── init_project.py
        └── validate_project.py
```

## Instalação

Se você nunca usou GitHub, comece pelo [guia para iniciantes](./docs/COMECE-AQUI.md).

A Skill instalável está na pasta [`meu-artigo`](./meu-artigo/).

### ChatGPT / Codex

Siga [docs/CHATGPT.md](./docs/CHATGPT.md). O adapter OpenAI está em `meu-artigo/agents/openai.yaml`.

### Claude

Siga [docs/CLAUDE.md](./docs/CLAUDE.md). O mesmo `SKILL.md`, referências e scripts constituem o núcleo portável; MCPs e ferramentas são mapeados conforme a instalação do Claude.

### Gemini

Siga [docs/GEMINI.md](./docs/GEMINI.md). Envie a pasta `meu-artigo/` ou um ZIP em que `SKILL.md` esteja na raiz da Skill.

### Prompt inicial

> “Use a Skill Meu Artigo. Meu problema de pesquisa é: [descreva o problema]. Quero desenvolver um artigo científico, acompanhar o passo a passo pelo C.A.D.A. e ainda não defini a revista.”

A própria Skill deve verificar as capacidades disponíveis, orientar conexões quando a plataforma permitir, criar o workspace e **começar a pesquisa**, não apenas explicar o método.

## Scripts incluídos

Os scripts são auxiliares determinísticos para etapas frágeis/repetitivas:

- `init_project.py` — cria um espelho local do workspace canônico;
- `dedupe_records.py` — normaliza identificadores e títulos, remove duplicatas exatas e **sinaliza** near-duplicates para revisão;
- `validate_project.py` — verifica a presença e consistência mínima dos artefatos canônicos do projeto.

Eles não substituem julgamento científico.

## Idioma

O nome e a documentação principal estão em português, mas a Skill deve responder no idioma do usuário e adaptar estratégias de busca às línguas relevantes para o campo científico.

## Testes com usuários

Para testar a Skill com pessoas que não participaram do desenvolvimento, use [docs/TESTE-DE-USABILIDADE.md](./docs/TESTE-DE-USABILIDADE.md).

O protocolo inclui:

- teste cego de onboarding;
- teste de busca;
- teste obrigatório de retomada em nova conversa;
- comparação entre plataformas;
- critérios de falha crítica;
- ficha mínima de registro;
- classificação do feedback em CORE, ADAPTER, UX e TOOLING.

## Estado do projeto

Esta é uma Skill de pesquisa em evolução. Seu objetivo é transformar o uso de IA na escrita científica de uma sequência de conversas isoladas em um **pipeline de pesquisa auditável, persistente, retomável e portável entre agentes**.
