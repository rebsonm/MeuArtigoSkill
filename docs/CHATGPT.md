# Adapter — ChatGPT / Codex

> Se você nunca usou GitHub, comece por [COMECE-AQUI.md](./COMECE-AQUI.md).

Este documento descreve como usar **Meu Artigo** em ambientes OpenAI. A metodologia central continua em `SKILL.md`.

## Antes de tentar instalar

A disponibilidade de Skills pode variar por conta, rollout e superfície do produto.

A documentação pública da OpenAI consultada em 07/10/2026 ainda cita Business, Enterprise, Healthcare e Edu como planos elegíveis. Porém, em teste direto no mesmo dia, a criação/importação de Skills estava funcional também em uma conta **ChatGPT Plus**.

Por isso, **não conclua a disponibilidade apenas pelo nome do plano**. O teste prático é verificar se sua conta mostra **Plugins → Habilidades/Skills** e as opções de criar/importar. Se essa área estiver disponível, siga normalmente o procedimento abaixo.

Fonte oficial:

- https://help.openai.com/pt-br/articles/20001066-skills-in-chatgpt

## 1. Baixe pelo GitHub

Na página do repositório:

1. clique em **Code**;
2. clique em **Download ZIP**;
3. mantenha esse ZIP completo para a instalação no ChatGPT.

Você pode descompactá-lo apenas para inspeção. A raiz do pacote contém `SKILL.md`, `references/`, `scripts/` e `agents/`.

## 2. Instale no ChatGPT

Quando sua conta/workspace oferecer Skills:

1. abra o ChatGPT;
2. na barra lateral, entre em **Plugins**;
3. abra a aba **Habilidades / Skills**;
4. clique em **Criar**;
5. escolha **Carregar do computador**;
6. selecione **o ZIP completo baixado diretamente do GitHub**.

Este é o procedimento validado para o Meu Artigo. No teste de 07/10/2026, importar o ZIP completo preservou corretamente `references/`, `scripts/`, `agents/` e os demais recursos. Evite reconstruir manualmente o ZIP ou enviar apenas uma parte da estrutura quando não houver necessidade.

## 3. Inicie em um chat novo

Use algo como:

> Use `$meu-artigo`. Meu problema de pesquisa é: [problema]. Quero desenvolver um artigo científico, acompanhar o passo a passo pelo C.A.D.A. e ainda não defini a revista.

Na primeira utilização, basta apresentar seu problema de pesquisa e deixar a própria Skill orientar o fluxo.

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

Essas integrações aceleram o fluxo, mas a metodologia deve continuar quando alguma não estiver disponível, usando recursos equivalentes.

A instalação/conexão de uma integração de terceiros exige ação explícita do usuário. A Skill deve apresentar a conexão e continuar automaticamente após a autorização.

## Papel das integrações

### Google Drive
Referência principal para workspace persistente, `CONTINUIDADE.md`, protocolo, matriz-mestra, PDFs, exports, manuscrito e arquivos de submissão.

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
