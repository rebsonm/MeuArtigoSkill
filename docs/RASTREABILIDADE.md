# Rastreabilidade no Meu Artigo

## Ideia central

O Meu Artigo não busca apenas ajudar a produzir um manuscrito.

Ele busca permitir que o pesquisador consiga **reconstruir como o manuscrito foi produzido**.

Na era da IA, isso significa preservar a proveniência do processo:

- quais buscas foram executadas;
- quais arquivos foram usados;
- quais decisões metodológicas foram tomadas;
- o que foi alterado e por quê;
- onde a IA participou;
- qual ferramenta/modelo foi usado quando conhecido;
- como o pesquisador verificou o resultado;
- de quais evidências derivam as principais afirmações.

## Gestão não é rastreabilidade

O projeto separa duas funções:

### C.A.D.A. — gestão

Responde:

> Onde estamos, o que falta, quem é responsável, qual o prazo e o que comprova a conclusão?

### Rastreabilidade — proveniência científica

Responde:

> Como chegamos até aqui, que decisões construíram o artigo, com quais fontes/ferramentas e como foram verificadas?

Isso evita tentar usar uma simples lista de tarefas como registro metodológico.

## Três níveis de controle

### 1. Planilha C.A.D.A. — modo universal

Não exige Trello, Jira ou ClickUp.

A própria matriz-mestra funciona como gerenciador do projeto.

A aba `11_CADA_Control` permite acompanhar:

- etapa;
- responsável;
- próxima ação;
- prazo;
- status;
- prioridade;
- dependências;
- bloqueios;
- evidência de avanço;
- evidência de conclusão.

Esse é o **modo padrão e universal** de gestão.

### 2. Gerenciador externo — modo opcional

ClickUp, Jira/Atlassian e Trello podem espelhar o C.A.D.A. para quem já usa essas ferramentas.

O vínculo é registrado em `12_PM_Sync`.

O gerenciador externo nunca substitui a matriz científica.

### 3. Trilha de rastreabilidade — proveniência

A aba `13_Traceability_Log` registra eventos materiais do processo científico.

A aba `14_AI_Use_Log` registra especificamente usos de IA relevantes para transparência e eventual declaração editorial.

O arquivo `RASTREABILIDADE.md` mantém uma síntese legível da construção do projeto.

## O que fica rastreável

Um exemplo:

```text
Claim C-17
   ↓
Evidence E-31, E-48
   ↓
Records R-081, R-144
   ↓
Search S2-R1 / snowball SB-03
   ↓
TRACE-0118, TRACE-0121
   ↓
CADA-0054
   ↓
PROTOCOLO v3
```

Assim, uma afirmação importante pode ser ligada às evidências e ao processo que levou à sua incorporação no manuscrito.

## E a IA?

Para usos materiais de IA, a Skill procura registrar:

- plataforma/ferramenta;
- modelo/versão quando disponível;
- finalidade;
- etapa científica;
- tipo de entrada;
- tipo de saída;
- se o uso foi assistivo ou substantivo;
- como ocorreu a revisão humana;
- se o resultado foi aceito, alterado ou rejeitado;
- artefatos relacionados;
- necessidade de declaração editorial.

O objetivo não é salvar toda conversa ou todo prompt.

A regra é registrar **eventos materialmente relevantes à construção científica**.

## Transparência editorial

Essa arquitetura está alinhada com uma tendência editorial crescente de exigir transparência sobre o uso de IA em pesquisa.

A Revista de Ciências da Administração, por exemplo, determina que aplicações substantivas de IA sejam descritas nos métodos, com ferramenta, versão, finalidade e procedimentos de validação humana, para assegurar rastreabilidade.

Referência editorial pública:

- Diretrizes para uso de IA — Revista de Ciências da Administração: https://periodicos.ufsc.br/index.php/adm/Diretrizes_para_uso_de_IA

## Limites de atribuição

Fundamentos acadêmicos e editoriais devem estar ligados a fontes identificáveis e verificáveis. Afirmações atribuídas a palestras ou apresentações não documentadas não devem ser registradas como citações ou evidências confirmadas.

## Resultado esperado

Ao final de um projeto, deve ser possível responder:

> Como este artigo foi construído?

sem depender apenas da memória do autor ou do histórico de um chat.

Esse é o papel da camada de rastreabilidade do Meu Artigo.


## Interoperabilidade

A rastreabilidade também pode ser exportada em formatos padronizados:

- **W3C PROV-O** para representar entidades, atividades, agentes e relações de proveniência;
- **RO-Crate 1.3** para empacotar o objeto de pesquisa e seus metadados;
- **SHA-256** para verificar fixidade dos arquivos do pacote.

Isso é uma camada de exportação. O pesquisador não precisa conhecer esses padrões para usar o Meu Artigo.

Veja `../meu-artigo/references/provenance-export.md`.


## Decisão, responsabilidade e estado congelado

A rastreabilidade distingue:

- `DEC_ID`: por que uma escolha científica foi feita;
- `GATE_ID`: onde o pesquisador humano validou uma transição crítica;
- `SNAP_ID`: qual era o estado oficial do projeto naquele momento.

Isso permite reconstruir não apenas o que aconteceu, mas também decisões, responsabilidade humana e mudanças entre versões.
