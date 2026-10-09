# Comece aqui — usando o Meu Artigo pelo GitHub

## Status atual de acesso

O Meu Artigo está em **versão beta pública**. O repositório, o código e a documentação podem ser acessados sem convite. A Skill permanece em desenvolvimento e seu uso deve respeitar os limites científicos documentados.

A beta pode ser consultada e instalada publicamente. Isso não autoriza a redistribuição de PDFs científicos de terceiros nem significa que a qualidade científica da Skill tenha sido validada empiricamente.

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

O repositório é público: não é necessária conta GitHub para consultar os arquivos ou obter um ZIP do código. Instalar, conectar plataformas e autorizar acesso a dados privados são operações separadas.

Você só precisaria de conta para ações como comentar, abrir uma Issue, favoritar o projeto ou colaborar diretamente no código.

Para testar a Skill, basta baixar os arquivos.

## 3. Como baixar

**Preferência: versão identificada.** Abra [Releases](https://github.com/rebsonm/MeuArtigoSkill/releases/tag/v0.8.0-beta.6), baixe `MeuArtigoSkill-v0.8.0-beta.6.zip` e, se desejar, confira o hash no `SHA256SUMS.txt`. Diferentemente do ZIP de código-fonte, esse pacote é preparado especificamente para instalar a Skill, com manifesto e licença. Consulte [implantação beta](IMPLANTACAO-BETA.md).

**Alternativa para consultar o código do projeto:** o botão **Code → Download ZIP** obtém uma cópia do repositório, que pode não corresponder a uma versão publicada. **Para instalar, prefira sempre o ZIP preparado em Releases.**

**No ChatGPT, quando houver suporte a Skills, utilize o upload do ZIP instalável completo:** a interface documenta esse recurso, mas a beta atual ainda precisa de teste funcional específico. Descompacte apenas se quiser inspecionar os arquivos ou usar outra plataforma.

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

O **ZIP de Releases é o pacote instalável recomendado**; o repositório também contém o código-fonte e o histórico de desenvolvimento. A pasta `docs/` contém guias de instalação e teste; `references/` e `scripts/` fazem parte do funcionamento da Skill.

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

As três usam o mesmo núcleo metodológico, mas as funções disponíveis e os mecanismos de instalação podem variar. A [matriz de compatibilidade](COMPATIBILIDADE-PLATAFORMAS.md) distingue o suporte anunciado pelos fornecedores dos testes ainda pendentes da Skill.

## 6. Como começar a usar

Se a sua conta oferecer Skills, no ChatGPT use **Plugins → Habilidades → Criar → Carregar do computador** para importar o ZIP completo. Depois de instalar/importar a Skill na sua IA, abra uma conversa nova e escreva algo como:

> Use a Skill Meu Artigo. Meu problema de pesquisa é: [descreva seu problema]. Quero desenvolver um artigo científico.

Logo no início, a Skill deve primeiro verificar o Google Drive. Se ele não estiver conectado, ela deve orientar a conexão e verificar novamente. Se ainda assim não houver acesso, ela deve perguntar claramente se você deseja continuar sem Drive usando apenas arquivos/resultados do Work ou armazenamento local. Ela só pode adotar esse fallback após sua confirmação afirmativa.

Depois de resolver a persistência, a Skill também deve perguntar se você já possui **revista-alvo**. Se possuir, tenha à mão o link/arquivo das normas para autores e, se existir, o template/layout da revista. Se ainda não tiver revista definida, isso não impede o início do projeto.

Você não precisa preparar:

- string booleana;
- planilha;
- protocolo;
- revisão;
- pasta no Drive — a Skill cria/retoma a estrutura depois de confirmar a conexão;
- critérios de inclusão;
- matriz de evidências.

A Skill deve ajudar a construir isso a partir do problema de pesquisa e mostrar o passo a passo por meio da gestão **C.A.D.A.**.

Quando gerar arquivos para enviar a revista, avaliador ou terceiro, a Skill também deve aplicar a política de anonimização. O padrão para arquivos externos é não expor identidade desnecessariamente e auditar o arquivo final, inclusive metadados ocultos. Veja [ANONIMIZACAO.md](./ANONIMIZACAO.md).

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

1. consultar a [lista de Releases](https://github.com/rebsonm/MeuArtigoSkill/releases);
2. baixar o ZIP **instalável** da versão identificada mais recente;
3. conferir a integridade quando necessário e atualizar a Skill pela função da sua plataforma, preservando os arquivos e decisões do projeto.

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
GitHub → Releases
   ↓
baixar MeuArtigoSkill-v0.8.0-beta.6.zip
   ↓
seguir o guia da sua IA
   ↓
fazer o upload ou descompactar, conforme a plataforma
   ↓
informar seu problema de pesquisa
```

## 12. Quero enviar uma sugestão ou relatar um problema

Existe um [protocolo preparado para avaliação futura com usuários](PROTOCOLO-BETA-USUARIOS.md), **ainda não executado**. Não há coleta de opiniões, sessões agendadas nem resultados de participantes neste momento.

Se desejar, você pode encaminhar espontaneamente uma observação, crítica metodológica, relato de erro ou sugestão de melhoria. **Esse envio livre não constitui participação em um estudo estruturado.** Para orientações de contribuição, consulte [CONTRIBUTING.md](../CONTRIBUTING.md) e não divulgue dados sensíveis em Issues públicas.

## 13. Quero entender o projeto por dentro

Depois da primeira utilização, fique à vontade para explorar:

- [CADA.md](./CADA.md) — como funciona a gestão do passo a passo;
- [MATRIZ-CADA.md](./MATRIZ-CADA.md) — como funciona o painel/planilha oficial;
- [RASTREABILIDADE.md](./RASTREABILIDADE.md) — como o processo de construção do artigo fica auditável;
- [GOVERNANCA-CIENTIFICA.md](./GOVERNANCA-CIENTIFICA.md) — como decisões, validação humana e snapshots funcionam;
- [JOURNAL-AWARE.md](./JOURNAL-AWARE.md) — como a revista-alvo orienta a construção desde o início;
- [ROBUSTEZ-CLAIMS.md](./ROBUSTEZ-CLAIMS.md) — como claims importantes são confrontados antes de congelar;
- [ANONIMIZACAO.md](./ANONIMIZACAO.md) — como arquivos externos são anonimizados e auditados antes de compartilhar/submeter;
- [MAPA-CORPUS.md](./MAPA-CORPUS.md) — como funciona o mapa do corpus e a consulta grounded;
- `../SKILL.md` — instrução central;
- `../references/` — metodologia detalhada;
- `../scripts/` — automações determinísticas;

