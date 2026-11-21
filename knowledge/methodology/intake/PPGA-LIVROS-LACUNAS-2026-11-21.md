# Auditoria de lacunas — biblioteca metodológica PPGA LIVROS, 21/11/2026

**Este documento separa rigorosamente fonte inventariada, identidade confirmada, leitura realizada, licença verificável, card provisório e validação. Não declare a biblioteca científica integralmente validada.**

## Cobertura efetivamente realizada

Foram consultadas no Google Drive as **17 entradas de primeiro nível** da pasta `PPGA - LIVROS`, com inspeção de pastas temáticas relevantes e níveis adicionais: Métodos Qualitativos I/II, Métodos Quantitativos, Working Paper e seus materiais, Estudos Organizacionais, Gestão de Projetos, Teoria e Estratégia, além do arquivo expandido `Adicionais`. O arquivo `Adicionais` contém cerca de 70 pastas temáticas; o inventário metodológico original registra 475 fontes, mas não cobre necessariamente todos os documentos adicionados posteriormente ao Drive. Algumas pastas de radar incluem muitos arquivos e exigem paginação; não foram tratadas como bibliotecas de metodologia a importar.

## Novidades incorporadas nesta frente

- **Marzi et al. (2025):** B-SLR com dez etapas, três checkpoints e distinção de bibliometria, revisão de textos e contribuição teórica. Publicação original CC BY 4.0 e card.
- **Snyder (2019):** escolha entre revisões sistemáticas, semissistemáticas e integrativas. Original no Drive com licença CC BY-NC-ND; somente card independente.
- **Grant & Booth (2009):** tipologia de revisões, abordagem SALSA. Original protegido; card independente.
- **Ângelo Domingos Salvador:** obra de pesquisa bibliográfica localizada em catálogos e discutida por Lima & Mioto (2007); **livro não lido diretamente, nem encontrado pelo título no PPGA**; card [P] com ressalva.
- **Jaakkola (2020):** quatro estratégias de artigos conceituais, PDF original CC BY 4.0 e card.
- **Elsbach e Van Knippenberg; Alvesson e Sandberg:** síntese integrativa e problematização.
- **PRISMA 2020 + PRISMA-S + PRISMA-ScR + PRISMA-P:** cards e template original de 27 pontos/fluxograma, com links oficiais; diretrizes de relato NÃO transformadas em método de revisão.
- **Outras disciplinas PPGA:** Braun/Clarke (análise temática), Miles/Huberman/Saldaña e Saldaña (codificação), Saunders (cebola; o arquivo com nome “Saunders 2017” contém na verdade **edição 2023**), Creswell (desenhos), Yin/Eisenhardt (estudos de caso), Hevner/Peffers (DSR), Suddaby (grounded theory), Sampaio/Sabbatini/Limongi (uso ético de IA).
- **A ampliar futuramente:** Zupic & Čater e Donthu aparecem como referências bibliográficas em Marzi, mas seus originais ainda não foram consultados nesta etapa.

## Diferença entre três camadas de acervo

- **475 fichas bibliográficas [P]:** cobertura registral do inventário original, não 475 resumos de artigos. Destas, 404 têm correspondência de título provisória e 71 continuam com identidade por esclarecer.
- **Cards metodológicos [I]/[P]:** redação original para decisão do pesquisador. São rascunhos e ainda **não** passaram por aceite científico independente com evidência. Quatro cards históricos não têm registro de aceitação; os demais também estão pendentes.
- **PDFs de terceiros distribuídos:** apenas originais com permissão de redistribuição identificada por obra/edição e SHA256. Catálogo de PDFs abertos não deve ser subtraído dos 475 como se cada arquivo correspondesse a um original daquele inventário.

## Pendências objetivas para uma biblioteca cientificamente pronta

1. **Direitos por documento:** 3 dos 475 registros do inventário têm decisão individual no ledger; **472 ainda não foram liberados para redistribuição** por aquela matriz. Alguns têm restrições explícitas, outros nem foram avaliados. Disponibilidade online não é licença.
2. **Identificação definitiva:** **71** registros continuam sem correspondência bibliográfica e **404** com correspondência apenas provisória; eliminar duplicatas de obras por DOI/edição/hash.
3. **Leitura e revisão de conteúdo:** cartões originais provisórios necessitam checagem humana de correspondência com cada fonte, pertinência, contraexemplos, copyright e validade das afirmações; metadados [P] nunca promovidos automaticamente a [L].
4. **Materiais ausentes:** não foi localizada cópia do livro de Ângelo Domingos Salvador; conservar referência externa em vez de inventar leitura.
5. **Testes de uso real:** instalação limpa, limitações de Python/HTTPS por plataforma, comportamento sem rede, escolha de cards não relevantes, recuperação de fontes corretas e erros de citação/paginação.
6. **RAG propriamente semântica:** o modo integrado é **busca lexical por metadados** com leitura limitada; não foi homologada recuperação vetorial ou eficácia científica.
7. **Versão estável:** PR #101 continua Draft; não há autorização para merge, release, nem aceite automático de gates. Antes de release faltam revisão científica, revisão jurídica final das licenças, homologação multiusuário e política de atualização.

**Decisão:** encerrada a ampliação temática desta rodada, **não** o trabalho de revisão de todas as fontes, nem a homologação de uma biblioteca científica completa.
