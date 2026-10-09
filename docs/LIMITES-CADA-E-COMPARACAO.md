# RT-07 — Escopo do C.A.D.A. e protocolo de avaliação independente

## O que o C.A.D.A. faz e o que não faz

**C.A.D.A. = Capturar, Atribuir, Definir prazo e Acompanhar** demandas administrativas documentadas. Na Skill Meu Artigo ele é a camada de **governança operacional da execução**, não um novo método de revisão da literatura e nem uma demonstração de que a pesquisa será cientificamente mais correta.

| Camada | Mecanismos | Evidência cabível | O que NÃO comprova |
|---|---|---|---|
| C.A.D.A., 11_CADA_Control e 15_CADA_Dashboard | Responsável, prazo, dependência, próximo passo, status, baixa documentada | Registros de tarefa e artefatos de conclusão | Qualidade científica, cobertura de busca, revisão humana efetiva |
| Procedimento científico | Protocolo, buscas, deduplicação, screening, full text, análise e síntese | Search_ID, Record_ID, Evidence_ID, Claim_ID e documentos originais | Efeito causal do C.A.D.A. |
| Decisão e validação científica | DEC_ID, GATE_ID, juízos metodológicos e revisão humana | Manifestações originais e registro de decisão rastreável | Qualidade automaticamente certificada por ter ocorrido um gate |
| Execução e proveniência | TRACE, recibos e snapshots | Hashes e resultados efetivamente capturados | Que uma afirmação ou conclusão acadêmica é verdadeira |

Os objetos de gestão podem se relacionar a um registro científico, mas o vínculo NÃO transfere sua autoridade epistemológica. Uma tarefa **DONE** não promove fontes a verificadas, não aprova o protocolo e não substitui um GATE-0004/GATE-0006.

## Auditabilidade técnica agora

O script `scripts/audit_governance_boundary.py` não depende de aplicações pagas. Com Python 3.10+:

```bash
python scripts/audit_governance_boundary.py audit /projeto --strict
python scripts/audit_governance_boundary.py audit /projeto --strict --output 00_Gestao_e_Continuidade/GOVERNANCE_BOUNDARY_REPORT.json
python scripts/audit_governance_boundary.py check-plan benchmarks/cada_comparison_protocol_v1.json
```

O relatório separa **atividades de gestão**, **registros científicos** e **comprovantes técnicos**. Ele identifica tarefas marcadas DONE com evidência operacional vazia ou tautológica e gates com apenas “DONE”/“CADA-0001” como suposta prova científica. A verificação de origem/qualidade científica permanece nos scripts especializados dos RT-01, RT-04, RT-05 e RT-06; este controle NÃO os substitui.

O módulo retorna `scientific_quality_validated=false` e `causal_CADA_effect_established=false`. Tarefas concluídas, prazos registrados e eventos rastreados não são medidas válidas da qualidade acadêmica.

Projetos novos usam `cada_science_boundary_required=true`. Projetos anteriores só migram após decisão explícita: conservar seus registros e não inferir que uma anotação histórica é prova técnica.

## RT-07 comparativo: protocolo preparado, sem execução empírica

O arquivo `benchmarks/cada_comparison_protocol_v1.json` é o protocolo prospectivo para uma futura comparação **com C.A.D.A. / sem C.A.D.A.**, com aplicação a episódios administrativos de pesquisa que sejam comparáveis.

As duas condições devem manter **o mesmo objeto de pesquisa, corpus, protocolo de busca, critérios, decisões humanas críticas e padrões de validação científica**. A intervenção que varia é a camada de gestão e acompanhamento; a ausência de C.A.D.A. não significa dispensar os registros e controles científicos.

O protocolo contém:

- unidade: demanda administrativa documentada com responsável, providência e evidência de conclusão verificáveis;
- desenho: episódios pareados e alocação prospectiva, conforme a viabilidade; não atribuir causalidade a diferenças de conveniência;
- resultados administrativos: tempo até a primeira ação, tempo até a baixa, retrabalho documentado e percentual de prazos não atendidos;
- desfechos de segurança científica: aderência ao protocolo, erros de sustentação dos claims e qualidade da triagem avaliados **independentemente**;
- riscos: seleção de tarefas mais fáceis, diferença de ferramentas, aprendizado, contaminação de condições, trabalho adicional e perdas de registros;
- análise: definir estimando, critérios de exclusão, tratamento de dados faltantes, intervalos de incerteza e divergências antes do primeiro episódio.

O protocolo **não contém observações nem estimativas**. Nenhum experimento foi realizado e nenhuma vantagem de eficiência ou qualidade científica foi demonstrada. Os campos de resultados foram deixados nulos/vazios deliberadamente. Não inserir números fictícios para completar a matriz.

## Limitações

O teste automatizado verifica apenas registros, consistência estrutural e inadmissibilidade de certos atalhos; não autentica seres humanos, não observa diretamente a execução de tarefas externas e não mede benefício gerencial.

O C.A.D.A. pode, como hipótese a ser testada, reduzir atraso, retrabalho e assimetria informacional. A eficácia depende de pesquisa empírica com evidências próprias e desenho comparativo adequado. Até lá, descrever como **função proposta** ou **capacidade operacional do software**, nunca como efeito comprovado.

Os relatórios de gestão podem ser compartilhados separadamente dos resultados científicos para evitar que indicadores administrativos se convertam em prova indevida de rigor acadêmico. Não foram criadas abas, famílias de identificadores nem integrações pagas.
