<!-- section: chapter -->
# 8. Estrutura recomendada do repositório

Adiciona estes ficheiros ou pastas à raiz, mantendo **un apenas lugar da verdade** :

```text
AGENTS.md                       # Fonte compartilhada, breve e versionada
CLAUDE.md                       # Opcional: importa @AGENTS.md + regras específicas do Claude
GEMINI.md                       # Referência a AGENTS.md ou link simbólico, conforme a ferramenta
.github/copilot-instructions.md # Regras de revisão ou de agente de codificação do GitHub Copilot, se usado
.github/instructions/           # Regras do Copilot específicas por caminho, se necessário
.aiignore                       # Exclusões da IA: segredos, artefatos grandes, arquivos gerados
.claude/rules/scala.md          # Regras do Claude específicas por caminho ou escopo, se úteis
.claude/rules/testing.md
.claude/rules/security.md
stryker4s.conf                  # Testes de mutação
docs/architecture.md
docs/testing.md
docs/review-checklist.md
docs/scala-style.md
scripts/ai-test-changed
scripts/ai-lint-changed
scripts/ai-diff-context
scripts/ai-rules-drift
```

O objetivo não é acumular documentação, mas evitar que o agente redescubra as mesmas regras em cada sessão. O arquivo deve permanecer curto, estável e operacional.

> ** Sincronização de ficheiros de contexto:** Codex carga as instruções globais de `CODEX_HOME`, depois
> os ficheiros da localização do projecto desde a raiz da pasta actual. Em cada nível,
> `AGENTS.override.md` prima sobre `AGENTS.md` ; as instruções mais próximas à pasta de trabalho
> Os nomes de fallback e o tamanho máximo dependem da configuração.
>
> Claude Code, com o Mod integrado `cc-plugin-agents-md`, utiliza por defeito `claude-md-or-agents-md` :
> `AGENTS.md` está carregado se nenhum `CLAUDE.md`, `.claude/CLAUDE.md` ou `CLAUDE.local.md` não existe no
> Pasta actual ou os seus pais. As instruções de utilizador/administradas e `.claude/rules/` continuam.
> `AGENTS.override.md` não é lido por Claude através deste fallback.
> `claude-md-and-agents-md` carrega ambas sem duplicar um ficheiro já importado. O erro pode ser.
> Não disponível em algumas superfícies; não substitui um importador explícito quando necessário.
>
> Para este workflow misto, prefere-se um `AGENTS.md` comum, e se `CLAUDE.md` Existe, começa com
> `@AGENTS.md`. Em seguida, mantenha apenas as regras realmente específicas de Claude. Verifica as instruções.
> carregadas num novo período de sessões (`/context all` Claude, e perguntar a Codex listar arquivos
> para sub-componentes, verifica também a descoberta da pasta real
> nenhum override pode enfraquecer uma regra de segurança externa.

A saber lado Claude Code : **rules** em `.claude/rules/` permite completar as instruções de projeto com instruções mais específicas, por exemplo, por subarborescência ou tipo de tarefa. Muitas vezes é melhor do que um enorme `CLAUDE.md` global quando este ficheiro existe.

Ou seja, também: o **auto-memory** Claude Code requer uma versão recente, documentada desde v2.1.59+. As primeiras linhas de `MEMORY.md` podem ser carregadas automaticamente, e os subagentes podem ter sua própria memória. Use esta memória para lembretes de patterns recorrentes, não para segredos, não para decisões de arquitetura não revisadas, e não como substituto da documentação versionada.

<!-- section: s-1 -->
## Conteúdo mínimo de `AGENTS.md`

```text
Comandos exatos de build, testes e formatação
Limites arquiteturais e invariantes de negócio pouco evidentes
Restrições de API pública, JSON e migração
Arquivos protegidos e escopo de escrita permitido
Convenções Scala ausentes na documentação atual
Condições de parada e definição de pronto
Referências à documentação e à especificação relevantes
```

Escreva estas regras ** para o agente, não como documentação humana** : prefere rotas, comandos, números e condições verificáveis. Grava algumas centenas de palavras como ponto de partida. README, tutoriais, lista exaustiva dos módulos e comparações de modelos permanecem em `docs/`, carregados a pedido.

<!-- section: s-2 -->
### Localização na configuração do utilizador

Conserva a matriz da secção 3 num documento de roteamento ou perfis de usuário Codex/Claude em vez de cada `AGENTS.md` : o depósito deve continuar a ser independente do modelo. Se uma orquestra deve consultar esta matriz, adiciona apenas um ponteiro a ela. As limitações de trabalho e segurança não mudam de acordo com o modelo.

<!-- section: s-3 -->
## Conteúdo mínimo de `CLAUDE.md`

```text
@AGENTS.md

## Claude Code
Use o modo de planejamento para mudanças arriscadas em vários arquivos.
```

Move as regras comuns do antigo `CLAUDE.md` para `AGENTS.md` (sem duplicação). O modo plano Claude é uma preferência de arness; as autorizações eficazes permanecem na configuração e no sandbox.

<!-- section: s-4 -->
## Por que conservar `AGENTS.md`

Com Codex e o Mod integrado `cc-plugin-agents-md` de Claude Code (fallback) `AGENTS.md` por omissão), `AGENTS.md` Os trabalhos recentes sobre os agentes de codificação indicam que um ficheiro de instruções deste tipo pode reduzir o tempo de execução e os tokens de saída mantendo ao mesmo tempo uma taxa de completação comparável. O efeito prático esperado é simples: menos contexto repetido, menos instruções esquecidas, menos deriva entre ferramentas.

> ** Estado dos testes: resultado misto, não benefício automático.** Outra avaliação de 2026 observa que os arquivos
> contexto geralmente reduz ligeiramente a taxa de sucesso e aumentam o custo em mais de 20 %, especialmente quando
> repetem o README ou adicionam requisitos desnecessários. Os ficheiros escritos pelos seguradores fazem melhor do que os '
> Gerados automaticamente, mas também devem ser medidos.
>
> Regra corrigida: `AGENTS.md` deve conter apenas o que muda efectivamente uma acção.
> Invariantes não evidentes, arquivos proibidos, convenções ausentes do README e regras de parada. Não há visitas guiadas
> narrativa do depósito, sem catálogo de tecnologias, sem conselhos genéricos. Compare regularmente uma amostra
> de tarefas com e sem o ficheiro.
> a mesma literatura: permanecer sob **~500 palavras**, centrado nas normas de prova, nas convenções de estilo e nas
> avisos de risco de não visita guiada do repositório e releir o ficheiro como código para cada revisão.

<!-- section: s-5 -->
#### Protocolo de validação: medir a eficácia de AGENTS.md

Um crack.md que não muda nada no resultado é o contexto morto que custa tokens em cada sessão. Protocolo de validação trimestral:

**Test A/B sobre 10 tarefas representativas:**

1. Selecione 10 tarefas reais do backlog (mix greenfield/bugfix/refator)
2. Para cada tarefa, executa 2 vezes:
    - Run A: com ramilletes.md no contexto
    - Run B: sem lips.md (ou com uma versão vazia)
3. Medição para cada run:
    - Número de voltas antes de completar
    - Número de ficheiros fora do 'scope' afectados
    - Número de erros de compilação
    - Cumprimento das convenções de prova
    - Custo total em Tokens
4. Compare:
    - Se não reduzir a NINGUNA métrica → é inútil, quítalo.
    - Se reduzir algumas métricas → só mantém as secções úteis.
    - Se aumentar o custo sem melhorar a qualidade → é prejudicial.

** Indicadores de um ramificador eficaz.md:**

- O agente cita os pedidos de teste exatos sem redescobrir os pedidos de teste.
- O agente não toca os arquivos proibidos sem que eles se lembrem.
- O agente respeita as convenções de nomeação desde o primeiro diff
- O número de "chamadas" humanas durante o período de sessões diminui.

** Indicadores de um ramificador.md prejudicial:**

- O agente produz diffs mais verboso (es "aplica" demasiadas regras)
- O custo em Tokens aumenta > 20% sem melhora mensuráveis
- O agente alucina comandos que não estão no arquivo
- As regras genéricas anotam as regras específicas

Regra de manutenção: cada vez que uma regra de AGENTS.md é violada por um agente Y que a violação é capturada em revisão, a regra é mal formulada ou no local errado. Corrígela ou materializa-la em um controle da seção 5 ou 15A em vez de adicionar uma frase mais.

<!-- section: s-6 -->
#### Auditoria da *rule drift*: verificar que as instruções seguem descrevendo a repo real

As regras destinadas aos agentes são voluntariamente específicas a rota, o comando, os módulos, os ficheiros proibidos e, precisamente por isso, envelhecem rapidamente. Uma instrução falsa é pior do que uma instrução ausente: obriga o agente a reconciliar `AGENTS.md` com um códigobase que já mudou.

Adiciona `scripts/ai-rules-drift` e executa-o depois de qualquer mudança de arquitetura/build, e depois pelo menos uma vez por semana se o depósito se mover muito:

```text
Verifique se:
- todo caminho citado em AGENTS.md / CLAUDE.md ainda existe
- todo módulo sbt citado ainda existe
- todo comando de compilação, teste e formatação continua válido
- bancos, serviços, diretórios ou scripts removidos deixaram de ser referenciados
- os arquivos protegidos ainda correspondem às áreas realmente críticas
- CLAUDE.md, se presente, continua importando ou complementando a fonte compartilhada esperada.
```

O script pode permanecer determinista para os checks simples (`test -e`, tamanho dos módulos, comandos `--help`/dry-run) e apenas fazer **informar** os casos ambíguos. Nunca permita ao agente que detecta a deriva a reescrever e depois auto-aprobar suas próprias regras persistentes: o diff de regras é revisto como código.

<!-- section: s-7 -->
### Instruções GitHub Copilot sem duplicar `AGENTS.md`

Se o repositório usar GitHub Copilot, conserva `AGENTS.md` como contrato comum e reserva `.github/copilot-instructions.md` as expectativas específicas de **review GitHub ** : gravidade dos findings, convenções de PR, arquivos de monitoramento e critérios que devem ser notificados. `.github/instructions/**/*.instructions.md` permite especializar essas regras por estrada. Evita copiar toda a arquitetura ou as regras. Scala : uma instrução comum deve permanecer em `AGENTS.md`.

Copilot Code Review lê as instruções e esquis da **rama de cabeça da PR** Portanto, uma modificação dessas normas faz parte da superfície de código que deve ser revista: um agente não deve poder suavizar as suas próprias limitações no mesmo PR sem que essa mudança seja explicitamente visível e validada .

