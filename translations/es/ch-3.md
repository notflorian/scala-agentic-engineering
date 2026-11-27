<!-- section: chapter -->
# 3. Selección y asignación de modelos

<!-- section: s-1 -->
## Regla simple

```text
Qwen / Haiku preparan y filtran.
Microdesarrollo bajo estrecho control humano → GPT‑6 Luna High o Sonnet 5.5 Medium.
Programación agéntica de principio a fin → GPT‑6.2 Sol Medium u Opus 5.5 Medium.
Depuración / arquitectura difíciles → Opus 5.5 High o GPT‑6.2 Sol High.
Caso puntual de máxima exigencia → GPT‑6.2 Astra Light o Fable 5.2 Low antes de llevar a ciegas al máximo el esfuerzo del modelo inferior.
Un solo agente que escribe por worktree.
La otra familia de modelos revisa o cuestiona, sin duplicar automáticamente todo el proceso.
Ultra / varios agentes solo cuando los subproblemas son realmente independientes.
IntelliJ valida.
Tú decides.
```

El enrutamiento debe minimizar el **costo de la tarea terminada**, no el precio de la primera apelación:

```text
carga total esperada
= exploración + implementación + verificación
+ probabilidad de retrabajo × coste del retrabajo
+ coste de coordinación
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
> Q4_K_M  → opción predeterminada para tener el máximo margen: IDE, sbt y varias JVM siguen funcionando con holgura.
> Q5_K_M  → opción predeterminada recomendada: mejor equilibrio entre calidad y memoria en esta máquina.
> Q6_K    → opción de alta calidad: viable si las otras aplicaciones mantienen un consumo razonable.
> Q8_0    → opción de evaluación: posible, aunque con menos margen y con una ventaja por demostrar frente a Q5/Q6.
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
> Opus 5.5 High insuficiente (capacidad)   → Fable 5.2 antes de Opus 5.5 Max, a medir en el benchmark privado de Scala
> Decisión difícil puntual (asesor)       → Fable 5.2 low/medium
> Misión autónoma larga                   → Fable 5.2 high (low/medium suelen dar por terminado el turno demasiado pronto)
> Tarea acotada, error de UI/frontend o revisión habitual → Opus 5.5 o Sonnet 5.5 siguen ofreciendo mejor relación calidad-precio
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
llamadas asíncronas a herramientas
→ seguir razonando o llamar a otras herramientas mientras se ejecuta una herramienta lenta

ajustes durante el turno
→ añadir una restricción o cambiar de rumbo sin reiniciar toda la tarea

actualizaciones de configuración
→ cambiar el esfuerzo durante la ejecución sin invalidar innecesariamente el prefijo de caché
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
GPT‑6 Luna High = microdesarrollo y workers de Codex bajo estrecho control humano.
GPT‑6.2 Sol Medium = opción predeterminada de Codex para programación agéntica de principio a fin.
GPT‑6.2 Sol High = funcionalidad compleja, migración y retrabajo difícil.
GPT‑6.2 Astra Light = escalado de capacidad antes de llevar automáticamente Sol al esfuerzo extremo.
Sonnet 5.5 Medium = microdesarrollo con Claude y tareas agénticas bien especificadas.
Opus 5.5 Medium = opción predeterminada de Claude para programación agéntica autónoma.
Opus 5.5 High = arquitectura, depuración y refactorizaciones difíciles.
Fable 5.2 Low = escalado al nivel más alto cuando Opus High sigue siendo insuficiente.
Astra frente a Fable = decidir según el coste por cambio aceptado, sin guiarse por el precio por token.
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
Microdesarrollo interactivo con participación humana
→ GPT‑6 Luna High o Sonnet 5.5 Medium

Incidencia habitual de principio a fin
→ GPT‑6.2 Sol Medium
→ Opus 5.5 Medium para la revisión independiente

Arquitectura / causa raíz / refactorización difícil
→ Opus 5.5 High
→ GPT‑6.2 Sol Medium/High para cuestionar la propuesta

Sol High se queda corto por un límite de capacidad
→ GPT‑6.2 Astra Light y después Medium si hace falta

Opus High se queda corto por un límite de capacidad
→ Fable 5.2 Low y después Medium si hace falta

Misma tarea de máxima exigencia, decisión entre Astra y Fable
→ dos worktrees / misma especificación / mismas pruebas
→ comparar el coste total + minutos de trabajo humano + calidad del diff
→ decisión humana
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
✅ Revisión a gran escala y triaje de bajo riesgo → GLM‑5.2 (High): precio por token muy inferior al de Opus, pero queda por medir el coste por tarea
✅ Extracción, clasificación y resúmenes de PR en volumen → GLM‑5.2 o Kimi K3, por lotes cuando el volumen encarezca Sonnet/Terra
✅ Generación de frontend / prototipo web → Kimi K3 (#1 Frontend Code Arena) si sales del alcance de Scala puro
✅ Segunda opinión independiente con pesos abiertos → un modelo de una 3e escuela de entrenamiento reduce los puntos ciegos que comparten Claude/GPT
✅ Código sensible / aislamiento de red / soberanía → GLM‑5.2 autoalojado (pesos MIT): nada sale de tu infraestructura
```

```text
❌ Modelo principal para Scala a diario en lugar de Sonnet 5.5: capaz, pero pierdes el ecosistema (Claude Code, subagentes, Metals MCP maduros)
❌ Tarea interactiva corta en Kimi K3 con el esfuerzo máximo: latencia y verbosidad, mala compra; usar low/high
❌ Decisión crítica de arquitectura en solitario: mantener Opus/Fable o buscar una segunda opinión real con Sol; un modelo de pesos abiertos sigue siendo una alternativa, no el árbitro
❌ «Sustituir» Qwen local: categoría equivocada (véase el error anterior)
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
3 errores sutiles de Scala 3: givens, implicits, varianza, tipos opacos
3 cambios en Play / Tapir / Pekko en entre 3 y 8 archivos
3 tareas de Spark / concurrencia / rendimiento
3 revisiones de PR con defectos conocidos introducidos expresamente
3 tareas de pruebas: ScalaTest, ScalaCheck, pruebas de mutación
```

Protocolo: mismo commit, mismo worktree inicial, mismas herramientas, mismo límite de tiempo, misma red, mismo paquete de contexto, mismos criterios de parada y **tres repeticiones por tarea**. Kimi debe ser probado por separado en `high` y `max`; GLM `High` y `Max`. Si los arneses no pueden ser idénticos, publica dos matrices y no asigna la diferencia al modelo.

Medidas obligatorias:

```text
- tarea aceptada por las pruebas y por la revisión humana;
- compilación, pruebas específicas y puntuación de mutación;
- defectos de seguridad o de contrato detectados;
- líneas añadidas / eliminadas y archivos afectados;
- número de reintentos, llamadas a herramientas y ciclos idénticos;
- tokens de entrada, caché, razonamiento y salida;
- coste total de API, latencia y minutos de trabajo humano hasta el merge;
- tasa de éxito pass@1 y estabilidad en tres ejecuciones.
```

Aproba GLM o Kimi en un flujo sólo si reduce el coste por cambio aceptado **sin** Degradar los guardaespaldas. Una puntuación editor superior pero más correcciones humanas es una regresión, no una ganancia.

<!-- section: s-17 -->
## Regla de decisión por tarea

<!-- section: s-18 -->
### Cuando utilice **Fable 5.2** (Mythos-class)

Fable 5.2 cuesta dos veces Opus 5.5 por token ($8/$40 contra $4/$20). Anthropic recomienda comenzar con **Opus 5.5 `medium`**, subir hacia `high`y luego reservar Fable 5.2 para una escalada de capacidad, prueba **Fable `low`** antes de empujar Opus sistemáticamente a `Extra`/`Max` :

```text
✅ Migración completa de un framework (Play 2 → 3, Pekko, actualización de Spark)
✅ Sesión autónoma de varias horas / varios días sin supervisión
✅ Refactorización entre módulos que afecta a > 10 archivos interdependientes
✅ Depuración de un error de negocio cuya causa está muy alejada del síntoma
✅ Decisión arquitectónica sin una «respuesta correcta evidente» después de probar Opus 5.5 High
✅ Tarea por la que, de otro modo, pagarías media jornada a un ingeniero sénior
```

```text
❌ Tarea de alcance claro y acotado: Sonnet 5.5 u Opus 5.5 ofrecen mejor relación calidad-precio
❌ Revisión de diff o resumen de PR: excesivo y costoso sin necesidad
❌ Generación de código repetitivo o fixtures: basta con Qwen o Haiku
❌ Cambio de una línea o parche específico: Luna High, Sonnet 5.5 Medium o Aider
❌ Tarea difícil pero interactiva y con tu participación: suele bastar con Opus 5.5 Medium/High
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
# MISIÓN (estática, no modificar durante la sesión)
Objetivo: [migración / refactorización concreta]
Fuera de alcance: [lo que se excluye explícitamente]
Invariantes: API públicas, contratos JSON y comportamientos enumerados en AGENTS.md
Duración máx.: [N horas] — Coste máx.: [N USD] — Diff máx. por hito: [N líneas]

# REGLAS DE PARADA (estáticas)
Detenerse e informar de inmediato si:
- es necesario infringir un invariante para avanzar;
- el mismo hito falla 2 veces por causas diferentes;
- debe cambiar build.sbt, una migración de base de datos o un contrato público;
- la duración restante estimada supera 2x la estimación inicial.

# PROTOCOLO (estático)
1. Leer AGENTS.md y MIGRATION_STATE.md.
2. Resolver UN hito: plan breve → diff → compilación → pruebas específicas.
3. Actualizar MIGRATION_STATE.md y registrar el hito en un commit.
4. Informe de progreso: hito completado, hitos pendientes, nuevos riesgos y desviaciones del plan.
5. Volver al paso 2.

# ESTADO (dinámico, adjuntar la versión actual de MIGRATION_STATE.md)
[estado]
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
✅ Incidencia completa cuando Claude se ocupa de todo el proceso: exploración → parche → pruebas
✅ Arquitectura, migración y planificación entre módulos
✅ Causa raíz alejada del síntoma, implicits/givens/efectos difíciles
✅ Refactorización amplia donde la coherencia global importa más que la edición puntual
✅ Revisión independiente de una PR escrita por Codex
✅ Orquestación de subagentes intensivos en lectura con contexto aislado
```

```text
medium → opción agéntica predeterminada
high   → depuración / arquitectura / trabajo complicado de largo recorrido
Extra  → >30 min y una secuencia realmente larga; no para una simple tarea «importante»
Max    → excepcional, máxima prioridad a la calidad y mejora medida
```

<!-- section: s-21 -->
### Cuando utilice **Sonnet 5.5**

La mejor opción Claude cuando **el senior mantiene fuerte la mano** o cuando la tarea de agente esté bien especificada. Anthropic recomienda explícitamente `medium` para el coding agente y el uso multistep de herramientas bien articuladas, luego `high` para tareas más largas o difíciles.

```text
✅ Error pequeño y reproducible
✅ Refactorización local con alcance bien delimitado
✅ Pruebas de negocio y pruebas basadas en propiedades específicas
✅ Traza de ejecución → diagnóstico → corrección
✅ Funcionalidad clara cuya arquitectura ya se ha decidido
✅ Worker de implementación que sigue un plan humano o de Opus
```

```text
low    → transformación simple / prioridad a la latencia
medium → opción predeterminada para microdesarrollo y programación agéntica bien especificada
high   → tarea más larga o más difícil
Extra / Max → solo si tus evaluaciones muestran una mejora; si no, pasar a Opus 5.5
```

Por lo tanto, la regla económica ya no es la de Sonnet con el máximo esfuerzo antes de Opus. Si Sonnet High falla por un límite de capacidad, **Opus Medium** es a menudo una mejor compra que un Sonnet Extra/Max prolongado.

<!-- section: s-22 -->
### Cuando utilice **Haiku 5.5**

Sistemáticamente para tareas *alta frecuencia y bajo riesgo* :

```text
✅ Subagentes de lectura o extracción de bajo riesgo (salida verificable)
✅ Resúmenes rápidos de logs y PR
✅ Clasificación y enrutamiento
✅ Cambios específicos de < 20 líneas
✅ Generación de mensajes de commit
✅ Llamadas repetitivas de bajo riesgo, si el benchmark confirma la mejora
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
✅ Microdesarrollo: modificación local cuya dirección controlas
✅ Pruebas simples, fixtures, código repetitivo, renombrados y transformaciones mecánicas
✅ Búsqueda de apariciones, resúmenes, logs y resúmenes de PR
✅ Worker/subagente cuya salida se verifica de inmediato
```

OpenAI recomienda comenzar Luna a **High**. No intentes convertir Luna en un agente fronterizo con Extra High: si la tarea se convierte en ambigua o conceptual, pasa a Sol 6.2 en lugar de pagar largas veces en un modelo demasiado pequeño.

<!-- section: s-24 -->
### Cuando utilice **GPT‑6.2 Sol**

```text
✅ Incidencia habitual de principio a fin: exploración → implementación → pruebas → PR
✅ Funcionalidad que afecta a varios archivos y error no trivial
✅ Revisión independiente de una PR escrita por Claude
✅ Migración acotada, compatibilidad y refactorización transversal
✅ Segunda opinión rigurosa sobre una arquitectura propuesta por Opus
```

```text
Light       → incidencia muy bien especificada, parche local, reproducción clara
Medium      → opción agéntica predeterminada para el trabajo diario
High        → funcionalidad compleja, causa raíz difícil, migración, muchos casos límite
Extra High  → capacidad suficiente, pero con necesidad real de más análisis o verificación
Ultra       → solo si el trabajo puede dividirse en investigaciones independientes
```

<!-- section: s-25 -->
### Cuando utilice **GPT‑6.2 Astra**

```text
✅ Sol High falla por falta de capacidad o criterio, sin que el contexto esté contaminado
✅ Seguridad, autenticación, contrato crítico o decisión en la que un rumbo equivocado obliga a rehacer el trabajo varias veces
✅ Flujo de principio a fin muy ambiguo, con muchas herramientas o uso directo del ordenador
✅ Revisor puntual de máxima capacidad para una decisión de gran impacto
```

Comienza con **Astra Light**. Para una tarea realmente fronteriza, Astra Light puede costar menos que un Sol Extra High, seguido de una recuperación, porque evita una mala trayectoria. Sube a Medium/High sólo si es necesario; Extra High/Ultra siguen siendo excepcionales.

<!-- section: s-26 -->
### Cuándo usar **el modo `ultra` en ChatGPT Work / Codex**

```text
✅ Mapa integral de la base de código de una aplicación heredada
✅ Migración entre módulos en un worktree dedicado
✅ Auditorías paralelas de arquitectura + pruebas + seguridad + rendimiento
✅ División de una refactorización en micro-PR
✅ Tarea donde varios análisis independientes aportan valor real
```

```text
❌ Petición aislada de «reescríbelo bien»
❌ Tarea interactiva corta
❌ Repositorio con pocas pruebas y sin límite de diff
❌ Modificación directa de archivos críticos sin un plan validado
```

En esta subsección, `ultra` nombre **modo de orquesta multi-agente del producto**, y no el nivel de esfuerzo `ultra` que algunos SDK Codex Ahora es adecuado para las persianas independientes; evitalo cuando los agentes escriben en el mismo estado mutable o cuando una única operación lenta domina la tarea. En una aplicación legacy, comienza por cartografiar, producir un registro de deuda, proponer pruebas de caracterización y luego cortar en microPRs. No comienza por escribir código.

Gálibo mínimo para una misión `ultra` :

```text
Actúas como equipo de revisores y agentes para una aplicación Scala heredada.

Roles que debes simular:
- arquitecto de sistemas heredados;
- líder técnico de Scala;
- revisor de seguridad defensiva;
- responsable de QA / ingeniero de pruebas;
- mantenedor escéptico.

Objetivo:
[objetivo preciso]

Restricciones:
- no cambiar comportamientos observables sin validación;
- detenerse antes de modificar build.sbt / migraciones de base de datos / contratos JSON públicos;
- micro-PR con menos de 300 líneas modificadas;
- pruebas de caracterización antes de refactorizar;
- cada conclusión debe citar los archivos examinados;
- distinguir hechos, hipótesis y recomendaciones.

Salida esperada:
1. mapa del alcance;
2. riesgos;
3. registro de deuda técnica;
4. pruebas de caracterización prioritarias;
5. plan dividido en micro-PR;
6. primera PR propuesta, sin aplicarla hasta que se valide el plan.
```

<!-- section: s-27 -->
## Matriz de selección modelo rápido

```text
Microdesarrollo bajo control humano       → GPT‑6 Luna High / Sonnet 5.5 Medium
Worker de lectura / triaje de bajo riesgo → Haiku 5.5 / Qwen local / GPT‑6 Luna
Parche local que requiere criterio medio  → GPT‑6.1 Terra Medium
Incidencia habitual de principio a fin   → GPT‑6.2 Sol Medium
Agente Claude de principio a fin          → Opus 5.5 Medium
Funcionalidad / error difícil             → GPT‑6.2 Sol High u Opus 5.5 High según el caso
Predomina la arquitectura / causa raíz   → Opus 5.5 High
Revisión cruzada                          → familia distinta a la del autor, Medium por defecto
Seguimiento de PR con Codex               → GPT‑6.2 Sol Medium (Goal / Heartbeat / Cloud)
Sol High insuficiente                     → GPT‑6.2 Astra Light
Opus High insuficiente                    → Fable 5.2 Low
Tarea secuencial de largo recorrido > 30 min → Opus 5.5 Extra (`xhigh`)
Base de código completa, trabajo paralelo → GPT‑6.2 Sol Ultra, sobre todo para tareas intensivas en lectura
Máxima exigencia                          → Astra Medium+ / Fable Medium+ una vez demostrada la necesidad
```

Regla práctica:

```text
El sénior dirige el trabajo → modelo rápido y económico.
El agente se ocupa de todo el proceso → Sol 6.2 u Opus 5.5.
Comprender importa más que escribir el parche → priorizar Opus.
Predomina la ejecución de principio a fin → priorizar Sol 6.2.
Aparece un límite de capacidad → Astra Light o Fable Low antes de llevar al extremo el esfuerzo del modelo inferior.
Ultra solo si el problema contiene varios frentes realmente independientes.
```

<!-- section: s-28 -->
## Ruta automática de las tareas de desarrollo

La matriz de selección no debe permanecer sólo manual. Para evitar quemar créditos en tareas simples o, a la inversa, enviar una tarea crítica a un modelo demasiado débil, añade un paso explícito de enrutamiento antes de cada tarea de agente.

El principio no es elegir el modelo más inteligente, sino el modelo más pequeño capaz de producir un resultado mergeable con un riesgo aceptable.

```text
Solicitud / ticket / traza de ejecución
→ clasificación de la tarea
→ estimación de dificultad + riesgo
→ selección del modelo mínimo aceptable
→ ejecución con permisos limitados
→ pruebas deterministas
→ escalado si falla
→ registro de coste / calidad
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
→ registro de coste y calidad
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
✅ clasificación de tareas, riesgos y dificultad
✅ enrutamiento de modelos: Luna / Sol / Astra / Sonnet / Opus / Fable
✅ selección gradual de algunas skills dentro de un catálogo amplio
✅ triaje de resultados de subagentes y evaluación de la pertinencia del contexto
✅ señal de cambio de tema / «¿conviene plantearse una compactación?»
✅ filtrado de notificaciones y decisiones que merecen atención humana

❌ escribir o explicar Scala
❌ problemas abiertos de arquitectura o de causa raíz
❌ cálculo, recuento o comparación de fechas
❌ decidir en solitario sobre un push, despliegue, eliminación, secreto o migración de base de datos
```

Arquitectura recomendada:

```text
reglas deterministas
→ Jev para una decisión cerrada y frecuente
→ el código combina probabilidades y umbrales
→ LLM generativo si el razonamiento es abierto o la confianza insuficiente
→ intervención humana si la acción es crítica o irreversible
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
Ciclo breve verificable: Qwen / Haiku / GPT‑6 Luna High / Sonnet 5.5 Medium
→ el agente se encarga de la tarea: GPT‑6.2 Sol Medium / Opus 5.5 Medium
→ dificultad: Sol High / Opus High
→ límite de capacidad: Astra Light / Fable Low
→ aumentar el esfuerzo solo si la capacidad basta pero falta razonamiento
→ Ultra solo si se puede paralelizar
→ intervención humana
```

**No cambies de modelo en medio de una conversación que se desvíe.** Si el fracaso viene de una trayectoria contaminada  la hipótesis falsa repetida, alucinaciones que se acumulan, correcciones que recrean otros errores  la situación es en sí misma parte del problema. Sonnet 5.5 → Opus 5.5, Sol 6.2 → Astra o Opus 5.5 → Fable 5.2 :

```text
1. Detener el modo de escritura.
2. Preparar HANDOFF.md: objetivo, estado del diff, hechos verificados, intentos fallidos, error actual e incógnitas.
3. Abrir una sesión nueva únicamente con la especificación + AGENTS.md + HANDOFF.md + archivos/diff pertinentes.
4. Subir de modelo en esta nueva sesión si la dificultad aún lo justifica.
```

La escalada de **capacidad** es útil sobre un problema propiamente dicho; no debe transportar la deuda conversacional de una sesión ya sesgada.

Escalada automática si:

```text
- aparece una señal determinista crítica (touches_* sensible, diff fuera de los límites previstos);
- confianza declarada por el LLM < 0.75 o confianza de Jev por debajo del umbral calibrado para esa decisión;
- el mismo error de compilación aparece 2 veces;
- una prueba específica sigue fallando tras 2 correcciones;
- diff fuera del alcance;
- se modifican más archivos de los previstos;
- más de 300 líneas de diff imprevistas;
- se ve afectado build.sbt, plugins.sbt, una migración de base de datos o un contrato JSON público;
- se modifica la API pública;
- el enrutador detecta un asunto de seguridad, concurrencia, rendimiento o dinero;
- el modelo declara explícitamente una incertidumbre alta;
- el coste estimado de un error supera el del modelo superior.
```

Interromps (sin escalar automáticamente) si:

```text
- se alcanza max_cost_usd (presupuesto local);
- se alcanza max_duration_minutes (límite de tiempo real):
  una sesión agéntica que entra en bucle falla de forma distinta a una que termina con un error,
  y recurrir a un modelo más caro no corrige un bucle.
```

Desacelerar automáticamente si:

```text
- tarea puramente textual;
- no requiere modo de escritura;
- sin riesgo de negocio;
- se esperan menos de 20 líneas;
- un solo archivo;
- objetivo determinista;
- prueba existente muy específica;
- contexto estable y conocido del proyecto.
```

<!-- section: s-34 -->
### Normas de no automatización

Nunca dejes que un router decida por sí solo sobre una escritura en:

```text
- build.sbt;
- plugins.sbt;
- resolvers;
- versiones de dependencias;
- migraciones de base de datos;
- contratos JSON públicos;
- seguridad;
- autenticación;
- autorización;
- concurrencia;
- gestión de dinero;
- eliminación de datos;
- scripts de despliegue o infraestructura.
```

En estos casos, el router sólo podrá proponer:

```text
- modelo recomendado;
- plan;
- archivos probables;
- pruebas que ejecutar;
- riesgos;
- regla de parada.
```

<!-- section: s-35 -->
### Subagentes Claude Code Recomendaciones

**Calibración Codex 6.2.** Para un pariente GPT‑6.2 Sol o Astra, ve con el mismo modelo y el mismo esfuerzo para los subagentes (recomendación oficial OpenAIA continuación, reduce el tier de las tareas verdaderamente mecánicas, de salida controlable: Luna/Haiku para grep, extracción, logs y resúmenes; Sol/Opus para invariantes, arquitectura y root causa. El mismo principio de medida vale lado Claude. Un revisor de la otra familia sigue siendo una sesión independiente, no un worker menos costoso del autor.

Claude Code es el mejor lugar para aplicar este enrutamiento a diario, ya que los subagentes pueden tener su propio contexto, herramientas y permisos.

```text
researcher
- Modelo: Haiku / Qwen si es externo
- Modo: read-only
- Función: encontrar archivos, usos, pruebas y documentación

scala-implementer
- Modelo: Sonnet 5.5 `medium`
- Modo: escritura limitada al repositorio
- Función: implementar tareas acotadas siguiendo un plan claro

hard-debugger
- Modelo: Opus 5.5 `high`
- Modo: escritura limitada, plan obligatorio
- Función: errores sutiles de Scala, implicits, efectos y causas alejadas del síntoma

migration-planner
- Modelo: Opus 5.5 `high`; Fable 5.2 `low` (decisión puntual) o `high` (tarea larga) si Opus llega a su límite
- Modo: plan primero, worktree dedicado
- Función: migraciones entre módulos, refactorizaciones largas y estrategia de división
- Nota: evaluar Dynamic Workflows (Opus 5.5 + muchos subagentes en paralelo)
  como alternativa a usar Fable como único agente en migraciones de toda la base de código

reviewer
- Modelo: Codex / GPT‑6.2 Sol `medium`; Astra `light` si es crítico
- Modo: no-write
- Función: revisión independiente y clasificación en bloqueante / importante / opcional

pr-summarizer
- Modelo: Qwen / GPT‑6 Luna
- Modo: no-write
- Función: resumen de PR, notas de versión y lista de comprobación final
```

<!-- section: s-36 -->
#### Aislamiento de contexto: el papel principal de los suboficiales en las tareas prolongadas

La ganancia de los subagentes no es sólo el paralelismo. Cada subagente trabaja en una **ventana de contexto fresco y aislado** ; el padre no necesita, por tanto, acumular las búsquedas, logs, archivos desviados y sin salida de cada subtarea. Este aislamiento protege el contexto principal contra el *context rot*.

El reparto recomendado es:

```text
AGENTE PRINCIPAL
- objetivo
- restricciones y elementos fuera del alcance
- plan validado
- decisiones tomadas
- diff actual
- pruebas esenciales
- riesgos pendientes

SUBAGENTES
- exploración de numerosos archivos
- búsqueda con Sourcebot / rg
- rutas de llamada, jerarquías, usos y cadenas de givens con ScalaSemantic
- grafo estructural entre lenguajes con Codebase-Memory si coexisten Java/Kotlin/Scala
- investigación en directo de tipos / givens / diagnósticos con Metals
- documentación externa
- logs y conjuntos de pruebas voluminosos
- mapa de un módulo heredado
```

Regla de decisión:

```text
¿Le seguirán siendo útiles al agente principal los detalles de la subtarea cuando esta termine?

NO → subagente aislado
SÍ → mantener en el contexto del agente principal
```

El mensaje de delegación debe ser un **contrato**, ya que el subagente no debe depender de toda la conversación histórica del padre:

```text
Misión:
[alcance preciso]

Modo:
solo lectura / escritura acotada

Busca:
[preguntas concretas]

Evita:
[fuera del alcance]

Devuelve únicamente:
1. conclusión;
2. pruebas con formato file:line;
3. pruebas ejecutables o comandos pertinentes;
4. incertidumbres restantes.

Extensión objetivo de la respuesta: < 1–2K tokens.
```

La vuelta es una interfaz, no una transcripción. Si un subagente cama 80K tokens y devuelve 1,5K, el aislamiento es útil; si lo lee 10K y devuelve 8K, ha movido sobre todo el ruido. Una métrica sencilla a seguir en las tareas largas es:

```text
isolation_ratio
= tokens consumidos por el subagente
/ tokens devueltos al agente principal
```

Así que el buen pattern es **Map → reduce** : varios workers especializados gastan el contexto local, luego el padre sintetiza algunos resultados cortos. Evita el anti-pattern reverse *context rot* en el contexto raíz.

Para **tu workflow solo Scala**, trata también al fan-out como un presupuesto de tokens/competidores:

```text
por defecto                         → 1 agente activo
2 investigaciones independientes    → 2 subagentes en modo de solo lectura
2 historias de usuario independientes → 2 agentes escritores como máximo al empezar (WIP incluye las PR en revisión)
3+ sesiones paralelas               → solo si se miden la ganancia y la capacidad de revisión
agente escritor                     → siempre 1 por rama / PR / worktree
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
Claude Code        → suscripción a Claude Max
Codex              → suscripción a ChatGPT
Qwen local         → MLX / llama.cpp / endpoint local
GitHub Copilot     → suscripción a GitHub Copilot
JetBrains AI       → suscripción a JetBrains AI
```

La necesidad API que queda es **excepcional** : cuando Claude Code y luego Codex permanecen bloqueados y quieres una opinión de otra familia de modelos, por ejemplo **GLM, Kimi, Gemini, Grok o un nuevo modelo para evaluar**. En ese caso, **OpenRouter es el mejor defecto** : una sola clave, ningún servidor que mantener, acceso rápido a muchos modelos y proveedores, facturación centralizada y disponibilidad de fallback.

```text
Bloqueo persistente
→ extraer el contexto mínimo útil
→ OpenRouter
   ├── GLM
   ├── Kimi
   ├── Gemini
   ├── Grok
   └── modelo nuevo que evaluar
→ comparar el análisis con Claude / Codex
→ decisión humana
```

**No conduzcas automáticamente el trabajo diario hacia OpenRouter.** La elección del modelo de rescate debe seguir siendo explícita: el objetivo es precisamente obtener otra perspectiva, no dejar que un router elija silenciosamente una familia diferente.

<!-- section: s-38 -->
#### Fallbacks: provider sí, modelo no predeterminado

OpenRouter puede cambiar automáticamente entre providers. Para esta guía, distingue dos niveles:

```text
Mismo modelo, proveedor A no disponible
→ mismo modelo, proveedor B
→ SÍ: resiliencia sin cambiar el modelo que revisa

GLM no disponible
→ Gemini
→ Kimi
→ Grok
→ NO por defecto: el cambio de modelo debe seguir siendo visible y deliberado
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
- nunca enviar el repositorio completo por defecto;
- preferir una reproducción mínima, unos pocos tipos o métodos, la traza de ejecución y la prueba específica;
- anonimizar el contexto de negocio cuando sea posible;
- elegir explícitamente proveedores compatibles con los requisitos de retención del proyecto;
- mantener el código más sensible en local o con proveedores directos ya aprobados.
```

<!-- section: s-41 -->
### Metricos para logger

El router debe ser ajustado a datos reales, no a intuición. Para cada tarea de agente, el clog:

```plaintext
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
- si Qwen falla con frecuencia en un tipo de tarea, enrutarlo directamente a Sonnet;
- si Sonnet resuelve un tipo de tarea sin observaciones en la revisión, evitar Opus;
- si Opus reduce mucho los ciclos de corrección, reservarlo para esa clase de tarea;
- si Opus `xhigh/max` basta donde antes usabas Fable, bajar de nivel;
- si Fable no reduce el retrabajo humano, reservarlo para sesiones realmente largas;
- si `max` solo encuentra observaciones opcionales, bajar a `high` o `medium`.
```

<!-- section: s-42 -->
### Prompt router minimum (fallback generativo)

Sí. Jev está disponible y las salidas están cerradas, prefiero `Choice` / `Score` / `Noul` Atómicos y luego combina los resultados en código. El prompt siguiente sigue siendo útil cuando se requiere un razonamiento abierto o como baseline de comparación.

```text
Eres un enrutador de tareas de desarrollo de software para un proyecto Scala/Java/Play/Spark.

Analiza la solicitud de abajo y devuelve únicamente JSON válido.

Objetivo: elegir el modelo más pequeño capaz de producir un resultado apto para fusionar con un riesgo aceptable.

Ten en cuenta:
- tipo de tarea;
- dificultad;
- riesgo de negocio;
- tamaño probable del diff;
- número probable de archivos;
- necesidad de escribir;
- necesidad de documentación externa;
- riesgo específico de Scala: implicits, givens, efectos, serialización JSON;
- archivos o áreas críticas: build.sbt, migraciones de base de datos, autenticación, seguridad, concurrencia y dinero;
- modelo, esfuerzo y, si hace falta, modo `pro` o multiagente (`ultra` en el producto);
- límite de coste y duración;
- regla de escalado;
- condiciones de parada.

Las señales deterministas (archivos críticos, tamaño del diff) prevalecen sobre tu nivel de confianza.

Solicitud:
[PEGA LA SOLICITUD]

Contexto disponible:
[PEGA ARCHIVOS, TRAZA DE EJECUCIÓN, ESTADÍSTICAS DEL DIFF O RESUMEN]
```

<!-- section: s-43 -->
### Principio rector del enrutamiento

```text
El enrutador no elige el modelo más inteligente.
Elige el modelo más barato capaz de producir un diff apto para fusionar,
con una regla de escalado explícita en cuanto aumenten el riesgo o la incertidumbre.
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
- objetivo preciso;
- restricciones;
- archivos o módulos probables;
- criterios de aceptación;
- pruebas que ejecutar;
- elementos fuera del alcance;
- límite explícito del diff;
- límite de coste y duración;
- regla de parada.
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

