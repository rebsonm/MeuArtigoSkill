# Meu Artigo v1.0.0-rc.1 — release notes (DRAFT, NOT PUBLISHED)

> **Release candidate / pré-release experimental proposta.** O texto abaixo destina-se à revisão do mantenedor **antes** de qualquer tag, merge em `main` ou publicação de GitHub Release. Não chamar de estável, aprovada cientificamente ou homologada no host.

## Visão geral

**Meu Artigo** é uma Skill para apoiar a construção, continuidade, auditoria e documentação de artigos científicos com C.A.D.A. (Capturar, Atribuir, Definir prazo/próximo passo, Acompanhar), governança de evidências, decisões científicas humanas e rastreabilidade entre fontes e alegações. O usuário continua responsável pelas decisões e validações científicas.

Esta **v1.0.0-rc.1** é uma candidata experimental para teste em ambiente compatível. A versão pública experimental anterior **v0.9.0-beta.6** permanece inalterada até decisão e publicação específicas.

## O que mudou nesta candidata

Resumo conservador do [CHANGELOG.md](../CHANGELOG.md) já presente na PR e de sua integração posterior:

- Integração operacional e reconciliação documental dos 15 workpackages V1 e 20 IB, com inventários de **475 fichas bibliográficas [P]**, **174 cards editoriais [I]/[P]**, e catálogo de **51 PDFs** externos ao ZIP padrão, consultáveis apenas nos limites e capacidades realmente disponíveis.
- Correções e rechecagem de 13 notas editoriais no livro de disposições; preservação da quarentena de entradas bloqueadas, sem confundir cards com evidência científica primária ou revisão independente.
- Continuidade mais conservadora: navegação pelo próximo passo registrado, identificação do bloqueio prioritário, conservação de decisões DEC, TRACE e sete gates humanos `GATE-0001..0007`.
- Reforço do isolamento de armazenamento: preferência por Google Drive **do próprio pesquisador**, verificação de permissões, leitura após escrita e recusa de sincronização presumida; fallback local só com consentimento específico.
- Diagnósticos de versão e integridade, incluindo verificador SHA-256 de todos os payloads e procedimento para observar transformações de `agents/openai.yaml`/`assets/icon.svg` após salvar a Skill, sem alterar o manifesto original nem aceitar recibo não revisado.
- Testes sintéticos adicionais, scanner de credenciais no código rastreado, checagens de links/proveniência, demonstração de mapa interativo **fictício** sem conexão de produção.
- Melhorias em instalação multiplataforma e interface de conversação com idioma adaptado ao pesquisador; não assume acesso a Web of Science, Scopus, Drive, ferramentas de protocolo externo ou recursos pagos.

## Compatibilidade e dependências

- **ChatGPT:** importação de Skills e execução de scripts dependem dos recursos efetivamente oferecidos pela conta/ambiente. A RC.1 ainda **não** possui certificado de instalação, persistência/readback ou execução end-to-end no host ChatGPT.
- **Claude/Claude Code e Gemini:** uso da Skill onde houver suporte de importação, arquivos e ferramentas; compatibilidade real dessa candidata **não homologada** nessas plataformas.
- **Python e HTTPS:** alguns leitores opcionais usam Python e conexão HTTPS a commit GitHub imutável; quando indisponíveis, permanece o núcleo metodológico documentado da Skill, sem alegação de consulta externa.
- **Bibliotecas opcionais:** `artifact_tool` para visualização XLSX (CSV permanece canônico), leitores PDF como `pypdf`/`PyMuPDF (fitz)`, `Pillow` para imagem, `openpyxl` para XLSX e `xlrd` para XLS legado, conforme módulos e fluxos realmente executados. Não existe garantia de que cada ambiente tenha todas essas dependências.
- **Armazenamento:** cada pesquisador conecta o **próprio** Drive quando deseja utilizá-lo. Instalar a Skill não concede acesso ao Drive do mantenedor nem instala ou conecta automaticamente um servidor externo de ferramentas gerenciado pelo projeto. O GitHub oferece o catálogo metodológico público de leitura opcional, **não** é a memória canônica de projetos particulares.

## Evidência da candidata (em 22/11/2026)

- PR [#112](https://github.com/rebsonm/MeuArtigoSkill/pull/112), commit de entrada `cc74f7f738db39dce19f5d1253dd17e295dd8146`, **Draft**.
- CI [Release audit #45033085251](https://github.com/rebsonm/MeuArtigoSkill/actions/runs/45033085251), status `completed/success`; **1.041 testes, 0 falhas, 2 skipped**.
- Artefato temporário [MeuArtigoSkill-rc-test-only](https://github.com/rebsonm/MeuArtigoSkill/actions/runs/45033085251/artifacts/14757923364) — **não é GitHub Release**. Extraia primeiro o ZIP externo de CI; instale somente seu `MeuArtigoSkill-v1.0.0-rc.1.zip`.
- SHA-256 do **ZIP instalável interno**: `c023560c0e1fbedfce72c963b98d8f930cd99adc1f5a07b3765361c968a53539`.
- SHA-256 do **BUNDLE_MANIFEST.json** interno: `ed06446142d2473d21258a4f0a4a611aeb8408d9fc70f9b47759938e434ebd80`.
- O pacote contém **152 payloads com hashes verificados (152/152)** e um manifesto externo à lista, total de 153 entradas, sem PDF de terceiros e sem os cards de referência externos. O checksum `SHA256SUMS.txt`, `VERSION`, `CITATION.cff`, recibo e manifesto correspondem ao pacote.
- O recibo de build aponta para `79deb997e1208db90190be7905421b3036c2dbd1`, commit temporário do merge de `cc74f7f7` em `29458793`. Comparação GitHub com o HEAD da PR: **zero diferenças de arquivo**.
- O verificador `scripts/verify_installed_bundle.py`, invocado sobre a **cópia extraída do ZIP** com versão e manifesto explicitamente pinados, retornou `status=PASS`, `integrity_mode=ALL_BUNDLE_BYTES_EXACT` e `payload_count=152`. Isso **não é** o teste da instalação real.

## Limites conhecidos e pendências para liberar a RC.1

- **T01/T02 HOST NOT_RUN:** identificação do executável efetivamente salvo e hashes/readback pós-Save. Se o host transformar YAML/SVG, usar apenas recibo externo que tenha conteúdo efetivamente revisado e revisão nominal, nunca `reviewed=true` automático.
- **T05/T06 HOST NOT_RUN:** localmente CSV 8 registros e XLSX 21 abas deram PASS, mas a disponibilidade de `artifact_tool` pode variar; fallback para CSV.
- **T32:** parser sintético foi aprovado, mas **não** há prova do comportamento do LLM da instalação real diante de conteúdo hostil recuperado.
- **T34:** leitura documental de projeto fictício no Drive passou, mas a **integração end-to-end da Skill instalada** e sincronização via conector Drive não foram demonstradas.
- **Isolamento multiusuário:** lógica/documentação apontam Drive individual; teste entre contas independentes em host ainda não foi realizado.
- **Issues [#102](https://github.com/rebsonm/MeuArtigoSkill/issues/102) e [#103](https://github.com/rebsonm/MeuArtigoSkill/issues/103):** riscos históricos públicos e de metadados privados estão documentados e permanecem abertos. Não afirmar que um audit de HEAD limpou histórico/refs/forks.
- A Skill não substitui validação por pares nem aprova automaticamente gates. Licença Apache-2.0 do software não se estende a obras de terceiros. Nenhum conteúdo externo está liberado por presunção.

## Instalação de teste (sem release)

1. No workflow de origem acima, baixe o **artefato de CI** chamado `MeuArtigoSkill-rc-test-only`.
2. Extraia o pacote externo; confira `SHA256SUMS.txt` e `BUNDLE_BUILD_RECEIPT.json`.
3. Importe no host compatível **somente** o ZIP interno `MeuArtigoSkill-v1.0.0-rc.1.zip`. Não use “Code → Download ZIP” do repositório nem o ZIP externo de Actions.
4. Confirme a versão *efetivamente executada* e o armazenamento autorizado do pesquisador antes de iniciar qualquer projeto. Não use dados científicos sensíveis nos testes.
5. Para aceite de host, seguir [HOST_PRESENTATION_ATTESTATION.md](HOST_PRESENTATION_ATTESTATION.md). Nunca editar o manifesto para esconder diferenças de hashes.

## Estado desta minuta

**DRAFT_ONLY / NOT_PUBLISHED.** Não existe nesta etapa um tag `v1.0.0-rc.1`, publicação de GitHub Release, merge de PR, instalação validada ou nova autorização científica produzida por este documento. A decisão de transformar a candidata em *pre-release* pública depende de ato posterior explícito do mantenedor.
