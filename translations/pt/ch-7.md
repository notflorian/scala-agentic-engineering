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
Antes de alterar código Scala:
- explique os tipos envolvidos
- indique os implicits/givens usados
- identifique os efeitos colaterais
- verifique os testes existentes
- preserve as assinaturas públicas
- altere a serialização JSON somente com cobertura de teste
```

<!-- section: s-3 -->
## Lista de verificação de Scala após o diff

```text
- O código realmente compila?
- Os imports estão corretos?
- Os implicits/givens continuam sendo resolvidos?
- Os tipos de erro foram preservados?
- Futures/IO/Effects continuam sem bloqueio?
- A serialização JSON permanece igual?
- Os testes cobrem o comportamento de negócio?
- O diff é mínimo?
```

<!-- section: s-4 -->
## Refatores mecânicos: scalafix antes do LLM

Para reescritas sintáxicas repetitivas (migração de sintaxe Scala 2 → 3, substituição sistemática de uma API depreciada, reorganização de importações), **scalafix é determinista onde um LLM é probabilista**: uma regra aplica-se da mesma maneira em 500 arquivos, sem alucinação ou esquecimento.

```text
LLM (Claude): escreva ou adapte a regra scalafix
scalafix: aplique a transformação em toda a base de código
LLM: trate os casos que a regra não conseguiu cobrir
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
- Use a sintaxe estrita do Scala 3 (indentação opcional, enums, extensões).
- Crie macros (inline, quoted) somente com aprovação humana prévia. Prefira sempre funções comuns.
```

<!-- section: s-6 -->
## Alucinação de dependências: o risco da salpicação da salpicação

Os modelos não só inventam números de versão: inventam **Nomes de artefatos inteiros**, e dos atacantes registram esses nomes plausível nos registros públicos para depositar neles cargas úteis. *slopsquatting*, mede-se em 2026 aproximadamente **19,7 %** amostras de código geradas que contenham pelo menos um nome de pacote halucinado, com mais de 200 000 nomes fictícios únicos identificados; os modelos de open-weight produzem aproximadamente quatro vezes mais do que os proprietários de fronteiras (~)~21,7 % contra ~5,2 % das despesas de manutenção antes de deixar Qwen local oferecer uma dependência.

Regras decorrentes da aplicação da reposição:

```text
- todo novo artefato em build.sbt deve existir no Maven Central ANTES de escrever a alteração
  (confirme pela rede, sem depender da memória do modelo)
- para toda dependência desconhecida, exija uma data de publicação inicial e um publicador
  com histórico estabelecido
- faça commit dos lockfiles (coursier / dependencyLock) e verifique os hashes na CI
- instalação por agente fora da lista de permissões → revisão humana antes da execução
- permita que um agente resolva dependências (sbt update) com um build modificado
  somente após a revisão do diff.
```

Esta é a versão do supply-chain da regra de verificação das versões via Context7 / Maven Central da secção 3 : o nome é um dado não confiável.

---

