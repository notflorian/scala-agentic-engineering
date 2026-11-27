<!-- section: chapter -->
# 6. Agentenbasierte testgetriebene Entwicklung (TDD) für sensiblen Fachcode

Für eine wichtige Gewerberegel umgekehrt Workflow:

```text
Spec → tests générés → tests validés humainement → implémentation → tests verts → review
```

Für kritische Aufgaben trennt auch die Autoren: Claude (oder Codex) bereitet die Tests vom Basis-Commit und Spec vor, der Mensch validiert das Oracle und dann der andere implementierte Agent. Der Writer schwächt diese Behauptungen nicht; wenn ein Oracle falsch ist, Korrektur ausdrücklich abgelenkt, bevor er wieder aufgenommen wird. Eine neue unabhängige Review-Sitzung inspiziert die Grenzfälle des endgültigen SHA. Für Mikrokorrektive behält eine kürzere Schleife.

Prompt test engineer unabhängig:

```text
Act as an independent test engineer. Read the approved specification, AGENTS.md and existing contracts.
Work from the base commit without inspecting any proposed implementation.
Design the smallest tests covering acceptance criteria, boundaries, failures and preserved invariants.
Map each test to a requirement; prefer observable behavior and property-based tests where meaningful.
For a bugfix, demonstrate the reproduction fails on the base commit for the expected reason.
Do not modify production code, existing assertions, build configuration or CI.
Do not derive expected results from the implementation under test.
Report uncovered requirements, ambiguous contracts, exact commands and execution results.
Stop for human approval of the oracle before handing the tests to the implementation agent.
```


Prognose:

```text
À partir de cette règle métier, écris d'abord les tests.
Ne modifie pas encore le code de production.
Les tests doivent couvrir :
- cas nominal
- cas limite
- non-régression
- comportement existant à préserver
```

Du liest die Tests, dann nur:

```text
Implémente le minimum de code pour faire passer ces tests.
Ne modifie pas les contrats publics.
```

Dieses Pattern ist einer der zuverlässigsten, um einen Agenten in einer kontrollierten Schleife arbeiten zu lassen, sofern die lokale Validierung durch eine CI unabhängig. **bugfix**, bittet zusätzlich um eine *Bug-Reproduktion Test* : es muss auf dem Start-Commit fehlschlagen, reproduzieren Sie den beobachteten Fehler und gehen Sie dann mit dem Patch. Ein nach dem Patch hinzugefügter Test ohne Nachweis, dass es vor fehlte, bringt viel weniger Informationen.

Für Scala erfordert [**Property-Based Testing** für komplexe Logik:

```text
À partir de cette règle métier, écris d'abord les tests en utilisant ScalaCheck (Property-based testing).
Ne te contente pas de tests unitaires classiques. Définis les générateurs (Gen) pour éprouver toutes les limites du domaine.
```

---

<!-- section: s-1 -->
## Beispiel: Wie sollten die erzeugten Eigenschaften aussehen?

Das LLM muss Eigenschaften erzeugen, die professionelle [**] Invarianten** kodieren, keine Einzeltests, die als `forAll` verkleidet sind. Zielbeispiel für einen Übergabedienst:

```scala
import org.scalacheck.*
import org.scalacheck.Prop.forAll

object DiscountServiceProps extends Properties("DiscountService"):

  // Générateurs qui éprouvent les limites du domaine : zéro, bornes, valeurs extrêmes.
  // C'est ici que le LLM apporte de la valeur — à condition de lui demander
  // les invariants en langage naturel AVANT le code.
  val amounts: Gen[BigDecimal] =
    Gen.frequency(
      8 -> Gen.chooseNum(1L, 100_000_00L).map(c => BigDecimal(c) / 100),
      1 -> Gen.const(BigDecimal(0)),
      1 -> Gen.const(BigDecimal("9999999999.99")) // borne haute du domaine
    )

  val rates: Gen[Int] =
    Gen.frequency(8 -> Gen.choose(1, 99), 1 -> Gen.const(0), 1 -> Gen.const(100))

  property("le montant remisé n'est jamais négatif") =
    forAll(amounts, rates) { (amount, rate) =>
      DiscountService.applyDiscount(amount, rate) >= BigDecimal(0)
    }

  property("la remise ne dépasse jamais le montant initial") =
    forAll(amounts, rates) { (amount, rate) =>
      DiscountService.applyDiscount(amount, rate) <= amount
    }

  property("0% est l'identité") =
    forAll(amounts) { amount =>
      DiscountService.applyDiscount(amount, 0) == amount
    }

  property("monotone : plus de remise → montant final plus petit ou égal") =
    forAll(amounts, rates, rates) { (amount, r1, r2) =>
      val (lo, hi) = if r1 <= r2 then (r1, r2) else (r2, r1)
      DiscountService.applyDiscount(amount, hi) <= DiscountService.applyDiscount(amount, lo)
    }
```

Die Monotonie-Eigenschaft ist das typische Beispiel dessen, was eine LLM nicht spontan erzeugt, sondern auf ausdrückliche Anfrage sehr gut produziert: [*"listet zuerst die Ordnungsbeziehungen und die Identitäten der Domain auf und encodet sie dann in Eigenschaften"*. Kreuzt mit Stryker4s (Abschnitt 5, Schritt 4), tötet diese Teststufe die überwiegende Mehrheit der Mutanten.

---

