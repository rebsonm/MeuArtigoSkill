# Adapter — Claude

> Se você nunca usou GitHub, comece por [COMECE-AQUI.md](./COMECE-AQUI.md).

Este documento descreve como usar **Meu Artigo** em Claude. A metodologia central continua em `meu-artigo/SKILL.md`.

## Antes de tentar instalar

Segundo a documentação oficial atual da Anthropic, Skills personalizadas no **claude.ai** podem ser enviadas em **Settings → Features** e estão disponíveis nos planos **Pro, Max, Team e Enterprise** quando a execução de código está habilitada.

Claude Code também reconhece Skills baseadas em filesystem.

Fonte oficial:

- https://platform.claude.com/docs/pt-BR/agents-and-tools/agent-skills/overview

## 1. Baixe pelo GitHub

Na página do repositório:

1. clique em **Code**;
2. clique em **Download ZIP**;
3. descompacte o arquivo;
4. localize a pasta `meu-artigo`.

## 2A. Instalação no claude.ai

1. compacte **somente** a pasta `meu-artigo` em um ZIP;
2. abra o Claude;
3. acesse **Settings → Features**;
4. localize a área de Skills personalizadas;
5. faça upload do ZIP;
6. confirme a Skill.

Cada usuário precisa instalar sua própria cópia no claude.ai.

## 2B. Instalação no Claude Code

Se você usa Claude Code:

- coloque a Skill pessoal em `~/.claude/skills/`; ou
- coloque-a no projeto em `.claude/skills/`.

A pasta deve manter seu `SKILL.md` e arquivos de suporte.

## 3. Comece em uma conversa nova

> Use a Skill Meu Artigo. Meu problema de pesquisa é: [problema]. Quero construir o artigo com rastreabilidade, continuidade e gestão C.A.D.A.

Para o teste, não descreva previamente o nosso workflow.

## Compatibilidade

Claude reconhece Skills estruturadas com `SKILL.md`, arquivos de referência e scripts executáveis. A arquitetura de divulgação progressiva — metadados no frontmatter, instruções centrais e referências lidas sob demanda — é compatível com este repositório.

## MCP e conectores

O núcleo da Skill **não pressupõe nomes de ferramentas do ChatGPT**.

No Claude:

1. identifique os MCPs/connectores realmente disponíveis;
2. mapeie-os para os papéis definidos no `SKILL.md`;
3. use nomes de ferramentas compatíveis com a instalação real;
4. não presuma que um servidor MCP está instalado.

Exemplos:

- armazenamento persistente → Google Drive, filesystem ou equivalente;
- descoberta acadêmica → mecanismo acadêmico/MCP disponível;
- contexto de citação → Scite ou equivalente;
- web/publisher retrieval → navegador, web search ou MCP correspondente;
- bases indexadas → export de Scopus/WoS ou connector real;
- gestão operacional C.A.D.A. → ClickUp, Jira, Trello ou MCP equivalente, se realmente disponível.

## Gestão C.A.D.A.

O C.A.D.A. é interno à Skill e não depende de MCP externo. Se um gerenciador de trabalho estiver conectado no Claude, use-o como espelho operacional conforme `references/work-management.md`. Preserve `11_CADA_Control` como fonte canônica.

## Scripts

Os scripts deste repositório são locais e determinísticos:

- `scripts/init_project.py`;
- `scripts/dedupe_records.py`;
- `scripts/validate_project.py`.

Quando a superfície permitir execução local, prefira executá-los em vez de reimplementar a lógica em linguagem natural.

## Persistência

Se Google Drive estiver conectado, reproduza o workspace canônico definido em `references/drive-workspace.md`.

Se não estiver:

1. crie o espelho local com `init_project.py`;
2. mantenha `CONTINUIDADE.md` atualizado;
3. sincronize depois com armazenamento persistente;
4. não dependa do histórico da conversa.

## Scopus e Web of Science

Trate como fontes bibliográficas externas, salvo quando um MCP real fornecer acesso.

Não invente conectores.

Quando houver login institucional, o usuário pode precisar executar a busca ou autenticar uma sessão autorizada. A Skill prepara query, filtros, export, validação e continuidade.

## Teste recomendado

Use um problema nunca discutido com o Claude usado no teste.

Observe:

- persistência;
- preservação do problema original;
- auditoria de novidade;
- escolha metodológica;
- strings e contagens;
- uso de scripts quando disponível;
- retomada correta em nova sessão.

## Nota de plataforma

A Anthropic recomenda manter `SKILL.md` conciso, usar referências separadas e preferir scripts determinísticos para operações verificáveis. Essa é a arquitetura adotada por este projeto.
