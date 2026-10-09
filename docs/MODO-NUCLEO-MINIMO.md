# Apresentação progressiva — núcleo mínimo e fluxo completo

O modo **núcleo mínimo** reduz a quantidade de informação operacional exibida ao pesquisador. **Não elimina registros, verificações, gates ou exigências de comprovação**: ambos os modos utilizam os mesmos arquivos e critérios científicos.

| Aspecto | Núcleo mínimo | Completo |
| --- | --- | --- |
| Conversa | Próxima providência, decisão e limitação relevante | Evidências, índices, registros e pendências detalhados |
| Triagem de artigos | Decisões críticas e divergências | Todos os registros consultáveis |
| Referências/claims | Somente riscos materiais e revisão requerida | Rastreamento detalhado por evidência |
| Revisão humana | Sempre requerida | Sempre requerida |
| Auditoria independente | Sem redução dos controles | Mesmos controles |
| Dados e IDs | Mesma base canônica | Mesma base canônica |

Novo projeto: `presentation_mode=MINIMAL`. Projetos antigos sem campo seguem `FULL` até decisão registrada de mudança. Escolha do modo diz respeito à **apresentação**, não ao tipo de revisão, escopo da pesquisa, autonomia para tomar decisões ou rigor da avaliação.

Com Python 3.10+ e arquivos do projeto:

```bash
python scripts/presentation_mode.py /projeto
python scripts/presentation_mode.py /projeto --mode FULL --confirmed-by "referência à solicitação explícita do pesquisador"
python scripts/presentation_mode.py /projeto --mode MINIMAL --confirmed-by "referência à solicitação explícita do pesquisador"
```

A alteração grava apenas as preferências no `PROJECT_CONFIG.json`, sem reescrever arquivos científicos, contagens, decisões ou evidências. O ator/texto declarados não autenticam automaticamente a identidade do pesquisador. Nem um log “bonito”, nem a conclusão de tarefas, nem a alternância entre modos demonstram qualidade científica.

A comparação empírica entre os dois modos é **prospectiva** e segue `benchmarks/minimal_full_comparison_protocol_v1.json`; não há usuários avaliados ou resultados coletados.
