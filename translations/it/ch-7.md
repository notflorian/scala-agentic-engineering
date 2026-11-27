<!-- section: chapter -->
# 7. Regole specifiche di Scala

<!-- section: s-1 -->
## Non lasciare che l'agente lo faccia automaticamente

* cambiare una firma pubblica;
* modificare implics, Givens, typeclasses o conversioni senza spiegazione;
* sostituire un tipo specifico con `Any`, `Object`, `String` o `Map[String, Any]`;
* ingoiare un errore con `recover { case _ => ... }`;
* rendere un effetto sincrono bloccando in un loop;
* modificare `build.sbt`, plugin, versioni o risolutori senza previa convalida e verifica della rete;
* touch DB migrazioni senza rollback plan;
* Semplifica un modello di dominio senza un test commerciale;
* cambiare la serializzazione pubblica JSON.

<!-- section: s-2 -->
## Per essere esplicitamente richiesto

```text
Prima di modificare codice Scala:
- spiega i tipi coinvolti;
- individua gli implicits/givens in uso;
- individua gli effetti collaterali;
- verifica i test esistenti;
- preserva le firme pubbliche;
- evita modifiche alla serializzazione JSON senza un test.
```

<!-- section: s-3 -->
## Checklist Scala dopo il diff

```text
- Il codice compila davvero?
- Gli import sono corretti?
- Gli implicits/givens si risolvono ancora?
- I tipi di errore sono preservati?
- Futures/IO/Effects sono non bloccanti?
- La serializzazione JSON è invariata?
- I test coprono il comportamento di business?
- Il diff è minimo?
```

<!-- section: s-4 -->
## Refattori meccanici: scalafix prima LLM

Per riscritture di sintassi ripetitiva (syntax migrazione) Scala 2 → 3, sostituzione sistematica della sostituzione API depreciated, riorganizzazione delle importazioni), **scalafix è deterministico dove un'operazione LLM è probabilità di aumento** : una regola si applica identicamente su richiesta 500 file, senza allucinazione o dimenticanza. Buona condivisione di ruolo:

```text
LLM (Claude): scrivi o adatta la regola scalafix
scalafix: applica la trasformazione all’intero codice
LLM: gestisci i casi che la regola non copre
```

E' la stessa logica che "le salvaguardie deterministe battono le istruzioni testuali", applicate ai refactors.

Un esempio concreto di condivisione del ruolo — una regola sintattica che LLM scrive una volta e che scalafix si applica su tutta la base senza deriva:

```scala
package fix

import scalafix.v1.*
import scala.meta.*

// Règle générée par Claude, relue par un humain, appliquée par scalafix.
// Migration : `logger.warn(msg, exception)` (API dépréciée)
//          →  `logger.warn(exception)(msg)` (nouvelle API curryfiée)
class MigrateLoggerWarn extends SyntacticRule("MigrateLoggerWarn"):

  override def fix(implicit doc: SyntacticDocument): Patch =
    doc.tree.collect {
      case t @ Term.Apply(Term.Select(qual, Term.Name("warn")), List(msg, ex))
          if qual.syntax.toLowerCase.contains("logger") =>
        Patch.replaceTree(t, s"${qual.syntax}.warn(${ex.syntax})(${msg.syntax})")
    }.asPatch
```

```bash
# Application déterministe sur 500 fichiers, en secondes :
sbt "scalafixAll MigrateLoggerWarn"
# Puis : le LLM ne traite QUE les cas que scalafix a laissés (rapport de la règle)
```

La prontezza di dare vuoto LLM non è "migrare le chiamate dei logger" ma: *"scrivete una regola alternativa scalafix `SyntacticRule` per questa trasformazione, con i suoi test, e elencare i modelli che la regola non coprirà"*. Il costo viene pagato una volta; l'applicazione è gratuita e riproducibile.

<!-- section: s-5 -->
## Specifiche tecniche Scala 3 - Non lo so. Scala 2

Modelli su misura LLM molto spesso mescolare le due sintassi o reinventare macro complesse.

```text
- Usa la sintassi rigorosa di Scala 3 (indentazione opzionale, enum, estensioni).
- Non creare macro (inline, quoted) senza previa approvazione umana. Preferisci sempre le funzioni standard.
```

<!-- section: s-6 -->
## Allucinazione della dipendenza: il rischio di slopsquatting compensare

I modelli non solo inventano i numeri di versione: inventiscono **nomi di artefatti interi**, e gli aggressori registrano questi nomi plausibili nei registri pubblici per depositare i carichi di pagamento. *slopsquatting anticipazione*, si misura in quantità 2026 a proposito di **19,7 %** campionati di codice generati contenenti almeno un nome del pacchetto allucinato, con più di 200 000 nomi fittizi unici identificati; i modelli open-weight producono circa quattro volte tanto quanto i confini proprietari (~ arrivare ~21,7 % contro ~ l'aumento ~5,2 % — tenere a mente prima di lasciare Qwen locale proponga una dipendenza.

Regole derivative da applicare al livello del repo:

```text
- prima di scrivere in build.sbt, verifica che ogni nuovo artefatto esista su Maven Central
  (verifica in rete, senza affidarti alla memoria del modello);
- per ogni dipendenza sconosciuta, esigi una data di prima pubblicazione e un autore
  con una reputazione documentata;
- includi i lockfile nei commit (coursier / dependencyLock) e verifica gli hash in CI;
- installazione avviata da un agente fuori dall’allowlist → revisione umana prima dell’esecuzione;
- non lasciare che un agente risolva le dipendenze (sbt update) con un build modificato
  prima di aver rivisto il diff.
```

Questa è la versione della regola "check version via Context7 / Maven Central" della sezione 3: il nome stesso è un dato inaffidabile.

---

