# Compatibilidade entre plataformas — Meu Artigo

Esta página distingue **o que os fornecedores documentam** da **verificação efetiva desta versão do Meu Artigo**. Uma plataforma reconhecer o formato `SKILL.md` não significa que todas as integrações, scripts e funcionalidades do projeto executem corretamente.

| Plataforma | Importação de Skill: o que está documentado | O que está comprovado nesta versão | O que ainda exige teste real |
| --- | --- | --- | --- |
| **ChatGPT** | Contas elegíveis podem carregar Skills em **Plugins → Habilidades → Criar → Carregar do computador**. | Estrutura do ZIP e testes automatizados independentes da interface. Há registro anterior de importação de versão diferente; **não valida a beta atual**. | Instalação da `v0.8.0-beta.8`, ativação, integração com Drive, execução de tarefas e retomada entre conversas. |
| **Claude** | Claude suporta Skills personalizadas via claude.ai e Claude Code. | Organização da pasta e compatibilidade estrutural do arquivo `SKILL.md`. | Upload desta beta, scripts permitidos, conectores disponíveis e persistência real. |
| **Gemini** | Google documenta upload de `SKILL.md`, pasta ou ZIP contendo `SKILL.md` na raiz; o recurso varia por conta/região. | O ZIP contém a estrutura exigida; testes automatizados independentes da interface. | Importação e fluxo completo, possibilidades de execução, Drive e limitações de rede. |

## Fontes oficiais

- [Skills no ChatGPT — OpenAI](https://help.openai.com/pt-br/articles/20001066-skills-no-chatgpt)
- [Agent Skills — Anthropic](https://platform.claude.com/docs/pt-BR/agents-and-tools/agent-skills/overview)
- [Criar e gerenciar Skills — Google Gemini](https://support.google.com/gemini/answer/17094296?hl=pt-BR)

Essas fontes orientam **disponibilidade e instalação de Skills**. Não garantem que a plataforma ofereça Scopus, Web of Science, navegação autenticada, todas as ações de Google Drive ou execução local. Verifique cada operação antes de registrar uma etapa como concluída.

## Padrão de armazenamento

Google Drive é o destino persistente preferencial. É preciso confirmar conexão e permissão de escrita; a simples presença do aplicativo não é comprovante de sincronização. Se o Drive continuar indisponível, a Skill deve pedir **autorização explícita para utilizar outra forma de armazenamento** e não avançar sem essa autorização.

## Como registrar um teste futuro

Para cada plataforma, registrar a versão exata da Skill, a superfície utilizada, os recursos disponíveis, o que foi executado, os comprovantes de escrita/retomada e as limitações. Não tratar importação bem-sucedida como validação científica ou demonstração de compatibilidade integral.

A execução dos testes funcionais entre plataformas permanece **PENDENTE** e integra o [plano de validações](VALIDACOES-PENDENTES.md). Os [guias individuais](COMECE-AQUI.md) são para instalação e primeiros passos, não relatórios de desempenho.
