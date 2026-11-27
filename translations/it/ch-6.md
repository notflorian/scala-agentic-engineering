<!-- section: chapter -->
# 6. TDD agentico per il codice di dominio sensibile

Per un'importante regola d'impresa, invertire il flusso di lavoro:

```text
Specifica → test generati → test validati da una persona → implementazione → test passati → revisione
```

Per i compiti critici, separare anche gli autori: Claude (o Codex]) prepara i test dal commit di base e spec, l'uomo convalida l'oracolo, poi l'altro agente implementa. Lo scrittore non indebolisce queste affermazioni; se un oracolo è sbagliato, la correzione esplicitamente arbitraria prima di riprendere. Una nuova sessione di revisione indipendente ispeziona i casi limite del SHA finale.

Prompt test engineer indipendente:

```text
Agisci come ingegnere di test indipendente. Leggi la specifica approvata, AGENTS.md e i contratti esistenti.
Parti dal commit di base senza esaminare implementazioni proposte.
Progetta i test minimi per coprire criteri di accettazione, casi limite, errori e invarianti da preservare.
Associa ogni test a un requisito. Preferisci comportamenti osservabili e test basati su proprietà quando opportuno.
Per la correzione di un bug, dimostra che la riproduzione fallisce sul commit di base per il motivo previsto.
Non modificare codice di produzione, asserzioni esistenti, configurazione di build o CI.
Non ricavare i risultati attesi dall’implementazione sotto test.
Riporta requisiti scoperti, contratti ambigui, comandi esatti e risultati di esecuzione.
Fermati e attendi l’approvazione umana dell’oracolo prima di passare i test all’agente incaricato dell’implementazione.
```


Prompt: anticipare

```text
Partendo da questa regola di business, scrivi prima i test.
Attendi prima di modificare il codice di produzione.
I test devono coprire:
- caso nominale;
- caso limite;
- assenza di regressioni;
- comportamento esistente da preservare.
```

Stai rileggendo i test.

```text
Implementa il minimo codice necessario per far passare questi test.
Preserva i contratti pubblici.
```

Questo modello è uno dei più affidabili per avere un lavoro di agente di loop controllato, a condizione che la convalida locale sia raddoppiata da un determinato CI indipendente. **bugfix:**, richieste in aggiunta una percentuale *bug-reproduzione test precedenti* : deve fallire sul commit originale, riprodurre il difetto osservato, quindi passare con la patch. Un test aggiunto dopo la patch senza la prova che ha fallito prima porta molto meno informazioni.

Per Scala, richiede **Property-Based Testing** per logica complessa:

```text
Per questa regola di business, scrivi prima i test con ScalaCheck (property-based testing).
Vai oltre i test unitari tradizionali. Definisci generatori (Gen) per esplorare tutti i casi limite del dominio.
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

