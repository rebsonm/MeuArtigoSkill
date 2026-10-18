# Meu Artigo — matriz executável das etapas restantes (18/10/2026)

Este documento distingue **tarefas técnicas** de **autorizações humanas ou
externas**. O plano mestre possui 18 entregas; as entregas 16, 17 e 18
continuam abertas. As dez pendências abaixo são unidades de aceitação
até disponibilização pública, não dez novos módulos de software.

## Baseline

- PR única de integração: #89 (Draft contra main); não integrar #87 ou #88 separadamente.
- Skill fonte: beta.9 (candidata); Plugin privado instalado beta.8, Skill
  embutida beta.6; última release de Skill confirmada beta.6.
- Ao criar este plano, os sete workflows estavam aprovados no
  SHA `ad340fc3a07b82c728e7152f8527ea8d95a6a0f4`; qualquer commit
  novo invalida seu valor para uma decisão de merge. Reexecutar no HEAD final.
- Marco técnico de continuidade: UI MCP validada na inicialização HTTP e
  sondas locais /healthz e /readyz com resposta mínima; ID do teste E05 e ID
  do piloto MCP não podem ser empacotados como app de produção. Estes
  mecanismos não substituem OAuth, TLS ou isolamento de Drives reais.

## Dez etapas restantes e entregas verificáveis

| ID | Entrega | Próxima atividade | Evidência para encerrar | Bloqueio |
|---|---|---|---|---|
| R01 | 16 | Revisão independente acumulada dos 162+ arquivos, segurança, fontes científicas e Auth0/F1–F9 | parecer independente e pendências HIGH resolvidas no SHA final | humano |
| R02 | 17 (pré-merge) | E05 no ChatGPT real: ALPHA/BRAVO, dez telas, resize, foco, troca de idioma, teardown e CSP efetiva | relatório visual reproduzível, versão exata e origem da indicação CSP | host/autorização E05 |
| R03 | 16 | Aprovação explícita da PR #89 por SHA e merge único na main | autorização específica e merge SHA | decisão do mantenedor |
| R04 | 16→17 | Reexecutar CI, pacote SHA-256 e regressões depois do merge | checks verdes e checksum do commit efetivo na main | R03 |
| R05 | 17 | HTTPS estável, Auth0 configuration, health/ready locais, logs sem conteúdo, segredos, rollback | prova operacional com ingress revisado; não é só /readyz=200 | autorização VPS |
| R06 | 17 | OAuth/PKCE real e A/B com duas identidades independentes, 401/403, revogação | registros sanitizados de login/negativas no ChatGPT | R05, consentimento |
| R07 | 17 | Google Drive individual A/B, F1–F9, journal, CAS, readback, negação cruzada | duas pastas canônicas verificadas e provas sintéticas/consentidas de isolamento | R06 |
| R08 | 17 | Fluxo E2E criar/retomar artigo, tarefas C.A.D.A., sete gates, visualização, falha e privacidade | aceite do mantenedor, políticas, rollback, sem aprovação científica automática | R07 |
| R09 | 18 | Empacotar/instalar beta privada de Skill + app de produção validado; piloto controlado | release ID anterior/atual, primeira utilização e feedback de usuários convidados | R08, autorização Plugin |
| R10 | 18 | Submissão With MCP, avaliação da plataforma, publicação e instalação externa | aprovação externa, entrada pública e teste por pesquisador independente | R09, autorização publicação |

**Total: dez etapas pendentes** (R01–R10). O que é realizável sem
autorização de infraestrutura inclui CI, testes negativos, revisão
estática, documentação, arquitetura e preparo de versões. Não contar
testes sintéticos como conclusão de R02/R05/R06/R07.

## Contrato de evidência documental

`python integrations/mcp-apps/scripts/release_gate.py --source-sha $(git rev-parse HEAD)`
retorna a matriz pendente por padrão. Opcionalmente `--records arquivo.json`
lê registros externos desidentificados. Mesmo que os dez registros
estejam documentados, a ferramenta **nunca** concede autorização
de merge, implantação, instalação ou publicação: a evidência e a
identidade de quem aprovou precisam ser conferidas fora do script.

Exemplo com um único registro hipotético, **não uma aprovação**:

```json
{
  "R01": {
    "status": "PASS",
    "source_sha": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "evidence_ref": "EVID-REVIEW-0001",
    "observer_role": "INDEPENDENT_REVIEWER"
  }
}
```

O campo `source_sha` precisa corresponder ao commit que estiver sendo
avaliado. Passes sem prova, com SHA antigo, campos extras ou papéis
inadequados devem falhar fechados. O script não aceita conteúdo dos
artigos, credenciais, IDs de arquivos, URLs privadas nem nomes de pessoas.

## Decisão atual

`GO_SOURCE_TESTS=PASS` **somente nos SHAs individualmente verificados**;
`GO_MERGE=NO-GO`; `GO_E05_REAL=NOT_VERIFIED`;
`GO_REAL_OAUTH_AB=NOT_VERIFIED`; `GO_DRIVE_AB=NOT_VERIFIED`;
`GO_PRIVATE_PLUGIN=NO-GO`; `GO_PUBLIC=NO-GO`.

Não fazer merge, deploy, alterar Auth0/Drive, instalar plugin nem publicar
sem uma aprovação própria para cada ato.
