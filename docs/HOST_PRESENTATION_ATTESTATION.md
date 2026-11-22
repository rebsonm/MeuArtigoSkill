# Homologação T02 — bytes de origem vs. apresentação gerenciada pelo ChatGPT

O pacote RC.1 contém `BUNDLE_MANIFEST.json` imutável. A plataforma pode
regravar **somente** dois arquivos de apresentação ao instalar/salvar:

- `agents/openai.yaml` — reserialização e política adicionada pelo host
- `assets/icon.svg` — substituição pelo ícone padrão do host

Essa alteração de superfície não demonstra, por si, adulteração; tampouco deve
ser ignorada ou usada para reescrever hashes de origem.

## Regra de aceite

**Modo padrão:** `verify_installed_bundle.py` continua estrito: todo payload
deve coincidir com seu SHA-256 original. Qualquer diferença é `FAIL`.

**Modo de apresentação atestada:** é permitido declarar `PASS` com
`integrity_mode=CORE_EXACT_HOST_PRESENTATION_ATTESTED` **somente se**:

1. `VERSION`, versão do manifesto e build forem os esperados.
2. O SHA-256 do manifesto instalado coincidir com um SHA-256 **obtido
   independentemente do ZIP de release testado**, e fornecido via CLI.
3. **Todos** os demais payloads, scripts e referências coincidirem byte a byte.
4. Os **únicos** hashes divergentes forem os dois nomes permitidos acima.
5. Houver um recibo externo à instalação, explicitamente revisado por operador
   responsável, contendo SHA-256 original, SHA-256 pós-salvamento, identificação
   do host ChatGPT, evidência de salvamento/readback e exame do conteúdo
   transformado. O recibo deve corresponder **exatamente** aos bytes atuais.
6. O ícone SVG efetivo passar na verificação XML de elementos/atributos
   potencialmente executáveis. YAML precisa ser UTF-8 e conter a interface.
7. O recibo **não** certificar a integridade científica, aprovação de gates,
   existência de direitos autorais ou identidade criptográfica do operador.

O recibo é uma **atestação auditável de revisão humana de bytes observados**,
não uma assinatura criptográfica do ChatGPT. Em instalações de maior risco,
exija assinatura externa e validação independente; sem isso, permaneça NO-GO.

## Procedimento seguro

1. Baixe o ZIP da CI do **mesmo SHA da PR** e confirme sua origem.
2. Em um terminal fora da Skill, obtenha o SHA do manifesto original do ZIP:

   `python -c "import hashlib,zipfile; z=zipfile.ZipFile('MeuArtigoSkill-v1.0.0-rc.1.zip'); print(hashlib.sha256(z.read('BUNDLE_MANIFEST.json')).hexdigest())"`

3. Instale/salve a Skill, então use o diretório *efetivamente instalado*:

   `python scripts/verify_installed_bundle.py --root /CAMINHO/INSTALADO`

   Se a plataforma transformou os dois arquivos, o modo estrito **deve falhar**
   e exibir os nomes divergentes.

4. Gere **apenas um rascunho**, sem aprovar nada:

   `python scripts/verify_installed_bundle.py --root /CAMINHO/INSTALADO --emit-host-receipt-draft > /AREA_SEGURA/recibo-host.json`

   A opção retorna código 2 deliberadamente; o rascunho contém `reviewed=false`.

5. Inspecione o YAML e o SVG **efetivamente salvos**, compare com os
   originais, verifique campos de instrução/política, detecte instruções
   suspeitas, identifique a transformação do host e examine o resultado da
   instalação recuperada. Não use uma simples declaração da IA como revisão
   independente. Registre **reviewer**, **review_evidence** (mínimo 30 caracteres)
   e **host_save_readback_evidence** (mínimo 20 caracteres), e só então marque
   `reviewed=true` no recibo **e em cada entrada transformada**.

6. Execute:

   `python scripts/verify_installed_bundle.py --root /CAMINHO/INSTALADO --expected-version 1.0.0-rc.1 --expected-manifest-sha256 HASH_DO_PASSO_2 --host-receipt /AREA_SEGURA/recibo-host.json`

7. O único aceite válido é `status=PASS` acompanhado de
   `integrity_mode=CORE_EXACT_HOST_PRESENTATION_ATTESTED` e indicação explícita
   dos nomes reescritos. Preserve o recibo e o hash de seu conteúdo fora da
   Skill, sem incluir informações privadas em PRs públicos.

**Falha obrigatória:** qualquer arquivo adicional divergente, recibo
incompleto/alterado, manifesto diferente, host desconhecido, XML potencialmente
executável, versão beta ou mudança posterior ao recibo.

## Outros critérios

- T06/XLSX: na ausência de `artifact_tool`, CSVs devem permanecer usáveis e
  a dependência visual documentada como bloqueio opcional.
- T05/T33/T32/T34 devem manter seus próprios ensaios e evidências; um
  recibo de apresentação não substitui esses testes.
- Nunca forçar release, merge, aprovação de gates ou manipulação de PDFs para
  obter um `PASS`.
