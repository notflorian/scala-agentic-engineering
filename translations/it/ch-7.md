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
Avant de modifier du Scala :
- explique les types impliqués
- indique les implicits/givens utilisés
- identifie les effets de bord
- vérifie les tests existants
- conserve les signatures publiques
- ne change pas la sérialisation JSON sans test
```

<!-- section: s-3 -->
## Checklist Scala dopo il diff

```text
- Le code compile-t-il vraiment ?
- Les imports sont-ils corrects ?
- Les implicits/givens restent-ils résolus ?
- Les types d'erreur sont-ils préservés ?
- Les Futures/IO/Effects ne bloquent pas ?
- La sérialisation JSON est inchangée ?
- Les tests couvrent-ils le comportement métier ?
- Le diff est-il minimal ?
```

<!-- section: s-4 -->
## Refattori meccanici: scalafix prima LLM

Per riscritture di sintassi ripetitiva (syntax migrazione) Scala 2 → 3, sostituzione sistematica della sostituzione API depreciated, riorganizzazione delle importazioni), **scalafix è deterministico dove un'operazione LLM è probabilità di aumento** : una regola si applica identicamente su richiesta 500 file, senza allucinazione o dimenticanza. Buona condivisione di ruolo:

```text
LLM (Claude) : écrire ou adapter la règle scalafix
scalafix : appliquer la transformation sur toute la base
LLM : traiter les cas que la règle n'a pas pu couvrir
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
- Utilise la syntaxe stricte Scala 3 (indentation optionnelle, enums, extensions).
- Interdiction stricte de créer des Macros (inline, quoted) sans validation humaine préalable. Préfère toujours des fonctions standards.
```

<!-- section: s-6 -->
## Allucinazione della dipendenza: il rischio di slopsquatting compensare

I modelli non solo inventano i numeri di versione: inventiscono **nomi di artefatti interi**, e gli aggressori registrano questi nomi plausibili nei registri pubblici per depositare i carichi di pagamento. *slopsquatting anticipazione*, si misura in quantità 2026 a proposito di **19,7 %** campionati di codice generati contenenti almeno un nome del pacchetto allucinato, con più di 200 000 nomi fittizi unici identificati; i modelli open-weight producono circa quattro volte tanto quanto i confini proprietari (~ arrivare ~21,7 % contro ~ l'aumento ~5,2 % — tenere a mente prima di lasciare Qwen locale proponga una dipendenza.

Regole derivative da applicare al livello del repo:

```text
- tout nouvel artefact dans build.sbt doit exister sur Maven Central AVANT l'écriture
  (vérification réseau, pas mémoire du modèle) ;
- pour toute dépendance inconnue : exiger une date de première publication et un éditeur
  avec un historique établi ;
- commiter les lockfiles (coursier / dependencyLock) et vérifier les hashes en CI ;
- toute installation initiée par un agent hors allowlist → revue humaine avant exécution ;
- ne jamais laisser un agent résoudre les dépendances (sbt update) avec un build modifié
  sans diff relu.
```

Questa è la versione della regola "check version via Context7 / Maven Central" della sezione 3: il nome stesso è un dato inaffidabile.

---

