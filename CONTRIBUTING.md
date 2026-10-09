# Contribuindo para Meu Artigo

O projeto é público e distribuído sob licença Apache 2.0. A versão beta aceita correções de documentação, melhorias técnicas e sugestões metodológicas fundamentadas. **Nenhum relato ou contribuição autoriza divulgar documentos acadêmicos protegidos, projetos de terceiros, credenciais ou dados pessoais.**

## Antes de contribuir

1. Consulte [guia de implantação beta](docs/IMPLANTACAO-BETA.md), [testes pendentes](docs/VALIDACOES-PENDENTES.md) e [segurança](SECURITY.md).
2. Veja se já existe uma Issue semelhante. Registre o comportamento observado, a versão da Skill, o passo executado, o resultado esperado e o resultado efetivo. Não atribua testes ou resultados a pessoas que não participaram.
3. Para mudanças de código, crie branch e pull request para a `main`. Mantenha compatibilidade com IDs e tabelas existentes; não adicione abas ou serviços pagos sem justificativa.
4. Execute `python scripts/release_audit.py`, `python -m unittest discover -s tests -v` e `python scripts/smoke_test_provenance.py`. Descreva quais controles foram afetados e anexe resultados técnicos, sem dados sensíveis.
5. Diferencie testes de software de evidência de qualidade científica. Fixtures sintéticas são permitidas **apenas** em testes descartáveis; não devem ser apresentadas como corpus ou publicação real.

## Requisitos de integridade

As consultas a fontes precisam ter proveniência verificável. Não invente DOI, pesquisa executada, avaliador, estudo, métrica de eficiência, comparação empírica ou aceite editorial. Documente limites, riscos de viés, direitos de PDFs e revisão humana realmente efetuada.

Ao sugerir alteração metodológica, identifique a fundamentação, o problema que resolve e os impactos sobre as regras existentes. Não reproduza longos trechos de artigos protegidos.

## Problemas de segurança

Não abra Issue pública com tokens, informação pessoal, métodos de exploração ou documentos confidenciais. Siga [SECURITY.md](SECURITY.md). Uma Issue não é canal privado.

## Política de manutenção

Contribuições passam por revisão técnica e não constituem aprovação automática. Releases beta usam numeração explícita; mudanças incompatíveis precisam ser descritas no changelog. O mantenedor pode rejeitar sugestões que comprometam rastreabilidade, direitos de terceiros ou rigor científico.


## Licença, atribuição e contribuições

Os materiais originais do repositório são distribuídos sob Apache License 2.0.
Ao redistribuir versões modificadas, observe as condições da licença,
inclusive manutenção de avisos de copyright e atribuição pertinentes,
conteúdo de NOTICE e indicação de arquivos modificados. A orientação
acadêmica sobre como citar o projeto está em CITATION.cff; não se deve
representar a citação científica formal como requisito adicional à licença.
Contribuições de terceiros devem respeitar sua titularidade e permissões.


## Procedimento de desenvolvimento e releases

Alterações devem seguir branch, Pull Request, verificação obrigatória de CI e
integração à branch principal. O guia para sincronizar metadados de versão e
publicar uma beta manualmente está em [publicação e versionamento](docs/GUIA-DE-RELEASES.md).
A versão distribuída mais recente não muda automaticamente com commits na branch
principal; não declare validação empírica a partir da aprovação de testes técnicos.
