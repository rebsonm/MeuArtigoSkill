# Meu Artigo RC.1 — publicação em três passos (decisão vigente em 22/11/2026)

**Decisão expressa e prevalente do mantenedor:** publicar os PDFs de terceiros no GitHub, preservando sua autoria e licenças. Esta determinação SUBSTITUI a recomendação anterior de publicação do acervo apenas como software-only. A Skill em ZIP continua sem embutir PDFs; o repositório público disponibiliza a biblioteca separadamente.

## 1. Publicar PDFs de terceiros e cards, com atribuição

- Inventário consolidado: **51 PDFs de terceiros**, **475 fichas de metadados bibliográficos [P]** e **174 cards editoriais [I]/[P]**, totalizando 649 cards.
- Cada PDF retém direitos/licença próprios; os 51 são catalogados sob condições CC BY declaradas pelos respectivos periódicos. Depois da verificação editorial específica dos dois casos pendentes, o catálogo declara **50 CC BY 4.0** e **1 CC BY sem versão especificada** (permissão de compartilhamento descrita expressamente na página da RPCA). Não inventar versão de licença.
- Créditos por obra estão no registro `knowledge/methodology/PDF-ATTRIBUTIONS.md` (autores, ano, título, DOI, link editorial, licença e link PDF). Os PDFs não herdam a licença Apache-2.0 do software.
- O arquivo histórico `SRC-0367` não integra esses 51 PDFs: sua licença CC BY-NC 4.0 requer respeito à finalidade não comercial, e a issue #102 continua aberta para histórico, sem acusação automática de infração. A issue #103 trata dos IDs de Drive em **históricos** já publicamente alcançáveis; merge por squash evita adicionar toda a sequência de commits da PR à `main`, mas não apaga refs históricas preexistentes.
- Não publicar outros PDFs do Drive privado nem converter os 475 metadados em 475 PDFs. Aprovação editorial dos cards não constitui evidência primária [L] nem validação dos gates científicos.

## 2. Corrigir o software sem restringir arbitrariamente uma licença CC BY

- `scripts/public_method_pdf.py` e `experimental/conceptual_rag/github_pdf_reader.py` aceitam o rótulo editorial CC BY e CC BY 4.0 (mas rejeitam NC, ND e SA quando não contempladas na política do catálogo); o usuário não terá PDFs licitamente compartilháveis silenciosamente bloqueados por simples ausência de número na etiqueta.
- Teste sintético `tests/test_pdf_license_version_retrieval.py` cobre ambos os leitores sem baixar PDFs reais. A verificação de hashes do catálogo, metadados, limites e riscos permanece.
- O acervo distingue fichas [P], orientação editorial [I] e afirmações de fonte primária [L]. A validação operacional (635 condicionais, 13 corrigidos, 1 excluído) **não** é validação científica de 649 fontes.
- T01 PASS reportado na instalação anterior; T02 FAIL estrito por dois arquivos apresentados pelo host (151/153), recibo reviewed=false; T32/T34 host NOT_RUN. Não publicar como funcionalidade certificada end-to-end ou versão estável.

## 3. Integrar ao GitHub e emitir candidata experimental

- Manter os 51 PDFs e 649 cards no repositório público. Depois de CI verde para o commit final, integrar PR #112 preferencialmente por **squash** para minimizar propagação de commits intermediários à `main` (sem alegar eliminação de histórico).
- Divulgar a biblioteca com seus créditos e licenças e o pacote instalável da Skill com hash do **mesmo código final**. Uma GitHub Release é diferente de merge; a publicação de pre-release exige o workflow manual autorizado no `main`, com conferência de metadados, e não pode ser declarada realizada antes de existir.
- Publicação é **experimental**, com limitações host T02/T32/T34 claramente identificadas. Issues #102/#103 devem continuar abertas até resolução, sem bloquear o direito de publicar PDFs efetivamente CC BY e devidamente creditados.
- Não aprovar gates, não expor Drive privado, não reescrever histórico/force-push e não incluir obras de terceiros além das autorizadas.

**Última instrução do mantenedor:** “PUBLIQUE OS PDFS TERCEIROS. Pare de tentar desfazer uma decisão minha”. Esta versão reconcilia o projeto com essa autorização; não reintroduzir recomendação de retirar os 51 PDFs como suposta exigência técnica.
