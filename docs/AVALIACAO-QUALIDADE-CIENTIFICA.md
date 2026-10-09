# Benchmark de qualidade científica: calibração pública e comparação reproduzível

O benchmark distingue três níveis de evidência: **(1) fatos publicados conferíveis**, **(2) resultados efetivamente produzidos pela Skill** e **(3) julgamentos científicos independentes**. Eles não são intercambiáveis.

## Conjunto de referência congelado

Arquivo: \`benchmarks/public_review_reference_v1.json\`.

Ele contém exclusivamente fatos bibliográficos e totais de seleção identificados em artigos reais, com links para os respectivos editores e, quando disponível, um repositório institucional:

1. Madan, R.; Ashok, M. *AI adoption and diffusion in public administration: A systematic literature review and future research agenda*. Government Information Quarterly 40(1), article 101774, 2023, DOI [10.1016/j.giq.2022.101774](https://doi.org/10.1016/j.giq.2022.101774). Na seção de triagem: 221 resultados da busca, 27 adicionais, 166 após remoção de duplicatas, 117 examinados integralmente e 73 incluídos. As diferenças **248**, **82**, **49** e **44** são cálculos aritméticos a partir desses totais publicados, não registros observados separadamente.
2. Aarab, A.; El Marzouki, A.; Boubker, O.; El Moutaqi, B. *Integrating AI in Public Governance: A Systematic Review*. Digital 5(4), 59, 2025, DOI [10.3390/digital5040059](https://doi.org/10.3390/digital5040059). Inclui 67 estudos. Outros números de etapas não são preenchidos se ausentes no conjunto congelado.
3. Goulart, J. de M.; Picalho, A. C.; Colombo, J. E. M.; Melo, P. A.; Fadel, L. M. *Processos de Governança em Inteligência artificial em Órgãos Públicos Brasileiros: revisão integrativa*. IJKEM, 2025, DOI [10.5007/2316-6517.2025.e109331](https://doi.org/10.5007/2316-6517.2025.e109331). O resumo do periódico informa **400 documentos recuperados**, **13 incluídos** (6 dissertações, 2 teses e 5 artigos), e cinco eixos temáticos. Etapas intermediárias não são inventadas. É a referência mais direta para uma futura replicação de **revisão integrativa**, que exigirá acesso à lista completa dos estudos e aos critérios de análise.
4. Page, M. J., et al. *The PRISMA 2020 statement*. BMJ 372:n71, 2021, DOI [10.1136/bmj.n71](https://doi.org/10.1136/bmj.n71). É uma diretriz de reporte; **não** é uma revisão a reproduzir. Participa apenas da calibração dos metadados.

Este é um conjunto pequeno, intencional e público. Não constitui amostra probabilística de periódicos, gabarito definitivo de categorias ou validação externa da qualidade da Skill.

## Reprodução prospectiva de uma revisão integrativa

Além do conjunto atual, há um [caso de reprodução integrativa preparado](REPRODUCAO-REVISAO-INTEGRATIVA.md), com protocolo em `benchmarks/integrative_replication_protocol_v1.json`. O caso é o artigo real de Straub et al. (2023), sobre conceitos e um framework de IA no governo. **Nenhum resultado da reprodução foi produzido**. A divergência entre os totais de conceitos/termos informados no resumo e nos destaques precisa de conferência antes da comparação.

## Como executar sem aplicativos pagos

Apenas Python 3.10+ e biblioteca padrão. O verificador de metadados utiliza os endpoints públicos do Crossref e OpenAlex já adotados pela Skill. Não exige chave paga; uma chave gratuita do OpenAlex é opcional para limites de consulta maiores.

### 1. Verificar os metadados reais

\`\`\`bash
python scripts/quality_benchmark.py pilot --output benchmark_pilot.json
\`\`\`

O comando realiza consultas **reais**, identifica inconclusões, contradições e alertas conhecidos. Nunca informa resultado verificado quando os serviços estão inacessíveis. Para validar a estrutura sem usar rede:

\`\`\`bash
python scripts/quality_benchmark.py pilot --offline --output benchmark_offline.json
\`\`\`

O resultado do \`pilot\` é apenas calibração de bibliografia externa, **não é avaliação de texto acadêmico gerado por IA**.

### 2. Comparar um resultado real da Skill

Execute o mesmo roteiro de trabalho científico, com critérios congelados, no modo-base e no modo-atualizado, preservando os resultados obtidos **realmente**. Prepare cada saída no formato de observações:

\`\`\`json
{
  "schema_version": 1,
  "cases": [
    {
      "case": "ai_diffusion_review",
      "doi": "10.1016/j.giq.2022.101774",
      "title": "AI adoption and diffusion in public administration: A systematic literature review and future research agenda",
      "stage_counts": {},
      "locators": []
    }
  ],
  "claims": []
}
\`\`\`

O exemplo mostra **apenas a estrutura e os metadados publicados**, não resultados fictícios da Skill. Os campos de \`stage_counts\`, \`locators\` e \`claims\` devem ser preenchidos somente após a execução real; não copie contagens do conjunto de referência para fingir que a Skill as reproduziu.

Avalie:

\`\`\`bash
python scripts/quality_benchmark.py evaluate \
  --candidate /caminho/resultado_observado.json \
  --workspace /caminho/do/projeto \
  --output /caminho/relatorio_qualidade.json
\`\`\`

Para comparação antes/depois, acrescente \`--baseline /caminho/baseline_observado.json\`. Sem observação para uma dimensão, a métrica é **null / não avaliada**, nunca 100%. Diferenças de versões só são interpretáveis com a mesma tarefa, fonte, período, critérios e denominadores.

## Dimensões e limitações das métricas

| Dimensão | Quando é mensurável | Limitação |
| --- | --- | --- |
| Identidade bibliográfica | Quando o trabalho informa DOI ou título comparável a uma referência congelada | Não mede se novas citações desconhecidas foram inventadas; uma auditoria mais ampla exige checar **todas** as referências geradas |
| Contagens/fluxos | Quando a execução apresenta seus próprios números | Precisão descritiva sobre os números publicados não reproduz a busca histórica nem decisões individuais |
| Localizadores | Quando o projeto dispõe do texto de origem legalmente acessível | MATCHED significa presença textual; não garante suporte semântico nem qualidade do estudo |
| Claims científicos | **Somente** com julgamentos fundamentados, externos às predições e entregues separadamente | Um campo JSON de "revisor" não autentica independência; discordâncias devem ser adjudicadas |
| Categorias teóricas | Quando existe uma rubrica e comparação independente contextualizada | Categorias novas justificadas não devem ser penalizadas apenas por diferirem da publicação-base |
| Tempo/retrabalho/usabilidade | Em desenho de avaliação próprio, com protocolo e métricas operacionais | Não corresponde à validade científica do manuscrito |

## Julgamento independente

O arquivo opcional de anotações requer \`schema_version: 1\`, \`reviewer_reference\` com a referência documental à avaliação real, e \`claims\` com \`claim_id\` e \`label\` (SUPPORTED, NOT_SUPPORTED ou UNCERTAIN). Ele é informado por \`--adjudications\`.

**Não** gere esse arquivo com as próprias respostas que serão avaliadas e não faça a IA declarar uma revisão "cega" inexistente. Um avaliador deve consultar as evidências diretamente e justificar divergências. Respeite o enquadramento ético aplicável caso a avaliação envolva participantes humanos.

## Protocolo de decisão

1. Congelar corpus, data, método, critérios e versão da Skill.
2. Executar roteiro-base e guardar saída bruta, hashes e eventuais indisponibilidades.
3. Executar versão alterada nas mesmas condições, de preferência com ordem contrabalanceada e informação de modelo/ferramentas documentada.
4. Auditar toda referência adicionada e checar fontes/locators originais.
5. Obter revisão independente dos claims e das categorias, sem aceitar o próprio modelo como gabarito.
6. Publicar cobertura, denominadores, erros, discordâncias e limites; não converter um piloto pequeno em "qualidade científica validada".

Os testes em \`tests/test_quality_benchmark.py\` usam mutações controladas e arquivos descartáveis para verificar o **software**; não são apresentados como dados de pesquisa. O piloto que utiliza APIs reais tem execução separada e relatório com as respostas efetivamente observadas.

Este conjunto inicial não substitui uma replicação completa de uma revisão integrativa publicada. Tal replicação requer acesso aos registros exportados, decisões de seleção, corpus e categorização primária, que não devem ser inventados ou extraídos apenas do resumo do artigo.
