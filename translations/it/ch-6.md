<!-- section: chapter -->
# 6. TDD agentico per il codice di dominio sensibile

Per un'importante regola d'impresa, invertire il flusso di lavoro:

```text
Spec → tests générés → tests validés humainement → implémentation → tests verts → review
```

Per i compiti critici, separare anche gli autori: Claude (o Codex]) prepara i test dal commit di base e spec, l'uomo convalida l'oracolo, poi l'altro agente implementa. Lo scrittore non indebolisce queste affermazioni; se un oracolo è sbagliato, la correzione esplicitamente arbitraria prima di riprendere. Una nuova sessione di revisione indipendente ispeziona i casi limite del SHA finale.

Prompt test engineer indipendente:

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


Prompt: anticipare

```text
À partir de cette règle métier, écris d'abord les tests.
Ne modifie pas encore le code de production.
Les tests doivent couvrir :
- cas nominal
- cas limite
- non-régression
- comportement existant à préserver
```

Stai rileggendo i test.

```text
Implémente le minimum de code pour faire passer ces tests.
Ne modifie pas les contrats publics.
```

Questo modello è uno dei più affidabili per avere un lavoro di agente di loop controllato, a condizione che la convalida locale sia raddoppiata da un determinato CI indipendente. **bugfix:**, richieste in aggiunta una percentuale *bug-reproduzione test precedenti* : deve fallire sul commit originale, riprodurre il difetto osservato, quindi passare con la patch. Un test aggiunto dopo la patch senza la prova che ha fallito prima porta molto meno informazioni.

Per Scala, richiede **Property-Based Testing** per logica complessa:

```text
À partir de cette règle métier, écris d'abord les tests en utilisant ScalaCheck (Property-based testing).
Ne te contente pas de tests unitaires classiques. Définis les générateurs (Gen) pour éprouver toutes les limites du domaine.
```

---

<!-- section: s-1 -->
## Esempio: Che cosa dovrebbero le proprietà generate guardare come casualità

Il LLM deve produrre proprietà che codificano **Invarianti negli scambi**, non test unitari mascherati come `forAll`. Esempio di destinazione per un servizio di sconto:

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

La proprietà monotonia è l'esempio tipico di ciò che un LLM] non genera spontaneamente ma produce molto bene su richiesta esplicita: *"Prima lista delle relazioni d'ordine e delle identità di dominio, poi codificarle in proprietà"*. Attraversato con Stryker4s (sezione 5, passo 4]), questo livello di test uccide la stragrande maggioranza dei mutanti.

---

