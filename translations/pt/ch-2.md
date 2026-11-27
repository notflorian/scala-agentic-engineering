<!-- section: chapter -->
# 2. Stack recomendado

com **MacBook Pro 16" M5 O Max, 18 Coração do CPU, 40 GPU e Neural Engine 16 Corações de coração, 128 Memória Unificada, SSD 8 O T**, **IntelliJ O Ultimato**, **Scala/Java / Play / Spark**E eu escolhi esse estágio:

| Cadeira                 | Ferramentas                                                 | papel                                                                                                                                   |
|------------------------|-------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| IDE Principal          | **IntelliJ O Ultimato**                                 | Navegação, tipagem, refactor, debug, testes e postos de controle de agentes                                                             |
| Assistência IDE         | **JetBrains AI**                                      | Code Completion, Next Edit Suggestions, AI Ações e pequenas transformações sem substituir o agente principal                         |
| Agente Claude principal | **Claude Code Max**                                   | Opus 5.5 `medium` para codificação agente, arquitetura e debugging; Sonnet 5.5 `medium` para micro-dev Fable 5.2 A escalada da fronteira |
| Modelo local           | **Qwen3-Coder-Next / Qwen3.8-27B**                    | Coder-Next como base rápida; Qwen3.8-27B Como o Challenger Quality-First para Medir                                                |
| Harness Local          | **Qwen Code ou OpenCode**                             | Qwen Code Agora é um harness agêntico completo; OpenCode Há uma alternativa a ser medida.                                        |
| Agente Codex / Revisão | **Codex em IntelliJ / ChatGPT Desktop / Codex CLI** | GPT‑6.2 Sol `Medium` A propriedade end-to-end; GPT‑6 Luna `High` em micro-dev GPT‑6.2 Astra `Light`+ para tarefas fronteiriças      |
| GitHub O Workflow        | **GitHub Copilot**                                    | Resultados → agente, PR, revisão automática e correções CI Para os repositórios GitHub                                                  |
| PR de rastreamento opcional   | **Codex Modo de meta / Heartbeats / Cloud; Claude Code `/ship` / `/steward` Cloud Auto-Fix - Claude Ship - Avaliação** | GPT‑6.2 Sol `Medium` Para o acompanhamento Codex Avaliações; agentes GitHub centralizados em equipe, sem substituir a revisão cruzada ou a CI |
| Pequeno Dif             | **Aider**                                             | Modificações direcionadas, git-first, circuito lint/test                                                                                     |
| IDE Agente Opcional    | **JetBrains Junho / JetBrains AI**                    | Agente nativo em IntelliJ Se você quiser permanecer no                                                                                  |
| Pesquisa de codebase     | **Sourcebot**                                         | Pesquisa multi-repos, símbolos, usos, arquivos relevantes                                                                           |
| ConhecimentosGraph         | **EscalaSemantic MCP Apresentação Codebase-Memory MCP**           | ScalaSemantic para o gráfico semântico Scala Codebase-Memory para o gráfico estrutural poligloto Java/Kotlin                       |
| Decisão Layer         | **Jev 1.14**                                          | Decisões fechadas com alta frequência: classificação, routing, skill selection, scoring e sinal de escalada                           |
| Docs atualizados            | **Context7**                                          | Verificação APIFrameworks e libs (anti-hallucinação)                                                                                |
| Agente de Integração IDE  | **JetBrains ACP + MCP**                               | ACP Conecte o IDE aos agentes; MCP Exponha ferramentas, contexto e ações IntelliJ                                                           |
| Otimização de tokens    | **RTK + Headroom**                                    | Redução de logs, diffs, outputs terminal                                                                                                |
| rotação API            | **OpenRouter**                                        | Acesso pontual aos modelos alternativos                                                                                                 |

Estatuto e maturidade das ferramentas:

| Ferramentas                   | Estatuto                                           | Ponto de vigilância antes da adoção                                                                                                                                  |
|-------------------------|--------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Claude Code             | Estable, ferramenta oficial                           | Opus 5.5 É o modelo Opus comum para o agente de codificação longa; Sonnet 5.5 É o terceiro rápido; Agent Teams permanece experimental, Ultrareview em pesquisa preview   |
| Claude Navegação             | Code Review GA; Steward / aprovações em beta     | Serviço de equipe / empresa cobrado separadamente; `/ship` e `/steward` locais são utilizados Claude CodeVer secção 12.                                             |
| Codex Pós-PR           | Modo de objetivo, tarefas programadas, nuvem e código revisão oficial | Heartbeats por superfície; permissões e quotas para verificar; Watch and Fix não confirmado; não fusion automático. 12. |
| Apresentação Claude Mods             | Disponível desde Claude Code 2.1.287            | Extensão JS/TS in-process; muito poderosa, mas não sandboxed: instalar apenas o código auditado e limitar o seu uso às necessidades que hooks/skills/MCP Cobrir mal |
| Jev 1.14                | Acesso precoce; API Sistemas One                    | Muito bom candidato para decisões fechadas; prazos para calibrar por tarefa, estado mínimo, nunca autoridade final sobre uma ação crítica                           |
| Qwen3-Coder-Next Localidade  | O lado estável do modelo                               | Sur em 128 Ação: Q4_K_M ≈ 48,4 Fica confortável; Q5_K_M ≈ 56,7 Recomendado; Q6_K ≈ 65,5 É viável; Q8_0 ≈ 84,8 Faça o teste de forma pontual                           |
| OpenCode                | Ativo, LSP parcialmente exp.                    | Validação do LSP Metals O seu repo antes da normalização                                                                                                           |
| Qwen Code               | Atividade, Alternativa Série                      | Auto-Memory / Skills, Subagentes, Worktrees, MCP/LSP; Agente Teams e Arena permanecem experientes                                                                     |
| ChatGPT Desktop / Codex | Aplicações Desktop ChatGPTCLI, extensão IDE e Cloud | Codex Agora você pode executar várias sessões/agentes; plugins e permissões ainda estão a ser auditadas                                                                  |
| JetBrains Junho / CLI   | **estável**em BYOK                                 | Opção credível, a ser distribuído por bake-off no depósito Scala                                                                                                      |
| Aider                   | estável, mantido                                 | Disciplina "menos arquivos" indispensável                                                                                                                         |
| Sourcebot               | estável                                           | Custo de alojamento e indicação multi-repos                                                                                                                     |
| Context7                | estável                                           | Cobertura variável de acordo com os libs Scala da Nizza                                                                                                                  |
| RTK                     | estável                                           | Hooks PreToolUse para testar em suas saídas sbt Realidade                                                                                                              |
| Headroom                | **Experimentação**                                 | Testar apenas logs/diffs não críticos                                                                                                                     |
| OpenRouter              | estável                                           | Zero infra; ideal como porta de saída pontual para GLM/Kimi/Gemini/Grok e novos modelos                                                                  |

JetBrains Há dois níveis MCP A diferença é: o apoio MCP O assistente do grupo existe desde IntelliJ Idéias 2025.1 Como cliente, e os clientes JetBrains Exibindo também um servidor MCP integrado desde 2025.2 para que os clientes externos tenham acesso às ferramentas da IDE. é particularmente importante para Scalaonde o agente precisa de símbolos, tipos, módulos, inspeções e configurações de execução, não apenas texto bruto.

Desde então IntelliJ Idéias 2026.1 Quem integrou Codex, Claude Agent e Junie, depois Cursor e GitHub Copilot Por meio do Registro ACP público (aberta no final de janeiro) 2026com uma gestão MCP por agente consolidado em 2026.2 Adicione uma distinção de protocolo: **ACP (Agente Cliente Protocolo) liga o IDE ao agente de codificação**Enquanto que **MCP Relaciona o agente com as ferramentas e o contexto**. IntelliJ Assim, pode servir de sim e de verdade estrutural, enquanto deixa Claude, Codexem Junho, GitHub Copilot Ou outro agente ACP Cada agente conserva sua própria harness, seus modelos, sua autenticação e suas permissões; a unidade substituível, portanto, não é mais apenas o LLM, mas o agente completo. as ferramentas do servidor MCP IntelliJ podem ser restringidas por agente; para o debugging Scala/JVMFerramentas de Debugger
Exposta pelo servidor MCP IntelliJ (Tools Preficionados `xdebug_`Ativação desde a configuração do MCP Servidores) permitem a coleta de stack, variáveis, threads e provas em tempo real sem injetar `println` no Código .

<!-- section: s-1 -->
### Arquitetura IntelliJ 2026.2 Recomendado

```text
IntelliJ IDEA
├── JetBrains AI
│   ├── Code Completion
│   ├── Next Edit Suggestions
│   └── AI Actions / pequenas transformações
├── Claude Code oficial
│   ├── plugin do JetBrains / CLI
│   └── Claude Code Desktop
│       → assinatura Claude Max, agente principal de raciocínio, depuração e arquitetura
├── Codex
│   ├── agente ACP no AI Chat
│   ├── ChatGPT Desktop / CLI
│   └── conta ChatGPT/OpenAI
│       → agente principal em issues padrão / revisor independente quando Claude implementa
└── GitHub Copilot
    └── camada nativa do GitHub para issues, PR, revisão automática e CI
```

**ACP Não substitui as integrações oficiais.** Para Claude, guarda **Claude Code oficial** Como principal caminho quando você quer aproveitar a assinatura Claude Max: o plugin JetBrains, o CLI e o cartão de código de Claude Desktop compartilham o mesmo harness Claude Code e suas regras (`AGENTS.md` em Fallback ou `CLAUDE.md`O que é permissão, hooks, MCPe as habilidades). Claude Code Desktop adiciona várias sessões isoladas por worktrees, revisão visual de diffs, terminal/editor integrados e rastreamento de PR. ACP principalmente, a interação que permite a IntelliJ para acolher vários agentes em uma UI comum.

Para CodexO agente integrado em IntelliJ Pode se autenticar com o **conta ChatGPT** Ou uma chave OpenAICom uma autenticação própria para o fornecedor, o uso do agente não consome os créditos AI JetBrainsA mesma lógica para os outros agentes ACP que usam sua própria conta de fornecedor. funções in-editor **Código Completo** e **Próximo Edit sugestões** Também não consome a quota de AI Credits. uma assinatura **JetBrains AI O Ultimato (35 Aos créditos / 30 dias )** É um orçamento para Junie, AI Chat e funções em nuvem. JetBrains Não é necessário financiar a maior parte do desenvolvimento agente, se Claude Code e Codex utilizam as suas respectivas assinaturas.

A notícia do lado JetBrains em 2026 : **Codex Atualmente, é integrado como agente na IDE** Junto com o Júnior e Claude, o registo ACP permite a adição de outros agentes, e um sistema de **Competências** reutilizável completo MCPA idéia se torna assim um **Planos de controle local** Navegação, diagnóstico e debugger permanecem JetBrains, enquanto o escritor ou revizor pode ser mudado por sessão sem abandonar o ambiente Scala/JVM.

---

