# Meu Artigo — entrada em operação real (pesquisadores em contas próprias)

Status: **SOURCE-ONLY / NÃO IMPLANTADO / SEM AUTORIZAÇÃO DE PUBLICAÇÃO**.
Documento de execução concentrado. O objetivo é disponibilizar uma versão
estável e atualizável, sem usar o túnel E05 de fixtures como produção. Nenhum
comando a seguir foi executado na VPS nesta PR.

## Pré-condições para a janela de ativação

1. PRs candidatas e versão reconciliadas em **um SHA revisado**; merge em
   `main` somente com autorização específica do mantenedor. Não integrar
   isoladamente a PR incremental #91 antes da candidata ancestral #89.
2. DNS sob controle do publicador para o host aprovado. Certificado TLS
   válido, cadeia completa e chave privada protegida. Usuário de serviço
   dedicado, código somente-leitura no runtime, logs sem cabeçalhos OAuth.
3. Tenant Auth0 de produção identificado, `issuer` HTTPS EXATO, metadata
   OAuth/OIDC com `code_challenge_methods_supported` contendo `S256`,
   cliente OAuth escolhido (CIMD/DCR/provided conforme suporte real), URL de
   retorno EXATA exibida pelo portal ChatGPT, fluxo Authorization Code + PKCE,
   escopo `mcp:read`, audiência igual ao recurso HTTPS `/mcp`. Nunca usar
   Client Secret, bearer, JWT, cookies, códigos OAuth ou screenshots de
   credenciais em logs, GitHub ou conversas.
4. Resolver o estado **NOT_OBSERVED da CSP aplicada no iframe real**.
   A aprovação de metadados CSP e a ausência do aviso na UI não bastam.
5. Autorização individual de duas contas ChatGPT independentes para os
   primeiros testes. Usar documentos **fictícios**, em Drives distintos,
   sem artigos confidenciais. O MCP serve UI transitória, NÃO administra
   o Drive nem armazena tokens Google.

## Verificação OFFLINE, sem ativar serviços

A partir do SHA revisado, na raiz do repositório:

```bash
python integrations/mcp-apps/scripts/public_ingress_preflight.py \
  --config integrations/mcp-apps/deploy/nginx-auth0-production.conf.template
python -m unittest discover -s integrations/mcp-apps/tests \
  -p test_public_ingress_preflight.py -v
```

`SOURCE_TEMPLATE_PASS` **não é** prova de TLS, login, CSP ou produção.
O template original antigo `nginx-auth0.conf.example` continua 404 e
não deve ser instalado como configuração ativa.

## Janela autorizada de operação (responsável: operador da VPS)

**Inspeção primeiro:** conferir baseline de hostname/DNS, serviços
existentes, estado da VPS, portas, owner e SHA. Não parar, sobrepor,
reiniciar nem renomear as instâncias E05 e stage17; não reutilizar seus
segredos, porta pública ou diretório de pesquisa. Preferir plano de rollback
aprovado antes de qualquer alteração.

**MCP em loopback:** preparar um checkout produtivo separado no SHA
integrado e um serviço restrito, `node server.mjs --http`, que mantenha
`MEU_ARTIGO_BIND_HOST=127.0.0.1`, porta local aprovada (o template pressupõe
8085), `MEU_ARTIGO_AUTH_MODE=auth0`,
`MEU_ARTIGO_AUTH_ISSUER=<issuer HTTPS exato>`,
`MEU_ARTIGO_AUTH_RESOURCE=https://<host aprovado>/mcp`,
`MEU_ARTIGO_MCP_MULTIUSER=YES`, sem `MEU_ARTIGO_PILOT_SUB`.
Ajustar `MEU_ARTIGO_ALLOWED_ORIGIN` apenas mediante observação do Origin
legítimo esperado; não usar `*`, `null` ou HTTP. As configurações de
identidade devem ficar em arquivo protegido do sistema, nunca na PR ou no
terminal/chat como segredos; o MCP nunca deve receber tokens de Google Drive.
Se o processo não abrir `/readyz` em loopback, STOP.

**Nginx:** copiar o arquivo **template** para local de revisão temporário
fora do `sites-enabled`; substituir hostname e caminhos reais de
certificado/chave. A configuração já nega todas as rotas exceto
`/mcp`, os dois caminhos RFC 9728 de metadados e
`/.well-known/openai-apps-challenge`. Não habilitar alias de challenge com
token inventado: obter o token EXATO no portal de publicação e gravar somente
no filesystem autorizado. Antes de habilitar a configuração revisada:

```bash
python integrations/mcp-apps/scripts/public_ingress_preflight.py \
  --config /CAMINHO/DE/CONFIGURACAO-RENDERIZADA.conf \
  --expected-host mcp.allflux.com.br --require-cert-files
sudo nginx -t
```

O host acima é **proposto, não verificado**: substituí-lo pelo domínio
efetivamente comprovado se for diferente. O preflight rejeita chave
privada acessível por grupo/outros e TLS inexistente, mas não valida o
certificado criptograficamente; `nginx -t` também não prova OAuth real,
CSP efetiva ou conectividade ChatGPT. Habilitar o site e fazer
`nginx -s reload` SOMENTE após autorização expressa do mantenedor e
backup verificado da configuração anterior. Manter acesso administrativo
independente e rollback funcional.

## Prova real mínima pós-ativação

Executar com os responsáveis consentidos, registrando apenas status e
SHA, NUNCA credenciais ou documentos:

| Verificação | Esperado |
| --- | --- |
| GET `https://<host>/.well-known/oauth-protected-resource` | 200 JSON; resource `https://<host>/mcp`, issuer e scope corretos |
| GET `https://<host>/.well-known/oauth-protected-resource/mcp` | 200 metadata coerente |
| POST `https://<host>/mcp` sem token | 401 + `WWW-Authenticate: Bearer` |
| POST com token expirado/issuer ou audience inválidos | 401 sem dados de pesquisa |
| POST com JWT válido e escopo insuficiente | 403 |
| GET `https://<host>/readyz` e `/healthz` | 404 externamente, 200 apenas em loopback |
| Outros caminhos arbitrários | 404, sem proxy aberto |
| OAuth ChatGPT A e B | Authorization Code+PKCE S256, scopes e issuer reconhecidos |
| Dados sintéticos Drive A e B | Isolamento recíproco, sem cache cruzado, nenhum documento real no MCP |
| CSP no iframe e painel | Enforcement real observado; interface responde nos dois perfis |

Código HTTP sozinho não comprova conteúdo/suporte de artigos ou decisões
científicas. Os sete gates permanecem sob responsabilidade humana. Para cada
falha, **STOP** e registrar código não sensível.

## Rollback sem perda de dados

Se houver erro, **desabilitar somente a rota produtiva nova** no proxy,
revalidar o arquivo anterior com `nginx -t` e recarregar Nginx.
Não interromper E05 nem o piloto antigo; não usar `git reset --hard`,
`rm -rf`, alterações recursivas de permissões ou apagar conexões/Drives.
Revogar credenciais comprometidas pelo painel Auth0, nunca por comandos
publicados. O serviço MCP não possui dados canônicos a migrar. Registrar
a versão anterior, SHA da falha, horários e decisão humana de rollback.

## Publicação e atualizações

O fluxo de distribuição a contas ChatGPT independentes é **With MCP**
no Diretório de Plugins, após registro/verificação do publicador, domínio
e políticas HTTPS, vídeo de demonstração, cinco positivos/três negativos,
OAuth de revisão e varredura. A publicação depende de aprovação da
plataforma. A candidata beta.9 e a PR #91 não são a v1.0.0 lançada.
Após publicação, mudanças elegíveis no servidor remoto passam por
rescans da plataforma; atualização de Skill/metadata exige novo pacote.
O URL público do servidor é compromisso de longo prazo: não alterar
o host sem planejar a migração com o suporte da plataforma.

### Próximas decisões (somente quando os bloqueios forem comprovados)

- **Mantenedor:** aceitar/rejeitar riscos R01 documentados (RA-01–RA-06),
  aprovar R02 com evidência CSP real, e autorizar merge no SHA exato.
- **Mantenedor + operador:** aprovar alteração efetiva de VPS/NGINX/Auth0
  depois dos testes e confirmar acesso a pesquisadoras(es) consentidos.
- **Mantenedor + plataforma:** submeter o plugin para revisão pública;
  autorizar a publicação após aprovação.

Referências oficiais:
- https://developers.openai.com/plugins/build/auth
- https://developers.openai.com/plugins/build/mcp-server
- https://developers.openai.com/plugins/deploy/submission
