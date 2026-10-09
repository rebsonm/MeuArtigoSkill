# Implantação da beta pública — Meu Artigo

**Versão preparada:** 0.8.0-beta.8 • **Estado:** beta pública para avaliação voluntária de uso, não validação científica.

## Obtenção

Utilize a página [Releases do GitHub](https://github.com/rebsonm/MeuArtigoSkill/releases), procurando `v0.8.0-beta.8`, e escolha `MeuArtigoSkill-v0.8.0-beta.8.zip`. O arquivo `SHA256SUMS.txt` da mesma versão permite conferir a integridade do download. A alternativa `Code → Download ZIP` representa a versão atual da branch, que pode ser diferente da versão fixa publicada.

O ZIP da Skill tem `SKILL.md` na raiz, além de `agents/`, `assets/`, `references/`, `scripts/`, `docs/`, `benchmarks/`, `LICENSE`, `CITATION.cff`, `VERSION` e manifest de SHA-256. Os dados de usuários, PDFs de terceiros, tokens, arquivos temporários e corpus científicos **não entram** nesse pacote.

## Instalação

O mecanismo de instalação de Skills depende da plataforma e das permissões da conta. Siga [ChatGPT](CHATGPT.md), [Claude](CLAUDE.md) ou [Gemini](GEMINI.md) e consulte a [matriz de compatibilidade](COMPATIBILIDADE-PLATAFORMAS.md) antes de instalar. Verifique as opções efetivamente disponíveis na conta. Não há garantia de que todas as plataformas forneçam execução local de scripts ou as mesmas integrações.

1. Verifique a versão do ZIP e, quando conveniente, compare seu hash com `SHA256SUMS.txt`.
2. Importe o ZIP oficial pelo recurso de upload da plataforma, quando existir. Em ferramentas baseadas em pastas, extraia os arquivos mantendo `SKILL.md` na raiz da pasta da Skill.
3. Inicie **um novo projeto**, descrevendo problema e objetivo de pesquisa; não aproveite corpus ou decisões de projetos anteriores.
4. Verifique a conexão e permissão de escrita do Google Drive antes de iniciar trabalho substantivo. Sem Drive, o modo alternativo só pode ser ativado após consentimento explícito.
5. Informe a revista-alvo e suas normas, caso já definidas. Não presuma que uma declaração de IA é permitida sem política oficial.
6. Mantenha as decisões científicas com o pesquisador, documentação real de fonte e limitações, sem simular revisores.
7. Nunca publique PDFs protegidos nem arquivos externos sem auditoria de anonimização e direitos.

Use o [checklist de primeiro uso](CHECKLIST-PRIMEIRO-USO.md) para acompanhar as etapas sem criar abas ou IDs adicionais.

## Compatibilidade ainda não demonstrada

O suporte documentado para instalar Skills no ChatGPT, Claude e Gemini **não valida a importação nem a operação ponta a ponta do Meu Artigo nesta beta**. A [matriz de compatibilidade](COMPATIBILIDADE-PLATAFORMAS.md) apresenta as condições documentadas e o que falta testar com ambientes reais.

## Controles que podem ser executados offline

No clone/descompactação do repositório, com Python 3.10+ e biblioteca padrão, são executáveis:
- `python scripts/release_audit.py` — estrutura/sintaxe/versão;
- `python -m unittest discover -s tests -v` — regressões do software;
- `python scripts/smoke_test_provenance.py` — verificação de proveniência demonstrativa controlada;
- `python scripts/build_skill_bundle.py` — pacote de distribuição com manifest e SHA-256.

Os testes podem criar fixtures **descartáveis** e não constituem investigação empírica da qualidade de artigos.

## Compatibilidade e atualização

Os projetos mais antigos não devem ser promovidos artificialmente às novas regras. Antes de migrar, preserve backups/snapshots e aplique somente as mudanças compatíveis de schema, mantendo decisões e originais. Atualizar a Skill **não** atualiza automaticamente as planilhas ou projetos existentes nem altera o estado do Drive sem ação registrada.

Guarde a referência de versão `v0.8.0-beta.8`, os arquivos científicos originais e as instruções editoriais vigentes. Para problemas, consulte [CONTRIBUTING](../CONTRIBUTING.md) e [SECURITY](../SECURITY.md).

## O que ainda não está comprovado

A aprovação dos testes automatizados demonstra controles técnicos, não validação científica completa, melhora causal decorrente do C.A.D.A., confiabilidade global em produção, disponibilidade de APIs externas, conformidade universal com revistas nem funcionamento idêntico em todas as plataformas. Essas frentes estão documentadas em [VALIDACOES-PENDENTES.md](VALIDACOES-PENDENTES.md).
