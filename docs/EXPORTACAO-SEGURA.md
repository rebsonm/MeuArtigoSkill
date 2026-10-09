# Exportação segura de proveniência — separação por público

Este documento define três **perfis de distribuição**, implementados em `scripts/export_provenance.py`.
Nenhum perfil concede direitos para compartilhar material acadêmico protegido, manuscritos
confidenciais, dados pessoais ou conteúdo sujeito a embargo.

## 1. PRIVATE — auditoria interna (padrão)

```bash
python scripts/export_provenance.py /caminho/do/projeto --audience PRIVATE
```

Este perfil mantém o pacote integral de proveniência, registros internos, controles,
e arquivos canônicos elegíveis, conforme as regras de direitos para textos completos.
O pacote tem prefixo `RO_CRATE_PRIVATE_` e **não deve ser redistribuído**
sem avaliação separada. Seus dados podem incluir nomes, histórico de decisões,
citações, comentários, documentos sob revisão e identificadores pessoais.
O fato de um SHA-256 corresponder aos arquivos não significa ausência de dados sensíveis.

Para incluir textos completos na exportação **privada**, continuam exigidos
`--include-fulltext --confirm-rights-review` e os registros individuais de direitos,
conforme [direitos de arquivos completos](DIREITOS-FULLTEXT-E-PDFS.md).
**Nem esse mecanismo autentica juridicamente a permissão de redistribuição.**

## 2. PUBLIC — estrutura neutra, sem dados da pesquisa

```bash
python scripts/export_provenance.py /caminho/do/projeto --audience PUBLIC
```

Gera estrutura RO-Crate com descrição técnica e grafo PROV **deliberadamente
redigido**, sem nomes de projeto, registros, evidências, buscas, textos,
documentos, metadados de identificadores científicos ou corpus. Não aceita
inclusão de textos completos nem exceções por manifesto de arquivos.

**Limitação funcional explícita:** é um artefato de transparência sobre o
limite de exportação, **não uma reprodução pública auditável da pesquisa**.
Não se deve descrevê-lo como pacote integral ou evidência independente
da qualidade do manuscrito.

## 3. COLLABORATIVE — colaboração com arquivos especificamente autorizados

```bash
python scripts/export_provenance.py /caminho/do/projeto \
  --audience COLLABORATIVE \
  --approved-files-manifest aprovacao-colaboracao.json
```

Sem manifesto, o resultado também é apenas a estrutura neutra.
Com manifesto, só admite arquivos textuais `.md` e `.txt` dentro da
pasta canônica `05_Manuscrito/Versao_Canonica/`, cada um vinculado a um
SHA-256 exato, com revisão de conteúdo e autorização humana declaradas.

**Estrutura do manifesto, a ser preenchido com avaliação verdadeira:**

```json
{
  "schema_version": 1,
  "audience": "COLLABORATIVE",
  "reviewed_by": "Identificação real do revisor autorizado",
  "reviewed_at": "2026-10-09T17:00:00-03:00",
  "review_scope": "Descrever o que foi revisado: confidencialidade, autorização e público destinatário",
  "files": [
    {
      "path": "05_Manuscrito/Versao_Canonica/NOME_REAL_ARQUIVO.md",
      "sha256": "SUBSTITUIR_PELO_SHA256_REAL_DE_64_CARACTERES"
    }
  ]
}
```

O exemplo é **um modelo vazio**, não uma declaração de revisão realizada.
Os arquivos devem ser conferidos manualmente antes de criar o manifesto.
Alterações de bytes invalidam a aprovação anterior. Links simbólicos,
arquivos fora da pasta, arquivos binários, dados pessoais evidentes e
indicadores típicos de credenciais são recusados.

A verificação de padrões técnicos não detecta todas as formas de informação
confidencial, direitos morais, material inédito, trechos protegidos, dados
identificáveis indiretamente, figuras ou compromissos com periódicos. A
**responsabilidade por essa análise permanece humana**. Os campos
`reviewed_by`/`reviewed_at` são declarações, não prova de identidade.

## Limites comuns e consistência dos relatos

- Exportar é diferente de **publicar**. A permissão deve considerar finalidade
  e destinatários específicos.
- Modos externos nunca incluem o grafo PROV completo de eventos individuais,
  mesmo quando um manuscrito foi autorizado, para evitar reidentificação por
  cruzamento de IDs e campos auxiliares.
- O relatório inclui o perfil de público e avisa que exportações externas
  são reduzidas; não declarar cobertura total da pesquisa.
- Não colocar nomes, URLs privadas ou documentos sensíveis em Issues públicas,
  testes, pacotes de instalação ou notas de versões.
- Para interoperabilidade privada integral, use `PRIVATE` e distribuição
  restrita, com as verificações institucionais e editoriais pertinentes.

A escolha de licença do **código da Skill** (Apache-2.0) não modifica as
licenças, direitos e sigilo de **dados e obras usados no projeto científico**.
