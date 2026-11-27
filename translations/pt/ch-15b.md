<!-- section: chapter -->
# 15B. Engenharia de releases, da PR pronta para integração ao software implantável

A merge não é o fim do teste. Para um código de negócio em produção, usa uma cadeia de validação proporcionada ao risco; não transforma os agentes em operadores de produção.

```text
spec + REQ/acceptance evidence
→ implementation gate (scope, compilation, tests)
→ review gate (independent findings, final PR head)
→ integration gate (CI on the actual merge candidate)
→ release gate (immutable artifact, staging, security)
→ production gate (authorized deployment, progressive rollout)
→ runtime verification (SLO, regressions, rollback)
```

**Release gate.** Construído uma vez que o artefato do commit entregue, teste este artefato, identifíquelo por digest imutável (imagem OCI, JAR, distribuição) e promeúselo sem reconstruir o staging e a produção. Conserva o SHA source, o digest, as versões de edifício/dependências, os resultados CI e, segundo o projeto, SBOM, scanners e certificados de procedência. A identidade de implantação é diferente do writer e da CI que executa código não confiável. Não há segredos de produção nos agentes; licenças temporárias e ambiente protegido por gate humano ou política de libertação.

**Canary / rolout progressivo.** Em um serviço crítico, exibe num perímetro reduzido ( instances, tráfego, sustentações ou trabalhos piloto) e compara com o grupo de controle. Define antes de começar as métricas, limiares de erro e latência, janela de observação e volume mínimo; sem sinal suficiente, suspende a promoção. Aumenta progressivamente apenas se os SLO e invariantes permanecem satisfeitos. Para um pequeno projeto ou trabalho não crítico, staging + smoke tests e rollback reprodutíveis podem bastar. O canary só é útil se ambas as versões forem efetivamente comparáveis e se a medida permite detectar retrocessos.

| Aplicação | Sinais de regressão que devem ser vigiados |
|-------------|------------------------------------|
| Play / Tapir | 5xx, latência p95/p99, erros profissionais, taxa de sucesso |
| Pekko / efeitos | mailboxes, timeouts, dead letters, recursos e saturação |
| Spark | volumes, diagramas, nulls, partições, duplicados, erros, custo/duração dos trabalhos |
| JVM | heap, GC, threads, CPU |
| Base de Dados | erros, locks, latência, integridade, migração |

Instrumento de logs estruturados, métricas e traços (OpenTelemetry se for adequado). Corrèle service/version/digest e evento de implantação. Não envie nem PII nem segredos aos logs/LLM. Define os critérios de parada e o responsável pela multa; se for ultrapassado um limiar , detenha a promoção , rollback através do tubo aprovado ou desactiva a funcionalidade , então abre um incidente e um ticket de correção . Não deixe que um agente corrija diretamente a produção .

**Rollback.[** Guarda o último artefato saudável, um procedimento testado, as flags de desactivação e os testes de recuperação. Uma migração DB destrutiva ou uma escrita irreversível não é anulada através da reafectação de um JAR: utiliza expand/contract, compatibilidade ascendente/descendiente durante o rolout, cópias de segurança/restauração testadas e plano de reconciliação para os dados. Para Spark, privilegia os tratamentos idempotents, rejugáveis e saídas isoladas antes da promoção. O humano valida as operações irreversíveis.

<!-- section: s-1 -->
### Definição de done da produção

```text
- PR et candidat d'intégration validés.
- Artefact immuable identifié, testé et promu par le pipeline autorisé.
- Staging et smoke tests passants ; rollback / récupération testés selon risque.
- Canary ou rollout approuvé ; aucune alerte ou régression au-delà des seuils.
- Fenêtre d'observation terminée ; métriques et exceptions documentées.
```

O primeiro estado é ?merge-ready ?, o segundo destacamento ?, o último estável ? ?. Medir esses estados separadamente em vez de atribuir o sucesso a um commit ou a uma revisão verde.

---

