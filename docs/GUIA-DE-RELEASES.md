# Publicação e versionamento — manutenção segura

Este guia se destina aos mantenedores da Skill. O código e a documentação
continuam abertos em Apache-2.0, com atribuição preservada em `NOTICE`.
Publicar uma release **não valida cientificamente** resultados ou alegações
de efetividade metodológica.

## Duas rotinas, responsabilidades separadas

1. **Release audit** (`.github/workflows/release-audit.yml`) executa-se
   para cada Pull Request e push na branch padrão. Preserva o job `audit`,
   exigido pela proteção da `main`. Verifica código, documentação, regras de
   privacidade, proveniência e integridade do ZIP. Opera com permissões
   `contents: read` e **não pode publicar** uma release.
2. **Publish beta (manual)** (`.github/workflows/publish-beta.yml`) só é
   iniciado em **Actions → Publish beta (manual) → Run workflow**, selecionando
   a `main`, e informando **`publish-beta`** no campo de confirmação.
   Sua ação com permissão `contents: write` só ocorre nesse job, após
   reexecutar todos os testes. Rejeita tags/releases existentes em vez de
   sobrescrever versões já distribuídas.

## Preparar uma versão nova

1. Crie uma branch de desenvolvimento e descreva as alterações realmente
   implementadas e verificadas no CHANGELOG (`Unreleased`).
2. Escreva as notas de versão verdadeiras em
   `docs/NOTAS-DA-VERSAO-<nova-versão>.md`, identificando a versão no texto.
   Não invente participantes de pesquisa, indicadores, corpus ou resultados.
3. Atualize **somente a fonte canônica** `VERSION`, por exemplo de
   `0.8.0-beta.8` para a próxima versão decidida, após as notas existirem.
4. Sincronize automaticamente o README, o CITATION e a seção do CHANGELOG:

   ```bash
   python scripts/sync_version.py --date AAAA-MM-DD
   ```

   Substitua `AAAA-MM-DD` pela data verdadeira da nova publicação. O script
   recusa ausência de notas, versão inválida ou metadados com estrutura
   inesperada. Ele **não cria publicação nem inventa resumo acadêmico**.

5. Execute antes da PR:

   ```bash
   python scripts/release_audit.py
   python -m unittest discover -s tests -v
   python scripts/check_documentation_links.py
   python scripts/audit_public_docs.py
   python scripts/smoke_test_provenance.py
   python scripts/build_skill_bundle.py
   ```

6. Abra a Pull Request e confirme que **`audit` está verde**, sem depender
   de aprovações fictícias. Integre à `main`.
7. Para **publicar** uma versão nova, acione manualmente o workflow de release
   na `main` e informe `publish-beta`. Confira o link de release e os
   arquivos `MeuArtigoSkill-v<versão>.zip` e `SHA256SUMS.txt`.

**Importante:** mudanças técnicas na `main` não tornam automaticamente
uma nova release pública. A versão `0.8.0-beta.8` permanece a última
release declarada até uma publicação posterior, com novo identificador.
Versões anteriores continuam disponíveis sob as respectivas licenças
concedidas à época.

## Política técnica

- Actions externas têm versões fixadas por commit SHA obtido dos projetos
  oficiais. Para atualizar, revisar dependências e a mudança antes de
  substituir o SHA, e executar os testes.
- O CI tem permissões de leitura. O job de publicação manual tem a permissão
  mínima adicional de escrita para criar uma nova release. Credenciais do
  checkout não ficam persistidas.
- Testes de documentação percorrem materiais públicos, inclusive arquivos
  Markdown na raiz e em `.github`, verificando vestígios internos e padrões
  de segredos com alta precisão. Isso **não garante** a ausência total de
  informação sensível e **não apaga** material já presente no histórico.
- Conteúdo de pesquisa e textos completos permanecem sujeitos às condições
  de confidencialidade, autorização e direitos próprias de cada documento.
