# Rotas metodológicas operacionais — Meu Artigo

O desenho científico é uma **decisão do pesquisador**, e não uma propriedade
inferida da disponibilidade de ferramentas, bases de dados ou de um modelo de IA.
Este roteiro operacionaliza de modo **condicional** fundamentos já documentados
em [fundamentação metodológica](../references/methodological-foundations.md)
e [desenho de artigo/revisão](../references/review-design.md). A implementação
não constitui instrumento metodológico validado nem metodologia específica
atribuída aos autores consultados.

## 1. Decisão e continuidade

- Inicializar o projeto preserva o texto original do problema. O argumento
  `--article-type` é apenas um rótulo; classes ambíguas ficam `UNDECIDED`.
  O argumento opcional `--method-route` seleciona um caminho provisório.
- O planejamento é guardado em
  `00_Gestao_e_Continuidade/METHOD_PROFILE.json`, sem novos identificadores
  de decisões, planilhas ou *gates*.
- A escolha só pode ser confirmada com **decisão humana real**, referência
  verificável de sua manifestação e justificativa registrada:
  ```bash
  python scripts/choose_method_route.py PROJETO \
    --route QUANTITATIVE \
    --decided-by "Pesquisador responsável" \
    --evidence "REFERENCIA_REAL_DA_MANIFESTACAO" \
    --rationale "JUSTIFICATIVA_REAL_FORMULADA_PELO_PESQUISADOR"
  ```
  Os trechos em maiúsculas são campos para dados reais; o comando **não**
  preenche respostas sozinho. A identidade alegada é registrada, não
  criptograficamente autenticada. O programa utiliza os registros DEC e TRACE
  já existentes e preserva os demais documentos.
- Se a pesquisa avançou a *gates* decisivos, a alteração automática de rota
  é bloqueada; exige revisão humana dos procedimentos e estados existentes,
  nunca reconstrução ou apagamento silencioso.
- A rota pode ser reexaminada pelo pesquisador. Para projetos antigos sem
  `method_route_governance_required`, não há migração automática de
  avaliações, arquivos ou decisões: a compatibilidade é preservada.

## 2. Panorama dos caminhos

| Rota | Pergunta científica central | Evidência/atividade relevante | Etapa que não deve ser imposta |
|---|---|---|---|
| `INTEGRATIVE_REVIEW` | Que entendimento novo resulta da integração crítica? | Busca delimitada, avaliação de estudos, categorias, tensões | Cobertura universal apenas por usar bases indexadas |
| `SYSTEMATIC_REVIEW` | Qual resposta decorre do conjunto elegível definido em protocolo? | Busca abrangente proporcional, elegibilidade, risco de viés, síntese | Uso automático da etiqueta sistemática só por seguir PRISMA |
| `PROBLEMATIZING_REVIEW` | Quais pressupostos precisam ser desafiados? | Literatura teoricamente seletiva, contraposições, reformulação | Triagem exaustiva como requisito universal |
| `CONCEPTUAL_THEORY` | Que mecanismo, argumento ou proposição se justifica? | Trabalhos próximos, linhagem conceitual, objeções, fronteiras | Coleta de campo e teste estatístico obrigatório |
| `QUALITATIVE` | Que sentidos, práticas ou processos ocorrem em um contexto? | Casos, participantes, documentos, reflexividade e interpretação | Supor que confiabilidade estatística define toda pesquisa interpretativa |
| `QUANTITATIVE` | Que descrição, associação, predição ou efeito é defensável? | Unidades, instrumentos, amostra observada, análise executada | Declarar causalidade a partir de correlação ou teste isolado |
| `MIXED_METHODS` | Por que e como integrar componentes QUAN e QUAL? | Vertentes substantivas, ponto real de integração, discordâncias | Tratar gráficos mais entrevistas como integração automática |
| `DESIGN_SCIENCE` | Que artefato resolve um problema e com que evidência de avaliação? | Problema, requisitos, construção verificável, avaliação real | Alegar efetividade só porque o artefato foi desenhado |

## 3. A Cebola de Pesquisa como conferência de coerência

O perfil contempla as seis camadas explicadas em
[fundamentos](../references/methodological-foundations.md#31-a-cebola-de-pesquisa-research-onion-integração-das-escolhas):
posição filosófica pertinente, lógica de desenvolvimento da teoria,
escolha metodológica, estratégia de investigação, horizonte temporal e
procedimentos/técnicas. Registra também a justificativa de **coerência**
entre pergunta, inferência visada e métodos.

As camadas **não têm correspondência determinística**. A posição
filosófica não é uma classificação imposta pelo algoritmo. Nos projetos
empíricos, a decisão de liberar o desenho verifica apenas que estratégia,
procedimentos e justificativa foram documentados; sua suficiência
epistemológica é avaliada pelo pesquisador, e não pelo código. Para
outros desenhos, preencher cada campo da cebola é opcional, desde que
seja explicitado o argumento pertinente ao tipo de pesquisa.

A interface **MINIMAL** pede somente a próxima decisão substantiva e seu
principal limite. A interface **FULL** expõe o registro técnico completo.
Os controles científicos subjacentes permanecem idênticos.

## 4. Controles particulares

**Quantitativo:** diferenciar `DESCRIPTIVE`, `ASSOCIATIONAL`,
`PREDICTIVE` e `CAUSAL` antes de propor inferências.
Registrar população/unidade, amostragem, mensuração, fontes de dados,
análise e limitações inferenciais. Para linguagem causal, requer-se
justificativa de identificação apropriada (por exemplo, contrafactual,
intervenção ou hipótese explícita e defensável); um modelo de regressão
não identifica efeito por si. Cálculo de poder, teste de pressupostos,
estimação e significância só podem ser relatados após execução e evidência.

**Qualitativo:** declarar tradição metodológica quando pertinente
(fenomenologia, narrativa, estudo de caso, *grounded theory* etc.),
unidade/fenômeno, seleção, materiais, análise e reflexividade.
Critérios de qualidade devem respeitar a tradição; não impor Kappa ou
saturação como regra universal.

**Misto:** declarar desenho `CONVERGENT`,
`EXPLANATORY_SEQUENTIAL`, `EXPLORATORY_SEQUENTIAL` ou `EMBEDDED`,
componentes QUAN e QUAL e o mecanismo de integração `CONNECTING`,
`BUILDING`, `MERGING` ou `EMBEDDING`. Explicitar a contribuição
da integração, o ponto temporal/analítico e como serão examinados
resultados divergentes. **Plano de integração não equivale a integração
executada.** A liberação final requer referência ao artefato real
da integração.

**Design science:** diferenciar fundamentação do problema,
características do artefato, decisões de construção e avaliação
empírica/analítica efetivamente conduzida. Protótipo disponível não é
prova de utilidade ou de adoção.

**Teoria e revisões:** a lógica de seleção de literatura e o significado
de “síntese” dependem da família de estudo. Somente revisões que
efetivamente operam com elegibilidade/corpus passam por congelamento
bibliográfico. Identificação e leitura de fontes continuam
rastreáveis em todo trabalho quando utilizadas.

## 5. Os mesmos sete gates, funções adequadas ao desenho

`GATE-0001` pergunta e contribuição; `GATE-0002` escolha
metodológica e protocolo; `GATE-0003` estratégia relevante de
literatura/fundamentação; `GATE-0004` corpus **bibliográfico**
ou materiais/dados/artefato **empírico**; `GATE-0005` síntese,
análise real, integração ou avaliação conforme a rota;
`GATE-0006` integridade das afirmações e apreciação científica;
`GATE-0007` conformidade com a revista e arquivos de submissão.

Nenhum *gate* é considerado aprovado apenas por conclusão de tarefa
C.A.D.A., por um campo preenchido ou por decisão sintética da IA.
A cada aprovação de novo projeto, o *gate* anterior deve estar
devidamente decidido. Ações intermediárias podem ser autônomas, mas
escolhas científicas críticas continuam sob decisão humana.

Nos desenhos empíricos, `GATE-0004` exige registro de **materiais
efetivamente obtidos/construídos** e referência de onde verificá-los.
`GATE-0005` exige registro de **análise/avaliação executada** e sua
evidência original; métodos mistos ainda exigem evidência da integração.
Um estado declarado no perfil é um **registro** e não comprova, por si,
a execução científica: a auditoria das evidências permanece obrigatória.

Não marcar `NOT_APPLICABLE` para contornar planejamento, material,
análise e auditoria científica. Se o posicionamento bibliográfico
prévio realmente não for pertinente, a exceção requer autoria, prova
da decisão e justificativa substantiva. `GATE-0007` pode permanecer
pendente quando não houver intenção de submeter a uma revista.

## 6. Linhagem e limites da evidência

- [L] evidencia o que uma fonte ou conjunto de dados acessível realmente
  sustenta; [I] identifica interpretação delimitada; [P] explicita a
  proposição original. **A existência de um DOI ou de um arquivo não
  prova suporte semântico de uma afirmação.**
- Uma decisão `APPROVED` exige revisão humana real e referência.
  Conferências automatizadas validam **estrutura e integridade formal**,
  não qualidade teórica, adequação causal ou resultados de campo.
- Nenhum código pode inferir resultados quantitativos, depoimentos,
  análises qualitativas, avaliações de artefatos, aprovações éticas,
  participação de pessoas ou impacto do C.A.D.A.
- O Drive segue canônico quando conectado; arquivos locais são estágio
  autorizado, nunca autorização automática para sincronizar ou compartilhar
  pesquisa. Revisões textuais, anexos de periódicos e textos integrais
  respeitam as regras de direitos e confidencialidade.
