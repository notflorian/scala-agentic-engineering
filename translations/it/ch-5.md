<!-- section: chapter -->
# 5. Flusso di lavoro standard per un’attività di dominio in Scala

<!-- section: s-1 -->
## Passo. 0: L'uomo che sta colando

Prima dell'AI, scrivi o chiarisci:

```text
Objectif :
Comportement actuel :
Comportement attendu :
Contraintes métier :
API publique à préserver :
Fichiers probablement concernés :
Tests ciblés :
Validation harness :
Risque :
Critère d'acceptation :
```

Numeri importanti requisiti di business e invarianti ([`REQ-01`], `REQ-02`, ecc.). Per ogni esigenza, dichiara la prova o la prova prevista prima dell'implementazione; un requisito senza oracolo deve essere esplicitamente contrassegnato e arbitrariato. Nella PR, combina il requisito, il comando/test, il risultato, convalidato SHA e i limiti di prova. La matrice di tracciabilità può rimanere molto breve per un biglietto banale.

`Validation harness` deve nominare **prima della modalità di scrittura** prova che l'agente può eseguire se stesso: compilazione mirata, test unità/integrazione, correzione ScalaCheck, scalafmt, forse addirittura Stryker4s Se ancora non sai come dimostrare che il cambiamento è corretto, il compito non è pronto ad essere delegato.

Senza questo, si paga i modelli per scoprire il problema invece di risolverlo.

> **Posizionamento vs. stato dell'arte 2026 ("Spec-Driven Development")** : questo inquadratura è esattamente ciò che serve
> l'industria si è formalizzata sotto il nome di SDD, diventare il contrappeso dominante a "vibe coding" — spec astenersi
> L'artefatto più redditizio prodotto dagli esseri umani quando l'agente scrive il codice.GitHub] Spec Kit, OpenSpec, urgente
> AWS Kiro, notazione EARS per i requisiti provabili) può strutturare questo flusso di lavoro, ma non è obbligatorio:
> già pratico guida la variante **spec-anchored** (le cornici spec e sopravvive al compito, il codice + test rimangono visibili
> la fonte della verità), che è la postura raccomandata per il codice commerciale esistente — al contrario della necessità
> **spec-as-source precedenti** (l'uomo modifica solo spec), che è ancora sperimentale.
> campo: il livello di dettaglio della specifica deve seguire la * criticità[* del codice — sovraspecificando uno script usa e getta è previsto
> di rifiuti, sotto specificando un contratto pubblico è una deriva garantita.
>
> **Scegliere un tooling impegnativo SDD senza framework-sprawl.** Il paesaggio circostante SDD
> Ora più di trenta quadri ([Spec Kit]], OpenSpec, Kiro, BMAD-METHOD, GSD, Tessl...).
> Le seguenti pratiche emergono: **GitHub Spec Kit** per greenfield (constituzione casuale → specificatamente → chiarimenti → Pianificazione →
> check-list → Servizi → analizzare → implementazione → convergere, con gradini di controllo opzionali);
> **OpenSpec per il tempo libero** per campo bruno iterativo — le specifiche riprodotte nel repo con frequenza *delta marketers anticipato* per cambiamento, il vuoto
> postura più vicina alla variante spec-anchored di questa guida; **AWS Kiro** se si desidera che l'integrazione EARS notazione
> e l'ecosistema AWS. Nessuno è un prerequisito: se `AGENTS.md` + il pacchetto di inquadramento sopra + le porte CI
> (sezione) 15A) già fanno il lavoro, aggiungendo un quadro aggiunto SDD aggiunge contesto, non qualità.
> negotiable: spec vive nel repo e sembra il codice — una spec tenuta fuori dalla versione diventa un secondo fattore
> fonte di verità diverges.

> **Due Harnesses da non confondere.** A Paper SDD pubblicato su Altro 31 Agosto 2026 offre un'utile distinzione tra
> **tecnica e tecnica** (modello, strumenti, contesto, autorizzazioni, test) e lievitazione **Metodologia Harness casuale** (spec, ruoli, abilità)
> Questo vocabolario **conferma** la struttura di questa guida:
> Claude Code, Codex o MCP]] non sostituisce la disciplina delle specifiche e della validazione umana.
> Tuttavia, principalmente concettuale e in gran parte basata sulla letteratura grigia; utilizza questa distinzione
> come quadro di progettazione, non come prova empirica che un determinato quadro SDD migliora la produttività.

> **Prima Real Practice Data.** Il CMU/Google Studio "Spec-Driven Development come Prescribed casual
> e come praticato" ha osservato che i professionisti esperti applicano già il SDD
> ** modo selettivo, soprattutto per nuove caratteristiche o cambiamenti rischiosi**, con specifiche scritte da agenti da un'intenzione
> Il difetto principale è quello dell'essere umano, e poi leggere di nuovo, e un controllo principalmente da test scritti da agenti.
> **Silent drift spec ↔ code[** quando non esiste un piano di manutenzione; Thoughtworks restituisce aggiungere ulteriore indicazione
> [*] istruzioni bloat* (specs e contesto che crescono fino a quando l'agente perde il thread).
> regole di questa guida: dosaggio di criticità, e spec versioned e recensito. Aggiunge solo una terza regola:
> **un test scritto dall'agente non convalida la propria spec**; mantiene la prova riproduttiva che non riesce prima della patch
> e il test di mutazione (sezione 5], passo 4). Nell'attrezzo, **`/speckit.converge`**] rilegge il codice contro l'interruzione
> `spec.md`, `plan.md` e non è così `tasks.md` e non è così **aggiunge solo compiti mancanti per arrivare `tasks.md`**. E' un controllo della frequenza
> la consistenza utile dopo l'implementazione, **non un oracolo**: né test indipendenti né revisione umana dovrebbero comportare
> essere cancellato sul pretesto che Spec Kit annuncia "Converged".

<!-- section: s-2 -->
#### Modello di spec operativo (copy-paste) casuale

Questo modello materializza la variante spec-anchored della guida. Vive nel repo (ad esempio `specs/TICKET-123.md`) e sembra codice.

<!-- section: s-3 -->
# SPEC: [TICKET-obiettivo123] — [Short title]

<!-- section: s-4 -->
## 1. Obiettivo (1 frase, azione verb)

[Es: "Aggiungi un tasso di sconto di livello di quantità al Servizio Sconto"] regolarmente

<!-- section: s-5 -->
## 2. Non oggettivi (esplicito, anti-driving) frequenza

- [Ex: "Non modificare il calcolo dello sconto esistente tramite codice promozionale"]
- [Ex: "Non toccare il pubblicoAPI del modulo di ricarica"]

<!-- section: s-6 -->
## 3. Comportamento previsto (regole aziendali, numerate)

1. [Regole di sicurezza] 1 : se quantità > = quantità 10, remise precedenti 5%]
2. [Regole di sicurezza] 2 : se quantità > = quantità 50, remise precedenti 12%]
3. [Rule 3: i cuscinetti non cumulano, il più alto si applica]

<!-- section: s-7 -->
## 4. vincoli tecnici dovuti

- API pubblico da conservare: [accurate firms] casual
- Serializzazione automatica JSON: [unchanged / aggiungi campo X con bussola posteriore]
- Prestazioni: [nessuna richiesta DB aggiuntiva in hot path]
- Concorso: [immutabile / atomità necessaria]

<!-- section: s-8 -->
## 5. I file probabilmente interessati

- `src/main/scala/.../DiscountService.scala`
- `src/test/scala/.../DiscountServiceSpec.scala`

<!-- section: s-9 -->
## 6. Test di accettazione (fatto criteri)

| Requisito/invariante | Prove previste |
|----------------------|-----------------|
| REQ-obiettivo01: soglie 10 | Test unità: 9 → 0 %, 10 → 5 % |
| REQ-obiettivo02: soglie 50 | Test unità: 49 → 5 %, 50 → 12 %; reset di proprietà ≤ operazione 12 % |
| REQ-obiettivo03: non cumulativo : | test di non regressione su cumulation; sconto invariato codice promozionale |
| REQ-obiettivo04: contrazione JSON | Test di compatibilità |
| REQ-obiettivo05: prestazioni : | Misurazione del numero di query DB sullo scenario di integrazione |

- [ ] Testare la mutazione: punteggio / mutanti importanti per giustificare i file interessati
- [ ] Risultati SHA e Requisiti; Eccezioni esplicite e Rischio Residuale

<!-- section: s-10 -->
## 7. Rischi e mitigazioni

| Rischio di scherma               | Probabilità | Impatto | Mititazione                      |
|----------------------|-------------|--------|---------------------------------|
| [Arrondi BigDecimal] | Medioriente       | Il mio nome   | [Use RoundingMode.HALF_UP] |

<!-- section: s-11 -->
## 8. Definizione di fatto (final blacklist)

- [ ] Compile senza preavviso
- [ ] Test mirati verdi
- [ ] scalafmtCheckAll Pass aggiuntivi
- [ ] Recensione secondo modello completato
- [ ] Diff < [N] linee alternative
- [ ] Nessun file off-scope modificato

Livello di dettaglio adattato alla criticità:

- Monouso Script → Sezioni 1, 2, 6 sufficienza
- Contratto pubblico / soldi / sicurezza → tutte le sezioni obbligatorie

---

<!-- section: s-12 -->
## Passo. 1: Ricerca mirata

Utilizzare in questo ordine:

1. **Sourcebot** per individuare i file, usi, test.
2. **IntelliJ** per controllare simboli, tipi, gerarchie.
3. **Context7** se un esterno API o una versione recente è coinvolta.
4. **Qwen locale per il tempo libero** per produrre un briefing.

Prompt Qwen: anticipazione

```text
Analyse ces fichiers et produis :
- résumé du flux métier
- classes et méthodes impliquées
- invariants à préserver
- tests existants
- risques
- ambiguïtés
- prompt propre à donner à Claude Code

Ne propose pas encore de patch.
```

---

<!-- section: s-13 -->
## Passo. 2: piano dello scrittore, senza modifiche

Scrittore di prompt (trasferimento)Codex] or Claude Code):

```text
Tu es l'agent writer de cette tâche.

Objectif :
[objectif]

Contraintes :
- diff minimal
- pas de changement d'API publique sans validation explicite
- préserver les comportements existants
- ajouter ou adapter les tests
- procéder par petites étapes
- expliquer les risques
- ne rien modifier avant validation

Commence par explorer le code et proposer un plan.
```

Regola del documento: **Nessun piano, nessuna modalità di scrittura**. Il piano deve elencare i file da modificare, i file da lasciare vuoto, la strategia di prova, i rischi e la dimensione prevista del diff.

---

<!-- section: s-14 -->
## Passo. 3: piccola implementazione :

Prompt: anticipare

```text
Exécute uniquement l'étape 1.
Ne touche pas aux autres étapes.
Garde le diff minimal.
Après modification, donne :
- fichiers modifiés
- raison de chaque changement
- commande de test ciblée
```

Per favore. Scala, evitare i grandi refattori automatici. Richiedi lotti di correzione 30 à 300 Le linee di diff quando possibile. I ritorni sul campo e gli studi recenti sulle PR convergono a piccole, strette PR, più facile da leggere e meno inclini a guasto CI. A livello organizzativo, lo studio della distribuzione teorica Claude Code / Copilota CLI a Microsoft (arXiv, luglio) 2026, decine di migliaia di ingegneri) misure ~24% delle PR mescolate più tra gli adottivi — l'effetto è reale, ma si materializza in PRs arrivare *Recensione di:*, non in giganti diffs.

---

<!-- section: s-15 -->
## Passo. 4: validazione IntelliJ + test

Agenti LLM sono noti per scrivere test "percorso felice" (test che passano ma non controllano casi di errore o limiti). Scala/SBT :

```text
scalafmtCheckAll
compile
Test / compile
testOnly <TestCiblé>
IntegrationTest / testOnly <TestCiblé>
```

Poi solo se il rischio lo giustifica:

```text
test
IntegrationTest / test
```

> **Nota sbt:**] configurazione `IntegrationTest` è **]deprecisa dal sbt 1.9.0]] ** per un sub-progetto simbolico
> dedicato (ad esempio un modulo `it`]] che `dependsOn(core % "test->test")`) o contrassegnati test. Se il tuo progetto lo utilizza
> di nuovo, i comandi di cui sopra rimangono validi, ma non lasciare mai che un agente migra questa configurazione da solo — contrassegnare
> È esattamente il tipo di cambiamento `build.sbt` che deve passare attraverso una validazione esplicita.
> modulo, addestramento
> andare direttamente a un sottoprogetto `it`. Pensate anche a dare all'agente l'ordine più veloce disponibile:
> `sbt --client` (o Bloop) evita di pagare per l'inizio di JVM ad ogni iterazione del loop di correzione della prova, questa aggiunta
> Chi è?
> può velocizzare i loop attici. **sbt 2.x**, `sbt` già utilizza la modalità client-server nativo `sbtn`
> default; `sbt --client` è ancora una forma esplicita. Misurare l'inizio del progetto reale: migrazione 1.x → 2.
> e cambiamento di tendenza `build.sbt` richiedono la validazione umana (vedere sezione casuale 15A).
>
> Se non fosse `serverConnectionType` è configurato per evitare `Tcp`, sbt 1.4.0 à 2.0.6 è un'esperienza
> vulnerabile all'esecuzione del codice non autenticata tramite BSP. Rimuove questa impostazione o si muove almeno a volersi **sbt 1.13.0
> 2.0.7**. Il trasporto locale predefinito (Unix socket o denominato pipe) non è interessato.
> prima di esporre la sequenza sbt server a un IDE remoto, agente o contenitore.

<!-- section: s-16 -->
#### Ottimizzazione dei dati sbt per l'agente loops precedenti

La velocità del loop di prova di compilazione è la prima leva di produttività dell'agente. Configurazione consigliata in `.sbtopts` (repo):

<!-- section: s-17 -->
# .sbtopts — ottimizzato per l'attivazione di loop

```text
-J-Xms2g
-J-Xmx8g
-J-XX:+UseZGC
-J-XX:+UseStringDeduplication
-Dsbt.supershell=false
-Dsbt.color=false
-Dsbt.log.noformat=true
```

Spiegazione delle scelte:

- `UseZGC` : opzione da misurare contro il G assegnato1 default sul deposito effettivo; non promettere un guadagno sistematico o si rompe sempre meno di somma 1 ms.
- `supershell=false` e `color=false`: riduce il rumore nelle uscite parsed dall'agente (meno gettoni, meno rotazioni di contesto)
- `noformat=true`: Idem, output grezzi più facili da parse casual

sbt 2.x, `sbt`]] già lancia il client nativo predefinito; `sbtn` rimane un utile ingresso esplicito:

<!-- section: s-18 -->
# Primo lancio (start server)

`sbt`

<!-- section: s-19 -->
# Chiamate successive dall'agente (quasi istantanee avviare)

`sbtn "compile"` `sbtn "testOnly *DiscountServiceSpec"`

Configurazione del server in `project/server.sbt`:

```scala
// Keep the build server on a local transport.
Global / serverConnectionType := ConnectionType.Local
```

Il trasporto locale è normalmente il default: **non espongono il server temporaneo sbt in TCP** per accelerare gli agenti. `build.sbt` solo per nascondere ricompilazioni o assegni: `onChangedBuildSource := IgnoreSourceChanges`, `Test / fork := false` e la disattivazione della Scaladoc può rendere il risultato non rappresentativo della direzione CI Preferite il modulo di destinazione e le suite (opzione`project`, `testOnly`) senza alterare la loro semantica. **sbt 2.x, `test` è incrementale e può riutilizzare i suoi risultati nella cache** : utilizzazione `testFull` per una validazione completa prima di una PR o in modalità CI.

**Benchmark prima/dopo sul vostro deposito.** Confrontare a prezzi bassi JVM e opzioni identiche, su almeno dieci cicli di compilazione incrementale + test mirati: latenza mediana, p assegnato95, riavvicinamenti sbt, pressione della memoria e stabilità dei test. Non presenta un risparmio di costi su un altro progetto come garanzia.

Per i progetti Play Framework o multi-module:

```text
sbt "project api" compile
sbt "project api" "testOnly *DiscountServiceSpec"
sbt "project integration" "testOnly *OrderFlowSpec"
```

Il punto principale rimane: non solo chiedere all'IA di essere cauti, eseguire test.

Scegliere le validazioni in base al rischio reale, senza impilare strumenti inutili:

| Rischio Scala/JVM]] | Evidenze rilevanti |
|------------------|-------------------|
| Calcolo aziendale | ScalaCheck, limiti, mutazione test dovuti |
| Compatibilità binaria / TASTy dovuti | MiMa / TASTy-MiMa quando rilevanti vantaggi |
| REST / JSON abitua | Collaudo, schematica e compatibilità |
| Concorso ed effetti | Ordine controllato, cancellazione, timeout, rilascio di risorse |
| La luce del sole | Datasets deterministici, nulls, schemi, partizioni, idealismo conseguente |
| Prestazioni JVM | JMH o benchmark riproducibili |
| Architettura | Scalafix / funzioni di fitness su bytecode o fonti alternative |
| Sicurezza | SAST in realtà copre Scala, SCA, scansione segreta e test di autorizzazione |

**CodeQL Java/Kotlin non prova una copertura automatica Scala** : Controlla l'elenco delle lingue supportate e testa l'analizzatore selezionato sui difetti noti. Non assegnare uno scanner di dipendenza ad un'analisi di origine.


<!-- section: s-20 -->
### Valore provvisto di test generati

Un test scritto dallo stesso agente dell'implementazione non è un oracolo indipendente. Il lavoro recente rileva che gli agenti producono frequentemente prove di osservazione o di stampa senza affermazioni discriminanti; aumentare il numero di test del prompt non è sufficiente per migliorare il tasso di risoluzione. Altre valutazioni di mutazione mostrano che le suite verdi non rilevano difetti realistici generati dagli agenti, e che la loro efficacia si deteriora anche quando il codice si evolve senza previsto cambiamento semantico.

Per un bugfix, mantenere la prova più proficua:

```text
1. ajouter un test de reproduction minimal ;
2. vérifier qu'il échoue sur le commit de base pour la bonne raison ;
3. appliquer le patch ;
4. vérifier que ce test puis la suite pertinente passent ;
5. faire varier l'oracle : propriétés, cas limites, tests métamorphiques ou mutants ciblés ;
6. faire relire le test avant l'implémentation lorsque le domaine est critique.
```

Non impostare una soglia di mutazione universale che incoraggerebbe "giocare la metrica". Confronta il punteggio sul perimetro interessato, richiede una giustificazione per ogni mutante superstite maggiore ed è principalmente l'assunzione **delta di mutazione segna punteggio casuale**, regressioni sfuggite e ritorni di revisione. Un test che non poteva fallire prima che la patch non dimostra la correzione.

**La fase di indurimento (Mutation Testing):** Una volta che l'IA ha scritto i test e sono verdi, convalida la loro robustezza con frequenza Stryker4s:

```text
sbt "project api" stryker
```

Un punteggio basso **può essere** rivela test insufficienti, ma anche mutanti equivalenti, irrilevanti o scarsamente mirati. Prima di esaminare i mutanti sopravvissuti, il loro impatto commerciale e le esclusioni; non aggiungere affermazioni artificiali per aumentare il punteggio. Se un mutante importante rimane vivo, restituisci il rapporto all'agente chiedendo un compromesso. **test di comportamento osservabile indipendente dalla patch casual**, poi riavviare i test mirati.

---

<!-- section: s-21 -->
#### Passo. 5: Verifica della forza prima della dichiarazione di completamento

Gli agenti LLM dichiari spesso "fatto" senza aver controllato. Aggiungi questa istruzione sistematica alla fine di ogni richiesta di implementazione:

Prima di dichiarare questo compito completato, si MUST: somma

1. Esegui il comando compilazione e mostra risultati casuali
2. Eseguire il test mirato e mostrare il risultato casuale
3. Controllare il diff dal database approvato, modifiche impegnate e non accettate, e i file non tracciati
4. Elenca i file modificati con motivo per ogni cambiamento
5. Se un passo fallisce, corretto e ripetuto da 1] Non dire "fatto" a meno che i 5 punti sopra siano soddisfatti.

Per automatizzare questi controlli, utilizzare gli script comuni nella sezione 5] (hooks) e sezione CI 15A. Il gancio `PostToolUse` compila solo: `Test/compile`] non esegue i test. I risultati delle suite e il diff completo devono essere associati al candidato SHA, e il CI deve ripetere la validazione in modo indipendente.

Variante per compiti critici (sicurezza, denaro, contratto pubblico):

Prima di dichiarare questo compito completato, eseguire e mostrare:

1. sbt compila (errore zero, zero warning new) Correzione
2. sbt "testonly *SpecFiblé" (tutti verdi)
3. sbt scalafmtCheckAll (conformare la formattazione)
4. Diff base necessaria → candidato e stato completo Git (solo file di piano)
5. Controllare che il diff NON contenga: TODO, FIXME, debug println, import inutilizzato, cambio della firma pubblica non richiesta Mostra il risultato di ogni passo. Se un passo non riesce, corregge e ripete. Non dichiarare "fatto" prima che i passi 5 siano verdi.

---

<!-- section: s-22 -->
## Passo. 6: auto-recensione da parte dello scrittore

Prompt: anticipare

```text
Fais une review de ton propre diff avant de le transmettre au reviewer indépendant.
Liste :
- risques métier
- cas limites
- tests manquants
- changements inutiles
- fichiers à relire manuellement
- hypothèses que tu as faites
```

Questo passaggio spesso rimuove gli errori evidenti prima di una recensione esterna. **Non vale mai la pena approvare**: l'agente che ha scritto il diff condivide le stesse ipotesi della sua implementazione e non può costituire il cancello finale; lo scrittore può ripulire; un contesto fresco di distinzione **l'altra famiglia di modelli precedenti** deve fornire i suoi risultati indipendenti. L'uomo accetta.

---

<!-- section: s-23 -->
## Passo. 7: recensione indipendente dall'altro modello famiglia casuale

Prompt reviewer: probabilità **Opus 5.5 Medioriente** se non fosse Codex ha scritto; **GPT‑6.2 Sol Medioriente** se Claude ha scritto. Andare in alto per una PR rischiosa e a Astra Light/Fable Low solo se la capacità aggiuntiva è giustificata:

```text
Act as an independent senior Scala/JVM code reviewer.

Review the exact PR head SHA against its merge base, approved specification, acceptance criteria and AGENTS.md.
Work in a fresh read-only session; do not modify the implementation. Do not rely on the writer's reasoning
until you have formed your own assessment.

Prioritize functional correctness, preserved invariants, regressions, compatibility, test oracle quality,
error handling, resource safety, concurrency, performance, security and scope violations.

For every actionable finding, provide severity, file/line, reviewed SHA, violated requirement or invariant,
a concrete failure scenario or reproduction, the smallest plausible correction, and remaining uncertainty.
Distinguish verified defects from hypotheses. Ignore stylistic preferences and unrelated refactoring.
Do not invent findings. Return a concise verdict and evidence-backed findings only.
Never approve or merge the PR yourself.
```

Variante con classificazione di gravità macchina-funzionale — preferibile per smistamento e un cancello alimentato solo da risultati convalidati in modo indipendente (vedi l'esempio di decodifica digitato nella sezione casuale 12):

```text
Classe chaque retour avec exactement un de ces labels :
- BLOCKING        : bug métier, perte de données, faille, contrat public cassé
- REGRESSION_RISK : comportement existant potentiellement altéré, cas limite non couvert
- STYLE           : lisibilité, convention, nommage — jamais bloquant
- OUT_OF_SCOPE    : amélioration valable mais hors ticket — à ignorer dans cette PR

Retourne uniquement du JSON valide :
{
  "findings": [ { "severity": "...", "file": "...", "message": "..." } ],
  "summary": "..."
}
```

La regola di cancello associata: `BLOCKING`] e `REGRESSION_RISK` devono essere trattati o esplicitamente contestati prima della fusione; `STYLE` è facoltativo; `OUT_OF_SCOPE` lascia nel backlog, mai nell'attuale diff.

Queste etichette restano soggette **recensione presupposto**Ogni ritorno di blocco deve essere prova verificabile: file e linea, violazione del contratto, riproduzione, guasto di prova o regola statica precisa. Senza prova, va in ordine umano; l'autoetichetta di un modello non deve mai bloccare una fusione da solo. Questa validazione evita costosi falsi positivi e loop "autoritratto IA pianificazione ↔ Recensione IA" che bruciano crediti senza nuove informazioni.

Il modello consigliato rimane: **uno scrittore, un recensore dell'altra famiglia**. Cross-examination è un'ipotesi di lavoro, non una garanzia: uno studio preliminare *Cross-Model alternative LLM Codice recensione* su di noi 116 problemi algoritmici con conseguente Opus 4.7 / GPT-5.5 osservato un guadagno Codex → Claude (in inglese)71,6 → 89,7 % successo) e una goccia Claude preoccupante → Codex (91,4 → 82,8 % o il programma è riscritto dal recensore senza eseguire le prove; Scala. Il recensore rileva e giustifica; lo scrittore corregge dopo la selezione. Misura i veri/falsi positivi, mancati difetti e regressioni introdotte dalle correzioni. Dopo una piccola correzione, mirata ri-revisione dei cambiamenti e degli invarianti; revisione completa solo se il rischio o la portata è cambiata.

> **Sforzo e limiti della recensione.** Suggerimenti 90 Django patches, uno studio preciso *Quanto sforzo fa un AI Code Reviewer urgente
> Necessità?* Trovare Opus 5.5 Media non inferiore a quella alta in un margine predefinito di probabilità 15 punti, ad un costo medio
> meno di circa 20 % Anche l'Alto accetta l'invito 45 % delle patch considerate errate dall'oracolo rinforzato; alcuni lievitazione
> le etichette rimangono discutibili. CR-obiettivoBench-v2 (584 difetti verificabili associati alle PR) conferma che la copertura
> Questi risultati rafforzano Media per la vita di tutti i giorni, ma non dimostrano che l'aggressione
> l'equivalenza universale Medio/alto e l'efficacia dei modelli attuali su Scala. Nessun cancello autonomo LLM.

 Per impostazione predefinita: **Soil: Sol 6.2 Media scritta → Opus 5.5 Media recensione**, ou eccitazione **Opus 5.5 Medio/alto scritto → Soil: Sol 6.2 Media recensione**. Luna/Haiku sono utilizzati per compiti meccanici; Astra/Fable sono solo mobilitati in escalation. `Ultra` rimane riservato alle missioni decoupable in assassi indipendenti.

---

<!-- section: s-24 -->
## Passo. 8: Correzione mirata

Non chiedete mai al recensore di applicare automaticamente tutti i suoi suggerimenti. Selezioni utili ritorni, poi tornate all'originale **writer**:

```text
Voici les retours de review que je valide :
[liste]

Corrige uniquement ces points.
Ignore les suggestions optionnelles.
Garde un diff minimal.
Relance les tests ciblés.
```

**Interrompe la revisione quando i criteri sono verdi.** Un passaggio corretto dopo la revisione è il default; un secondo è giustificato solo da un ritrovamento `BLOCKING` / `REGRESSION_RISK` Non utilizzare un tipo di prompt "iterario" fino a quando non è perfetto: oltre il miglior checkpoint, l'agente spesso finisce per inventare cambiamenti per soddisfare la domanda e può degradare il diff.

Se è richiesto un nuovo pass, confronta sistematicamente il nuovo diff al punto di controllo precedente e mantiene la versione che meglio soddisfa gli errori **spec + test + portata esatta**, non la versione più recente.

Se deleghi la correzione post-PR a Codex (modalità Goal, Heartbeat o Cloud), `/steward` o PR Steward (sezione 12), trasferisci esplicitamente la proprietà del ramo, con lo SHA iniziale, spec e solo ritorni consentiti. Smettere di monitorare prima di qualsiasi ripresa dello scrittore originale. Qualsiasi nuovo commit ravviva le relative validazioni; la revisione indipendente dovrebbe concentrarsi sul diff finale, non sulla SHA prima della correzione automatica.

<!-- section: s-25 -->
## Passo. 9: anti-guida salvaguardie dovute

Aggiungere regole di spegnimento esplicite, ridurre diffs inutili, cappi di correzione e crediti bruciati:

```text
Stop immédiat si :
- l'agent touche un fichier hors plan sans explication ;
- l'agent modifie build.sbt, plugins.sbt, resolvers ou versions sans validation explicite ;
- la même erreur de compilation revient 2 fois ;
- les tests ciblés échouent 2 fois avec des causes différentes ;
- le diff dépasse la taille annoncée ;
- le correctif commence à changer l'architecture au lieu de résoudre le ticket.
- l'agent tente une écriture destructrice, un push, un déploiement, un partage externe ou une action sur des secrets
  qui n'étaient pas explicitement autorisés.
```

In questo caso, non riavviarlo. Chiedi invece:

```text
Stop. Résume l'état exact :
- fichiers modifiés
- hypothèses faites
- erreur actuelle
- commandes exécutées
- prochaine action minimale proposée
Ne modifie rien.
```

> **Resuscitare senza pagare due volte per la stessa esplorazione.** Tre meccanismi Claude Code per sapere:
>
> - **Checkpoints**: ogni prompt crea un checkpoint (snapshot dei file prima di ogni edizione dagli strumenti di visualizzazione
>   Claude). `Échap Échap` o `/rewind` ripristina la conversazione, il codice o entrambi ad un punto precedente, incluso
>   Dopo la chiusura del terminale. Limite noto: solo modifiche effettuate tramite strumenti di editing Claude
>   sono seguiti, non quelli lanciati in Bash — un checkpoint non sostituisce un commit o un worktree.
> - **`/compact` Non lavare una cattiva ipotesi**: la compattazione riassume la conversazione e * ha conservato* così tanta voglia
>   l'ipotesi sbagliata che il modello si ripeta. Quando l'agente torna due volte alla stessa falsa traccia, la parata è destinata
>   `/clear` poi una rapida serratura con il nuovo stato — non una compattazione aggiuntiva.
> - **Le autorizzazioni in Deny-by-default**: `settings.json`] accetta le regole permettono / chiedono / negano; combina aallowlist pianificazione
>   stretto con esplicito negazione (rete, file critici, spinta) piuttosto che hand-in-loop approvazione.
>   Questa è la versione del prodotto delle regole non automatiche della sezione 3 .
> - **Modalità automatica di default**: dal 14 agosto 2026, la modalità automatica è la modalità di autorizzazione predefinita per le notizie aggiornate
>   sessioni su piani Pro, Max e Team. Il suo classificatore riduce le interruzioni, ma non è un gate temporaneo
>   commercio: assicurarsi che le vostre regole `deny` su `build.sbt`, migrazioni, flussi di lavoro CI e la spinta rimanga attiva (l'obiettivo principale
>   * regole di negazione dure* del blocco di modalità auto senza tener conto delle eccezioni `allow`), e mantenere i ganci sotto.

<!-- section: s-26 -->
#### Claude Mods: quando superare i classici ganci casuali

Da quando? **Claude Code 2.1.287**, una volta **Modo per l'uso** è un plugin il cui JavaScript/TypeScript handlers run in the process casual Claude Code. Un maniglione può arrivare **osservare, riscrivere o sostenere** un evento: chiamata strumento, prompt, turn, comando o interfaccia di rendering. MCP : un'altra MCP fornisce strumenti da un processo/servizio esterno; un Mod può cambiare il comportamento dell'imbracatura stessa. **3 Ottobre 2026**, la versione precedente 2.1.288 aggiungere già `$.ui.selection()` e diverse patch Mods/plugins: tratta quindi questo fattore API Come si dice? **giovani e in evoluzione**, e pin la versione successiva Claude Code per qualsiasi Mod che diventa critico nel flusso di lavoro.

| Per saperne di più                                                                                                 | Preferentializzazione |
|--------------------------------------------------------------------------------------------------------|----------------------|
| Ripetere le istruzioni/method                                                                 | **Abilità**            |
| Fornire l'accesso a un sistema esterno o strumento casuale                                                        | **MCP**              |
| Bloccare, autorizzare o registrare un evento con una regola semplice                                        | **Impostazioni aggancio**    |
| Interattivo UI, stato dell'evento, comando locale, intercettazione/rewrite assegnato | **Mod**]]              |

Il modo di cambiare API può salvare comandi, strumenti e sottoagenti, chiamare un modello, leggere lo stato e l'utilizzo della sessione, mantenere un negozio condiviso, leggere / scrivere file, eseguire un processo, chiamare HTTP o un documento temporaneo MCP, e comunicare con altre sessioni. Mods lavorare con i loro ganci nel terminale — compreso il terminale incorporato e plugin aggiuntivi JetBrains — così come nel Codice Tab di Claude Desktop; gli elementi dell'interfaccia utente non vengono restituiti su tutte le superfici senza testa/cuore.

**Non sostituire i tre ganci di shell qui sotto con un Mod solo perché è possibile.** Per cancelli semplici e deterministici (obiettivo`build.sbt`, migrazioni, max diff, prove obbligatorie), un gancio di regolazione rimane più piccolo, più leggibile e più facile da controllare. Utilizzare un Mod solo se avete bisogno di stato cross-event, un IU, un flusso di lavoro interattivo o un'intercettazione che il gancio classico esprime scarsamente.

> **Un confine di fiducia molto più ampio.** Un Mod corre con i diritti dell'utente, può leggere il significato
> rapido, chiamate degli strumenti, variabili e impostazioni dell'ambiente, processi di avvio o rete, riscrivete un messaggio
> query e spendere quota tramite le chiamate modello. I processi che inizia sono quelli necessari **fuori dalla sandbox Bash accennato** di un'altra
> Claude.
> Un Mod installato può anche approvare alcune chiamate che una regola `ask`] o `PreToolUse` utente avrebbe dovuto passare
> Stopped.
> Le autorizzazioni di Claude non costituiscono quindi una sandbox attorno al codice plugin.

Prima di installare o promuovere un Mod di Terze Parti:

```text
1. Vérifier la source du marketplace et figer la version/commit quand c’est possible.
2. Lire .claude-plugin/plugin.json, hooks/hooks.json, le module register.*, bin/ et .mcp.json éventuel.
3. claude plugin validate ./mon-mod
   → inspecter en particulier les lignes hooks: et calls: sans exécuter le Mod.
4. claude --plugin-dir ./mon-mod plugin details <nom>
   → vérifier l’inventaire réel des composants.
5. claude plugin test ./mon-mod
   → tests de hooks déterministes, sans session, login ni réseau.
6. Si le plugin a des evals : claude plugin eval ... avant promotion.
7. Premier essai avec --plugin-dir dans un worktree jetable ; --safe-mode comme voie de récupération.
```

Per un'organizzazione, il vero controllo deve vivere in **impostazioni gestite** (`allowManagedModsOnly`, ordine di plugin gestiti, casualità `disableAllHooks` in conformità con la politica) e nel Modenziale Integrato `cc-plugin-sec-default`, non nella buona volontà di un User Mod. Per il vostro uso personale, la regola equivalente è semplice: **built-in / codice personale audited > opaque community plugin aggiuntivi**, e nessun aggiornamento automatico di un Mod Sensitive senza rileggere la versione diff.

<!-- section: s-27 -->
#### Configurazione comune del gancio Claude Code / Codex

Separazioni **]local feedback** e non è così ** convalida cancello automatico**. Un gancio su un comando casuale `Edit` non vede necessariamente il Bash, preciso MCP o script IDE; non può garantire il contenimento. `ai-guard.sh` in base alla ricerca di stringhe in un comando: i percorsi dinamici, i collegamenti simlink e le esecuzioni indirette escono da questo filtro. 12; controlla i percorsi effettivamente modificati nel diff finale. I ganci non sono un sostituto per la correzione CI indipendente.

Esempi per un progetto di fiducia, `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$(git rev-parse --show-toplevel)/scripts/ai-compile-check.sh\"",
            "timeout": 120
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$(git rev-parse --show-toplevel)/scripts/ai-stop-audit.sh\""
          }
        ]
      }
    ]
  }
}
```

E' un'altra cosa. `.codex/hooks.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "apply_patch",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$(git rev-parse --show-toplevel)/scripts/ai-compile-check.sh\"",
            "timeout": 120
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$(git rev-parse --show-toplevel)/scripts/ai-stop-audit.sh\""
          }
        ]
      }
    ]
  }
}
```

Entrambe le imbracature chiamano gli stessi script (gli eventi e i carichi specifici per gli strumenti rimangono distinti). Codex richiede rileggere e approvare definizioni di gancio non gestite`/hooks`); non disabilita questo controllo. Un worktree può caricare i ganci del checkout principale; controlla le fonti effettivamente eseguite. I ganci e gli script fidati devono essere protetti dalla scrittura dell'agente; nell'ambiente gestito, posizionarli fuori dal worktree. Non eseguire ganci di progetto non controllati.

Script per il tempo libero `scripts/ai-compile-check.sh` (solo feedback di completamento; può essere disabilitato se troppo comune):

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
logFile=$(mktemp)
trap 'rm -f "$logFile"' EXIT
# Capture the process exit code, not a pattern in the logs.
if sbt --client "Test/compile" >"$logFile" 2>&1; then
  exit 0
else
  exitCode=$?
  printf 'sbt Test/compile failed (exit %s)\n' "$exitCode" >&2
  tail -n 40 "$logFile" >&2
  exit 2
fi
```

Il risultato si basa sul codice di ritorno di autorizzazione sbt, anche senza una linea conseguente `[error]`. `Test/compile` compila i test ma non li esegue. Non utilizzare correttamente `grep` o un comando RTK come arbitro di successo; mantiene il codice di ritorno del comando originale. In presenza di diverse sessioni, non lancia compilazioni concorrenti sullo stesso server sbt.

Script per il tempo libero `scripts/ai-stop-audit.sh` (non-bloccante, comune a entrambi imbracanti):

```bash
#!/usr/bin/env bash
set -euo pipefail
# No transcript heuristics and no forced retry on legitimate blockers.
cat >/dev/null
printf '%s\n' '{"systemMessage":"Completion requires a fresh validation receipt for the exact candidate SHA and independent CI; report blockers without claiming done."}'
```

Il gancio di arresto non cerca mai un ordine nella trascrizione: un riferimento a frequenza `testOnly` Non costringere l'agente a continuare quando un invariante o un bilancio impone una sosta. Per il completamento, richiede la relazione strutturata di autorizzazione `scripts/ai-validate.py` (sezione) 11) e controlli CI le prove locali prodotte sotto l'identità dell'agente sono utili per la diagnosi, ma falsificabili: la politica di assorbimento CI, i suoi script e i suoi risultati devono vivere all'interno di un confine indipendente dall'agente.

Un privilegiato Claude Mod o un gancio inaffidabile può modificare la pipeline; mantenere le restrizioni esterne e i controlli amministrati. Il cancello finale non può essere modificato e quindi auto-approvato dallo scrittore. I ganci possono essere ignorati o non attivati a seconda della superficie; controlla gli eventi, i percorsi e le autorizzazioni effettive prima dell'adozione.

<!-- section: s-28 -->
#### Protocollo di recupero quando l'agente loop

Un loop di agentic (stesso errore, stessa correzione, stesso fallimento) è una modalità di fallimento diversa dal semplice fallimento. Il modello di arrampicata non lo corregge. Ecco il protocollo in 4 passi:

**Step R1 — Stop e estrazione dello stato (0 token aggiuntivo **

Fermare immediatamente l'agente. Non riavviare "fissalo". Esegui: casuale

Stop. Non cambiare nulla. Summarizes 5 punti: sommare

1. File modificati finora (diff dal database approvato + git status)
2. Assunzione attuale su Causa urgente
3. Che cosa è stato tentato e perché non ha funzionato
4. La prossima azione minimale che proporresti
5. Quello che non sei sicuro di volersi

**Passo R:2 — Diagnosi umana con IDE (aumento5-10 min)**

Utilizzare IntelliJ per verificare cosa l'agente non può vedere:

- Il vero tipo di espressione (Ctrl+Shift+P / info type)
- La risoluzione effettiva di un implicito/dato (Ctrl+B sull'Implicit)
- Il tipo di gerarchia atteso vs. prodotto
- Debugger di punto di rottura su comportamento inaspettato

L'obiettivo è quello di trovare le informazioni strutturali che l'agente manca.

**Step R3 — Sessione fresca con contesto stretto**]

/clear Nuovo rapido con ONLY: aumento

- L'obiettivo (obiettivo)1 frase)
- L'esatto file o metodo interessato :
- Errore accurato (copiato dall'IDE, non dalla trascrizione)
- Informazioni strutturali trovate in R :2
- "Propone solo un minimo di cambiamento. Compile e test."

**Passo R:4 — Se fallimenti dopo R :3, modello escalation :**

È solo ora che la scalata Sonnet → Opus → Fable è giustificata, perché il contesto è pulito e il problema è ben posto.

Absolute anti-pattern: riavviare lo stesso modello nello stesso contesto sperando di ottenere un risultato diverso: questa è la definizione del loop.

> **Ri-anchoring periodico, la parata misurata contro la deriva lunga.**
> La ricerca 2026 sull'"agente azionato" (degradazione comportamentale misurata su traiettorie lunghe e la conseguente
> sistemi multi-agenti) converge su tre famiglie di mitigazione: consolidamento episodico della storia in aumento
> riassunti strutturati, ancoraggio comportamentale adattativo (ri-iniezione del charter e obiettivo periodicamente)
> e routing tenendo conto della deriva. Traduzione immediata per le vostre sessioni:
> - **ri-inietta la carta** (oggettiva, non oggettiva, invariante, definizione di fatto) ad ogni pietra miliare e al ritorno di equivalenza
>   subagent — non solo al primo prompt: un vincolo che non è più nella finestra recente non esiste più;
> - ** Generalizza il file di stato** (`MIGRATION_STATE.md`) in qualsiasi sessione lunga, non solo in missioni ufficiali
>   Fable: è l'ancora che sopravvive alle compattazioni e alle ripetizioni;
> - ** circuito di rottura a doppia soglia**: un avvertimento sulla ripetizione della stessa chiamata di strumento o lo stesso strumento chiamarlo
>   errore, poi una dura sosta sulla stessa seconda ripetizione — piuttosto che una sola soglia brutale;
> - ** sessione fresca in caso di loop**: modello di arrampicata non corregge un loop (sezione 3); `/clear` + frequenza
>   status + rereads charter, sì.

---

