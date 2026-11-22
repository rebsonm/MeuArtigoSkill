# Meu Artigo — decisão do mantenedor sobre distribuição dos PDFs 35, 48 e 49

**Data do registro:** 22/11/2026 (America/Fortaleza). **Origem da decisão:** instrução explícita do usuário solicitante no ChatGPT: “Pode liberar esses pdfs e manter como autorizador”. **Identificação do autorizador da decisão interna do projeto:** mantenedor solicitante, perfil GitHub `rebsonm`. **Autorização registrada:** `PROJECT_MAINTAINER_DISTRIBUTION_INTENT_APPROVED` para os três arquivos identificados abaixo. **Não é assinatura digital verificada, declaração de titularidade das obras, licença dos autores/editoras nem certificação jurídica dos materiais de terceiros.**

## Escopo exato e limite da decisão

Esta decisão abrange somente os três PDFs da última investigação (PDF-35 RPQ, PDF-48 UFF/RPCA, PDF-49 BPSR), **não** todos os 51 arquivos. O mantenedor autorizou internamente a intenção de liberar esses três e pediu que se mantivesse como autorizador dessa decisão. A instrução elimina a necessidade de pedir **nova permissão gerencial para este mesmo escopo**, mas **não remove** os requisitos já documentados de licença autoral aplicável, atribuição, eventuais exceções de terceiros e edição exata. O autorizador **não foi identificado como titular dos direitos autorais** desses artigos.

| PDF | Autorização gerencial do projeto | Prova de licença de terceiros | Decisão de distribuição pública efetiva |
|---|---|---|---|
| **PDF-35 — Campos/Saidel (2022), RPQ** | **AUTORIZADO PELO MANTENEDOR** | Página específica CC BY 4.0 versus rodapé genérico de revista “não comercial” sem esclarecimento; `10.33361/RPQ.2022.v.10.n.25.545` | **BLOQUEADO** até confirmação editorial da licença aplicável à edição; não atribuir direitos que o mantenedor não detém |
| **PDF-48 — Silva/Barbosa/Lima (2020), UFF** | **AUTORIZADO PELO MANTENEDOR** | CC BY com usos comerciais autorizados; versão e escopo de componentes/entrevistas ainda não confirmados; `10.12712/rpca.v14i1.38405` | **CONDICIONADO** à licença da edição exata e aos avisos sobre materiais incorporados |
| **PDF-49 — Figueiredo Filho et al. (2019), BPSR** | **AUTORIZADO PELO MANTENEDOR** | Link da licença do próprio artigo de 2019 aponta diretamente a CC BY 4.0; figuras 1, 2, 4 e 5 citam fontes externas e precisam de verificação individual; `10.1590/1981-3821201900020001` | **CONDICIONADO** à checagem de direitos de terceiros, créditos e versão do PDF |

## Identidade, integridade e evidência

- A PR #112 é do repositório `rebsonm/MeuArtigoSkill`; seu autor identificado pela API GitHub usa login `rebsonm`. A instrução em primeira pessoa nesta conversa é a evidência **da autorização gerencial**. **Não afirmar que este registro autentica uma assinatura eletrônica ou a titularidade das obras**.
- A auditoria de origem é [`PDF-35-48-49-EDITORIAL-RIGHTS-DEEP-REVIEW-2026-11-22.md`](./PDF-35-48-49-EDITORIAL-RIGHTS-DEEP-REVIEW-2026-11-22.md), commit `87352d53dd007d8a3514977d95b5f09fb9b50347`. O relato de 51 itens está em [`PUBLIC-PDF-RIGHTS-51-RECONCILIATION-2026-11-22.md`](./PUBLIC-PDF-RIGHTS-51-RECONCILIATION-2026-11-22.md).
- Os hashes SHA-256 dos PDFs do GitHub foram recalculados e são correspondentes ao catálogo: PDF-35 `b3e78db1e163a787ec0ac08c44fca1cbb2c664f53564581128779c65a8ddd1a8`; PDF-48 `ba56e9b7fff572af066706ddbe0d886f36eff0ecf8916227c1ff0ec7798a5870`; PDF-49 `c2dc25fc39a0782be735e723e5613eacf90562aadb4cfe00e51442cce056a7e8`.
- A licença Creative Commons exige crédito apropriado e não transfere ao usuário permissões sobre material de terceiros eventualmente excluído. Ver [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) e [considerações para reutilizadores](https://creativecommons.org/share-your-work/licensing-considerations/version4/).
- A lista `PUBLIC-PDF-TEST-APPROVALS-2026-11-22.json` define atualmente **29** PDFs. Ela exige CC BY **4.0 confirmada**, exclui registros `CC BY` sem versão, licenças NC e desconhecidas e declara expressamente que a revisão documental pela IA não atesta direitos de terceiros/edição exata. **Não modificar silenciosamente essa política**.

## Efeito da decisão e próximo passo

**FEITO:** autorização do mantenedor registrada como decisão interna para exatamente três PDFs, com identificação `rebsonm`. O mantenedor não precisa reiterar a mesma autorização interna se a edição e o escopo permanecerem os mesmos. **NÃO FEITO:** ampliação da allowlist, publicação de pacote com os três, alteração de licença/rights no catálogo, aprovação humana técnica/jurídica de direitos não examinados, envio de e-mail, merge, release ou alteração de gates. Os arquivos continuam disponíveis no repositório como antes e **não foram redistribuídos em novo pacote por este ato**.

**Responsáveis e condições ainda necessários:** RPQ — resposta editorial que elimine o conflito CC BY/NC; UFF — identificar licença aplicável à edição e fontes de material incorporado; BPSR — revisar exceções e créditos das figuras externas e a cópia específica. Após essas provas, o mantenedor/curadoria poderá decidir a implementação técnica (allowlist e build) com atribuição verificável. **PR #112 permanece Draft; release `NO_GO`.** Preservar Issues #102 e #103 e o teste T02 do host como restrições independentes.
