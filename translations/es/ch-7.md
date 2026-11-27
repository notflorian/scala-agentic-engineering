<!-- section: chapter -->
# 7. Reglas específicas de Scala

<!-- section: s-1 -->
## Nunca deje que el agente haga automáticamente

* cambiar una firma pública;
* modificar las implicaciones, los givenes, las clases o las conversiones sin explicación;
* sustituir un tipo específico por `Any`, `Object`, `String` o `Map[String, Any]` ;
* tragarse un error con `recover { case _ => ... }`;
* Hacer un efecto sincrónico en un bucle;
* modificar `build.sbt`, plugins, versiones o resolvers sin validación y verificación de red previa;
* tocar las migraciones DB sin un plan de rollback;
* - Simplificar un modelo de dominio sin pruebas de oficio;
* cambiar la serialización JSON público.

<!-- section: s-2 -->
## Por pedir explícitamente

```text
Antes de modificar Scala:
- explica los tipos implicados
- indica los implicits/givens utilizados
- identifica los efectos secundarios
- comprueba las pruebas existentes
- conserva las firmas públicas
- exige una prueba para cualquier cambio en la serialización JSON
```

<!-- section: s-3 -->
## Lista de comprobación de Scala después del diff

```text
- ¿El código compila de verdad?
- ¿Son correctos los imports?
- ¿Se siguen resolviendo los implicits/givens?
- ¿Se conservan los tipos de error?
- ¿Los Futures/IO/Effects siguen siendo no bloqueantes?
- ¿Se mantiene la serialización JSON?
- ¿Las pruebas cubren el comportamiento de negocio?
- ¿El diff es mínimo?
```

<!-- section: s-4 -->
## Refactores mecánicos: scalafix antes del LLM

Para reescrituras sintáxicas repetitivas (migración de sintaxis Scala 2 → 3, sustitución sistemática de una API depreciada, reorganización de importaciones), **scalafix es determinista donde uno LLM es probabilista** : una regla se aplica de la misma manera en 500 archivos, sin alucinación ni olvido. El reparto correcto de los roles:

```text
LLM (Claude): escribir o adaptar la regla scalafix
scalafix: aplicar la transformación en toda la base de código
LLM: encargarse de los casos que la regla no pudo cubrir
```

Es la misma lógica que los guardias deterministas golpean las instrucciones textuales  la aplicación a los refactores.

Ejemplo concreto de la distribución de los roles de una regla sintáctica que el LLM escribe una vez y que scalafix aplica sobre toda la base sin deriva:

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

El pronto a dar al LLM no es el migre de las llamadas de logger, pero: *"Escribir una regla scalafix `SyntacticRule` para esta transformación, con sus pruebas, y lista los patterns que la regla no cubrirá."*. El costo se paga una vez; la aplicación es gratuita y reproducible.

<!-- section: s-5 -->
## Especificaciones Scala 3 vs Scala 2

Los modelos LLM mezclan muy a menudo las dos sintaxis o reinventan macros complejas. Exige explícitamente:

```text
- Usa la sintaxis estricta de Scala 3 (indentación opcional, enums, extensiones).
- Las macros (inline, quoted) requieren aprobación humana previa. Prefiere siempre funciones estándar.
```

<!-- section: s-6 -->
## Alucinación de dependencias: el riesgo de la salpicadura de la salpicadura

Los modelos no sólo inventan números de versión: inventan **nombres de artefactos enteros**, y de los atacantes registran estos nombres plausibles en los registros públicos para depositar en ellos cargas útiles. *slopsquatting*, se mide en 2026 aproximadamente **19,7 %** muestras de código generado que contengan al menos un nombre de paquete halucinado, con más de 200 000 nombres ficticios únicos identificados; los modelos de open-weight producen aproximadamente cuatro veces más que los propietarios de fronteras (~21,7 % contra ~5,2 % de los gastos de mantenimiento antes de dejar Qwen local ofrecer una dependencia.

Normas derivadas que se aplicarán en la reposición:

```text
- antes de añadir un artefacto a build.sbt, verifica que exista en Maven Central
  (verificación mediante la red, sin confiar en la memoria del modelo);
- para cualquier dependencia desconocida, exige la fecha de primera publicación y un editor
  con trayectoria comprobada;
- registra los lockfiles en un commit (coursier / dependencyLock) y verifica los hashes en CI;
- toda instalación iniciada por un agente fuera de la allowlist → revisión humana antes de ejecutarla;
- impide que el agente resuelva las dependencias (sbt update) con un build modificado
  si el diff aún no se ha revisado.
```

Esta es la versión de supply-chain de la regla de verificación de las versiones vía Context7 / Maven Central de la sección 3 : el nombre mismo es un dato no fiable.

---

