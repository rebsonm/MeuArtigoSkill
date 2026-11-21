# V1-15/20 — RESULTADOS da auditoria de integridade, duplicatas e codificação

**Estado:** PARCIAL — auditoria documental e verificações estruturais realizadas; aceite técnico integral, científico e de direitos **NÃO** concedidos. **Onda:** A. **Dependências do ticket:** nenhuma. **Branch exclusiva:** `work/v1-15-20261121`.

## Fontes e delimitação

- Manifesto imutável `knowledge/methodology/intake/v1_parallel/V1-WORKPACKAGES-MANIFEST.json`, commit `7c92045310eb3b1474a9612a777fb0012a511592`, blob `2f85dc6c4283376b9fc3c312668f0a1f25a0a301`.
- Snapshot de leitura da PR #101 `c5e0ca9abd98f824f1576c3ad94c6e9a5d18e9bf`; `source_registry_catalog.json` blob `511b519f6524cd1f7f977dc41a330ce62fbd00c1`; `catalog.json` blob `6ca3ebde72b117717ae994390121c5aee884d7be`.
- Somente os cinco `rights-ledger-part-01..05.json` para metadados de inventário e os 20 `IB-XX-DELTA.json` nas branches IB correspondentes; fichas individuais SRC-0099 e editorial `cards/reviews.md` para recalcular amostras. **Nenhum PDF privado foi baixado, copiado ou publicado.**
- O ticket V1-15 autoriza apenas relatórios e scripts da própria etapa. Índices, catálogo, ledger, fichas de outras etapas e manifestos não foram modificados.

## Resultados efetivamente demonstrados

1. **Registro bibliográfico:** 475 caminhos e IDs distintos no índice congelado, sendo 132 `SOURCE_PDF_WORK_VERIFIED` e 343 `CATALOGUE_MATCH_NOT_ORIGINAL_VERIFIED`. Todos os 475 `sha256` do índice têm formato hexadecimal de 64 caracteres, o que **não comprova seu conteúdo**.
2. **Deltas das 20 etapas IB:** 343 registros examinados (IB-01..03: 18 cada; IB-04..20: 17 cada). Os 343 campos de hash das fichas têm formato correto. Nas comparações realizadas com o ledger: **0 divergências de filename e 0 divergências de size_bytes**. A necessidade de recomputar todos os 343 hashes de conteúdo ainda existe.
3. **Cards editoriais:** 174 paths distintos, todos com hash declarado de 64 caracteres; 170 marcados `DRAFT_NEEDS_INDEPENDENT_REVIEW` e quatro sem status explícito. **Nenhum** é promovido a aprovado por essas contagens.
4. **SHA-256 efetivamente recalculados (sobre bytes UTF-8 das fichas obtidas do GitHub):**
   - `SRC-0099` em `work/ib-01-20261121`: esperado e obtido `c9d2f4481f90ad19b91fa52e1e97a2dfa4412ca88574a88af80ccb3635264096` — **MATCH**.
   - `knowledge/methodology/cards/reviews.md` no snapshot congelado: esperado e obtido `331db84256e59599d0a8674b0064d9c3058a9261917efb03e403f083dfcde8af` — **MATCH**.
   - **Lista de divergências encontradas entre estes 2 conteúdos: vazia.** Outros 515 conteúdos não foram recalculados nesta execução; seria incorreto descrevê-los como validados.
5. **Duplicatas candidatas (11 grupos por tamanho de arquivo idêntico):** `0111/0454`, `0354/0438`, `0206/0337`, `0235/0267`, `0244/0371`, `0230/0344`, `0349/0391`, `0245/0370`, `0006/0435`, `0402/0430/0434`, `0234/0256` (todos os números se referem a IDs `SRC-XXXX`). É hipótese de cópia/obra comum, **não prova**: falta SHA-256 dos PDFs privados e conferência de identidade/edição. Nenhum ID deve ser eliminado automaticamente.
6. **Aliases de pastas (25 diferenças de string, sem diferença de nome ou tamanho do PDF):** IB-05 = sete (`SRC-0175..0180`, `SRC-0183`); IB-06 = nove (`SRC-0195..0198`, `SRC-0200..0204`); IB-14 = dois (`SRC-0368..0369`); IB-17 = sete (`SRC-0407..0409`, `SRC-0411..0414`). Casos associados a grafia corrompida de acentuação, **pendentes de cotejo com o Drive privado**. Mapa de equivalência candidato consta em `V1-15-DELTA.json`.

## Direitos, ciência e condições de uso

- No índice de origem, `rights_review` apresenta 458 `NOT_CHECKED` e 17 `VERIFIED_PUBLISHER_LICENSE` — isso não autoriza inferir direito de distribuição de edição/cópia privada e não representa revisão científica independente.
- Não se acrescentaram PDFs, não se validaram SHA-256 de PDFs, não se alteraram decisões de licença, nem se promoveram proposições [P]/[I] a evidências [L].
- A amostra SHA-256 prova somente integridade dos dois arquivos Markdown obtidos do GitHub nas refs especificadas. **Não houve revisão independente de originalidade ou fidelidade acadêmica**.

## Entregas e testes

- Script exclusivo `scripts/v1_15_integrity_audit.py`, commit `4d4cb1a2e448bb0fa0ff863b49f7d5725e9c30ca`: lê refs congeladas, normaliza schemas dos 20 DELTAs, recalcula 343+174 hashes, sinaliza 11 grupos de mesmo tamanho e 25 aliases sem acessar PDFs privados; não altera catálogos.
- Este script foi **criado, mas NÃO executado em checkout com todas as refs**; nenhum `CI PASS` é declarado. A implementação requer execução local controlada e leitura posterior dos resultados. Verificações estruturais via conector e os dois cálculos SHA-256 acima foram efetivamente executados.
- Recibo estruturado: `knowledge/methodology/intake/v1_parallel/V1-15-DELTA.json`. O HEAD do recibo deve ser relido após concluir a etapa.

## Bloqueios, concorrência do canônico e incidente de privacidade

- **MD canônico não gravado.** O alvo é um arquivo `text/markdown`, não um Google Doc nativo. A interface de atualização disponibilizada para raw Markdown substitui o arquivo inteiro e não oferece patch atômico de subseção nem guarda por versão. O conteúdo remoto mudou durante a auditoria (comprimento em caracteres de 306686 para 307566); uma substituição integral poderia apagar avanços de outras abas. **A regra de preservar estado em caso de conflito prevalece.** A subseção 31.15 continua pendente de atualização segura, com releitura e verificação.
- **Incidente restrito aos commits próprios V1-15:** o primeiro recibo DELTA incluiu por erro um identificador de localização do MD no Drive. O valor foi retirado do HEAD em commit posterior; o commit anterior permanece alcançável no histórico Git. Não reproduzir o identificador, não reescrever histórico, não fazer force-push, nem presumir que o saneamento do HEAD removeu a exposição histórica. Registrar para decisão de segurança/privacidade, incluindo articulação com o tratamento da Issue #103.
- Pendentes: hashes de 515 conteúdos Markdown, hash dos PDFs originais dos 11 grupos, validação dos 25 aliases no Drive, revisão humana de direitos/originalidade e fidelidade científica, testes do script e escrita segura do bloco 31.15.

## Próximos passos, sem antecipar V1-16

Executar o validador V1-15 em clone controlado com as 20 refs IB e o snapshot imutável; revisar divergências reais; pedir verificação autorizada do arquivo privado para duplicatas e aliases; examinar o incidente sem intervenção unilateral no histórico; atualizar o **mesmo** MD canônico apenas com recurso de gravação seguro, conferindo bloco 31.15 e preservação dos demais. **V1-16 permanece condicionada à entrega auditada de todas as V1-01..V1-15.** Nenhum merge, release, tag, force-push ou MCP foi realizado.
