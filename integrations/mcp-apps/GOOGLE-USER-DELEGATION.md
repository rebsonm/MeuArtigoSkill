# Google Drive de cada pesquisador — autorização individual e isolamento

## Contrato inegociável

**O Google Drive do mantenedor nunca é a credencial-padrão de usuários externos.**
Pesquisadores A, B, C e o mantenedor precisam autorizar **suas próprias
contas Google**, separadamente, pelo consentimento Google OAuth 2.0.
O acesso Auth0 ao MCP autentica a pessoa, mas **não concede automaticamente
acesso ao Google Drive**. Não reaproveitar o conector pessoal ChatGPT/Drive
do administrador como credencial do serviço.

**Fluxo de identidade:** ChatGPT -> JWT Auth0 individual -> `sub` Auth0
`google-oauth2|<google-sub>` -> consentimento OAuth individual no Google ->
Google UserInfo `sub` deve corresponder exatamente ao `sub` Google do Auth0
-> concessão de refresh criptografada para **essa identidade** -> chamada
Google Drive usando token delegado **dessa mesma identidade**. Cada
consulta revalida UserInfo; qualquer divergência bloqueia a consulta.

Identidade sem vínculo, consentimento recusado, conta Google diferente,
credencial revogada, sessão OAuth expirada, configuração insegura ou
autorizações cruzadas **não habilitam acesso nem fallback para outro Drive**.

### Duas modalidades, separadas

1. **Modo experimental anterior:** `MEU_ARTIGO_MULTIUSER_REGISTRY` e
   `MEU_ARTIGO_TENANT_DATA_ROOT` mapeiam projetos locais; isso **não**
   prova que cada usuário está acessando seu próprio Google Drive.
2. **Modo correto para o produto futuro:** `MEU_ARTIGO_GOOGLE_DRIVE_MODE=per_user`.
   Requer Auth0, identidade individual e consentimento Google, **proíbe**
   `MEU_ARTIGO_PROJECT_ROOT`, `MEU_ARTIGO_PILOT_SUB` e registro local.
   Não existe identidade compartilhada com fallback automático.
   `meu_artigo_google_projetos` consulta apenas a árvore canônica do
   próprio usuário, sem acessar conteúdo de documentos e sem criar pastas.

Esta PR implementa **somente leitura dos metadados** da estrutura
`My Drive/Meu Artigo/<pasta do artigo>`. O painel científico completo,
sincronização, leitura de PDF/Docs, criação de pastas e escrita documental
Google **não** estão implementados nesta integração. A ferramenta de painel
fail-closed no modo `per_user`, para impedir afirmações falsas de que um
projeto local é o projeto Google conectado.

### Ferramentas de um usuário já autenticado

- `meu_artigo_google_conectar`: gera URL individual de consentimento
  Google (com `state` anti-CSRF, PKCE S256, tempo de vida de 10 minutos).
- `meu_artigo_google_status`: mostra somente se a autorização Google
  **dessa identidade** está cadastrada.
- `meu_artigo_google_projetos`: atualiza token **daquela identidade**,
  confere o Google `sub`, localiza a pasta exata `Meu Artigo` filha
  direta de My Drive e enumera somente pastas-filhas, com paginação,
  limites e checagem de pais; sem conteúdo de documentos.
- `meu_artigo_google_desconectar`: elimina a autorização local
  **daquela identidade**, sem modificar arquivos do Drive.
  O usuário pode também revogar o aplicativo nas configurações do Google.

## Arquitetura de credenciais

- Não utilizar API key, service account genérica, Domain-Wide Delegation,
  conta do mantenedor ou token global para consultar usuários externos.
- O código troca o código OAuth Google por um token de atualização
  **do próprio pesquisador**; armazena somente esse token, com AES-256-GCM
  e chave fornecida externamente por um gerenciador de segredos.
- Um arquivo criptografado por `SHA-256(Auth0 sub)`, AAD associada ao
  `sub`; pasta privada preexistente `0700`, arquivos `0600`,
  sem symlinks, limite de tamanho, escrita temporária-atômica.
- Tokens de acesso são temporários, validados pela API Google UserInfo
  e **não são enviados para o modelo nem incluídos no resultado MCP**.
- HTTP continua local: `127.0.0.1:8085`. Nginx externo somente após
  revisão, HTTPS e aceites específicos.
- A solicitação Google inicial usa `openid` +
  `https://www.googleapis.com/auth/drive.metadata.readonly`.
  Este último é um **escopo restrito** e pode exigir verificação e
  avaliação de segurança antes de distribuição pública.
- O endpoint `/google/oauth/callback` é HTTP GET sem JWT Auth0 porque
  recebe o redirecionamento do navegador Google; somente um `state`
  previamente emitido e não consumido pode completar o vínculo. O
  `sub` Google é validado antes de persistir o refresh token.
  É indispensável desabilitar/redigir logs de query string nesse
  caminho no proxy — o callback contém um código de autorização.
- Não imprimir tokens, subject ou query string de callback em logs;
  não enviar credenciais ao ChatGPT ou a arquivos versionados.

### Configuração de homologação privada (NÃO EXECUTAR na produção)

Usar conta de serviço Linux dedicada, diretório privado, variáveis via
secret manager, Google OAuth web application específica de teste e
redirect autorizado exatamente `https://mcp.allflux.com.br/google/oauth/callback`.

```sh
MEU_ARTIGO_AUTH_MODE=auth0
MEU_ARTIGO_AUTH_ISSUER=https://SEU_TENANT.us.auth0.com/
MEU_ARTIGO_AUTH_RESOURCE=https://mcp.allflux.com.br/mcp
MEU_ARTIGO_GOOGLE_DRIVE_MODE=per_user
MEU_ARTIGO_GOOGLE_CLIENT_ID=<do Google Cloud, privado>
MEU_ARTIGO_GOOGLE_CLIENT_SECRET=<do secret manager, privado>
MEU_ARTIGO_GOOGLE_REDIRECT_URI=https://mcp.allflux.com.br/google/oauth/callback
MEU_ARTIGO_GOOGLE_TOKEN_DIR=/var/lib/meu-artigo/private-google-grants
MEU_ARTIGO_GOOGLE_TOKEN_KEY=<chave forte 32 bytes, base64url, secreta>
MEU_ARTIGO_BIND_HOST=127.0.0.1
MEU_ARTIGO_MCP_PORT=8085
```

No modo Google individual, **não definir** `MEU_ARTIGO_PILOT_SUB`,
`MEU_ARTIGO_PROJECT_ROOT`, `MEU_ARTIGO_MULTIUSER_REGISTRY` nem
`MEU_ARTIGO_TENANT_DATA_ROOT`. Se definidos, o programa recusa iniciar.

**Google Cloud:** criar o OAuth client do tipo aplicação web para
homologação, habilitar Drive API, informar tela de consentimento,
escopos e o redirect autorizado. Configurar apenas test users
autorizados, sujeitos à política de escopos e verificação do Google.
**Auth0:** cada conta efetivamente usa identidade `google-oauth2|`
cujo sufixo deve igualar o Google `sub` retornado pelo consentimento;
concluir autorização de cliente, PKCE, audience e `mcp:read`.
Não presumir que ter o mesmo endereço de email comprova a igualdade
do usuário — são IDs estáveis comparados, não nomes nem emails.

### Atenção sobre isolamento administrativo

Os usuários A/B/C ficam isolados pelo fluxo de autorização do
**aplicativo**. Um operador de VPS com root, acesso à memória do processo,
ao gerenciador de segredos ou ao cofre criptografado + sua chave pode
tecnicamente comprometer credenciais. Isso não é isolamento
criptográfico ponta a ponta contra o próprio administrador.
Para políticas que proíbam acesso até por administradores, é
necessária outra arquitetura de custódia de chaves e auditoria
independente. Nunca prometer ausência absoluta desse risco.

## Aceite para esta PR

`npm run test:google-delegation` usa provedores OAuth/Drive
completamente simulados. Testa dois consentimentos independentes,
estado único e não reutilizável, PKCE, conta Google errada,
credenciais isoladas e criptografadas, refresh+UserInfo por usuário,
lista canônica sem mistura, desvinculação de A sem afetar B, dados de
B ausentes do retorno de A e nenhuma queda silenciosa para painel local.

Testes sintéticos não provam configuração do Google Cloud, conta real
Auth0, verificação do escopo restrito, segurança de administração
da VPS, acesso público, integração ChatGPT ou que a versão instalada
do Plugin tenha recebido essas mudanças. **Não ativar o endpoint
público, configurar callbacks ou fazer merge/release/deploy sem
autorização específica.**
