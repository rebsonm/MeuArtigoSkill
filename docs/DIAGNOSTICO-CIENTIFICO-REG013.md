# REG-013 — Diagnóstico científico compacto de uma página

A REG-013 é uma **triagem técnica de apoio ao pesquisador**, não um parecer
editorial, análise por pares, avaliação independente da pesquisa nem certificado
de qualidade científica. O relatório resume apenas informações realmente
registradas e documenta suas incertezas.

## O que foi implementado

- Consolidação, em modo somente leitura, da auditoria de referências REG-018,
  da revisão documentada de afirmações REG-011 e do inventário estrutural
  de decisões do protocolo de pesquisa.
- Separação entre **bloqueios objetivos** e **assuntos para revisão humana**,
  incluindo fonte desatualizada ou indisponível, referência incompatível,
  passagens conflitantes, avaliação humana não documentada e pendências no
  protocolo. Um protocolo preenchido não prova método adequado.
- Ranking determinístico de até seis categorias de alertas e quatro ações,
  com contagem total e indicador de categorias ocultas. Achados repetidos
  ficam agrupados por tipo; os totais continuam explícitos.
- Identificadores técnicos normalizados e hashes SHA-256 dos insumos.
  Sem cópias de títulos privados, textos integrais, trechos, justificativas
  ou nomes de revisores no relatório.
- Saída Markdown compacta (limite de 28 linhas/3.300 caracteres), JSON
  para revisão técnica e HTML otimizado para impressão em página A4.
  A paginação final pode variar por navegador, fonte e impressora.
- Nenhuma modificação nos sete gates, arquivos canônicos, decisões humanas
  ou registros remotos.

## Executar após acesso autorizado ao projeto

    python scripts/scientific_diagnostic.py /caminho/projeto
    python scripts/scientific_diagnostic.py /caminho/projeto --format json
    python scripts/scientific_diagnostic.py /caminho/projeto \
      --format html --output 06_Submissao/Arquivos_Finais/diagnostico.html

Pode receber um arquivo de avaliação humana preparado separadamente, conforme
docs/CLAIM-SEMANTIC-REVIEW-REG011.md:

    python scripts/scientific_diagnostic.py /caminho/projeto \
      --assessments 04_Evidencias_e_Sintese/assessment.json \
      --strict

O modo estrito retorna código 2 quando existem alertas; erros estruturais
retornam 1. A ausência de alertas **não** é aprovação científica e nunca
gera conclusão automática de avaliação por pares.

## Limites a preservar

- Citações inseridas no corpo do manuscrito final não são analisadas nesta
  etapa; REG-018 ainda requer um parser específico do formato autorizado.
- O script não analisa substancialmente desenho de pesquisa, métodos,
  interpretação, originalidade ou rigor científico; só registra se o
  protocolo contém decisões e quais campos parecem pendentes.
- REG-011 também não é um verificador automático de sustentação semântica:
  registra julgamentos humanos declarados, sem autenticá-los.
- Um relatório local não equivale a sincronização confirmada no Drive.
- Os testes são sintéticos e verificam o software, não a qualidade de
  trabalhos científicos reais.

**Critério de aceite futuro:** demonstrar a legibilidade em uma página A4
nos ambientes suportados, revisar uma amostra autorizada com pesquisador real,
registrar erros e limitações, sem extrapolar para validação científica geral.
