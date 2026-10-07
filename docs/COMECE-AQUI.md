# Comece aqui — usando o Meu Artigo pelo GitHub

Este guia foi escrito para pesquisadores que **nunca usaram Git ou GitHub**, mas querem testar a Skill sem depender de alguém para instalar por eles.

Você não precisa saber programação. Também não precisa instalar Git, abrir terminal, criar branch ou fazer commit para usar a Skill.

## 1. O que é esta página?

Você está em um **repositório do GitHub**.

Um repositório é simplesmente uma pasta de projeto publicada na internet, com histórico de versões. Neste caso, ele contém:

- a Skill `Meu Artigo`;
- instruções de uso;
- referências metodológicas;
- pequenos scripts auxiliares;
- documentação para ChatGPT, Claude e Gemini.

O arquivo que aparece automaticamente na página inicial chama-se `README.md`. Ele funciona como a página de apresentação do projeto.

## 2. Preciso criar conta no GitHub?

Para **ler e baixar um repositório público**, normalmente não.

Você só precisaria de conta para ações como comentar, abrir uma Issue, favoritar o projeto ou colaborar diretamente no código.

Para testar a Skill, basta baixar os arquivos.

## 3. Como baixar

Na página principal do repositório:

1. procure o botão verde **Code**;
2. clique nele;
3. escolha **Download ZIP**;
4. salve o arquivo no computador;
5. extraia/descompacte o ZIP.

Depois de descompactar, você verá algo parecido com:

```text
MeuArtigoSkill/
├── README.md
├── docs/
└── meu-artigo/
```

A pasta que contém a Skill propriamente dita é:

```text
meu-artigo/
```

Não confunda com a pasta `docs/`, que contém apenas os guias de instalação e teste.

## 4. Qual arquivo eu uso?

Dentro de `meu-artigo/`, o arquivo principal é:

```text
SKILL.md
```

Ele contém as instruções centrais da Skill.

Mas, quando sua IA permitir importar uma **pasta ou ZIP**, prefira fornecer a pasta `meu-artigo/` inteira, porque ela também contém:

- `references/` — regras metodológicas detalhadas;
- `scripts/` — rotinas auxiliares;
- `agents/` — configuração específica de algumas plataformas.

## 5. Escolha sua IA

Depois de baixar, siga o guia correspondente. **A opção de instalar Skills depende do plano/conta de cada plataforma**, então leia o início do guia antes de procurar os menus:

- [Quero usar no ChatGPT / Codex](./CHATGPT.md)
- [Quero usar no Claude](./CLAUDE.md)
- [Quero usar no Gemini](./GEMINI.md)

As três usam o mesmo núcleo metodológico. O que muda é a forma de instalar e quais integrações cada plataforma consegue acessar.

## 6. Como começar o teste

Depois de instalar/importar a Skill na sua IA, abra uma conversa nova e escreva algo como:

> Use a Skill Meu Artigo. Meu problema de pesquisa é: [descreva seu problema]. Quero desenvolver um artigo científico.

Logo no início, a Skill também deve perguntar se você já possui **revista-alvo**. Se possuir, tenha à mão o link/arquivo das normas para autores e, se existir, o template/layout da revista. Se ainda não tiver revista definida, isso não impede o início do projeto.

Você não precisa preparar:

- string booleana;
- planilha;
- protocolo;
- revisão;
- pasta no Drive;
- critérios de inclusão;
- matriz de evidências.

A Skill deve ajudar a construir isso a partir do problema de pesquisa e mostrar o passo a passo por meio da gestão **C.A.D.A.**.

Você **não precisa conhecer ClickUp, Jira ou Trello**. A planilha/matriz do projeto já funciona como gerenciador completo no modo `MATRIX_ONLY`, com um painel visual próprio. Se você já usa alguma ferramenta de gestão e sua IA tiver essa integração, pode optar pelo modo `MATRIX_PLUS_EXTERNAL`.

Além de acompanhar tarefas, a Skill também mantém uma trilha de **rastreabilidade da construção do artigo**, registrando decisões materiais, alterações, fontes, uso de IA e validações humanas.

## 7. O que NÃO fazer no primeiro teste

Para conseguirmos avaliar se a Skill é realmente autoexplicativa:

- não leia o `SKILL.md` antes da primeira tentativa;
- não tente adivinhar o fluxo que o criador espera;
- não ensine a IA a usar a Skill;
- não adapte seu comportamento para “ajudar o teste”.

Use como usaria uma ferramenta real.

Se algo ficar confuso, isso é um resultado importante do teste.

## 8. Teste de continuidade

Depois que o trabalho avançar um pouco:

1. encerre aquela conversa;
2. abra uma conversa nova;
3. disponibilize a Skill novamente;
4. disponibilize os arquivos persistidos do projeto, quando necessário;
5. escreva apenas:

> Continue meu artigo.

A Skill deve conseguir recuperar o estado a partir de `CONTINUIDADE.md`, protocolo, matriz e demais artefatos, sem exigir que você conte toda a história novamente.

## 9. Quero atualizar para a versão mais recente

Como você está usando a versão baixada do GitHub, a forma mais simples é:

1. voltar à página do repositório;
2. clicar em **Code → Download ZIP** novamente;
3. substituir a cópia antiga pela nova.

O GitHub mantém todo o histórico de alterações, portanto versões anteriores não desaparecem do projeto.

## 10. Vocabulário mínimo do GitHub

Você não precisa dominar estes termos para usar a Skill, mas eles ajudam a entender a página:

| Termo | Significado prático |
|---|---|
| **Repository / repositório** | A pasta completa do projeto publicada no GitHub |
| **README** | O texto de apresentação que aparece na página inicial |
| **main** | A versão principal/atual do projeto |
| **Code** | Botão onde você encontra a opção de baixar o projeto |
| **Download ZIP** | Baixa uma cópia do projeto sem precisar usar Git |
| **commit** | Um registro de uma alteração feita no projeto |
| **branch** | Uma linha paralela de desenvolvimento; você não precisa usar para testar |
| **clone** | Baixar o projeto usando Git; também não é necessário para o teste |
| **Issue** | Espaço do GitHub para relatar problema, sugestão ou discussão |
| **release** | Uma versão publicada formalmente, quando o projeto utiliza esse recurso |

## 11. Quero apenas testar, não aprender Git

Perfeito.

Seu caminho é simplesmente:

```text
GitHub
   ↓
Code
   ↓
Download ZIP
   ↓
Descompactar
   ↓
abrir a pasta meu-artigo/
   ↓
seguir o guia da sua IA
   ↓
informar seu problema de pesquisa
```

## 12. Quero ajudar com feedback

Use o [protocolo de teste](./TESTE-DE-USABILIDADE.md).

Você não precisa preencher tudo durante o uso. O mais importante é registrar:

- onde ficou confuso;
- o que a IA pediu sem necessidade;
- o que ela deveria ter feito automaticamente;
- se inventou alguma informação;
- se conseguiu retomar em outro chat;
- o que funcionou muito bem.

## 13. Quero entender o projeto por dentro

Depois do primeiro teste, fique à vontade para explorar:

- [CADA.md](./CADA.md) — como funciona a gestão do passo a passo;
- [MATRIZ-CADA.md](./MATRIZ-CADA.md) — como funciona o painel/planilha oficial;
- [RASTREABILIDADE.md](./RASTREABILIDADE.md) — como o processo de construção do artigo fica auditável;
- [GOVERNANCA-CIENTIFICA.md](./GOVERNANCA-CIENTIFICA.md) — como decisões, validação humana e snapshots funcionam;
- [JOURNAL-AWARE.md](./JOURNAL-AWARE.md) — como a revista-alvo orienta a construção desde o início;
- [ROBUSTEZ-CLAIMS.md](./ROBUSTEZ-CLAIMS.md) — como claims importantes são confrontados antes de congelar;
- [MAPA-CORPUS.md](./MAPA-CORPUS.md) — como funciona o mapa do corpus e a consulta grounded;
- `../meu-artigo/SKILL.md` — instrução central;
- `../meu-artigo/references/` — metodologia detalhada;
- `../meu-artigo/scripts/` — automações determinísticas;
- `TESTE-DE-USABILIDADE.md` — desenho da avaliação com usuários.

O objetivo não é esconder o funcionamento, mas evitar que conhecer o mecanismo antes da primeira tentativa influencie o teste.
