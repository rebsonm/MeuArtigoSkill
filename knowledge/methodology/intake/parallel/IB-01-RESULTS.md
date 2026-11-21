# IB-01/20 — Recibo documental de execução

- **Data:** 21/11/2026. **Branch exclusiva:** `work/ib-01-20261121`; base imutável `c5e0ca9abd98f824f1576c3ad94c6e9a5d18e9bf`.
- **Escopo:** `SRC-0099`–`SRC-0116`, 18/18 PDFs privados localizados no Google Drive (nome, pasta, tamanho) e conferidos quanto a capa/expediente/resumo ou sumário, tipo editorial, identificadores quando visíveis e avisos de direitos.
- **Resultado:** 18/18 identidades documentais registradas em 18 fichas originais [P]. **Não** corresponde a leitura científica integral, validação [L], licença de PDF ou integração ao catálogo global.
- **Direitos:** nenhuma autorização de publicar arquivos PDF foi emitida. `SRC-0100` indica CC BY-NC-ND 4.0 do manuscrito aceito; `SRC-0101` contém cabeçalho CC BY 4.0 e aviso EDIPUCRS restritivo em conflito; obras SAGE, Emerald, Annual Reviews e JSTOR sujeitas a políticas e direitos específicos; livros, capítulos e traduções requerem licença da edição e titulares pertinentes.
- **Divergências:** `SRC-0111` é resenha de 2007 (apesar de nome 2010); `SRC-0103` cabeçalho 17(4) versus rodapé 17(3); `SRC-0108` sem editora/ISBN/paginação final confirmados; `SRC-0113` contém menção a modificação editorial em 2009.
- **Commits:** 18 fichas alteradas em commits próprios, mais correção de `SRC-0111` no commit `9ce3e388110cd74ff92be365a51aaa7e9af3c250`. Recibo `IB-01-DELTA.json` commit `334886e3242205ce0c34fc4568c46d9787adaf50`; ver último HEAD da branch após este recibo.
- **Auditoria de escopo executada:** comparação com o snapshot constatou alteração exclusiva nas 18 fichas da faixa IB-01 antes dos recibos; leitura automatizada verificou presença de [P], metadados e direitos em cada ficha, ausência de binários PDF embutidos e nenhuma promoção automática a [L]. As SHA-256 de cada ficha e respectivos commits estão no DELTA.
- **Integração pendente:** integrador central deve aplicar sequencialmente a branch, atualizar `source_registry_catalog.json`, os cinco ledgers, manifestos, hashes globais e testes da PR #101, sem confundir este recibo com atualização desses arquivos. CI do commit final deve ser verificada e registrada à parte.

## Evidência por documento

| Fonte | Tipo | Edição observada | Alerta prioritário |
|---|---|---|---|
| SRC-0099 | livro organizado | Silva e Stabile (orgs.), 2016 | Direitos: consultar ficha; não há autorização de redistribuição |
| SRC-0100 | artigo / manuscrito aceito | Perriam, Birkbak e Freeman, 2020 | Direitos: consultar ficha; não há autorização de redistribuição |
| SRC-0101 | artigo | Vimieiro e Bargas, 2019 | Conferir qual aviso aplica-se à cópia exata |
| SRC-0102 | artigo de revisão | Hampton, 2017 | Direitos: consultar ficha; não há autorização de redistribuição |
| SRC-0103 | artigo | Marietto, 2018 | Expediente 17(4), rodapés 17(3) |
| SRC-0104 | pré-print de capítulo | Laurier, 2010 | Direitos: consultar ficha; não há autorização de redistribuição |
| SRC-0105 | artigo / manuscrito autor | Mackellar, 2013 | Direitos: consultar ficha; não há autorização de redistribuição |
| SRC-0106 | artigo | Schwartz e Elsen, 2003 | Direitos: consultar ficha; não há autorização de redistribuição |
| SRC-0107 | artigo | Hennell, Limmer e Piacentini, 2020 | Direitos: consultar ficha; não há autorização de redistribuição |
| SRC-0108 | capítulo de livro | Campos, Silva e Albuquerque, 2021 | Editora/ISBN e paginação final pendentes |
| SRC-0109 | capítulo autoral | Fernando Manuel Bessa Fernandes, 2011 | Direitos: consultar ficha; não há autorização de redistribuição |
| SRC-0110 | tradução de texto em periódico | Georges Lapassade; trad. Nildo Viana, 2023 | Direitos: consultar ficha; não há autorização de redistribuição |
| SRC-0111 | resenha | Licia Valladares, 2007 (resenha de Whyte) | Arquivo nomeado 2010; PDF criado 20/06/2007 e referência em SRC-0103 informa 2007 |
| SRC-0112 | artigo | Gillespie e Michelson, 2011 | Volume e última página não confirmados |
| SRC-0113 | artigo | Braga e Nicolás, 2008 | Nota editorial de modificação em abril de 2009 |
| SRC-0114 | artigo traduzido | Rajae Ankoud, trad. Michael Scott, 2020 | Original Ostour 2020; tradução é outra edição |
| SRC-0115 | livro organizado | Flavio M. Heinz (org.), 2011 | Direitos: consultar ficha; não há autorização de redistribuição |
| SRC-0116 | artigo traduzido | Bulst, trad. Cybele C. de Almeida, 2005; original 1986 | Direitos: consultar ficha; não há autorização de redistribuição |

A lista individual de nomes, tamanhos, IDs de Drive, identificadores, direitos, commits e SHA-256 está em `IB-01-DELTA.json`. Nenhuma obra integral foi publicada ou convertida em Markdown.
