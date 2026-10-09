# Avaliação crítica da qualidade das fontes

Este componente verifica se a fonte é metodologicamente adequada à finalidade para a qual está sendo usada no artigo. **DOI verdadeiro não significa evidência robusta.** A Skill não emite automaticamente uma nota de qualidade nem substitui o julgamento do pesquisador.

## Abrangência gratuita

Requer Python 3.10+ e apenas a biblioteca padrão. O procedimento usa os mesmos Evidence_ID, a matriz canônica 05_Evidence_Matrix.csv e a aba existente 09_MATRIZ_EVID. Nenhum novo ID, nova aba ou serviço pago.

Famílias de critérios — ajustáveis ao desenho do artigo e ao protocolo:
- QUANTITATIVE: adequação do desenho, amostragem/viés, mensuração e análise;
- QUALITATIVE: adequação do desenho, amostragem/contexto, rastreabilidade da análise e reflexividade/limites;
- MIXED_METHODS: componentes quantitativo e qualitativo, integração de resultados e limitações da combinação;
- REVIEW: pergunta e escopo, cobertura de busca, seleção/extração e métodos de síntese/apreciação;
- CONCEPTUAL: precisão dos conceitos, coerência dos argumentos, diálogo com alternativas e limites de alcance;
- NORMATIVE: autoridade/versão, jurisdição/vigência, interpretação e distinção entre norma e achado empírico;
- OTHER: natureza da fonte, procedência, adequação ao claim e incerteza.

Essa é uma **lista de verificação operacional própria**, não uma reprodução nem certificação oficial de JBI, CASP, MMAT ou de outra escala. Quando a pesquisa ou revista exige instrumento validado específico, seguir suas regras e registrar a versão original; não fingir equivalência do checklist geral.

## Procedimento

1. Classifique a fonte por desenho real, não pelo prestígio ou fator de impacto da revista. Obras de natureza diferente não são comparáveis por um escore universal.
2. Gere um formulário estrutural sem preencher respostas automaticamente:

       python scripts/appraise_evidence.py template --family QUALITATIVE

   Salve o JSON em um arquivo temporário no workspace do projeto e preencha cada item com:
   - rating: YES, NO, UNCLEAR ou NOT_APPLICABLE;
   - basis: explicação fundamentada no texto efetivamente consultado, com indicação de seção/página se disponível.

3. A Skill pode preparar um quadro de informações para facilitar a leitura. **Não pode afirmar que realizou revisão humana** nem gerar respostas atribuídas ao usuário.
4. Após uma avaliação real do pesquisador, registre-a no CSV canônico, por exemplo:

       python scripts/appraise_evidence.py record "/caminho/do/projeto" \
         --evidence-id "EVID-0001" --family QUALITATIVE \
         --checklist "/caminho/do/projeto/criterios_avaliados.json" \
         --judgement USE_WITH_CAVEATS \
         --rationale "A análise responde ao problema, mas a seleção dos participantes limita a transferência dos achados." \
         --limitations "Os resultados são contextuais e não fundamentam extrapolação estatística para outras populações." \
         --reviewer "Pesquisador" \
         --review-evidence "Referência à manifestação humana original"

   Os textos acima são somente exemplos de **formato**. Não representam fonte examinada ou decisão humana real.

5. Para auditar documentação:

       python scripts/appraise_evidence.py audit "/caminho/do/projeto" --strict

## Julgamento científico registrado

- SUITABLE_FOR_CLAIM: avaliação humana registrada sem ressalvas nos itens aplicáveis. Só é permitido quando os itens do checklist são YES. Ainda assim, não é uma certificação automática da fonte.
- USE_WITH_CAVEATS: a fonte pode ser usada com restrições explicitadas, mantendo a qualificação nos claims.
- INSUFFICIENT_INFORMATION: o material disponível é insuficiente para sustentar o claim pretendido.
- DO_NOT_USE_FOR_CLAIM: o pesquisador julgou que não deve fundamentar a afirmação proposta.

A escolha desses estados continua sendo humana. O código rejeita inconsistências objetivas, como afirmar SUITABLE_FOR_CLAIM quando há item NO ou UNCLEAR, ou registrar critério sem fundamento. **Não conclui**, com base em quantos itens foram marcados YES, que a fonte é válida.

## GATE-0006 e integração com RT-01/RT-04

Novos projetos possuem critical_appraisal_required=true. Na aprovação do GATE-0006, o validador exige avaliação crítica para as Evidence_IDs efetivamente ligadas aos claims materiais (inclusive evidências contrárias). Uma evidência usada com julgamento INSUFFICIENT_INFORMATION ou DO_NOT_USE_FOR_CLAIM bloqueia o gate enquanto fundamentar o claim. Evidências qualificadas requerem justificativa científica e claims corretamente limitados.

Em projetos antigos, o modo não é ativado retroativamente. O campo Appraisal_criteria armazena JSON estruturado e os outros seis campos ficam na mesma linha da fonte. Atualizações posteriores requerem versionamento e novo registro de decisão: não sobrescrever silenciosamente avaliações já realizadas.

Uma alteração na matriz de evidências modifica seu SHA-256; portanto, relatórios de verificação de fontes do RT-01 deverão ser **regenerados** após a conclusão das avaliações antes do congelamento final.

## Limitações

- Um nome digitado como revisor não autentica a identidade da pessoa.
- Preenchimento não comprova qualidade real, interpretação correta nem acesso ao full text.
- Informação obtida apenas por resumo deve continuar marcada como tal; não extrapolar a crítica além do material acessado.
- Não excluir automaticamente fontes com ressalvas. A pertinência e o peso argumentativo dependem da pergunta e do tipo de afirmação.
- Livros conceituais, normas e estudos empíricos têm funções epistemológicas distintas. Não misturar autoridade normativa e demonstração empírica.
- Em projetos com Drive canônico, sincronizar os CSVs, manifestações humanas e checklist preenchido antes de afirmar que o workspace oficial está atualizado.

A ferramenta é um registro auditável da avaliação crítica, **não uma revisão por pares independente**.
