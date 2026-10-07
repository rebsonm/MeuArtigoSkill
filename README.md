# Meu Artigo — Skill para pesquisa e construção de artigos científicos

**Meu Artigo** é uma Skill **multiplataforma** para pesquisa e construção de artigos científicos. Ela transforma um problema, pergunta ou ideia de pesquisa fornecida pelo usuário em um **processo científico rastreável, persistente e orientado por evidências**. O núcleo metodológico vive em `meu-artigo/SKILL.md`; diferenças entre ChatGPT, Claude e Gemini ficam isoladas em adapters/documentação de plataforma.

Ela não entrega um “artigo pronto por mágica” e não reutiliza o conteúdo de um projeto anterior. O que a Skill reutiliza é um **método de trabalho**: organização do projeto, auditoria de novidade, protocolo, buscas bibliográficas, registro das decisões, deduplicação, screening, full text, matriz de evidências, síntese, redação e auditoria final.

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

## O que a Skill faz

A Skill conduz o pesquisador por um fluxo completo:

1. recebe o problema, pergunta, fenômeno ou ideia de artigo do usuário;
2. verifica as integrações de pesquisa disponíveis e orienta a conexão das que estiverem faltando;
3. cria um workspace persistente e padronizado no Google Drive;
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
19. mantém o projeto retomável por outro chat ou agente sem depender da memória da conversa.

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

> “Use a Skill Meu Artigo. Meu problema de pesquisa é: [descreva o problema]. Quero desenvolver um artigo científico e ainda não defini a revista.”

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
