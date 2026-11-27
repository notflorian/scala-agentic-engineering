<!-- section: chapter -->
# 4. Orçamento mensal realista e estratégia de cache

O orçamento deve ser gerido como um orçamento de engenharia, não como uma despesa abstrata da IIA. A boa métrica não é o custo por mensagem, mas sim:

```text
custo total de uma tarefa pronta para o merge
= custo do modelo + tempo humano + tempo de CI + achados de revisão + retrabalho por bugs
```

<!-- section: s-1 -->
## Orçamento inicial realista

| Posto                                                 |                 Orçamento indicativo | Nota                                                                                                                                                                                    |
|-------------------------------------------------------|---------------------------------:|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Claude Code via Claude Pro/Max                        |                      20 à 200+ $ | Max se justifica se Opus/Sonnet giram todos os dias; a cota é partilhada entre as superfícies Claude compatíveis.                                                                        |
| ChatGPT com Codex                                    |                     20 $ e mais | Mais adequado para o uso limitado; Pro se justifica se Sol 6.2 se torna um writer diário e não apenas um reviewer.                                                                        |
| JetBrains AI Ultimate                                 | ~300 $/ano; 35 AI Credits / 30 j | Use para funções de nuvem JetBrains e Junie; Código Completion / Next Edit Dicas e agentes autenticados em seus fornecedores não consomem esses créditos.                     |
| GitHub Copilot                                        |                         variável | Opcional: relevante sobretudo se GitHub é o centro do fluxo de trabalho issues/PR/review; amplamente redundante como terceiro gato de código.                                                      |
| OpenRouter / API pontual GLM/Kimi/Gemini/Grok      |                         0 à 50 $ | Porta de saída excepcional quando Claude/Codex/Qwen não são suficientes; o orçamento voluntário é fraco e limite máximo.                                                                         |
| GLM Coding Plan (Z.ai) a segunda assinatura opcional  |                 ~18 a 160 $/mês | Forfait open-weight *conformidade* : endpoint Anthropic-compatible, tomada em Claude Code para absorver review/triage sem colocar seus limites Claude. Lite ~18 $, Pro ~72 $, Max ~160 $. |
| Qwen local                                            |             0 $ sem eletricidade | Muito bom para pré-análise, síntese e boilerplate, mas não para decidir apenas em código crítico.                                                                                           |
| Sourcebot, Aider, OpenCode/Qwen Code, RTK             |                     0 para variável | Muitas ferramentas são de código aberto, mas o alojamento, índices e chaves API possíveis custam.                                                                                      |
| Headroom e ferramentas de compressão de contexto recentes |                     experimental | Para testar em logs/diffs não críticos antes de integrá-lo no fluxo de trabalho padrão.                                                                                                         |

Total do objetivo realista para uso intensivo apenas: **250 à 450 $/mes**, que será ajustado após duas semanas de medição real. 300 à 350 $ continua a ser plausível, mas não há que congelar: um único mau ciclo agente num contexto grande pode custar mais do que uma semana de micro-patas bem lagartas.

<!-- section: s-2 -->
## Pontos de preços e quotas que não devem ser mantidas no guia

Claude Code inclui-se nos planos Claude de pagamento compatíveis, mas o uso exato depende do plano, do modelo e dos limites de sessão. As páginas oficiais indicam especialmente Claude Pro a 20 $/mes, Max a partir de 100 $/mes, e utilizações Max 5x/20x de acordo com a oferta. Por conseguinte, mantenha o guia sob a forma de faixas, não como uma verdade contabilística permanente.

Lado Codex, evita transformar os nomes de modelos e ajustes ChatGPT na verdade contabilística permanente. O roteamento activo deste guia é **GPT‑6 Luna / GPT‑6.1 Terra / GPT‑6.2 Sol / GPT‑6.2 Astra **, com Sol 6.2 Medium como defeito agente. Os limites de uso, o acesso a Max/Ultra e a facturação dependem do plano, da superfície, da região e do rolout. Escreva as regras em torno da **Clase de trabalho e custo por mudança aceite**, depois verifica a página oficial antes de industrializar um perfil ou orçamento.

Antecedentes importantes: **Anthropic Reserva o uso por assinatura Claude Free/Pro/Max/Team/Enterprise às aplicações nativas Anthropic e às utilizações previstas nas suas condições.** Desde o início 2026, Anthropic proibiu explicitamente o uso de tokens OAuth dessas assinaturas em arneses de terceiros ou ferramentas não oficiais: esses fluxos devem passar por uma chave API dedicada (Claude Console ou nuvem provider) e respeitar os termos comerciais. Especificamente: Claude Code e Claude.ai para as assinaturas Claude; OpenCode/Qwen Code/Aider para Qwen locais, modelos API ou chaves BYOK, sem usar nunca um token de sessão Claude Pro/Max numa ferramenta externa.

Não confundir com o que *es* permissão: conectar Claude Code sobre o **endpoint Anthropic- Compatível com Z.ai.** com uma **llave Z.ai** (GLM Coding Plan, §3) é lícito Usas a chave de um fornecedor contra o endoso desse mesmo fornecedor, não desvias nenhum token OAuth Claude. A linha vermelha é o ** um token de assinatura Claude** fora das aplicações Anthropic, não apontar Claude Code para outro fornecedor com sua própria chave.

**Presuposto post-PR Claude Ship.** Em solitário, `/ship`, `/steward` e Cloud Auto-fix consomem o uso aplicável de Claude Code (Não há custo de VM separado para a nuvem Anthropic Segundo a documentação) ; não é gratuita a vigilância em segundo plano. GitHub de Claude Ship (Team/Enterprise) consomem créditos de uso da organização não incluídos na atribuição. `PR/mois × coût moyen de review × nombre de reviews par PR + corrections Steward + classifiers Approvals + CI supplémentaire`. Começa com uma revisão a pedido ou na abertura, não em cada push, e fixa um limite máximo mensal para a Code Review e PR Steward (este último não tem por defeito). `observe` de Approvals também pode ativar reviews e classificadores.
Não é suficiente para deter os agentes activos: Desactivar o Approvals, depois Steward, depois Código de revisão se quiser cortar estas despesas.

**Orçamento pós-PR Codex.** `@codex review` e revisões automáticas GitHub estão sujeitos às condições do Código de Revisão; `/review` local, Goal mode, Heartbeats e tarefas Codex Cloud autenticados com sua conta ChatGPT utilizam as designações aplicáveis ao plano e à superfície. Não há programa de vigilância arquivado nem chave. API OpenAI Para o fluxo de trabalho nativo não é necessário mais. No entanto, verifica as quotas, créditos adicionais e permissões efetivos: cada recuperação e correção podem consumir quota, mesmo sem nova diff. Preferir um objetivo bordado ou um Heartbeat curto com dedução por SHA e parada explícita; nunca os dois simultaneamente em um mesmo ramo. `openai/codex-action` Com chave API Ainda é uma opção de CI separadamente,
a reservar para as necessidades de automação que as superfícies nativas não cobrem.

<!-- section: s-3 -->
## Prompt caching: alavanca principal, mas para formular com precisão

Para não explorar o orçamento, estrutura os pedidos dos agentes de forma determinista:

1. Coloque o contexto estático na parte superior: `AGENTS.md`, regras Scala, arquitetura, convenções de testes.
2. Em seguida, coloca o contexto semiestático: esquemas, contratos JSON, convenções de trabalho.
3. Coloque o contexto dinâmico na parte inferior: ficheiros modificados, erros de compilação, logs de testes.
4. Evite mudar o cabeçalho de prompt para cada iteração se quiser beneficiar da 'cache'.

Uma 'cache' bem-sucedida pode reduzir o custo de ' **leitura** de Tokens de entrada ao redor de 10 % do custo input normal segundo os fornecedores (em modelos) Anthropic correntes: 5 % para Opus 5.5 y Sonnet 5.5, 2,5 % para Fable 5.2, 10 % para Haiku 5.5 ; 5 % para GPT‑6.2 Sol/Astra GPT‑6.1 Sol/Terra).90 % de poupança em toda a tarefa da rede: os tokens de saída, a escrita de cache, os tool calls e os erros de ciclo permanecem facturados.

<!-- section: s-4 -->
## Regras contra o crédito queimado

```text
- Nunca forneça o repositório inteiro por padrão.
- Forneça caminhos de arquivos e uma hipótese sobre a área afetada.
- Corte os logs no primeiro erro útil.
- Após 2 falhas idênticas, pare e retome o diagnóstico humano ou pela IDE.
- Após 3 arquivos alterados fora do plano, pare e peça um novo plano.
- Após 300 linhas inesperadas no diff, pare para revisão manual antes de continuar.
- Quando o contexto deixar de ajudar, escreva um `HANDOFF.md` explícito e abra uma nova sessão. Use `/compact` apenas como último recurso.
- Prefira rg, Sourcebot, IntelliJ, Metals ou scripts locais a grandes despejos de MCP.
```

**Ahorras na dupla assinatura.** Estabiliza o writer e o seu esforço durante uma trajetória; as mudanças de modelo podem perturbar a cache e adicionar rework. Um contexto fresco continua a ser voluntário para o revisor independente ou uma hipótese contaminada. Não lança nem revisão exaustiva sistemática sobre cada micro-patch, nem segundo steward sobre um mesmo PR. Deduca o seguimento por repo/PR/SHA/check/finding, privilegia uma retomada de eventos ou um Heartbeat borné quando a CI , e arréglalo no checkpoint. Medição das cotas consumidos por função e por tarefa (quando o fornecedor o expõe); diferença créditos incluídos, sobrecostos de pagamento e API. Uma quota ainda elevada não é motivo para abrir mais tickets.

