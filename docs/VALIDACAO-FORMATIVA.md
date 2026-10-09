# Validação formativa de decisões científicas

A Skill conduz as etapas operacionais autonomamente, mas exige que as transições científicas relevantes sejam compreendidas e deliberadas pelo pesquisador. O objetivo não é criar um questionário longo ou fazer o modelo produzir justificativas em nome do usuário.

## Onde se aplica

Nos novos projetos, `formative_gates_required=true` no `PROJECT_CONFIG.json` habilita o controle em aprovações dos `GATE-0001` a `GATE-0006`. Os sete gates existentes são preservados. O `GATE-0007`, dedicado à liberação de arquivos e submissão, mantém as salvaguardas próprias, sem resposta formativa adicional obrigatória.

Projetos antigos, sem essa opção, preservam sua compatibilidade; ativar o modo requer uma decisão explícita de migração. O recurso utiliza somente Python padrão e os campos existentes de `18_Human_Validation_Gates.csv` — não introduz planilhas, IDs, conectores nem custos.

## Como apresentar um gate

1. A IA apresenta, em linguagem simples, a decisão proposta, as principais alternativas, a evidência e as limitações. Evite jargões e uma resposta-modelo pronta.
2. Peça duas respostas curtas **do próprio pesquisador**:
   - Por que esta escolha é adequada ao problema do artigo?
   - Qual é uma limitação, risco ou possível alternativa dessa escolha?
3. Caso o pesquisador tenha dúvida, explique o conceito e mantenha o gate pendente. Pergunte novamente de modo direto; não produza uma resposta e a atribua ao pesquisador.
4. Preserve a referência verificável à resposta humana em `Validation_evidence` e registre a justificativa e a limitação no campo `Notes` em formato estruturado. Somente após isso a aprovação poderá ser registrada. Um "sim", "ok" ou justificativa em branco não é suficiente.

Exemplo de comando **com respostas demonstrativas apenas na documentação**:

```bash
python scripts/governance_events.py gate /caminho/do/projeto \
  --gate-id GATE-0002 \
  --decision APPROVED \
  --validated-by "Pesquisador" \
  --method "Revisão do protocolo metodológico" \
  --evidence "Referência à mensagem original do pesquisador" \
  --researcher-rationale "O desenho reúne perspectivas teóricas diferentes para esclarecer uma questão conceitual." \
  --researcher-limitation "A abrangência depende das fontes consultadas e das escolhas de seleção da literatura."
```

Os textos acima **não representam resposta humana real** e não podem ser copiados como evidência de decisão efetiva. Na utilização normal, extraia esses argumentos da manifestação direta do usuário, não de texto sugerido pelo agente.

## Auditoria e limites

O registrador bloqueia uma aprovação sem justificativa e limitação minimamente substantivas; `validate_project.py` também rejeita gates científicos concluídos com registros formativos ausentes, malformados ou discordantes de `Validation_evidence`/`Validated_by`/`Decision`.

A checagem automática detecta lacunas de preenchimento e incoerência estrutural; **não mede compreensão real**, não autentica a identidade de quem digitou o texto e não prova autoria humana. Uma justificativa extensa e plausível ainda poderá ser incorreta ou gerada artificialmente. Preservar a mensagem original e realizar revisão humana continua indispensável.

A própria Skill deve evitar produzir `researcher-rationale` ou `researcher-limitation` como se fossem respostas do pesquisador. Se a resposta for ambígua, pedir esclarecimento sem emitir aprovação. Registros estruturados internos podem conter detalhes sensíveis e não devem ser incluídos indiscriminadamente em pacotes de avaliação cega.

## Relação com o método de pesquisa

A aprovação não substitui avaliação metodológica, evidências, integridade do corpus ou auditorias independentes. Ela demonstra apenas que uma escolha científica foi explicitamente assumida e explicada pelo usuário, dentro das limitações dos controles disponíveis.
