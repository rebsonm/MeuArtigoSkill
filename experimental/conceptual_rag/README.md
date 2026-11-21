# Meu Artigo — RAG Conceitual no Google Drive (piloto experimental)

**Status:** prova de conceito local; não integrada ao ZIP oficial, não publicada, não homologada no ChatGPT e sem acesso automático ao Google Drive.

## Arquitetura

O Google Drive é o armazenamento **privado** da biblioteca, do Markdown convertido e dos índices persistentes. A extração e as consultas ocorrem localmente e apenas quando o host oferece execução de Python e acesso explícito aos arquivos. Google Drive não calcula embeddings nem garante consultas vetoriais. A pasta ser privada não impede escrita pelo proprietário; a Skill deve consumir os arquivos somente em leitura, por uma conexão com escopo de leitura quando disponível.

Estrutura recomendada:

- `01_Fontes_Originais`: PDFs licenciados/autorizações; originais preservados e não incluídos no repositório.
- `02_Biblioteca_MD`: um `.md` por obra e seu `.md.meta.json` de proveniência. **Conversão não aprova direito de uso ou qualidade.**
- `03_Indice_Conceitual`: dicionários/relacionamentos revisados por humanos; ainda não usados automaticamente por este MVP.
- `04_Indice_Semantico`: cópia versionada dos artefatos gerados localmente (`chunks.jsonl`, `lexical.sqlite3`, `vectors.f32` opcional, `manifest.json`).

A geração usa diretório de índice **novo e vazio** fora dos originais. Não substitua um índice anterior; cada versão deve ter seu próprio caminho. O índice contém trechos potencialmente protegidos — não compartilhar publicamente.

## PDF → MD: extração com proveniência de página

Instale PyMuPDF **somente no executor autorizado**, sem enviar PDFs a sites de terceiros:

```sh
python -m pip install pymupdf
python pdf_to_md.py /CAMINHO/obra.pdf /CAMINHO/02_Biblioteca_MD/obra.md \
  --source-id OBRA001 --title 'Título da obra'
```

Cada página recebe `<!-- source_page: N -->`. O conversor cria `obra.md.meta.json` com SHA256 do PDF e do MD, registra páginas problemáticas e define **`extraction_status=REVIEW_REQUIRED`** e **`rights_status=NOT_REVIEWED`**. PDFs escaneados sem texto necessitam OCR controlado e comparação com imagem; tabelas/figuras requerem inspeção manual. **Não apague o PDF original.**

Após revisão humana da integridade de texto, páginas, edição e permissões, atualizar o JSON de metadados de modo atribuível para `extraction_status=HUMAN_REVIEWED` e `rights_status=PRIVATE_AUTHORIZED` (ou `PUBLIC_DOMAIN` se realmente comprovado). Recalcular `md_sha256` caso o Markdown tenha sido corrigido. Esses rótulos são operacionais, não licença científica universal.

## Indexação e consulta

Sem modelo local, as consultas são **lexicais** (SQLite FTS5); o sistema nunca chama isso de busca vetorial:

```sh
python rag.py build --library /CAMINHO/02_Biblioteca_MD \
  --index /CAMINHO/04_Indice_Semantico/indice_v001
python rag.py query --index /CAMINHO/04_Indice_Semantico/indice_v001 \
  --text 'Qual a diferença entre revisão integrativa e sistemática?'
```

Para busca **híbrida de verdade**, forneça um modelo Sentence Transformers previamente instalado e armazenado **localmente**, após aprovar suas condições de uso e direitos, tanto na indexação quanto na consulta:

```sh
python -m pip install sentence-transformers
python rag.py build --library /CAMINHO/02_Biblioteca_MD \
  --index /CAMINHO/04_Indice_Semantico/indice_v002 --local-model /CAMINHO/MODELO_LOCAL
python rag.py query --index /CAMINHO/04_Indice_Semantico/indice_v002 \
  --text 'Pergunta metodológica' --local-model /CAMINHO/MODELO_LOCAL
```

O código exige `local_files_only=True` e não baixa modelos. Sem o encoder de consulta, o resultado é explicitamente `LEXICAL_ONLY`, mesmo havendo vetores no índice. A ordenação híbrida usa Reciprocal Rank Fusion; **similaridade não comprova sustentação semântica de claims**. Citações são apenas identificadores de obra, página e fragmento extraído, não aprovação acadêmica.

## Limites e critérios de aceite

1. Não ingerir PPGA - LIVROS, projetos privados ou PDFs protegidos automaticamente. O piloto deve começar com arquivos sintéticos ou fontes selecionadas com permissão.
2. Não montar biblioteca global pública ou indexar livros de terceiros no ZIP da Skill.
3. Não alterar os sete gates, rotas metodológicas, decisões do pesquisador ou armazenamento canônico dos artigos.
4. Conferir integridade, páginas, resumos e negativas por especialistas antes de qualificar como RAG metodológica homologada.
5. Avaliar 5–10 fontes heterogêneas, consultas literais e paráfrases, citações verificáveis, zero vazamento, paginação e custo de reindexação. O ambiente deve registrar quando `sentence-transformers`/modelo local não existe.
6. Validar Drive com operações autorizadas e recibos de leitura; esta prova de conceito não utiliza o conector.

**Versão/integração:** módulo experimental para *depois* de v1.0.0, sem modificar a RC #99/#100. `v1.1.0` é apenas hipótese de planejamento, não versão publicada.
