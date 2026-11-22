# V1-15/20 — RESULTADOS da auditoria de integridade, duplicatas e codificação

**Estado:** PARCIAL — auditoria documental e verificações estruturais realizadas; aceite técnico integral, científico e de direitos **NÃO** concedidos. **Onda:** A. **Dependências do ticket:** nenhuma. **Branch exclusiva:** `work/v1-15-20261121`.

## Fontes e delimitação

- Manifesto imutável `knowledge/methodology/intake/v1_parallel/V1-WORKPACKAGES-MANIFEST.json`, commit `7c92045310eb3b1474a9612a777fb0012a511592`, blob `2f85dc6c4283376b9fc3c312668f0a1f25a0a301`.
- Snapshot de leitura da PR #101 `c5e0ca9abd98f824f1576c3ad94c6e9a5d18e9bf`; `source_registry_catalog.json` blob `511b519f6524cd1f7f977dc41a330ce62fbd00c1`; `catalog.json` blob `6ca3ebde72b117717ae994390121c5aee884d7be`.
- Somente os cinco `rights-ledger-part-01..05.json` para metadados de inventário e os 20 `IB-XX-DELTA.json` nas branches IB correspondentes; **343 fichas source nas branches IB** e **174 cards editoriais no snapshot da PR #101** lidos integralmente para recomputação de hashes. **Atualização:** no saneamento posterior, 23 cópias de PDFs foram lidas de forma autenticada e temporária, exclusivamente para recomputar SHA-256; os arquivos temporários foram apagados e nenhum PDF foi incorporado ou publicado no GitHub.
- O ticket V1-15 autoriza apenas relatórios e scripts da própria etapa. Índices, catálogo, ledger, fichas de outras etapas e manifestos não foram modificados.

## Resultados efetivamente demonstrados

1. **Registro bibliográfico:** 475 caminhos e IDs distintos no índice congelado, sendo 132 `SOURCE_PDF_WORK_VERIFIED` e 343 `CATALOGUE_MATCH_NOT_ORIGINAL_VERIFIED`. Todos os 475 `sha256` do índice têm formato hexadecimal de 64 caracteres, o que **não comprova seu conteúdo**.
2. **Deltas das 20 etapas IB:** 343 registros examinados (IB-01..03: 18 cada; IB-04..20: 17 cada). Os 343 campos de hash das fichas têm formato correto. Nas comparações realizadas com o ledger: **0 divergências de filename e 0 divergências de size_bytes**. **343/343 conteúdos SHA-256 recomputados, 343 correspondências, 0 divergências e 0 falhas de leitura**, nos respectivos HEADs IB observados. Essa é integridade de Markdown, não de PDFs.
3. **Cards editoriais:** 174 paths distintos, todos com hash declarado de 64 caracteres; 170 marcados `DRAFT_NEEDS_INDEPENDENT_REVIEW` e quatro sem status explícito. **Nenhum** é promovido a aprovado por essas contagens.
4. **SHA-256 efetivamente recalculados (sobre bytes UTF-8 das fichas obtidas do GitHub):**
   - `SRC-0099` em `work/ib-01-20261121`: esperado e obtido `c9d2f4481f90ad19b91fa52e1e97a2dfa4412ca88574a88af80ccb3635264096` — **MATCH**.
   - `knowledge/methodology/cards/reviews.md` no snapshot congelado: esperado e obtido `331db84256e59599d0a8674b0064d9c3058a9261917efb03e403f083dfcde8af` — **MATCH**.
   - **Auditoria integral de hashes: 343/343 source cards + 174/174 editorial cards = 517/517 correspondências, 0 divergências e 0 arquivos indisponíveis.** Os dois hashes detalhados acima são exemplos verificáveis. O recálculo foi feito sobre o conteúdo UTF-8 efetivamente obtido das refs do GitHub; não se auditou o conteúdo científico; a auditoria independente dos PDFs foi realizada em etapa posterior e está documentada abaixo. As contagens por lote (18×3 + 17×17 e 17×10 + 4) estão no DELTA.
5. **Duplicatas candidatas (11 grupos por tamanho de arquivo idêntico):** `0111/0454`, `0354/0438`, `0206/0337`, `0235/0267`, `0244/0371`, `0230/0344`, `0349/0391`, `0245/0370`, `0006/0435`, `0402/0430/0434`, `0234/0256` (todos os números se referem a IDs `SRC-XXXX`). **Saneamento posterior: os SHA-256 de todas as 23 cópias privadas foram calculados e são iguais dentro de cada um dos 11 grupos.** A duplicidade binária foi comprovada, mas revisão bibliográfica independente, decisão de consolidação de registros e autorização de redistribuição continuam pendentes. Nenhum ID foi eliminado.
6. **Aliases de pastas (25 diferenças de string, sem diferença de nome ou tamanho do PDF):** IB-05 = sete (`SRC-0175..0180`, `SRC-0183`); IB-06 = nove (`SRC-0195..0198`, `SRC-0200..0204`); IB-14 = dois (`SRC-0368..0369`); IB-17 = sete (`SRC-0407..0409`, `SRC-0411..0414`). Os 25 PDFs foram localizados de modo único nos seis diretórios físicos com nomes corrompidos e confirmados por nome e tamanho. As grafias normalizadas nas fichas IB são **aliases de exibição**, não nomes para substituir o caminho físico. Existe outra pasta distinta com a grafia correta “Análise de Conteúdo”; não confundir nem fundir as duas. Mapa no `V1-15-DELTA.json`.

## Direitos, ciência e condições de uso

- No índice de origem, `rights_review` apresenta 458 `NOT_CHECKED` e 17 `VERIFIED_PUBLISHER_LICENSE` — isso não autoriza inferir direito de distribuição de edição/cópia privada e não representa revisão científica independente.
- Não se acrescentaram PDFs ao GitHub. Em saneamento separado foram conferidos 23 PDFs privados por SHA-256 sem publicação ou retenção de cópias locais; não se alteraram decisões de licença nem se promoveram proposições [P]/[I] a evidências [L].
- Os 517 SHA-256 recomputados verificam apenas os bytes dos arquivos Markdown nas refs especificadas; a auditoria não certifica identidade da obra, PDF original, autoria, licença de redistribuição, integridade de uma futura integração nem veracidade dos conteúdos. **Não houve revisão independente de originalidade ou fidelidade acadêmica**.

## Entregas e testes

- Script exclusivo `scripts/v1_15_integrity_audit.py`, commit `4d4cb1a2e448bb0fa0ff863b49f7d5725e9c30ca`: lê refs congeladas, normaliza schemas dos 20 DELTAs, recalcula 343+174 hashes, sinaliza 11 grupos de mesmo tamanho e 25 aliases sem acessar PDFs privados; não altera catálogos.
- Este script foi **criado, mas NÃO executado em checkout com todas as refs**; nenhum `CI PASS` é declarado. A implementação requer execução local controlada e leitura posterior dos resultados. Verificações estruturais e recomputação independente dos **517 hashes** foram efetivamente executadas em leituras autenticadas do GitHub com implementação SHA-256 cujo teste conhecido `abc` foi validado. O script Python proposto ainda necessita execução/reprodução em checkout; CI não foi executada.
- Recibo estruturado: `knowledge/methodology/intake/v1_parallel/V1-15-DELTA.json`. O HEAD do recibo deve ser relido após concluir a etapa.

## Bloqueios, concorrência do canônico e incidente de privacidade

- **MD canônico não gravado.** O alvo é um arquivo `text/markdown`, não um Google Doc nativo. A interface de atualização disponibilizada para raw Markdown substitui o arquivo inteiro e não oferece patch atômico de subseção nem guarda por versão. O conteúdo remoto mudou durante a auditoria (comprimento em caracteres de 306686 para 307566); uma substituição integral poderia apagar avanços de outras abas. **A regra de preservar estado em caso de conflito prevalece.** A subseção 31.15 continua pendente de atualização segura, com releitura e verificação.
- **Incidente restrito aos commits próprios V1-15:** o primeiro recibo DELTA incluiu por erro um identificador de localização do MD no Drive. O valor foi retirado do HEAD em commit posterior; o commit anterior permanece alcançável no histórico Git. Não reproduzir o identificador, não reescrever histórico, não fazer force-push, nem presumir que o saneamento do HEAD removeu a exposição histórica. Registrar para decisão de segurança/privacidade, incluindo articulação com o tratamento da Issue #103.
- Os 11 grupos de hashes PDF e os 25 aliases foram efetivamente reconciliados. **Permanecem bloqueadores:** permissão pública confirmada em 25 PDFs (qualquer pessoa com link), decisão sobre exposição histórica de identificador no Git, revisão humana de direitos e ciência, reprodução do script Python/CI, e escrita concorrente segura no bloco 31.15.

## Próximos passos, sem antecipar V1-16

Executar o validador V1-15 em clone controlado com as 20 refs IB e o snapshot imutável; revisar divergências reais; preservar o registro dos 11 grupos de PDFs binariamente idênticos e dos 25 aliases de exibição sem fundir IDs/pastas; auditar e conter as permissões públicas dos PDFs com deliberação do mantenedor; examinar o incidente sem intervenção unilateral no histórico; atualizar o **mesmo** MD canônico apenas com recurso de gravação seguro, conferindo bloco 31.15 e preservação dos demais. **V1-16 permanece condicionada à entrega auditada de todas as V1-01..V1-15.** Nenhum merge, release, tag, force-push ou MCP foi realizado.

## Saneamento controlado complementar — verificações executadas em 21/11/2026

### Duplicatas: auditoria binária das 11 classes (23 PDFs originais)

As cópias foram recuperadas por acesso autenticado ao Drive, usando correspondência exata de nome e tamanho, e seu SHA-256 foi calculado com `hashlib.file_digest` sobre os bytes integrais. Em todos os grupos os hashes das duas ou três cópias são **idênticos**; os digest completos por grupo estão no DELTA. Os PDFs de trabalho foram apagados da área temporária após a aferição, não enviados ao GitHub. Contagens: **23/23 PDFs verificados; 11/11 classes com equivalência binária; zero divergência SHA-256.**

| Grupo de SRC | Arquivos | SHA-256 do PDF (prefixo) | Resultado |
|---|---:|---|---|
| 0111/0454 | 2 | `9b12a0c0f29cc77c` | idênticos |
| 0354/0438 | 2 | `c8d8e7792adc0bc8` | idênticos |
| 0206/0337 | 2 | `9ec4986eacda3dfc` | idênticos |
| 0235/0267 | 2 | `9a2d07e4f62edfa6` | idênticos |
| 0244/0371 | 2 | `cf7139ab385e44ef` | idênticos |
| 0230/0344 | 2 | `b9160abe4e696547` | idênticos |
| 0349/0391 | 2 | `a4f11f5d1a13bb4c` | idênticos |
| 0245/0370 | 2 | `329b88773b6d4c1c` | idênticos |
| 0006/0435 | 2 | `fe1ba0c860a4c8b` | idênticos |
| 0402/0430/0434 | 3 | `daed917cbcca5ad7` | idênticos |
| 0234/0256 | 2 | `e383b25084ae5d73` | idênticos |

Conclusão restrita: comprovada identidade **binária** das cópias de cada grupo; não se comprova licença para republicação, nem se conclui que duas ocorrências em tópicos distintos sejam redundantes do ponto de vista da recuperação temática. Manter os 475 IDs e todas as ligações até decisão humana sobre modelagem de obras versus exemplares.

### Aliases: seis pastas reais, 25/25 fichas localizadas

Leitura de metadados diretamente dos seis diretórios físicos correspondentes aos seis agrupamentos de alias identificados no ledger (IB-05, IB-06, IB-14 e IB-17). **25/25 PDFs** localizados uma única vez na respectiva pasta original; 25/25 nomes e tamanhos coincidem. Os nomes reais das pastas apresentam grafias corrompidas; as formas normalizadas dos lotes IB servem apenas para exibição e pesquisa, **nunca** como substituição destrutiva de caminho. Especial atenção: existem duas pastas distintas, uma com a grafia normalizada `Análise de Conteúdo` e outra com grafia danificada; não confundir as duas.

### Achado de segurança P0 — ACL dos PDFs e histórico Git

- O repositório do GitHub é **público** e o histórico da branch V1-15 inclui um commit anterior com identificador do MD privado; o HEAD atual foi saneado, mas isso **não elimina** o commit histórico. Tratamento sob decisão do mantenedor e coordenação com a Issue #103; nenhuma reescrita ou force-push.
- O **MD canônico** está com permissão restrita ao próprio proprietário na verificação pontual. Contudo, **25/25 PDFs investigados nos aliases têm permissão efetiva `anyone:reader`**. Isso significa acesso por qualquer pessoa com o link; não foi verificado que todos os demais 450 arquivos do acervo tenham essa configuração. A exposição de identificadores no histórico pode, portanto, ter impacto real de acesso, não apenas de metadados.
- **Nenhuma ACL foi modificada**, em respeito ao escopo: a V1-15 não possui autorização específica para mudar acessos dos 25 PDFs pertencentes ao acervo compartilhado com outras etapas. Priorizar deliberação do proprietário sobre revisão das permissões, impacto sobre compartilhamentos legítimos e contenção, inclusive das demais cópias.
- Sem licença de distribuição de cópias privadas aprovada neste lote, sem publicação de PDFs, sem promoção de [P]/[I] a [L].

### Condição do MD canônico

O arquivo canônico é `text/markdown` em Drive, com histórico de **90 revisões** observado e modificações contemporâneas de outras abas. A ferramenta disponível **não oferece patch atômico por subseção nem substituição com pré-condição de versão**; substituir o arquivo integral a partir de leitura momentânea pode apagar edições concorrentes. Por isso, **o mesmo MD NÃO foi alterado** neste saneamento. Somente depois de exclusividade de escrita verificável ou ferramenta de atualização condicional deve-se aplicar o bloco 31.15 a seguir, relendo antes de gravar e conferindo todos os outros blocos depois.

## Anexo — subseção 31.15 pronta para reconciliação futura (NÃO aplicada ao Drive)

```markdown
### 31.15 — V1-15/20 — Integridade, duplicatas e codificação

- **Estado:** PARCIAL — auditorias binárias e metadados concluídas; bloqueadores de privacidade/permissões, reexecução do script em checkout, revisão humana e escrita segura do MD ainda pendentes.
- **Manifesto / branch:** commit imutável `7c92045310eb3b1474a9612a777fb0012a511592`; branch exclusiva `work/v1-15-20261121`; snapshot PR #101 `c5e0ca9abd98f824f1576c3ad94c6e9a5d18e9bf`. Onda A, sem dependências de início.
- **Escopo de evidência:** 475 registros em cinco ledgers; 343 registros IB (20 lotes), 343 source cards e 174 editorial cards. **517/517 hashes SHA-256 das fichas Markdown correspondentes; 0 divergências.** 0 divergências de nomes e tamanhos nas fichas do ledger.
- **Duplicatas físicas:** **11/11 grupos binariamente idênticos** por SHA-256 de **23/23 cópias PDF** obtidas apenas para auditoria; 0 hashes divergentes. Arquivos de trabalho apagados; nenhum PDF publicado, nenhuma ficha ou índice consolidado automaticamente, nenhuma licença concedida.
- **Aliases:** **25/25** arquivos localizados nas seis pastas originais de grafia corrompida, com correspondência única de nome e tamanho. Grafias normalizadas IB são aliases de apresentação. Preservar separadamente as duas pastas com variantes de “Análise de Conteúdo”.
- **Segurança:** repositório público; identificador do MD exposto no histórico de commit V1-15 anterior, retirado do HEAD sem reescrita; Issue #103 aberta. MD atual sem compartilhamento além do proprietário, **25/25 PDFs examinados com ACL `anyone:reader`**. ACLs não alteradas nesta etapa. Deliberação e contenção do mantenedor prioritárias.
- **Direitos/ciência:** 458/475 `NOT_CHECKED` e 17 `VERIFIED_PUBLISHER_LICENSE` conforme snapshot do registry; nenhuma licença nova ou direito de redistribuição inferido. 170/174 cards `DRAFT_NEEDS_INDEPENDENT_REVIEW`, quatro sem status; nenhuma aprovação científica independente.
- **Artefatos próprios:** `knowledge/methodology/intake/v1_parallel/V1-15-RESULTS.md`, `V1-15-DELTA.json`, `scripts/v1_15_integrity_audit.py`; somente esses três caminhos alterados nesta branch. Script Python ainda não executado em clone/CI; testes independentes de hash GitHub e PDF Drive efetuados.
- **MD / concorrência:** arquivo `text/markdown` sujeito a edição simultânea e sem gravação condicional disponível; **31.15 NÃO escrita no MD canônico**. Aplicar apenas em edição serializada/com garantia atômica e conferir readback.
- **Próximos passos e bloqueios:** coordenar contenção ACL dos PDFs com o mantenedor e Issue #103; não reescrever história sem aprovação; executar validador Python em checkout com todas as refs; revisar direitos e modelagem das duplicatas; efetuar reconciliação segura 31.15. Não fazer merge, release, tag, implementação MCP, publicação de PDFs ou avançar V1-16 antes de aprovação formal.
```

**O anexo é proposta de texto, não evidência de gravação ou aceite da etapa.**


## Continuidade adicional — classificação Unicode e redução de exposição (21/11/2026)

**FEITO, novo nesta continuidade (somente V1-15):**

- Reabertos o manifesto fixo, os dois recibos da branch existente e o MD canônico. A branch já possuía 10 commits sobre o manifesto e somente três caminhos próprios no diff; não houve recriação, merge nem alteração das conclusões antigas.
- Recalculados **três hashes SHA-256 de objetos Markdown exatos** com implementação independente, validada por três vetores (`abc`, UTF-8 acentuado e texto vazio): `SRC-0099` em `work/ib-01-20261121`, `cards/reviews.md` e `cards/design-science.md` no snapshot congelado. Resultado: **3/3 MATCH, zero diferenças**. Isso é nova contraprova amostral, NÃO execução de toda a auditoria de 517 arquivos nem de PDFs nesta continuidade.
- Reconciliados estruturalmente os registros antigos: **11/11 classes de duplicatas**, total de **23 cópias**, com digest PDF completo de 64 caracteres e indicação anterior de igualdade binária; **0 conflitos internos observados no recibo**. É verificação de consistência do relatório anterior, não novo acesso aos PDFs nem decisão de obra/licença. As 11 classes não devem ser confundidas com meras coincidências de tamanho; os hashes privados foram anteriormente aferidos, e os registros seguem distintos.
- **Novo achado Unicode:** 6/6 pares de strings de pasta registrados no DELTA (7 + 9 + 2 + 7 = **25 aliases**) são **strings distintas inclusive após NFC/NFKC**. Portanto, **0/6 equivalências canônicas ou de compatibilidade Unicode demonstradas**. Isso NÃO invalida os 25 vínculos já verificados por nome/tamanho/Drive: eles são mapeamentos documentados para caminhos físicos diferentes, não equivalência Unicode automática. Persistem duas pastas físicas distintas que não podem ser fundidas. Nenhum falso positivo de igualdade binária foi encontrado entre os 11 grupos conforme as evidências prévias; nenhum alias foi promovido a identidade de caminho por algoritmo.
- No script exclusivo `scripts/v1_15_integrity_audit.py`, adicionada classificação conservadora `EXACT_STRING` / `CANONICAL_UNICODE_EQUIVALENT_NOT_PHYSICAL_PATH_PROOF` / `COMPATIBILITY_UNICODE_EQUIVALENT_NOT_PHYSICAL_PATH_PROOF` / `DIFFERENT_STRING_NO_AUTO_EQUIVALENCE`. O JSON gerado pelo script não inclui mais nomes físicos de pasta nos objetos de alias, reduzindo exposição acidental. **Commits:** [correção](https://github.com/rebsonm/MeuArtigoSkill/commit/54c0022d304aea885c19d66e891718df707739be) e [ajuste de fixtures](https://github.com/rebsonm/MeuArtigoSkill/commit/c0818cd324a3673b8e7e54446210c2988563253a).
- **Testes:** lógica isolada reproduzida em Python com **5/5 fixtures PASS** (SHA-256 `abc`, NFC, NFKC, grafia danificada não equivalente e igualdade literal). Teste/CI do arquivo completo em checkout com as 20 refs **não executado**. Verificação de HEAD antes da atualização: nenhum combined status nem run de workflow retornado; isso NÃO é CI aprovada.
- Revisão preventiva dos recibos públicos no HEAD consultado: nenhum link direto `docs.google.com`/`drive.google.com` detectado no conteúdo dos dois recibos; o incidente de **identificador privado no histórico antigo Git** permanece **aberto**, pois sanitizar o HEAD não apaga commits passados. Os registros atuais de alias ainda contêm nomes de pastas preexistentes; não incluir novos localizadores nem PDFs privados.

**EM EXECUÇÃO / BLOQUEIOS:** reexecução integral e independente do script em checkout controlado com 20 refs IB; revisão humana de direitos/originalidade e de fidelidade científica; contenção de ACLs `anyone:reader` previamente encontrada nas 25 cópias do subconjunto auditado, com decisão do proprietário e coordenação da Issue #103; tratamento da exposição histórica sem rewrite unilateral; reconciliação concorrente do MD. O MD é `text/markdown` bruto e **não foi substituído**, porque não existe mecanismo de patch por seção com guarda de revisão demonstrado. Registrar estado por comentário próprio da §31.15, sem alegar atualização do corpo.

**PRÓXIMA AÇÃO ÚNICA:** executar `python scripts/v1_15_integrity_audit.py --self-test` e em seguida `--repo <checkout-controlado>` com todas as 20 refs IB disponíveis, guardando saída sanitizada e verificando **343/343 + 174/174**, 11 grupos, 25 aliases e zero discrepâncias antes de qualquer aceite técnico.

**CRITÉRIO VERIFICÁVEL PARA AVANÇAR:** resultado reproduzível do script na mesma revisão, com hashes e contagens reconciliadas, ausência de divergência sem justificativa, evidência de tratamento do risco de privacidade/ACL pelo responsável, e auditorias/autorizações independentes onde aplicáveis. `V1-16` e publicação `v1.0.0` não estão autorizadas. Nenhuma aprovação científica, jurídica ou de segurança presumida.


## Execução integral reproduzida — 517/517 (21/11/2026)

**FEITO NESTA CONTINUIDADE:** executado, com código de saída `0`, o script Python **exato** do blob Git `fff187a54c8857f318aa01518f6c6112c18fca88`, preservado na branch V1-15. Como o executor inicial não tinha rede Git e o executor secundário não dispunha do comando `git`, foram obtidos **por HTTPS, em leitura, os bytes públicos dos objetos exatos** do GitHub, usando as refs IB fixadas nos respectivos commits HEAD observados, além dos commits imutáveis do manifesto `7c92045...` e corpus `c5e0ca9...`. O comando `git show ref:path` foi atendido por um adaptador local de leitura que resolve cada ref para o SHA congelado e lê os bytes previamente recuperados. **Não foi um clone Git nativo e NÃO foi um workflow CI; foi execução integral do validador original sobre todos os arquivos necessários.** Os commits IB exatos e o SHA-256 da saída constam no DELTA próprio.

- **Autoteste Python:** `python v1_15_integrity_audit.py --self-test` → `SELF_TEST_OK: SHA-256 e relações Unicode, sem equivalência automática de pasta`; exit `0`.
- **Execução integral:** 546 arquivos de entrada obtidos (20 deltas IB, 343 source cards, 174 editorial cards, manifesto, registro, catálogo, 5 partes do ledger e script); **475** registros catalogados, **343/343 source cards** SHA-256 recalculados e coincidentes, **174/174 editorial cards** SHA-256 recalculados e coincidentes. **517/517 MATCH; zero erros de leitura, zero SHA divergente, zero IDs duplicados/ausentes/inesperados, zero diferenças de filename/size_bytes**.
- **Duplicatas candidatas por tamanho:** **11/11 grupos** identificados pelo script, sem deduplicação nem aprovação de identidade de obra. A igualdade binária de **23 PDFs** permanece evidência de auditoria anterior; **PDFs privados não foram relidos nesta execução**, portanto a saída do script conserva `original_pdf_sha256_verified=0`.
- **Aliases:** **25/25 diferenças de strings** localizadas; as 25 relações são `DIFFERENT_STRING_NO_AUTO_EQUIVALENCE` (nenhuma equivalência NFC/NFKC presumida). A correspondência física no Drive é evidência de trabalho anterior e não é testada pelo script.
- **Contador de divergências técnicas:** `technical_discrepancy_count=0`; comando integral terminou com **exit `0`**. SHA-256 do relatório JSON local sanitizado: `698ec4b95c9e5a1efc41c0ba63c24e79cadd64fac7763c2b0a08c8e14812a150`. Saída produzida somente no executor isolado; nenhum PDF ou relatório contendo identificador privado foi enviado ao repositório.
- **Limites de aceitação:** o sucesso técnico sobre os Markdown não substitui revisão científica e de originalidade, decisão jurídica por cópia, contenção das ACLs `anyone:reader` previamente identificadas, decisão sobre a exposição histórica no Git, execução CI em GitHub ou homologação em host final. O ticket permanece **PARCIAL / SEM GO**.

**EM EXECUÇÃO / BLOQUEIOS:** segurança e ACLs vinculadas à Issue #103, revisão de direitos, revisão científica independente, tratamento da referência privada no histórico Git, escrita segura no corpo da seção 31.15 do MD canônico. Não sobrescrever arquivo Markdown bruto sob concorrência. Nenhum merge, tag, release, alteração em `main`/catálogo/ledger ou publicação de PDFs.

**PRÓXIMA AÇÃO ÚNICA:** encaminhar ao mantenedor, em coordenação com a Issue #103, a revisão documentada e decisão de contenção das permissões `anyone:reader` nos 25 PDFs anteriormente identificados, sem alterar ACLs unilateralmente nesta etapa.

**CRITÉRIO PARA AVANÇAR:** evidência de ACL/privacidade tratadas e validadas por responsável competente, além da integridade 517/517 ora reproduzida e das revisões independentes exigidas para os materiais; somente então considerar consolidação V1-16 após auditadas também as demais etapas. Não declarar aprovação científica, jurídica ou segurança por teste de hash.


## Revalidação individual de ACL — 25/25 (21/11/2026)

**FEITO NESTA CONTINUIDADE — verificação efetiva, somente leitura:** a [Issue #103](https://github.com/rebsonm/MeuArtigoSkill/issues/103) foi relida e permanece **aberta**; não havia comentários registrados na consulta inicial. O incidente original envolve referências privadas remanescentes em histórico Git, apesar da contenção dos HEADs. A V1-15 havia documentado `anyone:reader` em 25 PDFs de aliases; **essa observação foi revalidada agora, diretamente na API de metadados/permissões do Google Drive**, sem baixar conteúdo e sem testar links com acesso anônimo.

**Método verificável:** com base nos cinco ledgers do snapshot congelado `c5e0ca9abd98f824f1576c3ad94c6e9a5d18e9bf` e nas seis classes do DELTA V1-15, foram localizadas as **seis pastas físicas originais**, individualizadas por nome exato no Drive. Para os 25 `SRC-XXXX` já atribuídos, a correspondência foi aferida por **pasta + filename exato + tamanho em bytes**. Houve **25/25 correspondências únicas**, zero ambiguidade e zero falha de leitura. Para cada arquivo, efetuou-se nova chamada de **metadados** e inspeção das permissões retornadas (`permission_metadata_available` em todos): **25/25 possuem permissão explícita `type=anyone`, `role=reader`**. Contagem por grupo físico (sem expor nomes de pasta ou IDs do Drive): **G1 6/6, G2 1/1, G3 9/9, G4 2/2, G5 3/3, G6 4/4**. Não é inferência pela existência de um link: é leitura direta dos metadados de ACL.

**Análise de impacto e limites:** `anyone:reader` indica que a posse do link pode permitir leitura por terceiros; não há prova nesta verificação de indexação, vazamento do link do PDF, download por terceiro, acesso efetivo não autorizado ou que os demais **450** registros tenham a mesma ACL. Direitos de cada edição/cópia permanecem independentes e não aprovados. A exposição histórica de identificadores no Git continua um risco separado; a remoção de referências no HEAD não revoga acesso por link.

**Proposta de contenção, condicionada a decisão formal do proprietário:** (1) inventariar compartilhamentos legítimos por arquivo e dependências de uso dos links; (2) autorizar especificamente substituir a permissão `anyone:reader` por acesso restrito nos 25 PDFs, **sem remover permissões individuais válidas**; (3) verificar em nova leitura dos 25 metadados que não resta `type=anyone`, registrar exceções e confirmar a continuidade do acesso dos usuários autorizados; (4) ampliar a revisão de ACL ao restante do acervo em atividade própria, articulada com #103. A V1-15 **não** possui autorização unilateral para revogar permissões; nenhum compartilhamento, proprietário, arquivo PDF ou histórico Git foi modificado.

**EM EXECUÇÃO / BLOQUEIOS:** decisão escrita sobre impacto/revogação dos links e contenção histórica, revisão de direitos/originalidade e revisão científica independente; a seção 31.15 do Markdown canônico bruto só pode ser alterada com método seguro diante de concorrência. O sucesso técnico `517/517` de hashes Markdown permanece válido para as refs congeladas, mas **não encerra P0**.

**PRÓXIMA AÇÃO ÚNICA:** obter autorização expressa e delimitada do proprietário sobre **revogar `anyone:reader` nos 25 PDFs**, após confirmar a preservação dos acessos individuais necessários; executar eventual revogação apenas em etapa autorizada, nunca implicitamente nesta V1-15.

**CRITÉRIO DE AVANÇO:** após decisão escrita, revalidar em 25/25 ACLs a ausência de `type=anyone` ou documentar exceção autorizada, juntamente com a avaliação separada do histórico Git e dos direitos. A V1-16 permanece bloqueada pelos demais pré-requisitos.
