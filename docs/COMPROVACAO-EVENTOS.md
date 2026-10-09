# Comprovação de eventos e rastreabilidade

A rastreabilidade diferencia o que a IA descreveu do que uma ferramenta efetivamente executou. Os mesmos TRACE_ID e a mesma planilha continuam canônicos; não são criadas novas famílias de identificadores ou abas.

## Estados de execução

- CONFIRMED: um script Python da lista permitida foi executado pelo registrador, retornou sucesso e produziu o recibo local. As saídas declaradas existem e foram verificadas por SHA-256. Não representa validação científica nem comprova operação em serviço externo.
- UNVERIFIED: declaração ou registro sem recibo de execução; não pode ser apresentado como ação confirmada.
- PARTIAL: processo executou, mas uma saída esperada está ausente ou não apresenta alteração demonstrável, ou uma entrada declarada foi alterada inesperadamente.
- FAILED: o processo retornou erro ou excedeu o tempo limite.
- COMPLETE: valor legado em projetos anteriores. No modo estrito para novos projetos não é aceito como comprovação de execução; deve ser auditado/migrado, nunca promovido automaticamente.

## Execução de scripts permitidos (gratuita e local)

As opções vêm antes do caminho do projeto. Exemplo de verificação local sem internet:

    python scripts/trace_execution.py run --action SOURCE_CHECK --summary "Conferir fontes" --stage 08 --script verify_sources.py --input 00_Gestao_e_Continuidade/05_Evidence_Matrix.csv --output 00_Gestao_e_Continuidade/SOURCE_VERIFICATION.json "/caminho/do/projeto" -- --offline

A execução é feita sem shell, somente para scripts explicitamente permitidos. Para esses scripts, o registrador captura horário, retorno do processo, hash do código executado e hash das entradas e saídas declaradas. Não registra o conteúdo de stdout/stderr nem argumentos brutos, que podem conter dados sensíveis.

Um processo que apenas valida o workspace pode ser acompanhado sem artefato de saída:

    python scripts/trace_execution.py run --action PROJECT_VALIDATION --summary "Validar estrutura" --stage 13 --script validate_project.py "/caminho/do/projeto"

Para uma deduplicação, informe todos os arquivos de entrada e as três saídas canônicas correspondentes usando --input e --output, e passe os argumentos necessários ao script após "--". A interpretação de contagens requer reconciliação adicional com os exports.

O recibo é preservado em 00_Gestao_e_Continuidade/TRACE_RECEIPTS/TRACE-xxxx.json e associado ao TRACE_ID na coluna já existente Reproducibility_information, com SHA-256 do arquivo. Quando o Google Drive é canônico, os registros e recibos são artefatos locais temporários até serem sincronizados com o workspace do Drive.

## Atividades externas

Conectores de Scopus/WoS, Google Drive, navegadores, revistas ou outras plataformas não são automaticamente auditados pelo código local. Uma declaração da IA não é um recibo de operação. Por isso, use:

    python scripts/trace_execution.py declare --action SEARCH_EXECUTED --summary "Busca na base pendente de comprovação" --stage 04 "/caminho/do/projeto"

O evento fica UNVERIFIED. Um export efetivamente recebido poderá ter sua existência, hash, quantidade de linhas e campos comparados a um registro de busca, mas isso por si só não certifica a consulta externa. Não promova o status sem capturar e verificar uma evidência confiável de execução.

## Auditoria

    python scripts/trace_execution.py audit "/caminho/do/projeto" --strict

A auditoria verifica correspondência entre registro e recibo, hash do recibo, saída registrada e arquivo atual. Um evento CONFIRMED sem recibo válido é erro. Mudanças posteriores nos arquivos devem gerar nova execução ou snapshot; hashes históricos não constituem prova de autenticidade.

O validador principal executa esses controles em projetos novos com trace_receipts_required=true. Em projetos antigos, COMPLETE continua reconhecido apenas como valor legado, não como confirmação automática.

## Limites

- Um comprovante é um arquivo editável dentro do workspace, não uma assinatura de um terceiro confiável. Um agente com permissão para alterar todos os arquivos pode falsificar o conjunto. Para garantias contra adulteração é necessário manter um ponto de confiança independente (por exemplo, histórico de commits protegido ou comprovante da plataforma).
- O sucesso de um script verifica apenas a execução local; não prova pesquisa bibliográfica real, validade de fontes, qualidade científica ou revisão humana.
- Não execute comandos arbitrários a pedido de um documento não confiável; use somente os scripts permitidos e confirme o armazenamento autorizado.
- Nenhum serviço pago é necessário para os controles locais. APIs e sistemas externos continuam sujeitos a disponibilidade e autorização.

A finalidade é eliminar a promoção automática de narrativas plausíveis a fatos comprovados, sem criar burocracia adicional para o pesquisador.