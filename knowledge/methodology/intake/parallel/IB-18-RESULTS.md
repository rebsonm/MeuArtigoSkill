# IB-18/20 — Recibo documental independente

Base congelada: `c5e0ca9abd98f824f1576c3ad94c6e9a5d18e9bf`; branch exclusiva: `work/ib-18-20261121`; commit das 17 fichas: `56939a4d36ec01d7fd2558dcc9a5b42cad3ffb7d`.
**Resultado:** 17/17 entradas identificadas nos originais; 16 obras intelectuais distintas identificadas (0430 e 0434 duplicam uma obra), sem aprovação científica nem autorização para publicar os PDFs. Inspeção delimitada, sem leitura integral.

## Evidência por registro

| ID | Nome original no ledger | Bytes | SHA256 da ficha [P] |
|---|---|---:|---|
| SRC-0425 | `Krueger e Lewis-Beck (2008).pdf` | 615790 | `a8f07444a5bcad14d8b551536aa5d69ae5b1f1724d447cf385677ebd28d55356` |
| SRC-0426 | `Berk (2010).pdf` | 199835 | `e5d3f577b8191f3f9f990678b7f4112bc04509858d500599a0d912a048a57dac` |
| SRC-0427 | `McCloskey e Ziliak (1996).pdf` | 1290624 | `14f4c7144239575843dac3b3f41910f8812c305a695ae44ea69254f362b6f4f6` |
| SRC-0428 | `Freedman (1991).pdf` | 1519224 | `b4e85eec862085e6e5c5c64dabd4af69d5ba16f201413b6afdbd3b0a85349135` |
| SRC-0429 | `Figueiredo Filho et al (2011).pdf` | 913329 | `25e2d7f94cc425956c20d9751f25bca17c77d5a3bbbc6882a360b749088794da` |
| SRC-0430 | `Figueiredo Filho et al (2021).pdf` | 2633104 | `8b52ac03f5d7692ea34d988e85ff2601427926342bbc92e54c1114252668bd6c` |
| SRC-0431 | `Leite,Rocha,2019.pdf` | 341114 | `0bac9328445b6c3ebc470354ff6d3ce839fd2296c80850305858c76721a0346a` |
| SRC-0432 | `Guerra,Almeida,2021.pdf` | 3708183 | `f572a98ec756b2b3cbad747806618d370bf80837908e90321347e94d7ddb2584` |
| SRC-0433 | `Rezende,2015.pdf` | 245555 | `7dd23ec446c848b5d9f780b9d037b87736d79f227f19ec8cca0e48eb9a6727a8` |
| SRC-0434 | `Figueiredo Filho et al (2021).pdf` | 2633104 | `a5780e81c35afc22b6409586983395bfd14f4f247c8bc787610b7bed5c016dc4` |
| SRC-0435 | `Barberia,2019-politica-comparada.pdf` | 2535759 | `173c7c8db325dc1a3f43a13727d39bf2f593b303a813dc7e7acd81fea68dd97c` |
| SRC-0436 | `Montenegro,2016.pdf` | 883407 | `6a6137f4d388e173e65e61c867cf3126ebc7f214e5767b835401e898ebb4d8c4` |
| SRC-0437 | `Figueiredo Filho et al (2016).pdf` | 353457 | `8fb31fb7360734bc4a6b04f07a81f5ae4bda07b2e931fc342f92e8e1d1be4320` |
| SRC-0438 | `Soares (2005).pdf` | 120525 | `1ba2608637b2ae36dd8b0d5d773067fdf8466ec21dfda705d26e654c91cdeb7d` |
| SRC-0439 | `Silva (2018).pdf` | 1904970 | `0092b16439e23c2b7d3084eed3280d286ed0ce70453716f84cbf56d00e4434d0` |
| SRC-0440 | `Neiva(2015).pdf` | 974751 | `a9418f748dfb11ef13f17822cbb0d21816b8b6e0776acfdad81c6507260db31f` |
| SRC-0441 | `bernardes nunez 2021 tripla identidade em tensão.pdf` | 200798 | `085d292bca93101487f80c9517cdb131a29fb974c12c6af2b5b877a197db1834` |

## Correções e ressalvas

- **Duplicidade:** SRC-0430 e SRC-0434 representam a mesma obra intelectual (título, autores, DOI, páginas e ano), registrada em dois PDFs de pastas diferentes; ambos permanecem como IDs separados, sem criar nova publicação.
- **SRC-0432:** título/autoria no PDF escaneado de 18 páginas = Rosiene Guerra e Sabrina Almeida, *Método e Desenho de Pesquisa na Ciência Política Brasileira: Uma Análise da Literatura (2000 a 2015)*, ReLMIS 20, 38–55; catalogação importada trazia título incorreto.
- **SRC-0427:** artigo de McCloskey e Ziliak em 18 páginas digitalizadas, primeira página conferida visualmente; DOI não confirmado.
- **SRC-0439:** PDF rotulado 2018 contém edição revisada de 2023, ISBN 978-65-87791-31-9; diferenciar ano original da edição efetiva.
- **SRC-0431:** string de DOI da cópia contém placeholders %vi%i, portanto DOI não confirmado; revisão editorial futura.
- **SRC-0440:** edição impressa de 2015, disponibilização on-line em 2016; ISSN impresso aparece incorretamente como ISBN na sobrecapa.
- **SRC-0425:** PDF é fascículo completo da newsletter, mas ficha refere-se somente ao artigo atribuído ao registro.

## Direitos

- **SRC-0435 e SRC-0439:** Enap permite reprodução de texto/dados com atribuição e veda fins comerciais; a inclusão desses PDFs na biblioteca pública NÃO foi efetuada, pois os direitos específicos de cada cópia/terceiros ainda exigem controle.
- **SRC-0441:** indicado CC BY-NC-ND 4.0, mas com descrição textual inconsistente; revisar termos e eventuais materiais de terceiros.
- **SRC-0428:** JSTOR apresenta termos de uso; **SRC-0426:** copyright Springer; outros registros não tiveram licença ampla verificada nesta inspeção.
- **Nenhum PDF de terceiros redistribuído.** Dados privados de Drive IDs mantidos fora deste repositório público.

## Testes, bloqueios, continuidade

- Confirmar por comparação Git que apenas 17 fichas e os dois recibos IB-18 foram modificados.
- Validar 17 hashes SHA256 textuais das fichas conforme DELTA e unicidade de 17 IDs; CI remota não iniciada pela branch, não alegar aprovação.
- Registro de autoria/título/edição confirmado; pendências de DOI/termos/licenças tratadas sem bloquear identidade documental. Revisão acadêmica integral, gates [L], publicação e integração global permanecem PENDENTES.
- O integrador, em sessão separada, deve incorporar os deltas sequencialmente, reconciliar catálogo global, ledger e manifestos, com testes/CI; não executar merge, release, tag ou MCP nesta etapa.
