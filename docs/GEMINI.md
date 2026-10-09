# Adapter — Gemini

> Se você nunca usou GitHub, comece por [COMECE-AQUI.md](./COMECE-AQUI.md).

Este documento descreve como usar **Meu Artigo** nos apps Gemini. A metodologia central continua em `SKILL.md`.

## Antes de tentar instalar

O Google documenta o carregamento de Skills nos apps Gemini, mas a função depende dos requisitos da conta, da região, do produto e das condições atuais. Consulte as [instruções oficiais do Gemini](https://support.google.com/gemini/answer/17094296?hl=pt-BR).

A documentação informa que uma Skill pode ser importada por `SKILL.md`, pasta ou ZIP com `SKILL.md` na raiz. **Isso confirma o formato de upload, não a execução completa da Skill Meu Artigo**; a beta `v0.8.0-beta.8` ainda precisa ser testada em ambiente real.

## 1. Baixe a versão identificada

1. Abra [a Release v0.8.0-beta.8](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v0.8.0-beta.8).
2. Baixe **`MeuArtigoSkill-v0.8.0-beta.8.zip`**, em vez do ZIP automático de código-fonte.
3. Para conferir a integridade, use o `SHA256SUMS.txt` da mesma versão.

## 2. Instale no Gemini

Se o recurso de Skills estiver disponível em sua conta:

1. abra a página de Habilidades no Gemini;
2. escolha a opção de upload, conforme a interface exibida;
3. selecione o ZIP da Release, contendo `SKILL.md` na raiz;
4. confira o conteúdo importado e conclua a criação.

O Google informa restrições a scripts que exigem acesso à internet. A disponibilidade de funções, recursos de execução e conexões deve ser verificada antes de qualquer afirmação de compatibilidade com o fluxo completo.

## 3. Comece em uma conversa nova

> Use a Skill Meu Artigo. Meu problema de pesquisa é: [problema]. Quero construir o artigo com rastreabilidade, continuidade e gestão C.A.D.A.

## Formato de upload documentado pelo Google

O Google informa que Skills podem ser carregadas por:

- `SKILL.md`;
- pasta com `SKILL.md` na raiz;
- ZIP com `SKILL.md` na raiz.

Também informa que Skills criadas em outras plataformas podem ser importadas.

## Limitações importantes

Segundo a documentação atual do Gemini:

- scripts que exigem acesso à internet não são suportados dentro de Skills;
- ferramentas disponíveis podem variar em relação a Gems e outros modos;
- arquivos de referência precisam acompanhar a Skill no upload;
- importação direta do repositório GitHub não substitui o upload da Skill.

Os scripts deste repositório são locais e determinísticos. Ainda assim, a execução depende da superfície e das permissões do Gemini.

## Preflight específico do Gemini

A [documentação oficial](https://support.google.com/gemini/answer/17094296?hl=pt-BR)
registra que Skills estão em disponibilização gradual e que scripts
**que exigem internet** não são suportados dentro da Skill.
Arquivos binários como `.xlsx` não são aceitos como referência
nesse upload. Isso não proíbe a existência da planilha canônica
em Drive, mas exige que sua criação e edição por ferramentas externas
sejam realmente verificadas em vez de presumidas.

Antes de iniciar o projeto, confira
[preflight por capacidades](../references/platform-capability-preflight.md)
e use apenas integrações efetivamente disponíveis. Não relatar
scripts Python executados ou uploads concluídos sem recibo.

## Integrações

Não tente reproduzir literalmente `agents/openai.yaml`.

Mapeie os recursos disponíveis para:

- armazenamento persistente;
- descoberta acadêmica;
- verificação bibliográfica;
- web/publisher retrieval;
- bases indexadas;
- execução local quando disponível;
- gerenciador de trabalho para espelhar o C.A.D.A., quando houver integração disponível.

O Google Drive é o armazenamento canônico padrão da Skill. Confirme que a conexão existe e é gravável antes do trabalho substantivo. Caso não esteja disponível, solicite a conexão, verifique novamente e só prossiga com armazenamento alternativo após **autorização explícita** do pesquisador; não confunda a integração disponível na plataforma com sincronização realmente executada.

## Gestão C.A.D.A.

O C.A.D.A. continua funcionando mesmo sem integração com ClickUp, Jira ou Trello. Se o Gemini disponibilizar uma integração equivalente, use-a apenas como espelho operacional; preserve o workspace e `11_CADA_Control` como fontes canônicas.

## Scopus e Web of Science

1. gerar query e filtros;
2. executar por acesso institucional/navegador quando necessário;
3. exportar metadados;
4. entregar o arquivo à Skill;
5. validar e deduplicar;
6. registrar a rodada.

Nunca presumir acesso direto.

## Verificação funcional recomendada

Avalie:

- reconhecimento da estrutura e referências;
- independência do adapter OpenAI;
- início do workflow apenas com problema de pesquisa;
- persistência;
- transparência das limitações;
- retomada após nova conversa.

## Regra

Quando uma função não existir no Gemini, registre a limitação e continue com alternativas metodologicamente válidas. Não enfraqueça o padrão científico para imitar uma automação inexistente.
