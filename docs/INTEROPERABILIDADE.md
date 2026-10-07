# Interoperabilidade — W3C PROV, RO-Crate e SHA-256

## O que isso muda para quem usa o Meu Artigo?

Quase nada na rotina.

O pesquisador continua trabalhando com:

- Painel;
- C.A.D.A.;
- linha do tempo;
- protocolo;
- buscas;
- evidências;
- claims;
- registro de uso de IA.

A interoperabilidade aparece quando o projeto precisa ser **auditado, preservado, compartilhado ou submetido**.

A Skill pode então gerar um pacote padronizado.

## O pacote auditável

Exemplo:

```text
RO_CRATE_meu-projeto_20261007T030000Z/
├── ro-crate-metadata.json
├── manifest-sha256.txt
├── provenance/
│   ├── prov.jsonld
│   ├── provenance-report.json
│   └── PROVENANCE_REPORT.md
└── payload/
    ├── 00_Gestao_e_Continuidade/
    │   ├── CONTINUIDADE.md
    │   ├── PROTOCOLO.md
    │   ├── RASTREABILIDADE.md
    │   ├── MATRIZ_MESTRA_*.xlsx
    │   └── logs e matrizes
    ├── 05_Manuscrito/
    └── 06_Submissao/
```

Por padrão, o corpus de full text não é incluído, porque pode conter arquivos protegidos por licença ou direitos autorais.

## W3C PROV-O

O W3C PROV é usado para expressar proveniência de forma interoperável.

No Meu Artigo:

| Meu Artigo | PROV |
|---|---|
| CADA_ID | contexto/plano |
| TRACE_ID | Activity |
| Search_ID | Activity |
| Record_ID | Entity |
| Evidence_ID | Entity |
| Claim_ID | Entity |
| pesquisador | Agent |
| IA/script | Agent |

Exemplos de relações:

```text
Claim
   wasDerivedFrom
Evidence

Record
   wasGeneratedBy
Search

Arquivo
   wasGeneratedBy
TRACE activity

TRACE
   wasAssociatedWith
Pesquisador / IA / script
```

Referência oficial:

https://www.w3.org/TR/prov-o/

## RO-Crate 1.3

RO-Crate empacota o objeto de pesquisa e seus metadados em JSON-LD.

O arquivo principal é:

`ro-crate-metadata.json`

O Meu Artigo usa a versão 1.3:

https://w3id.org/ro/crate/1.3

A raiz do pacote é representada como um `Dataset`, e os arquivos são relacionados por `hasPart`.

O arquivo W3C PROV fica dentro do próprio RO-Crate.

## SHA-256

O pacote também inclui:

`manifest-sha256.txt`

Cada arquivo recebe um hash SHA-256.

Se qualquer byte do arquivo mudar, o hash muda.

Isso permite verificar **fixidade**: se o pacote continua exatamente igual ao que foi exportado.

Fixidade não prova que a pesquisa está correta. Ela apenas ajuda a demonstrar que os arquivos não foram alterados desde a geração do manifesto.

## Relatório de proveniência

A exportação produz um relatório com:

- quantidade de TRACE events;
- número de entidades PROV;
- atividades PROV;
- agentes PROV;
- arquivos no RO-Crate;
- claims sem Evidence_ID;
- C.A.D.A. concluído sem evidência de conclusão;
- uso substantivo de IA aguardando validação humana;
- busca executada sem string literal;
- outros gaps detectados.

## Registro na planilha

A planilha possui a aba:

`16_INTEROPERABILIDADE`

Cada export recebe um ID:

`EXPORT-0001`

E registra:

- data/hora;
- padrões;
- caminho/URL;
- SHA-256 do pacote;
- status da validação;
- contagens do PROV;
- quantidade de arquivos do RO-Crate;
- warnings.

## Scripts

Gerar:

```bash
python scripts/export_provenance.py /caminho/ARTIGO_projeto_2026
```

Validar:

```bash
python scripts/validate_provenance_package.py /caminho/RO_CRATE_projeto.zip
```

Por padrão, o pacote é salvo em:

`06_Submissao/Arquivos_Finais/`

## Quando gerar?

Não é necessário gerar a cada ação.

Momentos úteis:

- protocolo congelado;
- corpus congelado;
- síntese concluída;
- versão do manuscrito congelada;
- antes da submissão;
- depois da submissão;
- quando revisor/editor solicita transparência;
- quando o pesquisador quer um snapshot auditável.

## O que isso permite afirmar?

Permite afirmar que o projeto possui uma **trilha de proveniência padronizada e intercambiável**.

Não permite afirmar automaticamente que o estudo é:

- válido;
- reproduzível em sentido estrito;
- livre de erros;
- metodologicamente correto.

Essas continuam sendo questões científicas.

## Princípio do Meu Artigo

A interface humana pode continuar simples:

```text
Painel → C.A.D.A. → Rastreabilidade
```

Por baixo:

```text
TRACE / Evidence / Claim
        ↓
     W3C PROV
        ↓
     RO-Crate
        ↓
SHA-256 / pacote auditável
```

A complexidade técnica fica na Skill, não no pesquisador.
