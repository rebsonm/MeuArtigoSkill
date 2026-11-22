# Meu Artigo RC.1 — Continuidade T02: verificação efetiva de acesso ao host ChatGPT

**Data:** 22/11/2026 (America/Fortaleza). **PR:** [#112](https://github.com/rebsonm/MeuArtigoSkill/pull/112). **Commit documental de entrada:** `2c2e6dfc27faf49c70e84083ac9cf6df7767d10b`, Draft, sem merge. **Documento de referência:** `knowledge/methodology/intake/RC1-HOST-T02-READBACK-PREFLIGHT-2026-11-22.md`. **Resultado formal deste passo:** `CANDIDATE_SOURCE_PASS; HOST_INSTALLED_BUILD_UNKNOWN; T02_HOST_NOT_RUN; RECEIPT_UNAPPROVED; NO_GO`.

## 1. Identificação que realmente é possível comprovar

A identidade do **artefato CI candidato** está confirmada; a identidade do **build efetivamente salvo/executado pelo host ChatGPT** **NÃO está confirmada**. Não são equivalentes:

- Run GitHub Actions [#44985770042](https://github.com/rebsonm/MeuArtigoSkill/actions/runs/44985770042), artifact ID `14740270362`; ZIP candidato de instalação gerado desse run e verificado por bytes.
- SHA-256 do ZIP padrão fixado: `fa6431207c25dd21cbd60428ccbd3d9a660c100423015499f1bcae25e9d3947d`.
- SHA-256 do `BUNDLE_MANIFEST.json` original: `c92edafbceba7df2e53a5b55cca788b5827c1cd1161da9ce298e692fc079f3a9`.
- `VERSION`/manifesto: `1.0.0-rc.1`; `build_source_commit`: `48407b55a851ba8e07b1468330c31d3bd97ffafd`; 152 arquivos do manifesto.
- SHA-256 **original** `agents/openai.yaml`: `a19fed5da9d342bcd546b8e5b5a4a994af620d98bd4a29bf5df697f8d854a8ed`; **original** `assets/icon.svg`: `c71cbfd42e483104a03ed2f8c2aa2c1f8b44c3bca15d0e618be7ecb1f15a6528`.
- Um ZIP RC.1 **anterior** possui SHA-256 `07b13b38646f45a1a8cdb5326f46fd4e7cab0a99ca6cf7c0c45436ca5500f5af`, manifesto `330d114a9bd8ef29b8cb01b37242c6d5e71696ee607ef2123956bcb64fdf6e25`, build source `7e9b26d5...`. **Não tratar versões nominais iguais como bytes iguais.** A fonte CI anterior e a posterior não provam qual está instalada no ChatGPT.

## 2. Verificações realmente executadas nesta continuidade

1. O kit fornecido na etapa anterior (`KIT_T02_HOST_REAL_UNAPPROVED.zip`) e o ZIP candidato foram localizados **somente no diretório temporário** `/mnt/data/t02_host_rc1_20261122`. A pasta é cópia de teste isolada e **não corresponde a uma instalação persistida pelo ChatGPT**.
2. O utilitário fornecido `host_t02_preflight.py` foi **executado sem `--actual-installed-root`**, com o ZIP exato e diretório externo de saída. A execução produziu:
   ```json
   {
     "candidate_source_status": "PASS",
     "actual_host_installation": "NOT_RUN",
     "host_readback": "NOT_RUN",
     "host_reviewed": false,
     "t02_accepted": false,
     "manifest_sha256": "c92edafbceba7df2e53a5b55cca788b5827c1cd1161da9ce298e692fc079f3a9",
     "build_source_commit": "48407b55a851ba8e07b1468330c31d3bd97ffafd"
   }
   ```
   O processo ter retornado código 0 indica **preflight do ZIP** concluído, **não** aceite do host.
3. Independente do utilitário, o ZIP candidato foi lido em memória: SHA-256 original YAML e SVG coincidiram com o manifesto; YAML de origem é UTF-8 com chave `interface:`; SVG de origem é XML com raiz `svg`, 48 nós, sem elementos de script/foreignObject observados nesta inspeção de estrutura. **Não foram vistos nem inspecionados conteúdos YAML/SVG instalados ou políticas injetadas pelo host.** Não inferir segurança geral ou revisão humana a partir de um exame estrutural da fonte.
4. A superfície `skills__list` acessível nesta sessão expôs **98 skills de plugins**, nenhuma chamada Meu Artigo. **Essa listagem não é um inventário completo das Skills pessoais efetivamente instaladas no ChatGPT**; não prova ausência ou presença da Skill do usuário. Não há ferramenta disponibilizada nesta sessão que retorne bytes de Save/readback da instalação no host. Não foi fornecido caminho comprovadamente persistido por operador autorizado.
5. Criado arquivo externo `T02_HOST_READBACK_ACCESS_AUDIT_20261122.json`, **3.035 bytes**, SHA-256 `f6d73f6ad7dcbd278cac734cd4eb3f74be24b302067d8bb84c349eea609c8e6e`, com a matriz de acessos e `reviewed=false`. A saída `host_preflight_UNAPPROVED.json` fica fora de qualquer instalação. Não houve criação de recibo assinado/revisado nem modificação da Skill.

## 3. Matriz de evidências e status

| Verificação | Resultado | Evidência / limitação |
|---|---|---|
| Kit anterior e ZIP fixado existentes | **PASS** | Leitura de arquivos locais; não são instalação host |
| Hash do ZIP do candidato | **PASS** | SHA-256 fixado conferido pelo script |
| Build/version/manifesto de origem | **PASS_SOURCE** | `1.0.0-rc.1`, `48407b55...`, manifesto pinado |
| YAML e SVG de origem | **PASS_SOURCE_HASH/STRUCTURE** | SHA exato, UTF-8/XML; não prova integridade pós-Save |
| Lista acessível de skills de plugins | **OBSERVED_ONLY** | 98 entries, nenhum item Meu Artigo; resultado não é prova de instalação ausente |
| Identidade do executável **realmente instalado** | **NOT_RUN** | Sem API/caminho autenticado de readback |
| Save, reabertura e evidência do host | **NOT_RUN** | Não houve ação real de Save/reabertura |
| SHA de manifesto **instalado** e 152 payloads | **NOT_RUN** | Nenhum arquivo da instalação real foi fornecido |
| Diferenças do YAML/SVG host x origem | **NOT_RUN** | Não há bytes pós-save |
| Revisão de políticas YAML e SVG **instalados** | **NOT_RUN** | Sem conteúdo instalado nem revisor efetivo |
| Recibo externo operador, `reviewed=true` | **NOT_RUN / PROIBIDO PRESUMIR** | Único registro disponível é não aprovado |
| `verify_installed_bundle.py --host-receipt` no real | **NOT_RUN** | Sem instalação nem recibo válido |
| T02 no host ChatGPT | **NOT_RUN / NO-GO** | Não é sucesso nem reprovação da instalação |
| T05/T06/T32/T33/T34 no host | **NOT_RUN** | Ensaios de sandbox prévios não foram promovidos a host |

## 4. Próxima ação executável pelo operador com acesso ao host

**Não reinstalar nem substituir para produzir prova retroativa.** O operador deve localizar a Skill atualmente executada no host; comprovar a identidade e o Save/readback de **seus** bytes e logs; usar o kit candidato fixado, que contém o verificador confiável, fora da instalação; rodar:

```bash
python host_t02_preflight.py \
  --candidate-zip MeuArtigoSkill-v1.0.0-rc.1-CANDIDATE.zip \
  --actual-installed-root /DIRETORIO/REAL/PERSISTIDO/PELO/HOST \
  --external-output /CAMINHO/SEGURO/FORA/DA/SKILL
```

Esse comando **não autentica o host sozinho**: o operador precisa comprovar a proveniência do diretório. Exigir verificação estrita com `--expected-version 1.0.0-rc.1 --expected-manifest-sha256 c92edafb...`. Se houver mudanças **somente** em `agents/openai.yaml` e `assets/icon.svg`, revisar diferenças de bytes, política e conteúdo e gerar **recibo externo do host real** com identificação/revisão efetivas; jamais marcar `reviewed=true` sem evidência. Qualquer outra alteração é bloqueio. Se o host não disponibilizar arquivos executáveis persistidos, manter `NOT_RUN` e usar meios suportados/operador do host para obter atestação — não fabricar caminho, hashes ou recibos a partir de ZIP original. Proteger YAML privado, logs e políticas contra exposição em PR pública.

## 5. Continuidade e restrições

**FEITO:** pin de origem e acesso executados/registrados; **EM EXECUÇÃO:** obtenção de evidência de Save/readback real; **PRÓXIMO:** decisão entre obter export/atestado do host ou mudar para ensaios funcionais/clearance autoral, sem equivalência indevida. A PR #112 fica Draft; sem merge/tag/release, sem revisão científica/copyright, sem mudança no `BUNDLE_MANIFEST.json`, `agents/openai.yaml`, `assets/icon.svg`, instalação, acervo privado, ACL ou gates metodológicos. Este é **registro aditivo**, não substituto do relatório anterior.
