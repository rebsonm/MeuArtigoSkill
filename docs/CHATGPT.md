# Adapter — ChatGPT / Codex

> Se você nunca usou GitHub, comece por [COMECE-AQUI.md](./COMECE-AQUI.md).

Este documento descreve como usar **Meu Artigo** em ambientes OpenAI. A metodologia central continua em `SKILL.md`.

## Antes de tentar instalar

A instalação de Skills no ChatGPT depende da elegibilidade da conta, da disponibilidade do recurso e das configurações do ambiente. Consulte a [documentação oficial de Skills](https://help.openai.com/pt-br/articles/20001066-skills-no-chatgpt).

**O que está documentado:** em contas elegíveis, o caminho é **Plugins → Habilidades → Criar → Carregar do computador**. A presença da opção deve ser verificada no próprio ambiente. Experiências pontuais de versões anteriores, inclusive com contas de outros planos, não comprovam disponibilidade geral nem compatibilidade integral desta beta.

**O que ainda falta validar:** importação e execução ponta a ponta do arquivo `v0.8.0-beta.8` em contas elegíveis do ChatGPT, inclusive retomada e gravação no Drive.

## 1. Baixe a versão oficial do GitHub

1. Abra [a versão beta publicada](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v0.8.0-beta.8).
2. Baixe **`MeuArtigoSkill-v0.8.0-beta.8.zip`**, na seção de arquivos disponibilizados.
3. Se desejar conferir a integridade, utilize o `SHA256SUMS.txt` do mesmo lançamento.
4. Preserve o ZIP completo; **não use o arquivo automático `Source code (zip)` como primeira opção de instalação**.

O arquivo instalável mantém `SKILL.md` na raiz e os recursos auxiliares. Descompactar é opcional para inspeção, não requisito para carregar no ChatGPT.

## 2. Instale no ChatGPT

Quando a sua conta oferecer o recurso:

1. abra o ChatGPT e acesse **Plugins → Habilidades**;
2. selecione **Criar → Carregar do computador**;
3. escolha o ZIP oficial da versão;
4. acompanhe a verificação da Skill e confirme a instalação se a interface permitir.

O procedimento de upload está documentado pelo fornecedor; a **execução de todos os recursos do Meu Artigo nesta versão ainda depende de teste funcional real**. Se os menus forem diferentes, consulte o guia oficial acima, sem presumir erro no pacote.

## 3. Inicie em um chat novo

Use algo como:

> Use `$meu-artigo`. Meu problema de pesquisa é: [problema]. Quero desenvolver um artigo científico, acompanhar o passo a passo pelo C.A.D.A. e ainda não defini a revista.

Na primeira utilização, basta apresentar seu problema de pesquisa e deixar a própria Skill orientar o fluxo.

## Preflight específico do ChatGPT

A [documentação oficial](https://help.openai.com/pt-br/articles/20001066-skills-in-chatgpt)
descreve Skills para contas qualificadas de ambientes de trabalho e
disponibilidade dependente da configuração do produto. Verifique a
presença efetiva do menu e as permissões no ambiente utilizado, sem
inferir elegibilidade a partir do nome do modelo ou de instalação anterior.
O fato de um plugin incluir uma Skill não significa que os aplicativos
ou conectores relacionados já estejam autenticados. Uma importação
bem-sucedida **não** constitui comprovação de execução do Meu Artigo.

Antes da primeira busca, aplique
[preflight por capacidades](../references/platform-capability-preflight.md).
Confirme gravação real no Drive, suporte aos scripts nesta superfície
e autenticidade dos retornos. Faltando prova, classifique ações externas
como `UNVERIFIED`; não confunda ações do ChatGPT Work, do ambiente
de plugins e de uma interface apenas conversacional.

## Compatibilidade técnica

A raiz do bundle contém:

- `SKILL.md`;
- arquivos em `references/`;
- scripts determinísticos em `scripts/`;
- configuração específica OpenAI em `agents/openai.yaml`.

O arquivo `agents/openai.yaml` é um **adapter da plataforma**, não parte da metodologia científica.

## Integrações preferenciais

O manifesto OpenAI declara como dependências preferenciais:

- Google Drive;
- Consensus;
- Scite;
- Firecrawl.

Consensus, Scite e Firecrawl aceleram o fluxo e podem ser substituídos por capacidades equivalentes quando indisponíveis. Google Drive é diferente: ele é a camada canônica de persistência do projeto no fluxo normal.

A instalação/conexão de uma integração de terceiros exige ação explícita do usuário. No caso do Google Drive, a Skill deve verificar a conexão antes de iniciar trabalho substantivo. Se não estiver conectado, deve apresentar o fluxo de conexão, aguardar a ação do usuário e verificar novamente. Se ainda assim o Drive não estiver disponível, deve perguntar explicitamente se o usuário quer continuar sem Drive usando apenas os arquivos/resultados do Work ou armazenamento local. Somente uma resposta afirmativa autoriza esse fallback. Sem essa confirmação, a Skill não deve iniciar um workspace local canônico nem avançar para busca, screening, síntese ou redação.

## Papel das integrações

### Google Drive
Backend canônico padrão para workspace persistente, `CONTINUIDADE.md`, protocolo, matriz-mestra, PDFs, exports, manuscrito e arquivos de submissão. Resultados gerados no Work podem ser usados como staging, mas precisam ser gravados/sincronizados no Drive antes de serem tratados como estado canônico. O fallback `WORK_FALLBACK` só existe após autorização explícita do usuário.

### Consensus
Preferido para descoberta inicial, calibração de termos, auditoria de novidade e literatura próxima. Não deve ser tratado como base bibliográfica exaustiva.

### Scite
Preferido para contexto/grafo de citação, verificação bibliográfica e full text quando legitimamente disponível.

### Firecrawl / web
Preferido para páginas de periódicos, editoras, repositórios, documentação oficial, normas e instruções de submissão.

### Gestão C.A.D.A.: ClickUp, Jira ou Trello

A gestão C.A.D.A. funciona mesmo sem um gerenciador externo.

Quando desejar o espelho operacional, o ChatGPT pode usar, quando conectados:

- **ClickUp**;
- **Atlassian**, para Jira;
- **Trello**.

A Skill deve usar um único gerenciador principal por artigo, registrar a escolha e manter `11_CADA_Control` como controle canônico. O vínculo com tickets/cards fica em `12_PM_Sync`.

Esses três provedores são alternativas entre si; por isso não são declarados simultaneamente como dependências obrigatórias em `agents/openai.yaml`.

## Scopus e Web of Science

Não presumir connector direto.

Quando necessárias:

1. gerar a string exata;
2. executar via navegador autorizado ou orientar o usuário;
3. especificar os campos do export;
4. validar o arquivo recebido;
5. registrar a rodada na matriz.

## Verificação funcional recomendada

1. iniciar um chat novo;
2. instalar/ativar apenas a Skill;
3. fornecer um problema de pesquisa inédito;
4. não explicar ao modelo o fluxo esperado;
5. observar workspace, preflight, painel C.A.D.A., auditoria de novidade e registro de estado;
6. interromper o projeto;
7. abrir outro chat e pedir apenas: **“Continue meu artigo.”**

## Se não houver Skills na sua conta

Para uma experiência comparável do mecanismo nativo, prefira Claude ou Gemini se sua conta nessas plataformas suportar Skills.

Você pode usar `SKILL.md` como contexto manual em uma conversa comum, mas isso deve ser registrado como **modo de compatibilidade**, não como uso da instalação nativa da Skill.

## Regra de portabilidade

Se uma capacidade específica da OpenAI não estiver disponível, seguir os papéis definidos em `SKILL.md` e usar um equivalente. Nunca transformar indisponibilidade de ferramenta em ausência de evidência.


## Ícone da Skill

O ícone pode ser empacotado junto com a Skill.

1. crie uma pasta `assets/` na raiz do bundle;
2. coloque nela o arquivo do ícone, por exemplo `assets/icon.svg` ou `assets/icon.png`;
3. em `agents/openai.yaml`, dentro de `interface:`, aponte os campos de ícone para esse arquivo:

```yaml
interface:
  display_name: "Meu Artigo"
  short_description: "Do problema ao artigo com gestão C.A.D.A."
  icon_small: "assets/icon.svg"
  icon_large: "assets/icon.svg"
```

Opcionalmente, a interface também aceita `brand_color` em hexadecimal, por exemplo `"#1ABCFE"`.

Os caminhos devem ser **relativos ao bundle da Skill** e o arquivo precisa estar realmente presente no ZIP. Depois de alterar o ícone, reinstale/atualize a Skill para que a interface processe o novo asset.
