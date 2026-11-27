<!-- section: chapter -->
# 7. Scala-spezifische Regeln

<!-- section: s-1 -->
## Niemals zulassen, dass der Agent es automatisch tut

* eine öffentliche Signatur zu ändern ,
* Änderungen von Impliziten, Givenen, TypeKlassen oder Konvertierungen ohne Erklärung;
* einen bestimmten Typ durch `Any`, `Object`, `String` oder `Map[String, Any]` ;
* einen Fehler mit `recover { case _ => ... }` schlucken;
* eine synchrone Wirkung in einer Schleife blockieren ,
* `build.sbt`, Plugins, Versionen oder Resolven ohne vorherige Validierung und Netzwerkprüfung;
* die DB-Migration ohne Rollback-Plan zu beeinflussen;
* ein Domänenmodell ohne professionellen Test zu vereinfachen;
* Änderung der öffentlichen Serialisierung JSON.

<!-- section: s-2 -->
## ausdrücklich zu beantragen

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
## Scala-Checkliste nach dem Diff

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
## Mechanische ReFactors: scalafix vor dem LLM

Für repetitive syntaktische Neuschreibe (Syntaxmigration) Scala 2 → 3, systematische Ersetzung einer API Abwertung, Neuorganisation von Importen), **scalafix ist deterministisch, wo ein LLM ist probabilist** : Eine Regel gilt auch für 500 Dateien, ohne Halluzinationen oder Vergessen. Die richtige Rollenverteilung:

```text
LLM (Claude) : écrire ou adapter la règle scalafix
scalafix : appliquer la transformation sur toute la base
LLM : traiter les cas que la règle n'a pas pu couvrir
```

Es ist die gleiche Logik, wie die deterministischen Wächter die Textanweisungen     ✓, die auf die Refactors angewendet wird, schlagen.

Konkretes Beispiel für die Rollenteilung: Eine syntaktische Regel, die LLM einmal schreibt und [scalafix auf die gesamte Basis anwendet .

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

Die Geschwindigkeit, um LLM zu geben, ist nicht die migrieren Anrufe logger ✓, sondern: *"schreibt eine Regel scalafix `SyntacticRule` für diese Transformation, zusammen mit seinen Tests, und Liste der Patterns, die die Regel nicht abdecken wird"*. Die Kosten werden einmal bezahlt; die Anwendung ist kostenlos und reproduzierbar.

<!-- section: s-5 -->
## Besonderheiten Scala 3 vs. Scala 2

Die Vorlagen LLM vermischen sehr oft beide Syntaxen oder erfinden komplexe Makros neu.

```text
- Utilise la syntaxe stricte Scala 3 (indentation optionnelle, enums, extensions).
- Interdiction stricte de créer des Macros (inline, quoted) sans validation humaine préalable. Préfère toujours des fonctions standards.
```

<!-- section: s-6 -->
## Halluzination von Abhängigkeiten: das Risiko -- slopsquatting --

Modelle erfinden nicht nur Versionsnummern: sie erfinden **Namen von ganzen Artefakten**, und Angreifer speichern diese plausiblen Namen in öffentlichen Registern, um nützliche Ladungen zu hinterlegen. Dieser supply-chain Angriff, dokumentiert als *Slopsquatting*, gemessen in 2026 bei ca. **19,7 %** Proben von generiertem Code, die mindestens einen Namen des halluzinierten Pakets mit mehr als 200 000 Einzigartige fiktive Namen; Open-weight-Modelle produzieren etwa viermal so viele wie proprietäre Grenzen (~21,7 % dagegen ~5,2 % vor dem Verlassen des Fahrzeugs zu halten Qwen • die Möglichkeit, eine Abhängigkeit vorzuschlagen.

Abgeleitete Regeln, die auf der Ebene der Repo anzuwenden sind:

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

Dies ist die Supply-Chain-Version der Regel, die Versionen über Context7 / Maven Centrale ✓ der Fachgruppe 3 : Der Name selbst ist eine unzuverlässige Angabe.

---

