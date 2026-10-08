# Anonimização de arquivos

O Meu Artigo adota anonimização por padrão para arquivos externos quando a identidade dos autores não é necessária.

A regra é simples:

`arquivo interno identificado -> derivado externo anonimizado -> auditoria -> revisão humana -> envio`

## O que é verificado

Antes de compartilhar ou submeter um arquivo para avaliação cega, a Skill deve verificar conteúdo visível e informações escondidas, incluindo:

- nomes de autores e coautores;
- afiliações, departamentos e instituições;
- e-mails, ORCID, telefone e outros identificadores;
- agradecimentos, financiamento e contribuições autorais que revelem autoria;
- nomes de organizações, participantes ou locais quando a confidencialidade exigir;
- comentários e controle de alterações;
- autor/criador e "última modificação por" nas propriedades do arquivo;
- caminhos locais do computador;
- links privados;
- nomes dos próprios arquivos;
- notas, planilhas ocultas e metadados de imagens/PDF quando aplicável.

A Skill não deve considerar um documento anônimo apenas porque o nome não aparece na primeira página. Em arquivos `EXTERNAL_ANONYMIZED`, o padrão é `ZERO_NONESSENTIAL_METADATA`: não pode permanecer identificação do software ou processo de geração. Campos como Author, Creator, Producer, Generator, Application, Company, criação/modificação, XMP, EXIF, IPTC e equivalentes devem ser removidos quando não forem tecnicamente necessários para renderizar o arquivo. Assim, “gerado com Python”, `pypdf`, ReportLab, Matplotlib, LibreOffice ou outro gerador também é tratado como vazamento de metadados.

## Perfil confidencial

Cada projeto possui um arquivo interno:

`00_Gestao_e_Continuidade/ANONYMIZATION_PROFILE.json`

Ele registra os termos que precisam ser procurados antes de uma liberação externa. Esse arquivo é confidencial e não entra nos pacotes enviados a revista, avaliador ou terceiro.

## Arquivos internos e externos

Arquivos internos podem manter autoria quando isso for necessário para gestão do projeto.

Para circulação externa, a regra padrão é `EXTERNAL_ANONYMIZED`.

Arquivos identificados, como folha de rosto, declaração de autoria, ORCID ou formulário do periódico, são gerados separadamente quando exigidos.

## Auto-citação

A Skill não remove automaticamente auto-citações. A política da revista deve ser seguida para evitar que a anonimização prejudique a integridade das referências.

## Sanitização e auditoria

A sequência para arquivos anonimizados é:

`python scripts/sanitize_metadata.py <arquivos> --in-place`

seguido de:

`python scripts/audit_anonymization.py <projeto> <arquivos>`

O sanitizador remove propriedades descritivas/proveniência e normaliza metadados de pacote quando isso pode ser feito sem alterar o conteúdo científico. Se um formato não puder ser limpo com segurança, ele falha e o arquivo permanece bloqueado. Comentários ou revisões que possam alterar o conteúdo não são aceitos/rejeitados silenciosamente.

O auditor analisa os arquivos efetivamente destinados ao compartilhamento e gera relatório em:

`06_Submissao/Anonimizacao/`

O GATE-0007 de liberação para submissão não deve ser aprovado enquanto houver achado de alto risco ou revisão necessária não resolvida.

A especificação completa está em [references/anonymization.md](../references/anonymization.md).
