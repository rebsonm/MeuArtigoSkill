# Meu Artigo RC.1 — preflight verificável para homologação T02 no host ChatGPT

**Data:** 2026-11-22 (America/Fortaleza). **PR:** [#112](https://github.com/rebsonm/MeuArtigoSkill/pull/112). **HEAD analisado:** `9edc6f1fbb0d640efc9c8ea09eee4e009b475759` (Draft, não mesclado). **Protocolo obrigatório:** [`docs/HOST_PRESENTATION_ATTESTATION.md`](https://github.com/rebsonm/MeuArtigoSkill/blob/9edc6f1fbb0d640efc9c8ea09eee4e009b475759/docs/HOST_PRESENTATION_ATTESTATION.md). **Estado:** `PASS_SOURCE_ZIP_ONLY; HOST_ACTUAL_INSTALLATION_NOT_RUN; HOST_RECEIPT_UNREVIEWED; RELEASE_NO_GO`.

## 1. Revisão de candidato e pin criptográfico

Foi recuperado *nesta sessão* o artefato de instalação RC.1 gerado pela CI **no HEAD mais recente** da PR: [Release audit run 44985770042](https://github.com/rebsonm/MeuArtigoSkill/actions/runs/44985770042), `completed/success`, artifact ID **14740270362** (`MeuArtigoSkill-rc-test-only`). Este ZIP externo contém um ZIP de instalação padrão sem PDFs de terceiros.

| Objeto inspecionado | SHA-256 de bytes efetivamente obtidos |
|---|---|
| ZIP externo (artifact GitHub 14740270362, 602445 B) | `1203ead80e33c954d4afb8e1aeb52b31b67e2af70030b0f1b1c578e431a61f32` |
| `MeuArtigoSkill-v1.0.0-rc.1.zip` aninhado, 610385 B | `fa6431207c25dd21cbd60428ccbd3d9a660c100423015499f1bcae25e9d3947d` |
| `BUNDLE_MANIFEST.json` extraído deste ZIP | `c92edafbceba7df2e53a5b55cca788b5827c1cd1161da9ce298e692fc079f3a9` |
| `agents/openai.yaml` de origem | `a19fed5da9d342bcd546b8e5b5a4a994af620d98bd4a29bf5df697f8d854a8ed` |
| `assets/icon.svg` de origem | `c71cbfd42e483104a03ed2f8c2aa2c1f8b44c3bca15d0e618be7ecb1f15a6528` |

**Identidade do executável declarada no manifesto:** `VERSION=1.0.0-rc.1`; `manifest.version=1.0.0-rc.1`; `build_source_commit=48407b55a851ba8e07b1468330c31d3bd97ffafd`; 152 arquivos referenciados no manifesto (+ arquivo manifesto, total 153). O `build_source_commit` é diferente do HEAD posterior da PR porque os relatórios documentais têm commits adicionais. Não usar o HEAD como substituto desse campo.

**Divergência histórica IMPORTANTE:** o ZIP RC.1 do ensaio offline anterior (CI #44985272850) tinha SHA-256 interno `07b13b38646f45a1a8cdb5326f46fd4e7cab0a99ca6cf7c0c45436ca5500f5af`, manifest SHA `330d114a9bd8ef29b8cb01b37242c6d5e71696ee607ef2123956bcb64fdf6e25`, `build_source_commit=7e9b26d50229758cec6aa0fb07ae10d96eea276f`. Isso **não é a mesma construção binária**, apesar do mesmo número de versão. Recibos de uma versão não podem aceitar os bytes da outra.

## 2. Verificações executadas de fato

- ZIP externo SHA-256 bate com o digest da API de artefatos GitHub. SHA-256 do ZIP interno, manifesto, YAML e SVG recalculados e contrastados com metadados/manifesto de origem.
- **Cópia extraída em sandbox:** `scripts/verify_installed_bundle.py --root [cópia temporária] --expected-version 1.0.0-rc.1 --expected-manifest-sha256 c92edafbceba7df2e53a5b55cca788b5827c1cd1161da9ce298e692fc079f3a9` retornou `status=PASS`, `ALL_BUNDLE_BYTES_EXACT`, 152 arquivos, zero ausentes/divergentes; **isso não é um teste do host instalado**.
- Em sandbox, o `--emit-host-receipt-draft` retorna JSON de recibo **NÃO APROVADO**, `reviewed=false`, `reviewer=""`, `transformed_assets=[]`, e exit code **2** como esperado. A lista vazia de transformações se refere **apenas à cópia extraída**, não aos ativos salvos pelo ChatGPT.
- Utilitário externo de preflight, criado nesta sessão e distribuído em kit de evidências sem PDFs, aceitou apenas o ZIP correspondente ao pin e rejeitou um arquivo de entrada incorreto com `CANDIDATE_ZIP_SHA256_MISMATCH`/exit 2. Quando chamado sem diretório real, relata explicitamente `actual_host_installation=NOT_RUN`, `host_readback=NOT_RUN`, `host_reviewed=false`, `t02_accepted=false`. Um teste do utilitário contra **cópia temporária**, intencionalmente rotulado `OPERATOR_SUPPLIED_DIRECTORY_INSPECTED_NOT_PROVEN_CHATGPT_HOST`, não é atestado de host.
- O catálogo de *plugin skills* acessível por esta sessão não forneceu caminho/bytes da Skill Meu Artigo efetivamente salva como personalização da conta; tampouco a pasta de sandbox `/mnt/data` corresponde ao host. **Não foi observada operação Save ou readback real da instalação.** Isto não prova que a Skill inexiste na conta: prova apenas ausência de superfície de leitura de sua instalação no ambiente atual.

## 3. Matriz de aceite — prova versus lacuna

| Critério | Prova observada | Veredito sobre o host |
|---|---|---|
| Origem da candidata e pacote | CI real e hashes externo/interno/manifesto recalculados | `PASS_SOURCE_ONLY` |
| Versão e identidade da candidata | `1.0.0-rc.1`, build `48407b55...` | `PASS_SOURCE_ONLY` |
| 152 payloads íntegros na cópia extraída | Verificador estrito `ALL_BUNDLE_BYTES_EXACT` | `PASS_SANDBOX_ONLY` |
| Identificar diretório EXECUTADO no host | Não há caminho/readback do host acessível | **`NOT_RUN`** |
| Manifesto/SHA instalado versus original | Sem bytes persistidos após Save no host | **`NOT_RUN`** |
| YAML/SVG efetivamente transformados pelo host | Somente SHA dos **originais**; não há SHA ou conteúdo instalado | **`NOT_RUN`** |
| Revisão substancial da política YAML / segurança SVG **instalados** | Não efetuada sobre arquivos do host | **`NOT_RUN`** |
| Recibo externo com operador e evidência real de readback | Rascunho `reviewed=false`, sem revisor ou Save | **`NOT_RUN` / `UNAPPROVED`** |
| Verificador final com `--host-receipt` real | Não executado (sem recibo válido) | **`NOT_RUN`** |
| T05, T06, T32, T33, T34 na instalação gerenciada | Não executados no host; resultado offline do ZIP é independente | **`NOT_RUN`** |
| Aprovação de direitos de PDF e sete gates científicos | Não demonstrada | `BLOCKED` / `PENDING` |

**Decisão:** `T02_HOST_NOT_RUN` e `NO_GO` para declarar a Skill instalada/homologada. Não confundir integridade do ZIP, resultado de CI, teste local ou rascunho de recibo com evidência de uso ou instalação no ChatGPT.

## 4. Procedimento pronto para operador real (sem gerar aprovação fictícia)

1. **Não reinstalar nem sobrescrever a instalação apenas para fabricar PASS.** Identificar a Skill efetivamente salva, responsável, ID/contexto do host, caminho de execução persistido, logs de Save e readback pós-save. Se o host não expuser esses bytes, registrar `NOT_RUN`.
2. Obter ZIP exato do run **44985770042** e comparar seu SHA-256 interno com `fa6431207...`; extrair o verificador de dentro de **ZIP verificado**, executando contra o **diretório do host** de leitura autorizada (não confiar em verificador modificado pela instalação). Comando de referência:

   ```bash
   python scripts/verify_installed_bundle.py \
     --root /ACTUAL/HOST/SAVED/SKILL \
     --expected-version 1.0.0-rc.1 \
     --expected-manifest-sha256 c92edafbceba7df2e53a5b55cca788b5827c1cd1161da9ce298e692fc079f3a9
   ```

3. No modo estrito, qualquer divergência tem `FAIL`. Somente os dois caminhos `agents/openai.yaml` e `assets/icon.svg` podem ser candidatos a **revisão de apresentação gerenciada**, nunca dispensa tácita. Toda outra divergência é bloqueio.
4. Gerar rascunho **do instalado real** (não do ZIP de origem): `python scripts/verify_installed_bundle.py --root /ACTUAL/HOST/SAVED/SKILL --emit-host-receipt-draft > /EXTERNAL/SECURE/host-receipt.json`. Exit code 2 é intencional. O rascunho identifica hashes de origem e hashes instalados observados; manter fora da instalação.
5. Operador nomeado examina *conteúdo pós-save*: YAML UTF-8 `interface`, `default_prompt`, políticas injetadas, permissões, referências externas e possíveis instruções de dados/privacidade; SVG XML seguro (sem elementos executáveis, eventos, `href/src`, `data:`, `javascript:`, imagens/referências remotas), inclusive comparação de conteúdo e hashes. **Só depois de revisão real**, preencher `reviewer`, `review_evidence` (>=30), `host_save_readback_evidence` (>=20), e `reviewed=true` onde efetivamente aplicável. Evidência de Save/readback tem que corresponder aos **bytes instalados** após salvar.
6. Executar novamente com `--host-receipt /EXTERNAL/SECURE/host-receipt.json --expected-manifest-sha256 c92edafb...`. Para transformações permitidas, exigir `PASS` e `CORE_EXACT_HOST_PRESENTATION_ATTESTED` com zero divergências não reconhecidas; se nenhuma transformação ocorreu, exigir `ALL_BUNDLE_BYTES_EXACT` e prova separada de Save/readback. Não publicar política/recibo privado no GitHub.
7. Executar e registrar T05/T06/T32/T33/T34 **separadamente** no host, em ambiente fictício e seguro, sem mudar decisões científicas reais. Anotar `PASS/FAIL/NOT_RUN` por teste.

O operador deve conservar o recibo externo seguro e um resumo de hashes/IDs sem dados sensíveis nos comentários da PR #112 e do MD de continuidade. A existência de um recibo JSON não é assinatura criptográfica do ChatGPT.

## 5. Próximas escolhas (sem autorização automática)

**A (recomendado):** executar Save/readback na instância real por operador autorizado e trazer evidência verificável; **B:** documentar alternativas suportadas caso a instalação do host não exponha bytes; **C:** resolver governança/autorização autoral antes de qualquer distribuição futura. A PR permanece Draft, sem merge/tag/release, alteração de `agents/openai.yaml`/`assets/icon.svg`, PDF, allowlist, ACL, gates, ou reescrita de histórico Git.
