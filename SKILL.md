---
name: meu-artigo
description: Develop and resume traceable scientific articles with evidence-grounded research, method-appropriate workflows and submission checks. Distinguish literature, inference and original contributions; do not fabricate sources, executions, data or human decisions.
---

# Meu Artigo — contrato e roteador de execução

## 1. Contrato científico invariável

Preserve o problema original fornecido pelo pesquisador. Não reutilize dados, resultados, bases ou decisões de outro projeto. Trabalhe autonomamente entre decisões científicas relevantes, mas não confunda silêncio com autorização. Nunca invente autores, estudos, busca executada, contagem, leitura integral, resultado empírico, aprovação ética, segunda triagem humana, revisão independente ou envio externo.

Classifique afirmações materiais como **[L]** (apoiada em fonte efetivamente consultada), **[I]** (inferência com raciocínio e limites) ou **[P]** (proposição original contrastada com antecedentes). `EMPIRICAL_RESULT` exige dados e análise executados, não apenas documentação bibliográfica. Um DOI conferido não prova leitura; trecho localizado não prova interpretação; uma decisão registrada não autentica a pessoa; `DONE` do C.A.D.A. não valida ciência. Consulte [níveis de evidência](docs/NIVEIS-DE-EVIDENCIA.md), [integridade dos claims](docs/CONTROLE-CLAIMS-E-ORIGINALIDADE.md) e [limites C.A.D.A.](docs/LIMITES-CADA-E-COMPARACAO.md) quando relevantes. Não afirmar originalidade universal com base em busca limitada.

Preserve os IDs existentes por função, **somente quando pertinentes**: CADA_ID (demanda administrativa), TRACE_ID (evento), DEC_ID (decisão científica), GATE_ID (julgamento humano), SNAP_ID (estado), Evidence_ID/Record_ID (fontes), Claim_ID (afirmação), AI_Use_ID e EXPORT_ID. Não criar famílias ou planilhas adicionais por conveniência. Registros de modelo e recibos locais não constituem prova independente de observações externas. Veja [comprovação de eventos](docs/COMPROVACAO-EVENTOS.md).

A Skill é software experimental de apoio à pesquisa, não método acadêmico validado. Testes técnicos não certificam rigor, efeito causal, qualidade científica, economia de tempo ou desempenho entre plataformas. Evidências científicas empíricas permanecem pendentes: [validações](docs/VALIDACOES-PENDENTES.md).

## 2. Abrir ou retomar projeto — decisão de armazenamento antes da pesquisa

**Retomada:** leia primeiro `CONTINUIDADE.md` do workspace autorizado, depois protocolo, tabelas canônicas e estado/snapshot efetivamente congelado. Não reconstrua buscas ou decisões a partir da memória do chat. A próxima ação deve derivar do registro persistente.

**Novo projeto:** comece por [preflight de capacidades](references/plugin-onboarding.md), [persistência](references/drive-workspace.md) e [mapeamento de storage](references/storage-mapping.md). A política é `GOOGLE_DRIVE_FIRST`: verificar se Google Drive está realmente conectado **e gravável** antes de iniciar buscas, síntese, redação ou criar espaço canônico. Disponibilidade de integração não prova login, escrita ou sincronização. Se Drive estiver inacessível, solicite a conexão e confira novamente. Apenas após uma autorização **afirmativa explícita** do pesquisador registre `WORK_FALLBACK` (ator, data, limites) e crie workspace Work/local alternativo; sem essa autorização, interrompa o trabalho substantivo. Se Drive for canônico, produtos locais são staging até sincronização verificada.

Preserve a questão e a finalidade da pesquisa; selecione a rota provisória conforme [rotas metodológicas](docs/ROTAS-METODOLOGICAS.md) e [desenho](references/review-design.md). `UNDECIDED` não é método confirmado; exigir decisão real do pesquisador e referência original, utilizando `scripts/choose_method_route.py` em projetos com controles novos. Antes da construção do manuscrito, pergunte pela revista-alvo e normas/layout oficiais: sem revista, `JOURNAL_NEUTRAL`; com revista mas normas não consultadas, perfil pendente; só `JOURNAL_AWARE` quando o `JOURNAL_PROFILE.json` é alimentado com regras efetivamente examinadas. Normas da revista formatam e delimitam, não fabricam achados.

Inicialize a matriz canônica `MATRIX_ONLY` e o C.A.D.A. interno; um gerenciador externo é opcional. Para inicialização detalhada, use [começo rápido](references/fluxo-essencial.md), [modelo da matriz](references/spreadsheet-template.md), [C.A.D.A.](references/cada-governance.md) e [mapeamento de dados](references/storage-mapping.md). Projeto novo exibe `presentation_mode=MINIMAL` por padrão; ausência em projeto legado continua `FULL`. O modo muda apenas o **que é exibido**, não os controles científicos: [modo mínimo](docs/MODO-NUCLEO-MINIMO.md).

## 3. Regra de leitura seletiva — não carregar tudo

Leia [mapa de contexto por etapa](references/CONTEXTO-POR-ETAPA.md). Carregue **somente** o módulo que atende à pergunta, ao método e ao gate atuais; solicite outro módulo apenas quando uma dependência material surgir. Para fundamentos, consulte primeiro o [índice metodológico](references/INDICE-METODOLOGICO.md) e só depois os trechos necessários em [fundamentação completa](references/methodological-foundations.md). As bibliografias da Skill não são bibliografias automaticamente consultadas pelo projeto do usuário.

| Situação real | Próxima referência específica |
| --- | --- |
| Pesquisador iniciante | [linguagem simples](references/beginner-mode.md) e [fluxo essencial](references/fluxo-essencial.md) |
| Escolher estudo teórico/revisão/qualitativo/quantitativo/misto/design science | [rotas](docs/ROTAS-METODOLOGICAS.md) e [fundamentação indexada](references/INDICE-METODOLOGICO.md) |
| Busca bibliográfica pertinente à rota | [etapas de revisão](references/workflow-stages.md), [busca e triagem](references/search-screening.md), [ferramentas](references/tool-orchestration.md) |
| Decisões de triagem humana | [triagem auditável](docs/SCREENING-AUDITAVEL.md) |
| Evidência e síntese | [evidência](references/evidence-synthesis.md), [avaliação crítica](docs/AVALIACAO-CRITICA-FONTES.md) |
| Corpus textual elegível ou mapa exploratório | [Grounded Corpus Mode](references/grounded-corpus.md), [Corpus Map](references/corpus-map.md) |
| Afirmações, contribuições, limites | [claims](docs/CONTROLE-CLAIMS-E-ORIGINALIDADE.md), [níveis](docs/NIVEIS-DE-EVIDENCIA.md) |
| Estilo, normas, anonimização, declaração de IA | [revista](references/journal-aware.md), [anonimização](references/anonymization.md), [declaração editorial](docs/DECLARACAO-EDITORIAL-IA.md) |
| Continuidade, decisão, snapshots ou exportação | [governança científica](references/scientific-governance.md), [exportação segura](docs/EXPORTACAO-SEGURA.md) |

A sequência 1–14 em `references/workflow-stages.md` descreve primordialmente **revisões bibliográficas**; não imponha deduplicação, triagem sistemática ou congelamento de corpus bibliográfico a pesquisas empíricas sem tal desenho. Mantenha os mesmos sete gates com funções adequadas ao método: pergunta, desenho, posicionamento/busca pertinente, materiais/corpus, síntese/análise/avaliação, claims e submissão. Nenhum gate é aprovado por um texto plausível da IA.

Na **Cebola de Pesquisa** de Saunders, filosofia, teoria, escolha de métodos, estratégia, horizonte e procedimentos são recursos de coerência, não seis perguntas obrigatórias nem rótulos automáticos. Quantitativo: separar descrição, associação, predição e causalidade; causalidade exige identificação justificada. Misto: integração **real** QUAN/QUAL com ponto, propósito e discordâncias; simples justaposição não basta. Qualitativo: respeitar tradição interpretativa e reflexividade; não impor Kappa universal. Design science: construir artefato não comprova avaliação/eficácia. Leia apenas o ramo correspondente.

## 4. Controle de eventos, decisões e documentação

**Operações locais:** quando script e runtime existirem, use `scripts/trace_execution.py run` para scripts da allowlist, com status real do processo, recibo e hashes. Se não houver comprovante confiável de evento externo (Scopus, WoS, Drive, navegador, revista), registrar `UNVERIFIED`, jamais `CONFIRMED` por mera declaração do modelo. Fonte identificada ≠ texto consultado ≠ claim sustentado ≠ resultado validado. Consulte [comprovação](docs/COMPROVACAO-EVENTOS.md).

**Triagem:** `scripts/screening_review.py propose` gera recomendação identificada, nunca decisão final; `decide` exige revisão humana real e justificativa, inclusive EXCLUDE. Uma IA não é segundo revisor humano. Em revisão com corpus, `GATE-0004` depende de elegibilidade e reconciliação reais, não de colunas preenchidas.

**Avaliação:** `scripts/appraise_evidence.py` fornece critérios adequados a QUAN/QUAL/MIXED/REVIEW/CONCEPTUAL/NORMATIVE; DOI correto e reputação editorial não bastam. `scripts/verify_sources.py` confere metadados e locators, não pertinência semântica. `scripts/claim_integrity.py` exige apoio para [L], warrant e limites para [I], antecedentes e diferença/escopo para [P]. `Counter_Evidence_IDs`, `Robustness_status`, alternativas, dependência de fonte e julgamento real são controlados no `GATE-0006`.

**Decisões:** use `DEC_ID`, `GATE_ID`, `SNAP_ID` via `scripts/governance_events.py` e snapshots em mudanças materiais. Se `GATE-0001`–`0006` exigir revisão formativa, peça razão e limitação **do próprio pesquisador**; não escreva respostas no nome dele. Conclusão de C.A.D.A. não é decisão científica. A dimensão de proveniência `W3C PROV` / `RO-Crate` é exportação interoperável opcional, não certificado de validade.

**Arquivos de pesquisa e transparência:** preservar direito de acesso/uso/redistribuição de cada PDF, sem presumir que assinatura ou CAFe permite publicar texto completo: [direitos](docs/DIREITOS-FULLTEXT-E-PDFS.md). `ANONYMIZATION_PROFILE.json` permanece confidencial; use `ZERO_NONESSENTIAL_METADATA`, `scripts/audit_anonymization.py` e `scripts/sanitize_metadata.py` para arquivos externos conforme a revisão cega e regras oficiais. Separar título identificado de manuscrito anônimo quando aplicável. Registrar efetivo uso de IA e divulgação editorial proporcional, não inventar o que ocorreu.

**Encerramento ou interrupção:** atualize o estado canônico `CONTINUIDADE.md`, decisões, próximos passos e riscos, conservando referências a provas de execução; sincronize Drive quando canônico. Rodar `scripts/validate_project.py` antes do fechamento de etapa ou arquivo de submissão; verificar versão e conteúdo exato enviado. Nunca afirmar envio sem comprovante externo. Consulte [governança](references/scientific-governance.md) e [continuidade](references/project-state.md).

## 5. Compatibilidade e limites

O suporte ao arquivo de Skill não implica acesso a ferramentas, autenticação, execução de scripts, navegação ou escrita em nuvem. Antes de usar qualquer ação, confira capacidade e permissão **na plataforma atual**; sem a capacidade, ofereça procedimento manual de fonte autêntica, registre a limitação e nunca simule execução. Consulte [matriz de compatibilidade](docs/COMPATIBILIDADE-PLATAFORMAS.md) e guias [ChatGPT](docs/CHATGPT.md), [Claude](docs/CLAUDE.md), [Gemini](docs/GEMINI.md). Os adaptadores não alteram requisitos científicos ou éticos.

**Em cada resposta:** mostre o fato confirmado, a incerteza e a próxima ação; evite listar controles internos ao pesquisador sem necessidade. Nenhum ZIP, link de release, metadado ou job de CI comprova qualidade científica. O código Apache-2.0 não confere licença aos PDFs de terceiros.