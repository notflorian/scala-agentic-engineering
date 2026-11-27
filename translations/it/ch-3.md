<!-- section: chapter -->
# 3. Selezione e assegnazione dei modelli

<!-- section: s-1 -->
## Semplici regole

```text
Qwen / Haiku préparent et filtrent.
Micro-dev sous fort contrôle humain → GPT‑6 Luna High ou Sonnet 5.5 Medium.
Agentic coding end-to-end → GPT‑6.2 Sol Medium ou Opus 5.5 Medium.
Debugging / architecture difficiles → Opus 5.5 High ou GPT‑6.2 Sol High.
Frontier ponctuel → GPT‑6.2 Astra Light ou Fable 5.2 Low avant de pousser aveuglément l'effort du modèle inférieur au maximum.
Un seul writer par worktree.
L'autre famille de modèles reviewe ou challenge, elle ne duplique pas automatiquement toute la trajectoire.
Ultra / multi-agent uniquement lorsque les sous-problèmes sont réellement indépendants.
IntelliJ valide.
Toi, tu décides.
```

Il routing deve ridurre al minimo il costo ** del compito completato**, non il costo della prima chiamata:

```text
charge totale attendue
= découverte + implémentation + vérification
+ probabilité de reprise × coût de reprise
+ coût de coordination
```

Un modello più costoso può quindi essere il miglior acquisto se evita una cattiva esplorazione, diversi diffs inutili e loop di frequenza CI. Al contrario, un micro-loop controllato da un senior rende Luna, Sonnet o Haiku dominante non appena l'errore viene rilevato in pochi minuti.

*Non delegare mai l'aggiornamento delle versioni in materia `build.sbt` senza richiedere all'agente di prima intervista un motivo MCP, Context7, Maven Central o documentazione ufficiale. I nomi e le versioni della biblioteca sono esattamente il tipo di informazioni che modella allucinate quando si lavora fuori contesto.*

<!-- section: s-2 -->
## Routing matrice automatica

| Complimenti                                                    | Modalità         | Consigliato Senior Officer                   | Secondo passaggio utile                           | Perché?                                                                           |
|----------------------------------------------------------|--------------|----------------------------------------------|------------------------------------------------|------------------------------------------------------------------------------------|
| Summarize a module, grep, uses, simple logs indicati            | Micro-dev urgente    | **Haiku 5.5** o Qwen locale per il tempo libero                  | Nessuno tranne ambiguità                           | Lettura ad alta frequenza, basso rischio                                             |
| Accurate modifiche meccaniche, caldaia, rinominanti   | Micro-dev urgente    | **GPT‑6 Luna E' un'ottima idea.**                          | Sonnet 5.5 Tipi medio così sottili             | Ottimo costo quando l'uomo mantiene la direzione opposta                                    |
| Scrivere un semplice test da un comportamento noto   | Micro-dev urgente    | **GPT‑6 Luna E' un'ottima idea.**                          | Sonnet 5.5 Media se ricca regola commerciale        | Semplicemente verificabile uscita automatica                                                       |
| Ritraccia di stack o guasto preciso                           | Micro-dev urgente    | **Sonnet 5.5 Medioriente**                        | Luna High per applicare una patch delimitata        | Sonnet porta più comprensione senza pagare l'Opuus casual                               |
| Piccolo bug riproducibile, noto perimetro                     | Micro-dev urgente    | **Sonnet 5.5 Medioriente**                        | Luna High per testare/meccanica modifica automatica         | Short loops, feedback immediato                                                 |
| patch locale, tipi non banali o invarianti            | Micro-dev urgente    | **GPT‑6.1 Terra Medioriente**                     | GPT‑6.2 Sol Mezzo se l'esplorazione necessaria  | Terzi intermedi da misurare su patch delimitati |
| Piccolo rifattore locale                                     | Micro-dev urgente    | **Sonnet 5.5 Medioriente**                        | Luna High per la verifica meccanica          | Senior mantiene l'architettura necessaria                                                  |
| Rivista mirata di un piccolo diff preciso                            | Verifiche | **GPT‑6.2 Sol La luce del sole**                        | Sonnet 5.5 Medio se secondo utile avviso         | Più giudizio di un lavoratore, senza pagare un agente completo revisione contabile            |
| Uscita standard completa, chiaro spec precedenti                     | Agenzie per l'uso      | **GPT‑6.2 Sol Medioriente**                       | **Opus 5.5 Medioriente** in recensione                  | Il meglio della perfezione Codex per l'esplorazione → patch per il tempo → test → PR:                        |
| Normale multi-file caratteristica distintiva                           | Agenzie per l'uso      | **GPT‑6.2 Sol Medioriente**                       | Opus 5.5 Media in recensione                      | Proprietario end-to-end con contenuto di costi aggiuntivi                                             |
| Caratteristica complessa, diversi strati precedenti                      | Agenzie per l'uso      | **GPT‑6.2 Sol E' un'ottima idea.**                         | Opus 5.5 Medio/Alta frequenza                           | Più pianificazione e verifica precedenti                                         |
| Architettura o scelta di migrazione                       | Agenzie per l'uso      | **Opus 5.5 E' un'ottima idea.**                            | Sol Medium per sfidare il piano finanziario             | Il Giudizio domina la produzione di codice casuale                                           |
| Root causa sconosciuto / bug urgente Scala Il mio amore                   | Agenzie per l'uso      | **Opus 5.5 E' un'ottima idea.**                            | Sol Medium/High per ipotesi indipendenti    | Comprendere il problema costa più di quello che è stato detto.                                     |
| Concorso, asincantesimo, difficile test casuali                 | Agenzie per l'uso      | **Opus 5.5 E' un'ottima idea.**                            | Sol High se la prima traccia fallisce           | Riduce il rischio di ancoraggio su una falsa causa accidentale                                    |
| Migrazione/compatibilità pubblica                       | Agenzie per l'uso      | **GPT‑6.2 Sol E' un'ottima idea.**                         | Opus 5.5 High in Contuale Recensione scritta           | Esecuzione disciplinata + secondo giudizio indipendente                                |
| Grande refattore trasversale                                | Agenzie per l'uso      | **Opus 5.5 E' un'ottima idea.**                            | Sol Medium/High in Recensione esatta                      | Opus per la consistenza globale; Terra per rompere angoli ciechi                     |
| Revisione normale di una PR scritta da Codex                 | Verifiche | **Opus 5.5 Medioriente**                          | Nessuno tranne che per la ricerca critica                    | Contesto fresco e altra famiglia di modelli precedenti                                         |
| Revisione normale di una PR scritta da Claude probabili                | Verifiche | **GPT‑6.2 Sol Medioriente**                       | Nessuno tranne che per la ricerca critica                    | Autore/reviewer automatico                                                           |
| Recensione architettura, invarianti, casi limite             | Verifiche | **Opus 5.5 E' un'ottima idea.**                            | Astra Light così alto palo di attesa    | Cercare errori concettuali piuttosto che rileggere solo il diff salta             |
| Sicurezza, Auth, Critical Contrattualmente                         | Criticismo in corso     | **GPT‑6.2 Astra La luce del sole**                        | Opus 5.5 In alto come recensione                   | Acquistare la capacità superiore senza andare direttamente in estremo sforzo urgente           |
| Problema molto ambiguo, sentenza finale                | Frontiers:     | **GPT‑6.2 Astra La luce del sole**                        | Opus 5.5 E' alto criticare il piano finanziario           | La capacità di giudicare conta più della lunghezza del diff salta                   |
| Decisione molto difficile nel mezzo di un compito normale    | Consulenza      | **Fable 5.2 Basso livello**                            | Sol/Opus rimane l'esecutore temporaneo                     | Acquistare ad hoc giudizio di confine senza trasferire tutto il compito assegnato         |
| Sol High fallisce per capacità limite                   | Arrampicata     | **GPT‑6.2 Astra La luce del sole**                        | Medio/alto solo se necessario            | Cambiare il livello può costare meno di un prolungato Extra High Sol frequenza                    |
| Opus High fallisce per limite di capacità                  | Arrampicata     | **Fable 5.2 Basso livello**                            | Sol/Astra per sfidare                      | Stessa logica: confine basso-effort prima di abbassare il massimo sforzo               |
| Semplice CI fallito dopo la corretta implementazione            | Resumed:      | **GPT‑6 Luna E' un'ottima idea.** o **Sonnet 5.5 Medioriente** | Arrampicata solo se problema concettuale      | Non pagare Sol/Opus per correzione locale e verificabile                     |
| Seguito post-PR indipendente ( frequenzaCI, review, mergeability)         | Resumed:      | **GPT‑6.2 Sol Medioriente**                      | Alto se la radice causa difficile; Sol 6.1 in fallback | Modalità di gol, battiti cardiaci o cloud; loop sequenziale legato, non Ultra eccitato           |
| Secondo fallimento rivelando una cattiva concezione          | Resumed:      | **GPT‑6.2 Sol E' un'ottima idea.** o **Opus 5.5 E' un'ottima idea.**    | Utilizzare l'altra famiglia per rompere l'ancora | Il problema non è più meccanico: l'ipotesi deve essere riqualificata                 |
| Guasti ripetuti nonostante Sol High / Opus Alta frequenza               | Arrampicata     | **GPT‑6.2 Astra La luce del sole** o **Fable 5.2 Basso livello**   | L'altra prima linea sfida urgente                 | La capacità diventa il fattore limitante; lasciando con un contesto del proprio assegnimento         |
| Sessione autonoma > frequenza 30 min, dipendenze sequenziali     | L'orizzonte lungo | ** Opus 5.5 Extra `xhigh`] **]] []]] []]]                 | Sol High alla fine tattica                              | Extra è giustificato per lunghezza, non simbolico importanza                |
| Lavoro estremamente difficile per diverse ore    | Frontiers:     | **Fable 5.2 E' un'ottima idea.**                           | Astra Light/Medium in Independent Review      | Prenota un alto costo di confine per le traiettorie dove evita grandi sovrapposizioni dovute |
| Sfruttamento codebase-scale decomposable casual                  | Multi-agent aggiunto  | **GPT‑6.2 Sol La mia vita è un'altra**                        | Opus Medium per la sintesi/review precedenti               | Ultra si applica soprattutto alle axe di lettura indipendenti                           |
| Test, esplorazione e triage massicciamente parallelizable apparent | Multi-agent aggiunto  | **GPT‑6.2 Sol La mia vita è un'altra**                        | Claude solo sulle principali anomalie dovute | Il parallelismo paga quando i subtaschi sono indipendenti e verificabili       |
| Diversi scrittori sugli stessi file precedenti                 | —            | **Per evitare**]                                 | Sequenziamento                                 | I costi di coordinamento superano generalmente il guadagno derivato                               |

> **Nota: Qwen3-Coder-Next Localizzazione** : il modello ufficiale è un MoE di precisione **80B parametri totali, compensare 3B attivato**, avec precedenti 48
> strati ibridi, un contesto nativo **262 144 Tokens equivale a** e funzionamento esclusivamente **non-pensare urgentemente**. Il mondo del lavoro
> Numero di telefono
> i parametri attivi ridotti migliorano il costo del calcolo, ma il **80B peso dovrebbe ancora risiedere in quantità
> La memoria
> ** : « 3B attivo" quindi non significa che si comporti in RAM come un denso assente 3B.
>
> Le dimensioni ufficiali di GGUF sono: **Q4_K_M 48,4 Vai a vedere.**, **Q5_K_M 56,7 Vai a vedere.**, **Q6_K 65,5 Vai a vedere.** e non è così **Q8_0 84,8 Vai a vedere.**. Il mondo del lavoro
> dimensione del file non è il consumo totale: aggiungere cache di contesto, buffer backend, il rischio
> macOS, IntelliJ, sbt e JVM del progetto. Su ** 128 **], le quattro varianti possono teoricamente essere considerate
> Non offrono lo stesso margine operativo.
>
> ```text
> Q4_K_M  → défaut « marge maximale » : IDE, sbt et plusieurs JVM restent confortables.
> Q5_K_M  → défaut recommandé : meilleur compromis qualité / mémoire sur cette machine.
> Q6_K    → option haute qualité : viable si les autres applications restent raisonnables.
> Q8_0    → option d'évaluation : possible, mais marge réduite et bénéfice à prouver face à Q5/Q6.
> ```
>
> La documentazione ufficiale Qwen usa precisamente **Q5_K_M** nel suo esempio `llama.cpp`, avec `-c 40960`, e non il comportamento
> massimo contesto 256K. Per il lavoro quotidiano, vai su autorizzazione **32K à 64K**, poi aumenta solo se un fattore
> Il contesto dichiarato dal modello è una capacità massima, non una configurazione.
> L'Europa
> default.
>
> **Raccomandazione per la tua M urgente5 Max. 128 Vai a vedere.** : : : : : : **Q4_K_M e Q urgente5_K_M** sulla SSD. frequenza5_K_M come profilo preciso
> preanalisi quotidiana, sintesi del modulo e generazione di semplici test; passaggio a Q aumentata4_K_M quando viene IntelliJ,
> plusieurs moduli aggiuntivi sbt, Scintilla ou descrescente JVM lourdes consomment déjà beaucoup de mémoire. Ne conserva Q supplente6_K ou Q :8_0 e non si è mai visto
> Una cosa?
> Scala mostra un guadagno misurabile di qualità. Con 8 A da SSD, lo storage non è il vincolo; l'eliminazione
> pressione
> memoria, latenza e qualità per compito sono.
>
> **Backend Apple Silicon**: test **MLX-LM e llama.cpp** Invece di congelare immediatamente un singolo motore.
> MLX: 4-bit e salti 8- esistono conversioni a bit, e un rapporto riproducibile di somma Qwen3-Coder-Next osservato decodifica
> molto più veloce sotto MLX che sotto una data versione di llama.cpp su Apple Silicon.
> versioni e non costituisce una garanzia per il M supplente5 Max; giustifica un punto di riferimento locale con versioni fisse.
> `llama.cpp` Tuttavia, è ancora il modo migliore documentato in avanti. Qwen ed espone facilmente un server OpenAI- compatibile.
>
> **Metal e wired memory**: non mostra " 75%" come un limite hardware assoluto `llama.cpp` visualizzato sull'immagine.
> `recommendedMaxWorkingSetSize`, che è il valore da osservare sulla versione di macOS e sul relativo Mac.
> Impostazioni senza documenti `iogpu.wired_limit_mb` esiste e viene utilizzato dalla comunità, ma non deve diventare un falso
> prerequisiti standard: prima testare il modello senza modifiche di sistema.8_0 può lavorare su una macchina automatica 128 Vai, cerca
> ma un contesto lungo o più slot possono avvicinare il processo a questo limite prima della RAM fisica
> o meno.
> Completamente occupato.
>
> **Protocollo di misura minimo**: confronta Q :4_K_M, Q5_K_M ed eventualmente Q intervenire6_K sugli stessi dieci compiti assegnati Scala, con l'aiuto
> lo stesso contesto e la stessa imbracatura. Misurare il rapido processo, il tasso di generazione, il tempo per arrivare
> primo token, massima memoria, pressione di memoria macOS, e frequenza di attività accettata.
> del numero di parametri attivi: l'architettura ibrida e l'implementazione dei kernel possono produrre limiti
> Variazione
> importante tra backends. sequenza
>
> **Qwen3.8-27B.** Il denso asservimento **Qwen3.8-27B** diventa il primo sfidante di qualità locale da aggiungere al vuoto
> Scala. Qwen pubblica un contesto fino a 1M in base alla distribuzione e ai punteggi editor di 73 su autorizzazione
> Terminale-e-Bench 2.1 e non è così 61,7 su SWE-bench Pro. Questi numeri non giustificano la sostituzione di Coder-Next per impostazione predefinita:
> prova.
> sia con la stessa imbracatura, lo stesso contesto, gli stessi strumenti e lo stesso budget temporale. **Coder-Next rimane l'unico
> base locale specializzata ed economica; Qwen3.8-27B è la sfida da dare priorità quando la qualità conta più risorse
> ** I tassi API Qwen3.8] dipendono dalla regione e non devono essere presentati come prezzo mondiale.

>
> **Qwen3.8-Omni-Flash.** Da quando? 17 Settembre 2026Alibaba offre anche questo modello precedente API multimodale: testo, immagine, casuale
> input audio e video, testo in uscita, chiamata funzione, pensiero configurabile, ricerca web, cache contestuale, messaggio
> **1M tokens of contestualizzazione** e fino a raggiungere **131 072 tokens of output casual** via Gatto Complezioni o RisposteAPI.
> routing per la scansione screencast, colloqui, interfacce o documentazione multimodale; ** non sostituisce**
> Qwen3-Coder-Next come base di codice locale o Qwen3.8-27B come sfidante Scala qualità-primo.
> a seconda della regione di distribuzione: tenere questi dati fuori dalle regole di routing sostenibili e controllare Model Studio a distanza
> Tempo di scelta.

<!-- section: s-3 -->
### Lato Anthropic

| Modello:         | API ID urgente              | Tariffa (input/output / M tokens) | Backgroundgrounds          | Sforzo di default | Il ruolo attivo in questa guida                                                           |
|----------------|---------------------|---------------------------------|-------------------|-------------------|------------------------------------------------------------------------------------|
| **Fable 5.2**  | `claude-fable-5-2`  | $8 / $40                        | 1M (uscita 128K) casuale  | `high`            | Frontier: ragionamento a lungo termine ed esigente quando Opus 5.5 non è sufficiente      |
| **Opus 5.5**   | `claude-opus-5-5`   | $4 / $20                        | 1M (uscita 128K) casuale  | **`medium`**      | Difetto agente: codifica autonoma, architettura, debug e grandi refattori dovuti      |
| **Sonnet 5.5** | `claude-sonnet-5-5` | $2 / $10                        | 1M (uscita 128K) casuale  | `high` API        | Micro-dev / compiti ben specificati; `medium` consigliati per agentic coding bounded interfere |
| **Haiku 5.5**  | `claude-haiku-5-5`  | $0.10 / $0.50 (prompt ≤ 100K)] []]]]   | 1M (uscita 128K) casuale  | `medium`          | Lavoratori, smistamento, estrazione, tronchi, sub-agenti a basso rischio                     |

> **Corrente di routine:**Anthropic raccomanda che la maggior parte dei flussi di lavoro inizi con probabilità **Opus 5.5**,
> il cui sforzo predefinito è `medium`, quindi regolare lo sforzo prima di cambiare il modello. **Sonnet 5.5**, l'argomento
> La codifica agenteca ben specificata inizia utilemente a `medium` e sale a `high` per compiti più lunghi o
> difficile.
> `xhigh` (notato) : **E' un'altra cosa.** in questa guida) e `max` sono riservati per i casi in cui le evali mostrano un guadagno. **Haiku 4.5 non si può fare
> Haiku 5.5, che lo sostituisce, lo sostiene con probabilità `medium` per default.** I paragrafi qui sotto su Sonnet pianificazione 5 / Opussure 5 rimangono i punti di riferimento della direzione
> migrazioni
> Non sostituiscono questa matrice attiva.

> **Migrazione API A proposito di: Opus 5.5 / Sonnet 5.5.** I due modelli impongono più disciplina al cliente che alla scorta
> generazioni precedenti: il pensiero adattativo è la dieta normale, la conseguente *strumento forzato usare* (`tool_choice: any/tool`)
> ritorna un errore 400, e l'argomento *blocchi di pensiero* devono rimanere attaccati al loro modello e alla conversazione che li ha portati
> **Opus 5.5** respinge anche i parametri di campionamento non standard e la procedura guidata di precarica; il suo sforzo di correzione
> predefinito è `medium`. **Sonnet 5.5** Utilizzazione `thinking: {"type": "between_tools"}` per rimuovere il pensiero iniziale
> (`low`] a favore di `high` solo), e ora restituisce il testo intermedio tra le chiamate degli strumenti in blocchi `thinking`.
> Su Claude API e Google Cloud, entrambi i modelli utilizzano gli attuali strumenti per computer-utente
> `computer_toolset_20260801` piuttosto che `computer_20251124`. Un modello di migrazione deve quindi testare **payloads, sommario
> lo streaming, gli strumenti e il curriculum di conversazione**, non solo sostituire il modello ID.

> **Sonnet 5**] Sonnet 4.6 `claude-sonnet-4-6`], sempre disponibile allo stesso prezzo aggiunto
> $3/$15) come autista giornaliero.*drop-in sostituzione[ accidentale* Il mio nome API, con tre cambiamenti comportamentali per arrivare
> sapere prima di migrare:
> - **Il pensiero adattivo abilitato da default** ; il manuale di pensiero esteso ( :`thinking: {type: "enabled"}` con la forza
>   `budget_tokens`) ora ritorna un altro ** errore 400** — migra a pensiero adattativo.
> - ** Parametri di campionamento bloccati**: qualsiasi valore non di default dell'esecuzione `temperature`, `top_p` o `top_k` Responsabilità
>   un errore 400.
> - **Nuovo tokenizer** (stessa linea comeOpus 4.7+): ~30% più gettoni per lo stesso testo (fino a 1.35x
>   Il tokenizer può sempre aumentare il numero di token caricati, quindi contare il rendimento
>   veloce con il punto finale di incontro di token e vedere i `max_tokens` stretti.
>
> Altre specificità operative: **Effort Controllo automatico** generalizzato (basso livello) : → **Traduzione:**, difetti *alto livello* su di noi
> l'API e non è così Claude Code), prima volta **cybersecurity salvaguarda il tempo reale** su un Sonnet (un rifiuto ritorna in HTTP)
> 200 con la forza `stop_reason: "refusal"`, non in errore — da gestire nel cliente), no Priority Tier, output assegnato 128K
> ([300K in lotto tramite l'intestazione beta `output-300k-2026-03-24`)]) È anche il nuovo modello predefinito degli aerei aggiuntivi
> Gratis e Pro su claude.ai.

> **Aggiornamenti comuni**: caching rapido e batching (-)–50% input e output) si applicano a *tutti i giorni* modelli
> Claude. Il prezzo della lettura della cache dipende dal modello: **Fable 5.2 costi $0.20/M tokens in cache leggere**
> (rispetto a $ accennare)$0.25/M per l'uso Fable 5.1). Batch rimane utile per il lavoro non di emergenza: riassunti PR raggruppati, dovuti
> Fable 5.2, Opus 5.5 e Sonnet 5.5] includono il contesto 1M a tariffa fissa
> standard, senza sovraccarico di contesto lungo.
>
> **Precisione tariffaria.** La cache di lettura è degno di nota **0,025× input aggiuntivi** su di noi Fable 5.2/5.1 ($0.20 e $ accadde$0.25/M),
> **0,05×** su di noi Opus 5.5 e non è così Sonnet 5.5 ($0.20 e $ accadde$0.10/M) e gli effetti negativi 0,1× su richiesta Haiku 4.5. Haiku 5.5 è l'unico modello attuale
> con un'immagine **più palier di lunghezza rapida**: al di là di una 100 000 token di entrata (cache incluse), tutte le sue tariffe sono soggette
> Numero cinque volte. Fable 5.2 $4/$20, Opus 5.5 $2/$10, Sonnet 5.5 $1/$5. Modalità veloce: Fable 5.2 $16/$80,
> Opus 5.5 $8/$40]. `inference_geo: "us"` si applica un moltiplicatore di 1,1 × sulle categorie interessate.

> **Claude Fable 5.2 sostituisce Fable 5.1 nel routing attivo di questa guida.** Particolare attenzione
> Tecnico: ID parametri `claude-fable-5-2` (`anthropic.claude-fable-5-2` su Bedrock), contesto esterno **1M**, uscita corrente **128K**,
> **$8/$40**, scrivere cache 5 Min $10 e non è così 1 h $16, cache lettura **$0.20/M**, lotto $ compensare$4/$20, modalità rapida `speed: "fast"` à
> $16/$80, il pensiero adattativo sempre attivo, lo sforzo predefinito `high`, cutoff giugno impegnati 2026, ritiro non prima dell'inizio
> 9 Novembre 2027. Stessi vincoli come : 5.1: **30 giorni di conservazione obbligatori (no RDA senza autorizzazione)
> Esprimere la voce**, `tool_choice: any/tool` e preriempire in termini di tempo 400, campionamento a omit, no Priority Tier, no strutturato
> outputs per le organizzazioni CMEK. Il modello genera circa probabilità 30 % più veloce rispetto alla 5.1. **Il mio amore 5.2** è la stessa cosa
> modello con meno garanzie, riservato alle organizzazioni verificate.
>
> **Positioning.** La matrice ufficiale rimane "la maggior parte dei carichi di lavoro iniziano con Opus 5.5 "; ci muoviamo verso l'eliminazione
> Fable 5.2 se le valli `xhigh` o [[`max` rimangono insufficienti a ragionare esigente o a lungo termine.
> Novità da incorporare in routing: on FrontierCode 2.0 (che misura se i manutentori interferirebbero con il cambiamento)
> Anthropic reportage **Fable 5.2 `high` à 45,3 %, a livello diOpus indicati 5.5 il miglior sforzo (preferire45,5 %), versare environ la quantità
> Metà del costo per compito assegnato**. Editor di punteggi al massimo sforzo: FrontierCode casuale 2.0 **49,1 %** (Opus 5.5 45,5; Astra :
> 42,8 ; Fable 5.1 32,4FrontierSWE / retromarcia2 **69,9 %** (Opus 62,3 ; Astra : 65,5), Indice del lavoro remoto 41,3 % contro l'inquinamento 21,3 %
> per Opus. Sulla breve codifica il divario è piccolo: Terminal- allenamentiBench 4.0 67,6 % contro l'inquinamento 66,4 % (Opusibile) `xhigh`), nella prospettiva
> Le misure indipendenti Vals confermano il grado: uguaglianza con probabilità Opus 5.5 su Terminal-obiettivoBench 4.0
> ([65,15 %] %), Opus davanti a SWE-bench Multimodal (eliminazione)70,2 % contro l'inquinamento 62,3 %).
> **Mini-SWE-agent** di Vals, questa uguaglianza corrisponde a circa **$14,56/Task for Fable contro l'abbandono
> $12,04 per l'Opuscolo**, con Fable più veloce (aumento)55 min contro l'incollaggio 64 min): il vantaggio del costo per compito annunciato
> di un'altra Anthropic on FrontierCode impegnati **non si diffonde** Le conseguenze pratiche:
>
> ```text
> Opus 5.5 High insuffisant (capacité)        → Fable 5.2 avant Opus 5.5 Max, à mesurer sur le benchmark Scala privé
> Décision difficile ponctuelle (advisor)     → Fable 5.2 low/medium
> Mission longue autonome                     → Fable 5.2 high (low/medium finissent plus souvent le tour trop tôt)
> Tâche bornée, bug UI/front, review courante → Opus 5.5 ou Sonnet 5.5 restent les meilleurs achats
> ```
>
> ** Cambiamenti di cambiamento dal Fable 5.1** (controllato nella guida ufficiale di migrazione):
> - **Il controllo del prefisso** ora vale per tutti gli account. Restituire un blocco di thinking con un `system`,
>   strumenti `tools` o una cronologia diversi da quelli usati per generarlo restituisce un errore 400 (`The block is bound to a different
>   conversation`). **Una modifica all’elenco degli strumenti MCP tra due richieste conta come modifica**. Mantieni
>   fisso l’elenco per tutta la sessione oppure usa le modifiche agli strumenti durante la conversazione (beta
>   `inline-tools-2026-09-15`, tramite messaggi con `role: "system"`). Fai attenzione agli harness che caricano strumenti
>   su richiesta e cambiano `tools`;
> - **Fable 5.1 e non è così Opus 5.5 non leggere i blocchi di pensiero di casualità Fable 5.2** (sono cancellati senza errore, quindi il fattore
>   ragionamento è perso in silenzio); Fable 5.2 leggi quelli di 5.1 e Opus 5.5.
>   [`fallbacks: "default"`], beta `server-side-fallback-2026-07-01`) mira solo `claude-opus-4-8` e mostra solo [[]
>   `claude-opus-5`: registra il modello eseguito; casuale
> - `computer_20251124` restituisce 400 (escluso Bedrock): usare `computer_toolset_20260801`;
> - il consigliere di un esecutore Fable 5.2 deve essere `claude-fable-5-2` o `claude-mythos-5-2`;
> - pensiero conta in aumento `max_tokens` (rischio di attesa `stop_reason: "max_tokens"` prima di qualsiasi testo) e necessità Fable 5.2 per la sua
>   ** limite di tasso proprio**, distinta da Fable 5/5.1Nuove beta utili: compattazione su richiesta
>   (`compact-2026-09-04`), blocchi mentali (attualizzanti`thinking-binding-controls-2026-08-01`, con l'aiuto
>   `prefix_mismatch_behavior: "drop_block"` solo come palliative).
>
> **Comportamenti che influiscono direttamente sulla qualità delle differenze e sul costo aggiunto** (promping guida automatica) Fable 5.2) :
> - **Proprietà del codice.** Senza istruzioni esplicite, il modello aggiunge alla struttura esistente, duplica e segnala la necessità
>   problemi simili invece di correggerli. La frase proposta da Anthropic ("Questa base di codice è tua...") non significa
>   unire il codice duplicato in circa la metà dei test, ma il costo circa 1,5 × token di uscita, aggiungere vuoto
>   test e documenti non richiesti e cambia un comportamento esistente in un processo in sei a dieci. **Per i biglietti
>   alla differenza minima di questa guida, non aggiungerla**; riservarla ad un compito esplicito di deduplica o refactor, ordinarla
>   e rileggere il diff piuttosto che il riassunto, che spesso omette piccoli cambiamenti.
> - **Over-delegation.** A proposito di: `xhigh` e non è così `max`, Fable 5.2 può lanciare i subagenti per rileggere il proprio lavoro, e la conseguente
>   i subagenti possono rappresentare una gran parte del costo della sessione. Audits le linee di `AGENTS.md`, abilità e frequenza
>   file di agenti che invitano a delegare, e controlla il modello predefinito di subagenti.
> - **Premature termina la fase finale** (elenco delle attività rimanenti, offrono di continuare) più frequenti per arrivare `low` e non è così `medium`:
>   per una lunga missione, aggiunge l'istruzione "non fermarsi finché non c'è ancora lavoro richiesto", mentre
>   distinguere l'ostacolo ordinario (da trattare) e il blocco deliberato (file proibito, guardia: da lasciare e anticipare
>   Mantenere le proprie conferme per azioni rischiose.
> - **Bilancio del server ̄circuit break.** Il mondo del lavoro `task_budget` API è indicativo: fisso a frequenza **soffitto esterno** costo, prezzo
>   numero di chiamate, durata e numero di tentativi nell'imbracatura. Troppo stretto `max_tokens` può interrompere
>   Fable prima del primo testo visibile, perché i token di pensiero contano nell'output.
>   silenzioso, utilizza gli aggiornamenti tool-to-tool quando disponibili invece di moltiplicare i rilanci.
> - **Istruzioni inerite per essere purificato** : "risposta senza deliberazione" non interrompe la riflessione da `medium`
>   (meno sforzo); linee "tratta questa risposta come finita" dal prompting temporaneo Opus 5.5 fare il lavoro
>   il modello molto meno in grado di recuperare con i propri errori; i bilanci dei gettoni scritti nel prompt dei comandi
>   può essere rimosso a `high`/`xhigh` senza perdita; le precauzioni di archiviazione obsolete riducono la memoria guidata
>   Questo è esattamente il ruolo di `/doctor prompt-audit` (sezione 3, subagenti).
>
> **Accesso e quota.** Claude Code **2.1.321+** (`claude --model claude-fable-5-2` ; gli alias : `fable` dipende da:
> I piani Max/Ultra ammissibili possono utilizzare Fable fino a una frazione incassata **50 % della percentuale di ricezione
> limiti settimanali**, a seconda delle condizioni effettive; l'uso su Pro può dipendere da crediti aggiuntivi previsti
> o promozione temporanea. Non confondere
> Mai. **modello visibile**, **quota inclusa** e non è così **fatturazione API/crediti ufficiali** : controlla la schermata di consumo e la frequenza
> Recalibrare lo sforzo `medium`, `high` e `xhigh`] e il costo per compito.

> **Nota tokenizer :**: il nuovo tokenizzatore è stato introdotto dal **Opus 4.7** (Non ho paura) 4.8) e genera fino a ~ stanziamenti ~35% della popolazione
> token oltre aOpus alternative 4.6 per lo stesso testo. **Sonnet: 5 adottare la stessa linea abituale** (~30% più gettoni rispetto alla quantità
> Sonnet 4.6], fino a 1.35x a seconda del contenuto). La penalità di conteggio rimane rilevante per Opus a pretendere
> prezzo identico; su Sonnet preciso 5, la tariffa permanente **$2/$10** compensa una gran parte dell'aumento del numero percentuale
> di gettoni in relazione a Sonnet 4.6. Il passaggio Opus 4.7 →] 4.8 non comporta alcuna penalità aggiuntiva per il tokenizer.

> **Opuscolo 5 e la transizione dal vuoto 4.8** Opuscolo 5 è ora il segreto **Modelli su misura Anthropic difficile da default** Votazioni
> identico a quello di Opus 4.8 ($5/$25) Guardia militare 4.8 solo come un fallback di compatibilità o un riferimento storico.
> - **Modalità veloce** ($10/$50, ~2.5x velocità standard): per un compito difficile ma preciso *Interattivo:* (debug in coppie),
>   Opuscolo 5 Veloce è spesso un acquisto migliore di Fable.
> - **Effort Controllo automatico**: guida per sforzo rimane il passo esplicito prima di arrivare Fable 5.2. On Opussure 5, `xhigh` e non è così `max`
>   richiedono che il pensiero rimanga attivo; `thinking: disabled` con questi livelli restituisce un errore 400.
> - **Flussi di lavoro dinamiche** rimane rilevante per il parallelismo su scala codebase; in dotazione Claude Code, completalo ora esatta
>   **Agent Teams** rimane sperimentale e **Ultrareview** in anteprima di ricerca: don't trasformarli normalmente
>   e ancora nelle dipendenze obbligatorie del flusso di lavoro.

> **Nota Claude Managed Agents :** (piattaforma ospitata, beta pubblica dal mese di aprile) 2026, header urgentemente
> `managed-agents-2026-04-01`) : dal Codice con Claude (articolo6 Maggio 2026), la piattaforma aggiunge precedenti **Risultati in corso** (grading)
> indipendente all'ingresso, loop di revisione se l'uscita non passa), **orchestrazione multi-agent frequenza** (fino a tre)
> 20 un sub-agente specializzato parallelo su un filesystem condiviso, **webhooks** (beta)]
> **Sognare l'amore** (anteprima di ricerca: la cura della memoria tra le sessioni).
> tasso API + $0.08 all'ora di sessione attiva. Per questa guida, questa è la terza opzione sulle missioni lunghe,
> accanto a Fable mono-agent e Opus + Dynamic Workflows — rilevanti soprattutto se si desidera un'imbracatura ospitata con frequenza
> Criteri di successo eseguibili (Outcomes è la versione della piattaforma della "gate of review" nella sezione Garanzia 15A).

> **OpenAI Agenti API** è il ciondolo lato ospitato OpenAI: utilizza il metodo
> imbragatura gestita da Codex con ** sessioni sostenibili[**], compattazione e recupero gestito, MCP e sub-agenti con contesto isolato.
> Due primitivi si materializzano direttamente il contesto ingegneristico della sezione 10: **tool search**] non fa pagare l'eliminazione
> definizioni degli strumenti che quando diventano rilevanti, e ** programmazione tool call** consente stringing, aggregazione
> parallelizzare e filtrare le chiamate prima di reiniettare solo risultati utili.
> OpenAI a Anthropic: confronto **]Agents API**, Claude Managed Agents and Local imbracature a costo di autorizzazione
> cambiamento accettato, mantenendo le stesse specifiche, test e regole di arresto.
>
> **L'uso del computer** può anche funzionare in un browser ospitato da OpenAI].
> crea la sessione, approva esplicitamente ogni nuova origine e gestisce l'autenticazione sensibile stessa.
> Un'approvazione originale non è una conferma per azione: per l'acquisto, la cancellazione o altre transazioni
> mantenere un runtime controllato o un gate applicativo separato.


Caratteristiche operative complementari:

| Modello:         | Relativamente la latenza | Prompt nascondiglio     | Batch (–):–50%) | Specifiche operative necessarie                                                                        |
|----------------|------------------|--------------------|--------------|---------------------------------------------------------------------------------------------------|
| **Fable 5.2**  | Moderatore          | Sì, leggere $ compensare$0.20/M | Sì.          | Il pensiero adattivo sempre su; difetto `high` ; sforzo per messaggio ; modalità veloce $ casuale$16/$80            |
| **Opus 5.5**   | Moderatore          | Sì.                | Sì.          | Il pensiero adattivo sempre su; difetto **`medium`** ; basso livello→Max.                                     |
| **Sonnet 5.5** | Svelto!           | Sì.                | Sì.          | Il pensiero adattivo; predefinito API `high`, ma `medium` raccomandato per codificare agentic ben specificato |
| **Haiku 5.5**  | Più veloce   | Sì, leggere $ compensare$0.01/M | Sì.          | Il pensiero adattativo predefinito; lo sforzo predefinito `medium`; il livello di prezzo oltre 100K tokens assegnati |

<!-- section: s-4 -->
### OpenAI Codex]]

**GPT‑6.2 Sol** è il difetto raccomandato per la correzione **codifica complessa e ripetuti workflow agente** In un'altra Codex quando disponibile. OpenAI posizionarlo come più efficace dal compito di Sol casualità 6.1, allo stesso tasso accelera API. **GPT‑6 Luna** obiettivi focalizzati, ripetibili e ad alto volume attività; **GPT‑6.1 Terra** è il livello intermedio. **GPT‑6.2 Astra** rimane l'escalation di capacità per i compiti più esigenti.

| Modello:          | API significare        | Prezzo standard / prezzi 1 Token M (input / output) | Ruolo consigliato in questa guida |
|-----------------|---------------|---------------------------------------------|-------------------------------|
| **GPT‑6 Luna**  | `gpt-6-luna`  | **$0.10 / $0.50** | Micro-dev, modifiche meccaniche, test semplici, ordinamento e lavoratori a basso rischio |
| **GPT‑6.1 Terra** | `gpt-6.1-terra` | **$1 / $5** | patch locale e recensione mirata quando Luna manca giudizio casual |
| **GPT‑6.2 Sol** | `gpt-6.2-sol` | **$2 / $10** | **Default Codex Agent Medium**: Emissione end-to-end, funzionalità multi-file, test, PR, revisione e stewardship |
| **GPT‑6.2 Astra** | `gpt-6.2-astra` | **$8 / $40** | Frontier: problema molto ambiguo, contratto critico, escalation della capacità produttiva |
| GPT‑6.1 Sol / GPT‑6 Astra | `gpt-6.1-sol` / `gpt-6-astra` | $2 / $10 ; $10 / $50 | I fallimenti se le versioni 6.2 non sono disponibili; basi storiche precedenti |

> **GPT‑6.1 Terra riempire il foro tra Luna e Sol.** Pubblicazione 26 Ottobre 2026 (`gpt-6.1-terra`),
> che costa **$1/$5** (input registrato $)$0.05/M), cioè la metà del terreno risultante 6.1, con la stessa finestra di riguardo 1,05M tokens.
> è disponibile in ordine ChatGPT Lavoro e formazione Codex (Plus, Pro, Enterprise, Edu; non nella scheda Chat) e richiede un aumento Codex
> Recenti CLI (in inglese)0.159+ a seconda delle fonti). OpenAI posiziona su correzioni di bug comuni, uso del computer, interferenza
> visione e scrittura; per la codifica esigente, ora preferisce **Sol 6.2 o Astra 6.2**.
> 50,3 % su Terminal-obiettivoBench 4.0 a max sforzo (obiettivo21,5 % per l'acquisto GPT‑5.6 Terra) Per questa guida, Terra diventa l'unico **candidato
> naturale per le patch delimitate e la revisione di piccoli diff** quando Luna è troppo equo e Sol troppo costoso: per essere separati
> prima di cambiare la matrice.

> **GPT‑6.2 Sol e Astra**: 1,05M token di finestre, di cui 922 Maximum input K e 128 Maximum output K.
> Cache letto: $ impegnati$0.10/M per Sol, $ accennare$0.40/M per Astra; cache scrittura automatica 30 min per l'acquisto 1,25× input, probabilità 12 h à 2,5×.
> Oltre 272K token di ingresso, ingresso/cache rate doppie e la velocità di uscita è moltiplicata per 1,5
> l'intera richiesta. Batch è 50% del tasso standard; Flex non è offerto su nuovi modelli 6.2.
> Non trasporre questi prezzi alla quota di sottoscrizione. Sol 6.1 Medium e Astra 6 La luce rimane in calo se viene utilizzata
> 6.2 non sono disponibili versioni. Stewardship è una capacità di cablaggio, non modello. Benchmarks indicati
> Questo non è il caso per i modelli 6.2.

> **Ultrafast è un service tier, non un nuovo modello o livello di sforzo.** Punto di riferimento storico: per rivendicare GPT-6 Astra, l'API Ultrafast
> Obiettivi fino a ~8× la velocità di Standard e fattura in contesto breve **$60/M input $ urgente$6/M in ingresso cache, $ precedenti$75/M cache attiva
> Scrivere e $ accattivanti$300/M uscita automatica**. Usarlo solo quando la latenza domina in realtà il costo totale; per loop successivi
> Agentics con molte chiamate degli strumenti, OpenAI raccomanda una connessione WebSocket Responses persistente.
> non supporta la residenza dei dati dell'UE: funziona nel trattamento globale o con residenza degli Stati Uniti.
> prodotto, Astra Ultrafast è incluso in particolare in quantità **Produrre la ricerca 500** e alcune offerte di Enterprise, pertanto non cambia
> routing di qualità di questa sezione: `Astra Standard` e `Astra Ultrafast` hanno la stessa capacità di modello.
> Su GPT‑6.2, controllare i tassi e i diritti del piano prima dell'attivazione; si riserva terzi veloci solo a loops precedenti
> interattivo molto limitato dalla latenza, non in attesa di CI.

In questo caso **Codex / Lavorare**, ragione con livelli visibili dovuti **La luce del sole → Medioriente → E' un'ottima idea. → Esclusivamente → La mia vita è un'altra**. L'impostazione predefinita di questa guida è **Soil Medio e Medio**, **Luna alta** per micro-loops e frequenza **Astra Lights** per un'escalation di capacità. `Ultra` è più di una singola corsa mono-agent ed è redditizio solo se il lavoro può effettivamente rompere in assi indipendenti. API, i nomi di livello rimangono evidenti `low/medium/high/xhigh/max` in base al modello: non confondere la formulazione prodotta con il valore portatile di correzione `reasoning.effort`.

Il mondo del lavoro GPT‑5.6 i modelli possono rimanere disponibili durante il rollout, ma non sono più il percorso attivo predefinito per questa guida.

<!-- section: s-5 -->
#### Cinque dimensioni da non confondere

| Lever:                            | Cosa cambia?                                                                                     | Pratiche regole                                                                                                           |
|-----------------------------------|-----------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|
| **Model**] significa                        | Capacità, velocità e prezzo: Luna, Terra, Sol urgente 6.2 o Astra uguale 6.2.                                 | Luna per il limite; Sol 6.2 per agentici ripetuti; Astra solo quando la capacità superiore riduce le coperture. |
| **Effort**]]] significare                        | Bilancio motivante: formulazione Codex Luce→Ultra; API `low/medium/high/xhigh/max` Secondo il modello. | Terreno: Media predefinita; Luna: Alto; Astra: Luce; aumentare solo se la pianificazione/verificazione garantisce.   |
| **`reasoning.mode: "pro"`** (API) | Più lavoro di modello per una risposta finale più affidabile.                                    | Indipendentemente dallo sforzo; confrontare standard/pro su compiti rappresentativi.                                          |
| **`ultra` come uno sforzo Codex**    | Alcuni SDK/harness riescono Codex ora esplodere `ultra` come un livello di ragionamento superiore a quello `max`. | Trattala come una capacità di imbracatura, non come valore portatile di Responses probabili API.                             |
| **Ultra / Multi-Agent**]           | Orchestrazione di diversi agenti o sessioni a seconda della superficie prodotta/aggiustaAPI.                         | Utilizzare solo se il lavoro effettivamente si separa in parti indipendenti.                                          |

In questo caso **Risposta API**, il valore massimo documentato dell'esecuzione `reasoning.effort` rimane invariato `max` e non è così **Multi-agent aggiunto** rimane una funzionalità beta distinta. In qualche imbragaturaCodex, casuale `ultra` può invece designare uno sforzo di ragionamento. Pertanto, non dedurre mai la semantica dalla parola "ultra" da sola: log la superficie, il modello, lo sforzo e il numero effettivo di agenti. OpenAI non pubblica un moltiplicatore di costi fissi; la misurazione totale dei costi, la latenza e il tasso di successo sul tuo repository prima della standardizzazione.

<!-- section: s-6 -->
#### Astra: Controllo delle missioni lunghe

Astra aggiunge tre funzionalità particolarmente utili per gli agenti:

```text
async tool calling
→ continuer à raisonner ou appeler d'autres outils pendant qu'un outil lent s'exécute

mid-turn steering
→ ajouter une contrainte ou changer de direction sans redémarrer toute la mission

configuration updates
→ changer l'effort en cours de trajectoire sans casser inutilement le préfixe de cache
```

Per un agente backend, preferisce l'autorizzazione **Risposta API** : lo strumento che chiama Astra è la superficie di riferimento. Astra non accetta limiti `reasoning.effort = none`né le impostazioni personalizzate di casualità `temperature` / `top_p` Documentato come incompatibile. **Modalità rapida** API può andare fino a ~2× più veloce per evitare **2× prezzo standard** ; non ha SLA di latenza e non deve diventare il default di una lunga missione.

<!-- section: s-7 -->
#### Disponibilità e superfici disponibili ChatGPT / Codex

| Informazioni generali                  | Accesso al modello e modalità accelerata                                                                                                               |
|--------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| **ChatGPT Lavorare / lavorare Codex** | GPT‑6.2 Sol e Astra, GPT‑6.1 Terra, Luna e fallback secondo piano, cliente, spazio di lavoro e rollout.                                              |
| **GPT‑6.2 Sol / Astra sbagliato**  | Inoltre, Pro, Business, Enterprise ed Edu in Codex/Work secondo i diritti; Light→Ultra controlli di sforzo secondo i parametri disponibili. |
| **GPT‑6 Luna**           | Modello economico per compiti focalizzati e ripetibili in Work/attrazioneCodex.                                                            |
| **Ultra / multi-agent**  | Da riservare agli assi indipendenti; non assimilarlo a "più riflessione" su una catena sequenziale.                    |
| **API**                  | `gpt-6.2-sol`, `gpt-6.2-astra`, `gpt-6.1-terra`, `gpt-6-luna` tramite superfici supportate; controllare gli strumenti e lo sforzo per modello.                |

I diritti effettivi dipendono sempre dal piano, dalla regione, dallo spazio di lavoro e dal rollout. Mai codificare una regola di prodotto durevole dal nome di un abbonamento.

<!-- section: s-8 -->
#### Caching, sicurezza e salvaguardie

GPT‑6.2 Sol fatturare la cache in ingresso **$0.10/M** contro $2/M in input standard; le scritture della cache rimangono a vuoto 1,25× input. GPT‑6 Luna per il tempo libero **$0.01/M** in ingresso cache. Stabilizza la parte superiore del prompt (attiva`AGENTS.md`convenzioni Scala, contratti, regole di prova) e lascia diffs, logs ed errori di seguito.

> **Due leve di costo per volume.** Suggerimenti GPT‑6.1 Sol e non è così GPT‑6 Luna, Batch e Flex costi aggiuntivi 50 % in meno rispetto a
> Standard; su richiesta GPT‑6.2 Sol/Astra, Batch mantiene questa riduzione, ma Flex non è offerto.
> Utilizzarli per la tolleranza di latenza: audit pianificati, riassunti di PR raggruppati, generazione di set-up e smistamento
> massa. Non trasporre automaticamente queste tariffe API quota ChatGPT/Codex]: l'indicatore giusto rimane il costo per autorizzazione
> compito completato nella superficie effettivamente utilizzata.

GPT‑5.6 rimane classificato "High" ma non "Critical" in cyber. **GPT‑6 Astra (generazione originale) è il primo modello casual OpenAI classificato Critical in cybersecurity** Questo livello di capacità è accompagnato da un monitoraggio traiettoriale più rigoroso: nel caso di un nuovo sistema, la capacità di monitorare le prestazioni di un nuovo sistema non è limitata ad un nuovo sistema. ChatGPT/Codex, un compito legittimo può essere rallentato, interrotto o chiesto di validazione; API, il lavoro può essere interrotto.

Con Astra, rendere ancora più esplicita: filescope, rete, operazioni esterne, scrittura distruttiva, bilancio, durata, condizioni di chiusura e validazione umana. Punto utile per il codice sensibile: **Astra supporta la conservazione dei dati zero per i clienti API idonei**, mentre Fable 5.2 impone 30 giorni per impostazione predefinita, a meno che non espressamente autorizzato daAnthropic.

<!-- section: s-9 -->
#### Benchmarks e prudence derivate

Le cifre di lancio di Astra sono particolarmente forti in termini di disponibilità **agente di codifica e computer uso corrente**, ma deve rimanere attaccata alla loro imbracatura. OpenAI rapporti in particolare: Terminal- attrezzatureBench 4.0 **57,9 % Astra vs. frequenza 55,8 % Fable 5.1**DeepSWE aggiunto 1.1 **74,1 % vs. frequenza 67,4 %**, FrontierCode Extended interfere **64,5 % vs. frequenza 63,6 %** e i suoi compiti di migrazione interna DB dovuti **63,9 % vs. frequenza 57,8 %**. Su AutomationBench, Astra ha raggiunto l'obiettivo **41,4 % vs. frequenza 31,4 %** per il futuro Fable 5.1Queste sono le valutazioni pubblicate da precedenti OpenAI : utile come segnale, mai come verdetto su richiesta Scala.

La valutazione indipendente Analisi Artificiale Nuances fortemente l'immagine. **Coding Agent Index v casual1.4**, Claude Code + Fable 5.1 (`max`, con fallback) ottiene compensare **70** contro la violenza **67** per il futuro Codex + Astra (in inglese)`max`), ma Astra consuma circa l'aumento **4,0M tokens/task contro gli interessi 7,1M** e costi circa l'esercizio **$4,72/Task contro $ impegnati$9,18**. Sulla soglia **Intelligence Index**, Fable 5.1 `max` è anche di fronte a (particolare**66 - Non lo so. 61**) L'insegnamento giusto non è quindi "Astra > Fable" : **Fable mantiene un piccolo vantaggio di qualità aggregata in questi protocolli, Astra un grande vantaggio dell'efficienza delle attività in materia Codex**.

Astra pubblica anche un ottimo promemoria a lungo contesto su MRCR v apparent2 : **100 % à 256–512K** e non è così **96,3 % à 512K–1M**. Non trasforma queste partiture in permesso di inviare l'intero monopolio: oltre 272K, aumenta la sua tariffa e aumenta *contestazione del contesto* è ancora un problema di ragionamento, non solo di capacità fisica.

Per questa guida, la conclusione robusta diventa:

```text
GPT‑6 Luna High = micro-dev et workers Codex sous contrôle humain fort.
GPT‑6.2 Sol Medium = défaut Codex pour l'agentic coding end-to-end.
GPT‑6.2 Sol High = feature complexe, migration et reprise difficile.
GPT‑6.2 Astra Light = escalade de capacité avant de pousser mécaniquement Sol à l'effort extrême.
Sonnet 5.5 Medium = micro-dev Claude et tâches agentiques bien spécifiées.
Opus 5.5 Medium = défaut Claude pour l'agentic coding autonome.
Opus 5.5 High = architecture, debugging et refactor difficiles.
Fable 5.2 Low = escalade frontier quand Opus High reste insuffisant.
Astra vs Fable = décider au coût par changement accepté, pas au prix par token.
```

<!-- section: s-10 -->
### GPT‑6 Astra - Non lo so. Claude Fable 5.2: punto di riferimento storico di due frontiere

Questo confronto mantiene le figure dell'ordine GPT‑6 Astra originale: per il routing attuale, usa compensazioni GPT‑6.2 Astra Se il cliente lo propone, il suo tasso di corto standard è $ compensato$8/$40 (cache read $)$0.40/M) ; non gli attribuisce i risultati del vecchio Astra. Confrontare i modelli attuali sulla stessa imbracatura e deposito.

Confronta il prezzo **modello nella sua vera imbracatura**, non un numero di editor isolato. Fable 5.2 è meno costoso da token standard che GPT‑6 Astra, ma la differenza di costo per compito dipende dal nascondiglio, dallo sforzo, dagli strumenti e dalle ripetizioni.

| Assemblee | GPT‑6 Astra | Claude Fable 5.2 | Pratiche conseguenze |
|-----|-------------|------------------|---------------------|
| Arresto naturale | Codex / ChatGPT Lavoro / Responsabilità API | Claude Code / Messaggi API] [ | Misurazione del sistema completo casuale |
| Ingresso/uscita standard del prezzo (token M) | **$10 / $50** | **$8 / $40** | Fable a buon mercato nominale probabilità nominale |
| Cache read (M tokens) | **$1** | **$0.20** | Vantaggio Fable su prefissi realmente riutilizzati |
| Lungo contesto | 1,05M; sovraccarico oltre 272K casual | 1M; tasso standard | Preferire contesto mirato in entrambi i casi |
| Effort: Effort | La luce del sole→Ultra su superficie; API basso costo→massimo. | basso costo→max; adattamento pensiero aggiunto | Fable `high` per una lunga autonomia, `low` per ad hoc consigli aggiuntivi |
| Uso del computer | Capable, con orchestrazione e strumenti necessari | Risultati di editing forti | Controllare gli scenari riproducibili |
| Qualità del diff mergeable frequenza | Valutazione delle armi Codex | FrontierCode 2.0: 49,1 % al massimo sforzo secondo Anthropic] | Modificare i protocolli non rivelano la superiorità generale |
| Indipendenza delle misure necessarie | Valutazioni di terze parti disponibili | Vals: uguaglianza con Opus sul Terminal-obiettivoBench 4.0, retromarcia in multimodalenziale | In attesa di un confronto Fable 5.2 / Astra con imbracature simili |
| ZDR: | Clienti idonei API | 30 giorni predefiniti, eccezione contrattuale richiesta | Filtra i compiti per esigenze di riservatezza |
| Lungo missione | Strumenti asincroni, acciaio a medio giro | Sforzo per torre, pensiero legato alla storia | Proteggere lo stato, gli strumenti e le regole di arresto |

**Benchmark lettura.** Anthropic Annuncio di apertura Fable 5.2 di fronte a Astra su FrontierCode probabili 2.0FrontierSWE / retromarcia2 e OSWorld emergenti 2.1Ma sono in ritardo. **risultati editoriali**. L'indice dell'agente di codifica dell'analisi artificiale Claude Code + Opus 5.5 à Codex + Astra indica un diverso compromesso tra i tassi di successo, i costi e la durata; **non misurare Fable 5.2**. Confronto storico Fable 5.1/Astra non dovrebbe più essere utilizzato come regola di routing attuale. I risultati Vals indipendenti mostrano anche che Fable 5.2 non è sistematicamente migliore diOpus voluto 5.5.

Pratico routing regola:

```text
Micro-dev interactif, humain dans la boucle
→ GPT‑6 Luna High ou Sonnet 5.5 Medium

Issue standard end-to-end
→ GPT‑6.2 Sol Medium
→ Opus 5.5 Medium en review indépendante

Architecture / root cause / refactor difficile
→ Opus 5.5 High
→ GPT‑6.2 Sol Medium/High pour challenger

Sol High insuffisant par limite de capacité
→ GPT‑6.2 Astra Light puis Medium si nécessaire

Opus High insuffisant par limite de capacité
→ Fable 5.2 Low puis Medium si nécessaire

Même tâche vraiment frontier, choix Astra vs Fable
→ deux worktrees / même spec / mêmes tests
→ comparer coût total + minutes humaines + qualité du diff
→ humain arbitre
```

Non impostare una coppia permanente "Claude scrittore / supplente Codex revisore». **Lo scrittore sceglie per natura di compito assegnato**: Rispondendo a: 6.2 generalmente ha il risultato standard; Opus 5.5 Più facilmente possiede l'architettura, il debug e i refactors dominati dal giudizio. L'altra famiglia poi funge da recensore indipendente o da sfidante. Duplicare le due traiettorie complete è giustificato solo per un panificio o una decisione veramente front-line.

<!-- section: s-11 -->
### Modelli cinesi a peso aperto (Kimi K3], GLM‑5.2, e il resto del cluster)

Da metà strada2026una terza famiglia è stata fondata accanto adAntropic andOpenAI: i modelli precedenti **Apritori di livello anteriore cinesi**, che raggiunge un codice agentec vicino a Sonnet/Opus ad un costo molto più basso per token. Scala chi è già pilotando Claude Code e non è così Codex, non sono sostituzioni per il driver giornaliero, ma **una leva di costo su una specifica classe di subtask** e un altro **opzione sovranità** (self-host) per il codice sensibile.

**Trappola di categoria da mettere fuori dal outset temporaneo** : questi modelli non sono necessari **Non è vero.** nella stessa categoria come segue Qwen3-Coder-Next. Qwen Locale (in inglese)80B/3B actives) è davvero sfruttabile sul tuo laptop casual 128 Vai: Q equivale4_K_M lascia un margine molto ampio, Q risultante5_K_M è il miglior difetto e Q interfere6_K rimane praticabile.8_0 può essere caricato, ma deve essere convalidato con contesto, IntelliJ e non è così sbt veramente aperto. GLM‑5.2 (753B) e sopra tutti gli altri Kimi K3 (2.8T) non tenere premuto **Non è vero.** locale su richiesta 128 Vai: Questi sono modelli precedenti **API** (Zai, Moonshot, frequenza) OpenRouter) oppure **self-host su server multi-GPU**. Moonshot raccomanda un'implementazione certa Kimi K3 su config esatta 64+ acceleratori. Quindi non metterli mai nella scatola " Qwen locali": vivono nella casella " API terze parti" o "team server".

| Modello:      | Editore / accesso                                                                                                    | Architettura                                                                                             | Backgroundgrounds                 | Prezzo: API (in / out /M) corrente                | Perf benchmark (misure indipendenti / editor) :                                                                                             |
|-------------|--------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|--------------------------|---------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| **Kimi K3** | Moonshot — Effetti API, OpenRouter (`moonshotai/kimi-k3`), Kimi Code CLI; attrezzature **pubblicato full ponders** licenziamento Kimi K3 | Moee: 2.8Totale T, addestramento **104B attivato** ; 896 esperti, esperti 16 KDA + Warning Residuals, visione nativa    | Fino a 1M secondo il piano contingente | **$3 / $15** (cache-hit input $ casual$0.30)  | Editor di scanner con max sforzo e diversi imbracature; eccellente frontend e segnali a lungo raggio, da confermare su Scala                   |
| **GLM‑5.2** | Zipu/Z.ai — API OpenAI- **e Anthropic-compatibile**, GLM Coding Plan; MIT checkpoint pubblicato casuale                      | Moee: **753B** Totale BF aggiunto16 ; numero attivo non ufficialmente documentato; scarsa attenzione « IndexShare » falsa | 1M                       | **$1.40 / $4.40** (cache input $)$0.26) | Editor Scores: SWE-bench Pro alternativa **62.1**, TerminalBench preciso 2.1 81.0 con Terminus-obiettivo2 e non è così 82.7 migliore imbracatura; confrontare con protocollo identico |

**Sforzo di ragionamento.** GLM‑5.2 Exhibit: **E' un'ottima idea.** e non è così **Max.**. Kimi K3 Exhibit: `reasoning_effort: low | high | max`. La pagina del modello/l'esameAPI indica il **`max` predefinito**, mentre Kimi Code può definire un diverso difetto in base alla sua versione e al suo piano: quindi imposta sempre lo sforzo esplicitamente in un benchmark o nell'automazione. 1M dipende dal piano: 256K su Moderato, fino a arrivare 1M su Allegretto e sopra. Per un breve compito interattivo, inizia a prevedere `low` o `high` ; prenotazione `max` lunghe missioni in cui il costo dell'uscita è giustificato.

<!-- section: s-12 -->
#### Dove entrano in cerca *tonnellata* routing sessuale

```text
✅ Review de volume et triage à faible enjeu   → GLM‑5.2 (High) : tarif token très inférieur à Opus, mais coût par tâche à mesurer
✅ Extraction, classification, PR summaries bulk → GLM‑5.2 ou Kimi K3, en batch, quand le volume rend Sonnet/Terra cher
✅ Génération frontend / maquette web           → Kimi K3 (#1 Frontend Code Arena) si tu sors du périmètre Scala pur
✅ Second avis open-weight indépendant          → un modèle d'une 3e « école » d'entraînement casse les angles morts communs Claude/GPT
✅ Code sensible / air-gapped / souveraineté     → GLM‑5.2 en self-host (poids MIT) : rien ne sort de ton infra
```

```text
❌ Driver quotidien Scala à la place de Sonnet 5.5 : capable, mais tu perds l'écosystème (Claude Code, subagents, Metals MCP mûrs)
❌ Tâche interactive courte sur Kimi K3 en effort max : latence et verbosité, mauvais achat ; utiliser low/high
❌ Décision d'architecture critique en solo : garde Opus/Fable ou un vrai second avis Sol ; l'open-weight y reste un challenger, pas l'arbitre
❌ « Remplacer » Qwen local : mauvaise catégorie (voir piège ci-dessus)
```

<!-- section: s-13 -->
#### Accesso occasionale a GLM via OpenRouter

Per questo flusso di lavoro, non aggiungere un abbonamento GLM dedicato per impostazione predefinita. **GLM rimane un modello di backup**, per chiamare via [OpenRouter quando Claude Code, Codex e Qwen locale non ha risolto il problema. Questo preserva la diversità dei modelli senza aggiungere un nuovo account, chiave e piano da seguire.

Se GLM diventa uno strumento usato ogni settimana o porta un guadagno misurabile su una classe di attività, allora rivaluta il valore dell'accesso diretto Z.ai. Finché questa soglia non è raggiunta, la semplicità prevale.

<!-- section: s-14 -->
#### Il resto del cluster (per individuare, non adottare tutto)

`MiniMax M3` (Giugno) 2026) è il primo open-weight a combinare la codifica di confine, contesto casuale 1M *e non è così* multimodalità nativa (testa di peso aperto su SWE-bench Pro a compensare 59.0 Prima di tutto GLM‑5.2). `DeepSeek V4` declina una V alternativa4 Pro e V alternativa4 Flash ($)$0.14/$0.28 /M) imbattibile sul rapporto costi/contesto lungo per la selezione massiccia. Nessuno è "migliore ovunque": la scena open-weight di medie dimensioni.2026 è un cluster stretto dove la scelta giusta dipende dal compito e dal prezzo, non una classifica globale.

<!-- section: s-15 -->
#### Due riserve da tenere a mente

1. **Provenza e distillazione.**Kimi K3 si identifica come "Claude" in almeno uno scambio segnalato. **non è la prova della distillazione dovuta** e non consente alcuna conclusione scientifica o contrattuale sui dati di formazione. Se la provenienza conta per un cliente, richiede la documentazione dell'editore e tratta le informazioni come sconosciuto fino a quando non è pubblicato.
2. **Metodologia del Benchmark.** Le tabelle dell'editor mescolano diversi imbracature (KimiCode, apparent Claude Code, Codex, mini-SWE agent) e K temporaneo3 è sensibile a preservare la storia di successione *pensare a*. Le deviazioni visualizzate sono spesso meno di un punto: non sempre sopravvivono a un cambio di imbracatura. **panificio controllato sui vostri compiti reali** (versione fissa, autorizzazioni fisse, test di accettazione deterministica, costo per cambiamento accettato), non adottato sulla base di una classifica.

<!-- section: s-16 -->
#### Protocollo di Bake-off Scala: Kimi K3 contro GLM‑5.2]

Non solo confronta le risposte finali. **15 attività private**, mai pubblicato, diviso tra:

```text
3 bugs Scala 3 subtils : givens, implicits, variance, types opaques
3 évolutions Play / Tapir / Pekko sur 3 à 8 fichiers
3 tâches Spark / concurrence / performance
3 reviews de PR avec défauts injectés connus
3 tâches de tests : ScalaTest, ScalaCheck, mutation testing
```

Protocollo: stesso commit, stesso piano di lavoro iniziale, stessi strumenti, stesso limite di tempo, stessa rete, stesso pacchetto di contesto, stessi criteri di spegnimento e visualizzazione **tre ripetizioni per task precedenti**Kimi dovrebbe essere testato separatamente in ordine `high` e non è così `max`; GLM in attesa `High` e non è così `Max`. Se le imbracature non possono essere identiche, pubblicare due matrici e non assegnare la deviazione al modello da solo.

Misure obbligatorie:

```text
- tâche acceptée par les tests et la review humaine ;
- compilation, tests ciblés, mutation score ;
- défauts de sécurité ou de contrat détectés ;
- lignes ajoutées / supprimées et fichiers touchés ;
- nombre de reprises, tool calls et boucles identiques ;
- tokens input, cache, reasoning et output ;
- coût API total, latence et minutes humaines jusqu'au merge ;
- taux de réussite pass@1 et stabilité sur trois runs.
```

Adotta GLM o Kimi su un flusso solo se riduce il costo per cambiamento accettato[** senza** degradare le salvaguardie. Un punteggio di editor più alto ma più correzioni umane è una regressione, non un guadagno.

<!-- section: s-17 -->
## Regola decisionale per compito :

<!-- section: s-18 -->
### Quando usare l'immagine **Fable 5.2** (Mythos-class)

Fable 5.2 costi due volte Opus 5.5 per token ($ aggiunto$8/$40 contro $4/$20). Anthropic raccomanda di iniziare con l'aiuto **Opus 5.5 `medium`**, per arrampicarsi verso l'alto `high`, poi riservarsi Fable 5.2 alle valli ancora insufficienti o sul vero lungo orizzonte. Per un'escalation di capacità, prova preventiva **Fablet: `low`** prima di spingere sistematicamente Opus a prevedere `Extra`/`Max` :

```text
✅ Migration complète d'un framework (Play 2 → 3, Pekko, Spark upgrade)
✅ Session autonome multi-heures / multi-jours sans supervision
✅ Refactor cross-modules sur > 10 fichiers interdépendants
✅ Débogage d'un bug métier dont la cause est très loin du symptôme
✅ Décision architecturale sans "bonne réponse évidente" après essai Opus 5.5 High
✅ Tâche où tu paierais sinon un senior engineer une demi-journée
```

```text
❌ Tâche bien scoped et bornée : Sonnet 5.5 ou Opus 5.5 sont de meilleurs achats
❌ Revue de diff ou PR summary : overkill, coût inutile
❌ Génération de boilerplate ou de fixtures : Qwen ou Haiku suffisent
❌ One-liner ou patch ciblé : Luna High, Sonnet 5.5 Medium ou Aider
❌ Tâche dure mais interactive avec toi dans la boucle : Opus 5.5 Medium/High suffit généralement
```

> **Posizione 5.2.** Anthropic raccomanda di tenere premuto **Opus 5.5 come punto di partenza** per la maggior parte dei comandi
> Fable 5.2 `low` è un consulente **] su un punto**, da valutare su un compito limitato e verificabile; per una missione
> veramente autonomo, inizia a `high` per ridurre le estremità prematuri del tour. **costo per cambiamento casuale.
> accettata** sul benchmark privato Scala, piuttosto che generalizzare i risultati del fornitore.
> $0.20/M migliora l'economia di prefissi stabili lunghi. Quando il verificatore è affidabile, anche testare lo schema elettrico
> **Low → retry High overfail**] include recapture, latenza, revisione e convalida umana.

<!-- section: s-19 -->
### Prompting per la ricerca Fable 5.2: Struttura a lunga missione :

Fable 5.2 (in inglese) 1M, uscita fino a esaurimento 128K) non è solo un Opus più forte, ma mira ad esigere il ragionamento e l'horizon a lungo termine quando le valutazioni Opus rimangono insufficienti. La continuità dei blocchi di pensiero e la stabilità delle definizioni degli strumenti diventano vincoli di imbracatura, oltre allo sforzo configurabile dal messaggio. `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2`. Le leve sottostanti rimangono valide per arrivare 5.2 ; punti specifici per evitare 5.2 (proprietà del codice, over-delegation, prematura svolta termina, storica append-only, istruzioni ereditate da purificare) sono dettagliati nella nota Fable 5.2 della sezione su "Coastenziale Anthropic ».

Cinque leve specifiche:

1. **Carta della missione alla testa del contesto, nascosta.** Il blocco iniziale (oggettivo, non oggettivo, invariante, regole di arresto) non deve mai cambiare tra le torri: beneficia della punzonatura rapida e funge da ancora anti-guida su lunghe sessioni. Tutto ciò che evolve (stato, errori, diffs) va dopo.
2. ** Explicit persistent state. frequenza** In una missione multi-ora, richiede un file di stato`MIGRATION_STATE.md` in the worktree) che il modello aggiorna ad ogni pietra miliare: moduli elaborati, moduli rimanenti, decisioni prese, blocchi. Si tratta di questo file — non la conversazione — che è la base per la compattazione contestuale o il recupero.
3. **Checkpoint con criteri di uscita.** Taglia la missione in pietre miliari verificabili da comandi deterministici (classifica`compile`, test mirati, scalafmtCheckAll). Nessuna transizione al prossimo milestone senza attuale pietra miliare verde.
4. **Percorre lo sforzo a turno senza cambiare il modello.** Utilizzare`medium/high` per l'esplorazione, `xhigh/max` per una decisione davvero difficile, poi bisogna `low/medium` per un'edizione meccanica. Lo sforzo per messaggio conserva la cache ed evita di pagare il massimo livello durante la traiettoria.
5. **Se è necessaria una compattazione, impongono il suo contratto sommario.** Richiesta di preservare esplicitamente i problemi e le risoluzioni, le tracce provate o scartate, le decisioni e i vincoli, lo stato attuale, i punti aperti e i dettagli difficili da ricostruire. La compattazione del server gestisce già questa necessità; per una compattazione lato client, mai sommare in prosa gratuita senza questi campi.

Modelli di missione Fable 5.2:

```text
# MISSION (statique — ne pas modifier en cours de session)
Objectif : [migration / refactor précis]
Non-objectifs : [ce qui est explicitement hors scope]
Invariants : API publiques, contrats JSON, comportements listés dans AGENTS.md
Durée max : [N heures] — Coût max : [N USD] — Diff max par jalon : [N lignes]

# RÈGLES D'ARRÊT (statique)
Stop et rapport immédiat si :
- un invariant doit être violé pour avancer ;
- le même jalon échoue 2 fois pour des causes différentes ;
- build.sbt, migration DB ou contrat public doit changer ;
- l'estimation de durée restante dépasse 2x l'estimation initiale.

# PROTOCOLE (statique)
1. Lire AGENTS.md et MIGRATION_STATE.md.
2. Traiter UN jalon : plan court → diff → compile → tests ciblés.
3. Mettre à jour MIGRATION_STATE.md et committer le jalon.
4. Rapport de progression : jalon terminé, jalons restants, risques nouveaux, écart au plan.
5. Reprendre en 2.

# ÉTAT (dynamique — joindre la version courante de MIGRATION_STATE.md)
[état]
```

> **Contingenza per il futuro Fable 5.2.** Non abbassare silenziosamente una sessione: Fable 5.1 e non è così Opus 5.5 non rileggere l'argomento
> Fable 5.2 I blocchi di pensiero non modificano anche vecchi messaggi, prefisso di sistema o elenco strumenti aggiuntivi
> riutilizzando questi blocchi: il controllo della consistenza può produrre un errore 400.
> modello è indispensabile, salva lo stato utile in `MIGRATION_STATE.md`], poi si rifà a un contesto adeguato.
> `tool_choice: any/tool` è vietato Fable 5.2; usa `auto`] e convalida il risultato con uno schema rigoroso.

> **Nota Operativa**: Un interruttore di sicurezza può cambiare il modello effettivamente eseguito.
> codice crittografico a basso livello o sicurezza, registra questo modello, controlla che mantiene il livello di capacità prevista e anticipata
> questo caso nella regola di arresto piuttosto che scoprirlo durante la sessione.

<!-- section: s-20 -->
### Quando usare l'immagine **Opus 5.5**

Ecco, basta. **predefinito Claude Code per autonome agentic codificando**. Il suo sforzo predefinito è quello di eseguire `medium`, che cambia il routing rispetto all'Opusenziale 5 : inizia a : `medium`, fino a raggiungere `high` quando il compito è difficile, quindi utilizzare `Extra` (`xhigh`) oppure `Max` che se la durata o gli eventi lo giustificano.

```text
✅ Issue complète quand Claude possède la trajectoire exploration → patch → tests
✅ Architecture, migration et plan multi-modules
✅ Root cause éloignée du symptôme, implicits/givens/effets difficiles
✅ Gros refactor où la cohérence globale domine la simple édition
✅ Review indépendante d'une PR écrite par Codex
✅ Orchestration de sous-agents read-heavy avec contexte isolé
```

```text
medium → défaut agentique
high   → debugging / architecture / long-horizon difficile
Extra  → >30 min et chaîne réellement longue ; pas pour une simple tâche "importante"
Max    → exceptionnel, qualité absolue prioritaire et gain mesuré
```

<!-- section: s-21 -->
### Quando usare l'immagine **Sonnet 5.5**

La scelta migliore Claude quando viene ** il senior mantiene la sua mano fortemente preoccupata** o quando l'attività agentec è ben specificata. Anthropic consiglia esplicitamente `medium` per l'uso di strumenti ben strutturati e multistep, allora casuale `high` per compiti più lunghi o difficili.

```text
✅ Petit bug reproductible
✅ Refactor local bien scoped
✅ Tests métier et property-based tests ciblés
✅ Stack trace → diagnostic → correctif
✅ Feature claire dont l'architecture est déjà décidée
✅ Worker d'implémentation derrière un plan humain ou Opus
```

```text
low    → transformation simple / latence prioritaire
medium → défaut micro-dev et agentic coding bien spécifié
high   → tâche plus longue ou plus difficile
Extra / Max → seulement si tes evals montrent un gain ; sinon passer à Opus 5.5
```

La regola economica non è più "Sforzo massimo Sonnet prima dell'Opus." Se Sonnet High non riesce ad ottenere un limite di capacità, ** Opus Medio:** è spesso un acquisto migliore di un Sonnet Extra/Max esteso.

<!-- section: s-22 -->
### Quando usare l'immagine **Haiku 5.5**

Sistematicamente per le mansioni *ad alta frequenza e basso rischio*:

```text
✅ Sous-agents de lecture ou extraction à faible risque (sortie vérifiable)
✅ Résumés de logs, PR summaries rapides
✅ Classification et routage
✅ Éditions ciblées < 20 lignes
✅ Génération de messages de commit
✅ Appels répétitifs à faible risque, si le benchmark confirme le gain
```

> **Haiku 5.5 sostituire Haiku 4.5 come operaio Claude.** Costi per l'uso **$0.10/$0.50** fino a che il prompt voglia arrivare
> rimane sotto controllo 100 000 tokens (cache read $ casual$0.01/M), i.e. ** dieci volte inferiore a quello dell'ordine Haiku 4.5** e lo stesso prezzo ordine come sommato
> GPT‑6 Luna ; al di là di 100Token K di entrata, cache inclusa, tasso aumenta a $ salta$0.50/$2.50Backgroundgrounds 1M, uscita corrente 128K,
> Il pensiero adattivo attivo per impostazione predefinita e ** parametro `effort` supportato (`medium` per impostazione predefinita)**.
> la prefill ora restituisce l'ordine 400, `temperature`/`top_p`/`top_k` sono da omettere, forza `budget_tokens` Responsabilità 400, il segreto
> pensiero conta in aumento `max_tokens`, e una forzata `tool_choice` rimane accettata ma rimuove la riflessione prima della chiamata.
> Il tokenizer ha circa 30% più gettoni di Haiku 4.5. Regola pratica: mantenere i contratti subagent
> **100K tokens[**]] per rimanere nell'atterraggio inferiore, che unisce la disciplina di isolamento della sezione 3.
> Haiku 4.5 rimane attivo, ma il ritiro è ora possibile in qualsiasi momento con il solito 60 avviso di giorni.

<!-- section: s-23 -->
### Quando usare l'immagine **GPT‑6 Luna**

```text
✅ Micro-dev : modification locale dont tu contrôles la direction
✅ Tests simples, fixtures, boilerplate, renommages et transformations mécaniques
✅ Recherche d'occurrences, résumés, logs et PR summaries
✅ Worker/subagent dont la sortie est vérifiée immédiatement
```

OpenAI] raccomanda di iniziare Luna a **High**. Non cercare di trasformare Luna in un agente di confine con Extra High: se il compito diventa ambiguo o concettuale, andare a Sol 6.2 piuttosto che pagare per lunghi periodi su un modello troppo piccolo.

<!-- section: s-24 -->
### Quando usare l'immagine **GPT‑6.2 Sol**

```text
✅ Issue standard complète : découverte → implémentation → tests → PR
✅ Feature multi-fichiers et bug non trivial
✅ Review indépendante d'une PR écrite par Claude
✅ Migration bornée, compatibilité et refactor transversal
✅ Second avis sérieux sur une architecture proposée par Opus
```

```text
Light       → issue très bien spécifiée, patch local, reproduction claire
Medium      → défaut agentique quotidien
High        → feature complexe, root cause difficile, migration, beaucoup de cas limites
Extra High  → capacité suffisante mais besoin réel de davantage d'analyse/vérification
Ultra       → uniquement si le travail se décompose en investigations indépendantes
```

<!-- section: s-25 -->
### Quando usare l'immagine **GPT‑6.2 Astra**

```text
✅ Sol High échoue parce que la capacité/jugement manque, pas parce que le contexte est pollué
✅ Sécurité, auth, contrat critique ou décision où une mauvaise direction coûte plusieurs reprises
✅ Workflow end-to-end très ambigu avec nombreux outils / computer use
✅ Reviewer frontier ponctuel sur une décision à fort impact
```

Comincia con l'aiuto ** Astra Lights**. Per un compito che è veramente front-end, Astra Light può costare meno in totale di un Sol Extra High seguito da un recupero, perché evita una cattiva traiettoria. Salire a Medium/High solo se necessario; Extra High/Ultra rimane eccezionale.

<!-- section: s-26 -->
### Quando usare l'immagine **modalità di utilizzo `ultra` In un'altra ChatGPT Lavorare / lavorare Codex**

```text
✅ Cartographie codebase-scale d'une application legacy
✅ Migration multi-modules en worktree dédié
✅ Audit architecture + tests + sécurité + performance en parallèle
✅ Décomposition d'un refactor en micro-PRs
✅ Mission où plusieurs sous-analyses indépendantes apportent une vraie valeur
```

```text
❌ One-shot “réécris proprement”
❌ Tâche interactive courte
❌ Repo mal testé sans limite de diff
❌ Modification directe de fichiers critiques sans plan validé
```

In questa sottosezione, occorrente `ultra` si riferisce al segreto ** modalità orchestrazione multi-agent del prodotto**, e non al livello di sforzo iniziale `ultra` che alcuni SDKs scusare Codex È adatto per le tapparelle indipendenti; evitalo quando gli agenti scrivono nello stesso stato mutabile o quando un'unica operazione lenta domina il compito. Su un'applicazione legacy, inizia a mappare, producendo un registro del debito, proponendo test di caratterizzazione, e poi tagliando in micro-PR. Non iniziare scrivendo il codice.

Minimo modello di missione `ultra`:

```text
Tu interviens comme équipe de reviewers/agents sur une application legacy Scala.

Rôles à simuler :
- architecte legacy ;
- tech lead Scala ;
- reviewer sécurité défensive ;
- QA / test engineer ;
- maintainer sceptique.

Objectif :
[objectif précis]

Contraintes :
- aucun changement de comportement observable sans validation ;
- pas de modification build.sbt / migrations DB / contrats JSON publics sans stop ;
- micro-PRs de moins de 300 lignes modifiées ;
- tests de caractérisation avant refactoring ;
- chaque conclusion doit citer les fichiers observés ;
- distinguer faits, hypothèses et recommandations.

Sortie attendue :
1. carte du périmètre ;
2. risques ;
3. registre de dette ;
4. tests de caractérisation prioritaires ;
5. plan en micro-PRs ;
6. première PR proposée, sans l'appliquer tant que le plan n'est pas validé.
```

<!-- section: s-27 -->
## Selezione veloce modello matrix impegnati

```text
Micro-dev, humain garde le contrôle      → GPT‑6 Luna High / Sonnet 5.5 Medium
Worker lecture / triage à faible risque  → Haiku 5.5 / Qwen local / GPT‑6 Luna
Patch local au jugement intermédiaire    → GPT‑6.1 Terra Medium
Issue standard end-to-end                → GPT‑6.2 Sol Medium
Agent Claude end-to-end                  → Opus 5.5 Medium
Feature / bug difficile                  → GPT‑6.2 Sol High ou Opus 5.5 High selon nature
Architecture / root cause dominante      → Opus 5.5 High
Review croisée                           → famille opposée à l'auteur, Medium par défaut
Suivi post-PR Codex                       → GPT‑6.2 Sol Medium (Goal / Heartbeat / Cloud)
Sol High insuffisant                     → GPT‑6.2 Astra Light
Opus High insuffisant                    → Fable 5.2 Low
Long-horizon séquentiel > 30 min         → Opus 5.5 Extra (`xhigh`)
Codebase-scale parallélisable            → GPT‑6.2 Sol Ultra, surtout read-heavy
Frontier absolu                          → Astra Medium+ / Fable Medium+ après preuve du besoin
```

Regola pratica:

```text
Le senior garde la direction → modèle rapide et économique.
L'agent possède la trajectoire → Sol 6.2 ou Opus 5.5.
La compréhension domine le patch → privilégier Opus.
L'exécution end-to-end domine → privilégier Sol 6.2.
Une limite de capacité apparaît → Astra Light ou Fable Low avant l'effort extrême du tier inférieur.
Ultra uniquement si le problème contient plusieurs axes réellement indépendants.
```

<!-- section: s-28 -->
## Routing automatico delle attività di sviluppo

La matrice di selezione non deve essere lasciata solo manuale. Per evitare di bruciare i crediti su semplici compiti o, al contrario, inviare un compito critico a un modello troppo debole, aggiunge un passo di routing esplicito prima di ogni compito agente.

Il principio non è quello di scegliere il modello più intelligente, ma il modello più piccolo in grado di produrre un risultato univoco con un rischio accettabile.

```text
Demande / ticket / stack trace
→ classification de tâche
→ estimation difficulté + risque
→ sélection du modèle minimal acceptable
→ exécution avec permissions limitées
→ tests déterministes
→ escalade si échec
→ log coût / qualité
```

<!-- section: s-29 -->
### Architettura consigliata

```text
CLI / IDE / ticket
→ task-classifier
→ context-builder
→ model-router
→ agent-runner
→ test-runner
→ reviewer
→ cost-quality log
```

| Componenti          | Role of the                                                         | Modello consigliato/tool impegnati                                                                             |
|--------------------|--------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| `task-classifier`  | Ordinare il compito, il rischio e le difficoltà necessarie                 | **Jev** se l'uscita è chiusa; Qwen locale / Haiku se il ragionamento aperto è richiesto         |
| `context-builder`  | Trova file utili, relazioni, test, documenti e comandi necessari | Sourcebot, ScalaSemantic MCP, Codebase-Memory MCP] se poliglot, rg, IntelliJ, Metals MCP], Context7]   |
| `model-router`     | Scegli il più piccolo modello accettabile                      | Regole deterministiche + Jev come segnale probabilistico; OpenRouter solo per punto arrampicata  |
| `agent-runner`     | Correre con le giuste autorizzazioni necessarie                         | Codex, Claude Code subagents, retrogrado Aider, OpenCode, Qwen Code                                              |
| `test-runner`      | Convalida in modo deterministico                              | sbt, IntelliJ, Metals MCP, CI                                                                         |
| `reviewer`         | Reread senza scrittura                                           | Famiglia contraria allo scrittore: Opus 5.5 Medio o medio GPT‑6.2 Sol Media; Astra/Fable solo se criticità |
| `cost-quality log` | Misurazione dei costi, qualità, feedback e feedback            | Local Scripts, follow-up tabella fattori                                                                      |

<!-- section: s-30 -->
### Jev: livello di decisione, non modello di codifica

**Jev 1.14 (`jev-1.14.0`)** è l'attuale modello di System One di successione TypeSafe AI. Non genera testo o codice: riceve un falso `state` e domande digitate, quindi riferire direttamente le decisioni probabilistiche. Il modello mentale giusto è un aumento **Semantic smart se si vuole** : ingresso aperto, rami definiti dallo sviluppatore.

| Primitivo di appartenenza | Utilizzare                                                           |
|-----------|-----------------------------------------------------------------|
| `Choice`  | scegliere tra opzioni chiuse: modello, agente, abilità, percorso |
| `Score`   | tasso su scala ordinata: rischio, pertinenza, priorità   |
| `Noul`    | stimare la probabilità di una proposta di essere vera alternativa            |

Jev 1.14 Costo: **$0.042/M tokens input precedenti** e non carica l'output. Il regime standard accetta perdite **64K tokens per richiesta urgente** e non è così **32K per l'acquisto `state` + la domanda più lunga** I limiti di flusso dipendono dall'organizzazione e sono letti nella console. Esiste un contesto sperimentale più lungo e gli input dell'immagine in condizioni, senza diventare il default del router. `jev-latest` punto in direzione `jev-1.14.0` : **pin la versione alternativa** non appena si calibrano le soglie, perché il cambiamento nella distribuzione può invalidare le soglie di rischio.

> **OpenAI Decisioni API.** Finepoint: `POST /v1/decisions`, ora generalmente disponibile `gpt-6-luna`, avec precedenti
> tipo di risposte `predicate`, `choice` e non è così `score`. Fino a esaurimento **400 domande di risposta** può condividere la stessa voce; testo, casuale
> Le immagini e i dati strutturati sono supportati in base al campo. Prezzo standard: **$0.10/M input tokens**, **$0.01/M conseguente
> cache entry tokens leggere**, nessuna fatturazione di output; voci di cache, voci lunghe e elaborazione
> La Commissione continuerà a monitorare l'attuazione della regionale `task-classifier` e non è così `model-router`, confronta le decisioni e gli obiettivi Jev su lo stesso argomento
> domande con calibrazione per compito e rischio, mai sul prezzo del token da solo.

In questo flusso di lavoro, i migliori candidati sono:

```text
✅ task / risk / difficulty classification
✅ model routing : Luna / Sol / Astra / Sonnet / Opus / Fable
✅ sélection progressive de quelques skills parmi un gros catalogue
✅ triage des résultats de subagents et pertinence d’un contexte
✅ signal topic-shift / « faut-il envisager une compaction ? »
✅ filtrage de notifications et décisions qui méritent l’attention humaine

❌ écrire ou expliquer du Scala
❌ architecture ou root-cause ouverts
❌ calcul, comptage ou comparaison de dates
❌ décider seul d’un push, déploiement, suppression, secret ou migration DB
```

Architettura consigliata:

```text
règles déterministes
→ Jev pour un jugement fermé et fréquent
→ code combine probabilités + seuils
→ LLM génératif si raisonnement ouvert ou confiance insuffisante
→ humain si action critique ou irréversible
```

**Tipo di sicurezza** L'argomento "zero allucinazioni" significa soprattutto che occorre Jev non esce da una struttura dichiarata o da un insieme di opzioni; può sempre selezionare l'opzione sbagliata. **346 009 richieste / richieste 37 dataset dati** trovare le probabilità `Choice` Questo è il caso per l'Unione europea, che è il più grande partner commerciale dell'Unione europea. `0.5` è male per alcuni compiti binari: le soglie devono essere soggette **calibrato da task e rischio derivato**.

Tre regole di integrazione:

1. **Il codice mantiene l'autorità.** Segnali determinanti (trasferimenti)`touches_security`, file critico, azione distruttiva) sempre prendere la precedenza sopra Jev.
2. **Stato minimo.** Jev sottopone anche il vuoto *contestazione del contesto*; filtro prima della chiamata e invia solo ciò che realmente cambia la decisione.
3. **Test di stabilità.** Suggerimenti `Choice`, periodicamente riordina le opzioni; valutazioni di autorizzazione `jev-1.13` indicare una possibile sensibilità all'ordine, da rivalidare su assegni `jev-1.14.0`. Il mondo del lavoro `state` adversarial può anche influenzare la risposta: Jev è un segnale, non una sandbox.

<!-- section: s-31 -->
### Classificazione minima

Il router deve produrre una decisione strutturata, non una risposta gratuita. Esempio di uscita prevista:

```json
{
  "task_type": "implementation | debug | test | review | migration | architecture | boilerplate | research",
  "risk": "low | medium | high | critical",
  "difficulty": "trivial | simple | normal | hard | frontier",
  "expected_files": "1 | 2-5 | 6-10 | 10+",
  "requires_code_write": true,
  "requires_external_docs": false,
  "touches_public_api": false,
  "touches_json_contract": false,
  "touches_database": false,
  "touches_build": false,
  "touches_security": false,
  "touches_concurrency": false,
  "model": "qwen | haiku55 | sonnet55 | opus55 | fable52 | gpt6_luna | gpt61_terra | gpt62_sol | gpt62_astra | gpt61_sol | gpt6_astra",
  "reasoning_effort": "light | low | medium | high | extra | xhigh | max | ultra | null",
  "reasoning_mode": "standard | pro | null",
  "multi_agent": false,
  "max_parallel_agents": 3,
  "max_cost_usd": 0.0,
  "max_duration_minutes": 0,
  "confidence": 0.0,
  "escalation_rule": "string",
  "stop_conditions": [
    "string"
  ]
}
```

**Gerarchia dei segnali** : criteri deterministici (attuali)`touches_*`, `expected_files`, prevista dimensione del diff) sono i trigger correlati *Primary:* e arrampicata. Se la classificazione viene da **Haiku/AiutoQwen**, `confidence` è un autovalutazione secondario e poco calibrato. frequenza **Jev**, utilizza la distribuzione e la conseguente `confidence` girato, ma con un vuoto **soglia calibrata da domanda e livello di rischio determinato**, mai un segreto `0.75` In entrambi i casi, l'alta fiducia non deve mai essere raggiunta. *de-escalating* Un segnale deterministico critico.

`reasoning_effort` deve essere standardizzato dalla superficie: Claude usa indubbia `low | medium | high | xhigh | max` su modelli compatibili, con conseguente **Opus 5.5 e non è così Haiku 5.5 `medium`** default; Codex visualizzazione **La luce del sole | Medioriente | E' un'ottima idea. | Esclusivamente | La mia vita è un'altra**, mentre API impegnati OpenAI expounds valori indicati `low | medium | high | xhigh | max` Secondo il modello. `multi_agent` Lo sforzo è una leva di qualità e di costo, ma un livello superiore con basso sforzo può essere più conveniente in totale di un livello inferiore spinto all'estremo.

<!-- section: s-32 -->
### Matrice automatica di routing

| Segnale rilevato                                               | Modelli iniziali                | Arrampicata                                                                      |
|--------------------------------------------------------------|-------------------------------|-------------------------------------------------------------------------------|
| Riepilogo, smistamento, grep, semplici log relativi                           | Haiku 5.5 / Qwen              | Sonnet 5.5 Medio se ambiguo ritardo                                                   |
| Boilerplate, DTO, fissaggi, edizione meccanica                | GPT‑6 Luna E' un'ottima idea.               | Sonnet 5.5 Mezzo se sottili tipi/domini dovuti                                    |
| Semplice o non regresso test localizzato                      | GPT‑6 Luna E' un'ottima idea.               | Sonnet 5.5 Medio se importante regola aziendale                                  |
| Patch mirato, l'uomo mantiene la direzione necessaria                       | Luna Alta / Informazioni Sonnet 5.5 Medioriente | Soil: Sol 6.2 Luce/Medium se l'esplorazione richiedesse                                |
| Patch legato con giudizio intermedio                      | GPT‑6.1 Terra Medioriente           | GPT‑6.2 Sol Mezzo se l'esplorazione necessaria |
| Funzione di affari legata, 1 a 5 file aggiuntivi                        | GPT‑6.2 Sol Medioriente            | Sol Alto se difficoltÃ; Opus Medium in recensione                                |
| Caratteristica 5 a 10 file con invarianti                      | GPT‑6.2 Sol Medio/Alta frequenza       | Opus 5.5 Elevato se l'architettura/radice causa domina                               |
| Inserire il tuo messaggio Scala sottile, implicito, dato, effetti dovuti                  | Opus 5.5 E' un'ottima idea.                 | Sol High per ipotesi indipendente; Fable Low se insufficiente capacità produttiva     |
| Multi-module bounded migrazione                               | GPT‑6.2 Sol E' un'ottima idea.              | Opus High in review; Astra Light se Sol cap accidental                             |
| Refactor codebase-scale                                      | Opus 5.5 E' un'ottima idea.                 | Extra così lungo orizzonte; Fable Low se Opus captazione                            |
| Recensione di un PR Codex abitua                                        | Opus 5.5 Medioriente               | Elevato rischio critico                                                       |
| Recensione di un PR Claude impegnati                                       | GPT‑6.2 Sol Medioriente            | Alta poi Astra Light se rischio confine                                      |
| Monitoraggio indipendente di una PR alternativa Codex                               | GPT‑6.2 Sol Medioriente            | Alta se difficile diagnosi; Sol frequenza 6.1 Medio se si vuole 6.2 non disponibile             |
| Sicurezza / Auth / Critical Contrattuativo                           | GPT‑6.2 Astra Luce + umano    | Astra Medium/High + recensione Opus High interfere                                          |
| Indipendenti axes acustici                                 | GPT‑6.2 Sol La mia vita è un'altra             | Astra Ultra solo se è effettivamente necessaria una capacità aggiuntiva |
| Cambiamento `build.sbt`, dipendenze, DB, contratto pubblico JSON | Non auto-scrittura automatica           | Piano + validazione umana                                                     |

<!-- section: s-33 -->
### Politica di arrampicata

Il routing automatico deve funzionare come una cascata controllata:

```text
Micro-boucle vérifiable : Qwen / Haiku / GPT‑6 Luna High / Sonnet 5.5 Medium
→ ownership agentique : GPT‑6.2 Sol Medium / Opus 5.5 Medium
→ difficulté : Sol High / Opus High
→ limite de capacité : Astra Light / Fable Low
→ effort supérieur seulement si la capacité est suffisante mais le raisonnement manque
→ Ultra seulement si parallélisable
→ humain
```

**Non solo cambiare un modello nel mezzo di una conversazione derailed.** Se il fallimento proviene da una traiettoria inquinata — ripetuta ipotesi falsa, accumulando allucinazioni, correzioni che ricreano altri errori — il contesto è di per sé parte del problema. Sonnet 5.5 → Opus 5.5, Soil perdono 6.2 → Astra o altro Opus 5.5 → Fable 5.2 :

```text
1. Stop write mode.
2. Produire HANDOFF.md : objectif, état du diff, faits vérifiés, essais échoués, erreur actuelle, inconnues.
3. Ouvrir une session fraîche avec seulement spec + AGENTS.md + HANDOFF.md + fichiers/diff pertinents.
4. Escalader le modèle dans cette nouvelle session si la difficulté le justifie toujours.
```

L'escalation di rivendicazione **capacità di** è utile su un problema correttamente posto; non deve portare il debito conversazionale di una sessione già biased.

Arrampicate automaticamente se:

```text
- un signal déterministe critique est présent (touches_* sensible, diff hors gabarit) ;
- auto-confidence LLM < 0.75, ou confidence Jev sous le seuil calibré pour cette décision ;
- erreur de compilation identique 2 fois ;
- test ciblé toujours rouge après 2 corrections ;
- diff hors scope ;
- plus de fichiers modifiés que prévu ;
- plus de 300 lignes de diff inattendues ;
- build.sbt, plugins.sbt, migration DB ou contrat JSON public est touché ;
- API publique modifiée ;
- le routeur détecte sécurité, concurrence, performance ou argent ;
- le modèle déclare explicitement une incertitude forte ;
- le coût estimé d'une erreur dépasse le coût du modèle supérieur.
```

Interrompi (senza arrampicata automatica) se:

```text
- max_cost_usd est atteint (budget local) ;
- max_duration_minutes est atteint (timeout wall-clock) :
  une session agentique qui boucle est un mode de défaillance distinct d'une session qui échoue,
  et l'escalade vers un modèle plus cher ne corrige pas une boucle.
```

De-escalation automaticamente se:

```text
- tâche purement textuelle ;
- aucun write mode nécessaire ;
- pas de risque métier ;
- moins de 20 lignes attendues ;
- fichier unique ;
- objectif déterministe ;
- test existant très ciblé ;
- contexte stable et déjà connu du projet.
```

<!-- section: s-34 -->
### Regole non automatiche

Non lasciare mai che un router decida da solo di scrivere su:

```text
- build.sbt ;
- plugins.sbt ;
- resolvers ;
- versions de dépendances ;
- migrations DB ;
- contrats JSON publics ;
- sécurité ;
- authentification ;
- autorisation ;
- concurrence ;
- gestion d'argent ;
- suppression de données ;
- scripts de déploiement ou d'infrastructure.
```

In questi casi, il router può solo proporre:

```text
- modèle recommandé ;
- plan ;
- fichiers probables ;
- tests à exécuter ;
- risques ;
- règle d'arrêt.
```

<!-- section: s-35 -->
### Raccomandati subagenti Claude Code

**Calibrazione della macchina Codex 6.2.** Per un genitore GPT‑6.2 Sol o Astra, vai con lo stesso modello e lo sforzo per i subagenti ( raccomandazione ufficiale) OpenAI) Quindi ridurre il trier dei compiti veramente meccanici, con uscita controllabile: Luna/Haiku per grep, estrazione, logs e astratti; Sol/Opus per invarianti, architettura e causa radice. Lo stesso principio di misura si applica a Claude. Un recensore dell'altra famiglia rimane una sessione indipendente, non un lavoratore meno costoso dell'autore.

Claude Code è il posto migliore per applicare questo routing su base giornaliera, poiché i subagenti possono avere il proprio contesto, strumenti e autorizzazioni.

```text
researcher
- Modèle : Haiku / Qwen si externe
- Mode : read-only
- Rôle : trouver fichiers, usages, tests, documentation

scala-implementer
- Modèle : Sonnet 5.5 `medium`
- Mode : write limité au repo
- Rôle : implémenter les tâches bornées sous contrôle d’un plan clair

hard-debugger
- Modèle : Opus 5.5 `high`
- Mode : write limité, plan obligatoire
- Rôle : bugs Scala subtils, implicits, effets, causes éloignées

migration-planner
- Modèle : Opus 5.5 `high` ; Fable 5.2 `low` (décision ponctuelle) ou `high` (mission longue) si Opus plafonne
- Mode : plan-first, worktree dédié
- Rôle : migrations multi-modules, refactors longs, stratégie de découpage
- Note : évaluer Dynamic Workflows (Opus 5.5 + subagents parallèles massifs)
  comme alternative à un Fable mono-agent sur les migrations codebase-scale

reviewer
- Modèle : Codex / GPT‑6.2 Sol `medium` ; Astra `light` si critique
- Mode : no-write
- Rôle : review indépendante, classement bloquant / important / optionnel

pr-summarizer
- Modèle : Qwen / GPT‑6 Luna
- Mode : no-write
- Rôle : résumé PR, release notes, checklist finale
```

<!-- section: s-36 -->
#### Isolamento del contesto: ruolo principale dei subagenti su lunghe operazioni

Il guadagno dei subagenti non è solo il parallelismo, ma ogni subagente lavora in una direzione ** contesto fresco e isolato finestra alternativa**; quindi il genitore non ha bisogno di accumulare le ricerche, i registri, i file e le estremità morte di ogni subaspect. *rotazione contesto*.

La condivisione consigliata è:

```text
PARENT
- objectif
- contraintes et non-objectifs
- plan validé
- décisions prises
- diff courant
- preuves essentielles
- risques ouverts

SUBAGENTS
- exploration de nombreux fichiers
- recherche Sourcebot / rg
- call paths, hiérarchies, usages et chaînes de givens via ScalaSemantic
- graphe structurel cross-language via Codebase-Memory si Java/Kotlin/Scala cohabitent
- investigation live des types / givens / diagnostics via Metals
- documentation externe
- logs et suites de tests volumineuses
- cartographie d'un module legacy
```

Regola della decisione:

```text
Les détails de cette sous-tâche seront-ils encore utiles au parent après sa fin ?

NON → subagent isolé
OUI → garder dans le contexte parent
```

Il messaggio della delegazione deve essere un ** contratto**, poiché il subagente non deve dipendere dall'intera storia di conversazione del genitore:

```text
Mission :
[périmètre précis]

Mode :
read-only / write borné

Cherche :
[questions précises]

Ne fais pas :
[hors scope]

Retourne uniquement :
1. conclusion ;
2. preuves file:line ;
3. tests ou commandes pertinents ;
4. incertitudes restantes.

Réponse cible : < 1–2K tokens.
```

Il ritorno è un'interfaccia, non una trascrizione. 80]K tokens e inviarli indietro 1,5K, l'isolamento è utile; se è a letto 10K e inviarlo indietro 8K, ha spostato principalmente il rumore.

```text
isolation_ratio
= tokens consommés par le subagent
/ tokens retournés au parent
```

Quindi il giusto schema è esattamente quello di decidere **mappa → ridurre la riduzione** Diversi lavoratori specializzati spendono il contesto locale, poi il genitore sintetizza alcuni risultati brevi.Evita l'anti-pattern inverso — sette agenti che ogni lettura del repo e restituiscono i rapporti di dieci pagine — che ricrea l'ipotesi *contestazione del contesto* nel contesto radice.

Per ** il flusso di lavoro da solista Scala**, tratta anche il fan-out come un bilancio di gettoni/quota:

```text
défaut                              → 1 agent actif
2 investigations indépendantes     → 2 subagents read-only
2 User Stories indépendantes        → 2 writers maximum pour commencer (WIP inclut les PR en review)
3+ sessions parallèles              → uniquement si le gain et la capacité de review sont mesurés
writer                              → toujours 1 par branche / PR / worktree
```

Logge al minimo sforzo `parallel_sessions_peak`, `subagent_count` e non è così `subagent_tokens`. Un subagent protegge il contesto del genitore, ma ricarica il proprio contesto: non è quindi mai "libero". Se non porta un isolamento utile o un lavoro realmente parallelo, non lo lancia.

Per il coordinamento, preferisce un fattore preciso ** Startopology:**Evita squadre in cui gli agenti parlano liberamente, condividono una cassetta postale o si distribuiscono uno stato mutabile. In questa guida, il "coordinatore" deve rimanere un semplice meccanismo **Destinazione**, non un sistema sociale di agenti.

> **Orchestrazione Claude Code**: **Agente Views** viene utilizzato per supervisionare diverse sessioni e attività;
> **Agent Teams** permette la collaborazione tra i corpi ma rimane sperimentale; **Ultrareview** è una recensione cloud casual
> **Remote Control** permette di supervisionare una sessione locale da un altro dispositivo
> Pur mantenendo l'esecuzione e MCP sulla macchina locale, queste superfici completano i sottoagenti; non riescono a calcolare
> cambiamento
> non la regola "uno scrittore per worktree".

> **Modo per l'uso `You should know` (2.1.287+)**: `cc-plugin-you-should-know` lancia un agente laterale durante le lunghe operazioni
> e visualizza sopra il prompt degli elementi che si o Claude potrebbe perdere. È ** disattivato per impostazione predefinita** e
> attive via `/plugin enable cc-plugin-you-should-know@builtin`. Trattala come segnale di vigilanza opportunistica,
> mai come un recensore indipendente, un oracolo o un cancello: le sue osservazioni devono ancora essere collegate a prove,
> un test verificabile o diff.

> **Claude Code 2.1.27x: isolamento più fine.** Da quando? 2.1.277, un subagent personalizzato o fornito da un plugin può arrivare
> dichiarare `omitClaudeMd` di non caricare `CLAUDE.md` utente, progetto e locale; amministrato politiche
> si riserva questa modalità a lavoratori di esplorazione altamente specializzati il cui contratto di delega contiene
> La stessa versione permette di allegare eventuali perdite `allowed_domains` a un comando
> Bash/PowerShell/Monitor: L'apertura di rete è valida per questo comando, non per l'intera sessione. ** Conferma:**
> su di noi
> "Contesto minimo per subagent" e "Minimum permesso per subagent" regole, senza giustificare l'eliminazione della ricezione
> contesto di progetto per un implementatore che ne ha bisogno.
>
> Poiché 2.1.278, la modalità Auto utilizza per impostazione predefinita un **Classificare lato server** sulle superfici compatibili e contrassegnare
> Anthropic
> indica che questo classificatore non aggiunge un costo di classificazione; `/status` indica se `Auto mode server` è attivo.
> Questo riduce un overhead di routing, non i requisiti di autorizzazione o revisione. Infine, plugin e competenze aggiuntive
> diventa artefatti testabili: `claude plugin eval` (2.1.269) esegue una serie di valutazioni scorted
> e riproducibile con output JSON/HTML, mentre `/skill-doctor` aiuta a individuare abilità caricate ma inutili.
> Un cambiamento persistente di plugin o abilità deve quindi passare attraverso eval + recensione prima della promozione.
>
> Le seguenti versioni aggiungono due strumenti complementari per evitare la deriva dell'imbracatura. **2.1.283**,
> `/doctor prompt-audit` (alias `/checkup prompt-audit`)] `CLAUDE.md`]], competenze, agenti e controlli per localizzare
> su di noi
> le istruzioni diventano obsolete o contraddittorie dopo un cambiamento nella generazione del modello.
> non interattivo, conseguente **`--bare`** è ora documentato come il modo per lanciare un'imbracatura minima: non
> auto-scoprimento di ganci/plugins/collegamentoMCP/memoria/istruzioni, e dal momento che 2.1.286 solo i server MCP esplicitamente
> nome sono collegati, senza promemoria di sistema o compiti di sfondo. Utilizzare `--bare` per **evals e script aggiuntivi
> Reproducibili alla ricerca**, non come la modalità giornaliera predefinita.

<!-- section: s-37 -->
### OpenRouter per il routing occasionale API

In questo caso **questo preciso lavoro soloflow impegnativo**, il routing principale non ha bisogno di un gateway APII cinque percorsi giornalieri hanno già la propria superficie e budget:

```text
Claude Code        → abonnement Claude Max
Codex              → abonnement ChatGPT
Qwen local         → MLX / llama.cpp / endpoint local
GitHub Copilot     → abonnement GitHub Copilot
JetBrains AI       → abonnement JetBrains AI
```

La necessità di API rimanente è **eccezionale.** Quando: Claude Code allora? Codex rimanere bloccato e desiderare un'opinione da un'altra famiglia di modelli, per esempio **GLM, Kimi, Gemini, Grok o un nuovo modello da valutare**In questo caso, bisogna evitare **OpenRouter è il miglior difetto** : una chiave, nessun server da mantenere, accesso rapido a molti modelli e fornitori, fatturazione centralizzata e disponibilità fallback.

```text
Blocage persistant
→ extraire le contexte minimal utile
→ OpenRouter
   ├── GLM
   ├── Kimi
   ├── Gemini
   ├── Grok
   └── nouveau modèle à tester
→ comparer l'analyse avec Claude / Codex
→ humain arbitre
```

**Non instradare automaticamente il lavoro quotidiano per arrivare OpenRouter.** La scelta del modello di emergenza deve rimanere esplicita: l'obiettivo è proprio quello di ottenere un'altra prospettiva, di non lasciare un router in silenzio scegliendo una famiglia diversa.

<!-- section: s-38 -->
#### Fallbacks: fornire sì, default nessun modello casuale

OpenRouter può passare automaticamente tra i fornitori. Per questa guida, si distingue due livelli:

```text
Même modèle, provider A indisponible
→ même modèle, provider B
→ OUI : résilience sans changer la nature du reviewer

GLM indisponible
→ Gemini
→ Kimi
→ Grok
→ NON par défaut : le changement de modèle doit rester visible et intentionnel
```

Per un'indagine tecnica, quindi, sempre log indicati ** il modello in realtà usato.** Un ricaduta inter-model può mascherare il motivo per cui una conclusione differisce da Claude o casuale Codex.

<!-- section: s-39 -->
#### Qwen locale: soggiorno diretto

Non aggiungere OpenRouter solo per standardizzare Qwen. `llama.cpp`, MLX o l'imbracatura locale possono già esporre un endpoint OpenAI-compatibile. Finché ci sono solo uno o due modelli locali, lo strato aggiuntivo non aggiunge abbastanza valore:

```text
Qwen local
→ llama-server / MLX
→ Qwen Code / OpenCode / script local
```

<!-- section: s-40 -->
#### Confidenzialità con un aggregatore

I fornitori accessibili tramite OpenRouter possono avere diverse politiche di conservazione.

```text
- ne jamais envoyer le repository entier par défaut ;
- préférer un reproducer minimal, quelques types/méthodes, la stack trace et le test ciblé ;
- anonymiser le contexte métier si possible ;
- choisir explicitement les providers compatibles avec les exigences de rétention du projet ;
- garder le code le plus sensible en local ou chez les fournisseurs directs déjà approuvés.
```

<!-- section: s-41 -->
### Loggers impegnati

Il router deve essere regolato a dati effettivi, non intuizione. Per ogni attività agente, log:

```text
task_type
risk
difficulty
decision_layer
decision_confidence
decision_threshold
decision_overridden
model_used
effort_level
fallbacks
parallel_sessions_peak
subagent_count
subagent_tokens
input_tokens
output_tokens
cost_usd
duration
files_changed
diff_lines
tests_run
tests_passed
review_findings
human_rework
merged_or_reverted
time_to_deploy
human_active_minutes
review_queue_minutes
review_true_positives
review_false_positives
review_missed_defects
quota_consumed_by_role
production_regressions
rollback_or_hotfix
```

Dopo due settimane, regolare le soglie:

```text
- si Qwen échoue souvent sur un type de tâche, route directement vers Sonnet ;
- si Sonnet réussit sans retours review sur un type de tâche, évite Opus ;
- si Opus réduit fortement les boucles de correction, garde-le pour cette classe ;
- si Opus `xhigh/max` suffit là où tu envoyais Fable, redescends ;
- si Fable ne produit pas moins de reprises humaines, réserve-le aux vraies sessions longues ;
- si `max` ne trouve que des remarques optionnelles, redescends vers `high` ou `medium`.
```

<!-- section: s-42 -->
### Prompt minimo router (generative fallback) attuali

Se Jev è disponibile e come le uscite sono chiuse, preferisce `Choice` / `Score` / `Noul` Il prompt qui sotto è utile quando è necessario un ragionamento aperto o come base per il confronto.

```text
Tu es un routeur de tâches de développement logiciel pour un projet Scala/Java/Play/Spark.

Analyse la demande ci-dessous et retourne uniquement du JSON valide.

Objectif : choisir le plus petit modèle capable de produire un résultat mergeable avec un risque acceptable.

Prends en compte :
- type de tâche ;
- difficulté ;
- risque métier ;
- taille probable du diff ;
- nombre probable de fichiers ;
- besoin d'écriture ;
- besoin de docs externes ;
- risque Scala spécifique : implicits, givens, effets, sérialisation JSON ;
- fichiers critiques : build.sbt, migrations DB, auth, sécurité, concurrence, argent ;
- modèle, effort et, si nécessaire, mode `pro` ou multi-agent (`ultra` côté produit) ;
- plafond de coût et de durée ;
- règle d'escalade ;
- conditions d'arrêt.

Les signaux déterministes (fichiers critiques, taille de diff) priment sur ta propre confidence.

Demande :
[COLLER LA DEMANDE]

Contexte disponible :
[COLLER FICHIERS, STACK TRACE, DIFF STAT OU RÉSUMÉ]
```

<!-- section: s-43 -->
### Principio di guida di routing dovuti

```text
Le routeur ne choisit pas le modèle le plus intelligent.
Il choisit le modèle le moins cher capable de produire un diff mergeable,
avec une règle d'escalade explicite dès que le risque ou l'incertitude augmente.
```

<!-- section: s-44 -->
## Impatto sul bilancio mensile :

*(indicativo relativo ordine dalle tariffe) API standard; abbonamento e quota non convertono meccanicamente in dollari API)*

| Modello:              |           Prezzo: API input/output / M direzione | Consigli per il volume                                                                          |
|---------------------|------------------------------------:|---------------------------------------------------------------------------------------------------|
| Qwen locale corrente          |                                   0 | Pre-analisi e sicure operazioni di volume                                                             |
| **Jev 1.14**        | **$0.042/M input; output gratuito**]] | Livello di decisione: classificazione, routing, punteggio e selezione delle competenze ad alta frequenza        |
| **GPT‑6 Luna**      |                   **$0.10 / $0.50** | Micro-dev urgente Codex, lavoratori, smistamento, semplici prove                                                   |
| **Haiku 5.5**       |                   **$0.10 / $0.50** | Sotto-agenti, triage; cuscinetto × percentuale5 se l'input è > 100K; sforzo per arrivare `medium` configurabile                        |
| **GPT‑6.2 Sol**     |                        **$2 / $10** | Fault: Codex agentic; ottimo punto di performance prima di Astra preventiva                                 |
| **Sonnet 5.5**      |                        **$2 / $10** | Micro-dev Claude difetto; `medium` per agentec codifica ben specificato                              |
| **Opus 5.5**        |                        **$4 / $20** | Deficit Claude agentique a `medium`; `high` per compiti difficili                             |
| **GPT‑6.2 Astra**   |                        **$8 / $40** | Salita di capacità; inizio a Luce impegnativa                                                          |
| **Fable 5.2**       |                        **$8 / $40** | Frontier Claude; iniziare a Low durante una capacità escalation                                 |
| Extra / Max / Ultra eccitazione |                            Variazione | Utilizzare solo dopo la misurazione: più sforzo non è sinonimo di un miglior costo per compito completato |

> **Il prezzo per token non è il TCO.** Valuta anche i risultati Fable 5.2`low` su attività limitate e verificabili: può costare meno per attività risolte
> che un modello più basso che cerca, rilegge e ripercorre di più; al contrario, Opus 5.5 `medium` può raggiungere l'obiettivo
> la stessa qualità di Fable su alcuni flussi di lavoro per una frazione del costo. Il benchmark locale deve quindi misurare
> ** costo per cambiamento accettato**, curriculum umani e minuti.

<!-- section: s-45 -->
## Anti-credito regola bruciata

Non lanciarlo Fable 5.2, GPT‑6.2 Astra, Opus 5.5 `Extra/Max` o costoso `Ultra` modalità a meno che non sia possibile fornire:

```text
- objectif précis ;
- contraintes ;
- fichiers ou modules probables ;
- critères d'acceptation ;
- tests à exécuter ;
- non-objectifs ;
- limite explicite de diff ;
- plafond de coût et de durée ;
- règle d'arrêt.
```

Un modello molto forte su una rapida sfocatura non produce un buon risultato: produce una deriva più costosa.

> **Limiti di legame piuttosto che disciplina da solo.** Varie impostazioni Claude Code trasformare questa regola in vuoto
> salvaguardie: `maxEffortLevel` si fa carico dello sforzo su tutti i fornitori; una regola di negazione che si rivolge a un parametro strumento
> (ad esempio `Agent(model:opus)`]] vieta di lanciare un subagent su un modello costoso; `CLAUDE_CODE_SUBAGENT_MODEL`
> fissare il modello di subagenti; `fallbackModel` elenco fino a tre modelli di piega testati in ordine (per arrivare
> log, vedi sopra); `/usage` rompe il consumo per abilità, subagent, plugin e server MCP; e
> agganci vedere l'attuale sforzo via `$CLAUDE_EFFORT`. Lato API, les **] budgets del tabellone** (beta)
> `task-budgets-2026-03-13`, `output_config.task_budget`) dare al modello un bilancio di gettoni per l'intero loop casuale
> Agente: è un bilancio suppletivo **indicativo**, non un soffitto, che deve essere raddoppiato da un vuoto `max_tokens` e un soffitto
> lato cliente; il suo valore è parte del prompt reso, quindi cambiandolo rompe la cache.
> modelli supportati prima di utilizzarlo su Fable 5.2 o Opus 5.5.

<!-- section: s-46 -->
#### Checklist pre-flight prima di qualsiasi attività > $ urgente$2 costi stimati

Prima di correre Fable 5.2, GPT‑6.2 Astra, Opus 5.5 con alto sforzo o una sessione multi-agent, convalida questa lista di controllo. Ogni casella non selezionata è un motivo per non eseguire e scendere come modello o un campo di applicazione.

□ Formulazione obiettivo 1 frase con azione verbenziale □ Obiettivi non spiegati (almeno 2) □ File/moduli rilevanti identificati (percorsi precisi) □ Criterio di accettazione testable definito □ Comando di prova mirato pronto per eseguire □ Set diff massimo accettabile (ad es. 300 linee) □ Limite di costo fisso (ad es. $ indicati$5) e durata massima (ad esempio: 30 min) □ Smettere di regola (se [condizione] □ Il piano è stato convalidato dall'umano PRIMA della modalità di scrittura □ Worktree dedicato creato se il compito tocca > arrivare 5 file □ Contesto minimo preparato (non "qui è l'intero repo")

Stime dei costi rapidi (ordine di grandezza):

| Complimenti               | Modello:      | Tokens stimato tassi      | Costi stimati |
|---------------------|-------------|---------------------|-------------|
| Caratteristiche 3 file  | Sonnet 5.5  | ~20K in / ~ retromarcia ~5K out   | ~$0.09      |
| Multi-module Bug frequenza   | Opus 5.5    | ~50K in / ~ retromarcia ~10K out  | ~$0.40      |
| Migrazione quadro di riferimento | Fable 5.2   | ~200K in / ~ retromarcia ~50K out | ~$3.60      |
| Audit Astra max segnali     | GPT‑6.2 Astra | ~100K in / ~ retromarcia ~20K out | ~$1.60      |

Se il costo stimato supera 3x il costo del modello inferiore per lo stesso compito, la differenza di qualità deve essere giustificata dal rischio. "Più intelligente" non è una giustificazione.
---

