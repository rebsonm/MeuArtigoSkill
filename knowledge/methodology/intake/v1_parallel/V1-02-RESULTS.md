# V1-02/20 — RESULTADOS E RECIBOS BIBLIOGRÁFICOS
**Estado:** ENTREGUE_PARA_AUDITORIA (curadoria documental, não aceite científico)  
**Data:** 21/11/2026, America/Fortaleza  
**Branch exclusiva:** `work/v1-02-20261121`  
**Manifesto fixo:** `7c92045310eb3b1474a9612a777fb0012a511592`  
**Snapshot atribuído:** `c5e0ca9abd98f824f1576c3ad94c6e9a5d18e9bf`  
**Escopo:** apenas SRC-0263, SRC-0283, SRC-0293, SRC-0297 e SRC-0314. Sem dependências prévias.  
**Limites:** sem alterações às fichas IB antigas, registry/catalog/rights-ledger, branches alheias, publicação, merge, licença ou gate.

## Método de conferência
Inspeção delimitada dos cinco PDFs específicos mantidos no Drive privado (primeira página, estrutura, impressos de paginação, metadados técnicos, sinais de direitos) e cotejo com as fichas IB originais das branches atribuídas. Pesquisa pública limitada aos mesmos cinco trabalhos (página de editora ou repositório, não literatura adicional). A criação/modificação técnica dos PDFs não é data de edição. Apenas hashes SHA-256 das cópias constam abaixo, sem IDs privados. As citações externas não provam igualdade binária da versão armazenada com o arquivo público. Sem revisão integral, parecer jurídico ou revalidação científica humana.

## Recibos por ID
### SRC-0263 — Políticas Públicas: Conceitos, Tipologias e Sub-Áreas
**Origem da ficha:** `work/ib-09-20261121` / `knowledge/methodology/source_cards/src-0263.md` (Git blob `7830a37c38a06203d434fa29bedf59ac8e68df1d`).  
**Cópia inspecionada:** `celina2.pdf` (29 páginas, 193799 bytes); SHA-256 `d2722e7fdcefcde1ef7b460c5fe4494221ad96e84066f261df598d44bd499172`.  
**Situação documental:** `IDENTIDADE_DA_OBRA_CONFIRMADA_COM_RESSALVA_DE_DIREITOS`. **Classificação científica:** [P] / `FICHA_DE_PROSPECCAO_NAO_REVISADA`; validação independente PENDENTE.

**Evidência:**
- Primeira página e nota do exemplar privado atestam autoria/título e 'trabalho elaborado ... em dezembro de 2002'
- PDF privado tem 29 páginas; PDF creationDate técnico 2006 não é o ano bibliográfico

**Patch-intent para integração posterior (não altera a ficha IB):**
```json
{
  "author": "Celina Souza",
  "work_date": "2002-12",
  "publication_form": "trabalho elaborado para a Fundação Luís Eduardo Magalhães",
  "identifier": "sem DOI/ISBN confirmado"
}
```
**Fontes públicas específicas da mesma obra:** <https://biblioteca.unisced.edu.mz/bitstream/123456789/3145/1/001-%20A-%20POLITICAS%20PUBLICAS.pdf>.  
**Direitos da cópia:** Nenhuma licença expressa observada na cópia particular; autor e entidade de destino não implicam licença; não redistribuir.  
**Pendências e bloqueios:** Determinar autorização de reprodução da edição exata se futuramente pretendida | Revisão científica independente permanece pendente.

### SRC-0283 — Getting Practical with Causal Mechanisms: The Application of Process-Tracing Under Real-World Evaluation Constraints
**Origem da ficha:** `work/ib-10-20261121` / `knowledge/methodology/source_cards/src-0283.md` (Git blob `40eb5ade4f0deb770e68d33979f200b79a33a4c8`).  
**Cópia inspecionada:** `Raimondo,2020.pdf` (17 páginas, 302386 bytes); SHA-256 `3758943249b2bce132828214435049cdc8f2fe95012dd422b4abf880799e29e5`.  
**Situação documental:** `OBRA_PUBLICADA_IDENTIFICADA_VERSAO_DA_COPIA_PENDENTE`. **Classificação científica:** [P] / `FICHA_DE_PROSPECCAO_NAO_REVISADA`; validação independente PENDENTE.

**Evidência:**
- Cópia privada: 17 páginas, capa de manuscrito de autora afiliada ao Independent Evaluation Group, sem folha de publicação
- Página da editora Wiley: título e autoria exatos, DOI 10.1002/ev.20430, edição Fall 2020, n. 167, pp. 45–58

**Patch-intent para integração posterior (não altera a ficha IB):**
```json
{
  "author": "Estelle Raimondo",
  "publication_year": 2020,
  "venue": "New Directions for Evaluation, v. 2020, n. 167, p. 45-58",
  "doi": "10.1002/ev.20430",
  "copy_version": "manuscrito/versão privada não comprovada como PDF editorial"
}
```
**Fontes públicas específicas da mesma obra:** <https://onlinelibrary.wiley.com/doi/abs/10.1002/ev.20430>.  
**Direitos da cópia:** Sem licença expressa no manuscrito; publicação comercial Wiley não presume autorização para redistribuir versão privada.  
**Pendências e bloqueios:** Confirmar correspondência de versão exata do manuscrito privado com a versão publicada | Examinar política de direitos do manuscrito antes de qualquer distribuição | Revisão científica independente pendente.

### SRC-0293 — Qualitative Comparative Analysis (QCA): usos e aplicações do método
**Origem da ficha:** `work/ib-10-20261121` / `knowledge/methodology/source_cards/src-0293.md` (Git blob `f93c6ef067d7394a81468f9f4468b90a20047d0a`).  
**Cópia inspecionada:** `Sandes-Freitas e Bizarro-Neto (2016).pdf` (16 páginas, 645133 bytes); SHA-256 `d8911bf8900e36117502c7601dd18e5283d4355d23f9ebebe9239c6879646e9e`.  
**Situação documental:** `REFERENCIA_DE_PERIODICO_IDENTIFICADA_LICENCA_PENDENTE`. **Classificação científica:** [P] / `FICHA_DE_PROSPECCAO_NAO_REVISADA`; validação independente PENDENTE.

**Evidência:**
- Cópia privada: título/autores, cabeçalho do volume 24, 2ª edição e paginação impressa 103–117, 16 páginas do PDF
- PDF hospedado no domínio oficial UFPE exibe os mesmos dados de autoria e paginação
- Fontes institucionais externas atribuem v.24, n.2 a 2015; não usar 2016 do nome ou metadado PDF como ano editorial

**Patch-intent para integração posterior (não altera a ficha IB):**
```json
{
  "authors": [
    "Vítor Sandes Freitas",
    "Fernando Bizzarro Neto"
  ],
  "year": 2015,
  "venue": "Revista Política Hoje, v. 24, n. 2, p. 103-117",
  "copy_pdf_creation_year": 2016,
  "warning": "ano de criação técnica do PDF não é data da edição; diferenças bibliográficas de paginação 103–117 vs 103–118 em referências secundárias"
}
```
**Fontes públicas específicas da mesma obra:** <https://periodicos.ufpe.br/revistas/politicahoje/article/download/3722/3024/8174> ; <https://sigaa.ufpi.br/sigaa/public/docente/turma.jsf?tid=330857>.  
**Direitos da cópia:** Nenhuma licença específica de redistribuição observada no PDF privado; política de direitos da edição requer checagem, sem republicação da cópia.  
**Pendências e bloqueios:** Se exigir confirmação editorial estrita, obter metadado oficial explícito do fascículo 24(2) de 2015 e resolver divergência de referência 103–117/103–118 | Revisão científica independente pendente.

### SRC-0297 — Qualitative Comparative Analysis (QCA): Aula 1 — Introdução ao método
**Origem da ficha:** `work/ib-11-20261121` / `knowledge/methodology/source_cards/src-0297.md` (Git blob `d2a3b1be22823d84aa89b721f8aed04de939cb81`).  
**Cópia inspecionada:** `QCA Aula 1 - Introdução ao método (MQ2023).pdf` (56 páginas, 2677663 bytes); SHA-256 `543ea9335fa77a47a3dcf79a0b621756e0a0975406501a592034609a0b13cb5a`.  
**Situação documental:** `BLOQUEADA_DATA_EDICAO_NAO_CONFIRMADA`. **Classificação científica:** [P] / `FICHA_DE_PROSPECCAO_NAO_REVISADA`; validação independente PENDENTE.

**Evidência:**
- Cópia privada: 56 slides, capa com título/autores/DCP–UFMG sem ano de edição
- PDF creationDate técnico 2023-11-13 e 'MQ2023' em filename não bastam para autenticar data da aula
- Página de curso posterior com docentes homônimos não autentica a versão específica do arquivo privado

**Patch-intent para integração posterior (não altera a ficha IB):**
```json
{
  "authors": [
    "Manoel Leonardo Santos",
    "Breno Marisguia"
  ],
  "institution": "DCP/UFMG",
  "kind": "slides de aula",
  "year": null,
  "edition": null
}
```
**Fontes públicas específicas da mesma obra:** <https://ufmg-mq2.com.br/analise-qualitativa-comparativa-qca/>.  
**Direitos da cópia:** Sem autorização de uso/reprodução expressa nos slides; elementos e figuras atribuídos a terceiros; não redistribuir.  
**Pendências e bloqueios:** Obter folha de rosto/expediente oficial ou confirmação documental dos autores sobre data/edição | Checar direitos dos componentes de terceiros | Revisão científica independente pendente.

### SRC-0314 — Controle sintético como ferramenta para avaliação de políticas públicas
**Origem da ficha:** `work/ib-11-20261121` / `knowledge/methodology/source_cards/src-0314.md` (Git blob `81f60d8c4db271d976c2d43251a3babde3d25e47`).  
**Cópia inspecionada:** `Ellery, Nascimento e Sachsida (ano).pdf` (24 páginas, 833574 bytes); SHA-256 `89479bf84fe37101dcfaf906b3275ad1561a327baa9c6f1ab6d583b673329c40`.  
**Situação documental:** `REFERENCIA_CAPITULO_IDENTIFICADA_DIREITOS_CONDICIONADOS`. **Classificação científica:** [P] / `FICHA_DE_PROSPECCAO_NAO_REVISADA`; validação independente PENDENTE.

**Evidência:**
- Cópia privada: 24 páginas com título/autores, capítulo 12 e paginação impressa 375–397
- Registro oficial da Biblioteca Digital do BNDES: obra, autores, IPEA, 2018 e pp. 375–397; arquivo público oficial anunciado como 814,04 KiB, similar ao arquivo privado 833574 B, porém igualdade de hashes não verificada

**Patch-intent para integração posterior (não altera a ficha IB):**
```json
{
  "authors": [
    "Roberto de Goes Ellery Junior",
    "Antônio Nascimento Júnior",
    "Adolfo Sachsida"
  ],
  "year": 2018,
  "kind": "capítulo 12",
  "book": "Políticas públicas: avaliando mais de meio trilhão de reais em gastos públicos",
  "editor": "Adolfo Sachsida (org.)",
  "publisher": "IPEA, Brasília",
  "pages": "375-397"
}
```
**Fontes públicas específicas da mesma obra:** <https://web.bndes.gov.br/bib/jspui/handle/1408/27227>.  
**Direitos da cópia:** O registro oficial BNDES informa reprodução do texto/dados com citação para usos não comerciais; tal nota não autoriza automaticamente redistribuir esta cópia privada nem materiais/figuras de terceiros. Não republicar PDF.  
**Pendências e bloqueios:** Se houver intenção de redistribuir, comprovar correspondência da edição exata, escopo do aviso e direitos de terceiros | Revisão científica independente pendente.


## Aceite técnico do pacote e limites
- [x] Cinco PDFs atribuídos inspecionados; cinco recibos com proveniência, hash, situação, correções propostas e direitos.
- [x] Nenhum ano ou edição inferido exclusivamente de filename, creationDate ou nome da pasta; divergências documentadas.
- [x] Sem PDF, trecho extenso ou ID privado no GitHub. Escopo de escrita apenas nos dois artefatos V1-02.
- [x] Nenhuma ficha IB anterior, catálogo global, registry, direitos-raw, manifesto ou outra etapa modificada.
- [ ] Identidade editorial residual SRC-0297 não resolvida; SRC-0283 versão exata não equiparada ao PDF editorial; política de direitos ainda pendente em vários itens.
- [ ] Revisão científica/editorial independente e decisão humana sobre direitos permanecem pendentes.
- [ ] Integração V1-16 só após todas as 15 etapas A auditadas e pré-requisitos satisfeitos.
- **Quarentena de SRC-0385:** pertence à V1-03 e foi preservada, não auditada nem liberada aqui.
- **Testes esperados:** sintaxe JSON, cinco IDs únicos, caminhos exclusivos, ausência de PDFs/IDs privados, leitura pós-commit no branch.  
- **Disposição:** `ENTREGUE_PARA_AUDITORIA`; não alterar contadores globais de 475 fontes/15 bloqueios neste lote isolado.

## Verificações executadas após a gravação GitHub

- PASSOU: JSON do DELTA analisado com parser, com cinco objetos e cinco `source_id` únicos correspondentes ao manifesto.
- PASSOU: hashes SHA-256 das cinco cópias privadas são hexadecimais com 64 caracteres; as cópias não foram incluídas no repositório.
- PASSOU: cada recibo registra direitos observados e pendências; `independent_scientific_approval=false` permanece explícito.
- PASSOU: comparação GitHub contra o commit fixo `7c92045310eb3b1474a9612a777fb0012a511592` apresentou **apenas** os dois caminhos exclusivos da V1-02 (`RESULTS.md` e `DELTA.json`), sem modificações de fichas IB, catálogo, manifesto ou outros lotes.
- PASSOU: ausência de links contendo IDs privados de PDFs do Drive nos próprios recibos; checagem textual de caminhos PDF não incluídos no diff.
- PENDENTE: revisão científica independente, licenças de cada cópia, resolução da data/edição SRC-0297, versionamento exato SRC-0283, integração global, testes de consulta e homologação de host. Esses testes não fazem parte do aceite científico desta etapa.
- Commits de criação dos recibos: `21e74038523903d0e4b0c5bbdd7b0158bf5fe076` (RESULTS), `557fca3e38e1e8b7e770f8e932583f65280a299b` (DELTA).
