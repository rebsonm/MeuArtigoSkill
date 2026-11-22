# Meu Artigo v1.0.0-rc.1 — preflight técnico de publicação (22/11/2026)

**Escopo:** preparação reprodutível de publicação técnica, **sem merge, tag, release, reinstalação ou mudança da lista de PDFs**. Este documento registra fatos observados até 22/11/2026 no estado **GitHub PR #112 Draft**, não é atestado de instalação em ChatGPT nem de autorização de publicação.

## Identidades congeladas (NÃO confundir commits)

| Campo | Valor e origem |
|---|---|
| Repositório/PR | `rebsonm/MeuArtigoSkill`, [PR #112](https://github.com/rebsonm/MeuArtigoSkill/pull/112), base `main`, Draft, merged=false |
| **PR HEAD inspecionado antes das alterações documentais** | `cc74f7f738db39dce19f5d1253dd17e295dd8146` |
| **Build source GitHub Actions** | `79deb997e1208db90190be7905421b3036c2dbd1` — merge de teste de `cc74f7f738db39dce19f5d1253dd17e295dd8146` em `29458793b800a83b7ae9727af7eef2495547a4cd` |
| Equivalência build × PR | GitHub compare `cc74f7f738db39dce19f5d1253dd17e295dd8146..79deb997` → `ahead_by=1`, **0 arquivos divergentes**; os seis arquivos de identidade verificados `SKILL.md`, `scripts/verify_installed_bundle.py`, `VERSION`, `agents/openai.yaml`, `CHANGELOG.md`, `README.md` têm blobs idênticos |
| GitHub Actions | [Release audit #45033085251](https://github.com/rebsonm/MeuArtigoSkill/actions/runs/45033085251), `completed/success`; job audit `success` |
| Suíte | **1.041 testes**, **0 falhas, 2 skipped** (CI Python **3.12.16**) |
| Artefato externo de CI | [`MeuArtigoSkill-rc-test-only`, ID 14757923364](https://github.com/rebsonm/MeuArtigoSkill/actions/runs/45033085251/artifacts/14757923364), tamanho **602.437 bytes** |
| SHA-256 do ZIP **externo** de CI | `c1a6053ec12648eae60120a27adbfcd22a5906dc972506536e47cf96d5b61597` |
| ZIP **interno instalável** | `MeuArtigoSkill-v1.0.0-rc.1.zip`, tamanho **610.386 bytes** |
| SHA-256 do ZIP **interno instalável** | `c023560c0e1fbedfce72c963b98d8f930cd99adc1f5a07b3765361c968a53539` |
| SHA-256 do manifesto interno | `ed06446142d2473d21258a4f0a4a611aeb8408d9fc70f9b47759938e434ebd80` |
| Versão em `VERSION` e `CITATION.cff` | `1.0.0-rc.1`, sem `date-released` |
| Estado de publicação | `source_release_channel=release-candidate`, `publication_verified=false`, `scientific_quality_validated=false`, `release_metadata=READY_FOR_CANDIDATE_TESTING`, `public_release_authorized=false` |

**Importante:** commits de notas de release/dossiê feitos **após** o HEAD de origem alteram o SHA documental da PR. Eles **não mudam retroativamente** o conteúdo deste ZIP de CI. Antes da publicação final, conferir que a fonte executável do release corresponde à candidata examinada e decidir se um novo build é necessário.

## Resultado da verificação realizada nesta sessão

1. Baixado **via conector GitHub** o artefato ID 14757923364 do workflow acima; SHA-256 externo calculado diretamente: **MATCH** com digest GitHub Actions.
2. ZIP externo examinado: possui **exatamente três arquivos**: `MeuArtigoSkill-v1.0.0-rc.1.zip`, `SHA256SUMS.txt` e `BUNDLE_BUILD_RECEIPT.json`; os dados de SHA, versão, distribuição e build-source entre os três **coincidem**.
3. ZIP instalável interno: `zipfile.testzip()=None` (**CRC PASS**); contém **153 entradas**, das quais **152 payloads** e `BUNDLE_MANIFEST.json`; não há caminhos absolutos, traversal `..`, links simbólicos ou nomes duplicados. **Nenhum PDF nem card externo embutido**; o repositório e a biblioteca pública opcional permanecem separados da Skill instalada.
4. `BUNDLE_MANIFEST.json` registra **152 hashes SHA-256**. Todos os 152 arquivos da candidata estão presentes e **152/152 SHA-256 conferidos**; `missing=0`, `extra=0`, `mismatched=0`. `SKILL.md` fica na raiz, como indicado no guia de instalação.
5. Executado o verificador real, extraído do próprio ZIP, **apenas sobre uma cópia temporária controlada**:
   ```sh
   python scripts/verify_installed_bundle.py \
     --root /PATH/TO/EXTRACTED/CANDIDATE \
     --expected-version 1.0.0-rc.1 \
     --expected-manifest-sha256 ed06446142d2473d21258a4f0a4a611aeb8408d9fc70f9b47759938e434ebd80
   ```
   Saída: `status=PASS`, `integrity_mode=ALL_BUNDLE_BYTES_EXACT`, `payload_count=152`, `expected_version_matches_executable=true`, `manifest_pinned=true`, `unresolved_mismatches=[]`. **T01/T02 do host continuam NOT_RUN**, pois a origem verificada é o ZIP extraído e não a pasta da Skill realmente salva no ChatGPT.

## Dependências e compatibilidade — conclusão estritamente verificável

| Recurso | Evidência | Estado / limite |
|---|---|---|
| Núcleo da Skill | `SKILL.md`, `agents/openai.yaml`, referências, 63 scripts Python no ZIP | **PASS estrutura/sintaxe AST de 63 scripts neste ambiente**; execução de todos em host não comprovada |
| Python | CI real em **Python 3.12.16**, análise AST local em **Python 3.13.5** | **PASS CI 3.12**; disponibilidade de Python em ChatGPT/Claude/Gemini **não garantida** |
| Formatos CSV/JSON | Mecanismos base e testes automatizados CI | **PASS em escopo CI/sandbox**; Drive remoto e planilhas nativas não são automaticamente sincronizados |
| XLSX visual opcional | `artifact_tool` em `build_matrix_template.py`; fallback CSV previsto | `artifact_tool` presente **neste** ambiente; host ChatGPT `NOT_RUN`; `xlrd` para XLS legado **não instalado localmente** |
| PDFs / figuras | `pypdf`, `PyMuPDF (fitz)`, `Pillow (PIL)` em módulos específicos, importados condicionalmente | Disponibilidade no host varia; não prometer OCR, leitura de todos os arquivos ou dependência empacotada |
| XLSX import/dedupe | `openpyxl` quando a funcionalidade é executada | Disponível no sandbox de inspeção, mas não garantido na instalação real |
| HTTPS / GitHub remoto | Leitores em `scripts/consult_*py` e `public_method_pdf.py` exigem conectividade e permissão | Biblioteca externa de **649 cards** e **51 PDFs** catalogados não entra no ZIP de instalação; consulta sob demanda e pinada por commit |
| Google Drive | `GOOGLE_DRIVE_FIRST`; conexão e escrita autorizadas por **cada pesquisador** | A instalação não conecta automaticamente o Drive pessoal do mantenedor, não concede tokens nem prova sincronização |
| MCP Apps/interface proprietária | Integração opcional de ferramentas já conectadas; demo HTML fictícia | **Não** há prova de servidor MCP próprio autenticado, painel de produção ou conexão automática |
| ChatGPT / Claude / Gemini | Documentação de compatibilidade por plataforma | **Compatibilidade condicional**, não homologação de RC.1 em contas reais |

A candidata é uma Skill textual com scripts utilitários. **Nenhum arquivo `requirements.txt` ou `pyproject.toml`** foi incluído no ZIP instalável; bibliotecas opcionais são capacidades do ambiente e devem apresentar fallback/limite em caso de ausência. Nenhuma dependência foi instalada, alterada ou disponibilizada ao usuário por este preflight.

## Changelog e notas de release

- O [`CHANGELOG.md`](../../../CHANGELOG.md) **já contém a seção `1.0.0-rc.1 — UNRELEASED`** com a evolução de controles de DEC/TRACE, rotas, rastreabilidade, biblioteca metodológica, melhorias da inicialização e procedimentos de Drive/host. **Não reescrever históricos nem acrescentar data de lançamento antes de publicar**.
- O `CITATION.cff` declara versão `1.0.0-rc.1`, autor e Apache-2.0, **sem `date-released`**. O DOI registrado se refere ao software/registro arquivado, não prova depósito desta versão.
- Criado rascunho de notas: [`docs/RC1-RELEASE-NOTES-DRAFT-2026-11-22.md`](../../../docs/RC1-RELEASE-NOTES-DRAFT-2026-11-22.md) com descrição, novidades, limitações, checksums e instruções de instalação. Está **DRAFT_NOT_PUBLISHED**.
- **Alterações a deixar para o ato de release, não executadas agora:** aprovar a versão exata de pacote; verificar/atualizar links de instalação e README que ainda recomendam beta.6; validar texto final do changelog, data e referência de release, associar tag e checksums ao mesmo commit/release; publicar GitHub pre-release somente mediante decisão separada do mantenedor.

## Testes pendentes (e o que NÃO repetir)

| ID/frente | Evidência já existente | Pendência concreta para aceite no host |
|---|---|---|
| T01 | ZIP, `VERSION`, `CITATION.cff`, manifesto e checksum **PASS** no pacote | **NOT_RUN** na Skill efetivamente instalada/salva |
| T02 | Manifesto 152/152 e verificador estrito **PASS no ZIP extraído**; histórico de 2 arquivos de apresentação transformados em outro host | **NOT_RUN:** obter readback do host, revisar YAML/SVG instalados, recibo externo realmente revisado, verificar 152 payloads contra manifest original |
| T05/T06 | PASS em fixture local de outra execução da RC.1: metadados CSV 8 linhas, XLSX 21 planilhas | Só smoke de host para inicialização/artefato XLSX; não repetir indiscriminadamente regressões e CI |
| T32 | PASS parser local sobre conteúdo não confiável, 11/11 cenários sintéticos CI | **NOT_RUN LLM host:** comportamento real da Skill diante de texto externo malicioso |
| T34 | PASS leitura documental de seis arquivos Drive, gates pendentes e 0 decisões; driver local não declarado | **NOT_RUN motor host:** retomada de projeto fictício no Drive por execução da Skill realmente instalada |
| Isolamento entre pesquisadores | Políticas e docs determinam projeto/Drive por pesquisador | Teste entre contas separadas, sem acesso ao armazenamento privado do mantenedor |
| Issues #102/#103 | Registro GitHub público documenta histórico de direitos e IDs privados | Permanecem `open`; não declarar histórico/forks/permissões saneados por PASS do audit HEAD |

**Demais testes T01–T34:** [matriz consolidada](RC1-T01-T34-CONSOLIDATED-MATRIX-2026-11-22.md); não transformar `PASS_HISTORICAL` em `PASS_HOST`. A CI do SHA inspecionado executou **1.041 testes automatizados com zero falhas e dois skipped**; **11/11 cenários integrados sintéticos** passaram. Isto elimina necessidade de repetir os mesmos testes de unidade sem mudança funcional.

## Checklist antes de eventual GitHub pre-release — sem executar nesta etapa

- [x] Origem da build reconciliada com HEAD da PR no instante do snapshot.
- [x] Artefato CI baixado, ZIP interno e checksum pinados, manifesto/versão/verificador 152/152.
- [x] Licença e citação do software conferidas; changelog `UNRELEASED` existente.
- [x] Minuta de release notes gravada sem publicar.
- [x] CI mais recente do SHA de origem passou: 1.041 testes, dois skips.
- [ ] Validar host real T01/T02 (e smoke T05/T06, T32/T34) **ou**, se o mantenedor optar por pre-release com limitações, deixar `NOT_RUN` explicitamente público.
- [ ] Verificar isolamento de armazenamento em ambiente multiusuário; não afirmar compatibilidade plena antes disso.
- [ ] Decidir tratamento dos riscos históricos #102/#103 antes de anunciar que estão encerrados ou que o repositório não apresenta exposição.
- [ ] Revisar o candidato **exato** após as alterações documentais desta PR e confirmar checksums/artefatos do commit escolhido para a release.
- [ ] Decisão expressa de publicação pelo mantenedor; escolher GitHub **pre-release** (não estável), tag e anexos `MeuArtigoSkill-v1.0.0-rc.1.zip`, `SHA256SUMS.txt`, notas, recibo **sem alegar execução de host**.
- [ ] Atualizar documentação de usuário após publicação, apontando para a release real e não para a beta.6.

**Decisão desta etapa:** `CANDIDATE_ARTIFACT_VERIFIED / SOURCE_ZIP_STRICT_PASS / CI_SUCCESS / PUBLICATION_NOT_EXECUTED`. PR #112 permanece Draft, sem merge, tag, release ou alteração de PDFs, permissões, gates e projetos Drive. Não houve contato editorial.
