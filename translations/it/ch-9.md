<!-- section: chapter -->
# 9. Integrazioni MCP prioritarie

<!-- section: s-1 -->
## Essenziale

| MCP                        | Role of the                                                                                 |
|----------------------------|--------------------------------------------------------------------------------------|
| **Metals MCP**             | Intelligenza Scala live : compilazione, diagnostica, tipi, simboli casuali                      |
| **ScalaSemanticismo MCP**      | Semantic grafo Scala via SemanticDB: usi, gerarchie, call pathes, Givens probabili     |
| **JetBrains MCP**          | Exhibit: IntelliJ, file aperti, azioni IDE                                      |
| **Sourcebot**              | Ricerca multi-ripristino/scoprimento codice base automatica                                             |
| **Codebase-Memory conseguente MCP**    | Conoscenza grafico strutturale poliglot persistente; in particolare Java/Kotlin/cross-service |
| **GitHub MCP**             | Questioni, PR, Azioni, assegni                                                          |
| **Context7**               | Aggiornato libs documentazione necessaria                                                         |
| **Playwright: MCP**         | Validazione IU se web app precedenti                                                             |
| **Sentry: MCP**             | bug diagnostici prod conseguente                                                                 |
| **Postgres solo lettura MCP** | Schematic, migrazione, richieste relative                                                         |
| **ast-grep urgentemente MCP**           | Ricerca strutturale e rifattori mirati                                           |

Caratteristiche operative (da controllare al momento dell'installazione — i trasporti e le versioni stanno cambiando rapidamente):

| MCP                    | Trasporto tipico               | Notevole versione minima                   | Manutenzione di giugno 2026                                    |
|------------------------|---------------------------------|--------------------------------------------|----------------------------------------------------------|
| Metals MCP             | stdio; standalone da 1.6.6] | Metals 1.5.3 (integrato) 1.6.6 (standalone) | Attivo (Scalameta)                                        |
| ScalaSemantic MCP      | MCP locale corrente                       | SemanticDB richiesto per il cuore dell'indice  | Giovane; specializzato Scala, da benchmarkare sul repoenziale      |
| JetBrains MCP          | Server integrato IDE vuoto             | IntelliJ 2025.2 (server)                  | Attivitā (obiettivo)JetBrains)                                        |
| Sourcebot              | HTTP                            | —                                          | Benefici                                                    |
| Codebase-Memory MCP    | MCP locale corrente                       | —                                          | Active; Hybrid LSP documentato per Java/Kotlin, non aggiornato Scala |
| GitHub MCP             | HTTP remoto o stdio temporaneo locale     | —                                          | Attività ufficiali (attuali)GitHub)                                  |
| Context7               | Aggiornamento remoto                    | —                                          | Benefici                                                    |
| Playwright MCP abitua         | e la mia vita                           | —                                          | Attivo (Microsoft) corrente                                        |
| Sentry MCP             | Aggiornamento remoto                    | —                                          | Attivo (Impresa Ufficiale)                                  |
| Postgres solo per la lettura MCP | e la mia vita                           | —                                          | Variabile a seconda dell'implementazione — auditer prima prodenziale     |
| ast-grep MCP significa           | e la mia vita                           | —                                          | Benefici                                                    |

> **Sviluppi nel Protocollo allegato MCP per sapere** : **MCP 2026-07-28 è ora il riferimento di riferimento pubblicato specificatamente**.
> Il cuore diventa schiava: ritiro delle sessioni di livello di protocollo, di `Mcp-Session-Id` e, per questa revisione,
> `initialize` / `notifications/initialized`. Ogni richiesta porta in `_meta` le informazioni raccolte
> di cui la versione e le capacità del cliente. `server/discover` permette di scoprire identità, versioni e privilegi
> La revisione formalizza anche il framework server **Estensioni**, les **Tasks** per un lungo lavoro,
> Il mondo del lavoro **MCP Appstenza**, l'autorizzazione allineata OAuth/OIDC e una politica di ammortamento; `Roots`, `Sampling` e non è così
> `Logging` sono ammortati. Per un nuovo sviluppo, **target 2026-07-28**, ma mantenere i test di compatibilità
> 2025-11-25 fino a quando tutti i clienti/server utilizzati non vengono migrati. Claude Code 2.1.27x ha generalizzato il suo cliente abituale
> MCP v2 e negoziazione 2026-07-28 per dirigere le connessioni HTTP, tra cui Bedrock, Vertex, Foundry e autorizzazioni
> Servizi offerti
> senza telemetria; rimane una modalità legacy, pertanto non assume che tutti i pari possano MCP di un ambiente
> recenti sviluppi
> hanno migrato allo stesso tempo.

> **MCP Gli eventi rimangono un'estensione proposta, non il nucleo del protocollo.** ChatGPT sapere come sperimentare gli abbonamenti
> `events/list`, `events/subscribe` e non è così `events/unsubscribe` con webhook consegna su server in aumento MCP 2.0
> [`2026-07-28`]). È utile per i flussi di lavoro degli eventi — ha creato commento, incidente, messaggio, cambiamento casuale
> lo stato — ma non rende un'integrazione critica dipendente da questa estensione fintanto che il suo stato e il suo sostegno
> I clienti/server transfrontalieri non sono stabilizzati.

<!-- section: s-2 -->
## ChatGPT e non è così Codex: ruoli distinti MCP non essere confuso

Dobbiamo distinguere i dati **ChatGPT Il tuo sito web**, lesbiche **i clienti Codex Localizzazione** e la paura **Agenti API**. MCP descrive un rapporto cliente/server; il fatto che un prodotto possa esporre anche un cliente/server API orchestrazione non la trasforma in un server MCP.

| Informazioni generali                                                       | Role of the MCP e trasporti                                                                            | Autenticazione                                                                      | Lettura / scrittura                                                                          |
|---------------------------------------------------------------|---------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **Codex CLI / Estensione IDE / host precedenti Codex di un'altra ChatGPT Il mio lavoro.** | **Client MCP**; Local STDIO e Remote HTTP Streamable; configurazione condivisa sullo stesso host | Bearer, OAuth, CIMD e DCR; `codex mcp login` per OAuth impegnativo                             | A seconda degli strumenti server, sandbox e approvazioni; possibile lettura e scrittura casuale |
| **ChatGPT web per il web**                                           | App Client per l'acquisto MCP **Rilevamento**                                                                   | OAuth secondo l'app apposta                                                                     | Modalità di sviluppo limitata agli strumenti `read` / `fetch`                                           |
| **ChatGPT web Business / Impresa / Edu preciso**                   | App Client per l'acquisto MCP remoto; **pieno di energia MCP In beta casuale**                                                | OAuth + workspace/admin controlli automatici                                                     | Strumenti di lettura e azioni `write` / `modify` possibile per MCP personalizzati        |
| **OpenAI Agenti API**                                         | Client MCP ospitato o dall'ambiente; HTTP o STDIO a seconda dell'origine della connessione         | Headers/Bearer, fedel box o variabili ambientali a seconda del trasporto | `allowed_tools` permette di ridurre esplicitamente la superficie esposta                          |

> **Documentazione OpenAI contraddittoria.** Il dettagliato Centro di assistenza mantiene **Pro = Osservare
> `read`/`fetch`**] e riservate il pieno MCP leggi/scrivi a Business/Enterprise/Edu, mentre la pagina dello sviluppatore mostra
> Generalista afferma ora che la modalità sviluppatore dà il pieno MCP lettura/scrittura a Plus e Pro.
> fonti ufficiali non convergono, mantengono la tabella sopra come ipotesi conservatrice e apparent ** rileva l'errore
> capacità effettivamente esposte dal conto / spazio di lavoro** prima di progettare un flusso di lavoro di scrittura.

**Codex non è più un server temporaneo MCP.** `codex mcp-server` e il binario `codex-mcp-server` L'integrazione che vuole guidare l'argomento Codex come un servizio deve migrare a mezzi finanziari **Codex App Server per l'uso**, che utilizza il proprio potere JSON-RPC e prospettive **non è un problema. MCP** ; Codex continua a consumare server in parallelo MCP esterno come cliente.

ChatGPT web non si collega direttamente a `localhost`. Per un'occasione MCP locale, privato o on-premise, lo espongono tramite il **Un'altra volta MCP Tunnel:** Invece di aprire il server pubblicamente, due limitazioni di superficie rimangono importanti: **La modalità agente non utilizza le applicazioni precedenti MCP personalizzato**, et scusa **Ricerca profonda** li usa solo in quantità `read` / `fetch`.

<!-- section: s-3 -->
### Gestire un'impresa MCP catalogo come un oggetto API Versione di prova

Quando un amministratore approva un'app modificata MCPTraduzione: ChatGPT, il prodotto mantiene un certificato **snapshot degli strumenti e dei loro input**. L'aggiunta, la rimozione o la modifica di uno strumento sul server non rende automaticamente la nuova superficie attiva, quindi un'evoluzione incompatibile può rompere le chiamate fino a quando un amministratore ha rivisto e ripubblicato il catalogo, e viene ChatGPT Attualmente non garantisce un avviso proattivo su questa deriva.

```text
changement de nom / schéma / permission / nouvel outil MCP
→ diff de surface
→ review
→ validation admin
→ publication
```

Questo **rule completa**, senza sostituirlo, la politica di sicurezza di questa sezione: versioni pinned, autorizzazioni minime, log degli strumenti e lettura/scrittura separazione.

<!-- section: s-4 -->
## grafo di conoscenza MCP per il futuro Scala, Java e Kotlin probabili

**Sourcebot non è una conoscenza grafo.** Resta lo strato di ricerca/scoperta: trovare rapidamente file, simboli, usi testuali ed estratti rilevanti, soprattutto su diversi restitories. Un grafico di conoscenza risponde ad un'altra classe di domande: relazioni tra simboli, percorsi di chiamata, gerarchie, dipendenze strutturali e l'impatto di un cambiamento.

<!-- section: s-5 -->
### Scala: preferire ScalaSemantic, completo di Metals frequenza

Per un deposito principalmente dovuto Scala, **ScalaSemanticismo MCP** è il miglior candidato identificato per lo strato "grafico semantico" che non solo ricostruisce il codice da un AST Tree-sitter: il suo indice principale è alimentato da frequenza **SemanticDB aggiunto**, per simboli già risolti durante la compilazione, espone richieste globali adattate agli agenti, inclusi usi esatti, firme, gerarchie, sovraccarichi, eccezioni `call_path`, alla ricerca di Givens e alla tracciatura di catene illecite

```text
Sourcebot
→ « où est X ? »
→ « quels fichiers parlent de Y ? »

ScalaSemantic MCP
→ « quels sont les usages exacts de ce symbole ? »
→ « quel chemin d'appel relie A à B ? »
→ « qui étend ce trait ? »
→ « quels givens peuvent produire T ? »
→ « de quels implicits dépend ce given ? »

Metals MCP
→ « quel est le type réel ici, maintenant ? »
→ « ce fichier compile-t-il ? »
→ « quels diagnostics le compilateur retourne-t-il ? »
→ « quels tests échouent ? »
```

ScalaSemantic e conseguente Metals sono i migliori. **Ulteriori informazioni**. ScalaSemantic è indice e eccellente per le relazioni globali; Metals SemanticDB è principalmente l'ultimo stato compilato: se il codice è stato appena modificato senza ricompilazione, occorre che il codice sia stato modificato senza ricompilazione. Metals Forse e' piu' figo.

Anche non presenta ScalaSemantic come un Neo invitati4j/ERF: è più precisamente una scusa **codice semantico grafico MCP**. Alcune operazioni rimangono approssimazioni di alto livello e non riproducono necessariamente tutta la logica del compilatore a un determinato sito di chiamata. In caso di contraddizione sulla risoluzione reale di un tipo, sovraccarico o Given, conseguente **Metals/scalac vince l'attesa**.

<!-- section: s-6 -->
### Java e Kotlin: Codebase-Memory diventa molto più interessante alternativa

**Codebase-Memory conseguente MCP** costruire un grafico di conoscenza persistente di funzioni, classi, catene di chiamata, percorsi HTTP e collegamenti cross-service da Tree-sitter. Il suo secondo passaggio "Hybrid LSP" attualmente documenta una ricca risoluzione per diverse lingue tra cui **Java e Kotlin impegnati**. Su queste due lingue, è quindi più rilevante di quanto non sia avvenuto. Scala per le questioni strutturali del codice di base.

```text
Java / Kotlin

Sourcebot
= recherche et discovery

Codebase-Memory MCP
= knowledge graph persistant
= call graph
= impact analysis
= architecture
= routes et relations cross-service

IntelliJ / LSP
= sémantique live et arbitrage local
```

Su una poliglottina JVM codice base, la distribuzione consigliata diventa:

```text
Scala pur
→ Sourcebot + ScalaSemantic + Metals

Java/Kotlin
→ Sourcebot + Codebase-Memory + IntelliJ/LSP

Scala + Java + Kotlin / microservices
→ Sourcebot
→ ScalaSemantic pour la sémantique Scala
→ Codebase-Memory pour la topologie polyglotte et cross-service
→ Metals / IntelliJ pour arbitrer la sémantique live
```

Il criterio determinante non è "ha una base grafica?", ma **quali informazioni genera bordi casuali** :

```text
Tree-sitter
→ structure syntaxique et résolution heuristique

SemanticDB
→ symboles résolus par le compilateur Scala

LSP / presentation compiler
→ état sémantique live du code courant
```

Per lo sviluppo Scala, quindi, preferisce un bordo SemanticDB ad un bordo ricostruito solo dal testo quando entrambi sono disponibili.

<!-- section: s-7 -->
### Effetto sul contesto ingegneristico

Questo livello di grafico è particolarmente utile se evita il caricamento di decine di file. Un subagent in sola lettura può query ScalaSemantic o Codebase-Memory, quindi traccia solo alcuni percorsi, simboli e prove probabili `file:line` al genitore: equivalere

```text
question d'impact
→ subagent isolé
→ knowledge graph / semantic graph
→ 5–10 relations pertinentes
→ vérification Metals / IntelliJ si nécessaire
→ résumé < 1–2K tokens
→ parent
```

Questo aumenta la frequenza`isolation_ratio` e riduce direttamente l'argomento *contestazione del contesto*. D'altra parte, non attivare diversi parametri MCP grafo per principio: benchmark su dieci compiti reali e mantenere solo quelli che riducono il numero di file letti, gettoni iniettati o frainteso.

<!-- section: s-8 -->
### Alternative da sapere senza standardizzarli

`agent4s` è un toolbox Scala MCP] Un interessante, basato sulla Scalameta con SemanticDB opzionale, che include riferimenti, gerarchie, dipendenze e call grafo. Si merita un panificio se ScalaSemantic non copre una classe di compiti, ma non aggiunge subito entrambi.

Joern costruisce un vero e proprio vuoto ** Codice Proprietà Graph gradimento** molto ricco per la sicurezza e l'analisi dei flussi di dati, ma il suo frontend sorgente non mira a stabilire Scala come lingua di primo ordine. JVM Scala è possibile, al costo di perdere parte delle astrazioni di origine; quindi Joern si riserva di audit specializzati piuttosto che il contesto giornaliero di introduzione Claude Code.

<!-- section: s-9 -->
## Metals MCP: lo strumento Scala] mancante nella maggior parte dei stack precedenti

E' probabilmente il segreto. MCP più sottoutilizzato da sviluppatori Scala. **Metals (server di lingua) Scala) spedisce un server temporaneo MCP da quando si è1.5.3** (Maggio in corso) 2025), e l'argomento **v1.6.6 "Osmium" (prevenzione)3 Marzo 2026) aggiunto un server temporaneo MCP standalone per il tempo libero** che funziona senza un editor aperto — così utilizzabile direttamente da Claude Code o Codex CLI in terminale. Questa stessa versione ha aggiunto il supporto della correzione **Gioca a Twirl modelli casual**, direttamente pertinente al vostro stack.

Gli strumenti presentati includono: `compile-file`, `compile-full`, `compile-module`, `test`, `inspect`, `get-docs`, `get-usages`, `get-source`, `import-build`, `find-dep`, strumenti Scalafix, strumenti necessari `glob-search` e non è così `typed-glob-search`. Lo strumento chiave per i cappi rimane preciso **`compile-file`** : l'agente scrive, compila il file, riceve errori di tipo/implicito e corregge immediatamente, senza pagare un ciclo determinato `sbt compile` completo di ogni iterazione.

Articolazione con JetBrains MCP e ScalaSemantic: aumento

```text
JetBrains MCP     = contexte IDE quand IntelliJ est ouvert (fichiers ouverts, inspections, run configs)
ScalaSemantic MCP = relations globales SemanticDB : usages, hiérarchies, call paths, givens
Metals MCP        = feedback compilateur live pour les agents terminal, même IDE fermé
```

I tre sono complementari, non ridondanti. Per lunghe sessioni Claude Code o compiti lanciati al di fuori di IDE (CI locale, parallel worktree), MetalsMCP] è quello che trasforma "l'agente indovina i tipi" in "l'agente interroga il compilatore".

> **Traduzione: Metals** : **Metals 1.6.9 è stato pubblicato da allora 14 Settembre 2026** (Dopo la morte) 1.6.8 di un'altra 23 Luglio).
> MCP, porta il `glob-search` su tutti i moduli, la risoluzione delle suite di prova tra moduli, la quantità
> suggerimento di`import-build` quando non si trova alcun obiettivo di costruzione e una correzione contro i blocchi di errore
> Linking. Questo è direttamente utile per i monorepos multi-module Play/opzionesbt: prendere in considerazione 1.6.9 come minimo per evitare
> Cicli agentici. Miletones Metals 2 esistono, ma non standardizzarli fino ad un rilascio stabile.

<!-- section: s-10 -->
## Esempio: loop di correzione di prova su `compile-file`

Skeleton: ZIO del loop che rende il valore di anticipazione Metals MCP — l'agente corregge contro l'accusa **compilazione**, non contro la propria fiducia, con un terminale di torri che materializza la regola "portare2 chessuales→ stop: il tempo libero

```scala
import zio.*

final case class Diagnostic(file: String, line: Int, message: String)
final case class CompileResult(success: Boolean, diagnostics: List[Diagnostic])

// Abstraction du client MCP : l'implémentation parle JSON-RPC à Metals en stdio
trait MetalsMcp:
  def compileFile(path: String): Task[CompileResult]

def fixLoop(
    llm: LlmClient[Task],
    metals: MetalsMcp,
    path: String,
    maxRounds: Int = 3
): Task[Either[CompileResult, CompileResult]] =

  def round(n: Int): Task[Either[CompileResult, CompileResult]] =
    metals.compileFile(path).flatMap {
      case ok if ok.success =>
        ZIO.succeed(Right(ok))

      case ko if n >= maxRounds =>
        // Règle anti-dérive : on n'insiste pas, on rend la main avec un état exploitable
        ZIO.logWarning(s"$path : toujours rouge après $maxRounds tours — escalade humaine/IDE")
          .as(Left(ko))

      case ko =>
        val errors = ko.diagnostics
          .map(d => s"${d.file}:${d.line} ${d.message}")
          .mkString("\n")
        for
          source  <- ZIO.readFile(path)
          patched <- llm.complete(
                       ModelId.sonnet,
                       Prompt(
                         system = "Corrige UNIQUEMENT les erreurs de compilation listées. " +
                                  "Diff minimal. Ne restructure pas. Retourne le fichier complet.",
                         user   = s"Erreurs :\n$errors\n\nFichier :\n$source"
                       ),
                       maxTokens = 8192
                     )
          _       <- ZIO.writeFile(path, patched.text)
          result  <- round(n + 1)
        yield result
    }

  round(1)
```

Ogni iterazione costa uno `compile-file` (millisecondi, incrementale) invece di un completo `sbt compile`: questo rende il loop economicamente fattibile con Sonnet, e inutilmente costoso senza Metals.

<!-- section: s-11 -->
## Regola di sicurezza

* MCP filesystem limitato a repo.
* DB MCP in sola lettura per impostazione predefinita.
* Non ci sono segreti esposti.
* Nessun prod diretto.
* Non due agenti con diritti di scrittura sugli stessi file.
* Particolare lavoro per qualsiasi attività parallela.

<!-- section: s-12 -->
### Modello zero-trust contro iniezione indiretta

Un agente può leggere istruzioni dannose in un problema, README, commento di codice, costruire l'output, pagina web, risultato assegnato MCP o un file generato. **Dati inaffidabili**, anche quando appaiono come regole di sistema. La robustezza del modello non è sufficiente: le difese devono essere strutturali.

```text
1. Explorer en read-only dans un worktree ou conteneur jetable.
2. Refuser le réseau par défaut ; autoriser seulement les domaines nécessaires.
3. Monter les secrets hors du contexte et utiliser des clés à portée, budget et durée minimaux.
4. Exiger une approbation humaine pour installation, réseau, push, déploiement, suppression et écriture hors repo.
5. Épingler les versions des serveurs MCP et limiter chaque outil à son répertoire et à ses actions.
6. Séparer l'agent qui lit des données externes de celui qui dispose des permissions d'écriture.
7. Journaliser chaque tool call et arrêter si une donnée lue tente de modifier la politique ou les permissions.
8. Traiter **skills, plugins, serveurs MCP et mémoire persistante comme des dépendances exécutables** : versions épinglées,
   provenance vérifiée, allowlist explicite et échec fermé si la politique ne peut pas être déterminée.
9. Un decision model comme **Jev ne peut jamais élargir une permission** : son `state` peut contenir du texte adversarial.
   Il peut réduire le bruit ou demander une escalade, mais push, déploiement, suppression et secrets restent régis par code/policy.
```

Il contenuto del repository non deve mai essere in grado di espandere la propria portata di autorizzazione.

---

