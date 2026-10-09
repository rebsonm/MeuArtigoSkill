# Uso de textos completos, licenças e direitos de redistribuição

## Quatro permissões diferentes

1. **Descoberta bibliográfica:** um DOI, um registro Crossref/OpenAlex ou um link encontrado identifica uma publicação. NÃO determina licença ou permissão de download.
2. **Acesso local:** leitura via biblioteca institucional, CAPES/CAFe, repositório, editor ou arquivo recebido legitimamente. Acesso legítimo não concede automaticamente permissão para publicar o PDF.
3. **Análise científica:** examinar, fichar e citar trechos na medida cabível à autorização e às normas aplicáveis. Não carregar nem enviar PDFs completos para APIs externas sem autorização apropriada.
4. **Redistribuição externa:** colocar a cópia integral em ZIP, RO-Crate, site, repositório público ou arquivo compartilhável exige uma autorização compatível **para aquele arquivo específico**.

O código da Skill é público; isso NÃO faz os PDFs baixados pelo pesquisador serem públicos ou licenciados sob a mesma licença do código. Metadados, fichamentos e citações não transmitem automaticamente o direito de republicar o texto integral.

## Registros sem novas planilhas

O controle aproveita os registros com Record_ID do arquivo canônico
\`00_Gestao_e_Continuidade/04_FullText_Tracker.csv\` e a aba existente
\`08_FULL_TEXT\`. Foram acrescentadas nove colunas, preservando as anteriores:

- Access_basis — OPEN_ACCESS, INSTITUTIONAL_ACCESS, PERSONAL_AUTHORIZED, DIRECT_PERMISSION ou UNKNOWN;
- Rights_basis — UNKNOWN, ALL_RIGHTS_RESERVED, CC0_1_0, CC_BY_4_0, CC_BY_SA_4_0, PUBLIC_DOMAIN, DIRECT_PERMISSION, INSTITUTIONAL_ACCESS ou PERSONAL_ACCESS;
- License_URI — licença aplicável à versão exata, quando cabível;
- Rights_evidence — página da publicação com licença específica ou referência a autorização documental;
- Permission_scope — escopo preciso, inclusive PUBLIC_REDISTRIBUTION quando uma permissão individual autorizar;
- Attribution_text — crédito, licença e avisos necessários;
- Source_sha256 — SHA-256 do documento efetivamente armazenado;
- Rights_reviewed_by — atribuição da revisão documental a uma pessoa, NÃO autenticação independente;
- Rights_review_evidence — referência verificável à manifestação original de revisão.

Os documentos devem permanecer na área \`03_Screening_e_FullText/FullText_Corpus\`, vinculados à coluna existente \`File_or_URL\` por **caminho relativo ao workspace**. Links externos podem constar como referência de acesso, mas não autorizam empacotamento sem o arquivo verificado.

## Conduta operacional

Para registrar fonte, confirmar quem disponibilizou o arquivo, qual versão foi acessada e sua base de acesso. Buscar licença no site da própria publicação ou autorização específica de quem detém os direitos; o endereço genérico da licença Creative Commons **não demonstra que um artigo específico está sob aquela licença**. Salvar a referência a essa verificação no tracker, mantendo o arquivo de autorização fora de pacotes compartilháveis quando contiver informação pessoal.

**Para análise interna**: arquivos autorizados podem permanecer no corpus privado conforme os direitos efetivos de acesso. Em caso de acesso incerto, registrar UNKNOWN e não assumir que o acesso foi permitido. A falta de acesso ao texto integral deve permanecer \`PENDING ACCESS\`, não EXCLUDE.

**Para exportação externa**: o padrão de \`scripts/export_provenance.py\` continua **sem PDFs/textos integrais**. A opção \`--include-fulltext\` agora falha sem confirmação explícita e sem uma avaliação positiva, arquivo por arquivo, do hash, da licença/permissão, da fonte da evidência e da revisão humana.

Não se permite exportar pelo fluxo automatizado documentos com licença desconhecida, todos os direitos reservados, acesso pessoal ou institucional como única base. As licenças CC BY-NC e CC BY-ND não são tratadas como autorização geral de redistribuição pública porque trazem restrições contextuais; casos especiais exigem uma análise jurídica/humana e autorização específica. Para CC BY/CC BY-SA é preciso crédito e atender às condições aplicáveis. A verificação automatizada só garante consistência das anotações; não certifica a validade jurídica da licença, a existência do permissionário ou que todas as obrigações de compartilhamento igual foram cumpridas.

Páginas oficiais de apoio:
- CC BY 4.0: https://creativecommons.org/licenses/by/4.0/
- CC BY-SA 4.0: https://creativecommons.org/licenses/by-sa/4.0/
- Licenças CC no Brasil: https://br.creativecommons.net/licencas/

## Comandos gratuitos

Auditoria do tracker e do corpus (não publica arquivos):

\`\`\`bash
python scripts/rights_audit.py /caminho/do/projeto
python scripts/rights_audit.py /caminho/do/projeto --strict
python scripts/rights_audit.py /caminho/do/projeto --check-export
\`\`\`

Exportar somente a proveniência e os artefatos padrão sem PDFs brutos:

\`\`\`bash
python scripts/export_provenance.py /caminho/do/projeto
\`\`\`

Somente quando cada documento estiver comprovadamente autorizado para redistribuição ampla e o pesquisador de fato tiver examinado os documentos de direitos:

\`\`\`bash
python scripts/export_provenance.py /caminho/do/projeto \
  --include-fulltext --confirm-rights-review
\`\`\`

O exportador interrompe a operação **antes** de gravar o evento TRACE/EXPORT, criar ZIPs ou copiar fontes quando não houver documentação suficiente. Em exportações permitidas, inclui \`provenance/FULLTEXT_RIGHTS.json\` com as atribuições e os hashes dos documentos. O manifesto de direitos é uma atestação auditável, **não parecer jurídico, autorização nova nem licença concedida pela Skill**.

ZIPs e arquivos compactados aninhados são omitidos do pacote padrão: poderiam conter PDFs não identificados e contornar a análise de direitos. Arquivos de fonte com symlinks ou caminhos fora do corpus também são rejeitados.

## Transparência e privacidade

- Não armazenar senhas de CAFe, tokens de biblioteca, credenciais e cookies nos registros.
- Não burlar paywalls ou controles tecnológicos para obter conteúdo.
- Não enviar PDFs restritos a modelos, serviços de IA ou repositórios externos sem uma base jurídica e autorização compatíveis.
- Não incorporar longas passagens protegidas ao relatório público apenas para demonstrar rastreabilidade.
- Os campos de licença e revisão são anotações do pesquisador; um texto atribuído a um humano pode ser forjado e exige conferência.
- O registro de obras em domínio público depende de avaliação por jurisdição, prazo de proteção e versão do documento. Uma etiqueta PUBLIC_DOMAIN isolada não é prova jurídica.
- Os controles de anonimização e regras específicas de periódico continuam sendo obrigatórios e independentes.

**Escopo de segurança:** o controle é conservador, não substitui aconselhamento jurídico e pode bloquear uma distribuição que venha a ser legalmente permitida em certo contexto. Nessa hipótese, revisar os direitos e registrar uma autorização adequada; não remover o bloqueio ou marcar uma licença falsa para avançar.

Nos projetos antigos, novos campos permanecem em branco até revisão genuína. Não preencher retrospectivamente permissões que nunca foram concedidas. Nos novos projetos, \`fulltext_rights_audit_required=true\` liga avisos e inconsistências à validação canônica, e o exportador protege a redistribuição independentemente da configuração de projeto.
