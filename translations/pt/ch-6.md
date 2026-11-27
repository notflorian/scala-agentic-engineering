<!-- section: chapter -->
# 6. TDD agêntico para código de negócio sensível

Para uma regra profissional importante, reveja o fluxo de trabalho:

```text
Spec → tests générés → tests validés humainement → implémentation → tests verts → review
```

Para as tarefas críticas, separa também os autores: Claude (ou Codex) prepara os testes desde o commit de base e a spec, o humano valida o oráculo e depois o outro agente implementa. O writer não enfraquece estas afirmações; se um oráculo for errado, correção explicitamente arbitrada antes de retomar. Uma nova sessão de revisão independente inspecciona os casos-limite do SHA final. Para os microcorretivos, mantém um ciclo mais curto.

Prompt teste engineer independente:

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
À partir de cette règle métier, écris d'abord les tests.
Ne modifie pas encore le code de production.
Les tests doivent couvrir :
- cas nominal
- cas limite
- non-régression
- comportement existant à préserver
```

Você só está lendo os testes.

```text
Implémente le minimum de code pour faire passer ces tests.
Ne modifie pas les contrats publics.
```

Este pattern é um dos mais confiáveis para fazer trabalhar um agente em ciclo controlado, desde que a validação local seja interrompida por uma CI independente. **bugfix**, pede também um *bug-reproduction teste* : deve falhar no commit de início, reproduzir o defeito observado e depois passar com o adesivo. Um teste adicionado após o adesivo sem prova de que não funcionava antes traz muito menos informações.

Para Scala, requer **Property-Based Testing** para a lógica complexa:

```text
À partir de cette règle métier, écris d'abord les tests en utilisant ScalaCheck (Property-based testing).
Ne te contente pas de tests unitaires classiques. Définis les générateurs (Gen) pour éprouver toutes les limites du domaine.
```

---

<!-- section: s-1 -->
## Exemplo: Como devem ser as propriedades geradas?

O LLM deve produzir propriedades que codifiquem ** invariantes ofícios**, não provas uniárias disfarçadas de `forAll`. Exemplo de objetivo para um serviço de desconto:

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

A propriedade de monotonia é o exemplo típico do que LLM não gera espontaneamente, mas produz muito bem a pedido explícito: *"Lista primeiro as relações de ordem e as identidades do domínio, depois encodéralas em propriedades"*. Cruzado com Stryker4s (secção 5, etapa 4), este nível de teste mata a grande maioria dos mutantes.

---

