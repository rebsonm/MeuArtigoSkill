# Comece aqui — usando o Meu Artigo pelo GitHub

## Status atual de acesso

O Meu Artigo está em **beta fechado**. O repositório está privado e este guia permanece documentado para a futura liberação de testes.

Enquanto o acesso não for aberto pelo autor, as instruções abaixo devem ser entendidas como o fluxo previsto para usuários autorizados/testadores futuros, e não como convite para distribuição pública.

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

Quando o repositório estiver público, normalmente não será necessária conta apenas para leitura/download. **Na fase atual, o repositório está privado e exige acesso autorizado.**

Você só precisaria de conta para ações como comentar, abrir uma Issue, favoritar o projeto ou colaborar diretamente no código.

Para testar a Skill, basta baixar os arquivos.

## 3. Como baixar

Na página principal do repositório:

1. procure o botão verde **Code**;
2. clique nele;
3. escolha **Download ZIP**;
4. salve o arquivo no computador.

**Se você vai instalar no ChatGPT, não precisa descompactar:** o procedimento validado é importar diretamente esse ZIP completo. Descompacte apenas se quiser inspecionar os arquivos ou usar outra plataforma.

Depois de descompactar, você verá algo parecido com:

```text
MeuArtigoSkill/
├── SKILL.md
├── agents/
├── references/
├── scripts/
├── docs/
└── README.md
```

A **raiz do repositório já é o bundle da Skill**. A pasta `docs/` contém guias de instalação e teste; `references/` e `scripts/` fazem parte do funcionamento da Skill.

## 4. Qual arquivo eu uso?

Na raiz do bundle, o arquivo principal é:

```text
SKILL.md
```

Ele contém as instruções centrais da Skill.

Quando sua IA permitir importar um **ZIP**, no ChatGPT prefira o ZIP completo baixado diretamente do GitHub, porque ele preserva a estrutura e os arquivos auxiliares. Ele contém:

- `references/` — regras metodológicas detalhadas;
- `scripts/` — rotinas auxiliares;
- `agents/` — configuração específica de algumas plataformas.

## 5. Escolha sua IA

Depois de baixar, siga o guia correspondente. **A opção de instalar Skills depende do plano/conta de cada plataforma**, então leia o início do guia antes de procurar os menus:

- [Quero usar no ChatGPT / Codex](./CHATGPT.md)
- [Quero usar no Claude](./CLAUDE.md)
- [Quero usar no Gemini](./GEMINI.md)

As três usam o mesmo núcleo metodológico. O que muda é a forma de instalar e quais integrações cada plataforma consegue acessar.

## 6. Como começar a usar

No ChatGPT, importe o ZIP completo em **Plugins → Habilidades → Criar/Carregar do computador**. Depois de instalar/importar a Skill na sua IA, abra uma conversa nova e escreva algo como:

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

## 7. Primeira utilização

Para experimentar o funcionamento normal da Skill:

- comece com um problema ou ideia real de pesquisa;
- não é necessário ler o `SKILL.md` antes de usar;
- não é necessário conhecer previamente o fluxo interno;
- deixe a própria Skill orientar as etapas e pergunte sempre que algo não estiver claro.

Use como usaria uma ferramenta real.

Se algo ficar confuso ou parecer metodologicamente inadequado, você pode registrar o ponto e, se desejar, encaminhá-lo como sugestão livre ao autor.

## 8. Como verificar a continuidade do seu próprio projeto

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
usar a pasta raiz descompactada
   ↓
seguir o guia da sua IA
   ↓
informar seu problema de pesquisa
```

## 12. Quero enviar uma sugestão ou relatar um problema

Não existe formulário, escala de percepção ou protocolo de avaliação de usuários no projeto.

Se quiser contribuir, envie livremente uma observação, crítica metodológica, relato de erro ou sugestão de melhoria. Não há roteiro obrigatório nem coleta padronizada de respostas.

## 13. Quero entender o projeto por dentro

Depois da primeira utilização, fique à vontade para explorar:

- [CADA.md](./CADA.md) — como funciona a gestão do passo a passo;
- [MATRIZ-CADA.md](./MATRIZ-CADA.md) — como funciona o painel/planilha oficial;
- [RASTREABILIDADE.md](./RASTREABILIDADE.md) — como o processo de construção do artigo fica auditável;
- [GOVERNANCA-CIENTIFICA.md](./GOVERNANCA-CIENTIFICA.md) — como decisões, validação humana e snapshots funcionam;
- [JOURNAL-AWARE.md](./JOURNAL-AWARE.md) — como a revista-alvo orienta a construção desde o início;
- [ROBUSTEZ-CLAIMS.md](./ROBUSTEZ-CLAIMS.md) — como claims importantes são confrontados antes de congelar;
- [MAPA-CORPUS.md](./MAPA-CORPUS.md) — como funciona o mapa do corpus e a consulta grounded;
- `../SKILL.md` — instrução central;
- `../references/` — metodologia detalhada;
- `../scripts/` — automações determinísticas;

