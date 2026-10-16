# Etapa 08 — Revisão de segurança F5–F9

Escopo exclusivo: testes e correções sintéticas na branch candidata da PR #78;
sem alteração no Google Drive, na VPS, na distribuição instalada ou na branch principal.

## Invariantes
- F5: um POST de criação é uma operação não idempotente. Qualquer exceção
  do executor, inclusive erro desconhecido depois de um efeito remoto,
  é ambígua e requer leitura nova; nunca repetir o POST cegamente.
- F5: o lock local deve conservar identidade do mesmo inode. Se outro
  ator substituir o arquivo, não reivindicar sucesso nem remover o lock alheio.
- F6: busca conectada e pastas existentes são evidências auxiliares somente
  leitura, nunca prova de ausência de conflitos entre tipos MIME.
- F7: recibos HMAC não são uma autoridade sem o head externo de confiança.
  Não reinicializar cadeia após perda do arquivo ou do estado.
- F8: CAS rejeitado, timeout ou readback inconsistente bloqueiam a criação.
  Não supor que a resposta do backend descreve o resultado de uma operação
  que possa ter sido aplicada.
- F9: o adaptador DynamoDB é opcional; exige tabela, item e permissões
  previamente provisionados pelo operador. Leitura consistente e
  ConditionExpression = comparação atômica de um head já existente.
  Respostas malformadas nunca são traduzidas em sucesso.

## Testes e limitações
Os testes em tests/test_drive_f5_f9_stage08.py usam fakes sem credenciais.
Eles cobrem concorrência simulada entre writers, perda de resposta após CAS
com efeito, retomada com journal pendente, replays de recibos assinados,
substituição de lock local, erros de I/O pós-criação e formatos inválidos AWS.
A implementação não prova linearizabilidade do serviço remoto em produção
nem elimina TOCTOU do filesystem entre lstat e unlink; a defesa cross-host
continua sendo F8/F9, mais segregação operacional e autorização humana.

A interface CLI F5 não disponibiliza backend CAS de produção e portanto
não pode habilitar writes. Uma configuração AWS real, uma leitura Drive com
credenciais delegadas e uma criação num ambiente de teste exigem decisão
explícita posterior e homologação em contexto isolado.
