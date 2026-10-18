# Meu Artigo — ChatGPT: empacotamento e gates de publicação

Estado: PR técnica em Draft. Nenhuma instalação, merge, release ou implantação autorizada por este documento.

## Dois canais, dois contratos diferentes

| Destino | ZIP | Associação MCP |
| --- | --- | --- |
| Privado do mantenedor | Skill e manifesto OpenAI com referência a app registrada | Arquivo .app.json apontando SOMENTE à app de produção verificada |
| Diretório público | Skill e manifesto sem referência à app registrada | Submissão With MCP pela OpenAI, com servidor HTTPS estável e avaliação independente |

O portal público NÃO aceita submissão de ZIP contendo .app.json ou referências apps para integrações existentes. A conexão com o servidor de produção é submetida diretamente no portal (With MCP). O túnel E05 é teste sintético e não satisfaz os requisitos de hospedagem pública.

Fontes oficiais:
- https://developers.openai.com/plugins/build/plugins
- https://developers.openai.com/plugins/deploy/submission
- https://developers.openai.com/plugins/deploy/submission-errors
- https://developers.openai.com/plugins/deploy/app-review
- https://developers.openai.com/plugins/build/mcp-server

## Gerar candidatos, sem publicar

Para ZIP pública (somente Skill, submissão With MCP em etapa separada):

    python scripts/build_chatgpt_plugin_candidate.py --channel public

Para ZIP privada, APENAS com app de produção previamente verificada:

    python scripts/build_chatgpt_plugin_candidate.py --channel private --app-id asdk_app_PRODUCTION_VERIFIED_ID

O ID acima é exemplo; o script apenas valida seu formato e veta o ID conhecido do E05, não comprova autorização/registro no workspace. Não instale a ZIP de exemplo em conta de usuário.

A construção usa o empacotador allowlist original da Skill e inclui o BUNDLE_MANIFEST auditado, a versão canônica, e os ícones públicos em SVG. A inspeção rejeita ZIP com paths inseguros, versões divergentes, arquivos adulterados, app sintética E05 no canal privado, associação de app no canal público e conteúdo de testes/hooks.

## Bloqueador de versionamento observado

- Código-fonte candidato na PR #82: VERSION 0.9.0-beta.6.
- Plugin pessoal instalado do mantenedor: metadata 0.9.0-beta.8; núcleo da Skill 0.9.0-beta.6.
- Nunca instalar pacote beta.6 sobre o beta.8. Após a revisão cumulativa, escolher nova versão candidata e sincronizar manifestos, BUNDLE_MANIFEST, CHANGELOG, release notes e build pelo procedimento próprio. O empacotador não altera VERSION nem afirma publicação.

## Caminho crítico até o lançamento

1. E05: autorizar atualização isolada e retestar dez menus, ALPHA/BRAVO, foco, hover, locale, CSP, resize e teardown em ChatGPT real.
2. Revisar diffs cumulativos da cadeia PR #78 a #82 e duplicidades de PRs antigas; obter decisão independente da integração.
3. Congelar SHA final, executar CI, CodeQL, release audit e testes do pacote no mesmo SHA.
4. Obter aprovação separada de merge, incorporar apenas a candidata consolidada em main e retestar o SHA integrado.
5. Implantar servidor MCP HTTPS de produção, separado do E05, com Auth0/PKCE e rollback após autorização específica.
6. Homologar contas A/B com Drives individuais, leitura e escrita guardadas, F1–F9, isolamento real e falhas fechadas.
7. Montar versão única da Skill + MCP para Plugin privado; revisar release ID atual antes de atualizar a instalação do mantenedor.
8. Realizar piloto com usuários voluntários e identidades distintas; documentar uso, limitações e política de privacidade sem coleta adicional.
9. Preparar submissão pública With MCP, verificar identidade do desenvolvedor, concluir revisão da OpenAI e publicar somente após aprovação.

## Gates

- GO_PACKAGE: ZIP validada e versões consistentes; não equivale a implantação.
- GO_MCP: HTTPS e OAuth reais homologados.
- GO_DRIVE: isolamento e readback independentes verificados.
- GO_PLUGIN_PRIVATE: novo Plugin funcionando na conta do mantenedor.
- GO_PUBLIC: publicação pública aprovada e observada externamente.

Observatório de usuários, frequência, metadados acadêmicos e ML ficam fora do escopo da versão inicial. Nenhum gate pode ser aprovado por teste sintético isoladamente.
