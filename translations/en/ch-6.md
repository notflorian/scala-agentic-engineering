<!-- section: chapter -->
# 6. Agentic TDD for sensitive business code

For an important business rule, reverse workflow:

```text
Spec → generated tests → human-approved tests → implementation → passing tests → review
```

For critical tasks, also separate the authors: Claude (or Codex]) prepares the tests from the basic commit and spec, the human validates the oracle, then the other agent implements. The writer does not weaken these assertions; if an oracle is wrong, correction explicitly arbitrated before resuming. A new independent review session inspects the limit cases of the final SHA. For micro-corrective, keep a shorter loop.

Prompt test engineer independent:

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


Prompt:

```text
Start by writing tests for this business rule.
Leave production code untouched for now.
The tests must cover:
- normal case
- edge case
- regression prevention
- existing behavior to preserve
```

You're rereading the tests.

```text
Implement the minimum code needed to pass these tests.
Keep public contracts intact.
```

This pattern is one of the most reliable to have a controlled loop agent work, provided that the local validation is doubled by a CI independent. **bugfix**, requests in addition one *bug-reproduction test* : it must fail on the original commit, reproduce the observed defect, then pass with the patch. A test added after the patch without proof that it failed before brings much less information.

For Scala, requires **Property-Based Testing** for complex logic:

```text
Start by writing tests for this business rule using ScalaCheck (property-based testing).
Go beyond conventional unit tests. Define generators (Gen) to exercise the full range of domain boundaries.
```

---

<!-- section: s-1 -->
## Example: What should the properties generated look like

The LLM must produce properties that encode **Invariants in trades**, not unit tests disguised as `forAll`. Example target for a discount service:

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

The monotony property is the typical example of what a LLM does not generate spontaneously but produces very well on explicit request: *"First list of order relations and domain identities, then encode them in properties"*. Crossed with Stryker4s (section 5, step 4), this level of testing kills the vast majority of mutants.

---

