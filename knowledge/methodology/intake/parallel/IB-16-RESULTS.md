# IB-16/20 — Resultado e rastreabilidade documental

**Data:** 21/11/2026 (America/Fortaleza). **Branch isolada:** `work/ib-16-20261121`, iniciada em `c5e0ca9abd98f824f1576c3ad94c6e9a5d18e9bf`.

- PDFs fechados no escopo e localizados no Drive por pasta/nome/tamanho: **17/17**.
- Identidades da versão efetivamente examinada: **16/17 verificadas**. **SRC-0403 BLOQUEADO** (impressão de capítulo web sem autoria, edição e data de publicação demonstradas na cópia).
- **17 fichas [P] atualizadas** em `knowledge/methodology/source_cards/`; todas seguem sem revisão científica independente [L], sem reprodução integral de terceiros.
- **Direitos observados:** `SRC-0405` CC BY 4.0 expressa; `SRC-0389` CC Attribution sem versão especificada; `SRC-0388`/`SRC-0402` indicam Creative Commons sem especificação da modalidade; demais versões com reserva de direitos, termos de reimpressão ou ausência de licença explícita. Nenhum PDF publicado.
- **Metadados divergentes do nome:** `SRC-0392` Small(2012) é publicação 2011; `SRC-0393` Rezende(2016) é edição 2014; `SRC-0398` Owens(2022) é apresentação de 2002 com overlay ResearchGate 2014; `SRC-0399` Lietz(2009) é periódico 2010, DOI verificado visualmente.
- **Múltiplas cópias:** `SRC-0391` e `SRC-0402` têm homônimos de mesmo tamanho em pastas distintas. Somente cópias das pastas atribuídas examinadas; duplicidade intelectual/hash entre diferentes IDs precisa de reconciliação pela integração, sem contabilizar nova obra automaticamente.
- **Pendências:** autenticar autoria/data/edição de `SRC-0403`; conferir o DOI de `SRC-0394`, agora visualmente confirmado como `10.17666/3088115-128/2015` após sanar erro de extração; resolver modalidades de Creative Commons, direitos de terceiros, duplicidades e revisão científica posterior.
- **Controle técnico:** ficha SHA-256 individual no JSON `IB-16-DELTA.json`; documento-fonte por ID do Drive e tamanho do ledger; arquivo da branch recebe `commit_da_branch` anterior ao recibo por impossibilidade de hash autorreferencial.
- **Sem alteração de** source_registry_catalog.json, rights-ledger-part-04.json, manifestos, catálogo de PDFs, snapshots, testes globais, main ou PR #101; sem merge/tag/release/MCP/publicação de PDFs.
- **CI:** não afirmado/apurado pelo recibo. Consultar status do HEAD e registrar no MD canônico.

## Matriz de conferência

| ID | PDF original | Edição comprovada | DOI observado | Direitos | Resultado |
|---|---|---|---|---|---|
| SRC-0388 | Figueiredo Filho et al (2023).pdf | 2023 | 10.17666/bib9906/2023 | CC genérica observada, modalidade e versão não verificadas | VERIFICADO |
| SRC-0389 | Schaefer e Figueiredo Filho (2023).pdf | 2023 | 10.1590/3811039/2023 | Creative Commons Attribution observada, versão não definida | VERIFICADO |
| SRC-0390 | King e Nielsen (2019).pdf | 2019 | 10.1017/pan.2019.11 | © 2019 autores, Cambridge CUP; sem CC expressa observada | VERIFICADO |
| SRC-0391 | Imai, Kim e Wang (2023).pdf | 2023 (©2021) | 10.1111/ajps.12685 | © 2021 Midwest Political Science Association; sem CC expressa | VERIFICADO |
| SRC-0392 | Small(2012).pdf | 2011 | 10.1146/annurev.soc.012809.102657 | © 2011 Annual Reviews; All rights reserved | VERIFICADO |
| SRC-0393 | Rezende (2016).pdf | 2014 | não confirmado | nenhuma licença CC expressa no expediente consultado | VERIFICADO |
| SRC-0394 | Silva (2015).pdf | 2015 | 10.17666/3088115-128/2015 | sem licença CC expressa; DOI no PDF com paginação concatenada | VERIFICADO |
| SRC-0395 | Paranhos et al (2016).pdf | 2016 | 10.1590/15174522-018004221 | sem CC expressa observada | VERIFICADO |
| SRC-0396 | Paranhos et al (2013).pdf | 2013 (ed. 2013–2014) | não confirmado | sem licença CC expressa observada | VERIFICADO |
| SRC-0398 | Owens (2022).pdf | 2002 (capa ResearchGate 2014) | não confirmado | sem licença expressa; ResearchGate não prova permissão | VERIFICADO |
| SRC-0399 | Lietz (2009).pdf | 2010 (recebido 2009) | 10.2501/S147078530920120X | © 2010 The Market Research Society; sem CC expressa | VERIFICADO |
| SRC-0400 | Tourangeau (2017).pdf | 2017 | 10.1108/QAE-06-2017-0034 | © Emerald Publishing Limited, regras de reimpressão | VERIFICADO |
| SRC-0402 | Figueiredo Filho et al (2021).pdf | 2021 (©2020) | 10.17666/bib9402/2021 | CC observada sem modalidade e versão específicas | VERIFICADO |
| SRC-0403 | Chapter 7 Clustering Analysis _ An R Companion for Introduction to Data Mining.pdf | impressão 14/12/2023, edição não identificada | não confirmado | nenhum aviso de licença explícita na cópia | BLOQUEADO |
| SRC-0404 | Figueiredo Filho, Silva Junior e Rocha (2012).pdf | 2012 | não confirmado | sem licença CC expressa observada | VERIFICADO |
| SRC-0405 | Figueiredo Fiho et al (2014).pdf | 2014 | 10.4236/am.2014.515232 | CC BY 4.0 expressa na primeira página | VERIFICADO |
| SRC-0406 | Lins (2020)_slides.pdf | 2020 | não confirmado | sem licença expressa observada | VERIFICADO |

## Próximos passos para integração

1. Manter a branch `work/ib-16-20261121` isolada; o integrador deverá importar a alteração sequencialmente, testar e reconciliar índices/hashes/totais globais sem tocar outras etapas.
2. `SRC-0403`: obter documento de crédito/autoria e versão inequívocos; não inferir a autoria do domínio da URL.
3. Rever `SRC-0394` DOI na cópia visual; `SRC-0391`/`SRC-0402` hashes entre homônimos e possível repetição de obra.
4. Verificar condições legais de Creative Commons/elementos de terceiros e review independente dos 17 cards [P].
