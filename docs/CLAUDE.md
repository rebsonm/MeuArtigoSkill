# Adapter — Claude

Este documento descreve como usar **Meu Artigo** em Claude. A metodologia central continua em `meu-artigo/SKILL.md`.

## Compatibilidade

Claude reconhece Skills estruturadas com `SKILL.md`, arquivos de referência e scripts executáveis. A arquitetura de divulgação progressiva — metadados no frontmatter, instruções centrais e referências lidas sob demanda — é compatível com a estrutura deste repositório.

Fonte oficial de referência:

- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

> Observação: interfaces, caminhos de instalação e capacidades de execução podem variar entre claude.ai, Claude Code e API. Use o mecanismo de Skills da superfície em que estiver trabalhando.

## Instalação

Use a pasta `meu-artigo/` como a pasta da Skill.

O arquivo principal deve continuar sendo:

`meu-artigo/SKILL.md`

Prompt inicial sugerido:

> Use a Skill Meu Artigo. Meu problema de pesquisa é: [problema]. Quero construir o artigo com rastreabilidade e continuidade.

## MCP e conectores

O núcleo da Skill **não pressupõe nomes de ferramentas do ChatGPT**.

No Claude:

1. identifique os MCPs/connectores realmente disponíveis;
2. mapeie-os para os papéis definidos no `SKILL.md`;
3. quando citar uma ferramenta MCP dentro de instruções específicas do Claude, prefira nomes totalmente qualificados no formato recomendado pela documentação da Anthropic;
4. não presuma que um servidor MCP está instalado.

Exemplo de papéis:

- armazenamento persistente → Google Drive, filesystem ou equivalente;
- descoberta acadêmica → mecanismo acadêmico/MCP disponível;
- contexto de citação → Scite ou equivalente;
- web/publisher retrieval → navegador, web search ou MCP correspondente;
- bases indexadas → export de Scopus/WoS ou connector real, quando existente.

## Scripts

Claude Skills podem trabalhar com scripts e filesystem, mas o ambiente varia por superfície.

Os scripts deste repositório são auxiliares determinísticos e não requerem acesso à internet:

- `scripts/init_project.py`;
- `scripts/dedupe_records.py`;
- `scripts/validate_project.py`.

Quando a superfície permitir execução local, prefira executá-los em vez de reimplementar sua lógica em linguagem natural.

## Persistência

Se Google Drive estiver conectado, reproduza o workspace canônico definido em `references/drive-workspace.md`.

Se não estiver:

1. crie o espelho local com `init_project.py`;
2. mantenha `CONTINUIDADE.md` atualizado;
3. sincronize depois com um armazenamento persistente;
4. não dependa do histórico da conversa.

## Scopus e Web of Science

Trate como fontes bibliográficas externas, salvo quando um MCP real fornecer acesso.

Não invente conectores.

Quando for necessário login institucional, o usuário pode precisar executar a busca ou autenticar uma sessão autorizada. A Skill prepara query, filtros, export, validação e continuidade.

## Teste recomendado

Use um problema que nunca tenha sido discutido com o Claude usado no teste.

Critérios centrais:

- detectou a necessidade de persistência?
- preservou o problema original?
- iniciou auditoria de novidade?
- escolheu o desenho metodológico sem inflar o rótulo?
- registrou strings e contagens?
- usou scripts quando disponíveis?
- retomou corretamente em uma sessão nova?

## Nota de plataforma

A Anthropic recomenda manter `SKILL.md` conciso, usar referências separadas e preferir scripts determinísticos para operações verificáveis. Essa é exatamente a arquitetura adotada por este projeto.
