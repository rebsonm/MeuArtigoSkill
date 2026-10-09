# Adapter — Claude

> Se você nunca usou GitHub, comece por [COMECE-AQUI.md](./COMECE-AQUI.md).

Este documento descreve como usar **Meu Artigo** em Claude. A metodologia central continua em `SKILL.md`.

## Antes de tentar instalar

O Claude oferece Skills personalizadas em superfícies como `claude.ai` e Claude Code, segundo a [documentação oficial da Anthropic](https://platform.claude.com/docs/pt-BR/agents-and-tools/agent-skills/overview). Disponibilidade e permissões variam conforme conta e produto. O suporte anunciado a Skills **não equivale à validação de todos os recursos do Meu Artigo**.

A instalação e a retomada de projetos usando o ZIP `v0.8.0-beta.7` ainda precisam de verificação em ambiente real.

## 1. Baixe o ZIP preparado

1. Abra [a Release v0.8.0-beta.7](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v0.8.0-beta.7).
2. Baixe **`MeuArtigoSkill-v0.8.0-beta.7.zip`** (não o `Source code (zip)`).
3. Se desejar, confirme o hash usando `SHA256SUMS.txt`.

## 2A. Instalação no claude.ai

Se a sua conta apresentar a opção de Skills personalizadas nas configurações:

1. acesse a área de Skills/recursos pessoais do Claude, conforme a interface atual;
2. selecione o upload de uma Skill;
3. envie o ZIP completo da Release;
4. confira se `SKILL.md` e os arquivos de apoio foram reconhecidos.

Os nomes das seções e a disponibilidade podem variar; confira a documentação oficial da sua interface antes de concluir que houve falha.

## 2B. Instalação no Claude Code

No Claude Code, descompacte o ZIP preparado preservando a pasta `MeuArtigoSkill` e coloque-a em `~/.claude/skills/` (escopo pessoal) ou em `.claude/skills/` (escopo do projeto), se esse for o mecanismo suportado pela sua versão. A pasta da Skill deve conter `SKILL.md` em sua raiz.

## 3. Comece em uma conversa nova

> Use a Skill Meu Artigo. Meu problema de pesquisa é: [problema]. Quero construir o artigo com rastreabilidade, continuidade e gestão C.A.D.A.

Na primeira utilização, basta apresentar o problema de pesquisa e deixar a própria Skill orientar o fluxo.

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

Se não estiver conectado:

1. explique ao usuário que o fluxo padrão utiliza o Google Drive e solicite a conexão;
2. verifique novamente se o Drive está disponível e gravável, sem presumir êxito;
3. se continuar indisponível, peça **autorização afirmativa e explícita** para continuar com armazenamento local/Work;
4. somente depois da autorização crie o espelho local com `init_project.py` e mantenha `CONTINUIDADE.md` atualizado;
5. trate o armazenamento local como alternativa autorizada para esse projeto; não o apresente como sincronizado no Drive.

Sem autorização, não inicie atividades científicas substantivas com persistência local presumida.

## Scopus e Web of Science

Trate como fontes bibliográficas externas, salvo quando um MCP real fornecer acesso.

Não invente conectores.

Quando houver login institucional, o usuário pode precisar executar a busca ou autenticar uma sessão autorizada. A Skill prepara query, filtros, export, validação e continuidade.

## Verificação funcional recomendada

Use, de preferência, um problema ainda não discutido naquela conversa.

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
