<!-- section: chapter -->
# 8. Struttura consigliata del repository

Aggiungi questi file o cartelle alla radice, mantenendo ** un posto di verità**: casuale

```text
AGENTS.md                       # Source commune, courte, versionnée
CLAUDE.md                       # Optionnel :Importe @AGENTS.md + règles Claude spécifiques
GEMINI.md                       # Pointeur vers AGENTS.md ou symlink selon ton outil
.github/copilot-instructions.md # Règles de review / coding agent GitHub Copilot, si utilisé
.github/instructions/           # Règles Copilot path-specific si nécessaire
.aiignore                       # Exclusions IA : secrets, gros artefacts, generated
.claude/rules/scala.md          # Règles Claude path/scopes si utiles
.claude/rules/testing.md
.claude/rules/security.md
stryker4s.conf                  # Mutation testing
docs/architecture.md
docs/testing.md
docs/review-checklist.md
docs/scala-style.md
scripts/ai-test-changed
scripts/ai-lint-changed
scripts/ai-diff-context
scripts/ai-rules-drift
```

Lo scopo non è quello di accumulare la documentazione, ma di evitare che l'agente riscopra le stesse regole in ogni sessione.

> **Sincronizzazione dei file di contesto:** Codex carica le istruzioni globali per l'uso `CODEX_HOME`, poi ho trovato
> i file del percorso del progetto dalla radice alla directory corrente. Ad ogni livello, casuale
> `AGENTS.override.md` ha la precedenza `AGENTS.md`; istruzioni più vicine alla directory di lavoro
> I nomi dei fallback e le dimensioni massime dipendono dalla configurazione.
>
> Claude Code, con il Mod incorporato `cc-plugin-agents-md`, utilizza per impostazione predefinita `claude-md-or-agents-md`:
> `AGENTS.md` viene caricato se non `CLAUDE.md`, `.claude/CLAUDE.md` o `CLAUDE.local.md` esiste nella direzione
> directory corrente o i suoi genitori. Istruzioni per l'uso/amministrazione e frequenza `.claude/rules/` Continua a leggere
> `AGENTS.override.md` non viene letto da Claude tramite questo fallback.
> `claude-md-and-agents-md` caricare entrambi senza duplicare un file già importato.
> non disponibile su determinate superfici; non sostituisce un'importazione esplicita quando necessario.
>
> Per questo flusso di lavoro misto, preferi un comune `AGENTS.md`, e se esiste un `CLAUDE.md`, iniziarlo per mezzo di un
> `@AGENTS.md`. Quindi mantenere solo le regole realmente specifiche a Claude. Controllare le istruzioni riportate
> caricato in una nuova sessione ([`/context all`] lato Claude, e chiedere Codex di elencare i file assegnati
> Per i sottomoduli, controllare anche la scoperta dalla directory reale.
> Nessun override dovrebbe essere in grado di indebolire una regola di sicurezza esterna.

Il mio amico Claude Code : l'innocuità **Norme** sotto la voce `.claude/rules/` consentire di completare le istruzioni del progetto con istruzioni più mirate, ad esempio sotto-tree o tipo di attività, spesso preferibili ad un enorme meccanismo `CLAUDE.md` globale quando questo file esiste.

Anche: il segreto **auto-memory automatica**Claude Code richiede una versione recente, documentata da v autorizzazione2.1.59+. Le prime linee di frequenza `MEMORY.md` può essere caricato automaticamente, e i sub-agenti possono avere la propria memoria. Utilizzare questa memoria per i promemoria di modelli ricorrenti, non per i segreti, non per le decisioni di architettura non visualizzate, e non come sostituto per la documentazione versioned.

<!-- section: s-1 -->
## Contenuto minimo di autorizzazione `AGENTS.md`

```text
Build, test and formatting commands (exact commands)
Non-obvious architecture boundaries and business invariants
Public API / JSON / migration constraints
Protected files and permitted write scope
Scala conventions absent from existing documentation
Stop conditions and definition of done
Pointers to relevant docs and spec
```

Scrivere queste regole ** per l'agente, non come documentazione umana**README, tutorial, l'elenco esaustivo dei moduli e dei confronti dei modelli rimangono in funzione dei percorsi, dei comandi, dei numeri e delle condizioni verificabili. `docs/`, caricato su richiesta.

<!-- section: s-2 -->
### Routing in configurazione utente

Mantiene la matrice di sezione 3 in un documento di routing o profili utente Codex/Claude piuttosto che in ogni `AGENTS.md`: il repository deve rimanere indipendente dal modello. Se un orchestratore dovrebbe consultare questa matrice, aggiunge solo un puntatore ad esso.

<!-- section: s-3 -->
## Contenuto minimo di autorizzazione `CLAUDE.md`

```markdown
@AGENTS.md

## Claude Code
Use plan mode for risky multi-file changes.
```

Muove le regole comuni dal vecchio meccanismo `CLAUDE.md` A proposito di: `AGENTS.md` Claude plan mode è una preferenza di imbracatura; le autorizzazioni effettive rimangono nella configurazione e sandbox.

<!-- section: s-4 -->
## Perché mantenere `AGENTS.md`

Con Codex e il Mod Integrato `cc-plugin-agents-md` del Claude Code (fallback) `AGENTS.md` predefinito), `AGENTS.md` Il lavoro recente sugli agenti di codifica indica che un file di istruzioni di questo tipo può ridurre il tempo di esecuzione e i token di uscita mantenendo un tasso di completamento paragonabile. L'effetto pratico atteso è semplice: contesto meno ripetuto, istruzioni meno dimenticate, meno deriva tra gli strumenti.

> **Dichiarazione di prove: risultato misto, non beneficio automatico.** Un'altra valutazione della situazione 2026 osserva che i file precedenti
> de contestation de réussite et augmentent le coût de plus de 20 %, soprattutto quando si verificano
> I file scritti dai manutentori fanno meglio di quelli scritti dai manutentori.
> Questi vengono generati automaticamente, ma devono anche essere misurati.
>
> Regola corretta: `AGENTS.md` deve contenere solo ciò che effettivamente cambia un'azione — comandi esatti, indicazione
> invarianti non ovvi, file vietati, convenzioni assenti da README e regole di arresto.
> narrazione del repository, nessun catalogo di tecnologie, nessun suggerimento generico.
> con e senza il file. Quantitativo ulteriore benchmark da parte della correzione
> la stessa letteratura: rimanere sotto **~500 parole**, concentrandosi sugli standard di prova, convenzioni di stile, e
> Avvertenze Hazard — nessuna visita guidata del repository — e leggere il file come codice in ogni recensione.

<!-- section: s-5 -->
#### Protocollo di convalida: misurare l'efficacia di AGENTS.md

Un AGENTS.md che non modifica il risultato è il contesto morto che costa i gettoni ad ogni sessione.

**Test A/B su richiesta 10 mansioni rappresentative:**

1. Selezioni 10 compiti reali backlog (mix greenfield/bugfix/refactor)
2. Per ogni compito, eseguire 2 tempi:
    - Eseguire A: con AGENTS.md in contestazione
    - Run B: senza AGENTS.md (o con una versione vuota)
3. Misurazione per ogni corsa:
    - Numero di giri prima del completamento
    - Numero di file offscope interessati
    - Numero di errori di compilazione
    - Conformità con le convenzioni di prova
    - Costo totale in tokens :
4. Confrontare:
    - Se AGENTS.md non riduce alcuna metrica → è inutile, cancellarla
    - Se riduce alcune metriche →] mantiene solo utili sezioni relative
    - Se aumenta il costo senza migliorare la qualità → è dannoso compensare

**Indicatori di un AGENTS.md efficace: somma**

- L'agente cita i comandi di prova esatti senza riscoprire i comandi necessari
- L'agente non tocca i file proibiti senza essere ricordato.
- L'agente è conforme alle convenzioni di denominazione del primo diff preciso
- Il numero di "richiavi" umani durante la sessione diminuisce

**Indicatori di AGENTI dannosi:**

- L'agente produce diffs più verbose (applies) troppe regole?
- Il costo dei gettoni aumenta > aumento 20% senza miglioramento misurabile
- L'agente allucinates comanda che non sono nel file esatto
- Regole generiche mina regole specifiche

Regola di manutenzione: Ogni volta che una regola AGENTS.md è violata da un agente E la violazione è presa in esame, la regola è o male formulata o nel posto sbagliato. Correggerla o materializzarla in un controllo di sezione 5]] o 15A piuttosto che aggiungere un'altra frase.

<!-- section: s-6 -->
#### Audit di emergenza *regole per la gestione*: controllare che le istruzioni descrivono ancora l'effettivo repoenziale

Le regole per gli agenti sono volutamente specifiche — percorsi, comandi, moduli, file proibiti — ed è proprio per questo che invecchiano rapidamente. Una falsa istruzione è peggiore di un'istruzione assente: costringe l'agente a riconciliare `AGENTS.md` con una base di codice che è già cambiata.

Aggiungere `scripts/ai-rules-drift` ed eseguirlo dopo qualsiasi modifica di architettura/costruire, quindi almeno una volta alla settimana se il repository si muove molto:

```text
Vérifier :
- chaque chemin cité dans AGENTS.md / CLAUDE.md existe encore ;
- chaque module sbt cité existe encore ;
- chaque commande de compile/test/format est encore valide ;
- aucun nom de DB, service, dossier ou script supprimé n'est encore référencé ;
- les fichiers « interdits » correspondent encore aux vraies surfaces critiques ;
- si CLAUDE.md existe, il importe ou complète toujours la source commune attendue.
```

Lo script può rimanere deterministico per semplici controlli (obiettivo`test -e`, moduli grep, controlli dovuti `--help`/dry-run) e non solo **reportage** Casi ambigui. Mai permettere all'agente che rileva la deriva di riscrivere e poi di autoapprovare le proprie regole persistenti: la regola diff si rivede come codice.

<!-- section: s-7 -->
### Istruzioni GitHub Copilot senza duplicato `AGENTS.md`

Se il repository utilizza precedenti GitHub Copilot, conservata `AGENTS.md` come contratto comune e prenotazione `.github/copilot-instructions.md` le specifiche aspettative di aumento **Rassegna GitHub** : gravità dei risultati, convenzioni PR, file da monitorare e criteri da segnalare. `.github/instructions/**/*.instructions.md` consentono di specializzare queste regole per percorso. Evitare di copiare tutte le architetture o regole precedenti Scala : un'istruzione comune deve rimanere in funzione `AGENTS.md`.

Copilot Code Review legge le istruzioni e le competenze della correzione ** ramo principale della PR. frequenza** Un emendamento a queste regole è quindi parte della superficie del codice da esaminare: un agente non deve essere in grado di rilassare i propri vincoli nella stessa PR senza che questo cambiamento sia esplicitamente visibile e convalidato.

