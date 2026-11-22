# Homologação técnica independente — pacote Meu Artigo RC.1 TEST-ONLY com 29 PDFs

**Data:** 2026-11-22 (America/Fortaleza). **Repositório:** `rebsonm/MeuArtigoSkill`. **PR:** [#112](https://github.com/rebsonm/MeuArtigoSkill/pull/112), Draft. **HEAD da PR antes da execução:** `2ffd2f9fa3aa04dd399ad64b4841db96ca313f78`. **Build source SHA declarado em ambos os manifestos:** `7e9b26d50229758cec6aa0fb07ae10d96eea276f`. **Escopo:** homologação LOCAL e ISOLADA de ZIPs de GitHub Actions, **não** inspeção da instalação real/gerenciada pelo host ChatGPT nem aprovação jurídica/científica.

## Fonte dos binários e cadeia de integridade

Foram recuperados os binários da própria execução [Release audit #44985272850](https://github.com/rebsonm/MeuArtigoSkill/actions/runs/44985272850) da PR #112; CI `completed/success`:

| Objeto | Artifact ID | Bytes | SHA-256 efetivamente calculado |
|---|---:|---:|---|
| Artifact ZIP externo `MeuArtigoSkill-PDFs-TEST-ONLY-NOT-RELEASE.zip` | `14739735732` | 23.167.871 | `4ddafa0f99e8a532a6bdf3907fdccb7c36d587588c5f5b1a9788ad3965f7814d` |
| ZIP interno de PDF `MeuArtigoSkill-v1.0.0-rc.1-PDFs-TEST-ONLY.zip` | envolvido acima | 23.178.838 | `6eaa65efee38aeb77258c8118dac4b8f75ce9f4169673c6e20e0fd3f505a1544` |
| Artifact ZIP externo `MeuArtigoSkill-rc-test-only.zip` | `14739606324` | 602.441 | `af3a293ccab58b0ff1ecb9398c6a84724aebba96cbaf2f02a85e30725e8f0659` |
| ZIP de instalação padrão `MeuArtigoSkill-v1.0.0-rc.1.zip` | envolvido acima | 610.385 | `07b13b38646f45a1a8cdb5326f46fd4e7cab0a99ca6cf7c0c45436ca5500f5af` |

Os digests dos dois arquivos ZIP externos coincidem com os `sha256:` declarados na API de artefatos GitHub. O ZIP de instalação padrão coincidiu também com `BUNDLE_BUILD_RECEIPT.json` e `SHA256SUMS.txt` internos no artefato de CI. Todos os ZIPs foram examinados contra erros CRC, caminhos absolutos/traversal, nomes duplicados e entradas symlink: nenhum detectado; **sem acesso à instalação persistida pelo host e sem reinstalar a Skill atual**.

## Ambiente, procedimentos e matriz de execução

Ambiente de ensaio: diretórios temporários separados (`trial`, `standard`), Python **3.13.5**, PyMuPDF/fitz **1.26.7**, rede externa indisponível. Testes somente locais, scripts copiados dos ZIPs; nenhum registro real de pesquisa foi aberto, criado ou modificado; nenhuma chamada à API OpenAI/GitHub para ler PDF nos testes de busca. `PYTHONDONTWRITEBYTECODE=1` usado para preservar integridade de diretórios sob teste. **Os 25 testes automatizados deram 25 PASS, 0 FAIL**:

| Eixo | Evidência efetivamente obtida | Resultado |
|---|---|---|
| ZIPs de entrada/saída | Quatro níveis ZIP (dois externos e dois internos), CRC, sem caminhos inseguros/duplicados/symlink | PASS |
| Cadeia de digest | Wrapper CI e recibo SHA-256 da Skill padrão, digests coincidentes | PASS |
| Versão/manifesto TEST-ONLY | `VERSION=1.0.0-rc.1`; 185 arquivos totais, **184/184 arquivos manifestados byte-idênticos**; manifesto `9cf015ac2fa55cee42f98b675f77658fef55212313407461c1046ecfc1d360bb` | PASS |
| Versão/manifesto da Skill padrão | 153 arquivos totais, **152/152 arquivos manifestados byte-idênticos**; manifesto `330d114a9bd8ef29b8cb01b37242c6d5e71696ee607ef2123956bcb64fdf6e25` | PASS |
| Verificador oficial | `python scripts/verify_installed_bundle.py --root <diretorio-extraido> --expected-version 1.0.0-rc.1`: `PASS`, `integrity_mode=ALL_BUNDLE_BYTES_EXACT` para trial e standard, sem divergência de presentation `agents/openai.yaml` e `assets/icon.svg` no cenário local | PASS |
| Escopo de 29 PDFs | `PUBLIC_PDF_TEST_SCOPE.json` contém **29**; os PDFs encontrados são exatamente esses 29, **sem 30º arquivo ou PDF fora da allowlist**; o catálogo de busca interno também tem **somente 29** (ao contrário dos 51 catalogados no repositório) | PASS |
| Hashes de PDFs | 29 PDFs locais, **29/29 SHA-256 e tamanhos recalculados** e coincidentes com scope e catálogo embutido; `%PDF-` presente. Total **27.287.058 bytes** | PASS |
| Leitura dos PDFs | PyMuPDF abriu **29/29 sem senha**, **316 páginas** no total; **29/29 com texto extraível** (mínimo 18.586 caracteres/documento); OCR não usado | PASS |
| Busca / recuperação offline | Cinco perguntas com recuperação direta de PDFs diferentes, `RETRIEVED_PDF_PAGES`, índice de página, `sha256`, metadados, versão/commit imutável e marca explícita de `scientific_quality_validated=false` | **5/5 PASS** |
| Sem correspondência | Pergunta fora do catálogo e consulta sobre PDF não incluído produziram `NO_MATCH_IN_PUBLIC_PDF_CATALOG`, `no_source_read_claim=true`, sem fingir leitura nem tentar rede | PASS |
| Integridade diante de alteração | Conteúdo PDF deliberadamente alterado **em memória**, sem modificar ZIP: `PDF_SIZE_OR_HASH_MISMATCH` impediu recuperação | PASS |
| Ausência de PDF no ZIP padrão | `MeuArtigoSkill-v1.0.0-rc.1.zip` contém **0 PDFs** e **não contém catálogo PDF local**. Em rede indisponível, a tentativa de busca devolveu `UNAVAILABLE_OR_BLOCKED`/`no_source_read_claim=true`; não houve leitura fictícia | PASS (com limitação de capacidade offline) |
| Atribuição de direitos | Os 29 registros do `PUBLIC_PDF_TEST_SCOPE.json` têm `exact_pdf_licence_certified_by_human=false`; nenhuma revisão jurídica/humana foi inferida de CI | PASS (sem aprovação de direitos) |

**Cinco consultas de recuperação verificadas:**

1. `Ten Simple Rules for Writing a Literature Review` → `pautasso-2013-literature-review.pdf`, página PDF índice 3.
2. `Interrupted time series regression public health interventions` → `lopez-bernal-cummins-gasparrini-2017.pdf`, página PDF índice 1.
3. `thematic saturation qualitative research interviews` → `guest-namey-chen-2020-saturation.pdf`, página PDF índice 16.
4. `Designing conceptual articles four approaches` → `jaakkola-2020-designing-conceptual-articles.pdf`, página PDF índice 1.
5. `responsible referencing simple rules` → `plos-pcbi-1006036.pdf`, página PDF índice 1.

Os índices são páginas PDF (base 1), não paginação impressa. O texto obtido é marcado `EXTRACTED_PDF_PAGE_NOT_SCIENTIFICALLY_VALIDATED`. A versão padrão foi invocada via CLI com rede indisponível e retornou **`UNAVAILABLE_OR_BLOCKED`**, sem alegar leitura; não inferir que ela recupera PDFs offline.

## Comparação do código executável com a PR

Os blobs Git SHA-1 dos arquivos **executáveis** e entrada do ZIP TEST-ONLY são idênticos aos do HEAD da PR #112 (consultados na mesma sessão):

- `scripts/public_method_pdf.py` — `1c7bf33b0347ceb94dafeb90215807e72857f2a2`.
- `scripts/verify_installed_bundle.py` — `1ca3d374f042571a067c348e183fecd7f451d836`.
- `SKILL.md` — `83b9b7a2b4ab1fdb3101f8a2052d98c9f8e64b05`.

O `knowledge/methodology/pdf_catalog.json` **não é byte-idêntico ao do HEAD** por desenho: o catálogo da PR contém 51 obras, mas o catálogo presente no ZIP TEST-ONLY contém **somente os 29 autorizados para teste**. O campo `build_source_commit=7e9b26...` dos manifestos é um pin de build e não coincide com o HEAD documental `2ffd2f...` da PR; **não confundir ambos os commits**. Os scripts relevantes foram comparados aos blobs do HEAD.

## Classificação e bloqueios que não foram resolvidos

**Técnica local — PASS RESTRITO.** Evidência suficiente para instalação temporária/extrator local, integridade do trial e recuperação offline dos exemplos selecionados. **Homologação no host ChatGPT — NOT_RUN/BLOCKED:** não foi possível inspecionar os arquivos **efetivamente salvos** no catálogo de Skills do host, aplicar as transformações possivelmente feitas pelo host a `agents/openai.yaml`/`assets/icon.svg`, executar a UI de Skills ou obter um recibo humano de readback. O PASS do ZIP extraído **não pode ser apresentado como PASS da instalação real**. Se o host transformar os dois arquivos, seguir `docs/HOST_PRESENTATION_ATTESTATION.md` e o verificador estrito sem marcar `reviewed=true` sem revisão real.

**Direitos — BLOCKED:** 29 casos são somente `AI_ASSISTANT_DOCUMENTARY_CHECK`; o campo `exact_pdf_licence_certified_by_human=false` em todos, sem sign-off. O histórico de conflito da RPQ, os dois `CC BY` genéricos, Issue #102 (direitos/histórico) e #103 (histórico de localizadores privados) permanecem tópicos separados. O escopo da auditoria documental dos 20 candidatos dos lotes 01–04 não gera novas permissões. **Nenhuma inclusão automática de PDFs nem declaração de domínio público ou redistribuição liberada.**

**Gate científico — PENDING:** testes de parser e páginas não demonstram correção científica nem qualidade metodológica da fonte. Nenhum dos sete gates foi alterado. **NÃO GO para merge, tag, release, publicação ou substituição do pacote instalado.**

## Artefatos locais reproduzíveis

Registros locais, sem os 29 PDFs: `homologate_offline.py` (SHA-256 `0e3cb3cc4d4aea89ccd8142509a6034bc20a9bcbf8f3d0fc8dc58a42b24f3dfc`), `homologation_local_results.json` (SHA-256 `58101d91def4f66c27cd173099067f27647e8e0849e34029a02d6b3d18a28877`), e log de execução final. A versão ZIP de evidências **não contém nenhum PDF de terceiros**, digest `0020f3515b3595ba386770789beef2d5c4695a6d086850cb4796490a8ac9b2d6`. Foi gerada separadamente para eventual revisão, **não anexada ao GitHub Release**.

## Próximo passo recomendado

**A — Host acceptance real:** executar o protocolo de readback na instância que tenha a Skill RC.1 **efetivamente instalada**, com recebimento do manifesto e SHA esperados, separação de assets gerenciados, teste de recuperação via interface e recibo externo; caso host não esteja acessível, manter `NOT_RUN`. Outras alternativas são **B — ajustar documentações de dependência de rede e consulta offline na distribuição padrão** ou **C — sanar pendências de direitos** antes de considerar qualquer distribuição. Nenhuma delas implica autorização para merge/release.
