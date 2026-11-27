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
Avant de modifier du Scala :
- explique les types impliqués
- indique les implicits/givens utilisés
- identifie les effets de bord
- vérifie les tests existants
- conserve les signatures publiques
- ne change pas la sérialisation JSON sans test
```

<!-- section: s-3 -->
## Lista de comprobación de Scala después del diff

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
## Refactores mecánicos: scalafix antes del LLM

Para reescrituras sintáxicas repetitivas (migración de sintaxis Scala 2 → 3, sustitución sistemática de una API depreciada, reorganización de importaciones), **scalafix es determinista donde uno LLM es probabilista** : una regla se aplica de la misma manera en 500 archivos, sin alucinación ni olvido. El reparto correcto de los roles:

```text
LLM (Claude) : écrire ou adapter la règle scalafix
scalafix : appliquer la transformation sur toute la base
LLM : traiter les cas que la règle n'a pas pu couvrir
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
- Utilise la syntaxe stricte Scala 3 (indentation optionnelle, enums, extensions).
- Interdiction stricte de créer des Macros (inline, quoted) sans validation humaine préalable. Préfère toujours des fonctions standards.
```

<!-- section: s-6 -->
## Alucinación de dependencias: el riesgo de la salpicadura de la salpicadura

Los modelos no sólo inventan números de versión: inventan **nombres de artefactos enteros**, y de los atacantes registran estos nombres plausibles en los registros públicos para depositar en ellos cargas útiles. *slopsquatting*, se mide en 2026 aproximadamente **19,7 %** muestras de código generado que contengan al menos un nombre de paquete halucinado, con más de 200 000 nombres ficticios únicos identificados; los modelos de open-weight producen aproximadamente cuatro veces más que los propietarios de fronteras (~21,7 % contra ~5,2 % de los gastos de mantenimiento antes de dejar Qwen local ofrecer una dependencia.

Normas derivadas que se aplicarán en la reposición:

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

Esta es la versión de supply-chain de la regla de verificación de las versiones vía Context7 / Maven Central de la sección 3 : el nombre mismo es un dato no fiable.

---

