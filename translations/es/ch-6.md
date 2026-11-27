<!-- section: chapter -->
# 6. TDD agéntico para código de negocio sensible

Para una regla profesional importante, revierte el flujo de trabajo:

```text
Spec → tests générés → tests validés humainement → implémentation → tests verts → review
```

Para las tareas críticas, separa también los autores: Claude (o Codex) prepara las pruebas desde el commit de base y la spec, el humano valida el oráculo y luego el otro agente implementa. El writer no debilita estas afirmaciones; si un oráculo es incorrecto, corrección explícitamente arbitrada antes de reanudar. Una nueva sesión de revisión independiente inspecciona los casos límite del SHA final. Para los microcorrectivos, mantiene un bucle más corto.

Prompt test engineer independiente:

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

Sólo estás leyendo las pruebas.

```text
Implémente le minimum de code pour faire passer ces tests.
Ne modifie pas les contrats publics.
```

Este pattern es uno de los más confiables para hacer trabajar a un agente en bucle controlado, siempre y cuando se duplique la validación local por una CI independiente. **bugfix**, pide además un *bug-reproduction test* : debe fallar en el commit de inicio, reproducir el defecto observado y luego pasar con el parche. Una prueba añadida después del parche sin prueba de que no funcionaba antes aporta mucha menos información.

Para Scala, requiere **Property-Based Testing** para la lógica compleja:

```text
À partir de cette règle métier, écris d'abord les tests en utilisant ScalaCheck (Property-based testing).
Ne te contente pas de tests unitaires classiques. Définis les générateurs (Gen) pour éprouver toutes les limites du domaine.
```

---

<!-- section: s-1 -->
## Ejemplo: ¿Cómo deben ser las propiedades generadas?

El LLM deberá producir propiedades que codifiquen ** invariantes oficios**, no pruebas unitarias disfrazadas de `forAll`. Ejemplo de objetivo para un servicio de descuento:

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

La propiedad de monotonía es el ejemplo típico de lo que LLM no genera espontáneamente pero produce muy bien a petición explícita: *"Lista primero las relaciones de orden y las identidades del dominio, luego encodéralas en propiedades"*. Cruzado con Stryker4s (sección 5, etapa 4), este nivel de prueba mata a la gran mayoría de los mutantes.

---

