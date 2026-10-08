# Adapter — Gemini

> Se você nunca usou GitHub, comece por [COMECE-AQUI.md](./COMECE-AQUI.md).

Este documento descreve como usar **Meu Artigo** nos apps Gemini. A metodologia central continua em `SKILL.md`.

## Antes de tentar instalar

Segundo a documentação oficial atual do Google, o gerenciamento completo de Skills fica no **web app do Gemini**. A disponibilidade depende dos requisitos atuais da conta; a documentação informa, entre outros requisitos, conta Google pessoal elegível e assinatura Google AI compatível.

Se a opção **Skills / Habilidades** não aparecer, confira a disponibilidade da sua conta antes de concluir que houve erro no arquivo.

Fontes oficiais:

- https://support.google.com/gemini/answer/17094296
- https://support.google.com/gemini/answer/18560919

Informações de plataforma podem mudar; estas instruções foram revisadas em 2026-10-06.

## 1. Baixe pelo GitHub

Na página do repositório:

1. clique em **Code**;
2. clique em **Download ZIP**;
3. descompacte;
4. entre na pasta descompactada; a raiz já é o bundle da Skill.

## 2. Instale no Gemini

No web app do Gemini:

1. abra a página **Skills / Habilidades**;
2. escolha **Upload / Fazer upload**;
3. selecione a pasta raiz, o arquivo `SKILL.md` ou o ZIP preparado;
4. revise a Skill;
5. clique em **Criar**.

O Gemini aceita uma pasta ou ZIP quando `SKILL.md` está na pasta principal da Skill.

O repositório foi estruturado para que `SKILL.md` fique diretamente na raiz do bundle, junto de `references/`, `scripts/` e `agents/`.

## 3. Comece em uma conversa nova

> Use a Skill Meu Artigo. Meu problema de pesquisa é: [problema]. Quero construir o artigo com rastreabilidade, continuidade e gestão C.A.D.A.

## Compatibilidade verificada

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

Se Google Drive/Workspace estiver conectado, ele é um bom candidato para o workspace canônico, conforme a conta e a superfície utilizadas.

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
