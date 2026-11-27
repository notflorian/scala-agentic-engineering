<!-- section: chapter -->
# 2. Stack consigliato

con **Il MacBook Pro 16" M5 di Max, 18 Il cuore della CPU, 40 Il cuore GPU, il motore neurale 16 dei cuori, 128 Go di memoria unificata, SSD 8 Il T**, **IntelliJ Ultimato**, **Scala/Java / Play / Spartano**Scegliamo questo stack:

| Coppia                 | strumento                                                 | Il ruolo                                                                                                                                   |
|------------------------|-------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| IDE principale          | **IntelliJ Ultimato**                                 | Navigazione, tipografia, rifattore, debug, test e posta di controllo degli agenti                                                             |
| Assistenza IDE         | **JetBrains AI**                                      | Codice Completion, Next Edit Suggerimenti, AI Azioni e piccole trasformazioni senza sostituire l'agente principale                         |
| Agente Claude Principale | **Claude Code di Max**                                   | Opus 5.5 `medium` per codifica agente, architettura e debugging; Sonnet 5.5 `medium` per micro-dev Fable 5.2 in escalata di frontiera |
| Il modello locale           | **Qwen3-Coder-Next / Qwen3.8-27B**                    | Coder-Next come baseline veloce; Qwen3.8-27B come Challenger Quality-First da misurare                                                |
| Harness locale          | **Qwen Code o OpenCode**                             | Qwen Code è ora un harness agenti completo; OpenCode C'è un'alternativa da misurare                                        |
| Agente Codex / rivedere | **Codex in IntelliJ / ChatGPT Il Desktop Codex Il CLI** | GPT‑6.2 Sol `Medium` per la proprietà end-to-end; GPT‑6 Luna `High` con micro-dev GPT‑6.2 Astra `Light`+ per i compiti di frontiera      |
| GitHub Il workflow        | **GitHub Copilot**                                    | Risultati → agente, PR, revisione automatica e correzioni CI Per i Ristoranti GitHub                                                  |
| Monitoraggio PR opzionale   | **Codex Modalità di target / Heartbeats / Cloud Claude Code `/ship` / `/steward` Cloud Auto-fix di Claude Ship** | GPT‑6.2 Sol `Medium` Per il monitoraggio Codex Agente - Agente GitHub centralizzati in squadra, senza sostituire la recensione crociata o la CI |
| Il piccolo diff             | **Aider**                                             | Modifiche mirate, git-first, circuito lint/test                                                                                     |
| IDE agente opzionale    | **JetBrains Giugno / JetBrains AI**                    | Agente nativo in IntelliJ Se vuoi rimanere nel                                                                                  |
| Ricerca codebase     | **Sourcebot**                                         | Ricerca multi-repos, simboli, usi, file pertinenti                                                                           |
| Il KnowledgeGraph         | **ScalaSemantico MCP Il codebase-memory MCP**           | ScalaSemantic per il grafico semantico Scala Codebase-Memory per il grafico strutturale poliglotta Java/Kotlin                       |
| Decisione Layer         | **Jev 1.14**                                          | Decisioni chiuse ad alta frequenza: classificazione, routing, skill selection, scoring e segnale di escalation                           |
| Docs aggiornato            | **Context7**                                          | Verificazione APIFrameworks e libs (anti-hallucinazione)                                                                                |
| Agente di integrazione IDE  | **JetBrains ACP + MCP**                               | ACP collegare l’IDI agli agenti; MCP Mostra strumenti, contesto e azioni IntelliJ                                                           |
| Ottimizzazione token    | **RTK + Headroom**                                    | Riduzione di logs, diffs, outputs terminali                                                                                                |
| Rotazione API            | **OpenRouter**                                        | Accesso puntuale ai modelli alternativi                                                                                                 |

Statuto e maturità degli strumenti:

| strumento                   | Statuto                                           | Punto di vigilanza prima dell'adozione                                                                                                                                  |
|-------------------------|--------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Claude Code             | Stabile, strumento ufficiale                           | Opus 5.5 è il modello opus comune per l'agente codifica lungo; Sonnet 5.5 è il terzo veloce; Agent Teams rimane sperimentale, Ultrareview in research preview   |
| di Claude Ship             | Codice di revisione GA; Steward / Approvazioni in beta     | Servizio Team/Enterprise facturato separatamente; `/ship` e `/steward` I locali sono utilizzati Claude CodeVedi sezione 12.                                             |
| Codex post-pr           | Modalità obiettivi, tassi programmati, Cloud e Code Review ufficiali | Heartbeats in base alla superficie; permissioni e quote da verificare; Watch and Fix non confermato; nessuna fusione automatica. 12. |
| di Claude Mods             | Disponibile da allora Claude Code 2.1.287            | Extension JS/TS in-process; molto potente ma non sandboxed: installare solo il codice controllato e limitare il suo utilizzo alle esigenze che hooks/skills/MCP coprire male |
| Jev 1.14                | accesso precoce; API Il sistema One                    | Ottimo candidato per le decisioni chiuse; soglie da calibrare per compito, stato minimo, mai autorità finale su un'azione critica                           |
| Qwen3-Coder-Next locale  | Il lato stabile del modello                               | sul 128 Sito: Q4_K_M ≈ 48,4 Gioca confortevole; Q5_K_M ≈ 56,7 Si raccomanda; Q6_K ≈ 65,5 Il lavoro è sostenibile; Q8_0 ≈ 84,8 Prova a tempo indeterminato                           |
| OpenCode                | Attivo, LSP in parte exp.                    | Validare il LSP Metals Il tuo repo prima della standardizzazione                                                                                                           |
| Qwen Code               | Attivo, alternativa seria                      | Auto-Memory/Skills, subagenti, worktrees, MCP/LSP; Agent Teams e Arena rimangono sperimentali                                                                     |
| ChatGPT Il Desktop Codex | App per desktop ChatGPT, CLI, estensione IDE e Cloud | Codex Ora è in grado di guidare diverse sessioni/agenti; plug-ins e permissioni rimangono da auditare                                                                  |
| JetBrains Giugno / CLI   | **stabilità**di BYOK                                 | Opzione credibile, da distribuire per bake-off sul deposito Scala                                                                                                      |
| Aider                   | Stabile, mantenuto                                 | Disciplina "poco di file" indispensabile                                                                                                                         |
| Sourcebot               | stabilità                                           | Costo di alloggio e indirizzo multi-repos                                                                                                                     |
| Context7                | stabilità                                           | Copertura variabile in base ai libs Scala di Niche                                                                                                                  |
| RTK                     | stabilità                                           | Hooks PreToolUse da testare sulle tue uscite sbt Reali                                                                                                              |
| Headroom                | **sperimentale**                                 | Testare solo su logs/diffs non critici                                                                                                                     |
| OpenRouter              | stabilità                                           | Zero infraroce; ideale come porta di uscita puntuale verso GLM/Kimi/Gemini/Grok e nuovi modelli                                                                  |

JetBrains A due livelli MCP Per distinguere: il sostegno MCP L’assistente è presente da allora IntelliJ Idea 2025.1 come cliente e come IDE JetBrains Esiste anche un servitore MCP integrato da allora 2025.2 per consentire ai clienti esterni di accedere agli strumenti dell'IDE. è particolarmente importante per Scaladove l'agente ha bisogno di simboli, tipi, moduli, ispezioni e configurazioni di esecuzione, non solo testo brutto.

Da allora IntelliJ Idea 2026.1 Chi ha integrato Codex, Claude Agent e Junie, poi Cursor e GitHub Copilot attraverso il registro ACP pubblico (aperto a fine gennaio) 2026Con una gestione MCP da un agente consolidato in 2026.2 – aggiunge una distinzione di protocollo: **ACP (Agente Cliente Protocollo) collegare l'IDE all'agente di codifica**Mentre che **MCP collegare l'agente agli strumenti e al contesto**. IntelliJ Può così servire di sì e di verità strutturale mentre lascia Claude, Codexdi giugno, GitHub Copilot o un altro agente ACP Ogni agente conserva la sua propria harness, i suoi modelli, l'autenticazione e le sue autorizzazioni; l'unità sostituibile non è quindi più solo il LLM, ma l'agente completo. gli strumenti del server MCP IntelliJ possono essere limitate da agenti; per il debugging Scala/JVMGli strumenti di debugger
Esposto dal Servitore MCP IntelliJ (Tratto di strumento prefinito `xdebug_`attivabile dalla configurazione del MCP Server) consentono di raccogliere stack, variabili, threads e prove runtime senza iniezione di `println` nel codice .

<!-- section: s-1 -->
### Architettura IntelliJ 2026.2 raccomandato

```text
IntelliJ IDEA
├── JetBrains AI
│   ├── Code Completion
│   ├── Next Edit Suggestions
│   └── AI Actions / petites transformations
├── Claude Code officiel
│   ├── plugin JetBrains / CLI
│   └── Claude Code Desktop
│       → abonnement Claude Max, agent principal sur raisonnement/debug/architecture
├── Codex
│   ├── agent ACP dans AI Chat
│   ├── ChatGPT Desktop / CLI
│   └── compte ChatGPT/OpenAI
│       → agent principal sur issues standard / reviewer croisé quand Claude écrit
└── GitHub Copilot
    └── couche GitHub-native : issues, PR, review automatique, CI
```

**ACP non sostituisce le integrazioni ufficiali.** Per Claude, guardate **Claude Code Ufficiale** come via principale quando si desidera sfruttare l'abbonamento Claude Max: il plugin JetBrains, il CLI e la scheda Codice di Claude Desktop condividono lo stesso harness Claude Code e le sue regole (`AGENTS.md` Il fallback o `CLAUDE.md`Permessi e hooks, MCPe le competenze). Claude Code Desktop aggiunge diverse sessioni isolate per worktrees, visualizzazione dei diff, terminal/editor integrati e monitoraggio delle PR. ACP In particolare, la struttura di interoperabilità che consente di IntelliJ di accogliere diversi agenti in una UI comune.

per CodexL’agente integrato a IntelliJ Si può autenticare con il **conta ChatGPT** o una chiave OpenAICon un'autenticazione specifica per il fornitore, l'uso dell'agente non consuma i crediti AI JetBrainsLa stessa logica per gli altri agenti ACP che utilizzano il proprio account fornitore. le funzioni in-editor **Codice di completamento** e **Successivo Edit Suggerimenti** non consuma nemmeno la quota di AI Credits. un abbonamento **JetBrains AI Ultimo (35 I crediti / 30 giorni )** Si tratta di un budget per Junie, AI Chat e le funzioni cloud. JetBrains non ha bisogno di finanziare il grande numero di sviluppo agenzico se Claude Code e Codex utilizzano i loro rispettivi abbonamenti.

Per notare il lato JetBrains in 2026 : **Codex È ora integrato come agente nelle IDE** insieme a Junie e Claude, il registro ACP può aggiungere altri agenti, e un sistema di **abilità** riutilizzabile completo MCPL’idea diventa così un **Controllo del piano locale** Navigazione, diagnosi e debugger rimangono JetBrains, mentre l'autore o il rivista può essere cambiato per sessione senza abbandonare l'ambiente Scala/JVM.

---

