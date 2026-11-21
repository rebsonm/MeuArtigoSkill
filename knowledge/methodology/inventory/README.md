# Inventário do acervo metodológico — etapa de licença

**Estado (21/11/2026):** inventário concluído, redistribuição **não** autorizada em bloco.

- Origem: pasta temática de pesquisa indicada pelo proprietário (IDs do Google Drive deliberadamente excluídos deste repositório público).
- Escopo inspecionado: **70 pastas de primeiro nível + 5 subpastas**, totalizando **475 PDFs**.
- Volume informado pela metadata do Drive: **688.482.286 bytes** (aproximadamente **688,5 MB**, antes de qualquer deduplicação).
- Entre os 475 arquivos, existem **466 nomes de arquivo distintos**; nomes repetidos **não** comprovam conteúdo duplicado.
- Maior PDF cadastrado: aproximadamente 91,5 MB. Todos os arquivos encontrados possuem menos de 100 MB, mas isso não implica viabilidade/recomendação de versioná-los no Git.
- Publicações efetivamente incluídas na branch: consultar `../pdf_catalog.json`; só documentos com redistribuição individualmente verificada podem entrar em `../pdfs/`.

## Partes do inventário

1. [Parte 01 — primeiras 18 pastas](./drive-source-candidates-part-01.json) — 170 PDFs
2. [Parte 02 — próximas 18 pastas](./drive-source-candidates-part-02.json) — 100 PDFs
3. [Parte 03 — próximas 18 pastas](./drive-source-candidates-part-03.json) — 104 PDFs
4. [Parte 04 — 16 pastas finais](./drive-source-candidates-part-04.json) — 66 PDFs
5. [Parte 05 — 5 subpastas](./drive-source-candidates-part-05.json) — 35 PDFs

Cada entrada representa **metadados**, não o PDF. `rights_status: NOT_REVIEWED` marca ausência de atestado de redistribuição no inventário. A licença é comprovada em separado, por arquivo, no catálogo de PDFs publicados. Acesso por link público, DOI ou uso acadêmico pessoal **não** tornam automaticamente um arquivo redistribuível.

**Regra:** nunca publicar um PDF protegido no repositório público, em qualquer branch, Git LFS, Actions ou Release, sem evidência documental da licença. Não colocar IDs, URLs privados, tokens, dados pessoais de acesso ou cópias de livros protegidos nos metadados públicos. Links bibliográficos e sínteses autorais são permitidos nos termos aplicáveis.

Para um eventual repositório GitHub **privado e dedicado** (separado do código público), ainda será preciso comprovar que o armazenamento e o acesso pretendidos são autorizados. A Skill só poderá ler fontes privadas com autenticação legítima no host; não inserir credenciais no ZIP público. Sem isso, a consulta privada não pode ser anunciada como disponível.

**Estado funcional:** inventário completo ≠ corpus integral instalado ≠ recuperação vetorial homologada. A instalação da Skill deve continuar leve; índices e documentos permanecem fora do ZIP.
