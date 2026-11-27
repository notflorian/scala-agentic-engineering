<!-- section: chapter -->
# 6. Agentenbasierte testgetriebene Entwicklung (TDD) für sensiblen Fachcode

Für eine wichtige Gewerberegel umgekehrt Workflow:

```text
Spezifikation → generierte Tests → menschlich validierte Tests → Implementierung → erfolgreiche Tests → Review
```

Für kritische Aufgaben trennt auch die Autoren: Claude (oder Codex) bereitet die Tests vom Basis-Commit und Spec vor, der Mensch validiert das Oracle und dann der andere implementierte Agent. Der Writer schwächt diese Behauptungen nicht; wenn ein Oracle falsch ist, Korrektur ausdrücklich abgelenkt, bevor er wieder aufgenommen wird. Eine neue unabhängige Review-Sitzung inspiziert die Grenzfälle des endgültigen SHA. Für Mikrokorrektive behält eine kürzere Schleife.

Prompt test engineer unabhängig:

```text
Arbeite als unabhängiger Test Engineer. Lies die genehmigte Spezifikation, AGENTS.md und die geltenden Verträge.
Gehe vom Basis-Commit aus, ohne den vorgeschlagenen Implementierungsstand anzusehen.
Entwirf möglichst kleine Tests für die Akzeptanzkriterien, Grenzfälle, Fehlerfälle und zu erhaltenden Invarianten.
Ordne jeden Test einer Anforderung zu. Bevorzuge beobachtbares Verhalten und, wo sinnvoll, Eigenschaftstests.
Zeige bei einem Bugfix, dass die Reproduktion auf dem Basis-Commit aus dem erwarteten Grund fehlschlägt.
Ändere weder Produktionscode noch bestehende Assertions, Build-Konfiguration oder CI.
Leite keine erwarteten Ergebnisse aus der zu testenden Implementierung ab.
Melde nicht abgedeckte Anforderungen, mehrdeutige Verträge, die genauen Befehle und ihre Ergebnisse.
Warte auf die menschliche Freigabe des Testorakels, bevor du die Tests an den implementierenden Agenten übergibst.
```


Prognose:

```text
Schreibe ausgehend von dieser fachlichen Regel zuerst die Tests.
Ändere den Produktionscode noch nicht.
Die Tests müssen Folgendes abdecken:
- Normalfall
- Grenzfall
- Regressionen
- zu erhaltendes Verhalten
```

Du liest die Tests, dann nur:

```text
Implementiere gerade genug Code, damit diese Tests bestehen.
Ändere die öffentlichen Verträge nicht.
```

Dieses Pattern ist einer der zuverlässigsten, um einen Agenten in einer kontrollierten Schleife arbeiten zu lassen, sofern die lokale Validierung durch eine CI unabhängig. **bugfix**, bittet zusätzlich um eine *Bug-Reproduktion Test* : es muss auf dem Start-Commit fehlschlagen, reproduzieren Sie den beobachteten Fehler und gehen Sie dann mit dem Patch. Ein nach dem Patch hinzugefügter Test ohne Nachweis, dass es vor fehlte, bringt viel weniger Informationen.

Für Scala erfordert [**Property-Based Testing** für komplexe Logik:

```text
Schreibe ausgehend von dieser fachlichen Regel zuerst Tests mit ScalaCheck (eigenschaftsbasiertes Testen).
Beschränke dich nicht auf klassische Unit-Tests. Definiere Generatoren (Gen), die sämtliche Grenzen des Wertebereichs prüfen.
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

