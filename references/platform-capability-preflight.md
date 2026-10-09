# Capacidades reais por plataforma — preflight operacional

Este quadro deve ser preenchido **por projeto/sessão com respostas reais das ferramentas**,
não por capacidades anunciadas no site do fornecedor. Documentação de instalação
e resultado de uso são categorias distintas. Nenhuma plataforma é escolhida
como método científico da pesquisa.

## Tabela de papéis, não de nomes de ferramentas

| Papel | Pergunta observável | Sem acesso verificado |
| --- | --- | --- |
| Carregamento da Skill | Os recursos `SKILL.md` e a referência necessária estão acessíveis no ambiente atual? | Registrar formato indisponível, não prometer execução |
| Persistência canônica | Google Drive está autenticado, com acesso ao espaço do projeto e escrita comprovada? | Exibir fluxo de conexão; sem êxito, exigir consentimento explícito ao `WORK_FALLBACK` antes de pesquisa substantiva |
| Descoberta acadêmica | Existe ferramenta disponível e qual foi a consulta efetivamente executada? | Propor consulta com status PLANNED/UNVERIFIED; não inventar resultados |
| Bases Scopus/WoS | Há acesso real ao sistema e export com origem, data, filtros e arquivo conferidos? | Preparar estratégia e instruir acesso autorizado do pesquisador |
| Execução determinística | Python / filesystem / comandos permitidos existem neste modo? | Não informar scripts como executados; fornecer instruções manuais, com limitações |
| Confirmação externa | Há recibo confiável de upload, escrita, export ou submissão? | `UNVERIFIED`, não `CONFIRMED` |
| Anonimização / direitos | Os arquivos exatos foram verificados sob regras editoriais e licenças? | Manter arquivo externo pendente de auditoria |

**Não preencher este quadro ficticiamente no projeto.** Use estados curtos:
`AVAILABLE_VERIFIED`, `AVAILABLE_NOT_TESTED`, `UNAVAILABLE`,
`UNKNOWN`. Distinguir explicitamente capacidade informada pelo
fornecedor de operação constatada **nesta sessão**. Esses rótulos
são comunicação de preflight, não nova planilha ou ID obrigatório.

## Observações documentais verificadas em outubro de 2026

- **ChatGPT:** documentação OpenAI descreve Plugins → Habilidades →
  Criar → Carregar do computador para contas elegíveis. A mesma fonte
  informa disponibilidade de Skills para contas qualificadas de
  organizações e sujeição às configurações do espaço de trabalho;
  a existência do menu não prova permissões de conectores, scripts ou Drive.
  [Fonte](https://help.openai.com/pt-br/articles/20001066-skills-in-chatgpt)
- **Claude:** o fornecedor descreve Skills personalizadas no claude.ai e
  no Claude Code. No claude.ai, o ZIP e as condições do plano importam;
  no Claude Code, Skills são diretórios locais `~/.claude/skills`
  ou `.claude/skills` do projeto. Instalar a Skill não equivale a
  instalar cada servidor MCP, ferramenta ou conector.
  [Fonte](https://platform.claude.com/docs/pt-BR/agents-and-tools/agent-skills/overview)
- **Gemini:** o Google documenta upload de `SKILL.md`, pasta e ZIP com
  entrada na raiz em contas/superfícies elegíveis; avisa que não há
  suporte a scripts que exigem acesso à internet nas Skills e que
  anexos binários como `.xlsx` não são formatos de referência aceitos
  no upload. Recursos e disponibilidade são graduais.
  [Fonte](https://support.google.com/gemini/answer/17094296?hl=pt-BR)

As páginas informam produtos externos sujeitos a mudança. Não se
declaram aqui importação, execução, integração com Drive, escrita,
retomada de projetos ou desempenho do Meu Artigo observados
nessas plataformas. A versão pública mais recente identificada no
repositório é `v0.8.0-beta.8`; a branch `main` poderá conter código
posterior até publicação manual de outra release.

## Falhas normais e resposta segura

1. Se conexão ainda exige ação do titular, apresentar o processo de
   autorização; não afirmar que a Skill clicou ou autenticou.
2. Se não existe ferramenta de Scopus/WoS, registrar a consulta
   **planejada**, o caminho de export e a ausência de comprovante.
3. Se um modelo escreveu que “subiu ao Drive” mas não existe recibo
   confiável, manter o resultado como `UNVERIFIED`.
4. Se falta ferramenta Python, não executar um substituto imaginado
   em linguagem natural nem declarar scripts validados.
5. O critério para fechar um gate é a evidência metodologicamente
   apropriada e decisão humana real, não a facilidade de uma plataforma.

A verificação funcional de cada plataforma é tarefa distinta,
registrada em [validações pendentes](../docs/VALIDACOES-PENDENTES.md).
