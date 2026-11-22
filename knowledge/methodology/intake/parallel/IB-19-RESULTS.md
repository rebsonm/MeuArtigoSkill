# IB-19/20 — Recibo de identificação documental (21/11/2026)

- **Escopo:** SRC-0442 até SRC-0458, 17 registros, sem reprocessamento fora do lote.
- **Fonte congelada:** `c5e0ca9abd98f824f1576c3ad94c6e9a5d18e9bf`; ledger parte 05; branch `work/ib-19-20261121`.
- **Localização e correspondência:** 17/17 registros coincidem em nome, tamanho e pasta de origem; um nome homônimo (`Valladares,2010.pdf`) foi desambiguado pela pasta Etnografia Política.
- **Conferência documental:** 17/17 identidades de obra reconhecidas diretamente na cópia, com uma ressalva de ano para SRC-0454 (metadados PDF criados em 2007; edição no corpo não explicita ano). Sem revisão científica independente.
- **Tipologia especial:** SRC-0442 é capítulo dentro de livro inteiro; SRC-0450 dissertação; SRC-0451 tese corrigida; SRC-0454 resenha, não livro; SRC-0455 coletânea; SRC-0452 trabalho de anais; SRC-0456 edição 2015, copyright 2014.
- **Direitos:** CC BY 4.0 expressa em SRC-0448, SRC-0457 e SRC-0458; CC BY-NC-ND 2.5 AR em SRC-0452; autorização restrita a estudo e pesquisa em SRC-0451; reserva expressa de direitos em SRC-0442, SRC-0453 e SRC-0455; em outros exemplares não se localizou licença expressa que permita publicação do PDF específico. Não houve redistribuição de binários.
- **Saída GitHub prevista:** 17 fichas editoriais [P], `IB-19-RESULTS.md`, `IB-19-DELTA.json` somente na branch independente. O DELTA identifica Drive IDs privados para futura integração documental, sem expor conteúdo dos PDFs.
- **Testes:** conferência de unicidade dos 17 IDs, pasta/tamanho/nomes, SHA256 do conteúdo UTF-8 de cada ficha, segregação [P] e restrição de caminhos. CI remota não presumida.
- **Pendências:** confirmação editorial da data de SRC-0454 no ato de integração; revisão jurídica de terceiros e termos de cada edição; integração serial no catálogo/ledger/manifests global; CI após integração; avaliação científica independente dos cards.
- **Sem alteração:** main, PR #101, ledger, source registry, snapshots, tags, release, MCP ou PDFs distribuídos.

## Commits individuais verificados na branch exclusiva

- SRC-0442: `7ca4a79ffd4ca5c7696eca2b133bfed22fb774d0`
- SRC-0443: `f26b6847c1ebea9a0b1452a2049779c8898924b2`
- SRC-0444: `67cf241d7eab3acaca85942a564233c10de2c33e`
- SRC-0445: `feda9aaf281de4e58cfbb8965c3f011ef65a7c73`
- SRC-0446: `f7d8f4b67eaff2589c85c4698cb80ab90e36caa5`
- SRC-0447: `31f7451ad835f0bbb91c9480814295c5576e33d1`
- SRC-0448: `5c91126106bbc54b9cde99c5bf6d9e8fe4ed4ce7`
- SRC-0449: `e357ccb6fe931f7e6b11b4a5cd0d543ac12d2b2f`
- SRC-0450: `b8137ea5a137f859d4abd90396712c4fde62331c`
- SRC-0451: `1af1d7f737277ba16df9d4a77bb61344df2b1f13`
- SRC-0452: `6fc2b61dfe78be52db820f09e041163f4f57b8e9`
- SRC-0453: `007f6c1342169fd69f9ff7d08eb25756ebf9399e`
- SRC-0454: `25908d1bae2bc93749bf62c73f2eee289fa33015`
- SRC-0455: `f888ac4791b4fa94fc81dc1c03def928549edcce`
- SRC-0456: `485f5abd7ae41311f9601eec86778200d3d75c7b`
- SRC-0457: `d47471fa5585ec366eb3de4351a16c2f864d2db5`
- SRC-0458: `650635628d6b1e3634b86ffd70cac5df27fc6e20`

## Estado de validação

As 17 fichas foram gravadas e devem ser reconciliadas com o DELTA por SHA256 do conteúdo de cada Markdown. Ainda não há CI remota confirmada para esta branch, tampouco merge, publicação de PDF ou aprovação científica. A integração global é tarefa de coordenação independente.
