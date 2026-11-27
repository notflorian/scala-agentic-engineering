<!-- section: chapter -->
# 1A. Vibe coding, programmazione assistita dall’IA e programmazione agentica

Il termine **vibe coding**, reso popolare da Andrej Karpathy nel febbraio 2025, descriveva in origine una pratica in cui il programmatore delega quasi tutta la scrittura del codice, accetta le proposte del modello e valuta il lavoro soprattutto in base al risultato osservabile. È un approccio efficace per un prototipo usa e getta, un’esplorazione o un’interfaccia a basso rischio. Come metodo di produzione è insufficiente per sistemi aziendali, finanziari, sensibili alla sicurezza o destinati a durare.

Due precisazioni sull’origine del termine chiariscono il dibattito del 2026. Karpathy ha spiegato che il tweet era per metà una battuta e riguardava progetti usa e getta del fine settimana. Non ha mai proposto il vibe coding come metodo di produzione. Già nel febbraio 2025, Simon Willison ha tracciato una distinzione di riferimento. Accettare i diff senza leggerli è vibe coding. Rivedere ogni riga e capire che cosa fa è programmazione assistita dall’IA. Il problema nasce quando si salta la revisione. Alla fine del 2025 si è aggiunto il termine **vibe engineering**, che descrive il lavoro di professionisti esperti capaci di accelerare molto con agenti LLM pur mantenendo la piena responsabilità per il software. Revisione, test e responsabilità distinguono queste due pratiche e sono al centro di questa guida.

Bisogna distinguere tre modi di lavoro:

| Modalità                        | Il controllo umano                                                     | Uso adeguato                                     | Il rischio principale                                           |
|-----------------------------|---------------------------------------------------------------------|--------------------------------------------------|------------------------------------------------------------|
| **Il Vibe Coding**             | Fattivo, validazione per sensazione e esecuzione                       | Prototype, spike, strumento personale gettabile        | Il debito invisibile, la sicurezza, la comprensione perduta            |
| **Ingegneria AI-assistita** | Lo sviluppatore progetta e rilieva, il modello accelera                 | Lavoro giornaliero su codice mantenuto              | Automatizzare le decisioni che dovrebbero rimanere umane    |
| **codifica agente**          | L'agente esplora, pianifica, modifica e prova in un perimetro limitato | Lavori ben specificati con test e permissioni | Derivo, cerchio, azione fuori perimetro, iniezione indiretta |

Per un anziano ScalaL'obiettivo non è quindi "più di vibe coding", ma una **Ingegneria Agente Controlata ** :

```text
specifica verificabile
→ contesto minimo ma sufficiente
→ piano
→ permessi proporzionati
→ esecuzione monitorata
→ compilazione e test deterministici
→ revisione indipendente
→ approvazione umana
```

**Prova-diretta Agentic Engineering** di: le SDD fissare il contratto, l'ingegneria harness rende le sue restrizioni eseguibili, e le prove determinano se il cambiamento può progredire. Per ciascun requisito, associare una prova indipendente (test di comportamento, ispezione, benchmark o misura runtime), il SHA effettivamente validato e i rischi non coperti. Una affermazione dell'agente, una revisione senza prove o un semplice status verde non costituiscono un oracolo. Il ciclo si conclude dopo la validazione dell'artefatto distribuito, non semplicemente alla fusione (sezione 15B).

<!-- section: s-1 -->
## Che cosa mostra lo stato dell'arte in 2026

1. **Solo il modello non determina il successo.** Harness, gli strumenti disponibili, il debugger, la qualità del contesto e i test possono modificare i risultati quasi così tanto quanto la scelta del modello. Le confronti tra i risultati pubblicati da fornitori sono validi solo se harness, sforzo, strumenti e protocollo sono comparabili.
2. **I benchmark brevi sovrascettano l’autonomia lunga.** Gli agenti ottenono buoni risultati su uscite isolate, ma cadono fortemente sulle evoluzioni multi-file, lunghe e storiche. SWE-EVO, per esempio, mira a compiti molto più lunghi di SWE-bench e evidenzia questa differenza.
3. **SWE-bench Verified non è più un buon standard unico.** OpenAI ha documentato problemi di contaminazione e test difetti. Per il codice, preferisce un portafoglio che comprende attività SWE-bench audit, Terminal-BenchI compiti di revisione e soprattutto un benchmark interno Scala Non pubblico .
4. **La produttività umana non è garantita da un buon punteggio agente.** Uno studio randomizzato di METR su sviluppatori esperti nei propri depositi ha osservato un rallentamento con gli strumenti di avvio 2025I dati poi raccolti suggeriscono un possibile miglioramento, ma METR giudica il nuovo test non affidabile a causa di scelte di selezione e misure difficili con diversi agenti concorrenti. 2026. La misurazione locale del tempo fino alla fusione rimane indispensabile. ordine di dimensione dell'aggiornamento di febbraio 2026 Valutazione puntuale di circa 18 % percentuale di accelerazione sulla subcoorta storica (intervallo di fiducia −38 % à +9 % percentuale) e circa 4 % Percentuale dei nuovi partecipanti (IC)
   −15 % à +9 %) — un segnale troppo rumoroso per concludere, che METR ha preferito trattare ristrutturando il protocollo piuttosto che pubblicando un singolo numero. Dettagli decisivi per la guida: nel test iniziale, i partecipanti hanno stimato in media di essere ~20 % Percentuale più veloce grazie all'IA mentre erano ~19 % più lento — la differenza tra percezione e misurazione è il motivo per cui questa guida richiede metriche locali (costo per cambiamento accettato, tempo fino alla fusione) piuttosto che il senso delle sessioni.
5. **Le istruzioni di deposito sono utili solo se funzionano.** Le ricerche su `AGENTS.md` Trova un vantaggio quando il file contiene comandi, convenzioni non standard, invarianti e regole di sospensione. Una lunga descrizione generale dell'architettura può aumentare il contesto senza migliorare il risultato.
6. **Il multi-agente non è un multiplicatore automatico di intelligenza.** Aiuta quando le sub-attività sono veramente indipendenti, che le responsabilità e i file sono separati e che un agente radice sintetizza. su uno stato mutabile condiviso, aumenta i conflitti, i costi e gli errori di coordinamento.
7. **Un patch tecnicamente corretto non è sufficiente per valutare un agente.** Misura anche il rispetto dello scopo, le regole di sospensione e le convenzioni, la qualità del piano, la capacità di segnalare l'incertitudine e il costo della revisione umana. Due agenti che passano gli stessi test possono avere un valore molto diverso se uno genera due volte più rework o cambiamenti al di fuori del perimetro.
8. **La memoria, le competenze e le regole persistenti diventano una superficie di ingegneria.** Gli agenti in grado di sviluppare la propria memoria, le loro abilità o il loro routing non dovrebbero mai promuovere questi cambiamenti. Qualsiasi evoluzione persistente deve essere diffusa, versata, testabile, rivista e reversibile prima dell'attivazione.
9. **Una grande finestra di contesto non rimuove il *Il contesto rot*.** Le valutazioni 2026 distingue la capacità fisica della finestra e la qualità efficacia dell'uso del suo contenuto: con la stessa attività, più tokens possono degradarsi recupero, rispetto delle restrizioni e ragionamento molto prima del limite massimo. 1M tokens”, ma mantenere un **Set di lavoro minimo e decisivo**I subagenti isolati sono una parata strutturale: consumano localmente un sacco di contesto e riferiscono al genitore solo un risultato condensato.

Conclusione: il livello di confine aumenta la superficie di possibili compiti, ma la qualità dell'ingegneria intorno all'agente rimane il fattore controllabile più importante.

<!-- section: s-2 -->
### Complemento metodologico

> **SWE-bench Pro non sostituisce solo SWE-bench Verified.** OpenAI Ora si ritiene che circa 30 % Percentuale dei compiti di
> SWE-bench Pro sono anche difettose: test troppo rigorosi, requisiti nascosti assenti del prompt, copertura
> insufficiente o errata registrazione. l'audit 8 Giugno 2026
> (Pipeline automatizzata è: 27,4 % Percentuale dei 731 Testi pubblici segnati; annotazione da cinque ingegneri senior: 34,1 %)
> Inoltre ha guidato OpenAI à **Rimuovere esplicitamente la sua raccomandazione** per effettuare la valutazione di codifica di
> riferimento — un segnale più forte dell'unica stima. Il portfolio di valutazione corretto quindi combina diversi assi
> Piuttosto che un nuovo
> Classificazione unica.

| Asse da misurare                | Valutazione utile                 | Quello che rivela                                                                               |
|------------------------------|----------------------------------|-------------------------------------------------------------------------------------------------|
| Correzione di deposito classico | SWE-bench, con audit delle attività | Capacità di riparazione su uscite isolate                                                       |
| Il compito originale lungo       | **Il DeepSwe**                      | Contaminazione ridotta, verificatori scritti per accettare diverse soluzioni valide           |
| Collaborazione iterativa      | **Il SWE-Interact** di SWE-Together | Scoperta di intenzione, memorizzazione delle restrizioni, necessità di correzioni umane            |
| Esplorazione del deposito         | **Il SWE-Explore**                  | Localizzazione a livello di linee e efficacia del contesto                                     |
| Ciclo completo                | **Il SWE-Cycle**                    | Ricostruzione dell'ambiente, implementazione e generazione di test in una stessa traiettoria |
| La realtà del tuo lavoro       | **Il benchmark Scala privato**        | Costo e qualità su Play, Pekko, Tapir, Spark, impliciti, serie e costruzione reale          |

Per un compito di codice, misurare il **Costo per cambiamento accettato** per la gestione della consegna, il **Costo per cambiamento stabilito e stabilito** (sezione 15b) non il tasso di successo brutto:

```text
costo per modifica accettata
= token + latenza + minuti di lavoro umano + CI + rilavorazioni + difetti sfuggiti
```

Utilizza un'unità comune per accumulare questi costi (ad esempio euro con un costo orario esplicito), o mantiene i componenti separati. I tokens e i minuti non si aggiungono direttamente. Per il costo fino alla produzione, aggiunge la distribuzione, la validazione del runtime, rollback/hotfix e i difetti osservati durante una finestra fissata prima della misura. Non si considera stabile che un cambiamento abbia terminato questa finestra.

Non cercare una "produzione AI" globale. Stratifica al minimo le misure per **greenfield, manutenzione, legacy, bugfix, migrazione, refactor e codice critico** : gli studi 2026 ottenere risultati contraddittori proprio perché non misurano sempre le stesse attività, sviluppatori o costi di revisione.

<!-- section: s-3 -->
### Un benchmark verde non è ancora un diff fusibile

La valutazione METR è stata effettuata su 296 PR generati da agenti ha scoperto che il grade SWE-bench ha dato in media **24,2 punti di successo di più** che i manutenti incaricati di valutare se il cambiamento era veramente utile e fusibile; circa la metà dei PR che passavano i test non sarebbero stati mollati. Il campione si riferisce solo a tre depositi, modelli precedenti alla generazione più recente e un solo test senza iterazione sul feedback manutente: questo non è un limite fondamentale di capacità, ma questo invalida l'equivalenza naiva `tests du benchmark passants = changement acceptable`.

Per i compiti lunghi, SlopCodeBench osserva inoltre un accumulo di duplicazione, verbosità e erosione strutturale mentre i punti di controllo si arricchiscono. Un rapido richiesto di qualità riduce alcuni difetti all'inizio senza eliminare la loro crescita. Il buon regime di prova quindi accumula quattro barriere indipendenti:

```text
contratto di business esplicito
→ riproduzione che fallisce prima della correzione
→ test deterministici, proprietà e test di mutazione
→ una persona responsabile rivede il diff, il perimetro e la manutenibilità
```

I punti di riferimento servono alla routing e agli esperimenti; non devono mai diventare un permesso di autonomia o di fusione.

> **Differenza tra scrivere e consegnare.** Il Working Paper NBER *Codice di scrittura vs. Codice di spedizione* osservare, su più di
> 500 000 sviluppatori GitHubUn aumento stimato dell’attività è molto più elevato per i commeti che per le
> Progetti e rilasciati. lo studio rimane osservativo con apparizione: non dimostra un effetto causale
> limitare il WIP alla capacità di revisione e consegna, e misurare fino alla produzione.

<!-- section: s-4 -->
### Guarda la produzione per il Vibe Coding

Gli studi empirici di 2026 su applicazioni veramente "vibe codificate" si trovano famiglie di difetti ripetuti: logica provvisoria lasciata in produzione, entrate non filtrate, segreti esposti, dimenticato di restrizioni nel corso delle torri e ottimizzazione locale che deteriora il sistema globale. Un modello più forte o un modello migliore rapido riduce questi difetti, ma non li elimina.

> **Ordine di dimensioni misurate in 2026.** L’audit di 200 applicazioni “vibe codificate” e implementate
> (1 471 vulnerabilità valide) trova almeno una vulnerabilità in **90 % dei depositi**di cui più di tre
> Quartes di gravità alta o critica; il controllo di accesso rotto appare in 75,5 % percentuale dei depositi, circa 20×
> La linea di base OWASP 2025Una scansione indipendente di 1 400+ applicazioni finiscono nella stessa ordine di dimensioni (65 %
> hanno almeno un problema di sicurezza, 58 % almeno un percentuale di vulnerabilità critica, 400+ segreti esposti)
> L'analisi delle cause radiali classifica questi difetti in tre famiglie - **Memoria** (conflitti dimenticati tra i
> di tour, **obiettivo** (optimizzazione locale che deteriora il sistema globale) e **Conoscenza** (patterni pericolosi
> riprodotti): esattamente i tre meccanismi che i gatti deterministi e la rivista umana di questo guide devono
> interrompere, poiché nessuna immediata correzione duraturo.

```text
Prototipo in vibe coding
→ nessun dato o chiave di produzione
→ test funzionali + sicurezza + prestazioni + manutenibilità
→ revisione umana del diff e delle dipendenze
→ passaggio al flusso agentico controllato
→ solo allora: distribuzione
```

Una sessione di codifica vibe non dovrebbe mai spingere direttamente nella produzione, anche quando la dimostrazione sembra funzionale. **Cambiamento del regime di prova**Non è solo un passo successivo del gatto.

