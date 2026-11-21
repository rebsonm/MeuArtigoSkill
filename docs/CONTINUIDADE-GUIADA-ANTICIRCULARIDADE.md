# Continuidade guiada e sinal de circularidade (proposta incremental)

**Estado:** implementação experimental somente leitura, empilhada sobre as propostas
de coerência metodológica. Não constitui publicação ou recurso da referência
científica histórica `v0.9.0-beta.6`.

## Linha de base verificável

- Existe um roteador canônico: `scripts/next_step_router.py`.
- Existe o resumo de retomada: `scripts/research_resume_brief.py`.
- Existe o explicador de bloqueios: `scripts/research_blocker_guide.py`.
- A apresentação tradicional do resumo mostra códigos e referências técnicas,
  mas não oferece no próprio resumo uma condição de saída da ação indicada.
- O registro TRACE já guarda comprovantes de execuções locais e hashes; não
  existe uma prova geral de equivalência semântica de todas as tentativas.
- Na PR imediatamente anterior, a suíte executou 815 testes sem falhas.

Não há medida de tempo, esforço cognitivo ou produtividade de usuários reais.

## Escolha arquitetural

A melhoria está dentro do resumo existente, sem registrar uma segunda lista
de tarefas, outro sistema de gates ou outra fonte de verdade. A mesma
projeção do painel e o mesmo roteador determinam a ação. O modo guiado
apresenta a informação essencial; o modo JSON existente preserva os detalhes.

Execução num projeto local com fallback autorizado:

```bash
python scripts/research_resume_brief.py PROJECT --format guided
python scripts/research_resume_brief.py PROJECT --format guided-json
python scripts/research_resume_brief.py PROJECT --format json
```

O texto guiado informa: situação, estado registrado (não validação),
pendência, uma única próxima ação, motivo e condição de conclusão.
A descrição de um critério de saída **não comprova** que ele foi atendido.
Não há classificação automática de conclusão científica do manuscrito.

## Heurística anticircularidade (escopo inicial estrito)

O sinal experimental usa apenas comprovantes TRACE existentes e, por
segurança, está limitado a projetos com `WORK_FALLBACK` autorizado e
continuidade conciliada. Ele inspeciona as duas últimas entradas TRACE
registradas para a mesma tarefa canônica e requer:

1. Duas tentativas reais `FAILED`/`PARTIAL` do mesmo script permitido.
2. Comprovantes locais referenciados no TRACE, íntegros por SHA-256.
3. Mesmo script, versão registrada, fingerprint dos argumentos e entradas.
4. Nenhum avanço observável nas saídas ou nos arquivos de entrada.
5. Tarefa não declarada recorrente e operação diferente das verificações
   rotineiras, que podem legitimamente ser repetidas.

Se todos os critérios forem atendidos, o resumo recomenda **diagnosticar
o impedimento**, sem criar uma tarefa, emitir nova aprovação ou proibir
a execução posterior. O código não verifica a verdade do que foi
executado fora do processo local, nem a equivalência semântica de ações
distintas, nem afirma que o trabalho científico permaneceu estagnado.

**Ausência de comprovantes não prova circularidade.** Uma alteração real de
entradas ou de abordagem mantém a possibilidade legítima de novo ciclo.
Para projetos no Drive, a leitura local continua insuficiente para esse
diagnóstico: é necessário conferir a origem canônica com ferramentas
autorizadas; nenhuma sincronização é presumida.

## Critérios de aceitação e métricas

| Indicador | Base anterior observável | Critério técnico proposto |
| --- | --- | --- |
| Uma ação principal na retomada | Resumo em códigos, sem apresentação orientada explícita | Exatamente uma ação e um critério de saída |
| Perguntas duplicadas sobre decisão | Não mensurado empiricamente | Não sobrepor decisão humana à tarefa já autorizada |
| Duas tentativas sem progresso | Sem sinal de diagnóstico no resumo | Sinal somente com dois comprovantes equivalentes válidos |
| Falso bloqueio por dado novo | Não mensurado empiricamente | Sem sinal de ciclo quando muda o fingerprint da entrada |
| Falso bloqueio de rotina | Não mensurado empiricamente | Não alertar monitoramento declarado e verificação rotineira |
| Reconciliação do Drive | Acesso local não prova sincronização | Falhar fechado sem inventar estado |
| Registros novos | Nenhum neste incremento | Zero novos registros canônicos |
| Preservação da governança | Gates dependem do pesquisador | Zero aprovações e zero alterações canônicas |
| Compatibilidade | 815 testes na base anterior | Toda a regressão e novos testes no commit proposto |

Não declarar redução percentual de fricção, ganho de produtividade nem
validade científica sem avaliação independente. O contador de testes
será preenchido somente com resultado efetivo do CI.

## Encerramento e fases pendentes

Esta primeira etapa não automatiza os estados **CONCLUÍDO** ou
**ENCERRADO COM RESSALVAS** para projetos inteiros: exigiria conferir
critérios de entrega e decisões científicas efetivas. Por enquanto,
**BLOQUEADO** representa impedimentos tecnicamente registrados.

Próximas evoluções condicionadas a evidências:

- Integrar avisos de circularidade para operações externas apenas quando
  existirem recibos ou eventos equivalentes verificáveis.
- Tratar fechamento com ressalvas sem ultrapassar gates obrigatórios.
- Reutilizar `METHOD_PROFILE`, DEC, TRACE e o ledger de claims para
  dependências documentadas e hipóteses de retirada de fontes.
- Comparar por testes A–L e posteriormente avaliar com pesquisadores
  reais, respeitando eventual revisão ética quando aplicável.

**Limite:** código e testes de software não são estudos de usabilidade,
provas de validade metodológica, nem autorização de avanço científico.
