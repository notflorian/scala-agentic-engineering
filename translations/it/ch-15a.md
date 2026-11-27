<!-- section: chapter -->
# 15A. CI/CD per flussi di lavoro agentici

CI è il giudice deterministico finale del principio guida — a condizione che si adatta alle PR agentiche, che hanno modalità specifiche di fallimento: prove che non possono fallire, diffs fuori modello, loop costosi.

<!-- section: s-1 -->
## Le quattro PR porte specifiche

```text
1. Gate de gabarit et scope : diff base → candidat, fichiers protégés, taille et nombre de fichiers
2. Gate de qualité de test : suites réellement exécutées + mutation score et mutants importants selon risque
3. Gate de review : findings BLOCKING / REGRESSION_RISK vérifiés traités ou arbitrés humainement
4. Gate de budget : tout job appelant un LLM a un timeout ET un plafond de coût
```

Due assi complementari da considerare una volta che le quattro porte sono in posizione:

- **Architectural drift control** : Thoughtworks Technology Radar (April) 2026) nota che l'uso intensivo degli agenti accelera la deriva tra il codice reale e l'architettura mirata, e raccomanda di collegare controlli deterministici (funzioni di idoneità — ArchUnit, che analizza il bytecode) JVM e quindi anche opere su richiesta Scala compilato) con una valutazione dettagliata LLM a rule ArchUnit "il modulo salta `api` non dipende dall'implementazione » eseguito in modalità CI Costo meno di una torre agente e fermare una deriva strutturale che né scalafmt né compensare Stryker4s Non vedere.
- ** Duplication Control impegnati**: SlopCodeBench (sezione logica) 1A) misura un accumulo di duplicazione sui punti di controllo dell'agente; una scansione simile a jscpd (copy-paste rilevatore che getta le fonti Scala) sui file colpiti trasforma questo segnale in una metrica o addirittura un cancello seguito.La duplicazione è il difetto meno visibile nella revisione umana e uno dei più costosi nella manutenzione ritardata.

Suggerimenti GitHub, **Copilota Code Review o altro Codex Code Review può essere aggiunto come segnale automatico**, ma non sostituisce nessuna di queste porte. Una revisione del bot non è un'approvazione umana; controlla le regole relative GitHub iniziare con una recensione su richiesta o all'apertura, poi prenotare la recensione dopo la correzione alle modifiche che lo giustificano e alle nuove SHA che richiedono la validazione indipendente.

**Claude Approvals non è la prova della qualità.** Una regola `claude: approves` non attiva il Codice Review da solo; `seats: 1` può contare l'autore e gli autori `seats: 0` può permettere una fusione senza lettura umana. GitHub può anche contare l'approvazione del bot nella sua quota di revisione. Per il flusso di lavoro di questa guida, tenere premuto`claude: comments` inizialmente, gli approvatori umani indipendenti nelle squadre, e una fusione umana in solo. Mai usare una classificazione probabilistica come unico arbitro di un cambiamento critico.

La presenza di spicco `.claude/approvals.yml` può disabilitare le recensioni automatiche su percorsi coperti, anche in modalità di osservazione: per tenerli, riferimento `claude/code_review` nelle regole (ad es. sotto controllo `advisory`). Una condizione di Approvamenti non legge i risultati della correzione CI: mantiene i test di compilazione, di test, di scalafmt, di sicurezza e di mutazione, come richiesto controllo GitHub separato. Come squadra, protegge il ramo di destinazione e la politica con CODEOWNERS, proibisce bypass agli agenti e invalida vecchie approvazioni quando il diff cambia. Rende il controllo Approvazioni obbligatorie solo dopo aver valutato le decisioni osservate; non attiva auto-merge o merge coda senza un efficace cancello umano per i cambiamenti che lo richiedono. Un controllo verde, una discussione risoluta o un commento "nessun lavoro validazione non sono mai.

<!-- section: s-2 -->
### GitHub Regole e cancello indipendenza

Impose necessarie verifiche dall'integrazione prevista, senza bypass per le identità di agente; protegge i rami di destinazione, divieto di forza-push e rimozione, approvazione di recenti cambiamenti e invalidazione di vecchie approvazioni quando cambia diff. `CODEOWNERS` per i file di controllo; solo, non configura una regola impossibile da soddisfare da parte dell'autore, mantiene la fusione umana e il controllo politico separato. Non conta un robot di revisione come un umano. `merge_group`In caso di conflitto, cambiamento di SHA o anticipazione della base, rivalutare lo stato; un'eventuale modifica di SHA o anticipazione della base; CI Green su una vecchia revisione non convalida il nuovo candidato.

<!-- section: s-3 -->
## Esempio: `.github/workflows/ai-review.yml`

Esempio per il repository a due moduli in sezione casuale 11 (sbt 1.x). Fig le azioni a un CONDIVIDATO completo e controlla le loro dipendenze transitive; aggiornarle tramite PR dedicato. GitHub, non da un campo di PR controllato dal suo autore. `github.sha` è il candidato per l'integrazione `pull_request` e non è così `merge_group`; la revisione umana riguarda la testa di diff base/PR, distinta da questo commit di prova; per una fusione di coda, i controlli devono essere eseguiti anche sul gruppo di fusione.

```yaml
name: ai-review
on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]
  merge_group:
    types: [checks_requested]

permissions:
  contents: read

concurrency:
  group: ai-review-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: true

jobs:
  deterministic-checks:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6
        with:
          fetch-depth: 0
          ref: ${{ github.sha }}
          persist-credentials: false
      - uses: actions/setup-java@b6effb05e454b25005698d916606bdc6ffcbf961 # v5
        with:
          distribution: temurin
          java-version: '21'
      - uses: sbt/setup-sbt@20cf087132cf939c160f0e53f87ba33634003e3e # v1

      # Validate the integration candidate; fail on a missing base or wrong checkout.
      - name: Validate candidate
        env:
          BASE_SHA: ${{ github.event.pull_request.base.sha || github.event.merge_group.base_sha }}
          CANDIDATE_SHA: ${{ github.sha }}
        run: |
          set -euo pipefail
          test "$(git rev-parse HEAD)" = "$CANDIDATE_SHA"
          test -n "$BASE_SHA"
          git merge-base --is-ancestor "$BASE_SHA" "$CANDIDATE_SHA"
          python3 scripts/ai-validate.py --base "$BASE_SHA" --mode validate \
            --receipt "$RUNNER_TEMP/validation.json"

  mutation-gate:
    needs: deterministic-checks
    runs-on: ubuntu-latest
    timeout-minutes: 40
    steps:
      - uses: actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6
        with:
          ref: ${{ github.sha }}
          persist-credentials: false
      - uses: actions/setup-java@b6effb05e454b25005698d916606bdc6ffcbf961 # v5
        with:
          distribution: temurin
          java-version: '21'
      - uses: sbt/setup-sbt@20cf087132cf939c160f0e53f87ba33634003e3e # v1
      # Configure Stryker's break threshold and inspect surviving mutants in the actual project.
      - name: Mutation testing
        run: sbt "project api" stryker
```

**Confidence confine di successione CI :** Il mondo del lavoro YAML illustra i controlli, non un meccanismo inviolabile da solo. PR può modificare gli script e il flusso di lavoro che contiene, o anche costruire comandi o report. Protegge i flussi di lavoro, gli script, le regole di prova, le politiche e i report. `CODEOWNERS` ; se disponibile, imporre un requisito di flusso di lavoro fidato da un repository/commit protetto (regole e organizzazione) e caricare il validatore da questa fonte piuttosto che dal candidato. Un cambiamento politico legittimo è tramite una PR separata e validazione umana. Solo senza richiedere il flusso di lavoro esterno, confronta questi file alla base e non consente una fusione fino a quando non è stato rivisto un cambiamento nella porta. `AGENTS.md`.

Il checkout PR può eseguire il codice arbitrario tramite autorizzazione sbt: nessun segreto privilegiato, nessun segno di scrittura, nessun segreto `pull_request_target` esecuzione del codice PR, nessuna cache condivisa con lavori privilegiati senza controllo sorgente. I rapporti di prova sono prove operative, non certificati inviolabili se il codice di prova è ostile. CI secondo la politica di progetto; la convalida deve essere ridisegnata sul candidato finale (e sull'impegno consegnato così diverso).

Questioni dottrinali:

* ** i giudici determinanti passano prima**: Compile, format e test mirati sono poco costosi rispetto a una chiamata LLM — un lavoro LLM che funziona su codice che non compila è bruciato di bilancio;
* se una recensione LLM di un'altra CI è veramente automatizzato, darlo a frequenza **La chiave di volta API Condividi su Facebook**, un timeout e un tappo di spesa specifico per il lavoro; per uso prevalentemente interattivo tramite Claude e conseguente ChatGPT, questa automazione rimane facoltativa ;
* **il lavoro LLM è la sola lettura** Egli commenta la PR, non commette mai. Un agente che corregge nella correzione CI ricrea il problema dei "due agenti di scrittura" della sezione successiva 16, peggio (senza essere umano nel loop);
* **`sbt --client` in locale, segreto JVM fresco in cambio CI** : il demone immancabile sbt è la leva dei loop locali; in funzione CI, una cache di dipendenza controllata può accelerare la risoluzione, ma non sostituisce test o isolamento. **sbt 2.0.0 è stabile dal momento che l'argomento 14 Giugno 2026** ; utilizza almeno l'uso **2.0.7** (o) **1.13.0** sulla branca dell'amore 1.x) a causa della correzione BSP/TCP del fattore 21 Agosto: definizioni di costruzione in materia Scala 3JDK: 17 minimo, nativo cliente abitua `sbtn` (a partire molto più veloce — direttamente utile per gli anelli dell'agente), cache locale/distanza compatibile Bazel e non è così `test` Questa guida segue la convenzione esercitata sbt 1.x: migrazione per arrivare sbt 2.x è un cambiamento di costruzione critico che non delega mai ad un agente — piano umano, ramo dedicato, plugin di compatibilità check (opzione60+ supportato, tra cui Play e attrezzature Scala.js in progress), poi adattamento di questi lavori.

**Autofissione Codex In un'altra CI : esplicita eccezione per la revisione del lavoro in sola lettura.** Se è davvero necessario un patch stream ospitato, separa il lavoro di generazione dalla patch (senza spingere a destra) dal lavoro di pubblicazione controllato; limita i trigger agli eventi approvati e agli attori. `pull_request_target`) Fig le azioni da parte di SHA, applicare autorizzazioni minime, timeout, budget esterno e una serratura competitiva da parte delle PR; controllare la testa SHA prima della pubblicazione, quindi riavviare i controlli richiesti. LLM. Commenti, log e patch rimangono dati inaffidabili; il fallimento non deve mai portare a un cambiamento nelle porte.

Lo stesso taglio è tradotto in GitLab supplente CI: tre fasi (in inglese)`deterministic`, `mutation`, `llm-review`), stesse porte, precedenti `rules: changes` per eseguire Stryker solo sui moduli interessati.

---

