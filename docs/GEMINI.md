# Adapter — Gemini

Este documento descreve como usar **Meu Artigo** nos apps Gemini. A metodologia central continua em `meu-artigo/SKILL.md`.

## Compatibilidade verificada

Os apps Gemini aceitam Skills enviadas como:

- um arquivo `SKILL.md`;
- uma pasta contendo `SKILL.md` na raiz;
- um arquivo `.zip` contendo `SKILL.md` na raiz.

O Google também informa que Skills criadas em outras plataformas podem ser importadas por upload do `SKILL.md`.

Fontes oficiais:

- https://support.google.com/gemini/answer/17094296
- https://support.google.com/gemini/answer/18560919

Informações de plataforma podem mudar; estas instruções foram revisadas em 2026-10-06.

## Como preparar o upload

Não envie o ZIP do repositório inteiro se o `SKILL.md` ficar dentro de uma subpasta.

Use a pasta:

`meu-artigo/`

ou crie um ZIP cujo nível raiz seja:

```text
SKILL.md
references/
scripts/
agents/
```

O Gemini precisa encontrar `SKILL.md` na raiz da Skill enviada.

## Instalação

Na interface de Skills do Gemini:

1. escolha Upload;
2. selecione `SKILL.md`, a pasta `meu-artigo/` ou o ZIP preparado;
3. revise a Skill;
4. crie/salve;
5. inicie um chat com um problema de pesquisa inédito.

Prompt inicial sugerido:

> Use a Skill Meu Artigo. Meu problema de pesquisa é: [problema]. Quero construir o artigo com rastreabilidade e continuidade.

## Limitações importantes

Segundo a documentação atual do Gemini:

- scripts que exigem acesso à internet não são suportados dentro de Skills;
- ferramentas disponíveis podem variar em relação a Gems e outros modos do Gemini;
- o acesso direto a arquivos do GitHub como fonte da Skill não é a rota principal de importação.

Os scripts deste repositório são locais e determinísticos. Ainda assim, a execução efetiva depende da superfície e das permissões do Gemini.

## Integrações

Não tente reproduzir literalmente o manifesto `agents/openai.yaml`.

No Gemini, a Skill deve identificar os recursos disponíveis e mapear por papel:

- armazenamento persistente;
- descoberta acadêmica;
- verificação bibliográfica;
- web/publisher retrieval;
- bases indexadas;
- execução local quando disponível.

Se Google Drive/Workspace estiver conectado, ele é um bom candidato para reproduzir o workspace canônico, mas a disponibilidade depende da conta e da superfície utilizada.

## Scopus e Web of Science

A lógica é a mesma das demais plataformas:

1. gerar query e filtros;
2. executar por acesso institucional/navegador quando necessário;
3. exportar metadados;
4. entregar o arquivo à Skill;
5. validar e deduplicar;
6. registrar a rodada.

Nunca presumir acesso direto.

## Teste recomendado

O Gemini é especialmente útil no teste de portabilidade porque o `SKILL.md` pode ser importado de outra plataforma.

Avalie:

- a Skill reconheceu a estrutura e referências?
- ignorou corretamente o adapter OpenAI?
- conseguiu iniciar o workflow com apenas um problema de pesquisa?
- conseguiu criar uma persistência equivalente?
- respeitou limitações de ferramentas sem inventar resultados?
- continuou corretamente após nova conversa usando os artefatos persistidos?

## Regra

Quando uma função não existir no Gemini, registre a limitação e continue com alternativas metodologicamente válidas. Não enfraqueça o padrão científico para imitar uma automação inexistente.
