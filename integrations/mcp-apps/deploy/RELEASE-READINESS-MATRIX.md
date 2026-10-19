# Meu Artigo — matriz consolidada de lançamento | 19/10/2026

> Fonte operacional única. Atualize com fatos e provas; testes sintéticos e workflows de CI não validam isolamento de usuários nem aprovação científica. Esta matriz NÃO autoriza merge da PR #91, alteração de VPS/Auth0/Google Drive, submissão ou publicação do Plugin.

**Projeto:** Meu Artigo, publicador individual **Rebson de Morais Mendes**, suporte **rebsonm@gmail.com**.
**Versão candidata:** `0.9.0-beta.9` (source/ZIP, **não** versão pública instalada/lançada).
**Site oficial:** `https://rebsonm.github.io/MeuArtigoSkill/` (GitHub Pages deployment SUCCESS, sem comprovação GET/TLS independente neste ambiente).
**MCP candidato:** `https://mcp.allflux.com.br/mcp`, escopo `mcp:read`.
**Candidata exclusiva do Plugin:** PR #91, `release/prepare-public-mcp-20261018`, base `main`, NÃO MESCLADA.
**Site isolado:** PR #92, integrada em `main` no commit `bd399a12b59acca151ffce3ab186fdc86b6901c1`.
**Regra:** não confundir hospedagem do site com disponibilização pública do Plugin.

| Macroetapa | Evidência concluída | Pendência vinculante | Resultado |
| --- | --- | --- | --- |
| **01 — Consolidação e CI** | PR #91 concentra candidata do Plugin; workflows de Release audit, CodeQL JS/Python, segurança, qualidade e Chromium sintético aprovados no SHA anteriormente verificado. | Parecer/revisão independente R01 (0 reviews apresentados); conferir CI novamente em qualquer HEAD novo. | **PARCIAL — código candidato verificado, segurança independente PENDENTE** |
| **02 — MCP e painel real** | 4 testes de chamada de ferramenta em ChatGPT: sem snapshot, snapshot fictício vazio, FULL com 7 gates pendentes e rejeição de campo extra; proprietário confirmou navegação de 10 telas funcionando. | CSP *efetiva do host* ainda não comprovada sob as configurações do navegador/ChatGPT. | **PARCIAL — integração/UX PASS, CSP PENDENTE** |
| **03 — Dois pesquisadores e Drive** | Conexão individual A verificou apenas metadados de pastas, sem leitura/escrita de documentos, sem compartilhamento público observado nos três itens. | Conta B consentida, login Auth0/PKCE e scope independentes, A→B→A, proibição de acesso cruzado, logout/cache, teste 401/403. | **PARCIAL — A PASS, B/isolamento NÃO EXECUTADOS** |
| **04 — Pacote, revisão e integração** | Bundle Skill+MCP `0.9.0-beta.9` preparado, verificações anteriores de integridade realizadas; o gerador foi atualizado para inserir `websiteURL`, `supportURL`, `privacyPolicyURL` e `termsOfServiceURL` oficiais e a identidade individual. | Nova CI e ZIP do HEAD atual; revisão independente R01 e decisão humana explícita antes do merge da PR #91, release, VPS/prod Plugin. | **PARCIAL — pacote candidato, integração NÃO AUTORIZADA** |
| **05 — Site GitHub Pages** | Proprietário aprovou identidade visual com a arte canônica `assets/icon.svg`. PR #92 integrada isoladamente; GitHub Actions `39328997760`: build SUCCESS/deploy SUCCESS e URL do ambiente. | GET HTTPS 200 independente nas 4 páginas (o fetch externo desta sessão não conseguiu comprovar); revisão jurídica independente é pendente e não deve ser presumida concluída. | **IMPLANTADO — publicação comprovada pelo GitHub; auditoria externa/JURÍDICA PENDENTE** |
| **06 — Diretório OpenAI** | Material técnico e cinco casos positivos/três negativos estruturados no ZIP candidato; roteiro de vídeo e reviewer packet preparados. | Verificação individual OpenAI, project permission `api.apps.write`, reviewer test account consentida, OAuth callback/PKCE, challenge de domínio, scan de ferramentas/CSP, demo real, 5+3 testes reais, submissão e aprovação externa. | **NÃO SUBMETIDO — NO-GO até aceite final** |

## Quatro URLs destinadas à metadata pública

- `websiteURL`: https://rebsonm.github.io/MeuArtigoSkill/
- `supportURL`: https://rebsonm.github.io/MeuArtigoSkill/suporte.html
- `privacyPolicyURL`: https://rebsonm.github.io/MeuArtigoSkill/privacidade.html
- `termsOfServiceURL`: https://rebsonm.github.io/MeuArtigoSkill/termos.html

Estes quatro campos constam agora na construção do `plugin.json` público e são verificados por teste de empacotamento. Não há `demo_recording_url` inventada nem credencial embutida no ZIP. `mcp.json` usa URL HTTPS estável e OAuth `mcp:read`.

## Próximo bloco UNIFICADO de aceite — execução com o colega e revisor de segurança

**Pré-condições:** um colega com conta própria ChatGPT + Google Drive, consentimento expresso; eventual revisor de segurança independente; acesso administrativo do dono ao provedor de identidade e ao portal, sem compartilhar senhas/tokens com o assistente.

1. Confirmar R01 — revisão independente documentada dos diffs/alertas CodeQL atuais e decisão de riscos.
2. Registrar CSP efetiva do iframe do próprio ChatGPT, separando eventuais erros de challenge Cloudflare do código Meu Artigo.
3. Autorizar exclusivamente A e B no Auth0, sem flags abertas publicamente; ensaiar login PKCE e negações HTTP 401/403; não imprimir JWTs/segredos.
4. Criar apenas arquivos fictícios e executar A→B→A via conectores Google Drive **individuais**; verificar ausência de leitura cruzada, nenhuma aprovação científica e nenhuma persistência no MCP.
5. Executar em contas de teste os **5 prompts positivos e 3 negativos**, registrar resultados em tabela cega; reexecutar só casos reprovados.
6. Gravar vídeo de 2–3 min sem dados reais; verificar links HTTPS das quatro páginas; concluir domínio/identidade/scan no portal e fazer upload do ZIP **somente após GO expresso do publicador**.

## Decisão automática vs. humana

- `SOURCE_PACKAGE_CI_PASS` não equivale a `LIVE_A_B_PASS`, `SECURITY_INDEPENDENT_APPROVED` ou `OPENAI_REVIEW_APPROVED`.
- `RELEASE_GO` = **NO** até que o proprietário analise evidências concluídas de segurança, CSP, A/B e servidor + revisão de publicação.
- O site público de pré-lançamento pode funcionar enquanto o Plugin permanece privado.
- Alterar a PR #91 com segurança/release metadata NÃO implanta automaticamente nova versão do MCP, nem altera o conteúdo da Skill instalada.

**Documentos relacionados:** `PUBLIC-DIRECTORY-REVIEW-PACKET.md`, `site-drafts/REVIEW-AND-VIDEO.md`. Documentação oficial: https://developers.openai.com/plugins/deploy/submission e https://developers.openai.com/plugins/deploy/app-review.
