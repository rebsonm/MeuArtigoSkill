# Matriz C.A.D.A. — template oficial do Meu Artigo

A planilha é o **modo padrão de gestão** do Meu Artigo.

O pesquisador não precisa conhecer Jira, ClickUp, Trello ou qualquer outra ferramenta de gestão.

## O que a planilha responde

A primeira aba, `00_PAINEL`, foi desenhada para responder rapidamente:

- Onde estamos?
- O que falta?
- O que faço agora?
- O que está bloqueado?
- Qual é o prazo?
- Como chegamos até aqui?
- Qual evidência sustenta esta afirmação?
- Onde a IA participou?
- Como essa participação foi validada?

## As 20 abas

| Aba | Função |
|---|---|
| `00_PAINEL` | cockpit de governança científica |
| `01_CADA` | tarefas, responsáveis, próxima ação, prazo, status e evidências |
| `02_LINHA_TEMPO` | rastreabilidade cronológica do processo |
| `03_PROJETO` | identidade científica do projeto |
| `04_EVIDENCIAS` | mapa sintético de evidências |
| `05_PROTOCOLO` | decisões metodológicas versionadas |
| `06_BUSCAS` | strings, filtros, contagens e exports |
| `07_SCREENING` | seleção e justificativas |
| `08_FULL_TEXT` | acesso e decisão de textos completos |
| `09_MATRIZ_EVID` | extração detalhada de evidências |
| `10_SINTESE` | padrões, contradições, limites e inferências |
| `11_CLAIMS` | afirmações do manuscrito ligadas às evidências |
| `12_USO_IA` | ferramenta/modelo, finalidade e validação humana |
| `13_SUBMISSAO` | requisitos e comprovantes |
| `14_PM_SYNC` | sincronização opcional com gerenciador externo |
| `15_CONFIG` | vocabulários e parâmetros |
| `16_INTEROPERABILIDADE` | exports W3C PROV/RO-Crate, SHA-256 e validação |
| `17_DECISOES` | decisões científicas materiais, alternativas e justificativas |
| `18_VALIDACOES` | gates de validação humana em transições críticas |
| `19_SNAPSHOTS` | estados congelados e comparáveis do projeto |

## Dois modos

### MATRIX_ONLY

É o padrão.

A planilha é suficiente para gerir todo o projeto.

### MATRIX_PLUS_EXTERNAL

A planilha continua sendo canônica, mas os itens de `01_CADA` também podem ser espelhados em ClickUp, Jira ou Trello.

## Geração automática

Em ambientes com `artifact_tool`, use:

```bash
python scripts/build_matrix_template.py \
  --output MATRIZ_MESTRA_meu-projeto.xlsx \
  --project-name "Meu projeto" \
  --problem "Meu problema de pesquisa"
```

O `scripts/init_project.py` tenta executar esse gerador automaticamente.

Se o ambiente não tiver `artifact_tool`, a IA deve reproduzir a mesma estrutura em uma planilha nativa usando:

`references/spreadsheet-template.md`

Quando nenhuma ferramenta visual de planilha existir, os CSVs do workspace são o modo de compatibilidade final.

## Fonte de verdade

A planilha organiza e conecta o processo, mas cada tipo de registro possui seu papel:

- `01_CADA`: gestão;
- `02_LINHA_TEMPO`: processo/proveniência;
- `05_PROTOCOLO`: decisões metodológicas;
- `06_BUSCAS`: execução bibliográfica;
- `09_MATRIZ_EVID`: evidência;
- `11_CLAIMS`: argumento do manuscrito;
- `12_USO_IA`: transparência sobre IA.

O dashboard é derivado dessas abas e nunca deve substituir os registros canônicos.

## Princípio

A planilha não foi desenhada apenas para controlar tarefas.

Ela combina:

**gestão + evidência + proveniência + transparência de IA + continuidade**

Esse é o papel da matriz no Meu Artigo.


## Exportação auditável

A aba `16_INTEROPERABILIDADE` registra cada pacote gerado pela Skill.

O pacote contém:

- `ro-crate-metadata.json` — RO-Crate 1.3;
- `provenance/prov.jsonld` — grafo W3C PROV-O;
- `manifest-sha256.txt` — fixidade dos arquivos;
- relatório de proveniência;
- artefatos canônicos do projeto.

A exportação pode ser feita com:

```bash
python scripts/export_provenance.py /caminho/do/projeto
python scripts/validate_provenance_package.py /caminho/do/pacote.zip
```


## Governança sem burocratizar

As novas abas não criam mais trabalho cotidiano:

- `17_DECISOES` só recebe decisões materialmente científicas;
- `18_VALIDACOES` contém apenas sete gates padrão;
- `19_SNAPSHOTS` registra estados congelados, não cada edição.

O pesquisador continua usando principalmente `00_PAINEL`, `01_CADA` e as abas científicas da etapa atual.
