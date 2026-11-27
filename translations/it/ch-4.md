<!-- section: chapter -->
# 4. Budget mensile realistico e strategia di caching

Il bilancio deve essere gestito come un bilancio di ingegneria, non come una spesa astratta. La corretta metrica non è il costo per messaggio, ma:

```text
coût total d'une tâche mergeable
= coût modèle + temps humain + temps CI + retours review + reprises de bugs
```

<!-- section: s-1 -->
## Realistic start budget

| Posti di lavoro                                                 |                 budget indicativo | Nota:                                                                                                                                                                                    |
|-------------------------------------------------------|---------------------------------:|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Claude Code via Claude Pro/Max impegnati                        |                      20 à 200+ $ | Max è giustificato se Opus/Sonnet gira ogni giorno; la quota è condivisa tra superfici Claude compatibili.                                                                        |
| ChatGPT con Codex                                    |                     20 $ e altro ancora | Più adatto per uso limitato; Pro è giustificato se Sol 6.2 diventa uno scrittore quotidiano e non solo un recensore.                                                                        |
| JetBrains AI Ultimo messaggio                                 | ~300 $/anno; 35 AI Credits / alternativa 30 j | Aiutante per le funzioni cloud JetBrains e Junie; Codice di Complezione / Prossimo Modifica Suggerimenti e agenti autenticati presso il loro fornitore non consumano questi crediti.                     |
| GitHub Copilot                                        |                         Variazione | Facoltativo: rilevante soprattutto se GitHub è il centro dei problemi di flusso di lavoro/PR/review; ampiamente ridondante come terza chat di codice.                                                      |
| OpenRouter / API punto GLM/Kimi/Gemini/Grok rilevamento      |                         0 à 50 $ | Porta di uscita eccezionale quando Claude/attrazioneCodex/Qwen non è sufficiente; volontariamente basso e incassato budget.                                                                         |
| GLM Coding Plan (Z.ai) — secondo abbonamento facoltativo  |                 ~18 a 160 $/mese esatto | Pacchetto aperto-peso *conformance per il tempo libero* : endpoint = Anthropic-compatibile, plugging in direzione Claude Code per assorbire recensione/triage senza rompere i tuoi limiti Claude. Lite ~ allenamenti ~18 $, Pro ~ alternativa ~72 $, Max ~160 $. |
| Qwen locale corrente                                            |             0 $ escluso elettricità | Molto buono per pre-analisi, sintesi e caldaia, ma non per decidere da solo su codice critico.                                                                                           |
| Sourcebot, Aider, OpenCode/Qwen Code, RTK             |                     0 a variabili | Molti strumenti sono open source, ma possibile hosting, indici e chiavi API costo.                                                                                      |
| Headroom e gli strumenti di compressione contesto recenti |                     sperimentazioni | Da testare su log/diff non critici prima di integrarlo nel flusso di lavoro standard.                                                                                                         |

Totale obiettivo realistico per uso personale intensivo: **250 à 450 $/giorno**, da regolare dopo due settimane di misurazione effettiva. 300 à 350 $ rimane plausibile, ma non dovrebbe essere congelato: un singolo anello cattivo agentec su un grande contesto può costare più di una settimana di micro-patches ben invertite.

<!-- section: s-2 -->
## Punti di prezzo e quote da non fissare nella guida aggiuntiva

Claude Code è incluso nei piani di pagamento compatibili Claude, ma l'uso esatto dipende dal piano, dal modello e dai limiti di sessione. Le pagine ufficiali indicano in particolare Claude Pro a prevedere 20 $/mese, Max da sommare 100 $/mese, e utilizza Max precedenti 5x/20x a seconda dell'offerta. Quindi mantenere la guida sotto forma di forchette, non come una verità contabile permanente.

Il mio amico Codex, evitare di cambiare i nomi dei modelli e le impostazioni precedenti ChatGPT Il routing attivo di questa guida è destinato **GPT‑6 Luna / GPT‑6.1 Terra / GPT‑6.2 Sol / GPT‑6.2 Astra**, con Sol uguale 6.2 I limiti di utilizzo, l'accesso a Max/Ultra e la fatturazione dipendono dal piano, dalla superficie, dalla regione e dall'implementazione. **classe di attività e costo per cambiamento accettato**, quindi controllare la pagina ufficiale prima di industrializzare un profilo o budget.

Importante promemoria: **Anthropic si riserva Claude Free/Pro/Max/Team/Enterprise l'utilizzo dell'abbonamento per applicazioni native Anthropic e gli usi previsti nelle sue condizioni.** Dal principio dell'educazione 2026, Anthropic vieta esplicitamente l'uso di gettoni OAuth di questi abbonamenti in imbracature di terze parti o strumenti non ufficiali: questi flussi devono passare attraverso una chiave codifica API Questo è un fornitore dedicato (Claude Console o cloud) e rispetta i termini commerciali. Claude Code e Claude.ai per gli abbonamenti Claude; OpenCode/Qwen Code/Aider per il futuro Qwen locali, modelli esterni API o tasti BYOK, senza mai riutilizzare un token di sessione Claude Pro/Max in uno strumento esterno.

Da non confondere con gli altri *è un'esperienza* permesso: plug-in temporaneo Claude Code su il buio **endpoint per la ricerca Anthropic- Z.ai compatibile** con un'immagine **Z.ai chiave alternativa** (GLM Coding Plan, § alternativa3) è lecito — si utilizza la chiave di un fornitore contro il punto finale di quello stesso fornitore, non deviare alcun token OAuth Claude. **riutilizzo di un abbonamento a Claude aken importi** fuori delle applicazioni Anthropic, non puntando Claude Code a un altro fornitore con la propria chiave.

** Post-PR Budget Claude Ship.** In solo, casual `/ship`, `/steward` e Cloud Auto-fix consumano l'utilizzo applicabile di autorizzazioni Claude Code (non c'è costo di VM separato per il cloud). Anthropic] secondo la documentazione); il monitoraggio dello sfondo non è gratuito. GitHub (Team/Enterprise) consumano crediti di utilizzo non di allocation organizzativi inclusi. `PR/mois × coût moyen de review × nombre de reviews par PR + corrections Steward + classifiers Approvals + CI supplémentaire`. Inizia con una recensione su richiesta o all'apertura, non su ogni spinta, e imposta un massimale mensile per Code Review e PR Steward (quest'ultimo non ha per impostazione predefinita). `observe` può anche attivare recensioni e classificare
Disabilitare l'utilizzo del credito non è sufficiente per fermare gli agenti attivi: Disabilitare Approvamenti, quindi Steward, e poi Codice Review se si desidera tagliare tali spese.

**Post-PR budget aggiuntivi Codex.** `@codex review` e recensioni automatiche GitHub sono soggette alle condizioni di Code Review; `/review` locale, modalità Goal, battiti cardiaci e compiti correlati Codex Cloud autenticato con il tuo account precedenti ChatGPT utilizzare il piano applicabile e le allocazioni superficiali. Nessun script di monitoraggio archiviato o chiave casuale API OpenAI Tuttavia, controllare le quote, i crediti aggiuntivi e le autorizzazioni effettive: ogni take-over e ogni correzione possono consumare quote, anche senza nuove differenze. Preferisce un obiettivo limitato o un Heartbeat con dedotto da SHA e shutdown esplicito; mai entrambi contemporaneamente sulla stessa filiale. `openai/codex-action` con la chiave API rimane un'opzione di autorizzazione CI fatturati separatamente, da riservare alle esigenze di automazione che le superfici native non coprono.

<!-- section: s-3 -->
## Caching prompt: leva maggiore, ma per formulare esattamente gli assegni

Per non far esplodere il bilancio, strutturare le richieste di agenti in modo deterministico:

1. Posizionare il contesto statico in alto: `AGENTS.md`, regole Scala, architettura, convenzioni di test.
2. Posizionare il contesto semistatico successivo: schemi, contratti JSON, accordi commerciali.
3. Posizionare il contesto dinamico in basso: file modificati, errori di compilazione, log di prova.
4. Evitare di cambiare l'intestazione del prompt in ogni iterazione se si desidera beneficiare della cache.

Una cache di successo può ridurre il costo di autorizzazione **lettura** di gettoni di entrata a circa 10 % del normale costo di ingresso da parte del fornitore (su modelli) Anthropic Correnti: 5 % per l'acquisto Opus 5.5 e non è così Sonnet 5.5, 2,5 % per l'acquisto Fable 5.2, 10 % per l'acquisto Haiku 5.5 ; 5 % per l'acquisto GPT‑6.2 Sol/Astra e dintorni GPT‑6.1 SolNon è una "Terra".90 % di risparmio sull'intero compito: token di uscita, scrittura cache, chiamate degli strumenti e errori del loop rimangono fatturati.

<!-- section: s-4 -->
## Anti-credito regole bruciate

```text
- Ne donne jamais toute la repo par défaut.
- Donne des chemins de fichiers et une hypothèse de zone concernée.
- Coupe les logs à la première erreur utile.
- Après 2 échecs identiques, stop : repasse en diagnostic humain/IDE.
- Après 3 fichiers modifiés hors plan, stop : demande un nouveau plan.
- Après 300 lignes de diff inattendues, stop : review manuelle avant suite.
- Quand le contexte n'aide plus : `HANDOFF.md` explicite + session fraîche ; `/compact` n'est qu'un dernier recours.
- Préfère rg, Sourcebot, IntelliJ, Metals ou scripts locaux aux longs dumps MCP.
```

** Risparmio su abbonamento doppio.** Stabilizza lo scrittore e il suo sforzo durante una traiettoria; i cambiamenti del modello possono interrompere la cache e aggiungere rilavoro.Un contesto fresco rimane volontario per il recensore indipendente o un'ipotesi contaminata. Non lanciare una revisione sistematica completa su ogni micro-patch o secondo passo sulla stessa PR. Deduce il follow-up da repo/PR/SHA/check/finding, preferisce un recupero eventi o un Heartbeat limitato quando il trucco CI Misura le quote consumate dal ruolo e dal compito (se esposte dal fornitore); distingue i crediti inclusi, i sovraccarichi e gli assegni API. Una quota ancora alta non è un motivo per aprire più biglietti.

