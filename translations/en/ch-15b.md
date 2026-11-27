<!-- section: chapter -->
# 15B. Release engineering from mergeable PR to deployable software

Merge is not the end of the evidence. For a trade code in production, uses a validation chain proportionate to the risk; does not transform agents into production operators.

```text
spec + REQ/acceptance evidence
→ implementation gate (scope, compilation, tests)
→ review gate (independent findings, final PR head)
→ integration gate (CI on the actual merge candidate)
→ release gate (immutable artifact, staging, security)
→ production gate (authorized deployment, progressive rollout)
→ runtime verification (SLO, regressions, rollback)
```

**Release gate.** Build once the commit artifact is delivered, test this artifact, identify it by immutable digest (OIC image, JAR, distribution) and promote it without rebuilding it between staging and production. Keeps the source SHA, digest, build/dependance versions, results CI and, depending on the project, SBOM, scans and proof of provenance. The deployment identity is distinct from the writer and the CI which executes unreliable code. No production secrets in agents; temporary permissions and environment protected by human gate or release policy.

**Canary / progressive rollout.** On a critical service, deploys on a reduced perimeter ( instances, traffic, drivers or jobs) and compares to the control group. Defined before starting metrics, error and latency thresholds, observation window and minimum volume; without sufficient signal, suspends promotion. Increases gradually only if SLOs and invariants remain satisfied. For a small project or a non-critical job, staging + smoke tests and repeatable rollback may suffice. The canary is only useful if both versions are actually comparable and if the measure allows for detecting regressions.

| Implementation | Regression signals to be monitored |
|-------------|------------------------------------|
| Play / Tap | 5xx, latency p95/p99, business mistakes, success rate |
| Pekko / effects | mailboxes, timesouts, dead letters, resources and saturation |
| Spark | volumes, schematics, nulls, partitions, duplicates, errors, cost/duration of jobs |
| JVM | heap, GC, threads, CPU |
| Database | errors, locks, latency, integrity, migration |

Structured, metric and trace log instrument (OpenTelemetry if adapted). Correct service/version/digest and deployment event. Sends neither PII nor secrets in logs/LLM. Set down the shutdown criteria and the operator; if a threshold is crossed, stop the promotion, rollback via the approved pipeline or disables the functionality, then opens an incident and a correction ticket. Do not let an agent correct the production directly.

**Rollback.** Keeps the last healthy artifact, a tested procedure, deactivation flags and evidence of recovery. A destructive DB migration or irreversible writing does not cancel by redeploying a JAR: uses expand/contract, ascending/descending compatibility during rollout, proven backup/restoration and data reconciliation plan. For Spark, prefers idempout, replayable and isolated outputs before promotion. Human validates irreversible operations.

<!-- section: s-1 -->
### Definition of production side

```text
- PR and integration candidate validated.
- Immutable artifact identified, tested, and promoted by the authorized pipeline.
- Staging and smoke tests passing. Rollback / recovery tested according to risk.
- Canary or rollout approved, with no alerts or regressions exceeding thresholds.
- Observation window completed, with metrics and exceptions documented.
```

The first state is "merge-ready", the second "deployed", the last "stable". Measure these states separately rather than attribute success to a green commit or review.

---

