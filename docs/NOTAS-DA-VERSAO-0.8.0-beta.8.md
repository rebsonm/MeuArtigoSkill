# Meu Artigo — versão beta 0.8.0-beta.8

Atualização da **etapa 1: segurança de exportação, atribuição e política de distribuição**.

## Alterações realizadas

- Adotada a **Apache License 2.0** integral para a distribuição da versão atual, com arquivo **NOTICE** atribuindo autoria a Rebson de Morais Mendes.
- Atualizados README, CITATION.cff, CONTRIBUITING, auditoria de release e empacotador para identificar **Apache-2.0** e preservar a atribuição no ZIP.
- Separação da exportação de proveniência nos públicos **PRIVATE** (auditoria interna completa, padrão), **PUBLIC** (apenas estrutura técnica redigida, sem registros da pesquisa) e **COLLABORATIVE** (estrutura redigida e, opcionalmente, textos de manuscrito revisados individualmente por humano e vinculados ao SHA-256).
- Bloqueio de textos completos nos pacotes externos e recusa de arquivos com caminhos indevidos, links simbólicos, bytes alterados após revisão ou padrões evidentes de credenciais/dados pessoais.
- Adicionados testes adversariais de regressão e guia de exportação segura.
- Corrigida referência residual indevida na política de segurança; a documentação corrente não deve revelar nomes de coleções de consulta privada.
- O histórico Git e as releases anteriores **não foram reescritos**; versões já distribuídas sob MIT conservam as respectivas permissões.

## Limitações e responsabilidades

A Apache-2.0 exige preservação dos avisos pertinentes da licença e NOTICE e indicação de modificações, **não exige citação acadêmica formal** como condição de uso. A citação sugerida em CITATION.cff é recomendada, não obrigatória pela licença. A licença de código não se aplica automaticamente a textos, PDFs e documentos científicos de terceiros.

Pacotes externos redigidos **não substituem** os registros privados completos nem demonstram validade científica da pesquisa. A declaração de revisão humana é verificável quanto aos arquivos e seus hashes, mas a identidade e a autorização do revisor **não são autenticadas pelo código**. Publicar ou compartilhar exige revisão jurídica, ética e editorial conforme cada caso.

A proteção obrigatória da branch principal depende de configuração administrativa do GitHub; não é afirmada como implementada por esta release. Avaliações empíricas de qualidade científica continuam pendentes.
