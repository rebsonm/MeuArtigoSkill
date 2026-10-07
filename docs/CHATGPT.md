# Adapter — ChatGPT / Codex

> Se você nunca usou GitHub, comece por [COMECE-AQUI.md](./COMECE-AQUI.md).

Este documento descreve como usar **Meu Artigo** em ambientes OpenAI. A metodologia central continua em `meu-artigo/SKILL.md`.

## Antes de tentar instalar

Segundo a documentação oficial atual da OpenAI, Skills no ChatGPT estão disponíveis para usuários elegíveis dos planos **Business, Enterprise, Healthcare e Edu**, sujeitos às configurações do workspace e à disponibilidade do produto.

A disponibilidade pode variar entre ChatGPT, Codex e outras superfícies.

Se você não encontrar a área **Plugins → Habilidades/Skills**, isso provavelmente significa que a instalação nativa de Skills ainda não está disponível naquele ambiente. Nesse caso, não é erro seu nem da Skill.

Fonte oficial:

- https://help.openai.com/pt-br/articles/20001066-skills-in-chatgpt

## 1. Baixe pelo GitHub

Na página do repositório:

1. clique em **Code**;
2. clique em **Download ZIP**;
3. descompacte o arquivo;
4. entre na pasta `MeuArtigoSkill`;
5. localize a subpasta `meu-artigo`.

A Skill está nessa subpasta.

## 2. Instale no ChatGPT

Quando sua conta/workspace oferecer Skills:

1. abra o ChatGPT;
2. na barra lateral, entre em **Plugins**;
3. abra a aba **Habilidades / Skills**;
4. clique em **Criar**;
5. escolha **Carregar do computador**;
6. forneça o pacote da Skill.

Se a interface exigir um único arquivo, compacte **somente** a pasta `meu-artigo` antes do upload. O pacote da Skill precisa preservar `SKILL.md`, `references/`, `scripts/` e `agents/`.

Não envie o ZIP completo do repositório como substituto da pasta da Skill, porque ele também contém README e documentação de distribuição.

## 3. Inicie em um chat novo

Use algo como:

> Use `$meu-artigo`. Meu problema de pesquisa é: [problema]. Quero desenvolver um artigo científico e ainda não defini a revista.

Para o teste de usabilidade, não explique à IA como a Skill deveria funcionar.

## Compatibilidade técnica

A pasta `meu-artigo/` contém:

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

## Scopus e Web of Science

Não presumir connector direto.

Quando necessárias:

1. gerar a string exata;
2. executar via navegador autorizado ou orientar o usuário;
3. especificar os campos do export;
4. validar o arquivo recebido;
5. registrar a rodada na matriz.

## Teste recomendado

1. iniciar um chat novo;
2. instalar/ativar apenas a Skill;
3. fornecer um problema de pesquisa inédito;
4. não explicar ao modelo o fluxo esperado;
5. observar workspace, preflight, auditoria de novidade e registro de estado;
6. interromper o projeto;
7. abrir outro chat e pedir apenas: **“Continue meu artigo.”**

## Se não houver Skills na sua conta

Para um teste comparável do mecanismo nativo, prefira Claude ou Gemini se sua conta nessas plataformas suportar Skills.

Você pode usar `SKILL.md` como contexto manual em uma conversa comum, mas isso deve ser registrado como **modo de compatibilidade**, não como teste da instalação nativa da Skill.

## Regra de portabilidade

Se uma capacidade específica da OpenAI não estiver disponível, seguir os papéis definidos em `SKILL.md` e usar um equivalente. Nunca transformar indisponibilidade de ferramenta em ausência de evidência.
