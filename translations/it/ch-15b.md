<!-- section: chapter -->
# 15B. Ingegneria del rilascio, dalla PR pronta per il merge al software distribuibile

La fusione non è la fine delle prove: per un codice commerciale in produzione, si utilizza una catena di validazione proporzionata al rischio; non trasforma gli agenti in operatori di produzione.

```text
specifica + evidenze sui requisiti e criteri di accettazione
→ controllo dell’implementazione (perimetro, compilazione, test)
→ controllo della revisione (rilievi indipendenti, SHA finale della PR)
→ controllo di integrazione (CI sul candidato effettivo al merge)
→ controllo di rilascio (artefatto immutabile, staging, sicurezza)
→ controllo di produzione (distribuzione autorizzata, rollout progressivo)
→ verifica in esercizio (SLO, regressioni, rollback)
```

**Rilasciare il gate.** Costruisci una volta che l'oggetto commit viene consegnato, testa questo artefatto, identificalo da digeritivo immutabile (immagine OIC, JAR, distribuzione) e promuoverlo senza ricostruirlo tra staging e produzione. Mantiene la sorgente SHA, digest, build/dependance versioni, risultati CI e, a seconda del progetto, SBOM, scansioni e prove di provenienza. L'identità di distribuzione è diversa dallo scrittore e dall'arbitro CI nessun segreto di produzione in agenti; autorizzazioni temporanee e ambiente protetto da cancello umano o politica di rilascio.

**Canario / progressivo rollout.** Difenso prima di iniziare metriche, errori e soglie di latenza, finestra di osservazione e volume minimo; senza sufficiente segnale, sospende la promozione. Aumenta gradualmente solo se SLO e invarianti rimangono soddisfatti. Per un piccolo progetto o un lavoro non critico, staging + test di fumo e ripetibile rollback può essere sufficiente.

| Attuazione | Segnali di regressione da monitorare |
|-------------|------------------------------------|
| Giocare / Toccare | 5xx, la latenza p sollecitare95/p99, errori di business, tasso di successo |
| Pekko / effetti negativi | mailbox, timeout, lettere morte, risorse e saturazione |
| La luce del sole | volumi, schemi, nulls, partizioni, duplicati, errori, costo/durata dei lavori |
| JVM | heap, GC, threads, CPU preventiva |
| Banca dati | errori, serrature, latenza, integrità, migrazione |

Strumento di log strutturato, metrico e tracciato (OpenTelemetry se adattato). Corretto servizio/versione/digestione e implementazione evento.LLM. Impostare i criteri di spegnimento e l'operatore; se una soglia è attraversata, interrompere la promozione, rollback tramite il pipeline approvato o disabilitare la funzionalità, quindi aprire un incidente e un biglietto di correzione.

**Rollback.** Mantiene l'ultimo artefatto sano, una procedura testata, bandiere di disattivazione e prove di recupero. Una migrazione DB distruttiva o scrittura irreversibile non annulla ridicolizzando un JAR: utilizza l'espansione/appaltimento, l'ascendente/discendente di compatibilità durante il rollout, il backup collaudato / il ripristino e il piano di riconciliazione dei dati.

<!-- section: s-1 -->
### Definizione di produzione side impegnati

```text
- PR e candidato all’integrazione validati.
- Artefatto immutabile identificato, testato e promosso dalla pipeline autorizzata.
- Staging e smoke test superati; rollback e ripristino testati secondo il rischio.
- Canary o rollout approvato; nessuna anomalia o regressione oltre le soglie.
- Finestra di osservazione conclusa; metriche ed eccezioni documentate.
```

Il primo stato è "già pronto", il secondo "deployed", l'ultimo "stabile". Misurare questi stati separatamente piuttosto che attribuire il successo a un commit verde o a una recensione.

---

