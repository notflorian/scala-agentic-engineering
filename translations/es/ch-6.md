<!-- section: chapter -->
# 6. TDD agéntico para código de negocio sensible

Para una regla profesional importante, revierte el flujo de trabajo:

```text
Especificación → pruebas generadas → pruebas validadas por una persona → implementación → pruebas en verde → revisión
```

Para las tareas críticas, separa también los autores: Claude (o Codex) prepara las pruebas desde el commit de base y la spec, el humano valida el oráculo y luego el otro agente implementa. El writer no debilita estas afirmaciones; si un oráculo es incorrecto, corrección explícitamente arbitrada antes de reanudar. Una nueva sesión de revisión independiente inspecciona los casos límite del SHA final. Para los microcorrectivos, mantiene un bucle más corto.

Prompt test engineer independiente:

```text
Actúa como ingeniero de pruebas independiente. Lee la especificación aprobada, AGENTS.md y los contratos existentes.
Trabaja desde el commit base sin examinar ninguna implementación propuesta.
Diseña las pruebas más pequeñas que cubran los criterios de aceptación, los límites, los fallos y los invariantes que deben mantenerse.
Vincula cada prueba con un requisito. Prioriza el comportamiento observable y las pruebas basadas en propiedades cuando tenga sentido.
Para una corrección de errores, demuestra que la reproducción falla en el commit base por el motivo esperado.
No modifiques el código de producción, las aserciones existentes, la configuración de compilación ni la CI.
No deduzcas los resultados esperados de la implementación que estás probando.
Informa de los requisitos sin cobertura, los contratos ambiguos, los comandos exactos y los resultados de ejecución.
Detente hasta que una persona apruebe el oráculo antes de entregar las pruebas al agente de implementación.
```


Prompt:

```text
A partir de esta regla de negocio, escribe primero las pruebas.
De momento, deja intacto el código de producción.
Las pruebas deben cubrir:
- caso nominal
- caso límite
- ausencia de regresiones
- comportamiento existente que debe mantenerse
```

Sólo estás leyendo las pruebas.

```text
Implementa el código mínimo necesario para que pasen estas pruebas.
Conserva los contratos públicos.
```

Este pattern es uno de los más confiables para hacer trabajar a un agente en bucle controlado, siempre y cuando se duplique la validación local por una CI independiente. **bugfix**, pide además un *bug-reproduction test* : debe fallar en el commit de inicio, reproducir el defecto observado y luego pasar con el parche. Una prueba añadida después del parche sin prueba de que no funcionaba antes aporta mucha menos información.

Para Scala, requiere **Property-Based Testing** para la lógica compleja:

```text
A partir de esta regla de negocio, escribe primero las pruebas con ScalaCheck (pruebas basadas en propiedades).
Ve más allá de las pruebas unitarias tradicionales. Define los generadores (Gen) para probar todos los límites del dominio.
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

