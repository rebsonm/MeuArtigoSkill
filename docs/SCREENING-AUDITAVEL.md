# Screening auditável: separar sugestões da IA de decisões científicas

Este procedimento utiliza a **mesma** tabela 03_Screening.csv e a **mesma** aba 07_SCREENING da matriz-mestra. Não introduz novas abas, famílias de IDs, contas pagas ou exigência de dois revisores humanos fictícios.

## O que significa cada etapa

**Pass1**: triagem de título e resumo; decisão final humana INCLUDE, BORDERLINE ou EXCLUDE.

**Pass2**: priorização após revisão mais próxima de título/resumo para os registros retidos em Pass1; valores FULL TEXT — CORE, FULL TEXT — SUPPORT ou EXCLUDE. Pass2 não substitui a avaliação de elegibilidade efetiva do texto completo em 04_FullText_Tracker.csv. Prioridade CORE/SUPPORT não significa qualidade metodológica.

Uma IA pode **propor** cada uma das decisões, explicando o motivo e apontando onde a sugestão foi produzida. Essa proposta nunca é escrita nos campos finais. A decisão só é registrada no campo final após uma resposta efetiva e atribuída ao pesquisador, preservando a referência à mensagem/documento que a originou.

## Campos adicionais nas tabelas já existentes

Para cada Pass1 e Pass2, a matriz possui:
- AI_proposal — decisão sugerida pela IA, ainda provisória;
- AI_reason — justificativa da sugestão, sem presumi-la verdadeira;
- AI_source — referência à mensagem ou saída real do modelo;
- reviewed_by — revisor humano identificado;
- review_evidence — referência à manifestação efetiva do revisor;
- disagreement_reason — razão registrada quando a decisão humana diverge da sugestão.

Os campos antigos Pass1_decision/Pass1_reason e Pass2_decision/Pass2_reason continuam representando a decisão final, sua motivação e o protocolo empregado. IDs de pesquisa existentes são preservados.

## Execução gratuita

Requer Python 3.10+ e biblioteca padrão. Exemplos de forma de comando, não de decisões reais:

    python scripts/screening_review.py propose "/projeto" --stage pass1 --record-id "R-0001" --proposal BORDERLINE --reason "O resumo possui indicadores pertinentes mas não descreve o contexto de aplicação." --source "Referência à saída real do agente"

Somente depois de o pesquisador realmente examinar os dados e manifestar sua decisão:

    python scripts/screening_review.py decide "/projeto" --stage pass1 --record-id "R-0001" --decision INCLUDE --reason "O resumo demonstra aderência ao critério de inclusão referente à governança documental." --reviewer "Pesquisador" --evidence "Referência à manifestação original do pesquisador" --disagreement-reason "O pesquisador identificou aderência ao conceito central que a recomendação inicial não reconheceu."

Quando houver discordância, o último argumento será obrigatório. A decisão original é preservada: não é permitido substituir silenciosamente um julgamento já gravado. Revisões posteriores devem ter novo registro no DEC_ID/TRACE_ID existente, com justificação e cópia versionada do estado anterior.

A execução do script confirma apenas que a tabela foi alterada. Um nome digitado em --reviewer não autentica a identidade humana nem comprova que o usuário leu o documento; o campo --evidence deve apontar para a mensagem ou revisão real e precisa ser conferido externamente.

## Auditoria e congelamento

    python scripts/screening_review.py audit "/projeto" --strict

Para conferir se há elementos pendentes antes de congelar o corpus:

    python scripts/screening_review.py audit "/projeto" --strict --freeze

Nos projetos novos, o parâmetro screening_human_decisions_required=true ativa a validação cruzada pelo script principal validate_project.py. O GATE-0004 aprovado não pode prosseguir com sugestões não apreciadas, revisores ausentes, exclusões sem justificativa, divergências sem resolução ou registros não duplicados sem decisões concluídas nas passagens aplicáveis.

O estado BORDERLINE exige uma resolução na Pass2 antes do congelamento. Duplicatas realmente identificadas exigem vínculo Canonical_record_id; sugestões do modelo não servem, isoladamente, para afirmar que um item é duplicado.

Projetos antigos mantêm a compatibilidade enquanto não ativarem a regra. Caso precisem migrar, as colunas novas são acrescentadas quando o primeiro evento é registrado, **sem inventar revisões retroativas**. Para auditar registros antigos sem modificá-los, execute audit --strict; a correção dos registros deve se basear em evidências humanas reais.

## Integridade e limitações

- Não usar a IA como segundo revisor humano independente. Havendo apenas um pesquisador, informar screening por revisor único e rechecagem de BORDERLINE e amostra de INCLUDE/EXCLUDE, conforme protocolo.
- Não excluir fontes apenas porque o texto completo está inacessível. Isso significa PENDING ACCESS na trilha de texto integral, não irrelevância científica.
- Não transformar a sugestão da IA em decisão final silenciosamente, nem gerar uma justificativa ou um revisor humano fictício.
- Exigir motivo claro para EXCLUDE e reexaminar os casos limítrofes; fontes potencialmente relevantes devem permanecer retidas até a revisão necessária.
- Revisão em lote só é válida quando o protocolo documenta um procedimento humano realmente realizado, com critérios, cobertura e referência ao registro de avaliação. Não atribuir automaticamente avaliações individuais à aprovação genérica de uma lista.
- Sem acesso ao Google Drive canônico, os CSVs e artefatos locais podem ser apenas staging autorizado. Sincronize revisões e referências de evidência ao workspace original antes de afirmar que a matriz canônica está atualizada.

Este controle é procedimental; não mede por si só sensibilidade/especificidade da triagem ou concordância entre avaliadores humanos. Essas afirmações exigem avaliação empírica separada.
