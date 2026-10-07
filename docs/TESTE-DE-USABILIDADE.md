# Protocolo de teste com usuários — Meu Artigo

## Objetivo

Avaliar se a Skill funciona para pessoas que **não participaram de sua criação**, em diferentes IAs, sem depender de explicações prévias do autor.

O teste deve medir duas coisas separadamente:

1. qualidade da **metodologia**;
2. qualidade da **implementação em cada plataforma**.

## Regra principal

O participante não deve receber uma aula sobre o workflow antes do teste.

Entregue apenas:

- link/arquivo da Skill;
- instrução de instalação correspondente à IA;
- uma frase pedindo que use um problema de pesquisa próprio.

Não explique pastas, matriz, screening, Consensus, Scite, PRISMA, deduplicação ou `CONTINUIDADE.md` antes da primeira execução.

## Amostra inicial sugerida

Mínimo útil:

- 2 participantes no ChatGPT;
- 2 participantes no Claude;
- 2 participantes no Gemini.

Idealmente misture:

- pesquisador experiente;
- pós-graduando;
- usuário com pouca experiência em IA;
- usuário com pouca experiência em revisão de literatura.

Evite que todos testem o mesmo tema.

## Tarefa do participante

Mensagem-padrão:

> Instale a Skill Meu Artigo. Depois use apenas o seu problema de pesquisa para começar. Trabalhe normalmente e não tente seguir um roteiro escondido. Quando a IA pedir algo, responda como você responderia em um projeto real.

Exemplo de formato de entrada:

> Meu problema de pesquisa é: [problema]. Quero desenvolver um artigo científico.

## Cenário A — início do zero

Observar se a Skill:

- preserva o problema original;
- identifica quando o tema está amplo;
- faz auditoria inicial de novidade;
- começa a pesquisar em vez de apenas explicar como pesquisar;
- verifica ferramentas/integrações;
- cria ou propõe persistência;
- cria `CONTINUIDADE.md`;
- cria protocolo e matriz de acompanhamento;
- diferencia método de ferramenta;
- evita chamar qualquer busca estruturada de revisão sistemática.

## Cenário B — busca bibliográfica

O participante deve avançar até pelo menos uma rodada de busca.

Observar se:

- blocos conceituais foram construídos;
- string literal ficou registrada;
- filtros ficaram separados da lógica conceitual;
- contagens foram registradas;
- export bruto foi preservado;
- a IA detectou limitações reais de acesso;
- não inventou Scopus/WoS/conectores.

## Cenário C — continuidade

Este é um teste obrigatório.

1. interromper o trabalho no meio de uma etapa;
2. fechar a conversa;
3. abrir uma conversa nova;
4. disponibilizar apenas a Skill e os artefatos persistidos;
5. pedir: **“Continue meu artigo.”**

Sucesso significa que a nova sessão consegue identificar:

- problema;
- pergunta atual;
- método;
- decisões congeladas;
- buscas já feitas;
- contagens;
- estado do screening/full text/evidências;
- bloqueios;
- próxima ação válida.

Se depender de o usuário recontar tudo, a persistência falhou.

## Cenário D — portabilidade

O mesmo participante ou um segundo participante pode usar o mesmo problema em duas plataformas.

Comparar:

- número de perguntas desnecessárias;
- tempo até a primeira pesquisa útil;
- qualidade do protocolo;
- capacidade de persistência;
- qualidade da busca;
- aderência ao método;
- transparência de limitações;
- retomada;
- tendência a inventar capacidades.

Não comparar apenas a qualidade textual do manuscrito.

## Formulário de avaliação

Escala de 1 a 5:

| Critério | Pergunta |
|---|---|
| Clareza inicial | Ficou claro o que você precisava fornecer? |
| Autonomia | A IA avançou sem pedir confirmações desnecessárias? |
| Direcionamento | A IA realmente conduziu a pesquisa? |
| Organização | O projeto ficou organizado e compreensível? |
| Rastreabilidade | Você consegue descobrir de onde vieram decisões e contagens? |
| Continuidade | Outro chat conseguiu retomar o trabalho? |
| Rigor | A IA evitou inventar resultados, fontes e métodos? |
| Usabilidade | Você conseguiria usar isso sem ajuda do criador? |
| Confiança | Você confiaria no processo para um artigo real? |
| Valor | A Skill reduziu trabalho operacional sem tirar seu controle científico? |

Perguntas abertas:

1. Em que momento você ficou confuso?
2. O que a IA pediu que parecia desnecessário?
3. O que ela deveria ter feito automaticamente e não fez?
4. Houve alguma coisa que ela afirmou sem evidência?
5. Você entendeu onde estavam salvos os dados do projeto?
6. A nova conversa conseguiu continuar?
7. Qual foi a parte mais útil?
8. Qual foi a parte mais frustrante?
9. Você usaria novamente?
10. O que mudaria primeiro?

## Registro técnico mínimo

Para cada sessão, registrar:

```text
Test_ID:
Data:
Plataforma:
Modelo:
Plano/conta:
Skill_version/commit:
Tema:
Experiência do participante:
Integrações disponíveis:
Integrações ausentes:
Workspace criado:
CONTINUIDADE.md criado:
Matriz criada:
Auditoria de novidade iniciada:
Método proposto:
Busca executada:
Export validado:
Erros observados:
Intervenções humanas extras:
Teste de retomada:
Resultado da retomada:
Observações:
```

## Critérios de falha crítica

Marcar como falha crítica se ocorrer qualquer um:

- inventar artigo/citação;
- inventar acesso a base;
- inventar contagem;
- dizer que leu full text quando não leu;
- reutilizar conteúdo substantivo de outro projeto sem pedido;
- chamar o método de sistemático sem base;
- sobrescrever histórico de busca executada;
- não preservar estado suficiente para retomada;
- produzir manuscrito sem trilha de evidência.

## Critério de sucesso da versão

Uma versão pode ser considerada robusta quando:

- usuários externos conseguem iniciar sem treinamento;
- a maior parte das etapas operacionais acontece autonomamente;
- decisões científicas importantes ficam visíveis;
- falhas de ferramenta são registradas sem virar invenção;
- o workflow é retomável;
- o núcleo funciona em pelo menos duas plataformas sem alteração metodológica;
- diferenças entre plataformas ficam limitadas aos adapters/capacidades.

## Feedback para o repositório

Após cada rodada, consolidar feedback em quatro classes:

- **CORE** — falha da metodologia central;
- **ADAPTER** — falha específica de uma plataforma;
- **UX** — instrução/onboarding confuso;
- **TOOLING** — limitação ou erro de integração/script.

Isso evita corrigir uma limitação do Gemini, Claude ou ChatGPT alterando indevidamente a metodologia universal.
