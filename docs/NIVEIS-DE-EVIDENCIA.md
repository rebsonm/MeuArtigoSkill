# Níveis distintos de comprovação científica

O **Meu Artigo** não transforma automaticamente um registro de sistema em
confirmação científica. Há quatro perguntas diferentes e nenhum nível pode
ser inferido do anterior. Esse desdobramento é uma **regra de integridade do
software**, não uma escala metodológica validada por terceiros.

| Nível | O que é constatável | O que ainda não foi demonstrado |
|---|---|---|
| 1. Identidade bibliográfica | Metadados do DOI, título, ano e autoria correspondem a registros acadêmicos consultados | Leitura do texto original, qualidade metodológica ou adequação à afirmação |
| 2. Passagem literal consultável | Uma sequência textual aparece em arquivo realmente acessível e identificado; relatório pode registrar hash e localização | Que a interpretação feita do trecho é correta ou representativa do estudo |
| 3. Julgamento humano documentado | A matriz declara validação/apreciação humana e aponta para uma manifestação original | Autenticidade independente da identidade do revisor e validade científica da conclusão |
| 4. Resultado empírico sustentado | Existem dados/materiais, procedimentos efetivamente realizados e análise/avaliação rastreável | Validade de inferência, ausência de vieses, generalização ou reprodução independente |

## Procedimento com os mesmos arquivos

- `05_Evidence_Matrix.csv`: registrar o que realmente foi examinado,
  `Evidence_ID`, o localizador e o papel da fonte.
- `SOURCE_VERIFICATION.json`: resultado da verificação de metadados e
  passagens conforme `scripts/verify_sources.py`, vinculado por SHA-256 à
  matriz. Apenas `metadata_status=VERIFIED` indica conferência documental de
  identidade bibliográfica; apenas `locator_status=MATCHED` indica que um
  trecho literal pôde ser encontrado na cópia consultada. Ambos podem estar
  ausentes e jamais provam suporte semântico.
- `09_Claims_Ledger.csv`: registrar `Claim_type`, fonte, `Trace_IDs`,
  limites, `Researcher_review_evidence` e status de revisão científica.
  As categorias **[L], [I] e [P] continuam independentes**: texto de fonte,
  inferência delimitada e proposição original não são intercambiáveis.
- `17_Decision_Log.csv`, `18_Human_Validation_Gates.csv` e
  `METHOD_PROFILE.json`: preservar manifestações originais do pesquisador,
  método escolhido e ligação a materiais, análises e integração quando
  houver afirmações sobre resultados empíricos.
- `EMPIRICAL_RESULT`: ao congelar as afirmações em projetos novos com rotas
  explícitas, exigir rota empírica/design science, referência documental
  de materiais e análise realmente realizada, decisões válidas de
  `GATE-0004` e `GATE-0005`, `Trace_IDs` e revisão humana rastreável.
  A presença desses campos **ainda não certifica** o achado ou a identidade
  de quem revisou: deve-se examinar as fontes originais e as condições da
  inferência. Um estudo apenas planejado permanece sem resultados.

Execute a inspeção conservadora de forma local, no workspace já autorizado:

```bash
python scripts/scientific_evidence_tiers.py /caminho/do/projeto
python scripts/scientific_evidence_tiers.py /caminho/do/projeto --freeze
```

A saída distingue contagens de **indícios documentais** e inclui os limites
`bibliographic_identity_proves_text_read=false`,
`literal_locator_proves_claim_semantics=false`,
`human_review_record_authenticates_reviewer=false` e
`empirical_scientific_result_independently_validated=false`.
Não produz pontuação de qualidade científica e não requer uma nova aba ou
família de identificadores.

A auditoria de fechamento `GATE-0006` usa essa verificação quando o
projeto tem governança metodológica ativa. Em projetos mais antigos,
a escolha de uma nova rota e a migração dos registros científicos requerem
decisão documentada: nunca preencher retroativamente uma validação.

## Limites e auditabilidade

- Uma simples referência de arquivo ou URL em `METHOD_PROFILE.json`
  **não prova** que o arquivo existe, está atualizado ou foi examinado.
  Sempre confira evidência original e permissões do projeto, inclusive
  quando Google Drive é o repositório canônico.
- A auditoria do script só verifica presença e coerência formal dos
  registros. Nenhum resultado de campo, análise estatística ou avaliação
  de artefato foi executado pelo ato de preencher esse protocolo.
- O reconhecimento de uma sequência literal não comprova a fidelidade
  semântica da interpretação; isso requer leitura contextualizada.
- Nenhuma inferência causal deve ser feita exclusivamente a partir de
  correlação, contraste simples antes/depois ou aprovação do protocolo.
- Os relatórios de testes de engenharia e os *gates* não equivalem a
  avaliação científica independente da Skill, que continua pendente.
