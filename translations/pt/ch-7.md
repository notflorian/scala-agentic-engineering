<!-- section: chapter -->
# 7. Regras específicas de Scala

<!-- section: s-1 -->
## Nunca deixe que o agente faça automaticamente

* mudar uma assinatura pública;
* modificar as implicações, os givenes, as classes ou as conversões sem explicação;
* substituir um tipo específico pela `Any`, `Object`, `String` ou `Map[String, Any]` ;
* engolir um erro com `recover { case _ => ... }`;
* Fazer um efeito sincrónico num ciclo;
* modificar `build.sbt`, plugins, versões ou resolver sem validação e verificação de rede prévia;
* tocar a migração DB sem um plano de rollback;
* - Simplificar um modelo de domínio sem provas de ofício;
* mudar a serialização JSON público.

<!-- section: s-2 -->
## Por pedir explicitamente.

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
## Lista de verificação de Scala após o diff

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
## Refatores mecânicos: scalafix antes do LLM

Para reescritas sintáxicas repetitivas (migração de sintaxe Scala 2 → 3, substituição sistemática de uma API depreciada, reorganização de importações), **scalafix é determinista onde um LLM é probabilista**: uma regra aplica-se da mesma maneira em 500 arquivos, sem alucinação ou esquecimento.

```text
LLM (Claude) : écrire ou adapter la règle scalafix
scalafix : appliquer la transformation sur toute la base
LLM : traiter les cas que la règle n'a pas pu couvrir
```

É a mesma lógica que os guardas deterministas batem as instruções textuais a aplicação aos refatores.

Exemplo concreto da distribuição dos papéis de uma regra sintática que o LLM escreve uma vez e que scalafix aplica sobre toda a base sem deriva:

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

O breve a dar ao LLM não é o migre das chamadas de logger, mas: *"Escrever uma regra scalafix `SyntacticRule` para esta transformação, com seus testes, e lista os patterns que a regra não cobrirá."*. O custo é pago uma vez; a aplicação é gratuita e reprodutível.

<!-- section: s-5 -->
## Especificações Scala 3 vs Scala 2

Os modelos LLM misturam muito frequentemente as duas sintaxes ou reinventam macros complexas. Exige explicitamente:

```text
- Utilise la syntaxe stricte Scala 3 (indentation optionnelle, enums, extensions).
- Interdiction stricte de créer des Macros (inline, quoted) sans validation humaine préalable. Préfère toujours des fonctions standards.
```

<!-- section: s-6 -->
## Alucinação de dependências: o risco da salpicação da salpicação

Os modelos não só inventam números de versão: inventam **Nomes de artefatos inteiros**, e dos atacantes registram esses nomes plausível nos registros públicos para depositar neles cargas úteis. *slopsquatting*, mede-se em 2026 aproximadamente **19,7 %** amostras de código geradas que contenham pelo menos um nome de pacote halucinado, com mais de 200 000 nomes fictícios únicos identificados; os modelos de open-weight produzem aproximadamente quatro vezes mais do que os proprietários de fronteiras (~)~21,7 % contra ~5,2 % das despesas de manutenção antes de deixar Qwen local oferecer uma dependência.

Regras decorrentes da aplicação da reposição:

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

Esta é a versão do supply-chain da regra de verificação das versões via Context7 / Maven Central da secção 3 : o nome é um dado não confiável.

---

