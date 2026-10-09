# Verificação de fontes e passagens

A verificação bibliográfica é separada da redação feita por IA. O script confere metadados de DOI em bases abertas e procura passagens somente em cópias locais legitimamente acessíveis. Não certifica a qualidade metodológica nem a interpretação semântica de claims.

## Custos e pré-requisitos
- Python 3.10+; as consultas externas usam apenas bibliotecas padrão.
- Crossref: API pública gratuita, sem conta e sem chave. Sujeita a limites de taxa.
- OpenAlex: consultas básicas gratuitas sem chave. Chave gratuita opcional em OPENALEX_API_KEY, útil em volumes maiores.
- PDFs: instalação opcional de biblioteca gratuita pypdf (pip install pypdf) ou pdftotext já disponível. TXT e Markdown funcionam sem bibliotecas extras.
- Nenhum PDF completo é transmitido a Crossref/OpenAlex. Sem código executável disponível, a Skill não pode afirmar que fez verificações determinísticas.

## Utilização
Com o workspace autorizado e a Evidence Matrix preenchida:

    python scripts/verify_sources.py "/caminho/do/projeto" --strict

Para conferir apenas locators locais, sem acesso às APIs:

    python scripts/verify_sources.py "/caminho/do/projeto" --offline

Opcionalmente, --mailto EMAIL ativa identificação no Crossref. O resultado é gravado em 00_Gestao_e_Continuidade/SOURCE_VERIFICATION.json. Quando o Google Drive é canônico, sincronize o relatório para lá; resultado local isolado não substitui o workspace.

O script vincula 05_Evidence_Matrix.csv, 04_FullText_Tracker.csv e 03_Screening.csv, usando Evidence_ID e Record_ID. Textos em arquivos locais podem ser declarados em FullText_path, Full_text_path, PDF_path, Source_path ou File_path, ou no File_or_URL do tracker. Arquivos remotos nunca são baixados automaticamente.

Para testar um locator, forneça uma passagem literal de pelo menos cinco palavras (25 caracteres), opcionalmente com p. N. Somente a indicação "p. 12" não comprova a ocorrência textual.

## Interpretação
- Metadados VERIFIED: pelo menos um provedor identifica o DOI e corrobora título, ano/autor quando informados, sem contradições detectadas. Não significa que o claim seja verdadeiro.
- MISMATCH, INVALID_DOI e NOT_FOUND exigem correção ou investigação. NOT_FOUND exige ausência expressa em ambos os serviços.
- NO_DOI: livros e documentos legítimos sem DOI não são excluídos automaticamente; exigem outro tipo de verificação.
- UNVERIFIED: provedor indisponível, dados insuficientes ou modo offline. Não é aprovação.
- MATCHED: passagem encontrada no texto extraído da cópia local. PASSAGE_NOT_FOUND e PAGE_MISMATCH exigem revisão do original e da extração.
- TEXT_UNAVAILABLE, REMOTE_NOT_DOWNLOADED e LOCATOR_NOT_CHECKABLE: pendências, não demonstração de fraude.
- retraction_alert/update_alert: exigem avaliação do aviso editorial e das consequências científicas; não determinam exclusão automática.
- claim_support_status permanece NOT_SEMANTICALLY_VERIFIED, inclusive quando DOI e locator coincidem. Cabe à revisão humana avaliar o suporte real ao argumento.

O relatório conserva os resultados e hashes, sem reproduzir textos longos protegidos. Não compartilhe arquivos com caminhos internos ou títulos sensíveis.

Antes de GATE-0006, confira o relatório atualizado e documente as verificações humanas necessárias. Em projetos com source_verification_required=true, o validador impede a aprovação com relatório ausente, desatualizado ou contendo divergências determinísticas. Pendências não devem ser tratadas como confirmações automáticas.