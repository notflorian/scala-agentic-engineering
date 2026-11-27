<!-- section: chapter -->
# 15B. Ingeniería de releases, de una PR lista para integrar a software desplegable

La merge no es el final de la prueba. Para un código de negocio en producción, utiliza una cadena de validación proporcionada al riesgo; no transforma los agentes en operadores de producción.

```text
spec + REQ/acceptance evidence
→ implementation gate (scope, compilation, tests)
→ review gate (independent findings, final PR head)
→ integration gate (CI on the actual merge candidate)
→ release gate (immutable artifact, staging, security)
→ production gate (authorized deployment, progressive rollout)
→ runtime verification (SLO, regressions, rollback)
```

**Release gate.** Construido una vez que el artefacto del commit entregado, prueba este artefacto, identifíquelo por digest inmutable (imagen OCI, JAR, distribución) y promeúselo sin reconstruirlo entre staging y producción. Conserva el SHA source, el digest, las versiones de edificio/dependencias, los resultados CI y, según el proyecto, SBOM, escáneres y certificados de procedencia. La identidad de despliegue es distinta del writer y de la CI que ejecuta código no confiable. No hay secretos de producción en los agentes; permisos temporales y entorno protegido por gate humano o política de liberación.

**Canary / rollout progresivo.** En un servicio crítico, despliega en un perímetro reducido ( instances, tráfico, sostenes o trabajos piloto) y compara con el grupo de control. Define antes de comenzar las métricas, umbrales de error y latencia, ventana de observación y volumen mínimo; sin señal suficiente, suspende la promoción. Aumenta progresivamente sólo si los SLO e invariantes permanecen satisfechos. Para un pequeño proyecto o un trabajo no crítico, staging + smoke tests y rollback reproducible pueden bastar. El canary sólo es útil si ambas versiones son efectivamente comparables y si la medida permite detectar retrocesos.

| Aplicación | Señales de regresión que deben vigilarse |
|-------------|------------------------------------|
| Play / Tapir | 5xx, latencia p95/p99, errores profesionales, tasa de éxito |
| Pekko / efectos | mailboxes, timeouts, dead letters, recursos y saturación |
| Spark | volúmenes, diagramas, nulls, particiones, duplicados, errores, costo/duración de los trabajos |
| JVM | heap, GC, threads, CPU |
| Base de datos | errores, locks, latencia, integridad, migración |

Instrumento de logs estructurados, métricas y trazas (OpenTelemetry si es adecuado). Corrèle service/version/digest y evento de despliegue. No envíe ni PII ni secretos a los logs/LLM. Define los criterios de parada y el responsable de la multa; si se supera un umbral , detiene la promoción , rollback a través de la tubería aprobada o desactiva la funcionalidad , luego abre un incidente y un ticket de corrección . No deje que un agente corrija directamente la producción .

**Rollback.[** Guarda el último artefacto saludable, un procedimiento probado, las flags de desactivación y las pruebas de recuperación. Una migración DB destructiva o una escritura irreversible no se anula mediante la reasignación de un JAR: utiliza expand/contract, compatibilidad ascendente/descendiente durante el rollout, copias de seguridad/restauración probadas y plan de reconciliación para los datos. Para Spark, privilegia los tratamientos idempotents, rejugables y salidas aisladas antes de la promoción. El humano valida las operaciones irreversibles.

<!-- section: s-1 -->
### Definición de done de la producción

```text
- PR et candidat d'intégration validés.
- Artefact immuable identifié, testé et promu par le pipeline autorisé.
- Staging et smoke tests passants ; rollback / récupération testés selon risque.
- Canary ou rollout approuvé ; aucune alerte ou régression au-delà des seuils.
- Fenêtre d'observation terminée ; métriques et exceptions documentées.
```

El primer estado es ?merge-ready ?, el segundo despliegue ?, el último estable ? ?. Medir estos estados por separado en lugar de atribuir el éxito a un commit o a una revisión verde.

---

