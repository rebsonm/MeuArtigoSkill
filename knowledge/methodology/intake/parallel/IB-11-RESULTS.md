# IB-11/20 — Recibo auditável da conferência documental

- **Data:** 21/11/2026 (America/Fortaleza)
- **Branch exclusiva:** `work/ib-11-20261121`
- **Snapshot de partida:** `c5e0ca9abd98f824f1576c3ad94c6e9a5d18e9bf`
- **Commit das 17 fichas:** `ba4a425aa160e7e8d0a23726cbae06ad91d12e38`
- **Escopo:** 17/17 PDFs localizados no Drive privado por ID, nome e tamanho do ledger; 15 identidades documentais verificadas; 2 bloqueadas: **SRC-0297** (data não consta dos slides) e **SRC-0314** (ano/edição do livro ausentes no capítulo).
- **Direitos:** 0304 CC BY 4.0; 0309 CC BY-NC 3.0; 0307 reprodução com citação e vedação comercial; 0299, 0305 e 0313 possuem restrições editoriais expressas. Os demais não trazem licença suficiente para concluir redistribuição; **zero PDFs publicados**.
- **Divergências:** títulos do catálogo global invertidos para 0312 (PDF JSS Synth 2011) e 0313 (PDF JASA Tobacco 2010); nome de 0303 diz 2015, mas documento publicado em 2018; 0301 é monografia, 0311 e 0314 são capítulos autorais.
- **Originais inspecionados:** exclusivamente os 17 PDFs deste lote (capa, resumo/sumário, expediente e licenças observáveis); não se atribuiu verificação da ciência contida nos textos.
- **Arquivos criados/alterados:** 17 fichas `knowledge/methodology/source_cards/src-XXXX.md` de IB-11, `knowledge/methodology/intake/parallel/IB-11-RESULTS.md` e `IB-11-DELTA.json`. Catálogo global, ledger, manifestos, testes globais, main e PR #101 ficaram intactos.
- **Testes documentais:** unicidade 17/17, 17 hashes SHA-256 das fichas, 17 Drive IDs, consistência com ledger; CI GitHub remota a verificar no HEAD. Nenhuma aprovação [L] ou gate científico.
- **Pendências:** obter documentação primária de ano/edição de 0297 e 0314; esclarecer permissões e terceiros; integração sequencial posterior dos 17 cartões e correção de inversão no catálogo sob coordenação; revisão científica separada.
- **Proibições respeitadas:** sem merge, release, tag, MCP ou publicação de PDF protegido.

| ID | Estado | Título do PDF | Direitos resumidos |
|---|---|---|---|
| SRC-0296 | verificado | Conducting Configurational Comparative Research With Qualitative Comparative Analysis: A Hands-On Tutorial for Applied Evaluation Scholars and Practitioners | © The Author(s) 2016; autorização SAGE necessária; licença aberta não observada |
| SRC-0297 | bloqueado | Qualitative Comparative Analysis (QCA): Aula 1 — Introdução ao método | licença não observada; imagens/citações de terceiros não liberadas |
| SRC-0299 | verificado | Introduction to Monte Carlo simulation | © 2008 IEEE; uso institucional limitado; restrições expressas |
| SRC-0300 | verificado | Simulações de Monte Carlo no ensino de Ciência Política | licença de redistribuição não identificada nesta cópia |
| SRC-0301 | verificado | Método de Monte Carlo e Aplicações | licença expressa de redistribuição não identificada |
| SRC-0302 | verificado | Networks in Political Science: Back to the Future | Cambridge University Press; licença aberta não observada |
| SRC-0303 | verificado | Social Network Analysis as a research method in political science. An attempt to use it in coalition research | licença aberta não observada |
| SRC-0304 | verificado | Análise de redes sociais: o método e sua utilização nas Ciências Sociais brasileiras | CC BY 4.0 declarada na cópia; atribuição obrigatória e atenção a terceiros |
| SRC-0305 | verificado | Network Analysis and Political Science | © 2011 Annual Reviews, all rights reserved; for personal use only |
| SRC-0306 | verificado | Ciência política e análise de redes: uma metodologia para o mapeamento de comunidades temáticas | licença expressa não identificada na cópia |
| SRC-0307 | verificado | Análise de Redes em Ciências Sociais | © 2018 Enap; reprodução permitida com citação, vedado fim comercial |
| SRC-0308 | verificado | Introdução à análise de redes sociais online | direitos desta edição cedidos à Edufba; autorização de redistribuição não observada |
| SRC-0309 | verificado | What is social network analysis? | © John Scott 2012; CC BY-NC 3.0, atribuição e uso não comercial |
| SRC-0311 | verificado | Metodologia de Análise de Redes Sociais | licença de redistribuição não identificada |
| SRC-0312 | verificado | Synth: An R Package for Synthetic Control Methods in Comparative Case Studies | licença expressa de redistribuição não observada |
| SRC-0313 | verificado | Synthetic Control Methods for Comparative Case Studies: Estimating the Effect of California's Tobacco Control Program | Taylor & Francis; termos de acesso institucional, sem licença aberta observada |
| SRC-0314 | bloqueado | CONTROLE SINTÉTICO COMO FERRAMENTA PARA AVALIAÇÃO DE POLÍTICAS PÚBLICAS | expediente/licença da edição geral ausentes; não autorizar PDF |

O DELTA contém todos os campos de auditoria por registro, incluindo arquivo, pasta, tamanho, localizador privado, autores, DOI/ISBN, tipologia, escopo, direitos, hashes e commit de fichas.
