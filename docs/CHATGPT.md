# Adapter — ChatGPT / Codex

Este documento descreve como usar **Meu Artigo** em ambientes OpenAI. A metodologia central continua em `meu-artigo/SKILL.md`.

## Compatibilidade

A pasta `meu-artigo/` segue o formato de Skill com:

- `SKILL.md`;
- arquivos em `references/`;
- scripts determinísticos em `scripts/`;
- configuração específica OpenAI em `agents/openai.yaml`.

O arquivo `agents/openai.yaml` é um **adapter da plataforma**, não parte da metodologia científica.

## Instalação

Importe/adicione a pasta `meu-artigo/` como Skill no ambiente OpenAI que suporte Skills.

Prompt inicial sugerido:

> Use `$meu-artigo`. Meu problema de pesquisa é: [problema]. Quero desenvolver um artigo científico e ainda não defini a revista.

## Integrações preferenciais

O manifesto OpenAI declara como dependências preferenciais:

- Google Drive;
- Consensus;
- Scite;
- Firecrawl.

Essas integrações aceleram o fluxo, mas a metodologia deve continuar quando alguma não estiver disponível, usando recursos equivalentes.

A instalação/conexão de uma integração de terceiros exige ação explícita do usuário. A Skill deve apresentar a conexão e continuar automaticamente após a autorização.

## Papel das integrações

### Google Drive
Referência principal para:

- workspace persistente;
- `CONTINUIDADE.md`;
- protocolo;
- matriz-mestra;
- PDFs;
- exports brutos;
- manuscrito;
- arquivos de submissão.

### Consensus
Preferido para:

- descoberta inicial;
- calibração de termos;
- auditoria de novidade;
- identificação de literatura próxima.

Não deve ser tratado como base bibliográfica exaustiva.

### Scite
Preferido para:

- contexto de citação;
- grafo de citações;
- verificação bibliográfica;
- apoio à leitura quando full text estiver legitimamente disponível.

### Firecrawl / web
Preferido para:

- páginas de periódicos;
- editoras;
- repositórios;
- documentação oficial;
- normas;
- instruções de submissão.

## Scopus e Web of Science

Não presumir connector direto.

Quando necessárias:

1. gerar a string exata;
2. executar via navegador autorizado ou orientar o usuário;
3. especificar os campos do export;
4. validar o arquivo recebido;
5. registrar a rodada na matriz.

## Teste recomendado

Para avaliar se a Skill funciona sem o contexto de desenvolvimento:

1. iniciar um chat novo;
2. ativar/importar apenas a Skill;
3. fornecer um problema de pesquisa inédito;
4. não explicar ao modelo como o fluxo deveria funcionar;
5. observar se ele cria/propõe o workspace, faz preflight de integrações, inicia auditoria de novidade e registra estado;
6. interromper o projeto;
7. abrir outro chat e verificar se `CONTINUIDADE.md` e a matriz permitem a retomada.

## Regra de portabilidade

Se uma capacidade específica da OpenAI não estiver disponível, seguir os papéis definidos em `SKILL.md` e usar um equivalente. Nunca transformar indisponibilidade de ferramenta em ausência de evidência.
