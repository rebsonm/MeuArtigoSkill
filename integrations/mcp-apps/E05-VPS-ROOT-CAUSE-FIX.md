# E05 — correção de origem para autonomia na VPS (18/10/2026)

**Estado:** implementada e testada no repositório candidato, NÃO instalada no serviço real.

## Evidência e causa
- Na VPS o E05 foi atualizado para `3ed581f9...` e passou a pré-homologação; a unidade systemd ficou enabled/failed, status 1.
- O bootstrap original inicia com `--profile meu-artigo-e05`, mas o procedimento que funcionou anteriormente utilizou o caminho **explícito** `--profile-file /opt/meu-artigo-e05/tunnel-profiles/meu-artigo-e05.yaml`. Isso é divergência de contrato confirmada no fonte; não prova isoladamente toda a causa do status 1.
- Diagnósticos transitórios anteriores usaram origem errada de credenciais e/ou detecção textual; `control_plane_api_key=FAIL` naquele teste não demonstra chave revogada.

## Solução única no fonte
`e05-vps-runtime-launch.sh` é instalado pelo bootstrap como único launcher. Roda sob `meuartigo-e05`, lê somente a cópia protegida pela diretiva `LoadCredential` em `$CREDENTIALS_DIRECTORY`, executa `doctor --json` e `run` com **os mesmos argumentos** de perfil e de arquivo de chave. Não registra conteúdo bruto nem a chave; recusa configuração ausente com código 78. `RestartPreventExitStatus=78` impede ciclos de reinício com configuração inválida; outros erros mantêm reinício conforme política. Testes com credenciais e cliente fictícios cobrem PASS/FAIL e isolamento.

**Este é um reparo de código. Não substitui ativação e teste remoto.** Não pedir novamente ao usuário a execução de scripts sucessivos sem um canal operacional apropriado; a aplicação na unidade existente requer acesso remoto autorizado, inexistente nesta execução.

## Matriz C.A.D.A.
| Objeto | Responsável | Dependência | Estado |
| --- | --- | --- | --- |
| OPS-01 Git / OPS-02 código E05 | Operador | Histórico | **Concluídos na VPS** |
| OPS-03 chave e cliente | Operador | Histórico | Arquivos presentes, autenticação remota não provada |
| OPS-04 contrato launcher/systemd | Engenharia | CI SHA específico | **Corrigido no fonte; CI em validação** |
| OPS-05 processo E05 estável | Operador VPS autorizado | Aplicar atualização verificada | **Pendente na VPS** |
| R02 ChatGPT ALPHA/BRAVO e CSP | Testador | OPS-05 + host real | **Pendente** |
| R01 / R03–R10 | Revisor e mantenedor | Critérios específicos | **Pendentes** |

Plano original: D01–D15 com implementação técnica candidata; D16–D18 abertos; dez gates finais R01–R10 ainda **0/10** concluídos.

Referências: https://github.com/openai/tunnel-client/blob/master/docs/configuration.md ; https://github.com/openai/tunnel-client/blob/master/cmd/client/doctor_command.go ; https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html
