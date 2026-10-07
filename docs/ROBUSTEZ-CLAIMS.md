# Auditoria de robustez dos claims

O Meu Artigo não verifica apenas se uma afirmação possui alguma evidência.

Antes de congelar os claims principais, ele também pergunta:

> Esta afirmação resiste à contestação?

A auditoria acontece dentro do `GATE-0006 — Claims / auditoria científica`. Não cria nova aba nem novo identificador.

## Para cada claim material

A Skill verifica, quando aplicável:

- evidências que sustentam o claim;
- evidências contrárias no próprio corpus;
- explicações alternativas plausíveis;
- condições de contorno;
- dependência excessiva de uma única fonte;
- força e qualidade da sustentação;
- se a formulação vai além do que a evidência permite;
- classificação epistêmica: literatura `[L]`, inferência `[I]` ou proposição `[P]`.

## Teste de dependência

Quando houver uma evidência central, a Skill deve perguntar:

> Se esta evidência fosse retirada, o claim continuaria defensável?

Isso não é um teste estatístico universal. É uma checagem de dependência argumentativa.

## Status

O ledger pode registrar:

- `NOT_AUDITED`;
- `ROBUST`;
- `QUALIFIED` — defensável, mas exige condição/limite explícito;
- `REVISE`;
- `REJECT`;
- `NOT_APPLICABLE`.

Um claim `QUALIFIED` deve carregar a qualificação para o manuscrito.

## Regra

Evidência contrária não deve ser tratada automaticamente como motivo para excluir o claim.

Ela pode:

- reduzir sua força;
- restringir seu contexto;
- exigir reformulação;
- revelar heterogeneidade;
- criar uma contribuição teórica mais precisa.

## Validação humana

A IA pode identificar candidatos a contradição ou explicações alternativas.

A decisão de congelar um claim material permanece humana e é registrada no GATE-0006.

O objetivo é reduzir claims plausíveis porém frágeis e tornar explícitos os limites da argumentação.
