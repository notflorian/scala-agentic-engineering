<!-- section: chapter -->
# 6. TDD agêntico para código de negócio sensível

Para uma regra profissional importante, reveja o fluxo de trabalho:

```text
Especificação → testes gerados → testes validados por uma pessoa → implementação → testes passando → revisão
```

Para as tarefas críticas, separa também os autores: Claude (ou Codex) prepara os testes desde o commit de base e a spec, o humano valida o oráculo e depois o outro agente implementa. O writer não enfraquece estas afirmações; se um oráculo for errado, correção explicitamente arbitrada antes de retomar. Uma nova sessão de revisão independente inspecciona os casos-limite do SHA final. Para os microcorretivos, mantém um ciclo mais curto.

Prompt teste engineer independente:

```text
Atue como engenheiro de testes independente. Leia a especificação aprovada, o AGENTS.md e os contratos existentes.
Parta do commit-base sem examinar nenhuma implementação proposta.
Projete os menores testes que cubram os critérios de aceitação, os limites, as falhas e as invariantes preservadas.
Relacione cada teste a um requisito. Prefira comportamentos observáveis e testes baseados em propriedades quando fizer sentido.
Para uma correção, demonstre que a reprodução falha no commit-base pelo motivo esperado.
Não modifique código de produção, asserções existentes, configuração de build ou CI.
Não derive os resultados esperados a partir da implementação sob teste.
Relate requisitos sem cobertura, contratos ambíguos, comandos exatos e resultados da execução.
Pare e aguarde a aprovação humana do oráculo antes de entregar os testes ao agente de implementação.
```


Prompt:

```text
Comece escrevendo testes para esta regra de negócio.
Deixe o código de produção como está por enquanto.
Os testes precisam cobrir:
- caso normal
- caso-limite
- prevenção de regressões
- comportamento existente a preservar
```

Você só está lendo os testes.

```text
Implemente o mínimo de código necessário para os testes passarem.
Preserve os contratos públicos.
```

Este pattern é um dos mais confiáveis para fazer trabalhar um agente em ciclo controlado, desde que a validação local seja interrompida por uma CI independente. **bugfix**, pede também um *bug-reproduction teste* : deve falhar no commit de início, reproduzir o defeito observado e depois passar com o adesivo. Um teste adicionado após o adesivo sem prova de que não funcionava antes traz muito menos informações.

Para Scala, requer **Property-Based Testing** para a lógica complexa:

```text
Comece escrevendo testes para esta regra de negócio com ScalaCheck (testes baseados em propriedades).
Vá além dos testes unitários convencionais. Defina geradores (Gen) que exercitem todos os limites do domínio.
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

