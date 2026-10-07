# Protocolo de teste com usuários — Meu Artigo

## Objetivo

Avaliar se a Skill funciona para pessoas que **não participaram de sua criação**, em diferentes IAs, sem depender de explicações prévias do autor.

O teste deve medir três coisas separadamente:

1. qualidade da **metodologia científica**;
2. qualidade da **gestão C.A.D.A. e visibilidade do passo a passo**;
3. qualidade da **implementação em cada plataforma**.

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
- evita chamar qualquer busca estruturada de revisão sistemática;
- cria `11_CADA_Control` e um painel C.A.D.A.;
- mostra claramente a etapa atual e a próxima ação.

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

## Cenário E — gestão C.A.D.A. e gerenciador externo

Quando a plataforma oferecer ClickUp, Jira/Atlassian, Trello ou equivalente, testar também a camada de gestão.

Observar se:

- a Skill escolhe ou reutiliza **um** gerenciador principal, sem duplicar o projeto em vários;
- cada tarefa externa mostra o `CADA_ID`;
- as tarefas são criadas em nível útil de gestão, sem gerar um card para cada referência bibliográfica;
- responsável, próxima ação, prazo, status e bloqueio ficam compreensíveis;
- `11_CADA_Control` permanece como controle canônico;
- `12_PM_Sync` registra o vínculo com a tarefa externa;
- marcar um card como concluído não altera sozinho uma decisão científica;
- ao perguntar **“onde estamos?”**, a IA informa etapa, concluídos, pendências, bloqueios, prazo e próxima ação.

O teste também deve ser feito sem gerenciador externo. Nesse caso, avaliar se o modo `MATRIX_ONLY` permite gerir o artigo integralmente pela planilha, sem exigir conhecimento prévio de ClickUp, Jira ou Trello.

## Cenário F — rastreabilidade do processo

Avançar o projeto até que ocorram algumas decisões materiais e depois verificar se é possível reconstruí-las sem recorrer ao histórico do chat.

Observar se:

- existe `RASTREABILIDADE.md`;
- `13_Traceability_Log` registra eventos materiais com `Trace_ID`;
- mudanças de pergunta, método, busca, corpus, síntese ou manuscrito deixam trilha;
- ações relevantes ligam CADA_ID aos Search_ID/Record_ID/Evidence_ID/Claim_ID correspondentes;
- usos materiais de IA aparecem em `14_AI_Use_Log`;
- finalidade e ferramenta/modelo são registradas quando conhecidas;
- usos substantivos de IA registram um procedimento real de validação humana;
- a pessoa consegue responder **“como chegamos a esta versão do artigo?”** sem depender da memória da conversa.

Falha se a IA apenas produzir documentos finais sem deixar proveniência suficiente para reconstruir o processo.

## Cenário G — pacote auditável e interoperabilidade

Quando o projeto já tiver rastreabilidade suficiente, pedir:

> Gere um pacote auditável deste artigo.

Observar se:

- a IA gera ou propõe export W3C PROV / RO-Crate sem exigir que o usuário conheça os padrões;
- o pacote recebe `EXPORT-####`;
- `16_INTEROPERABILIDADE` registra o export;
- existe `ro-crate-metadata.json`;
- existe `provenance/prov.jsonld`;
- existe `manifest-sha256.txt`;
- o validador confirma a estrutura/checksums;
- full texts protegidos não são incluídos automaticamente;
- warnings de proveniência ficam visíveis;
- a IA não confunde “pacote válido” com “pesquisa cientificamente válida”.

## Formulário de avaliação

Escala de 1 a 5:

| Critério | Pergunta |
|---|---|
| Clareza inicial | Ficou claro o que você precisava fornecer? |
| Autonomia | A IA avançou sem pedir confirmações desnecessárias? |
| Direcionamento | A IA realmente conduziu a pesquisa? |
| Organização | O projeto ficou organizado e compreensível? |
| Passo a passo | Você conseguia saber em que etapa estava e o que vinha depois? |
| C.A.D.A. | Responsável, prazo, status, bloqueios e evidências de conclusão ficaram claros? |
| Rastreabilidade | Você consegue descobrir de onde vieram decisões, contagens e mudanças importantes do artigo? |
| Transparência de IA | Ficou claro onde a IA atuou e como o pesquisador validou o que foi usado? |
| Gestão por planilha | Você conseguiria gerir o projeto só pela matriz, sem Trello/Jira/ClickUp? |
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
CADA_Control criado:
Gerenciador externo:
Container externo:
PM_Sync criado:
Traceability_Log criado:
AI_Use_Log criado:
RASTREABILIDADE.md criado:
CADA_Dashboard criado:
Modo de gestão (MATRIX_ONLY/MATRIX_PLUS_EXTERNAL):
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
- perder ou duplicar CADA_IDs;
- tratar o gerenciador externo como fonte de verdade científica;
- não registrar mudanças metodológicas materiais na trilha de rastreabilidade;
- usar IA substantivamente sem registrar qualquer forma de validação humana;
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


## Cenário G — governança científica

Levar o projeto até pelo menos um gate crítico e observar se:

- uma decisão material recebe DEC_ID;
- alternativas e justificativa ficam registradas;
- a Skill não pede aprovação em tarefas rotineiras;
- o gate fica READY somente quando a condição de entrada é atendida;
- a aprovação humana é explícita;
- a aprovação gera um SNAP_ID;
- o pesquisador consegue comparar dois snapshots;
- o relatório para revisor/editor reflete apenas os artefatos canônicos;
- é possível reconstruir: decisão → ação → evidência → validação → estado congelado.

Falha crítica se a Skill marcar um gate como aprovado sem resposta humana explícita.


## Cenário H — Mapa do Corpus e Grounded Corpus Mode

Aplicar somente quando o projeto real do testador já tiver corpus retido e full text disponível.

Observar se:

- `20_MAPA_CORPUS` usa somente metadados reais;
- campos sem metadados permanecem vazios ou aparecem como warning;
- a Skill não chama o desenho de bibliométrico apenas por gerar o mapa;
- clusters só aparecem quando existe uma relação de rede operacionalmente definida;
- uma pergunta em Grounded Corpus Mode usa somente CORE/SUPPORT com full text disponível;
- a resposta material aponta Record_ID/Evidence_ID/locator quando disponíveis;
- a Skill informa quando o corpus não sustenta a resposta;
- conhecimento externo não entra silenciosamente;
- sínteses ou claims materiais seguem para validação humana.

Falha crítica se a Skill inventar metadados, citações, clusters, evidências ou completar uma resposta grounded com conhecimento externo sem declarar a mudança de modo.


## Cenário I — revista-alvo desde o intake

Aplicar com uma revista e regras reais escolhidas pelo próprio testador.

Observar se:

- a Skill pergunta pela revista-alvo logo no início;
- pede regras oficiais e template/layout quando houver;
- cria/atualiza JOURNAL_PROFILE sem inventar requisitos;
- distingue contrato formal de perfil científico/editorial;
- usa as regras para orientar estrutura e checklist desde a construção;
- registra fonte e data de verificação;
- não muda resultados/evidências para melhorar aderência;
- se não houver revista, continua em JOURNAL_NEUTRAL sem bloquear.

Falha crítica se a Skill inventar regra editorial ou afirmar conformidade sem ter lido a fonte.

## Cenário J — robustez dos claims

Aplicar somente quando existirem claims reais do projeto.

Observar se, antes do GATE-0006:

- cada claim material tem Evidence_IDs;
- evidência contrária é procurada/registrada quando existe;
- explicações alternativas são consideradas;
- condições de contorno ficam explícitas;
- dependência de fonte única é identificada;
- claims QUALIFIED levam sua qualificação ao manuscrito;
- claims REVISE/REJECT impedem congelamento indevido;
- a validação humana é real, não inferida.

Falha crítica se o GATE-0006 for aprovado com claims materiais ainda NOT_AUDITED, REVISE ou REJECT.
