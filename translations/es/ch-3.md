<!-- section: chapter -->
# 3. Selección y asignación de modelos

<!-- section: s-1 -->
## Regla simple

```text
Qwen / Haiku préparent et filtrent.
Micro-dev sous fort contrôle humain → GPT‑6 Luna High ou Sonnet 5.5 Medium.
Agentic coding end-to-end → GPT‑6.2 Sol Medium ou Opus 5.5 Medium.
Debugging / architecture difficiles → Opus 5.5 High ou GPT‑6.2 Sol High.
Frontier ponctuel → GPT‑6.2 Astra Light ou Fable 5.2 Low avant de pousser aveuglément l'effort du modèle inférieur au maximum.
Un seul writer par worktree.
L'autre famille de modèles reviewe ou challenge, elle ne duplique pas automatiquement toute la trajectoire.
Ultra / multi-agent uniquement lorsque les sous-problèmes sont réellement indépendants.
IntelliJ valide.
Toi, tu décides.
```

El enrutamiento debe minimizar el **costo de la tarea terminada**, no el precio de la primera apelación:

```text
charge totale attendue
= découverte + implémentation + vérification
+ probabilité de reprise × coût de reprise
+ coût de coordination
```

Por lo tanto, un modelo más caro puede ser la mejor compra si evita una exploración incorrecta, varios diffs innecesarios y los rizos de CI. Por el contrario, un micro-bucle controlado por un senior hace que Luna, Sonnet o Haiku dominantes tan pronto como el error se detecta en cuestión de minutos.

*Nunca delegar la actualización de las versiones en `build.sbt` Sin exigir que el agente interrogue primero a un MCP, Context7, Maven Central o la documentación oficial. Los nombres y versiones de las bibliotecas son exactamente el tipo de información que los modelos alucinan cuando trabajan fuera de contexto.*

<!-- section: s-2 -->
## Matriz de enrutamiento

| Tarea                                                    | Modo         | Agente principal recomendado                   | Segundo paso útil                           | ¿Por qué?                                                                           |
|----------------------------------------------------------|--------------|----------------------------------------------|------------------------------------------------|------------------------------------------------------------------------------------|
| Resuelve un módulo, grep, usos, logs simples            | Micro-dev    | **Haiku 5.5** o Qwen local                  | Ninguna salvo ambigüedad                           | Lectura de alta frecuencia, bajo riesgo                                             |
| Modificación mecánica precisa, boilerplata, renombrado   | Micro-dev    | **GPT‑6 Luna High[**                          | Sonnet 5.5 Medium si los tipos sutiles             | Muy buen costo cuando el humano mantiene la dirección                                    |
| Escribir una prueba simple de un comportamiento conocido   | Micro-dev    | **GPT‑6 Luna High[**                          | Sonnet 5.5 Medium si regla profesional rica        | Salida fácilmente verificable                                                       |
| Stack rastro o fisuras precisas                           | Micro-dev    | **Sonnet 5.5 Medium[**                        | Luna High para aplicar un parche borné        | Sonnet trae más comprensión sin pagar Opus                               |
| Pequeño error reproducido, perímetro conocido                     | Micro-dev    | **Sonnet 5.5 Medium[**                        | Luna High para pruebas/editar mecánica         | Pendientes cortos, feedback inmediato                                                 |
| Patch local, tipos o invariantes no triviales            | Micro-dev    | **GPT‑6.1 Terra Medium[**                     | GPT‑6.2 Sol Medium si es necesario explorar  | Tercer intermedio que se medirá en los parches bornados |
| Pequeño refactor local                                     | Micro-dev    | **Sonnet 5.5 Medium[**                        | Luna High para inspección mecánica          | El mayor conserva la arquitectura                                                  |
| Revisión dirigida de un pequeño diff                            | Verificación | **GPT‑6.2 Sol Light**                        | Sonnet 5.5 Medium si la segunda opinión útil         | Más juicio que un worker, sin pagar una revisión de agente completa            |
| Issue estándar completo, spec claro                     | Agente      | **GPT‑6.2 Sol Medium[**                       | **Opus 5.5 Medium** en review                  | Mejor defecto Codex para exploración → parche → pruebas → PR                        |
| Fátura multiarchivo normal                           | Agente      | **GPT‑6.2 Sol Medium[**                       | Opus 5.5 Medium en review                      | Ownership end-to-end con costo contenido                                             |
| Factura compleja, varias capas                      | Agente      | **GPT‑6.2 Sol High[**                         | Opus 5.5 Medium/High                           | Mayor planificación y verificación                                         |
| Arquitectura o elección de migración                       | Agente      | **Opus 5.5 High[**                            | Sol Medium para desafiar el plan             | El juicio domina la producción de código                                           |
| Causa desconocida / error Scala sutil                   | Agente      | **Opus 5.5 High[**                            | Sul Medium/High para hipótesis independientes    | Entender el problema cuesta más que el parche                                     |
| Competencia, async, flaky test difícil                 | Agente      | **Opus 5.5 High[**                            | Sol High si la primera pista falla           | Reduce el riesgo de anclar una causa falsa                                    |
| Migración / compatibilidad pública                       | Agente      | **GPT‑6.2 Sol High[**                         | Opus 5.5 High en revisión conceptual           | Ejecución disciplinada + segunda sentencia independiente                                |
| Mayor refactor transversal                                | Agente      | **Opus 5.5 High[**                            | Sol Medium/High en review                      | Opus para la coherencia global; Sol para romper los ángulos muertos                     |
| Revisión normal de un PR escrito por Codex                 | Verificación | **Opus 5.5 Medium[**                          | Ninguna excepto finding critique                    | Contexto fresco y otras familias de modelos                                         |
| Revisión normal de una PR escrita por Claude                | Verificación | **GPT‑6.2 Sol Medium[**                       | Ninguna excepto finding critique                    | Simetría autor/reviewer                                                           |
| Review arquitectura, invariantes, casos límite             | Verificación | **Opus 5.5 High[**                            | Astra Light tan alto en juego    | Buscar errores conceptuales en lugar de leer el diff             |
| Seguridad, auth, contrato crítico                         | Crítica     | **GPT‑6.2 Astra Light**                        | Opus 5.5 High como reviewer                   | Comprar capacidad superior sin salir directamente en un esfuerzo extremo           |
| Problema muy ambiguo, juicio end-to-end                | Frontier     | **GPT‑6.2 Astra Light**                        | Opus 5.5 High para criticar el plan           | La capacidad de juicio cuenta más que la longitud del diff                   |
| Decisión muy difícil en medio de una tarea normal    | Advisor      | **Fable 5.2 Low[**                            | Sol/Opus sigue siendo el ejecutante                     | Comprar puntualmente el juicio fronterizo sin transferir toda la tarea         |
| Sol High falla por límite de capacidad                   | Escalada     | **GPT‑6.2 Astra Light**                        | Medium/High sólo si es necesario            | Cambiar de tier puede costar menos que un Sol Extra High prolongado                    |
| Opus High falla por límite de capacidad                  | Escalada     | **Fable 5.2 Low[**                            | Sol/Astra para challenger                      | La misma lógica: Limitar poco esfuerzo antes de esfuerzo máximo inferior               |
| Fallo CI simple después de la implementación correcta            | Reanudación      | **GPT‑6 Luna High** o **Sonnet 5.5 Medium** | Escalada sólo si problema conceptual      | No pagar Sol/Opus por una corrección local y verificable                     |
| Seguimiento post-PR autónomo (CI, review, mergeabilidad)         | Reanudación      | **GPT‑6.2 Sol Medium[**                      | High si root causa difícil; Sol 6.1 en fallback | Goal mode, Heartbeats o Cloud; bucle secuencial borneado, no Ultra           |
| Segundo fracaso que revela una mala concepción          | Reanudación      | **GPT‑6.2 Sol High** o **Opus 5.5 High**    | Usar la otra familia para romper el ancla | El problema ya no es mecánico: hay que recalificar la hipótesis                 |
| Fallos repetidos a pesar de Sol High / Opus High               | Escalada     | **GPT‑6.2 Astra Light** o **Fable 5.2 Low**   | La otra frontera en la que se encuentra la frontera                 | La capacidad se convierte en el factor limitante; volver a salir con un contexto propio         |
| Sesión autónoma > 30 min, dependencias secuenciales     | Largo horizonte | **Opus 5.5 Extra (`xhigh`)**                 | Sol High al final                              | Extra está justificado por la longitud, no por la importancia simbólica                |
| Trabajo extremadamente difícil durante varias horas    | Frontier     | **Fable 5.2 High[**                           | Astra Light/Medium en review indépendant      | Reservar el alto costo de la frontera a las trayectorias en las que se evita la repetición de grandes |
| Exploration codebase-scale descomposable                  | Multiagente  | **GPT‑6.2 Sol Ultra**                        | Opus Medium para síntesis/review               | Ultra se aplica sobre todo a los ejes read-heavy independientes                           |
| Pruebas, exploración y clasificación en gran escala conexa | Multiagente  | **GPT‑6.2 Sol Ultra**                        | Claude sólo sobre las anomalías importantes | El paralelismo paga cuando las subtareas son independientes y verificables       |
| Varios writers en los mismos archivos                 | —            | **Para evitar**                                 | Secacionalización                                 | El costo de coordinación suele ser superior al beneficio                               |

> **Nota Qwen3-Coder-Next locales** : el modelo oficial es un MoE de **80B parámetros en total, 3B activados**, avec 48
> capas híbridas, un contexto nativo de **262 144 tokens** y un funcionamiento exclusivamente **no-thinking**.
> Número
> reducido de parámetros activos mejora el coste de cálculo, pero los **80B de peso deben residir en
> memoria
> ** : « 3Por tanto, B activos de 3B.
>
> Los tamaños oficiales de la GGUF son: **Q4_K_M 48,4 Go**, **Q5_K_M 56,7 Go**, **Q6_K 65,5 Go** y **Q8_0 84,8 Go**. La
> tamaño del archivo no es sin embargo el consumo total: añade la caché de contexto, los buffers del backend, el
> servidor, macOS, IntelliJ, sbt y los JVM del proyecto. **128 Go**, las cuatro variantes pueden teóricamente ser
> Los costes de funcionamiento de las empresas de servicios de transporte de mercancías por carretera y de los servicios de transporte de mercancías por carretera no son iguales en el caso de las empresas de transporte por carretera.
>
> ```text
> Q4_K_M  → défaut « marge maximale » : IDE, sbt et plusieurs JVM restent confortables.
> Q5_K_M  → défaut recommandé : meilleur compromis qualité / mémoire sur cette machine.
> Q6_K    → option haute qualité : viable si les autres applications restent raisonnables.
> Q8_0    → option d'évaluation : possible, mais marge réduite et bénéfice à prouver face à Q5/Q6.
> ```
>
> Documentación oficial Qwen utiliza correctamente **Q5_K_M** en su ejemplo `llama.cpp`, avec `-c 40960`y no el
> contexto máximo de 256K. Para el trabajo diario de agente, **32K à 64K**, a continuación, aumenta sólo si una
> El contexto declarado por el modelo es una capacidad máxima, no una configuración
> económica
> por defecto.
>
> **Recomendación para tu M5 Max 128 Go** : conserva **Q4_K_M y Q5_K_M** en el SSD. Use Q5_K_M como perfil
> diario de análisis previo, resumen de módulos y generación de pruebas simples; cambia a Q4_K_M cuando IntelliJ,
> varios módulos sbt, Spark o JVM Consumen ya mucha memoria. No conserva Q6_K o Q8_0 que si
> uno
> bake-off Scala muestra un aumento de calidad mensurable. Con 8 To de SSD, el almacenamiento no es la restricción; la
> presión
> memoria, latencia y calidad por tarea lo son.
>
> **Backend Apple Silicon** : prueba **MLX-LM y llama.cpp** En lugar de congelar inmediatamente un solo motor.
> Conversiones MLX 4-bit y 8-bit existen, y un informe reproducible sobre Qwen3-Coder-Next observó un decodificación
> Mucho más rápido en MLX que en una versión dada de llama.cpp en Apple Silicon. Este resultado depende de
> versiones y no constituye una garantía para el M5 Max; justifica un benchmark local con versiones congeladas.
> `llama.cpp` Sin embargo, sigue siendo la vía mejor documentada por Qwen y expone fácilmente un servidor OpenAI- Compatible.
>
> **Metal y memoria por cable** : no presenta 75 % de la cantidad total de material. `llama.cpp` cartel
> Inicio `recommendedMaxWorkingSetSize`, que es el valor que debe observarse en la versión de macOS y el Mac afectados.
> configuración no documentada `iogpu.wired_limit_mb` existe y es utilizada por la comunidad, pero no debe convertirse en un
> prerequisitos estándar: prueba primero la plantilla sin cambios en el sistema. Q8_0 puede funcionar en una máquina 128 Vamos,
> pero un contexto largo o varias ranuras pueden acercar el proceso a este límite antes de que la RAM física
> o bien
> Está totalmente ocupada.
>
> **Protocolo de medición mínimo** : compara Q4_K_M, Q5_K_M y posiblemente Q6_K sobre las mismas diez tareas Scala, avec
> el mismo contexto y el mismo arness. Medición por separado del prompt processing, el caudal de generación, el tiempo hasta el
> primer token, memoria máxima, presión de memoria macOS y tasa de tareas aceptadas. No deduzca la velocidad
> del único número de parámetros activos: la arquitectura híbrida y la implementación de los kernels pueden producir
> Diferencias
> Es importante entre backends.
>
> **Qwen3.8-27B.** El denso **Qwen3.8-27B** se convierte en el challenger local quality-first a añadir al
> bake-off Scala. Qwen publica un contexto que puede llegar hasta 1M dependiendo del despliegue y las puntuaciones editor de 73 sobre
> Terminal-Bench 2.1 y 61,7 en SWE-bench Pro. Estas cifras no justifican sustituir Coder-Next por defecto:
> prueba
> los dos con el mismo arness, el mismo contexto, las mismas herramientas y el mismo presupuesto de tiempo. **Coder-Next sigue siendo el mismo.
> baseline local especializada y económica; Qwen3.8-27B es el challenger que se prefiere cuando la calidad cuenta más
> que el caudal.** Tarifas API Qwen3.8 dependen de la región y no deben presentarse como un precio mundial.

>
> **Qwen3.8-Omni-Flash.** Desde el 17 septiembre 2026, Alibaba también propone este modelo API multimodal: texto, imagen,
> audio y vídeo en entrada, texto en salida, function calling, thinking configurable, búsqueda web, caché de contexto,
> **1M tokens de contexto** y hasta **131 072 tokens de salida** via Chat Completions o Responses API. Completa
> el enrutamiento para el análisis de screencasts, talks, interfaces o documentación multimodal; ** no sustituye**
> Qwen3-Coder-Next como baseline local de código ni Qwen3.8-27B como challenger Scala quality-first. Sus tarifas varían
> según la región de despliegue: mantenga este dato fuera de las reglas de enrutamiento durable y comprueba Model Studio en
> momento de la elección.

<!-- section: s-3 -->
### En relación con Anthropic

| Modelo         | API ID              | Tarifa (input/output / M tokens) | Antecedentes          | Esfuerzo predeterminado | Función activa en esta guía                                                           |
|----------------|---------------------|---------------------------------|-------------------|-------------------|------------------------------------------------------------------------------------|
| **Fable 5.2**  | `claude-fable-5-2`  | $8 / $40                        | 1M (salida 128K)  | `high`            | Frontier: razonamiento exigente y largo horizonte cuando Opus 5.5 no es suficiente      |
| **Opus 5.5**   | `claude-opus-5-5`   | $4 / $20                        | 1M (salida 128K)  | **`medium`**      | Fallo agente: coding autónomo, arquitectura, debugging y grandes refactors      |
| **Sonnet 5.5** | `claude-sonnet-5-5` | $2 / $10                        | 1M (salida 128K)  | `high` API        | Micro-dev / tareas bien especificadas; `medium` recomendado para Agentic coding borné |
| **Haiku 5.5**  | `claude-haiku-5-5`  | $0.10 / $0.50 (prompt ≤ 100K)   | 1M (salida 128K)  | `medium`          | Trabajadores, clasificación, extracción, logs, subagentes de bajo riesgo                     |

> **Rodamiento corriente:** Anthropic recomienda iniciar la mayoría de los workloads con **Opus 5.5**,
> cuyo esfuerzo por defecto es `medium`, y luego ajustar el esfuerzo antes de cambiar de modelo. Para **Sonnet 5.5**, el
> coding agentifique bien especificado comienza útilmente a `medium` y sube a `high` para tareas más largas o
> Es difícil.
> `xhigh` (notado **Extra** en esta guía) y `max` se reservan para los casos en que los evals muestran una ganancia. **Haiku 4.5 n
> no soporta el parámetro de esfuerzo; Haiku 5.5, que lo reemplaza, lo soporta con `medium` por defecto.** Los párrafos que aparecen a continuación en Sonnet 5 / Opus 5 siguen siendo puntos de referencia de
> migración
> históricos; no sustituyen a esta matriz activa.

> **Migración API vers Opus 5.5 / Sonnet 5.5.** Ambos modelos imponen más disciplina al cliente que los
> generaciones anteriores: el adaptive thinking es el régimen normal, el *forced tool use* (`tool_choice: any/tool`)
> devuelve un error 400, y los *thinking blocks[* deben permanecer unidos a su modelo y a la conversación que los tiene
> productos. **Opus 5.5** también rechaza los parámetros de Sampling no estándar y el asistente prefill; su esfuerzo por
> falta es `medium`. **Sonnet 5.5** utilizar `thinking: {"type": "between_tools"}` para eliminar el thinking inicial
> (`low` a `high` únicamente), y ahora devuelve el texto intermedio entre tool calls en bloques `thinking`.
> En Claude API y Google Cloud, ambos modelos utilizan el toolset computador-uso actual
> `computer_toolset_20260801` en lugar de `computer_20251124`. Por lo tanto, una migración de modelos debe probar **payloads,
> streaming, tools y reanudación de conversación**, no sólo reemplazar el ID del modelo.

> **Sonnet 5** sustituye Sonnet 4.6 (`claude-sonnet-4-6` siempre disponible a la misma tarifa
> $3/$15) como driver diario. *drop-in replacement* lado API, con tres cambios de comportamiento en
> conocer antes de migrar:
> - **Adaptive thinking activado por defecto** ; el extended thinking manual (`thinking: {type: "enabled"}` con
>   `budget_tokens`) devuelve ahora una **error 400** - Migrando al adaptive thinking.
> - **Configuración de Sampling bloqueada** : cualquier valor no fallido de `temperature`, `top_p` o `top_k` devuelve
>   un error 400.
> - **Nuevo tokenizer** (mismo linaje queOpus 4.7+) : ~30% de tokens más para el mismo texto (hasta 1.35x
>   El tokenizer siempre puede aumentar el número de tokens facturados; por lo tanto, recuenta los
>   Prompts con el endpoint de token counting y vuelve a verlos `max_tokens` apretados.
>
> Otras particularidades operativas: **Effort Control** general (nivel bajo) → **xhigh**, defecto *high* sobre
> l'API y Claude Code), primero **seguridad cibernética en tiempo real** en un Sonnet (una negativa regresa en HTTP
> 200 con `stop_reason: "refusal"`, no en error  la administración de  la Priority Tier en el cliente, no la salida 128K
> (300K en batch a través del header beta `output-300k-2026-03-24`. También es el nuevo modelo predeterminado de los planos
> Free y Pro en claud.ai.

> **Envíos conjuntos**: el pronto caching y el batch (el –50% input y el output) se aplican a * todos* los modelos
> Claude. Sin embargo, la tarifa de lectura del caché depende del modelo: **Fable 5.2 cuesta $0.20/M tokens en caché leído**
> (contra $0.25/M para Fable 5.1). La lucha sigue siendo útil para el trabajo no urgente: PR summaries agrupados,
> auditorías planificadas y generación de fixturas. Fable 5.2, Opus 5.5 y Sonnet 5.5 incluyen el contexto 1M al precio
> estándar, sin sobrecarga de contexto largo.
>
> **Precisión arancelaria.** La caché read vale la pena **0,025× Input** sobre Fable 5.2/5.1 ($0.20 y $0.25/M),
> **0,05×** sobre Opus 5.5 y Sonnet 5.5 ($0.20 y $0.10/M) y 0,1× sobre Haiku 4.5. Haiku 5.5 es el único modelo actual
> con un **paso de longitud de prompt** : más allá de 100 000 tokens de entrada (caché incluido), todas sus tarifas son
> Multiplicados por cinco. Fable 5.2 $4/$20, Opus 5.5 $2/$10, Sonnet 5.5 $1/$5. Fast mode: Fable 5.2 $16/$80,
> Opus 5.5 $8/$40. `inference_geo: "us"` aplica un multiplicador de 1,1× en las categorías correspondientes.

> **Claude Fable 5.2 Reemplazar Fable 5.1 en el enrutamiento activo de esta guía.** Ficha
> técnica: ID `claude-fable-5-2` (`anthropic.claude-fable-5-2` sobre Bedrock), contexto **1M**, salida **128K**,
> **$8/$40**, caché write 5 Min dólares$10 y 1 h $16, caché read **$0.20/M**, batch $4/$20, moda rápida `speed: "fast"` à
> $16/$80, adaptive thinking siempre activo, esfuerzo predeterminado `high`, cutoff junio 2026, retirada no antes del
> 9 Noviembre 2027. Las mismas limitaciones que 5.1 : **30 días de retención obligatorios (no ZDR sin autorización)
> expresa)**, `tool_choice: any/tool` y prefill en 400, sampling para omitir, sin Priority Tier, sin estructurad
> outputs para las organizaciones CMEK. El modelo genera alrededor de 30 % más rápido que 5.1. **Mythos 5.2** es el mismo
> modelo con menos salvaguardias, reservado a las organizaciones verificadas.
>
> **Posicionamiento.** La matriz oficial sigue siendo el siguiente: Opus 5.5 - se pasa a
> Fable 5.2 si los evals `xhigh` o `max` siguen siendo insuficientes en razonamiento exigente o largo horizonte.
> Novedades para integrar en el enrutamiento: en FrontierCode 2.0 (que mide si los sostenedores merecían el cambio),
> Anthropic informa **Fable 5.2 `high` à 45,3 %, a nivel deOpus 5.5 al mejor esfuerzo (45,5 % (%), aproximadamente la
> mitad del costo por tarea**. Puntuación editor al mejor esfuerzo: FrontierCode 2.0 **49,1 %** (Opus 5.5 45,5 ; Astra
> 42,8 ; Fable 5.1 32,4), FrontierSWE v2 **69,9 %** (Opus 62,3 ; Astra 65,5), Remote Labor Index 41,3 % en contra 21,3 %
> Para Opus. En el coding corto la diferencia es baja: Terminal-Bench 4.0 67,6 % contra 66,4 % (Opus `xhigh`, en la
> margen de error. Las medidas independientes Vals confirman el matiz: igualdad con Opus 5.5 en Terminal-Bench 4.0
> (65,15 %), Opus frente a SWE-bench Multimodal (70,2 % frente a 62,3 %).
> **Mini-SWE-agent** de Vals, esta igualdad corresponde sin embargo a alrededor de **$14,56/tarea para Fable contra
> $12,04 para Opus**, con Fable más rápido (55 min contra 64 min) : la ventaja de coste por trabajo anunciado
> por Anthropic en FrontierCode **no se generaliza** a los demás arneses.
>
> ```text
> Opus 5.5 High insuffisant (capacité)        → Fable 5.2 avant Opus 5.5 Max, à mesurer sur le benchmark Scala privé
> Décision difficile ponctuelle (advisor)     → Fable 5.2 low/medium
> Mission longue autonome                     → Fable 5.2 high (low/medium finissent plus souvent le tour trop tôt)
> Tâche bornée, bug UI/front, review courante → Opus 5.5 ou Sonnet 5.5 restent les meilleurs achats
> ```
>
> **Breaking changes desde Fable 5.1** (verificados en la guía de migración oficial):
> - el **prefix check[** se aplica ahora a todas las cuentas: un thinking block devuelto con un `system`,
>   `tools` o un historial diferente de los que lo han producido da un 400 (`The block is bound to a different
>   conversation`). **Un cambio de lista de herramientas MCP entre dos peticiones cuenta como una edición** : alfiler
>   la lista de herramientas durante la sesión, o utiliza los cambios de herramientas durante la conversación (beta
>   `inline-tools-2026-09-15`, a través de mensajes `role: "system"`.
>   solicitud modificando `tools`;
> - **Fable 5.1 y Opus 5.5 no leen los thinking blocks de Fable 5.2** (se suprimen sin errores, por lo tanto el
>   el razonamiento se pierde en silencio) ; Fable 5.2 lee los de 5.1 yOpus 5.5.
>   (`fallbacks: "default"`, beta `server-side-fallback-2026-07-01`) sólo se dirigen a `claude-opus-4-8` y
>   `claude-opus-5`: registra el modelo ejecutado;
> - `computer_20251124` devuelve 400 (excepto Bedrock): utilizar `computer_toolset_20260801` ;
> - el advisor de un ejecutante Fable 5.2 debe ser `claude-fable-5-2` o `claude-mythos-5-2` ;
> - el thinking cuenta en `max_tokens` (riesgo de `stop_reason: "max_tokens"` antes de cualquier texto) y Fable 5.2 a su
>   **propio bazo limit**, separada de la de Fable 5/5.1Nuevos betas útiles: compaction à la demande
>   (`compact-2026-09-04`), binding des thinking blocks (`thinking-binding-controls-2026-08-01`, avec
>   `prefix_mismatch_behavior: "drop_block"` sólo como paliativo).
>
> **Comportamientos que afectan directamente a la calidad de los diffs y al coste** (Guía de prompting) Fable 5.2) :
> - **Propiedad del código.** Sin consigna explícita, el modelo añade a la estructura existente, dúplica y indica los
>   problemas vecinos en lugar de corregirlos. La frase propuesta por Anthropic (el código de This codebase is yours...  ¡)
>   fusionar el código duplicado en aproximadamente la mitad de los ensayos, pero cuesta aproximadamente 1,5 ¡de tokens de salida, añade
>   pruebas y Docs no solicitados y modifica el comportamiento existente en un ensayo de seis a diez. **Para tickets
>   a diff minimum de esta guía, no la añada** ; reservála para una tarea explícita de deducción o de refactor,
>   y relee el diff en lugar del resumen, que a menudo omite pequeños cambios.
> - **Delegación.** À `xhigh` y `max`, Fable 5.2 puede lanzar subagentes para leer su propio trabajo, y
>   subagentes pueden representar una gran parte del coste de la sesión. Audition las líneas de `AGENTS.md`, skills y
>   archivos de agentes que invitan a delegar, y comprueba el modelo predeterminado de los subagentes.
> - **Fines de vuelta prematuros** (lista de tareas restantes, oferta de continuar) más frecuentes a `low` y `medium` :
>   para una misión larga, añade la consigna
>   Se distingue entre el obstáculo ordinario (que se tratará) y el bloqueo deliberado (archivo prohibido, guardafuegos: se deja y
>   Mantén tus propias confirmaciones para las acciones arriesgadas.
> - **Presupuesto del servidor de  la unidad de corte de circuito.** El `task_budget` API es indicativo: fija un **techo externo** coste,
>   número de llamadas, duración y número de intentos en el arness. `max_tokens` demasiado apretado puede interrumpir
>   Fácil antes del primer texto visible, ya que los tokens de thinking cuentan en la salida. Si la sesión parece
>   silenciosa, utiliza las actualizaciones entre herramientas cuando están disponibles en lugar de multiplicar los estímulos.
> - **Instrucciones heredadas que deben purgarse**: Las respuestas sin deliberar  la respuesta no detiene la reflexión a partir de `medium`
>   (Baja más bien el esfuerzo) , las líneas Opus 5.5 Den
>   el modelo mucho menos capaz de recuperar sus propios errores; los presupuestos de tokens escritos en el pronto
>   pueden ser retirados en `high`/`xhigh` sin pérdida; las precauciones anticuadas acumuladas en memoria reducen
>   Este es exactamente el papel de `/doctor prompt-audit` (sección 3, subagentes).
>
> **Acceso y cuota.** Claude Code **2.1.321+** (`claude --model claude-fable-5-2` ; el alias `fable` depende
> Los planes Max/Ultra admisibles pueden utilizar Fable hasta una fracción máxima de **50 % de los
> límites semanales**, según las condiciones reales; el uso en Pro puede depender de créditos adicionales
> o de una promoción temporal.
> Nunca **modelo visible**, **cuota incluida** y **facturación API/créditos** : control de la pantalla de consumo y los
> condiciones del plan en el momento de la sesión. Reajusta los esfuerzos `medium`, `high` y `xhigh` y el coste por tarea.

> **Note tokenizer** : el nuevo tokenizer fue introducido por **Opus 4.7** (No 4.8y genera hasta ~35% de
> tokens además deOpus 4.6 para el mismo texto. **Sonnet 5 adopta la misma línea** (~30% de tokens más que
> Sonnet 4.6, hasta 1.35x según el contenido). La penalización de conteo sigue siendo pertinente para las migraciones Opus a
> la misma tarifa; en Sonnet 5, la tarifa permanente **$2/$10** compensa una gran parte del aumento del número
> de tokens en comparación con Sonnet 4.6. El pasaje Opus 4.7 → 4.8 no lleva ninguna penalización adicional de tokenizer.

> **Opus 5 y transición desde 4.8** : Opus 5 es ahora el **modelo Anthropic difícil por defecto** Tarifa
> idéntico a Opus 4.8 ($5/$25). Guardia 4.8 sólo como fallback de compatibilidad o referencia histórica.
> - **Fast Mode** ($10/$50, ~2.5x la velocidad estándar): para una tarea dura, pero *interactiva* (debugging en pair),
>   Opus 5 Fast es a menudo una mejor compra que Fable.
> - **Effort Control** : rodar por esfuerzo sigue siendo el paso explícito antes Fable 5.2. En Opus 5, `xhigh` y `max`
>   requieren que el thinking se mantenga activado; `thinking: disabled` con estos niveles devuelve un error 400.
> - **Dynamic Workflows** sigue siendo pertinente para el paralelismo de códigobase-scale; en Claude Code, completalo ahora
>   Con Agente View. **Agente Equipo** sigue siendo experimental y **Ultrareview** en research preview: no los transforma
>   aún en dependencias obligatorias del flujo de trabajo.

> **Nota Claude Managed Agents** (plataforma alojada, beta pública desde abril 2026, header
> `managed-agents-2026-04-01`: desde Code with Claude (6 Mayo 2026), la plataforma añade **Outcomes** (grader)
> independiente en sección, bucle de revisión si el output no pasa), la ** orquestración multiagente** (hasta
> 20 Suboficiales especializados en paralelo en un filesystem compartido), **webhooks** de sesiones (beta)
> , y el **Dreaming** (research preview: curation de memoria entre sesiones). Tarification: tokens au
> tarifa API + $0.08 por hora de sesión activa. Para esta guía es la tercera opción sobre misiones largas,
> al lado de Fable monoagente y Opus + Dynamic Workflows
> criterios de éxito ejecutables (Outcomes es la versión de la plataforma de revisión de la sección 15A).

> **OpenAI Agentes API** es el mientras alojado lado OpenAI : utiliza el
> arness gestionado de Codex con **períodos de sesiones sostenibles**, compacción y recuperación gestionadas, MCP y subagentes en contextos aislados.
> Dos primitivos materializan directamente el context engineering de la sección 10: **tool search** no carga los
> definiciones de herramientas que cuando se vuelven pertinentes, y el **programmatic tool calling** permite la cadena,
> Ajustar y filtrar llamadas antes de inyectar sólo los resultados útiles. No es una nueva razón
> Preferir OpenAI à Anthropic : compara **Agentes API**, Claude Managed Agentes y arneses locales al costo por
> cambio aceptado, manteniendo las mismas specificaciones, pruebas y reglas de parada.
>
> **Computer use** también puede ejecutarse en un navegador alojado por OpenAI.
> crea la sesión, aprueba explícitamente cada nuevo origen y gestiona las autenticacións sensibles.
> Una aprobación original no es una confirmación por acción: para compra, supresión u otra operación
> Por lo tanto, mantén un runtime controlado o una gate applicative separada.


Características operativas complementarias:

| Modelo         | Latencia relativa | Prompt caching     | Batch (Beef[–50% ]%) | Especificaciones operacionales                                                                        |
|----------------|------------------|--------------------|--------------|---------------------------------------------------------------------------------------------------|
| **Fable 5.2**  | Moderada          | Sí; read $0.20/M | Sí.          | Adaptive thinking siempre on ; defecto `high` ; esfuerzo por mensaje ; fast $16/$80            |
| **Opus 5.5**   | Moderada          | Sí.                | Sí.          | Adaptive thinking siempre on ; defecto **`medium`** ; Low→Max                                     |
| **Sonnet 5.5** | Rápido           | Sí.                | Sí.          | Adaptive thinking ; defecto API `high`, pero `medium` recomendado para agentic coding bien especificado |
| **Haiku 5.5**  | La más rápida   | Sí; read $0.01/M | Sí.          | Adaptive thinking por defecto; esfuerzo `medium` por defecto; nivel de precios más allá de 100K tokens |

<!-- section: s-4 -->
### En relación con OpenAI / Codex

**GPT‑6.2 Sol** es el defecto recomendado para el **coding complejo y los flujos de trabajo agenticos repetidos** en Codex cuando esté disponible. OpenAI lo posiciona como más eficaz por tarea que Sol 6.1, a la misma tarifa API. **GPT‑6 Luna** se refiere a las tareas focalizadas , repetibles y de alto volumen; **GPT‑6.1 Terra** es el tier intermedio. **GPT‑6.2 Astra** sigue siendo la escalada de capacidad para las tareas más exigentes.

| Modelo          | ID API        | Precio estándar / 1 M tokens (input / output) | Función recomendada en esta guía |
|-----------------|---------------|---------------------------------------------|-------------------------------|
| **GPT‑6 Luna**  | `gpt-6-luna`  | **$0.10 / $0.50** | Micro-dev, cambios mecánicos, pruebas simples, clasificación y workers de bajo riesgo |
| **GPT‑6.1 Terra** | `gpt-6.1-terra` | **$1 / $5** | Patch local y repaso dirigido cuando Luna falta de juicio |
| **GPT‑6.2 Sol** | `gpt-6.2-sol` | **$2 / $10** | **Fallo Codex Agente Medium**: issue end-to-end, feature multi-archivoirs, tests, PR, review et stewardship |
| **GPT‑6.2 Astra** | `gpt-6.2-astra` | **$8 / $40** | Frontier: problema muy ambiguo, contrato crítico, escalada de capacidad |
| GPT‑6.1 Sol / GPT‑6 Astra | `gpt-6.1-sol` / `gpt-6-astra` | $2 / $10 ; $10 / $50 | Fallbacks si las versiones 6.2 no están disponibles; baselines históricos |

> **GPT‑6.1 Terra llena el agujero entre Luna y Sol.** Salió el 26 octubre 2026 (`gpt-6.1-terra`),
> Cuesta **$1/$5** (cached input $0.05/M), es decir, la mitad de Sol 6.1, con la misma ventana de alrededor 1,05M tokens.
> está disponible en ChatGPT Work y Codex (Plus, Pro, Enterprise, Edu; no en la pestaña Chat) y pide una Codex
> CLI reciente (0.159+ según las fuentes). OpenAI lo coloca en las correcciones de errores corrientes, computer use,
> la visión y la escritura; para el coding exigente, ahora prefiere **Sol 6.2 o Astra 6.2**. Puntuación publicada:
> 50,3 % en Terminal-Bench 4.0 a máximo esfuerzo (21,5 % para GPT‑5.6 TerraPara esta guía, Terra se convierte en el **Candidato
> natural para parches bornados y repaso de pequeños diffs** cuando Luna es demasiado justo y Sol demasiado caro: para partir
> por bake-off antes de cambiar la matriz.

> **GPT‑6.2 Sol y Astra**: 1,05M tokens de ventana, de los cuales 922K de entrada máxima y 128K de salida máxima.
> Escondido read: $0.10/M para Sol, $0.40/M para Astra; caché write 30 min a 1,25× input, 12 h à 2,5×.
> Más allá de 272K tokens de entrada, las tarifas input/cache doblan y la tarifa output se multiplica por 1,5 para
> Batch está en la sala de espera. 50 % de la tarifa estándar; Flex no se propone en los nuevos modelos 6.2.
> No transponga estos precios a la cuota de suscripción. Sol 6.1 Medium y Astra 6 Light siguen siendo fallbacks si los
> Las versiones 6.2 no están disponibles. El stewardship es una capacidad del arness, no del modelo.
> anteriores siguen siendo baselines históricos, que no deben atribuirse a los modelos 6.2.

> **Ultrafast es un tier de servicio, no un nuevo modelo ni un nivel de esfuerzo.** Base histórica: para GPT-6 Astra, l'API Ultrafast
> se refiere a hasta ~8 ¡la velocidad de Standard y factura en contexto corto **$60/M input, $6/M cached input, $75/M caché
> write y $300/M output**. Utilízalo sólo cuando la latencia realmente domina el coste total; para los rizos
> Agente de muchos tool calls, OpenAI recomienda una conexión de respuesta persistente en WebSocket. Ultrafast no
> no es compatible con la residencia de los datos de la UE: funciona en un tratamiento global o con residencia de EE.UU.
> producto, Astra Ultrafast está incluido en **Pro 500** y algunas ofertas Enterprise. Por lo tanto, no cambia
> el enrutamiento de calidad de esta sección: `Astra Standard` y `Astra Ultrafast` tienen la misma capacidad modelo.
> En GPT‑6.2, comprueba las tarifas y los derechos del plan antes de activar; sólo reserva a terceros rápidos a los rizos
> interactivas realmente limitadas por la latencia, no a la espera de CI.

En **Codex / Work**, razona con los niveles visibles **Light → Medium → High → Extra High → Ultra**. El defecto de esta guía es **Sol Medium**, **Luna High** para microbouchles y **Astra Light** para una escalada de capacidad. `Ultra` supera un simple run mono-agente y sólo es rentable si el trabajo puede descomponerse realmente en ejes independientes. API, los nombres de los niveles `low/medium/high/xhigh/max` según el modelo: no confunde el texto producido con el valor portátil de `reasoning.effort`.

Los modelos GPT‑5.6 pueden estar disponibles durante el rollout, pero ya no constituyen la ruta activa predeterminada de esta guía.

<!-- section: s-5 -->
#### Cinco dimensiones que no deben confundirse

| Levier                            | Lo que está cambiando                                                                                     | Regla práctica                                                                                                           |
|-----------------------------------|-----------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|
| **Modelo**                        | Capacidad, velocidad y precios: Luna, Terra, Sol 6.2 o Astra 6.2.                                 | Luna para el borné; Sol 6.2 para la lefluente repetida; Astra sólo cuando la capacidad superior reduce las repeticiones. |
| **Effort**                        | Presupuesto de razonamiento: Codex Light→Ultra; API `low/medium/high/xhigh/max` según modelo. | Suelo: Medium predeterminado; Luna: High; Astra: Light; aumentar sólo si planificación/verificación lo justifica.   |
| **`reasoning.mode: "pro"`** (API) | Más trabajo modelo para una respuesta final más confiable.                                    | Independiente del esfuerzo; comparar estándar/pro en tareas representativas.                                          |
| **`ultra` como esfuerzo Codex**    | Algunos SDK/harness Codex exponen ahora `ultra` como nivel de reasoning por encima de `max`. | Tratarlo como una capacidad del arness, no como un valor portátil de la Responses API.                             |
| **Ultra / Multi-agent**           | Orquestación de varios agentes o sesiones según la superficie producida/API.                         | Usarlo sólo si el trabajo se divide realmente en partes independientes.                                          |

En la ventana **Responses API**, el valor máximo documentado de `reasoning.effort` se queda `max` y **Multiagente** sigue siendo una característica beta distinta. En algunos arnesess Codex, `ultra` Por el contrario, no dedujeras nunca la semántica de la única palabra " ultra" , que se refiere a la superficie, el modelo, el esfuerzo y el número real de agentes. OpenAI no publica ningún multiplicador de coste fijo; medida de coste total, latencia y tasa de éxito en tu depósito antes de estandarización.

<!-- section: s-6 -->
#### Astra: controles para misiones prolongadas

Astra añade tres capacidades especialmente útiles a los agentes:

```text
async tool calling
→ continuer à raisonner ou appeler d'autres outils pendant qu'un outil lent s'exécute

mid-turn steering
→ ajouter une contrainte ou changer de direction sans redémarrer toute la mission

configuration updates
→ changer l'effort en cours de trajectoire sans casser inutilement le préfixe de cache
```

Para un backend agentista, prefiere la **Responses API** : el tool calling Astra y es la superficie de referencia. Astra no acepta `reasoning.effort = none`, ni los ajustes personalizados de `temperature` / `top_p` documentados como incompatibles. **Fast mode** API puede llegar hasta ~2× más rápido para **2× precio estándar** ; no tiene un SLA de latencia y no debe convertirse en el defecto de una misión larga.

<!-- section: s-7 -->
#### Disponibilidad y superficies ChatGPT / Codex

| Superficie                  | Acceso modelo y modo                                                                                                               |
|--------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| **ChatGPT Work / Codex** | GPT‑6.2 Sol y Astra, GPT‑6.1 Terra, Luna y fallbacks según plan, cliente, workspace y rollout.                                              |
| **GPT‑6.2 Sol / Astra**  | Más, Pro, Business, Enterprise y Edu en Codex/Work según derechos; controles de esfuerzo Light→Ultra según parámetros disponibles. |
| **GPT‑6 Luna**           | Modelo económico para tareas focalizadas y repetibles en Work/Codex.                                                            |
| **Ultra / multiagente**  | Para reservar a los ejes independientes; no asimilarlo a un mayor reflejo  la cadena secuencial.                    |
| **API**                  | `gpt-6.2-sol`, `gpt-6.2-astra`, `gpt-6.1-terra`, `gpt-6-luna` a través de las superficies soportadas; comprobar las herramientas y los esfuerzos por modelo.                |

Los derechos efectivos siempre dependen del plan, la región, el workspace y el rollout. Nunca codifiques una regla de producto duradera a partir del único nombre de una suscripción.

<!-- section: s-8 -->
#### Caching, seguridad y guardaespaldas

GPT‑6.2 Sol factura el cached input **$0.10/M** contra $2/M en input estándar; las caché writes permanecen en 1,25× input. GPT‑6 Luna baja en **$0.01/M** En cached input. Estabiliza la parte superior del prompt (`AGENTS.md`, convenios Scala, contratos, reglas de prueba) y deja diffs, logs y errores abajo.

> **Dos palancas de coste en volumen.** Sobre GPT‑6.1 Sol y GPT‑6 Luna, Batch y Flex 50 % menos que
> Estándar; en GPT‑6.2 Sol/Astra, Batch conserva esta reducción, pero Flex nspc no se propone.
> Utilízalos para lo que tolera la latencia: auditorías planificadas, PR summaries agrupadas, generación de fixturas y clasificación
> masiva. No transponga automáticamente estas tarifas API cuota ChatGPT/Codex : el indicador correcto sigue siendo el costo por
> tareas terminadas en la superficie realmente utilizada.

GPT‑5.6 sigue siendo clasificado como cibernético por el grupo de alto nivel, pero no por el grupo de Critical. **GPT‑6 Astra (generación original) es el primer modelo OpenAI Crítica de seguridad cibernética** : con las herramientas adecuadas, puede encontrar vulnerabilidades desconocidas y desarrollar nuevas cadenas de explotación. Este nivel de capacidad va acompañado de un monitoring de trayectoria más estricto: en ChatGPT/Codex, una tarea legítima puede ser ralentizada , pausada o solicitar una validación; API, el trabajo se puede parar.

Este aumento de la capacidad no justifica ninguna autonomía adicional. Con Astra, haz aún más explícitos: scope de archivos, red, operaciones externas, escrituras destructivas, presupuesto, duración, condiciones de parada y validación humana. Punto favorable para el código sensible: **Astra soporta el Zero Data Retention para los clientes API admisibles**, pero Fable 5.2 obliga 30 días por defecto a menos que se autorice expresamenteAnthropic.

<!-- section: s-9 -->
#### Benchmarks y prudencia

Las cifras de lanzamiento de Astra son particularmente fuertes en el **coding agentique et computer use**, pero deben permanecer atados a su arnés. OpenAI informa en particular: Terminal-Bench 4.0 **57,9 % Astra vs 55,8 % Fable 5.1**, DeepSWE 1.1 **74,1 % vs 67,4 %**, FrontierCode Extended **64,5 % vs 63,6 %** y sus tareas internas de migración DB **63,9 % vs 57,8 %**. En AutomationBench, Astra alcanzó **41,4 % vs 31,4 %** para Fable 5.1. Estas son evaluaciones publicadas por OpenAI : útiles como señal, nunca como veredicto sobre Scala.

La evaluación independiente Artificial Analysis matiza fuertemente la tabla. En su **Coding Agent Index v1.4**, Claude Code + Fable 5.1 (`max`, con fallback) consigue **70** contra **67** para Codex + Astra (`max`), pero Astra consume aproximadamente **4,0M tokens/tarea contra 7,1M** y cuesta alrededor de **$4,72/tâche contre $9,18**. Sobre el **Intelligence Index**, Fable 5.1 `max` está también delante (**66 vs 61**) Por lo tanto, la buena enseñanza no es " Astra" > Fable "B": **Fable mantiene una pequeña ventaja de calidad agregada en estos protocolos, Astra una ventaja importante de eficacia por tarea en Codex**.

Astra también publica un muy buen recordatorio largo contexto en MRCR v2 : **100 % à 256–512K** y **96,3 % à 512K–1M**. No conviertas estas puntuaciones en permiso para enviar el monorepo entero: más allá de 272K, su tarifa aumenta y el *context rot* Sigue siendo un problema de razonamiento, no sólo de capacidad física.

Para esta guía, la conclusión robusta se convierte en:

```text
GPT‑6 Luna High = micro-dev et workers Codex sous contrôle humain fort.
GPT‑6.2 Sol Medium = défaut Codex pour l'agentic coding end-to-end.
GPT‑6.2 Sol High = feature complexe, migration et reprise difficile.
GPT‑6.2 Astra Light = escalade de capacité avant de pousser mécaniquement Sol à l'effort extrême.
Sonnet 5.5 Medium = micro-dev Claude et tâches agentiques bien spécifiées.
Opus 5.5 Medium = défaut Claude pour l'agentic coding autonome.
Opus 5.5 High = architecture, debugging et refactor difficiles.
Fable 5.2 Low = escalade frontier quand Opus High reste insuffisant.
Astra vs Fable = décider au coût par changement accepté, pas au prix par token.
```

<!-- section: s-10 -->
### GPT‑6 Astra vs Claude Fable 5.2: referencia histórica de dos fronteros

Esta comparación conserva las cifras del GPT‑6 Astra original: para el enrutamiento corriente, utiliza GPT‑6.2 Astra Si el cliente lo propone. Su tarifa estándar es $8/$40 (cache read $)$0.40/M) ; no le atribuye los resultados del antiguo Astra. Comparar los modelos actuales en el mismo arness y el mismo depósito.

Compare el **modelo en su arness real**, no un número de editor aislado. Fable 5.2 es más barato por token estándar que GPT‑6 Astra, pero la diferencia de coste por tarea depende del caching, el esfuerzo, las herramientas y las reproducciones.

| Eje | GPT‑6 Astra | Claude Fable 5.2 | Consecuencias prácticas |
|-----|-------------|------------------|---------------------|
| Harness natural | Codex / ChatGPT Work / Responses API | Claude Code / Mensajes API | Medir el sistema completo |
| Precio estándar input / output (M tokens) | **$10 / $50** | **$8 / $40** | Más barato nominalmente |
| Cache read (M tokens) | **$1** | **$0.20** | Ventaja Fable en prefijos realmente reutilizables |
| Largo contexto | 1,05M; sobrecarga más allá de 272K | 1M; tarifa estándar | Preferir contexto específico en ambos casos |
| Esfuerzo | Light→Ultra por superficie; API low→max | low→max ; adaptive thinking | Fable `high` para larga autonomía, `low` para dictamen puntual |
| Computer use | Capaz, con orquesta y herramientas | Resultados de editor fuertes | Verificar en escenarios reproducibles |
| Calidad de diff mergeable | Evaluaciones con arness Codex | FrontierCode 2.0: 49,1 % al mejor esfuerzo según Anthropic | Los protocolos de edición no demuestran una superioridad general |
| Independencia de medidas | Evaluaciones de terceros disponibles | Vals: igualdad con Opus en Terminal-Bench 4.0, retroceso en multimodal | Esperar una comparación Fable 5.2 / Astra de arness comparable |
| ZDR | Clientes API admisibles | 30 días por defecto, excepción contractual necesaria | Filtrar tareas por requisitos de privacidad |
| Misiones prolongadas | Async tools, mid-turn steering | Esfuerzo por torre, thinking relacionado con el historial | Proteger estado, herramientas y reglas de parada |

**Lectura de benchmarks.** Anthropic anuncio Fable 5.2 delante de Astra en FrontierCode 2.0, FrontierSWE v2 y OSWorld 2.1, pero son unos **resultados de edición**El Coding Agente Índice de Análisis Artificial Comparado Claude Code + Opus 5.5 à Codex + Astra indica un compromiso diferente entre tasa de éxito , coste y duración; **no mide Fable 5.2**La comparación histórica Fable 5.1/Astra ya no debe servir como regla de enrutamiento actual. Los resultados independientes de Vals también muestran que Fable 5.2 no es sistemáticamente mejor queOpus 5.5.

Regla de enrutamiento práctica:

```text
Micro-dev interactif, humain dans la boucle
→ GPT‑6 Luna High ou Sonnet 5.5 Medium

Issue standard end-to-end
→ GPT‑6.2 Sol Medium
→ Opus 5.5 Medium en review indépendante

Architecture / root cause / refactor difficile
→ Opus 5.5 High
→ GPT‑6.2 Sol Medium/High pour challenger

Sol High insuffisant par limite de capacité
→ GPT‑6.2 Astra Light puis Medium si nécessaire

Opus High insuffisant par limite de capacité
→ Fable 5.2 Low puis Medium si nécessaire

Même tâche vraiment frontier, choix Astra vs Fable
→ deux worktrees / même spec / mêmes tests
→ comparer coût total + minutes humaines + qualité du diff
→ humain arbitre
```

Ya no se fija un par permanente Claude writer / Codex reviewer  law. **El writer se elige por naturaleza de tarea** : Sol 6.2 por lo general posee la salida estándar; Opus 5.5 La otra familia se utiliza para repasar o replantearse independientemente. Duplicar las dos trayectorias completas sólo está justificado para un bake-off o una decisión realmente fronteriza.

<!-- section: s-11 -->
### En relación con los modelos open-weight chinos (Kimi K3, GLM‑5.2, y el resto del cluster)

Desde2026, una tercera familia se impuso al lado deAnthropic y deOpenAI : los modelos **Abiertos chinos de nivel fronterizo**, que alcanzan una codificación de agentes cerca de Sonnet/Opus a un costo por token muy inferior. Para un senior Scala que ya está pilotando Claude Code y Codex, no son sustitutos del driver diario, pero **una palanca de coste en una clase exacta de subtareas** y una **opción de soberanía** (self-host) para código sensible.

**Trampa de categoría que debe enunciarse inmediatamente** : estos modelos no son **no** en la misma categoría que Qwen3-Coder-Next. Qwen local (80B/3B activos) es realmente explotable en tu laptop 128 GB: Q4_K_M deja un margen muy amplio, Q5_K_M es el mejor defecto y Q6_K sigue siendo viable. Q8_0 puede ser cargado, pero debe validarse con el contexto, IntelliJ y sbt Realmente abiertos. GLM‑5.2 (753B) y sobre todo Kimi K3 (2.8T) ne tiennent **no** local sobre 128 Go: son modelos **API** (Z.ai, Moonshot, OpenRouter) o **self-host en servidor multi-GPU**. Moonshot recomienda, por otra parte, un despliegue Kimi K3 en configs de 64+ Analizador. Por lo tanto, nunca los pongas en la casilla de verificación de la casilla de verificación. Qwen local: viven en la casilla de verificación API tercero o servidor de equipo de  lavabo.

| Modelo      | Editor / acceso                                                                                                    | Arquitectura                                                                                             | Antecedentes                 | Precio API (in / out /M)                | Base de referencia (medidas independientes/editor)                                                                                             |
|-------------|--------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|--------------------------|---------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| **Kimi K3** | Moonshot API, OpenRouter (`moonshotai/kimi-k3`), Kimi Code CLI; **pesos completos publicados** Licenciado Kimi K3 | MoE 2.8T total, **104B activados** ; 896 expertos, 16 activados; KDA + Atención Residentes, visión nativa    | Hasta 1M según el plan | **$3 / $15** (cache-hit input $0.30)  | Puntuación editor de esfuerzo máximo y con varios arneses; excelentes señales frontal y largo horizonte, para confirmar en Scala                   |
| **GLM‑5.2** | Zhipu/Z.a.i. API OpenAI- **y Anthropic- Compatible**, GLM Coding Plan; checkpoint MIT publicado                      | MoE **753B** Total BF16 ; número de activos no documentados oficialmente ; esparcimiento atención | 1M                       | **$[$1.40 /$4.40** (cache input $0.26) | Puntuación editor: SWE-bench Pro **62.1**, TerminalBench 2.1 81.0 con Terminus-2 y 82.7 mejor arness; para comparar con el mismo protocolo |

**Esfuerzo de razonamiento.** GLM‑5.2 exposición **High** y **Max**. Kimi K3 exposición `reasoning_effort: low | high | max`La página modelo/API indica **`max` predeterminado**, mientras que Kimi Code puede definir un defecto diferente según su versión y plan: por lo tanto, siempre fija el esfuerzo explícitamente en un benchmark o automatización. 1M depende del plan: 256K en Moderato, hasta 1M en Allegretto y arriba. Para una tarea interactiva corta, comienza en `low` o `high` ; reserva `max` a las misiones prolongadas en las que esté justificado su coste de salida.

<!-- section: s-12 -->
#### Donde entran en *ton* enrutamiento

```text
✅ Review de volume et triage à faible enjeu   → GLM‑5.2 (High) : tarif token très inférieur à Opus, mais coût par tâche à mesurer
✅ Extraction, classification, PR summaries bulk → GLM‑5.2 ou Kimi K3, en batch, quand le volume rend Sonnet/Terra cher
✅ Génération frontend / maquette web           → Kimi K3 (#1 Frontend Code Arena) si tu sors du périmètre Scala pur
✅ Second avis open-weight indépendant          → un modèle d'une 3e « école » d'entraînement casse les angles morts communs Claude/GPT
✅ Code sensible / air-gapped / souveraineté     → GLM‑5.2 en self-host (poids MIT) : rien ne sort de ton infra
```

```text
❌ Driver quotidien Scala à la place de Sonnet 5.5 : capable, mais tu perds l'écosystème (Claude Code, subagents, Metals MCP mûrs)
❌ Tâche interactive courte sur Kimi K3 en effort max : latence et verbosité, mauvais achat ; utiliser low/high
❌ Décision d'architecture critique en solo : garde Opus/Fable ou un vrai second avis Sol ; l'open-weight y reste un challenger, pas l'arbitre
❌ « Remplacer » Qwen local : mauvaise catégorie (voir piège ci-dessus)
```

<!-- section: s-13 -->
#### Acceso ocasional a GLM a través de OpenRouter

Para este flujo de trabajo, no añadas una suscripción de GLM por defecto. **GLM sigue siendo un modelo de emergencia**, a llamar vía OpenRouter cuando Claude Code, Codex y Qwen local no han permitido resolver el problema. Esto conserva la diversidad de modelos sin añadir una nueva cuenta, una nueva clave y un nuevo plan a seguir.

Si GLM se convierte en una herramienta utilizada cada semana o aporta una ganancia mensurable en una clase de tareas, entonces reevalua el interés de un acceso directo Z.ai. Mientras no se alcance este umbral, la simplicidad prima.

<!-- section: s-14 -->
#### El resto del cluster (para ubicar, no para adoptar todo)

`MiniMax M3` (junio 2026) es el primer open-weight en combinar codificación fronteriza, contexto 1M *y* multimodalidad nativa (cabeza de Open-weight en SWE-bench Pro a 59.0 antes GLM‑5.2). `DeepSeek V4` decae un V4 Pro y un V4 Flash$0.14/$0.28 /M) imbatible en la relación coste/contexto largo para la clasificación masiva. Ninguno es el mejor en todas partes  la escena de la noche libre de mediados de2026 es un cluster apretado donde la elección correcta depende de la tarea y el precio, no de una clasificación global.

<!-- section: s-15 -->
#### Dos reservas a la cabeza

1. **Progenancia y destilación.** Kimi K3 se identificó como  ¡Dl Claude         , en al menos un intercambio informado. Esta autoidentificación anecdótica **no es una prueba de destilación** y no permite ninguna conclusión científica o contractual sobre los datos de entrenamiento. Si la procedencia cuenta para un cliente, requiere documentación del editor y trata la información como desconocida hasta que se publica.
2. **Metodología de benchmark.** Las tablas de edición mezclan arneses diferentes (KimiCode, Claude Code, Codex, mini-SWE-agente) y K3 es sensible a la preservación de la historia de *thinking*. Las diferencias que se muestran a menudo son inferiores a un punto: no siempre sobreviven a un cambio de arneses. Regla sin cambios: **Bake-off controlado en tus tareas reales** (versiones fijas, permisos fijos, pruebas de aceptación deterministas, costo por cambio aceptado), no adopción basada en una clasificación.

<!-- section: s-16 -->
#### Protocolo de bake-off Scala : Kimi K3 contra GLM‑5.2

No sólo compara las respuestas finales. Use como mínimo **15 tareas privadas**, nunca publicadas, repartidas entre:

```text
3 bugs Scala 3 subtils : givens, implicits, variance, types opaques
3 évolutions Play / Tapir / Pekko sur 3 à 8 fichiers
3 tâches Spark / concurrence / performance
3 reviews de PR avec défauts injectés connus
3 tâches de tests : ScalaTest, ScalaCheck, mutation testing
```

Protocolo: mismo commit, mismo worktree inicial, mismas herramientas, mismo límite de tiempo, misma red, mismo paquete de contexto, mismos criterios de parada y **tres repeticiones por tarea**. Kimi debe ser probado por separado en `high` y `max`; GLM `High` y `Max`. Si los arneses no pueden ser idénticos, publica dos matrices y no asigna la diferencia al modelo.

Medidas obligatorias:

```text
- tâche acceptée par les tests et la review humaine ;
- compilation, tests ciblés, mutation score ;
- défauts de sécurité ou de contrat détectés ;
- lignes ajoutées / supprimées et fichiers touchés ;
- nombre de reprises, tool calls et boucles identiques ;
- tokens input, cache, reasoning et output ;
- coût API total, latence et minutes humaines jusqu'au merge ;
- taux de réussite pass@1 et stabilité sur trois runs.
```

Aproba GLM o Kimi en un flujo sólo si reduce el coste por cambio aceptado **sin** Degradar los guardaespaldas. Una puntuación editor superior pero más correcciones humanas es una regresión, no una ganancia.

<!-- section: s-17 -->
## Regla de decisión por tarea

<!-- section: s-18 -->
### Cuando utilice **Fable 5.2** (Mythos-class)

Fable 5.2 cuesta dos veces Opus 5.5 por token ($8/$40 contra $4/$20). Anthropic recomienda comenzar con **Opus 5.5 `medium`**, subir hacia `high`y luego reservar Fable 5.2 para una escalada de capacidad, prueba **Fable `low`** antes de empujar Opus sistemáticamente a `Extra`/`Max` :

```text
✅ Migration complète d'un framework (Play 2 → 3, Pekko, Spark upgrade)
✅ Session autonome multi-heures / multi-jours sans supervision
✅ Refactor cross-modules sur > 10 fichiers interdépendants
✅ Débogage d'un bug métier dont la cause est très loin du symptôme
✅ Décision architecturale sans "bonne réponse évidente" après essai Opus 5.5 High
✅ Tâche où tu paierais sinon un senior engineer une demi-journée
```

```text
❌ Tâche bien scoped et bornée : Sonnet 5.5 ou Opus 5.5 sont de meilleurs achats
❌ Revue de diff ou PR summary : overkill, coût inutile
❌ Génération de boilerplate ou de fixtures : Qwen ou Haiku suffisent
❌ One-liner ou patch ciblé : Luna High, Sonnet 5.5 Medium ou Aider
❌ Tâche dure mais interactive avec toi dans la boucle : Opus 5.5 Medium/High suffit généralement
```

> **Posicionamiento 5.2.** Anthropic recomienda que se conserve **Opus 5.5 como punto de partida** para la mayoría de los
> workloads. Fable 5.2 `low` es un **advisor puntual**, a evaluar en una tarea limitada y verificable; para una misión
> Realmente autosuficiente, comienza en `high` para reducir los fines de la vuelta prematura. **costo por cambio
> aceptado** en el benchmark Scala privado, en lugar de generalizar los resultados del proveedor.
> $0.20/M mejora la economía de los prefijos largos estables. Cuando el verificador es fiable, también prueba el esquema
> **Low → retry High sur fail** incluyendo repetidos, latencia, revisión y validación humana.

<!-- section: s-19 -->
### Prompting Fable 5.2 : estructurar una misión larga

Fable 5.2 (ventana) 1M, salida hasta 128K) no es un simple Opus más fuerte, sino que apunta al razonamiento exigente y a largo plazo cuando las evaluaciones Opus siguen siendo insuficientes. La continuidad de los thinking blocks y la estabilidad de las definiciones de herramientas se convierten en limitaciones del arness, además del esfuerzo configurable por mensaje. Referencia: `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2`. Las palancas siguientes siguen siendo válidas para 5.2 ; los puntos específicos de 5.2 (propiedad del código, sobre-delegación, fines de vuelta prematuros, histórico append-only, instrucciones heredadas para purgar) se detallan en la nota Fable 5.2 de la sección  lata Anthropic ».

Cinco palancas específicas:

1. **Carta de misión en cabeza de contexto, oculta.** El bloque inicial (objetivo, no objetivos, invariantes, reglas de parada) nunca debe cambiar entre las torres: se beneficia del prompt caching y sirve de ancla anti-derive en las sesiones largas. Todo lo que evoluciona (estado, errores, diffs) va después.
2. **Estado persistente explícito.** En una misión multi-hora, requiere un archivo de estado (`MIGRATION_STATE.md` en el worktree) que el modelo actualiza a cada hito: módulos tratados, módulos restantes, decisiones tomadas, bloqueos. Este archivo
3. **Checkpoints con criterio de salida.** Corta la misión en hitos verificables mediante comandos deterministas (`compile`, pruebas selectivas, escalafmtCheckAll). No pasa al siguiente hito sin un hito corriente verde.
4. **Ruta el esfuerzo por turno sin cambiar de modelo.** Use `medium/high` para la exploración, `xhigh/max` para una decisión realmente difícil, entonces `low/medium` para una edición mecánica. El per-mensaje de esfuerzo preserva el caché y evita pagar el nivel máximo durante toda la trayectoria.
5. ** En caso de que una compaction sea necesaria, impone su contrato de resumen.** Solicitar que se preserven explícitamente problemas y resoluciones, pistas probadas o descartadas, decisiones y limitaciones, estado actual, puntos abiertos y detalles difíciles de reconstruir. La compaction servidor ya gestiona esta necesidad; para una compaction del cliente, nunca resume en prosa libre sin estos campos.

Gabarit de mission Fable 5.2:

```text
# MISSION (statique — ne pas modifier en cours de session)
Objectif : [migration / refactor précis]
Non-objectifs : [ce qui est explicitement hors scope]
Invariants : API publiques, contrats JSON, comportements listés dans AGENTS.md
Durée max : [N heures] — Coût max : [N USD] — Diff max par jalon : [N lignes]

# RÈGLES D'ARRÊT (statique)
Stop et rapport immédiat si :
- un invariant doit être violé pour avancer ;
- le même jalon échoue 2 fois pour des causes différentes ;
- build.sbt, migration DB ou contrat public doit changer ;
- l'estimation de durée restante dépasse 2x l'estimation initiale.

# PROTOCOLE (statique)
1. Lire AGENTS.md et MIGRATION_STATE.md.
2. Traiter UN jalon : plan court → diff → compile → tests ciblés.
3. Mettre à jour MIGRATION_STATE.md et committer le jalon.
4. Rapport de progression : jalon terminé, jalons restants, risques nouveaux, écart au plan.
5. Reprendre en 2.

# ÉTAT (dynamique — joindre la version courante de MIGRATION_STATE.md)
[état]
```

> **Continuidad Fable 5.2.** No retrograde silenciosamente una sesión: Fable 5.1 y Opus 5.5 no conectan los
> thinking blocks de Fable 5.2. Tampoco edita mensajes antiguos, el prefijo del sistema o la lista de herramientas
> reutilizando estos bloques: el control de coherencia puede producir un error 400. Si un cambio de herramientas o de
> modelo es indispensable, guarda el estado útil en `MIGRATION_STATE.md`, y luego vuelve a salir con un contexto propio.
> `tool_choice: any/tool` está prohibido en Fable 5.2 ; utiliza `auto` y valida el resultado con un esquema estricto.

> **Nota operativa**: una variable de seguridad puede cambiar el modelo realmente ejecutado. Si la misión toca el
> código cripto o seguridad bajo nivel, logice este modelo, compruebe que mantiene el nivel de capacidad esperado y previsto
> este caso en la regla de parada en lugar de descubrirlo durante la sesión.

<!-- section: s-20 -->
### Cuando utilice **Opus 5.5**

Es el **defecto Claude Code para el agente autónomo**. Su esfuerzo por defecto es `medium`, lo que cambia el enrutamiento en comparación con Opus 5 : comienza en `medium`, sube a `high` cuando la tarea es difícil, a continuación, utilizar `Extra` (`xhigh`) o `Max` si la duración o los evals lo justifican.

```text
✅ Issue complète quand Claude possède la trajectoire exploration → patch → tests
✅ Architecture, migration et plan multi-modules
✅ Root cause éloignée du symptôme, implicits/givens/effets difficiles
✅ Gros refactor où la cohérence globale domine la simple édition
✅ Review indépendante d'une PR écrite par Codex
✅ Orchestration de sous-agents read-heavy avec contexte isolé
```

```text
medium → défaut agentique
high   → debugging / architecture / long-horizon difficile
Extra  → >30 min et chaîne réellement longue ; pas pour une simple tâche "importante"
Max    → exceptionnel, qualité absolue prioritaire et gain mesuré
```

<!-- section: s-21 -->
### Cuando utilice **Sonnet 5.5**

La mejor opción Claude cuando **el senior mantiene fuerte la mano** o cuando la tarea de agente esté bien especificada. Anthropic recomienda explícitamente `medium` para el coding agente y el uso multistep de herramientas bien articuladas, luego `high` para tareas más largas o difíciles.

```text
✅ Petit bug reproductible
✅ Refactor local bien scoped
✅ Tests métier et property-based tests ciblés
✅ Stack trace → diagnostic → correctif
✅ Feature claire dont l'architecture est déjà décidée
✅ Worker d'implémentation derrière un plan humain ou Opus
```

```text
low    → transformation simple / latence prioritaire
medium → défaut micro-dev et agentic coding bien spécifié
high   → tâche plus longue ou plus difficile
Extra / Max → seulement si tes evals montrent un gain ; sinon passer à Opus 5.5
```

Por lo tanto, la regla económica ya no es la de Sonnet con el máximo esfuerzo antes de Opus. Si Sonnet High falla por un límite de capacidad, **Opus Medium** es a menudo una mejor compra que un Sonnet Extra/Max prolongado.

<!-- section: s-22 -->
### Cuando utilice **Haiku 5.5**

Sistemáticamente para tareas *alta frecuencia y bajo riesgo* :

```text
✅ Sous-agents de lecture ou extraction à faible risque (sortie vérifiable)
✅ Résumés de logs, PR summaries rapides
✅ Classification et routage
✅ Éditions ciblées < 20 lignes
✅ Génération de messages de commit
✅ Appels répétitifs à faible risque, si le benchmark confirme le gain
```

> **Haiku 5.5 Reemplazar Haiku 4.5 Como worker Claude.** Cuesta **$0.10/$0.50** Mientras el prompt
> se mantiene bajo 100 000 tokens (cache read $0.01/M), o bien **dix fois moins que Haiku 4.5** y el mismo orden de precio que
> GPT‑6 Luna ; más allá de 100K tokens de entrada, incluido el caché, la tarifa pasa a $0.50/$2.50. Contexto 1M, salida 128K,
> adaptive thinking activo por defecto y **parámetro `effort` compatible (`medium` por defecto)**. Trampas migratorias:
> el prefill devuelve ahora 400, `temperature`/`top_p`/`top_k` se omiten, `budget_tokens` devuelve 400, le
> thinking cuenta en `max_tokens`, y uno `tool_choice` Forzado permanece aceptado pero elimina la reflexión antes de la llamada.
> El tokenizer cuenta con aproximadamente 30 % de tokens más que Haiku 4.5. Regla práctica: Mantenga los contratos de subagentes
> ** bajo 100K tokens[** para permanecer en la parte inferior, lo que se une a la disciplina de aislamiento de la sección 3.
> Haiku 4.5 permanece activo, pero ahora es posible retirarlo en cualquier momento con el aviso habitual de 60 días.

<!-- section: s-23 -->
### Cuando utilice **GPT‑6 Luna**

```text
✅ Micro-dev : modification locale dont tu contrôles la direction
✅ Tests simples, fixtures, boilerplate, renommages et transformations mécaniques
✅ Recherche d'occurrences, résumés, logs et PR summaries
✅ Worker/subagent dont la sortie est vérifiée immédiatement
```

OpenAI recomienda comenzar Luna a **High**. No intentes convertir Luna en un agente fronterizo con Extra High: si la tarea se convierte en ambigua o conceptual, pasa a Sol 6.2 en lugar de pagar largas veces en un modelo demasiado pequeño.

<!-- section: s-24 -->
### Cuando utilice **GPT‑6.2 Sol**

```text
✅ Issue standard complète : découverte → implémentation → tests → PR
✅ Feature multi-fichiers et bug non trivial
✅ Review indépendante d'une PR écrite par Claude
✅ Migration bornée, compatibilité et refactor transversal
✅ Second avis sérieux sur une architecture proposée par Opus
```

```text
Light       → issue très bien spécifiée, patch local, reproduction claire
Medium      → défaut agentique quotidien
High        → feature complexe, root cause difficile, migration, beaucoup de cas limites
Extra High  → capacité suffisante mais besoin réel de davantage d'analyse/vérification
Ultra       → uniquement si le travail se décompose en investigations indépendantes
```

<!-- section: s-25 -->
### Cuando utilice **GPT‑6.2 Astra**

```text
✅ Sol High échoue parce que la capacité/jugement manque, pas parce que le contexte est pollué
✅ Sécurité, auth, contrat critique ou décision où une mauvaise direction coûte plusieurs reprises
✅ Workflow end-to-end très ambigu avec nombreux outils / computer use
✅ Reviewer frontier ponctuel sur une décision à fort impact
```

Comienza con **Astra Light**. Para una tarea realmente fronteriza, Astra Light puede costar menos que un Sol Extra High, seguido de una recuperación, porque evita una mala trayectoria. Sube a Medium/High sólo si es necesario; Extra High/Ultra siguen siendo excepcionales.

<!-- section: s-26 -->
### Cuándo usar **el modo `ultra` en ChatGPT Work / Codex**

```text
✅ Cartographie codebase-scale d'une application legacy
✅ Migration multi-modules en worktree dédié
✅ Audit architecture + tests + sécurité + performance en parallèle
✅ Décomposition d'un refactor en micro-PRs
✅ Mission où plusieurs sous-analyses indépendantes apportent une vraie valeur
```

```text
❌ One-shot “réécris proprement”
❌ Tâche interactive courte
❌ Repo mal testé sans limite de diff
❌ Modification directe de fichiers critiques sans plan validé
```

En esta subsección, `ultra` nombre **modo de orquesta multi-agente del producto**, y no el nivel de esfuerzo `ultra` que algunos SDK Codex Ahora es adecuado para las persianas independientes; evitalo cuando los agentes escriben en el mismo estado mutable o cuando una única operación lenta domina la tarea. En una aplicación legacy, comienza por cartografiar, producir un registro de deuda, proponer pruebas de caracterización y luego cortar en microPRs. No comienza por escribir código.

Gálibo mínimo para una misión `ultra` :

```text
Tu interviens comme équipe de reviewers/agents sur une application legacy Scala.

Rôles à simuler :
- architecte legacy ;
- tech lead Scala ;
- reviewer sécurité défensive ;
- QA / test engineer ;
- maintainer sceptique.

Objectif :
[objectif précis]

Contraintes :
- aucun changement de comportement observable sans validation ;
- pas de modification build.sbt / migrations DB / contrats JSON publics sans stop ;
- micro-PRs de moins de 300 lignes modifiées ;
- tests de caractérisation avant refactoring ;
- chaque conclusion doit citer les fichiers observés ;
- distinguer faits, hypothèses et recommandations.

Sortie attendue :
1. carte du périmètre ;
2. risques ;
3. registre de dette ;
4. tests de caractérisation prioritaires ;
5. plan en micro-PRs ;
6. première PR proposée, sans l'appliquer tant que le plan n'est pas validé.
```

<!-- section: s-27 -->
## Matriz de selección modelo rápido

```text
Micro-dev, humain garde le contrôle      → GPT‑6 Luna High / Sonnet 5.5 Medium
Worker lecture / triage à faible risque  → Haiku 5.5 / Qwen local / GPT‑6 Luna
Patch local au jugement intermédiaire    → GPT‑6.1 Terra Medium
Issue standard end-to-end                → GPT‑6.2 Sol Medium
Agent Claude end-to-end                  → Opus 5.5 Medium
Feature / bug difficile                  → GPT‑6.2 Sol High ou Opus 5.5 High selon nature
Architecture / root cause dominante      → Opus 5.5 High
Review croisée                           → famille opposée à l'auteur, Medium par défaut
Suivi post-PR Codex                       → GPT‑6.2 Sol Medium (Goal / Heartbeat / Cloud)
Sol High insuffisant                     → GPT‑6.2 Astra Light
Opus High insuffisant                    → Fable 5.2 Low
Long-horizon séquentiel > 30 min         → Opus 5.5 Extra (`xhigh`)
Codebase-scale parallélisable            → GPT‑6.2 Sol Ultra, surtout read-heavy
Frontier absolu                          → Astra Medium+ / Fable Medium+ après preuve du besoin
```

Regla práctica:

```text
Le senior garde la direction → modèle rapide et économique.
L'agent possède la trajectoire → Sol 6.2 ou Opus 5.5.
La compréhension domine le patch → privilégier Opus.
L'exécution end-to-end domine → privilégier Sol 6.2.
Une limite de capacité apparaît → Astra Light ou Fable Low avant l'effort extrême du tier inférieur.
Ultra uniquement si le problème contient plusieurs axes réellement indépendants.
```

<!-- section: s-28 -->
## Ruta automática de las tareas de desarrollo

La matriz de selección no debe permanecer sólo manual. Para evitar quemar créditos en tareas simples o, a la inversa, enviar una tarea crítica a un modelo demasiado débil, añade un paso explícito de enrutamiento antes de cada tarea de agente.

El principio no es elegir el modelo más inteligente, sino el modelo más pequeño capaz de producir un resultado mergeable con un riesgo aceptable.

```text
Demande / ticket / stack trace
→ classification de tâche
→ estimation difficulté + risque
→ sélection du modèle minimal acceptable
→ exécution avec permissions limitées
→ tests déterministes
→ escalade si échec
→ log coût / qualité
```

<!-- section: s-29 -->
### Arquitectura recomendada

```text
CLI / IDE / ticket
→ task-classifier
→ context-builder
→ model-router
→ agent-runner
→ test-runner
→ reviewer
→ cost-quality log
```

| Componente          | Función                                                         | Modelo / herramienta recomendado                                                                             |
|--------------------|--------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| `task-classifier`  | Ordenar la tarea, el riesgo y la dificultad                 | **Jev** si la salida está cerrada; Qwen local / Haiku si es necesario un razonamiento abierto         |
| `context-builder`  | Encontrar archivos, relaciones, pruebas, docs y pedidos útiles | Sourcebot, ScalaSemantic MCP, Codebase-Memory MCP si polyglotte, rg, IntelliJ, Metals MCP, Context7   |
| `model-router`     | Elegir el modelo más pequeño aceptable                      | Reglas deterministas + Jev como señal probabilista; OpenRouter sólo para escalada puntual  |
| `agent-runner`     | Ejecutar con los permisos correctos                         | Codex, Claude Code subagentes, Aider, OpenCode, Qwen Code                                              |
| `test-runner`      | Validar de manera determinista                              | sbt, IntelliJ, Metals MCP, CI                                                                         |
| `reviewer`         | Leer sin escribir                                           | Familia opuesta al writer: Opus 5.5 Medium o GPT‑6.2 Sol Medium; Astra/Fable sólo tan crítico |
| `cost-quality log` | Medir costo, calidad, retroalimentación y repaso            | Scripts locales, cuadro de seguimiento                                                                      |

<!-- section: s-30 -->
### Jev : decision layer, no coding model

**Jev 1.14 (`jev-1.14.0`)** es el modelo System One actual de TypeSafe AINo genera texto ni código: recibe un `state` y preguntas típicas, luego devuelve directamente decisiones probabilistas. El buen modelo mental es un **Semántica** : entrada abierta, ramas definidas por el desarrollador.

| Primitiva | Uso                                                           |
|-----------|-----------------------------------------------------------------|
| `Choice`  | elegir entre opciones cerradas: modelo, agente, skill, carretera |
| `Score`   | notar en una escala ordenada: riesgo, pertinencia, prioridad   |
| `Noul`    | Estimar la probabilidad de que una propuesta sea verdadera            |

Jev 1.14 cuesta **$0.042/M tokens input** y no factura la salida. El régimen estándar acepta **64K tokens por solicitud** y **32K para `state` + la cuestión más larga** ; los límites de flujo dependen de la organización y se leen en la consola. Un contexto experimental más largo y las entradas de imagen existen bajo condiciones, sin convertirse en el defecto del router. `jev-latest` punta hacia `jev-1.14.0` : **aprieta la versión** tan pronto como calibre umbrales, ya que el cambio de distribución puede invalidar los umbrales de riesgo.

> **OpenAI Decisions API.** Endpoint `POST /v1/decisions`, disponible actualmente en `gpt-6-luna`, con
> Respuestas típicas `predicate`, `choice` y `score`. Hasta **400 Preguntas** pueden compartir una misma entrada; texto,
> Imágenes y datos estructurados se soportan según el campo. Precio estándar: **$0.10/M tokens de entrada**, **$0.01/M
> tokens de entrada en caché leído**, sin facturación de salida , las escrituras de caché, entradas largas y procesamientos
> Las regiones siguen sus tarifas. `task-classifier` y el `model-router`, compara las decisiones con las Jev en los mismos
> preguntas con una calibración por tarea y riesgo, nunca sobre el precio único del token.

En este flujo de trabajo, los mejores candidatos son:

```text
✅ task / risk / difficulty classification
✅ model routing : Luna / Sol / Astra / Sonnet / Opus / Fable
✅ sélection progressive de quelques skills parmi un gros catalogue
✅ triage des résultats de subagents et pertinence d’un contexte
✅ signal topic-shift / « faut-il envisager une compaction ? »
✅ filtrage de notifications et décisions qui méritent l’attention humaine

❌ écrire ou expliquer du Scala
❌ architecture ou root-cause ouverts
❌ calcul, comptage ou comparaison de dates
❌ décider seul d’un push, déploiement, suppression, secret ou migration DB
```

Arquitectura recomendada:

```text
règles déterministes
→ Jev pour un jugement fermé et fréquent
→ code combine probabilités + seuils
→ LLM génératif si raisonnement ouvert ou confiance insuffisante
→ humain si action critique ou irréversible
```

**Tipo de safe  la correcta.** El argumento de que la exposición a las alucinaciones es cero Jev no sale de una estructura o de un conjunto de opciones declarado; siempre puede seleccionar la opción equivocada. Una evaluación independiente sobre **346 009 peticiones / 37 datasets** encuentra probabilidades `Choice` bien calibradas, pero también muestra que un umbral universal de `0.5` es malo para algunas tareas binarios: los umbrales deben ser **Calibrados por tarea y riesgo**.

Tres normas de integración:

1. **El código mantiene la autoridad.** Las señales deterministas (`touches_security`, archivo crítico, acción destructiva) siempre prevalecen sobre Jev.
2. ** Estado mínimo.** Jev también sufre *context rot* ; filtro antes de la apelación y n.o envía que lo que realmente cambia la decisión.
3. **Prueba la estabilidad.** Sobre `Choice`, reordena puntualmente las opciones; evaluaciones de `jev-1.13` indican una posible sensibilidad al orden, para validar en `jev-1.14.0`. El `state` opositor también puede influir en la respuesta: Jev Es una señal, no una sandbox.

<!-- section: s-31 -->
### Clasificación mínima

El router debe producir una decisión estructurada, no una respuesta libre. Ejemplo de salida esperado:

```json
{
  "task_type": "implementation | debug | test | review | migration | architecture | boilerplate | research",
  "risk": "low | medium | high | critical",
  "difficulty": "trivial | simple | normal | hard | frontier",
  "expected_files": "1 | 2-5 | 6-10 | 10+",
  "requires_code_write": true,
  "requires_external_docs": false,
  "touches_public_api": false,
  "touches_json_contract": false,
  "touches_database": false,
  "touches_build": false,
  "touches_security": false,
  "touches_concurrency": false,
  "model": "qwen | haiku55 | sonnet55 | opus55 | fable52 | gpt6_luna | gpt61_terra | gpt62_sol | gpt62_astra | gpt61_sol | gpt6_astra",
  "reasoning_effort": "light | low | medium | high | extra | xhigh | max | ultra | null",
  "reasoning_mode": "standard | pro | null",
  "multi_agent": false,
  "max_parallel_agents": 3,
  "max_cost_usd": 0.0,
  "max_duration_minutes": 0,
  "confidence": 0.0,
  "escalation_rule": "string",
  "stop_conditions": [
    "string"
  ]
}
```

**Jerarquía de las señales** : los criterios deterministas (`touches_*`, `expected_files`, tamaño de diff esperado) son los disparadores *primaria* Enrutamiento y escalada. Si la clasificación viene de **Haiku/Qwen**, `confidence` Sigue siendo una autoestima secundaria y mal calibrada. Si viene de **Jev**, utiliza la distribución y la `confidence` vueltas, pero con un **umbral calibrado por pregunta y nivel de riesgo**, nunca uno `0.75` universal. En ambos casos, una confianza elevada nunca debe *de escalada* una señal determinista crítica.

`reasoning_effort` debe ser estandarizado por superficie: Claude utiliza `low | medium | high | xhigh | max` en modelos compatibles, con **Opus 5.5 y Haiku 5.5 `medium`** por defecto; Codex cartel **Light | Medium | High | Extra High | Ultra**, mientras que elAPI OpenAI exposición de valores `low | medium | high | xhigh | max` según modelo. `multi_agent` El esfuerzo es una palanca de calidad y de coste, pero un tierno superior a bajo esfuerzo puede ser más barato en total que un tier inferior empujado al extremo.

<!-- section: s-32 -->
### Matriz automática de enrutamiento

| Señal detectada                                               | Modelo inicial                | Escalada                                                                      |
|--------------------------------------------------------------|-------------------------------|-------------------------------------------------------------------------------|
| Resumen, clasificación, grep, logs simples                           | Haiku 5.5 / Qwen              | Sonnet 5.5 Medium si ambiguo                                                   |
| Boilerplate, DTO, fixtures, edición mecánica                | GPT‑6 Luna High               | Sonnet 5.5 Medium si type/dominio sutil                                    |
| Prueba simple o no-regresión localizada                      | GPT‑6 Luna High               | Sonnet 5.5 Medium si regla profesional importante                                  |
| Patch objetivo, humano mantiene la dirección                       | Luna High / Sonnet 5.5 Medium | Sol 6.2 Light/Medium si es necesario explorar                                |
| Patch bornado con juicio intermedio                      | GPT‑6.1 Terra Medium           | GPT‑6.2 Sol Medium si es necesario explorar |
| Facturación profesional limitada, 1 à 5 archivos                        | GPT‑6.2 Sol Medium            | Sol High si dificultad ; Opus Medium en review                                |
| Factura 5 a 10 archivos con invariantes                      | GPT‑6.2 Sol Medium/High       | Opus 5.5 High si arquitectura/root causa domina                               |
| Bug Scala sutil, implicacits, givens, efectos                  | Opus 5.5 High                 | Suelo High para la hipótesis independiente ; Fable Low si capacidad insuficiente     |
| Migración de múltiples módulos borneados                               | GPT‑6.2 Sol High              | Opus High en review ; Astra Light si Sol techo                             |
| Refactor codebase-scale                                      | Opus 5.5 High                 | Extra tan largo horizonte; Fable Low si Opus techo                            |
| Revisión de una PR Codex                                        | Opus 5.5 Medium               | High si riesgo crítico                                                       |
| Revisión de una PR Claude                                       | GPT‑6.2 Sol Medium            | High y luego Astra Light si hay riesgo de frontera                                      |
| Seguimiento autónomo de un PR Codex                               | GPT‑6.2 Sol Medium            | High si diagnóstico difícil; Sol 6.1 Medium si 6.2 no está disponible             |
| Seguridad / Auth / contrato crítico                           | GPT‑6.2 Astra Light + humano    | Astra Medium/High + review Opus High                                          |
| Ejes read-heavy independientes                                 | GPT‑6.2 Sol Ultra             | Astra Ultra sólo si la capacidad adicional es realmente necesaria |
| Cambio `build.sbt`, dependencias, DB, contrato JSON público | No hay autoescritura           | Plan + validación humana                                                     |

<!-- section: s-33 -->
### Política de escalada

El enrutamiento automático debe funcionar como una cascada controlada:

```text
Micro-boucle vérifiable : Qwen / Haiku / GPT‑6 Luna High / Sonnet 5.5 Medium
→ ownership agentique : GPT‑6.2 Sol Medium / Opus 5.5 Medium
→ difficulté : Sol High / Opus High
→ limite de capacité : Astra Light / Fable Low
→ effort supérieur seulement si la capacité est suffisante mais le raisonnement manque
→ Ultra seulement si parallélisable
→ humain
```

**No cambies de modelo en medio de una conversación que se desvíe.** Si el fracaso viene de una trayectoria contaminada  la hipótesis falsa repetida, alucinaciones que se acumulan, correcciones que recrean otros errores  la situación es en sí misma parte del problema. Sonnet 5.5 → Opus 5.5, Sol 6.2 → Astra o Opus 5.5 → Fable 5.2 :

```text
1. Stop write mode.
2. Produire HANDOFF.md : objectif, état du diff, faits vérifiés, essais échoués, erreur actuelle, inconnues.
3. Ouvrir une session fraîche avec seulement spec + AGENTS.md + HANDOFF.md + fichiers/diff pertinents.
4. Escalader le modèle dans cette nouvelle session si la difficulté le justifie toujours.
```

La escalada de **capacidad** es útil sobre un problema propiamente dicho; no debe transportar la deuda conversacional de una sesión ya sesgada.

Escalada automática si:

```text
- un signal déterministe critique est présent (touches_* sensible, diff hors gabarit) ;
- auto-confidence LLM < 0.75, ou confidence Jev sous le seuil calibré pour cette décision ;
- erreur de compilation identique 2 fois ;
- test ciblé toujours rouge après 2 corrections ;
- diff hors scope ;
- plus de fichiers modifiés que prévu ;
- plus de 300 lignes de diff inattendues ;
- build.sbt, plugins.sbt, migration DB ou contrat JSON public est touché ;
- API publique modifiée ;
- le routeur détecte sécurité, concurrence, performance ou argent ;
- le modèle déclare explicitement une incertitude forte ;
- le coût estimé d'une erreur dépasse le coût du modèle supérieur.
```

Interromps (sin escalar automáticamente) si:

```text
- max_cost_usd est atteint (budget local) ;
- max_duration_minutes est atteint (timeout wall-clock) :
  une session agentique qui boucle est un mode de défaillance distinct d'une session qui échoue,
  et l'escalade vers un modèle plus cher ne corrige pas une boucle.
```

Desacelerar automáticamente si:

```text
- tâche purement textuelle ;
- aucun write mode nécessaire ;
- pas de risque métier ;
- moins de 20 lignes attendues ;
- fichier unique ;
- objectif déterministe ;
- test existant très ciblé ;
- contexte stable et déjà connu du projet.
```

<!-- section: s-34 -->
### Normas de no automatización

Nunca dejes que un router decida por sí solo sobre una escritura en:

```text
- build.sbt ;
- plugins.sbt ;
- resolvers ;
- versions de dépendances ;
- migrations DB ;
- contrats JSON publics ;
- sécurité ;
- authentification ;
- autorisation ;
- concurrence ;
- gestion d'argent ;
- suppression de données ;
- scripts de déploiement ou d'infrastructure.
```

En estos casos, el router sólo podrá proponer:

```text
- modèle recommandé ;
- plan ;
- fichiers probables ;
- tests à exécuter ;
- risques ;
- règle d'arrêt.
```

<!-- section: s-35 -->
### Subagentes Claude Code Recomendaciones

**Calibración Codex 6.2.** Para un pariente GPT‑6.2 Sol o Astra, ve con el mismo modelo y el mismo esfuerzo para los subagentes (recomendación oficial OpenAIA continuación, reduce el tier de las tareas verdaderamente mecánicas, de salida controlable: Luna/Haiku para grep, extracción, logs y resúmenes; Sol/Opus para invariantes, arquitectura y root causa. El mismo principio de medida vale lado Claude. Un revisor de la otra familia sigue siendo una sesión independiente, no un worker menos costoso del autor.

Claude Code es el mejor lugar para aplicar este enrutamiento a diario, ya que los subagentes pueden tener su propio contexto, herramientas y permisos.

```text
researcher
- Modèle : Haiku / Qwen si externe
- Mode : read-only
- Rôle : trouver fichiers, usages, tests, documentation

scala-implementer
- Modèle : Sonnet 5.5 `medium`
- Mode : write limité au repo
- Rôle : implémenter les tâches bornées sous contrôle d’un plan clair

hard-debugger
- Modèle : Opus 5.5 `high`
- Mode : write limité, plan obligatoire
- Rôle : bugs Scala subtils, implicits, effets, causes éloignées

migration-planner
- Modèle : Opus 5.5 `high` ; Fable 5.2 `low` (décision ponctuelle) ou `high` (mission longue) si Opus plafonne
- Mode : plan-first, worktree dédié
- Rôle : migrations multi-modules, refactors longs, stratégie de découpage
- Note : évaluer Dynamic Workflows (Opus 5.5 + subagents parallèles massifs)
  comme alternative à un Fable mono-agent sur les migrations codebase-scale

reviewer
- Modèle : Codex / GPT‑6.2 Sol `medium` ; Astra `light` si critique
- Mode : no-write
- Rôle : review indépendante, classement bloquant / important / optionnel

pr-summarizer
- Modèle : Qwen / GPT‑6 Luna
- Mode : no-write
- Rôle : résumé PR, release notes, checklist finale
```

<!-- section: s-36 -->
#### Aislamiento de contexto: el papel principal de los suboficiales en las tareas prolongadas

La ganancia de los subagentes no es sólo el paralelismo. Cada subagente trabaja en una **ventana de contexto fresco y aislado** ; el padre no necesita, por tanto, acumular las búsquedas, logs, archivos desviados y sin salida de cada subtarea. Este aislamiento protege el contexto principal contra el *context rot*.

El reparto recomendado es:

```text
PARENT
- objectif
- contraintes et non-objectifs
- plan validé
- décisions prises
- diff courant
- preuves essentielles
- risques ouverts

SUBAGENTS
- exploration de nombreux fichiers
- recherche Sourcebot / rg
- call paths, hiérarchies, usages et chaînes de givens via ScalaSemantic
- graphe structurel cross-language via Codebase-Memory si Java/Kotlin/Scala cohabitent
- investigation live des types / givens / diagnostics via Metals
- documentation externe
- logs et suites de tests volumineuses
- cartographie d'un module legacy
```

Regla de decisión:

```text
Les détails de cette sous-tâche seront-ils encore utiles au parent après sa fin ?

NON → subagent isolé
OUI → garder dans le contexte parent
```

El mensaje de delegación debe ser un **contrato**, ya que el subagente no debe depender de toda la conversación histórica del padre:

```text
Mission :
[périmètre précis]

Mode :
read-only / write borné

Cherche :
[questions précises]

Ne fais pas :
[hors scope]

Retourne uniquement :
1. conclusion ;
2. preuves file:line ;
3. tests ou commandes pertinents ;
4. incertitudes restantes.

Réponse cible : < 1–2K tokens.
```

La vuelta es una interfaz, no una transcripción. Si un subagente cama 80K tokens y devuelve 1,5K, el aislamiento es útil; si lo lee 10K y devuelve 8K, ha movido sobre todo el ruido. Una métrica sencilla a seguir en las tareas largas es:

```text
isolation_ratio
= tokens consommés par le subagent
/ tokens retournés au parent
```

Así que el buen pattern es **Map → reduce** : varios workers especializados gastan el contexto local, luego el padre sintetiza algunos resultados cortos. Evita el anti-pattern reverse *context rot* en el contexto raíz.

Para **tu workflow solo Scala**, trata también al fan-out como un presupuesto de tokens/competidores:

```text
défaut                              → 1 agent actif
2 investigations indépendantes     → 2 subagents read-only
2 User Stories indépendantes        → 2 writers maximum pour commencer (WIP inclut les PR en review)
3+ sessions parallèles              → uniquement si le gain et la capacité de review sont mesurés
writer                              → toujours 1 par branche / PR / worktree
```

Al menos `parallel_sessions_peak`, `subagent_count` y `subagent_tokens`, un subagente protege el contexto del padre, pero carga su propio contexto: por lo tanto, nunca es  ¡gratis! , y si no aporta aislamiento útil ni trabajo realmente paralelo, no lo lanza.

Para la coordinación, prefiere una **topología en estrella** : el padre delega contratos independientes y sintetiza retornos. Evita los equipos donde los agentes hablan libremente, comparten un mailbox o se distribuyen ellos mismos un estado mutable. En esta guía, el coordinador **Delegador simple**, no un sistema social de agentes.

> **Orquestración Claude Code** : **Agente View** será responsable de supervisar varias sesiones y tareas;
> **Agent Teams** permite la colaboración entre instancias pero sigue siendo experimental; **Ultrareview[** es una revisión de la nube
> Multi-agente en investigación previa. **Remote Control** permite supervisar una sesión local desde otro dispositivo
> al mismo tiempo que se mantienen la ejecución y los MCP en la máquina local. Estas superficies completan los subagentes;
> Cambiar
> no la regla ... un solo writer por worktree ...

> **Mod `You should know` (2.1.287+)** : `cc-plugin-you-should-know` lanza un side agente durante las tareas largas
> y muestra por encima del prompt los elementos que tú o Claude podrías perder. Es **desactivado por defecto** y
> seltragentiva vía `/plugin enable cc-plugin-you-should-know@builtin`. Trátalo como una señal de vigilancia oportunista,
> nunca como un revisor independiente, un oráculo o un gate: sus observaciones todavía deben estar relacionadas con una prueba,
> una prueba o un diff verificable.

> **Claude Code 2.1.27x: aislamiento más fino.** Desde 2.1.277, un subagente personalizado o proporcionado por un plugin puede
> declarar `omitClaudeMd` para no cargar `CLAUDE.md` usuario, proyecto y local; las políticas administradas
> Reserve este modo a los trabajadores de exploración muy especializados cuyo contrato de delegación contenga
> ya todo el contexto necesario. La misma versión permite atar `allowed_domains` a un comando
> Bash/PowerShell/Monitor: la apertura de red es válida para este comando, no para toda la sesión. ** confirma**
> n
> • normas mínimas por subagentes • y • permisos mínimos por subtarea • • sin justificar la supresión del
> contexto proyecto para un implementer que lo necesita.
>
> Desde 2.1.278, el modo Auto utiliza por defecto un **Clasificar lado servidor** en las superficies compatibles y
> Anthropic
> indica que este clasificador no añade costes de clasificación; `/status` indica si `Auto mode server` está activo.
> Esto reduce un overhead de enrutamiento, no los requisitos de autorización o revisión. Por último, plugins y skills
> se convierten en artefactos de prueba: `claude plugin eval` (2.1.269) realiza una serie de evaluaciones de la puntuación
> y reproducibles con salida JSON/HTML, mientras que `/skill-doctor` ayuda a detectar los esquís cargados pero innecesarios.
> Por lo tanto, un cambio persistente de plugin o skill debe pasar por eval + review antes de la promoción.
>
> Las siguientes versiones añaden dos herramientas complementarias para evitar la deriva del arness. Desde **2.1.283**,
> `/doctor prompt-audit` (alias `/checkup prompt-audit`) audita `CLAUDE.md`, skills, agentes y mandos para detectar
> n
> instrucciones que se han vuelto obsoletas o contradictorias después de un cambio de generación de modelos. Y en modo
> no interactivo, **`--bare`** ahora se documenta como la forma de lanzar un arness mínimo: no
> auto-discovery de los hooks/plugins/MCP/memoria/instrucción, y desde 2.1.286 solo los servidores MCP explícita
> no se han conectado, sin recordatorios del sistema ni tareas de fondo. Use `--bare` para **evals y scripts
> Reproducciones**, no como modo diario predeterminado.

<!-- section: s-37 -->
### OpenRouter para el enrutamiento API casual

En **este workflow solo preciso**, el enrutamiento principal no necesita una gateway APILos cinco caminos diarios ya tienen su propia superficie y presupuesto:

```text
Claude Code        → abonnement Claude Max
Codex              → abonnement ChatGPT
Qwen local         → MLX / llama.cpp / endpoint local
GitHub Copilot     → abonnement GitHub Copilot
JetBrains AI       → abonnement JetBrains AI
```

La necesidad API que queda es **excepcional** : cuando Claude Code y luego Codex permanecen bloqueados y quieres una opinión de otra familia de modelos, por ejemplo **GLM, Kimi, Gemini, Grok o un nuevo modelo para evaluar**. En ese caso, **OpenRouter es el mejor defecto** : una sola clave, ningún servidor que mantener, acceso rápido a muchos modelos y proveedores, facturación centralizada y disponibilidad de fallback.

```text
Blocage persistant
→ extraire le contexte minimal utile
→ OpenRouter
   ├── GLM
   ├── Kimi
   ├── Gemini
   ├── Grok
   └── nouveau modèle à tester
→ comparer l'analyse avec Claude / Codex
→ humain arbitre
```

**No conduzcas automáticamente el trabajo diario hacia OpenRouter.** La elección del modelo de rescate debe seguir siendo explícita: el objetivo es precisamente obtener otra perspectiva, no dejar que un router elija silenciosamente una familia diferente.

<!-- section: s-38 -->
#### Fallbacks: provider sí, modelo no predeterminado

OpenRouter puede cambiar automáticamente entre providers. Para esta guía, distingue dos niveles:

```text
Même modèle, provider A indisponible
→ même modèle, provider B
→ OUI : résilience sans changer la nature du reviewer

GLM indisponible
→ Gemini
→ Kimi
→ Grok
→ NON par défaut : le changement de modèle doit rester visible et intentionnel
```

Por lo tanto, para una investigación técnica, siempre se registra ** el modelo realmente utilizado**. Un fallo intermodelo puede ocultar la razón por la que una conclusión difiere de Claude o Codex.

<!-- section: s-39 -->
#### Qwen local: permanece directo

No añade OpenRouter únicamente para uniformar Qwen. `llama.cpp`, MLX o el arness local ya pueden exponer un endpoint OpenAI-compatible. Mientras sólo haya uno o dos modelos locales, la capa adicional no aporta suficiente valor:

```text
Qwen local
→ llama-server / MLX
→ Qwen Code / OpenCode / script local
```

<!-- section: s-40 -->
#### Confidencialidad con un agregador

Los proveedores accesibles a través de OpenRouter pueden tener diferentes políticas de retención. Para código profesional sensible:

```text
- ne jamais envoyer le repository entier par défaut ;
- préférer un reproducer minimal, quelques types/méthodes, la stack trace et le test ciblé ;
- anonymiser le contexte métier si possible ;
- choisir explicitement les providers compatibles avec les exigences de rétention du projet ;
- garder le code le plus sensible en local ou chez les fournisseurs directs déjà approuvés.
```

<!-- section: s-41 -->
### Metricos para logger

El router debe ser ajustado a datos reales, no a intuición. Para cada tarea de agente, el clog:

```text
task_type
risk
difficulty
decision_layer
decision_confidence
decision_threshold
decision_overridden
model_used
effort_level
fallbacks
parallel_sessions_peak
subagent_count
subagent_tokens
input_tokens
output_tokens
cost_usd
duration
files_changed
diff_lines
tests_run
tests_passed
review_findings
human_rework
merged_or_reverted
time_to_deploy
human_active_minutes
review_queue_minutes
review_true_positives
review_false_positives
review_missed_defects
quota_consumed_by_role
production_regressions
rollback_or_hotfix
```

Después de dos semanas, ajusta los umbrales:

```text
- si Qwen échoue souvent sur un type de tâche, route directement vers Sonnet ;
- si Sonnet réussit sans retours review sur un type de tâche, évite Opus ;
- si Opus réduit fortement les boucles de correction, garde-le pour cette classe ;
- si Opus `xhigh/max` suffit là où tu envoyais Fable, redescends ;
- si Fable ne produit pas moins de reprises humaines, réserve-le aux vraies sessions longues ;
- si `max` ne trouve que des remarques optionnelles, redescends vers `high` ou `medium`.
```

<!-- section: s-42 -->
### Prompt router minimum (fallback generativo)

Sí. Jev está disponible y las salidas están cerradas, prefiero `Choice` / `Score` / `Noul` Atómicos y luego combina los resultados en código. El prompt siguiente sigue siendo útil cuando se requiere un razonamiento abierto o como baseline de comparación.

```text
Tu es un routeur de tâches de développement logiciel pour un projet Scala/Java/Play/Spark.

Analyse la demande ci-dessous et retourne uniquement du JSON valide.

Objectif : choisir le plus petit modèle capable de produire un résultat mergeable avec un risque acceptable.

Prends en compte :
- type de tâche ;
- difficulté ;
- risque métier ;
- taille probable du diff ;
- nombre probable de fichiers ;
- besoin d'écriture ;
- besoin de docs externes ;
- risque Scala spécifique : implicits, givens, effets, sérialisation JSON ;
- fichiers critiques : build.sbt, migrations DB, auth, sécurité, concurrence, argent ;
- modèle, effort et, si nécessaire, mode `pro` ou multi-agent (`ultra` côté produit) ;
- plafond de coût et de durée ;
- règle d'escalade ;
- conditions d'arrêt.

Les signaux déterministes (fichiers critiques, taille de diff) priment sur ta propre confidence.

Demande :
[COLLER LA DEMANDE]

Contexte disponible :
[COLLER FICHIERS, STACK TRACE, DIFF STAT OU RÉSUMÉ]
```

<!-- section: s-43 -->
### Principio rector del enrutamiento

```text
Le routeur ne choisit pas le modèle le plus intelligent.
Il choisit le modèle le moins cher capable de produire un diff mergeable,
avec une règle d'escalade explicite dès que le risque ou l'incertitude augmente.
```

<!-- section: s-44 -->
## Impacto en el presupuesto mensual

*(orden relativo indicativo a partir de las tarifas API estándar; la suscripción y cuota no se convierten mecánicamente en dólares API)*

| Modelo              |           Precio API input/output / M | Recomendación de volumen                                                                          |
|---------------------|------------------------------------:|---------------------------------------------------------------------------------------------------|
| Qwen local          |                                   0 | Preanálisis y tareas seguras en volumen                                                             |
| **Jev 1.14**        | **$0.042/M input ; output gratis** | Decision layer: clasificación, routing, escoring y selección de skills de alta frecuencia        |
| **GPT‑6 Luna**      |                   **$0.10 / $0.50** | Micro-dev Codex, workers, clasificación, pruebas simples                                                   |
| **Haiku 5.5**       |                   **$0.10 / $0.50** | Subagentes, clasificación ; nivel ×5 si input > 100K; esfuerzo `medium` Configurable                        |
| **GPT‑6.2 Sol**     |                        **$2 / $10** | Falta Codex agente; excelente punto de rendimiento antes de Astra                                 |
| **Sonnet 5.5**      |                        **$2 / $10** | Falta de micro-dev Claude; `medium` para agente coding bien especificado                              |
| **Opus 5.5**        |                        **$4 / $20** | Falta de Claude agente a `medium` `high` para tareas difíciles                             |
| **GPT‑6.2 Astra**   |                        **$8 / $40** | Escalada de capacidad ; comenzar en Light                                                          |
| **Fable 5.2**       |                        **$8 / $40** | Frontier Claude; comenzar en Low durante una escalada de capacidad                                 |
| Extra / Max / Ultra |                            variable | Usar sólo después de la medición: más esfuerzo no es sinónimo de mejor coste por tarea terminada |

> **El precio por token no es el TCO.** Evalua también Fable 5.2 `low` sobre tareas limitadas y verificables: puede costar menos por tarea resuelta
> que un modelo inferior que busque , relee y backtracke más; viceversa , Opus 5.5 `medium` puede alcanzar la
> la misma calidad que Fable en algunos workloads para una fracción del coste. Por lo tanto, el benchmark local debe medir
> **costo por cambio aceptado**, reproducidos y minutos humanos.

<!-- section: s-45 -->
## Regla anti-créditos quemados

No lances Fable 5.2, GPT‑6.2 Astra, Opus 5.5 `Extra/Max` o un modo `Ultra` costoso que si usted puede proporcionar:

```text
- objectif précis ;
- contraintes ;
- fichiers ou modules probables ;
- critères d'acceptation ;
- tests à exécuter ;
- non-objectifs ;
- limite explicite de diff ;
- plafond de coût et de durée ;
- règle d'arrêt.
```

Un modelo muy fuerte en un rápido borrón no produce un buen resultado: produce una deriva más cara.

> **Limitaciones de ejecución en lugar de disciplina por sí sola.** Varios ajustes Claude Code Transforman esta regla en
> guardafuegos: `maxEffortLevel` limita el esfuerzo a todos los proveedores; una regla deny que apunta a un parámetro de herramienta
> (por ejemplo, `Agent(model:opus)`) prohíbe lanzar un subagente a un modelo caro; `CLAUDE_CODE_SUBAGENT_MODEL`
> fija el modelo de los subagentes; `fallbackModel` lista hasta tres modelos de retroceso probados en orden (a
> periodizar, véase supra); `/usage` ventila el consumo por skill, subagente, plugin y servidor MCP ; y
> hooks ven el esfuerzo corriente vía `$CLAUDE_EFFORT`. Lado API, las **Grupo de presupuesto** (beta
> `task-budgets-2026-03-13`, `output_config.task_budget`) dan al modelo un presupuesto de tokens para todo el bucle
> Agente: Es un presupuesto. **indicativo**, no un techo, que debe ser duplicado con un `max_tokens` y un techo
> lado cliente; su valor es parte de la rápida rendición, por lo que cambiarla rompe la caché. Verifica en la doc la lista
> Modelos que se soportan antes de usarlo en Fable 5.2 o Opus 5.5.

<!-- section: s-46 -->
#### Checklist pre-flight antes de cualquier tarea > $2 de costo estimado

Antes de iniciar Fable 5.2, GPT‑6.2 Astra, Opus 5.5 con esfuerzo alto o una sesión multiagente, valida este checklist. Cada casilla sin marcar es una razón para NO iniciar y bajar en modelo o scope.

□ Objetivo formulado en 1 frase con verbo de acción □ No objetivos explícitos (al menos 2) □ Archivos y módulos pertinentes identificados (vías exactas) □ Criterios de aceptación de prueba definidos □ Orden de prueba dirigida lista para ejecutar □ Diff máximo aceptable fijado (por ejemplo: < 300 líneas) □ Límite máximo de costo fijado (por ejemplo: $5) y límite de duración (por ejemplo: 30 min) □ Regla de parada formulada ("detener si [condición]") □ El plan ha sido validado por el humano ANTES del modo write □ Worktree dedicado creado si la tarea toca > 5 archivos □ Contexto mínimo preparado (no hay "toda la repos")

Estimación de los costes rápidos (orden de magnitud):

| Tarea               | Modelo      | Tokens estimados      | Costo estimado |
|---------------------|-------------|---------------------|-------------|
| Feature 3 archivos  | Sonnet 5.5  | ~20K in / ~5K out   | ~$0.09      |
| Bug de múltiples módulos   | Opus 5.5    | ~50K in / ~10K out  | ~$0.40      |
| Migración marco de trabajo | Fable 5.2   | ~200K in / ~50K out | ~$3.60      |
| Auditoría Astra max     | GPT‑6.2 Astra | ~100K in / ~20K out | ~$1.60      |

Si el coste estimado supera 3x el coste del modelo inferior para la misma tarea, la diferencia de calidad debe justificarse por el riesgo. "Más inteligente" no es una justificación.
---

