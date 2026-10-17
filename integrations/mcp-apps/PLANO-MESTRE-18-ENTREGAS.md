# PLANO MESTRE — 18 ENTREGAS E MATRIZ DE EXIBIÇÃO

**Atualizado:** 2026-10-17. **Ponto atual: ENTREGA 16/18**, consolidação/adaptação, **sem merge**. 

**Escopos distintos:** (a) Plano Mestre de 18 entregas de engenharia; (b) 12 experiências de exibição propostas para a interface; (c) 10 telas HTML do MCP Apps; (d) 21 abas da matriz C.A.D.A. Nenhum desses totais substitui os demais.

## Arquitetura consolidada (decisão de 17/10)

- A Skill mantém a pesquisa no Drive autorizado do pesquisador e seus registros canônicos.
- O ChatGPT do pesquisador, usando o conector Drive da própria conta, lê planilhas e arquivos necessários.
- O ChatGPT extrai exclusivamente tarefas, gates, próxima ação e diagnóstico técnico estritamente delimitados; não envia documentos integrais.
- O MCP **recebe e processa temporariamente** essa projeção por chamada e exibe no painel. O MCP não acessa Google Drive, não tem token Google e não persiste pesquisas na VPS. Não é solução zero-knowledge.
- Nenhuma interface aprova gate, comprova sincronização Drive ou substitui documentos científicos originais.
- Em sessões A/B/C, somente os dados da conexão corrente podem ser projetados. Sem snapshot válido, painel fica vazio; nenhum estado anterior é reutilizado.

## Matriz de controle das 18 entregas

| Nº | Entrega original | Estado verificado/registrado | O que existe | O que ainda falta | Evidência/base |
|---|---|---|---|---|---|
| 01 | Congelar a base e registrar SHAs | Histórico técnico registrado | Base e commits candidatos inventariados | Reconciliar SHA final da pilha antes do merge | GH/PR 78 e 79 |
| 02 | Mapear funcionalidades e duplicações | Histórico técnico registrado | Matriz de absorção para Skill/Drive/MCP | Revalidar remoção de redundâncias na #79 | GH/PR 78 |
| 03 | Definir contratos e arquitetura única | Adaptada, requer aceite | Contratos Drive e ciência; separação Skill/ChatGPT/MCP atualizada | Revisar privacidade dos campos transitórios | integrations/mcp-apps/PLANO-MESTRE-18-ENTREGAS.md |
| 04 | Fortalecer CI, dependências e segurança | Verificada no CI | Workflows de release, segurança, CodeQL e MCP | Manter checks verdes no mesmo SHA de integração | GH/PR 78 e 79 |
| 05 | Reconciliar PR #74 e base segura | Verificada em candidata isolada | Integração controlada com PR #77, diffs, lock e CI | Revisão humana final do diff antes de incorporar | GH/PR 78 |
| 06 | Fixar raiz canônica do Google Drive | Verificada sinteticamente | Busca/reutilização, hierarquia, duplicações e parent check | Aceite com leitura real de cada usuário, sem escrita | GH/PR 78 |
| 07 | Endurecer Drive F1–F4 | Verificada sinteticamente | Guardas de identidade, parent e providências antes da escrita | Validar backend e permissões reais no piloto | GH/PR 78 |
| 08 | Endurecer Drive F5–F9 | Verificada sinteticamente | Journal, CAS e recuperação testados em cenários falsos | Concorrência, idempotência e recibos Drive reais não comprovados | GH/PR 78 |
| 09 | Construir painel azul | Verificada sinteticamente | 10 telas HTML em 4 idiomas e verificações visuais | Confirmar exibição dentro do ChatGPT com dados autorizados | GH/PR 78; assets/research_site.html |
| 10 | Consolidar servidor MCP Apps único | Verificada sinteticamente; arquitetura adaptada | Servidor UI, tool de painel, HTTP/stdio; dados transitórios via host | Instalação e renderização reais no ChatGPT | GH/PR 79 |
| 11 | Implementar Auth0 OAuth do MCP | Implementação testada offline | JWT RS256/JWKS, audience, scopes, HTTP local | OAuth/PKCE com Auth0 real e ChatGPT pertence à etapa 17 | GH/PR 78 e 79 |
| 12 | Incorporar auditoria científica da PR #65 | Verificada sinteticamente | REG-018 e REG-011; consultas sem aprovação automática | Aceite científico independente por método | GH/PR 78 |
| 13 | Diagnósticos científicos reproduzíveis | Verificada sinteticamente | REG-013/001/019 e sidecars, status não avaliado quando faltam provas | Aferir validade com casos reais autorizados e revisão humana | GH/PR 78 |
| 14 | Integrar projeção de métodos da PR #66 | Verificada sinteticamente | Cinco caminhos de exploração, nenhuma decisão automática | Confirmar diversidade metodológica com revisores | GH/PR 78 |
| 15 | Homologação horizontal Skill/HTML/MCP | Verificada sinteticamente | Skill, painel nativo, HTML e MCP em testes integrados | Repetir ponta a ponta com versões instaladas e Drive de teste | GH/PR 78 e 79 |
| 16 | Consolidar e incorporar PRs | EM ANDAMENTO — SEM MERGE | PR #79 empilhada sobre #78; adaptações de host→MCP e testes novos | Revisão final e decisão humana GO/NO-GO de merge; main inalterada | GH/PR 78 e 79 |
| 17 | Homologar OAuth na Contabo e no ChatGPT | PENDENTE — EXTERNO | Testes sintéticos e domínio mcp.allflux.com.br planejado | Instalar em VPS isolada, OAuth real, teste de dois ChatGPT/Drive distintos | GH/PR 79; docs/CHATGPT-MCP-HOST-ACCEPTANCE.md |
| 18 | Publicar versão controlada | PENDENTE — BLOQUEADA | Governança de release e beta prevista | Somente após 16+17, aceites, versão/rollback, Plugin/release autorizados | docs/INTEGRATED-SKILL-HOMOLOGATION.md |

**Atenção histórica:** o rótulo “Etapa 17” usado para a fase corretiva CodeQL/GHAS pré-piloto não substituiu a entrega **17 original (OAuth na Contabo e no ChatGPT)**. O CodeQL da PR #78 foi reconciliado documentalmente (GHAS #5–11), e a segurança permanece como gate transversal às entregas, não como etapa final concluída.

## Matriz das 12 experiências de exibição

Esta matriz descreve as 12 experiências visuais anteriormente propostas; não constitui novas entregas 19–30 do Plano Mestre. Um módulo visível em teste **não** significa que um fluxo real de Google Drive→ChatGPT→MCP tenha sido homologado.

| Nº | Experiência | Situação / implementação existente | Lacuna |
|---|---|---|---|
| 01 | Painel geral | Tela overview presente; leitura real ainda não homologada | Parcial |
| 02 | Próxima ação | Componente do painel e campo next_action | Parcial |
| 03 | Mapa científico | Corpus Map na matriz; não integra todas as 10 telas | Pendente de integração visual |
| 04 | Quadro C.A.D.A. | Tela tasks presente; recebe projeção de até 200 itens | Parcial |
| 05 | Buscas e fontes | Tela sources; comprovação bibliográfica não feita no MCP | Parcial |
| 06 | Evidências [L]/[I]/[P] | Tela evidence; sem entrega de passagens/arquivos integrais | Parcial |
| 07 | Validação humana | Tela validations/steps; sete gates sem aprovação automática | Parcial |
| 08 | Linha do tempo | Tela trace disponível; histórico real depende de registros | Parcial |
| 09 | Prontidão editorial | Tela submission com advertências de não verificado | Parcial |
| 10 | Sincronização | Tela sync informa que MCP não verifica Drive | Parcial |
| 11 | Primeiro uso | Contrato de onboarding na Skill; UX dentro do host não observada | Pendente de E2E |
| 12 | Mobile e modo escuro | Estilo/testes estáticos; aparelho/tema real não homologado | Pendente de E2E |

As **10 telas HTML** existentes são: Visão geral, Etapas, Tarefas C.A.D.A., Fontes e buscas, Evidências, Validações, Métodos, Rastreabilidade, Submissão, Sincronização. Primeiro uso, mapa científico e mobile/tema são experiências transversais, não necessariamente telas próprias.

## Entrega 16 — adaptação e consolidação de fato

**Feito em PR #79, empilhada sobre PR #78:**

1. Eliminado acesso direto do servidor MCP a Drive, tokens e pastas privadas.
2. Adicionado `host_projection.mjs`: aceita somente dados de exibição do próprio ChatGPT, com validação estrita, sem gravar e com falsidade científica bloqueada.
3. A ponte MCP Apps mantém estados de A/B separados por requisição, sem reter snapshot do usuário anterior; HTML preservado para compatibilidade.
4. A Skill tem instruções explícitas em `references/mcp-tool-use.md` para ler os **registros que já existem** no Drive conectado do pesquisador e projetar somente campos autorizados.
5. Testes sintéticos adversariais com usuários fictícios A/B, limites de payload, schemas e visualização em dez telas.
6. O GitHub CI deve ser verificado sempre no mesmo HEAD final; checks históricos não substituem os checks novos.

**Falta nesta entrega:** revisão humana integral do diff PR #78 + PR #79, decisão de integração/merge, confirmação de versões compatíveis e eventual escolha de distribuição. Não fazer merge nesta entrega sem autorização.

## Entrega 17 — homologação externa real, ainda pendente

1. Verificar disponibilidade e habilitação do Plugin/MCP na conta ChatGPT de teste.
2. Configurar Auth0 e VPS `mcp.allflux.com.br/mcp` somente com autorização específica; habilitar Nginx/TLS sem expor Node diretamente.
3. Pesquisador A autoriza **seu próprio** Google Drive no ChatGPT e abre projeto de teste; pesquisador B repete com **seu** Drive, em outra conta isolada.
4. ChatGPT de A lê os registros reais autorizados de A e chama `meu_artigo_painel` somente com projeção mínima. Repetir para B, trocar projeto, revogar sessão, falhar rede e verificar nenhuma exibição cruzada.
5. Verificar UI real (10 telas, 4 idiomas, primeiro uso, acessibilidade e responsividade) e os sete gates, sem aprovações presumidas.
6. Registrar receipts, incidentes, logs sem dados privados, versão instalada e GO/NO-GO independente. Não alegar aprovação se o host não expuser o MCP Apps real.

## Entrega 18 — publicação controlada, ainda pendente

Somente após decisão sobre PRs/merge, OAuth E2E, controle de privacidade, compatibilidade de Skill/Plugin, critérios de rollback, autorização de release, revisão científica humana e estratégia de grupos convidados.

## Marcadores de acompanhamento (obrigatórios a partir de agora)

Em cada atualização exibir: **Entrega N/18; objetivo; feitos na rodada; pendências; SHA e PR; checks no mesmo SHA; autorização necessária; próxima ação**. Registrar separadamente as 12 experiências e seus níveis de evidência: código, teste sintético, host real ou avaliação humana.

**Fontes:**
- https://github.com/rebsonm/MeuArtigoSkill/pull/78
- https://github.com/rebsonm/MeuArtigoSkill/pull/79
- https://github.com/rebsonm/MeuArtigoSkill/blob/feature/mcp-multiuser-readonly-isolation/references/mcp-tool-use.md
- https://github.com/rebsonm/MeuArtigoSkill/blob/feature/mcp-multiuser-readonly-isolation/integrations/mcp-apps/README.md
- https://github.com/rebsonm/MeuArtigoSkill/blob/feature/mcp-multiuser-readonly-isolation/docs/MATRIZ-CADA.md
