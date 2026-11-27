<!-- section: chapter -->
# 3. Seleção e roteamento de modelos

<!-- section: s-1 -->
## Regra simples

```text
Qwen / Haiku preparam e filtram.
Microdesenvolvimento sob forte controle humano → GPT‑6 Luna High ou Sonnet 5.5 Medium.
Codificação agêntica de ponta a ponta → GPT‑6.2 Sol Medium ou Opus 5.5 Medium.
Depuração / arquitetura difíceis → Opus 5.5 High ou GPT‑6.2 Sol High.
Tarefa ocasional de fronteira → GPT‑6.2 Astra Light ou Fable 5.2 Low antes de elevar cegamente o esforço do modelo inferior ao máximo.
Um único agente com permissão de escrita por worktree.
A outra família de modelos revisa ou questiona o trabalho, sem repetir automaticamente todo o percurso.
Ultra / multiagente apenas quando os subproblemas são realmente independentes.
O IntelliJ valida.
Você decide.
```

O roteamento deve minimizar o **costo da tarefa terminada**, não o preço do primeiro recurso:

```text
esforço total esperado
= descoberta + implementação + verificação
+ probabilidade de retrabalho × custo do retrabalho
+ custo de coordenação
```

Portanto, um modelo mais caro pode ser a melhor compra se evitar uma exploração incorreta, vários diffs desnecessários e os riços de CI. Pelo contrário, um micro-bucle controlado por um idoso faz que Luna, Sonnet ou Haiku dominantes logo que o erro seja detectado em questão de minutos.

*Nunca delegar la actualización de las versiones en `build.sbt` Sin exigir que el agente interrogue primero a un MCP, Context7, Maven Central o la documentación oficial. Los nombres y versiones de las bibliotecas son exactamente el tipo de información que los modelos alucinan cuando trabajan fuera de contexto.*

<!-- section: s-2 -->
## Matriz de roteamento

| Tarea                                                    | Modo         | Agente principal recomendado                   | Segundo passo útil                           | Porquê?                                                                           |
|----------------------------------------------------------|--------------|----------------------------------------------|------------------------------------------------|------------------------------------------------------------------------------------|
| Resolve um módulo, grep, usos, logs simples            | Micro- dev    | **Haiku 5.5** ou Qwen local                  | Nenhuma salvo ambiguidade                           | Leitura de alta frequência, baixo risco                                             |
| Modificação mecânica precisa, boilerplata, renomeada   | Micro- dev    | **GPT‑6 Luna High[**                          | Sonnet 5.5 Medium se os tipos subtis             | Muito bom custo quando o humano mantém o endereço                                    |
| Escrever um teste simples de um comportamento conhecido   | Micro- dev    | **GPT‑6 Luna High[**                          | Sonnet 5.5 Medium se regra profissional rica        | Saída facilmente verificável                                                       |
| Stack rasto ou fissuras precisas                           | Micro- dev    | **Sonnet 5.5 Medium[**                        | Lua High para aplicar um adesivo borné        | Sonnet traz mais compreensão sem pagar Opus                               |
| Pequeno erro reproduzido, perímetro conhecido                     | Micro- dev    | **Sonnet 5.5 Medium[**                        | Luna High para testes/editar mecânica         | Brincos curtos, feedback imediato                                                 |
| Patch local, tipos ou invariantes não triviais            | Micro- dev    | **GPT‑6.1 Terra Medium[**                     | GPT‑6.2 Sol Medium se necessário explorar  | Terceiro intermediário a medir nos adesivos bornados |
| Pequeno refator local                                     | Micro- dev    | **Sonnet 5.5 Medium[**                        | Luna High para inspeção mecânica          | O maior conserva a arquitetura                                                  |
| Revisão dirigida de um pequeno diff                            | Verificação | **GPT‑6.2 Sol Light**                        | Sonnet 5.5 Medium se a segunda opinião útil         | Mais julgamento do que um worker, sem pagar uma revisão de agente completa            |
| Issue padrão completo, spec claro                     | Agente      | **GPT‑6.2 Sol Medium[**                       | **Opus 5.5 Medium** em review                  | Melhor defeito Codex para exploração → adesivo → teste → PR                        |
| Fátura multiarquivo normal                           | Agente      | **GPT‑6.2 Sol Medium[**                       | Opus 5.5 Medium em review                      | Ownership end-to-end com custo conteúdo                                             |
| Fatura complexa, várias camadas                      | Agente      | **GPT‑6.2 Sol High[**                         | Opus 5.5 Medium/High                           | Maior planejamento e verificação                                         |
| Arquitetura ou escolha de migração                       | Agente      | **Opus 5.5 High[**                            | Sol Medium para desafiar o plano             | O julgamento domina a produção de código.                                           |
| Causa desconhecida / erro Scala sutil                   | Agente      | **Opus 5.5 High[**                            | Sul Medium/High para hipóteses independentes    | Entender o problema custa mais do que o adesivo.                                     |
| Concorrência, async, flaky teste difícil                 | Agente      | **Opus 5.5 High[**                            | Sol High se a primeira pista falhar           | Reduz o risco de ancorar uma causa falsa                                    |
| Migração / compatibilidade pública                       | Agente      | **GPT‑6.2 Sol High[**                         | Opus 5.5 High em revisão conceitual           | Execução disciplinada + segunda sentença independente                                |
| Maior refator transversal                                | Agente      | **Opus 5.5 High[**                            | Sol Medium/High em review                      | Opus para a coerência global; Sol para quebrar os ângulos mortos                     |
| Revisão normal de um PR escrito pela Codex                 | Verificação | **Opus 5.5 Medium[**                          | Nenhuma excepto finding critique                    | Contexto fresco e outras famílias de modelos                                         |
| Revisão normal de uma PR escrita por Claude                | Verificação | **GPT‑6.2 Sol Medium[**                       | Nenhuma excepto finding critique                    | Simetria autor/reviewer                                                           |
| Revisão arquitetura, invariantes, casos-limite             | Verificação | **Opus 5.5 High[**                            | Astra Light tão alto em jogo    | Procurar erros conceituais em vez de ler o diff             |
| Segurança, auth, contrato crítico                         | Crítica     | **GPT‑6.2 Astra Light**                        | Opus 5.5 High como reviewer                   | Comprar capacidade superior sem sair diretamente em um esforço extremo           |
| Problema muito ambíguo, julgamento end-to-end                | Frontier     | **GPT‑6.2 Astra Light**                        | Opus 5.5 High para criticar o plano           | A capacidade de julgamento conta mais do que o comprimento do diff                   |
| Decisão muito difícil no âmbito de uma tarefa normal    | Advisor      | **Fable 5.2 Low[**                            | Sol/Opus continua a ser o executánte                     | Comprar pontualmente o julgamento fronteiriço sem transferir toda a tarefa         |
| Sol High falha por limite de capacidade                   | Escalada     | **GPT‑6.2 Astra Light**                        | Medium/High apenas se necessário            | Mudar de tier pode custar menos que um Sol Extra High prolongado                    |
| Opus High falha por limite de capacidade                  | Escalada     | **Fable 5.2 Low[**                            | Sol/Astra para challenger                      | A mesma lógica: Limitar pouco esforço antes de esforço máximo inferior               |
| Falhou CI simples após a implementação correta            | Reanudação      | **GPT‑6 Luna High** ou **Sonnet 5.5 Medium** | Escalada apenas se problema conceitual      | Não pagar Sol/Opus por uma correção local e verificável                     |
| Acompanhamento pós-PR autónomo (CI, review, mergeabilidade)         | Reanudação      | **GPT‑6.2 Sol Medium[**                      | High se root causa difícil; Sol 6.1 em fallback | Goal mode, Heartbeats ou Cloud; ciclo sequencial borneado, não Ultra           |
| Segundo fracasso que revela uma má concepção.          | Reanudação      | **GPT‑6.2 Sol High** ou **Opus 5.5 High**    | Usar a outra família para quebrar a âncora | O problema já não é mecânico: há que requalificar a hipótese.                 |
| Fallos repetidos apesar de Sol High / Opus High               | Escalada     | **GPT‑6.2 Astra Light** ou **Fable 5.2 Low**   | A outra fronteira onde se encontra a fronteira                 | A capacidade se torna o fator limitante; voltar a sair com um contexto próprio         |
| Sessão autónoma > 30 min, dependências sequenciais     | Longo horizonte | **Opus 5.5 Extra (`xhigh`)**                 | Sol High no final                              | Extra é justificado pelo comprimento, não pela importância simbólica                |
| Trabalho extremamente difícil durante várias horas    | Frontier     | **Fable 5.2 High[**                           | Astra Light/Medium em review indépendant      | Reservar o alto custo da fronteira às trajetórias em que se evita a repetição de grandes |
| Exploration codebase-scale descomposable                  | Multiagente  | **GPT‑6.2 Sol Ultra**                        | Opus Medium para síntese/review               | Ultra é aplicado sobretudo aos eixos read-heavy independentes                           |
| Testes, exploração e classificação em grande escala conexa | Multiagente  | **GPT‑6.2 Sol Ultra**                        | Claude apenas sobre as anomalias importantes | O paralelismo paga quando as subtareas são independentes e verificáveis.       |
| Vários writers nos mesmos arquivos                 | —            | **Para evitar**                                 | Secacionalização                                 | O custo de coordenação é geralmente superior ao benefício.                               |

> **Nota Qwen3-Coder-Next locais** : o modelo oficial é um MoE de **80B parâmetros no total, 3B ativados**, avec 48
> camadas híbridas, um contexto nativo de **262 144 tokens** e um funcionamento exclusivamente **no-thinking**.
> Número
> reduzido de parâmetros ativos melhora o custo de cálculo, mas os **80B de peso devem residir em
> memória
> **: « 3 Por conseguinte, B activos de 3B.
>
> Os tamanhos oficiais da GGUF são: **Q4_K_M 48,4 Go**, **Q5_K_M 56,7 Go**, **Q6_K 65,5 Go** e **Q8_0 84,8 Go**. La
> tamanho do ficheiro não é, no entanto, o consumo total: adiciona a 'cache' de contexto, os 'buffers' do backend, o '
> servidor, macOS, IntelliJ, sbt e JVM do projeto. **128 Go**, as quatro variantes podem teoricamente ser:
> Os custos de funcionamento das empresas de serviços de transporte rodoviário de mercadorias e dos serviços de transporte rodoviário de mercadorias não são iguais no caso das empresas de transporte rodoviário.
>
> ```text
> Q4_K_M  → padrão com “margem máxima”: a IDE, o sbt e várias JVMs continuam com folga.
> Q5_K_M  → padrão recomendado: melhor equilíbrio entre qualidade e memória nesta máquina.
> Q6_K    → opção de alta qualidade: viável se os demais aplicativos usarem recursos moderadamente.
> Q8_0    → opção de avaliação: possível, mas com menor folga e benefício ainda a comprovar frente a Q5/Q6.
> ```
>
> Documentação oficial Qwen usa corretamente **Q5_K_M** no seu exemplo `llama.cpp`, avec `-c 40960` e não o
> contexto máximo de 256K. Para o trabalho diário de agente, **32K à 64K**, a seguir, aumenta apenas se uma
> O contexto declarado pelo modelo é uma capacidade máxima, não uma configuração
> Economia
> por omissão.
>
> **Recomendação para o seu M5 Max 128 Go** : conserva ** Q4_K_M e Q5_K_M** no SSD. Use Q5_K_M como perfil
> diário de análise anterior, resumo de módulos e geração de testes simples; muda para Q4_K_M quando IntelliJ,
> vários módulos sbt, Spark ou JVM Consumem já muita memória. Não conserva Q6_K ou Q8_0 que se:
> um
> bake-off Scala mostra um aumento de qualidade mensuráveis. Com 8 To de SSD, o armazenamento não é a restrição; a
> pressão
> memória, latência e qualidade por tarefa são.
>
> **Backend Apple Silicon** : teste **MLX-LM e chama.cpp** Em vez de congelar imediatamente um único motor.
> Conversões MLX 4-bit e 8-bit existem, e um relatório reprodutível sobre Qwen3-Coder-Next observou descodificação.
> Muito mais rápido em MLX do que em uma versão dada de chama.cpp na Apple Silicon. Este resultado depende de
> versões e não constitui uma garantia para o M5 Max; justifica um benchmark local com versões congeladas.
> `llama.cpp` No entanto, continua a ser a via mais bem documentada por Qwen e expõe facilmente um servidor OpenAI- Compatível.
>
> **Metal e memória por cabo** : não apresenta 75 % da quantidade total de material. `llama.cpp` cartel
> Início `recommendedMaxWorkingSetSize`, que é o valor que deve ser observado na versão de macOS e Mac afetados.
> configuração não documentada `iogpu.wired_limit_mb` existe e é utilizada pela comunidade, mas não deve se tornar um
> pré-requisitos padrão: primeiro teste o modelo sem alterações no sistema. Q8_0 pode funcionar em uma máquina 128 Vamos,
> Mas um contexto longo ou várias ranhuras podem aproximar o processo a este limite antes que a RAM física
> ou bem.
> Está totalmente ocupada.
>
> **Protocolo de medição mínimo** : compara Q4_K_M, Q5_K_M e possivelmente Q6_K sobre as mesmas dez tarefas Scala, avec
> o mesmo contexto e o mesmo arness. Medição separadamente do prompt processing, o caudal de geração, o tempo até o
> Primeiro token, memória máxima, pressão de memória macOS e taxa de tarefas aceitas. Não deduza a velocidade.
> do único número de parâmetros ativos: arquitetura híbrida e implementação dos kernels podem produzir
> Diferenças
> É importante entre backends.
>
> **Qwen3.8-27B.** O denso **Qwen3.8-27B** se torna o challenger local quality-first a adicionar ao
> bake-off Scala. Qwen publica um contexto que pode chegar até 1M dependendo da implantação e dos escores editor de 73 sobre
> Terminal-Bench 2.1 e 61,7 em SWE-bench Pro. Estes valores não justificam substituir o Coder-Next por defeito:
> teste
> os dois com o mesmo arness, o mesmo contexto, as mesmas ferramentas e o mesmo orçamento de tempo. **Coder-Next continua a ser o mesmo.
> Baseline local especializado e econômica; Qwen3.8-27B é o challenger que se prefere quando a qualidade conta mais
> ** Tarifas API Qwen3.8 dependem da região e não devem ser apresentados como um preço global.

>
> **Qwen3.8-Omni-Flash.** Do 17 Setembro 2026, o Alibaba também propõe este modelo API multimodal: texto, imagem,
> áudio e vídeo em entrada, texto em saída, function calling, thinking configurable, busca web, cache de contexto,
> **1M Tokens de contexto** e até **131 072 tokens de saída** via Chat Completions ou Responses API. Completa
> o roteamento para a análise de screencasts, talks, interfaces ou documentação multimodal; ** não substitui**
> Qwen3-Coder-Next como baseline local de código ou Qwen3.8-27B como challenger Scala quality-first. Suas tarifas variam
> segundo a região de implantação: mantenha este dado fora das regras de roteamento durável e comprova Model Studio em
> momento da escolha.

<!-- section: s-3 -->
### Em relação à Anthropic

| Modelo         | API ID              | Tarifa (input/output / M Tokens) | Antecedentes          | Esforço por omissão | Função activa neste guia                                                           |
|----------------|---------------------|---------------------------------|-------------------|-------------------|------------------------------------------------------------------------------------|
| **Fable 5.2**  | `claude-fable-5-2`  | $8 / $40                        | 1M (salida 128K)  | `high`            | Frontier: raciocínio exigente e longo horizonte quando Opus 5.5 não é suficiente      |
| **Opus 5.5**   | `claude-opus-5-5`   | $4 / $20                        | 1M (salida 128K)  | **`medium`**      | Fallo agente: coding autônomo, arquitetura, debugging e grandes refatores      |
| **Sonnet 5.5** | `claude-sonnet-5-5` | $2 / $10                        | 1M (salida 128K)  | `high` API        | Micro- dev / tarefas bem especificadas; `medium` recomendado para Agentic coding borné |
| **Haiku 5.5**  | `claude-haiku-5-5`  | $0.10 / $0.50 (prompt ≤ 100K)   | 1M (salida 128K)  | `medium`          | Trabalhadores, classificação, extração, logs, subagentes de baixo risco                     |

> **Rodamento corrente:** Anthropic recomenda iniciar a maioria dos workloads com **Opus 5.5**,
> cujo esforço por defeito é `medium`, e depois ajustar o esforço antes de mudar de modelo. Para **Sonnet 5.5**, o
> coding agentifique bem especificado começa útilmente a `medium` e sobe para `high` para tarefas mais longas ou
> É difícil.
> `xhigh` (nãotado **Extra** neste guia) e `max` são reservados para os casos em que os evals mostram um ganho. **Haiku 4.5 n.
> Não suporta o parâmetro de esforço; Haiku 5.5, que o substitui, o suporta com `medium` por defeito.** Os parágrafos que aparecem a seguir em Sonnet 5 / Opus 5 continuam a ser pontos de referência de
> Migração
> históricos; não substituem esta matriz ativa.

> **Migração API vers Opus 5.5 / Sonnet 5.5.** Ambos os modelos impõem mais disciplina ao cliente do que os
> gerações anteriores: o adaptive thinking é o regime normal, o *forced tool use* (`tool_choice: any/tool`)
> devolve um erro 400, e os *thinking blocks[* devem permanecer unidos ao seu modelo e à conversa que os tem.
> **Opus 5.5** também rejeita os parâmetros de Sampling não padrão e o assistente pré-fill; seu esforço por
> falta é `medium`. **Sonnet 5.5** usar `thinking: {"type": "between_tools"}` para remover o thinking inicial.
> (`low` a `high` apenas) e agora devolve o texto intermédio entre tool calls em blocos `thinking`.
> Em Claude API e Google Cloud, ambos os modelos utilizam o toolset computador-uso atual.
> `computer_toolset_20260801` em vez de `computer_20251124`. Portanto, uma migração de modelos deve testar **payloads,
> streaming, tools e reinício de conversa**, não só substituir o ID do modelo.

> ** Sonnet 5** substitui Sonnet 4.6 (`claude-sonnet-4-6` sempre disponível à mesma tarifa.
> $3/$15) como driver diário. *drop-in replacement* lado API, com três mudanças de comportamento em
> conhecer antes de migrar:
> - **Adaptive thinking ativado por defeito** ; o extended thinking manual (`thinking: {type: "enabled"}` com
>   `budget_tokens`) devolve agora uma **error 400** - Migrando ao adaptive thinking.
> - **Configuração de Sampling bloqueada** : qualquer valor não falhado de `temperature`, `top_p` ou `top_k` devolve
>   um erro 400.
> - **Novo tokenizer** (mismo linhagem queOpus 4.7+) : ~30% de tokens mais para o mesmo texto (até 1.35x
>   O tokenizer sempre pode aumentar o número de tokens faturados; portanto, reconta os
>   Prompts com o endpoint de token counting e volta a vê-los `max_tokens` apertados.
>
> Outras particularidades operacionais: **Effort Control** geral (nível baixo) → **xhigh**, defeito *high* sobre
> l'API e Claude Code), primeiro ** segurança cibernética em tempo real** em um Sonnet (uma recusa retorna em HTTP)
> 200 com `stop_reason: "refusal"`, não em erro a administração da Priority Tier no cliente, não a saída 128K
> (300K em batch através do header beta `output-300k-2026-03-24`. Também é o novo modelo predefinido dos planos.
> Free e Pro em claud.ai.

> **Empregues conjuntos**: o logo caching e o batch (o –50% input e o output) aplicam-se a * todos* os modelos.
> Claude. No entanto, a taxa de leitura da 'cache' depende do modelo: **Fable 5.2 custa $0.20/M Tokens em 'cache' lido**
> (contra $0.25/M para Fable 5.1). A luta continua a ser útil para o trabalho não urgente: PR summaries agrupados,
> auditorias planejadas e geração de fixturas. Fable 5.2, Opus 5.5 e Sonnet 5.5 incluem o contexto 1M ao preço
> padrão, sem sobrecarga de contexto longo.
>
> **Precisão pautal.** A cache read vale a pena **0,025× Input** sobre Fable 5.2/5.1 ($0.20 e $0.25/M),
> **0,05×** sobre Opus 5.5 e Sonnet 5.5 ($0.20 e $0.10/M) e 0,1× sobre Haiku 4.5. Haiku 5.5 é o único modelo atual.
> com um **passo de comprimento de prompt** : para além de 100 000 tokens de entrada (cache incluído), todas as suas tarifas são:
> Multiplicados por cinco. Fable 5.2 $4/$20, Opus 5.5 $2/$10, Sonnet 5.5 $1/$5. Fast mode: Fable 5.2 $16/$80,
> Opus 5.5 $8/$40. `inference_geo: "us"` aplica um multiplicador de 1,1× nas categorias correspondentes.

> **Claude Fable 5.2 Substituir Fable 5.1 no roteamento activo deste guia.** Ficha
> técnica: ID `claude-fable-5-2` (`anthropic.claude-fable-5-2` sobre Bedrock), contexto **1M**, saída **128K**,
> **$8/$40**, cache write 5 Min dólares$10 e 1 h $16, cache read **$0.20/M**, batch $4/$20, moda rápida `speed: "fast"` à
> $16/$80, adaptive thinking sempre ativo, esforço por omissão `high`, cutoff junho 2026, retirada não antes do
> 9 Novembro 2027. As mesmas limitações que 5.1 : **30 dias de retenção obrigatórios (não ZDR sem autorização)
> expressa)**, `tool_choice: any/tool` e pré-fill em 400, sampling para omitir, sem Priority Tier, sem estruturad
> O modelo gera cerca de 30 % mais rápido do que 5.1. **Mythos 5.2** é o mesmo.
> modelo com menos salvaguardas, reservado às organizações verificadas.
>
> **Posicionamento.** A matriz oficial continua a ser o seguinte: Opus 5.5 - passa a -
> Fable 5.2 se os evals `xhigh` ou `max` continuarem a ser insuficientes em raciocínio exigente ou longo horizonte.
> Notícias para integrar no roteamento: em FrontierCode 2.0 (que mede se os seguradores mereciam a mudança)
> Anthropic informa **Fable 5.2 `high` à 45,3 %, ao nível deOpus 5.5 ao melhor esforço (45,5 % (%), aproximadamente a
> metade do custo por tarefa**. Pontuação editor ao melhor esforço: FrontierCode 2.0 **49,1 %** (Opus 5.5 45,5 ; Astra
> 42,8 ; Fable 5.1 32,4), FrontierSWE v2 **69,9 %** (Opus 62,3 ; Astra 65,5), Remote Labor Index 41,3 % en contra 21,3 %
> Para Opus. No coding curto a diferença é baixa: Terminal-Bench 4.0 67,6 % contra 66,4 % (Opus `xhigh`, na
> margem de erro. As medidas independentes Vals confirmam a matiz: igualdade com Opus 5.5 no Terminal-Bench 4.0
> (65,15 %), Opus versus SWE-bench Multimodal (70,2 % vs 62,3 %).
> **Mini-SWE-agent** de Vals, esta igualdade corresponde, no entanto, a cerca de **$14,56/tareia para Fable contra
> $12,04 para Opus**, com Fable mais rápido (55 min contra 64 min) : a vantagem de custo por trabalho anunciado
> por Anthropic na FrontierCode ** não se generaliza** aos outros arneses.
>
> ```text
> Opus 5.5 High fica aquém em capacidade        → Fable 5.2 antes de Opus 5.5 Max, a medir no benchmark privado de Scala
> Decisão difícil pontual (consultor)            → Fable 5.2 low/medium
> Missão longa autônoma                          → Fable 5.2 high (low/medium tendem a encerrar o turno cedo demais)
> Tarefa delimitada, bug de UI/frontend, revisão rotineira → Opus 5.5 ou Sonnet 5.5 ainda oferecem o melhor custo-benefício
> ```
>
> **Breaking changes a partir de Fable 5.1** (verificados no guia de migração oficial):
> - o **prefix check[** é agora aplicável a todas as contas: um thinking block devolvido com um `system`,
>   `tools` ou um histórico diferente dos que o produziram dá um 400 (`The block is bound to a different
>   conversation`). **Uma mudança de lista de ferramentas MCP entre dois pedidos conta como uma edição** : alfiler
>   a lista de ferramentas durante a sessão, ou use as alterações de ferramentas durante a conversa (beta)
>   `inline-tools-2026-09-15`, através de mensagens `role: "system"`.
>   Pedido modificando `tools`;
> - **Fable 5.1 e Opus 5.5 não leem os thinking blocks de Fable 5.2** (se suprimem sem erros, portanto o(
>   O raciocínio é perdido em silêncio) ; Fable 5.2 lê os de 5.1 eOpus 5.5.
>   (`fallbacks: "default"`, beta `server-side-fallback-2026-07-01`) só se dirigem a `claude-opus-4-8` e
>   `claude-opus-5`: registra o modelo executado;
> - `computer_20251124` devolve 400 (excepto Bedrock): utilizar `computer_toolset_20260801` ;
> - O advisor de um executánte Fable 5.2 deve ser `claude-fable-5-2` ou `claude-mythos-5-2` ;
> - o thinking conta na `max_tokens` (risco de `stop_reason: "max_tokens"` antes de qualquer texto) e Fable 5.2 para o seu
>   **propio bazo limit**, separada da de Fable 5/5.1Novos betas úteis: compaction à demande
>   (`compact-2026-09-04`), binding des thinking blocks (`thinking-binding-controls-2026-08-01`, avec
>   `prefix_mismatch_behavior: "drop_block"` apenas como paliativo).
>
> **Comportamentos que afetam diretamente a qualidade dos diffs e o custo** (Guia de prompting) Fable 5.2) :
> - **Propiedade do código.** Sem inscrição explícita, o modelo acrescenta à estrutura existente, dúplica e indica os
>   problemas vizinhos em vez de corrigi-los. A frase proposta pela Anthropic (o código de This codebase is yours...)
>   Juntar o código duplicado em cerca de metade dos testes, mas custa aproximadamente 1,5 de tokens de saída, acrescenta
>   testes e Docs não solicitados e modifica o comportamento existente em um ensaio de seis a dez. **Para tickets.
>   a diff minimum deste guia, não a cunhada** ; reservá-la para uma tarefa explícita de dedução ou de refator,
>   e reele o diff em vez do resumo, que muitas vezes omite pequenas mudanças.
> - **Delegação.** À `xhigh` e `max`, Fable 5.2 pode lançar subagentes para ler seu próprio trabalho, e
>   Subagentes podem representar uma grande parte do custo da sessão. Audition as linhas de `AGENTS.md`, skills e
>   Ficheiros de agentes que convidam a delegar e verifique o modelo predefinido dos subagentes.
> - **Fines de volta prematuros** (lista de tarefas restantes, oferta de continuar) mais frequentes a `low` e `medium` :
>   para uma missão longa, acrescenta o nome
>   Distingue-se entre o obstáculo ordinário (que se tratar) e o bloqueio deliberado (arquivo proibido, guarda-fogo: deixa-se e)
>   Mantenha suas próprias confirmações para as ações arriscadas.
> - **Presuposto do servidor da unidade de corte de circuito.** O `task_budget` API é indicativo: fixa um ** techo externo** custo,
>   Número de chamadas, duração e número de tentativas no arness. `max_tokens` demasiado apertado pode interromper.
>   Fácil antes do primeiro texto visível, já que os tokens de thinking contam na saída. Se a sessão parecer
>   silenciosa, use as atualizações entre ferramentas quando disponíveis em vez de multiplicar os estímulos.
> - **Instruções herdadas que devem ser purgadas**: As respostas sem deliberar a resposta não detêm a reflexão a partir de `medium`
>   (Baixa o esforço) , as linhas Opus 5.5 Den
>   o modelo muito menos capaz de recuperar seus próprios erros; os orçamentos de Tokens escritos no breve
>   Podem ser retirados em `high`/`xhigh` sem perda; as precauções antiquadas acumuladas em memória reduzem
>   Este é exatamente o papel da `/doctor prompt-audit` (secção 3, subagentes).
>
> **Acesso e quota.** Claude Code **2.1.321+** (`claude --model claude-fable-5-2` ; o alias `fable` depende
> Os planos Max/Ultra admissíveis podem utilizar Fable até uma fração máxima de **50 % dos
> limites semanais**, segundo as condições reais; o uso em Pro pode depender de créditos adicionais
> ou de uma promoção temporária.
> Nunca **modelo visível**, **cuota incluída** e **facturação API/créditos** : controle do ecrã de consumo e dos
> Condições do plano no momento da sessão. Reajusta os esforços `medium`, `high` e `xhigh` e o custo por tarefa.

> **Note tokenizer** : o novo tokenizer foi introduzido por **Opus 4.7** (Não 4.8 e gera até ~35% de
> Tokens para além deOpus 4.6 para o mesmo texto. ** Sonnet 5 adota a mesma linha** (~30% de Tokens mais do que
> Sonnet 4.6, até 1.35x de acordo com o conteúdo). A criminalização de conteo continua a ser relevante para as migrações Opus a.
> a mesma tarifa; em Sonnet 5, a tarifa permanente **$2/$10** compensa grande parte do aumento do número
> Tokens em comparação com Sonnet 4.6. A passagem Opus 4.7 → 4.8 não leva nenhuma penalização adicional de tokenizer.

> **Opus 5 e transição desde 4.8** : Opus 5 é agora o **modelo Anthropic difícil por defeito** Tarifa
> idêntico a Opus 4.8 ($5/$25). Guarda 4.8 apenas como falência de compatibilidade ou referência histórica.
> - **Fast Mode** ($10/$50, ~2.5x a velocidade padrão): para uma tarefa dura, mas *interativa* (debugging em pair),
>   Opus 5 Fast é muitas vezes uma melhor compra que Fable.
> - **Effort Control** : rodar por esforço continua sendo o passo explícito antes Fable 5.2. Em Opus 5, `xhigh` e `max`
>   exigem que o thinking se mantenha ativado; `thinking: disabled` com estes níveis devolve um erro 400.
> - **Dynamic Workflows** continua a ser relevante para o paralelismo de códigobase-scale; em Claude Code, completa agora.
>   Com o Agente View. **Agente Equipe** continua sendo experimental e **Ultrareview** em research preview: não os transforma.
>   Ainda em dependências obrigatórias do fluxo de trabalho.

> **Nota Claude Managed Agents** (plataforma alojada, beta pública desde abril 2026, header
> `managed-agents-2026-04-01`: desde Code with Claude (6 Mayo 2026), a plataforma acrescenta **Outcomes** (grader)
> independente na secção, ciclo de revisão se o output não acontecer), a ** orquestração multiagente** (até
> 20 Suboficiales especializados em paralelo em um filesystem compartilhado, **webhooks** de sessões (beta)
> , e o **Dreaming** (research preview: curation de memória entre sessões). Tarification: tokens au
> tarifa API + $0.08 por hora de sessão ativa. Para este guia é a terceira opção sobre missões longas,
> ao lado de Fable monoagente e Opus + Dynamic Workflows
> critérios de sucesso executáveis (Outcomes é a versão da plataforma de revisão da secção 15A).

> **OpenAI Agentes API** é o enquanto alojado lado OpenAI : utiliza o
> Arness gerenciado de Codex com **períodos de sessões sustentáveis**, compacção e recuperação geridas, MCP e subagentes em contextos isolados.
> Dois primitivos materializam diretamente o context engineering da secção 10: **tool search** não carga os
> definições de ferramentas que, quando relevantes, e o **programmatic tool calling** permite a cadeia,
> Ajustar e filtrar chamadas antes de injetar apenas os resultados úteis. Não é uma nova razão.
> Preferir OpenAI à Anthropic : compara **Agentes API**, Claude Managed Agentes e arneses locais ao custo por
> mudança aceite, mantendo as mesmas specificações, testes e regras de parada.
>
> **Computer use** também pode ser executado em um navegador hospedado por OpenAI.
> cria a sessão, aprova explicitamente cada nova origem e gere as autenticaçãos sensíveis.
> Uma aprovação original não é uma confirmação por ação: para compra, supressão ou outra operação.
> Portanto, mantenha um runtime controlado ou uma gate applicative separada.


Características operacionais complementares:

| Modelo         | Latencia relativa | Prompt caching     | Batch (Beef[–50%]%) | Especificações operacionais                                                                        |
|----------------|------------------|--------------------|--------------|---------------------------------------------------------------------------------------------------|
| **Fable 5.2**  | Moderada          | Sim; read $0.20/M | Sim.          | Adaptive thinking sempre on ; defeito `high` ; esforço por mensagem ; fast $16/$80            |
| **Opus 5.5**   | Moderada          | Sim.                | Sim.          | Adaptive thinking sempre on ; defeito **`medium`** ; Low→Max                                     |
| **Sonnet 5.5** | Rápido           | Sim.                | Sim.          | Adaptive thinking ; defeito API `high`, mas `medium` recomendado para agentic coding bem especificado |
| **Haiku 5.5**  | A mais rápida   | Sim; read $0.01/M | Sim.          | Adaptive thinking por defeito; esforço `medium` por defeito; nível de preços para além de 100K tokens |

<!-- section: s-4 -->
### Em relação à OpenAI / Codex

**GPT‑6.2 Sol** é o defeito recomendado para o **coding complexo e os fluxos de trabalho agenticos repetidos** em Codex quando disponível. OpenAI o posiciona como mais eficaz por tarefa que Sol 6.1, à mesma tarifa API **GPT‑6 Luna** refere-se às tarefas focalizadas , repetiveis e de alto volume; **GPT‑6.1 Terra ** é o tier intermediário. **GPT‑6.2 Astra** continua a ser a escalada de capacidade para as tarefas mais exigentes.

| Modelo          | ID API        | Preço padrão / 1 M tokens (input / output) | Função recomendada neste guia |
|-----------------|---------------|---------------------------------------------|-------------------------------|
| **GPT‑6 Luna**  | `gpt-6-luna`  | **$0.10 / $0.50** | Micro-dev, mudanças mecânicas, testes simples, classificação e workers de baixo risco |
| **GPT‑6.1 Terra** | `gpt-6.1-terra` | **$1 / $5** | Patch local e revisão dirigida quando Lua falta de julgamento |
| **GPT‑6.2 Sol** | `gpt-6.2-sol` | **$2 / $10** | **Fallo Codex Agente Medium**: issue end-to-end, feature multi-archivoirs, testes, PR, review et stewardship |
| **GPT‑6.2 Astra** | `gpt-6.2-astra` | **$8 / $40** | Frontier: problema muito ambíguo, contrato crítico, escalada de capacidade |
| GPT‑6.1 Sol / GPT‑6 Astra | `gpt-6.1-sol` / `gpt-6-astra` | $2 / $10 ; $10 / $50 | Fallbacks se as versões 6.2 não estiverem disponíveis; baselines históricos |

> **GPT‑6.1 Terra enche o buraco entre Lua e Sol.** Saiu o 26 Outubro 2026 (`gpt-6.1-terra`)
> Cuesta **$1/$5** (cached input $0.05/M), isto é, metade do Sol 6.1, com a mesma janela de cerca 1,05M Tokens.
> está disponível na ChatGPT Work e Codex (Plus, Pro, Enterprise, Edu; não na página Chat) e pede uma Codex
> CLI recente (0.159+ de acordo com as fontes). OpenAI coloca-o nas correcções de erros correntes, computer use,
> a visão e a escrita; para o coding exigente, agora prefere **Sol 6.2 ou Astra 6.2**. Pontuação publicada:
> 50,3 % no Terminal-Bench 4.0 no máximo esforço (21,5 % para GPT‑5.6 TerraPara este guia, Terra torna-se o **Candidato
> natural para adesivos bornados e revisão de pequenos diffs** quando a Lua é demasiado justo e Sol demasiado caro: para partir
> por bake-off antes de mudar a matriz.

> **GPT‑6.2 Sol e Astra**: 1,05M tokens de janela, dos quais 922K de entrada máxima e 128K de saída máxima.
> Escondido read: $0.10/M para Sol, $0.40/M para Astra; cache write 30 min a 1,25× input, 12 h à 2,5×.
> Para além de 272K Tokens de entrada, as tarifas input/cache dobran e a tarifa output são multiplicadas por 1,5 para
> Batch está na sala de espera. 50 % da tarifa padrão; a Flex não se propõe nos novos modelos 6.2.
> Não transponha estes preços à quota de assinatura. Sol 6.1 Medium e Astra 6 Light permanecem fallbacks se os
> As versões 6.2 não estão disponíveis. O stewardship é uma capacidade do arness, não do modelo.
> anteriores ainda são baseslines históricos, que não devem ser atribuídos aos modelos 6.2.

> **Ultrafast é um tier de serviço, não um novo modelo ou um nível de esforço.** Base histórica: para GPT-6 Astra, l'API Ultrafast.
> refere-se a até ~8 a velocidade de Standard e factura em contexto curto **$60/M input, $6/M cached input, $75/M cache
> write e $300/M output**. Use-o apenas quando a latência realmente domina o custo total; para os riços
> Agente de muitos tool calls, OpenAI recomenda uma conexão de resposta persistente em WebSocket. Ultrafast no
> Não é compatível com a residência dos dados da UE: funciona num tratamento global ou com residência dos EUA.
> O produto, o Astra Ultrafast está incluído na **Pro 500** e algumas ofertas Enterprise. Por conseguinte, não muda.
> o roteamento de qualidade desta seção: `Astra Standard` e `Astra Ultrafast` têm a mesma capacidade modelo.
> Na GPT‑6.2, verifica as tarifas e os direitos do plano antes de ativar; só reserva a terceiros rápidos aos riços.
> interativas realmente limitadas pela latência, não à espera de CI.

Na **Codex / Work**, raciocina com os níveis visíveis **Light → Medium → High → Extra High → Ultra**. O defeito deste guia é **Sol Medium**, **Luna High** para microbouchles e **Astra Light** para uma escalada de capacidade. `Ultra` supera um simples run mono-agente e só é rentável se o trabalho pode se decompor realmente em eixos independentes. API, os nomes dos níveis `low/medium/high/xhigh/max` segundo o modelo: não confunde o texto produzido com o valor portátil de `reasoning.effort`.

Os modelos GPT‑5.6 podem estar disponíveis durante o rolout, mas já não constituem a rota ativa por omissão deste guia.

<!-- section: s-5 -->
#### Cinco dimensões que não devem ser confundidos

| Levier                            | O que está mudando.                                                                                     | Regra prática                                                                                                           |
|-----------------------------------|-----------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|
| **Modelo**                        | Capacidade, velocidade e preços: Lua, Terra, Sol 6.2 ou Astra 6.2.                                 | Lua para o borné; Sol 6.2 para a lefluente repetida; Astra apenas quando a capacidade superior reduz as repetições. |
| **Effort**                        | Orçamento de raciocínio: Codex Light→Ultra; API `low/medium/high/xhigh/max` de acordo com modelo. | Suelo: Medium por omissão; Lua: High; Astra: Light; aumentar apenas se o planejamento/verificação o justificar.   |
| **`reasoning.mode: "pro"`** (API) | Mais trabalho modelo para uma resposta final mais confiável.                                    | Independente do esforço; comparar padrão/pro em tarefas representativas.                                          |
| **`ultra` como esforço Codex**    | Alguns SDK/harness Codex expõem agora `ultra` como nível de reasoning acima de `max`. | Tentar como uma capacidade do arness, não como um valor portátil da Responses API.                             |
| **Ultra / Multi-agent**           | Orquestra de vários agentes ou sessões de acordo com a superfície produzida/API.                         | Usar apenas se o trabalho for realmente dividido em partes independentes.                                          |

Na janela **Responses API**, o valor máximo documentado de `reasoning.effort` fica `max` e **Multiagente** permanece uma característica beta diferente. Em alguns arnesess Codex, `ultra` Pelo contrário, não deduzis nunca a semântica da única palavra " ultra" , que se refere à superfície, ao modelo, ao esforço e ao número real de agentes. OpenAI não publica nenhum multiplicador de custo fixo; medida de custo total, latência e taxa de sucesso no seu depósito antes de padronização.

<!-- section: s-6 -->
#### Astra: controlos para missões prolongadas

Astra acrescenta três capacidades especialmente úteis aos agentes:

```text
async tool calling
→ continuar raciocinando ou acionar outras ferramentas enquanto uma ferramenta lenta estiver em execução

mid-turn steering
→ adicionar uma restrição ou mudar de direção durante a missão sem reiniciá-la

configuration updates
→ ajustar o esforço durante a execução sem invalidar desnecessariamente o prefixo do cache
```

Para um backend agentista, prefere a **Responses API** : o tool calling Astra e é a superfície de referência. Astra não aceita `reasoning.effort = none`, nem os ajustes personalizados de `temperature` / `top_p` documentados como incompatíveis. **Fast mode** API pode chegar até ~2× mais rápido para **2× preço padrão** ; não tem um SLA de latência e não deve se tornar o defeito de uma missão longa.

<!-- section: s-7 -->
#### Disponibilidade e superfícies ChatGPT / Codex

| Superfície                  | Acesso modelo e modo                                                                                                               |
|--------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| **ChatGPT Work / Codex** | GPT‑6.2 Sol e Astra, GPT‑6.1 Terra, Lua e fallbacks segundo plano, cliente, workspace e rolout.                                              |
| **GPT‑6.2 Sol / Astra**  | Mais, Pro, Business, Enterprise e Edu em Codex/Work segundo direitos; controles de esforço Light→Ultra segundo parâmetros disponíveis. |
| **GPT‑6 Luna**           | Modelo econômico para tarefas focalizadas e repetiveis em Work/Codex.                                                            |
| **Ultra / multiagente**  | Para reservar os eixos independentes; não assimilar a um maior reflexo a sequência.                    |
| **API**                  | `gpt-6.2-sol`, `gpt-6.2-astra`, `gpt-6.1-terra`, `gpt-6-luna` através das superfícies suportadas; verificar as ferramentas e os esforços por modelo.                |

Os direitos efectivos dependem sempre do plano, da região, do workspace e do rolout. Nunca codifique uma regra de produto durável a partir do único nome de uma assinatura.

<!-- section: s-8 -->
#### Caching, segurança e guarda-costas

GPT‑6.2 Sol factura o cached input **$0.10/M** contra $2/M em input padrão; as cache writes permanecem em 1,25× input. GPT‑6 Luna baixa em **$0.01/M** Em cached input. Estabiliza a parte superior do prompt (`AGENTS.md`, convenções Scala, contratos, regras de teste) e deixa diffs, logs e erros abaixo.

> **Dos alavancas de custo em volume.** Sobre GPT‑6.1 Sol e GPT‑6 Luna, Batch e Flex 50 % menos que
> Padrão; em GPT‑6.2 Sol/Astra, Batch conserva esta redução, mas Flex nspc não se propõe.
> Utiliçalos para o que tolera a latência: auditorias planejadas, PR summaries agrupadas, geração de fixturas e classificação
> Em massa. Não transponha automaticamente estas tarifas API quota ChatGPT/Codex : o indicador correto continua a ser o custo por
> tarefas terminadas na superfície realmente utilizada.

GPT‑5.6 permanece classificado como cibernético pelo grupo de alto nível, mas não pelo grupo de Critical. **GPT‑6 Astra (geração original) é o primeiro modelo OpenAI Crítica de segurança cibernética**: com as ferramentas adequadas, pode encontrar vulnerabilidades desconhecidas e desenvolver novas cadeias de exploração. Este nível de capacidade é acompanhado de um monitoring de trajetória mais estrito: em ChatGPT/Codex, uma tarefa legítima pode ser abranda , pausada ou solicitar uma validação; API, o trabalho pode ser interrompido.

Este aumento da capacidade não justifica qualquer autonomia adicional. Com Astra, faça ainda mais explícitos: scope de arquivos, rede, operações externas, escrituras destrutivas, orçamento, duração, condições de parada e validação humana. Ponto favorável para o código sensível: **Astra suporta o Zero Data Retention para os clientes API admissíveis**, mas Fable 5.2 obriga 30 dias por defeito a menos que se autorize expressamenteAnthropic.

<!-- section: s-9 -->
#### Benchmarks e prudência

Os números de lançamento de Astra são particularmente fortes no **coding agentique et computer use**, mas devem permanecer amarrados ao seu arnês. OpenAI informa em particular: Terminal-Bench 4.0 **57,9 % Astra vs. 55,8 % Fable 5.1**DeepSWE 1.1 **74,1 % vs. 67,4 %**, FrontierCode Extended **64,5 % vs. 63,6 %** e suas tarefas internas de migração DB **63,9 % vs. 57,8 %**. Em AutomationBench, Astra alcançou **41,4 % vs. 31,4 %** para Fable 5.1. Estas são avaliações publicadas por OpenAI : úteis como sinal, nunca como veredicto sobre Scala.

A avaliação independente artificial Analysis matiza fortemente a tabela. **Coding Agent Index v1.4**, Claude Code + Fable 5.1 (`max`, com fallback) consegue **70** contra **67** para Codex + Astra (`max`), mas Astra consome aproximadamente **4,0M tokens/tareia contra 7,1M** e custa ao redor de **$4,72/tâche contre $9,18**. Sobre o **Intelligence Index**, Fable 5.1 `max` está também à frente (**66 vs. 61**) Portanto, o bom ensino não é " Astra" > Fable "B": **Fable mantém uma pequena vantagem de qualidade agregada nestes protocolos, Astra uma vantagem importante de eficácia por tarefa em Codex**.

Astra também publica um lembrete muito bom longo contexto em MRCR v2: **100 % à 256–512K** e **96,3 % à 512K–1M**. Não converta estas pontuações em permissão para enviar o monorepo inteiro: para além de 272K, sua tarifa aumenta e o *context rot* continua a ser um problema de raciocínio, não só de capacidade física.

Para este guia, a conclusão robusta se torna:

```text
GPT‑6 Luna High = microdesenvolvimento e workers Codex sob forte controle humano.
GPT‑6.2 Sol Medium = opção padrão do Codex para codificação agêntica de ponta a ponta.
GPT‑6.2 Sol High = funcionalidade complexa, migração e recuperação difícil.
GPT‑6.2 Astra Light = escalada de capacidade antes de elevar automaticamente o esforço do Sol ao máximo.
Sonnet 5.5 Medium = microdesenvolvimento no Claude e tarefas agênticas bem especificadas.
Opus 5.5 Medium = opção padrão do Claude para codificação agêntica autônoma.
Opus 5.5 High = arquitetura, depuração e refatoração difíceis.
Fable 5.2 Low = escalada para um modelo de fronteira quando Opus High ainda é insuficiente.
Astra vs Fable = decida pelo custo por alteração aceita, em vez do preço por token.
```

<!-- section: s-10 -->
### GPT‑6 Astra vs Claude Fable 5.2: referência histórica de dois fronteiros

Esta comparação mantém os números do GPT‑6 Astra original: para o roteamento corrente, utiliza GPT‑6.2 Astra Se o cliente o propor. A sua tarifa padrão é $8/$40 (cache read $)$0.40/M) ; não lhe atribui os resultados do antigo Astra. Comparar os modelos atuais no mesmo arness e no mesmo depósito.

Compare a **modelo no seu arness real**, não um número de editor isolado. Fable 5.2 é mais barato por token padrão do que GPT‑6 Astra, mas a diferença de custo por tarefa depende do caching, do esforço, das ferramentas e das reproduções.

| Eixo | GPT‑6 Astra | Claude Fable 5.2 | Consequências práticas |
|-----|-------------|------------------|---------------------|
| Harness natural | Codex / ChatGPT Work / Responses API | Claude Code / Mensagens API | Medir o sistema completo |
| Preço padrão input / output (M tokens) | **$10 / $50** | **$8 / $40** | Mais barato nominalmente |
| Cache read (M tokens) | **$1** | **$0.20** | Janela Fable em prefixos realmente reutilizáveis |
| Longo contexto | 1,05M; sobrecarga para além de 272K | 1M; taxa padrão | Preferir contexto específico em ambos os casos |
| Esforço | Light→Ultra por superfície; API low→max | low→max ; adaptive thinking | Fable `high` para longa autonomia `low` para parecer pontual |
| Computer use | Capaz, com orquestra e ferramentas | Resultados de editor fortes | Verificar em cenários reproduzidos |
| Qualidade de diff mergeable | Avaliações com arness Codex | FrontierCode 2.0: 49,1 % ao melhor esforço segundo Anthropic | Os protocolos de edição não demonstram superioridade geral |
| Independência de medidas | Avaliações de terceiros disponíveis | Vals: igualdade com Opus em Terminal-Bench 4.0, retrocesso em multimodal | Esperar uma comparação Fable 5.2 / Astra de arness comparável |
| ZDR | Clientes API admissíveis | 30 dias por defeito, excepção contratual necessária | Filtrar tarefas por requisitos de privacidade |
| Missões prolongadas | Async tools, mid-turn steering | Esforço por torre, thinking relacionado ao histórico | Proteger o Estado, as ferramentas e as regras de paragem |

**Lectura de benchmarks.** Anthropic anúncio Fable 5.2 diante de Astra en FrontierCode 2.0, FrontierSWE v2 e OSWorld 2.1, mas são uns **resultados de edição**El Coding Agente Índice de Análise Artificial Comparado Claude Code + Opus 5.5 à Codex + Astra indica um compromisso diferente entre taxa de sucesso , custo e duração; ** não mede Fable 5.2**A comparação histórica Fable 5.1/Astra já não deve servir como regra de roteamento atual. Os resultados independentes de Vals também mostram que Fable 5.2 não é sistematicamente melhor do queOpus 5.5.

Regra de roteamento prática:

```text
Microdesenvolvimento interativo com supervisão humana
→ GPT‑6 Luna High ou Sonnet 5.5 Medium

Issue padrão de ponta a ponta
→ GPT‑6.2 Sol Medium
→ Opus 5.5 Medium para revisão independente

Arquitetura / causa raiz / refatoração difícil
→ Opus 5.5 High
→ GPT‑6.2 Sol Medium/High para questionar a abordagem

Sol High insuficiente por limite de capacidade
→ GPT‑6.2 Astra Light, depois Medium se necessário

Opus High insuficiente por limite de capacidade
→ Fable 5.2 Low, depois Medium se necessário

Mesma tarefa realmente de fronteira, Astra vs Fable
→ dois worktrees / mesma especificação / mesmos testes
→ comparar custo total + minutos de trabalho humano + qualidade do diff
→ decisão humana
```

Já não se fixa um par permanente Claude writer / Codex reviewer law. **O writer é escolhido por natureza de tarefa** : Sol 6.2 geralmente possui a saída padrão; Opus 5.5 A outra família é utilizada para repassar ou replantear-se independentemente. Duplicar as duas trajetórias completas só é justificado para um bake-off ou uma decisão realmente fronteiriça.

<!-- section: s-11 -->
### Em relação aos modelos open-weight chineses (Kimi K3, GLM‑5.2, e o resto do cluster)

Desde2026, uma terceira família foi imposta ao lado deAnthropic e deOpenAI : os modelos **Abiertos chineses de nível fronteiriço**, que atingem uma codificação de agentes perto de Sonnet/Opus a um custo por token muito inferior. Para um idoso Scala que já está pilotando Claude Code e Codex, não são substitutos do driver diário, mas ** uma alavanca de custo numa classe exata de subtareas** e uma **opção de soberania** (self-host) para código sensível.

**Trampa de categoria que deve ser imediatamente enunciada** : estes modelos não são **não** na mesma categoria que Qwen3-Coder-Next. Qwen local (80B/3B ativos) é realmente explorável no seu laptop. 128 GB: Q4_K_M deixa uma margem muito ampla, Q.5_K_M é o melhor defeito e Q6_K continua a ser viável.8_0 Pode ser carregado, mas deve ser validado com o contexto, IntelliJ y sbt Realmente abertos. GLM‑5.2 (753B) e sobretudo Kimi K3 (2.8T) ne tiennent **não** local sobre 128 Go: são modelos **API** (Z.ai, Moonshot, OpenRouter) o **self-host no servidor multi- GPU**. Moonshot recomenda, por outro lado, uma implantação Kimi K3 em configs de 64+ Analisador. Assim, nunca os coloque na caixa de verificação da casa de verificação. Qwen local: vivem na caixa de verificação API terceiro ou servidor de equipamento de lavatório.

| Modelo      | Editor / Acesso                                                                                                    | Arquitetura                                                                                             | Antecedentes                 | Preço API (in / out /M)                | Base de referência (medidas independentes/editor)                                                                                             |
|-------------|--------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|--------------------------|---------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| **Kimi K3** | Moonshot API, OpenRouter (`moonshotai/kimi-k3`), Kimi Code CLI; **pesos completos publicados** Licenciado Kimi K3 | MoE 2.8T total, **104B ativados** ; 896 especialistas, 16 ativados; KDA + Atenção Residentes, visão nativa    | Até 1M segundo o plano | **$3 / $15** (cache-hit input $0.30)  | Pontuação editor de esforço máximo e com vários arneses; excelentes sinais frontal e longo horizonte, para confirmar em Scala                   |
| **GLM‑5.2** | Zhipu/Z.a.i. API OpenAI- ** e Anthropic- Compatível**, GLM Coding Plan; checkpoint MIT publicado                      | MoE **753B** Total BF16 ; número de activos não documentados oficialmente ; esparcimento atenção | 1M                       | **$[$1.40 /$4.40** (cache input $0.26) | Pontuação editor: SWE-bench Pro **62.1**, TerminalBench 2.1 81.0 com Terminus-2 e 82.7 melhor arness; para comparar com o mesmo protocolo |

**Esforço de raciocínio.** GLM‑5.2 exposição **High** y **Max**. Kimi K3 exposição `reasoning_effort: low | high | max`A página modelo/API indica **`max` Predefinição:**, enquanto Kimi Code pode definir um defeito diferente segundo sua versão e plano: portanto, sempre fixa o esforço explicitamente em um benchmark ou automação. 1M depende do plano: 256K em Moderato, até 1M em Allegretto e acima. Para uma tarefa interativa curta, começa em `low` o `high` ; reserva `max` às missões prolongadas em que se justifica o seu custo de saída.

<!-- section: s-12 -->
#### Onde entram em *ton* roteamento

```text
✅ Revisão em volume e triagem de baixo risco    → GLM‑5.2 (High): preço por token bem menor que Opus, mas é preciso medir o custo por tarefa
✅ Extração, classificação e resumos de PR em lote → GLM‑5.2 ou Kimi K3 em lote, quando o volume encarece Sonnet/Terra
✅ Geração de frontend / protótipo web          → Kimi K3 (#1 Frontend Code Arena) se a tarefa for além de Scala puro
✅ Segunda opinião independente com pesos abertos → um modelo de uma 3ª escola de treinamento pode revelar pontos cegos comuns a Claude e GPT
✅ Código sensível / ambiente isolado / soberania → GLM‑5.2 hospedado localmente (pesos MIT): nada sai da sua infraestrutura
```

```text
❌ Uso diário em Scala no lugar de Sonnet 5.5: o modelo é capaz, mas você perde o ecossistema (Claude Code, subagentes, Metals MCP maduro)
❌ Tarefa interativa curta com Kimi K3 no máximo esforço: latência e verbosidade prejudicam o custo-benefício. Use low/high
❌ Decisão crítica de arquitetura sem segunda opinião: mantenha Opus/Fable ou obtenha um parecer independente de Sol. O modelo de pesos abertos serve para questionar a decisão
❌ “Substituir” o Qwen local: categoria errada (veja a armadilha acima)
```

<!-- section: s-13 -->
#### Acesso ocasional a GLM através de OpenRouter

Para este fluxo de trabalho, não adicione uma assinatura de GLM por defeito. **GLM continua sendo um modelo de emergência**, a chamar via OpenRouter quando Claude Code, Codex e Qwen local não permitiram resolver o problema. Isto mantém a diversidade de modelos sem adicionar uma nova conta, uma nova chave e um novo plano a seguir.

Se o GLM se torna uma ferramenta utilizada a cada semana ou traz um ganho mensurável em uma classe de tarefas, então reavalia o interesse de um acesso direto Z.ai. Enquanto este limiar não for alcançado, a simplicidade prima.

<!-- section: s-14 -->
#### O resto do cluster (para localizar, não para adotar tudo)

`MiniMax M3` (junio) 2026) é o primeiro open-weight a combinar codificação fronteiriça, contexto 1M *y* multimodalidade nativa (cabeça de Open-weight em SWE-bench Pro a 59.0 antes GLM‑5.2). `DeepSeek V4` decae um V4 Pro e um V4 Flash$0.14/$0.28 /M) imbatível na relação custo/contexto longo para a classificação massiva. Nenhum é o melhor em todas as partes a cena da noite livre de meados de2026 É um cluster apertado onde a escolha correta depende da tarefa e do preço, não de uma classificação global.

<!-- section: s-15 -->
#### Duas reservas à cabeça

1. **Progenancia e destilação.** Kimi K3 foi identificado como Dl Claude , em pelo menos um intercâmbio informado. Esta auto-identificação anecdótica ** não é um teste de destilação** e não permite nenhuma conclusão científica ou contratual sobre os dados de treinamento. Se a proveniência conta para um cliente, requer documentação do editor e trata a informação como desconhecida até que seja publicada.
2. **Metodologia de benchmark.** As tabelas de edição misturam arneses diferentes (KimiCode, Claude Code, Codex, mini-SWE-agente) e K3 é sensível à preservação da história de *thinking*. As diferenças que são muitas vezes inferiores a um ponto: nem sempre sobrevivem a uma mudança de arneses. Regra sem alterações: **Bake-off controlado em suas tarefas reais** (versões fixas, permissões fixas, testes de aceitação deterministas, custo por mudança aceite), não adoção baseada em uma classificação.

<!-- section: s-16 -->
#### Protocolo do bake-off Scala : Kimi K3 contra GLM‑5.2

Não só compara as respostas finais. Use pelo menos **15 tarefas privadas**, nunca publicadas, repartidas entre:

```text
3 bugs sutis de Scala 3: givens, implicits, variância, tipos opacos
3 alterações em Play / Tapir / Pekko que afetam de 3 a 8 arquivos
3 tarefas de Spark / concorrência / desempenho
3 revisões de PR com defeitos conhecidos inseridos de propósito
3 tarefas de teste: ScalaTest, ScalaCheck, testes de mutação
```

Protocolo: mesmo commit, mesmo worktree inicial, mesmas ferramentas, mesmo limite de tempo, mesma rede, mesmo pacote de contexto, mesmos critérios de parada e **tres repetições por tarefa**. Kimi deve ser testado separadamente em `high` e `max`; GLM `High` e `Max`. Se os arneses não puderem ser idênticos, publica duas matrizes e não atribui a diferença ao modelo.

Medidas obrigatórias:

```text
- tarefa aceita pelos testes e pela revisão humana
- compilação, testes direcionados, pontuação de mutação
- defeitos de segurança ou de contrato detectados
- linhas adicionadas ou removidas e arquivos afetados
- número de tentativas, chamadas de ferramentas e ciclos repetidos
- tokens de entrada, cache, raciocínio e saída
- custo total da API, latência e minutos de trabalho humano até o merge
- taxa de sucesso pass@1 e estabilidade em três execuções.
```

Aproba GLM ou Kimi num fluxo apenas se reduzir o custo por mudança aceite **sin** Degradar os guarda-costas. Uma pontuação editor superior mas mais correcções humanas é uma regressão, não um ganho.

<!-- section: s-17 -->
## Regra de decisão por tarefa

<!-- section: s-18 -->
### Quando utilizar **Fable 5.2** (Mythos-class)

Fable 5.2 custa duas vezes Opus 5.5 por token ($8/$40 contra $4/$20). Anthropic Recomenda- se que comece com **Opus 5.5 `medium`**, subir para `high`e depois reservar Fable 5.2 para uma escalada de capacidade, teste **Fable `low`** Antes de empurrar o Opus sistematicamente para `Extra`/`Max` :

```text
✅ Migração completa de um framework (Play 2 → 3, Pekko, atualização do Spark)
✅ Sessão autônoma de várias horas ou dias sem supervisão
✅ Refatoração entre módulos em > 10 arquivos interdependentes
✅ Depuração de um bug de negócio cuja causa está longe do sintoma
✅ Decisão arquitetônica sem resposta óbvia após testar Opus 5.5 High
✅ Tarefa pela qual você pagaria meio dia de trabalho a um engenheiro sênior
```

```text
❌ Tarefa bem delimitada: Sonnet 5.5 ou Opus 5.5 oferecem melhor custo-benefício
❌ Revisão de diff ou resumo de PR: capacidade e custo desnecessários
❌ Geração de boilerplate ou fixtures: Qwen ou Haiku são suficientes
❌ Alteração de uma linha ou correção direcionada: Luna High, Sonnet 5.5 Medium ou Aider
❌ Tarefa difícil, mas interativa sob sua supervisão: Opus 5.5 Medium/High costuma bastar
```

> **Posicionamento 5.2.** Anthropic recomenda que se conserve **Opus 5.5 como ponto de partida** para a maioria dos
> workloads. Fable 5.2 `low` é um **advisor pontual**, a avaliar numa tarefa limitada e verificável; para uma missão
> Realmente auto-suficiente, começa em `high` para reduzir os fins da volta prematura. **costo por mudança.
> aceite** no benchmark Scala privado, em vez de generalizar os resultados do fornecedor.
> $0.20/M melhora a economia dos prefixos longos estáveis. Quando o verificador é confiável, também prova o esquema
> **Low → retry High sur fail** incluindo repetidos, latência, revisão e validação humana.

<!-- section: s-19 -->
### Prompting Fable 5.2 : estruturar uma missão longa

Fable 5.2 (janela) 1M, saída até 128K) não é um Opus mais forte, mas aponta para o raciocínio exigente e a longo prazo quando as avaliações Opus continuam a ser insuficientes. A continuidade dos thinking blocks e a estabilidade das definições de ferramentas tornam-se limitações do arness, além do esforço configurável por mensagem. Referência: `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2`. As alavancas seguintes permanecem válidas para 5.2 ; os pontos específicos de 5.2 (propriedade do código, sobre-delegação, fins de volta prematuros, histórico append-only, instruções herdadas para purgar) são detalhadas na nota Fable 5.2 da secção lata Anthropic".

Cinco alavancas específicas:

1. ** Carta de missão em cabeça de contexto, oculta.** O bloco inicial (objectivo, não objetivos, invariantes, regras de parada) nunca deve mudar entre as torres: beneficia-se do prompt caching e serve de âncora anti-derive nas sessões longas. Tudo o que evolui (estado, erros, diffs) vai depois.
2. ** Estado persistente explícito.** Em uma missão multi-hora, requer um ficheiro de estado (`MIGRATION_STATE.md` no worktree) que o modelo actualiza a cada marco: módulos tratados, módulos restantes, decisões tomadas, bloqueios. Este ficheiro
3. **Checkpoints com critério de saída.** Corta a missão em marcos verificáveis através de comandos deterministas (`compile`, testes seletivos, escalafmtCheckAll). Não passa para o próximo marco sem um marco comum verde.
4. **Ruta o esforço por turno sem mudar de modelo.** Use `medium/high` para a exploração, `xhigh/max` para uma decisão realmente difícil, então `low/medium` para uma edição mecânica. O per-mensagem de esforço preserva a cache e evita pagar o nível máximo durante toda a trajetória.
5. ** Se uma compaction for necessária, impõe o seu contrato de resumo.** Solicitar que se preservem explicitamente problemas e resoluções, pistas testadas ou descartadas, decisões e limitações, estado atual, pontos abertos e detalhes difíceis de reconstruir. A compaction servidor já gere esta necessidade; para uma compaction do cliente, nunca resume em prosa livre sem estes campos.

Gabarit de mission Fable 5.2:

```text
# MISSÃO (estática — manter inalterada durante a sessão)
Objetivo: [migração / refatoração específica]
Fora do escopo: [o que está explicitamente fora do escopo]
Invariantes: APIs públicas, contratos JSON e comportamentos listados em AGENTS.md
Duração máxima: [N horas] — Custo máximo: [N USD] — Diff máximo por marco: [N linhas]

# REGRAS DE PARADA (estáticas)
Pare e relate imediatamente se:
- avançar exigir violar um invariante
- o mesmo marco falhar 2 vezes por causas diferentes
- for preciso mudar build.sbt, uma migração de banco ou um contrato público
- a duração restante estimada ultrapassar 2x a estimativa inicial.

# PROTOCOLO (estático)
1. Leia AGENTS.md e MIGRATION_STATE.md.
2. Cuide de UM marco: plano curto → diff → compilação → testes direcionados.
3. Atualize MIGRATION_STATE.md e faça o commit do marco.
4. Relate o progresso: marco concluído, marcos restantes, novos riscos e desvios do plano.
5. Retome no passo 2.

# ESTADO (dinâmico — anexe a versão atual de MIGRATION_STATE.md)
[estado]
```

> **Continuidade Fable 5.2.** Não retrograde silenciosamente uma sessão: Fable 5.1 e Opus 5.5 não conecta os
> thinking blocks do Fable 5.2. Nem edita mensagens antigas, prefixo do sistema ou lista de ferramentas.
> reutilizando estes blocos: o controlo de coerência pode produzir um erro 400. Se uma mudança de ferramentas ou de
> modelo é indispensável, guarda o estado útil em `MIGRATION_STATE.md`, e depois volta a sair com um contexto próprio.
> `tool_choice: any/tool` é proibido em Fable 5.2 ; utiliza `auto` e valida o resultado com um esquema estrito.

> **Nota operacional**: uma variável de segurança pode mudar o modelo realmente executado. Se a missão tocar o
> Código cripto ou segurança baixo nível, logice este modelo, verifique que mantém o nível de capacidade esperado e previsto
> Este caso na regra de parada em vez de o descobrir durante a sessão.

<!-- section: s-20 -->
### Quando utilizar **Opus 5.5**

É a **defeito Claude Code para o agente autônomo**. O seu esforço por defeito é `medium`, o que muda o roteamento em comparação com Opus 5 : começa em `medium`, sobe para `high` quando a tarefa é difícil, a seguir, utilizar `Extra` (`xhigh`) ou `Max` se a duração ou os evals o justificarem.

```text
✅ Issue completa quando Claude assume o percurso exploração → correção → testes
✅ Arquitetura, migração e planejamento entre módulos
✅ Causa raiz distante do sintoma, implicits/givens/efeitos difíceis
✅ Grande refatoração em que a coerência geral é mais importante que a edição pontual
✅ Revisão independente de uma PR escrita pelo Codex
✅ Orquestração de subagentes de leitura intensiva com contexto isolado
```

```text
medium → padrão para trabalho agêntico
high   → depuração, arquitetura ou trabalho difícil de longo prazo
Extra  → >30 min e tarefas com uma sequência realmente longa de etapas, além de uma simples tarefa “importante”
Max    → uso excepcional, com prioridade absoluta à qualidade e ganho mensurável
```

<!-- section: s-21 -->
### Quando utilizar **Sonnet 5.5**

A melhor opção Claude quando **o idoso mantém forte a mão** ou quando a tarefa de agente estiver bem especificada. Anthropic recomenda explicitamente `medium` para o coding agente e o uso multistep de ferramentas bem articuladas, depois `high` para tarefas mais longas ou difíceis.

```text
✅ Bug pequeno e reproduzível
✅ Refatoração local com escopo bem definido
✅ Testes de negócio direcionados e baseados em propriedades
✅ Stack trace → diagnóstico → correção
✅ Funcionalidade clara com arquitetura já decidida
✅ Worker de implementação seguindo um plano humano ou elaborado pelo Opus
```

```text
low    → transformação simples / prioridade para baixa latência
medium → padrão para microdesenvolvimento e codificação agêntica bem especificada
high   → tarefa mais longa ou difícil
Extra / Max → apenas se as avaliações mostrarem ganho. Caso contrário, passe ao Opus 5.5
```

Portanto, a regra econômica já não é a de Sonnet com o máximo esforço antes de Opus. Se Sonnet High falha por um limite de capacidade, **Opus Medium** é muitas vezes uma melhor compra que um Sonnet Extra/Max prolongado.

<!-- section: s-22 -->
### Quando utilizar **Haiku 5.5**

Sistemáticamente para tarefas *alta frequência e baixo risco* :

```text
✅ Subagentes de leitura ou extração de baixo risco com resultados verificáveis
✅ Resumos de logs e resumos rápidos de PR
✅ Classificação e roteamento
✅ Edições direcionadas < 20 linhas
✅ Geração de mensagens de commit
✅ Chamadas repetitivas de baixo risco se o benchmark confirmar o ganho
```

> **Haiku 5.5 Substituir Haiku 4.5 Como worker Claude.** Cuesta **$0.10/$0.50** Enquanto o prompt
> é mantido sob 100 000 tokens (cache read $0.01/M), ou **dix fois moins que Haiku 4.5** e a mesma ordem de preço que
> GPT‑6 Luna ; para além de 100K Tokens de entrada, incluindo cache, a tarifa passa para $0.50/$2.50. Contexto 1M, saída 128K,
> adaptive thinking ativo por defeito e **parâmetro `effort` compatível (`medium` por defeito)**. Trampas migratórias:
> o pré-fill devolve agora 400, `temperature`/`top_p`/`top_k` se omitem, `budget_tokens` devolve 400, le
> thinking conta na `max_tokens`, e um `tool_choice` Forçado permanece aceito, mas elimina a reflexão antes da chamada.
> O tokenizer conta com aproximadamente 30 % de tokens mais do que Haiku 4.5. Regra prática: Mantenha os contratos de subagentes
> ** sob 100K Tokens[** para permanecer na parte inferior, o que se liga à disciplina de isolamento da secção 3.
> Haiku 4.5 permanece ativo, mas agora é possível removê-lo em qualquer momento com o aviso habitual de 60 dias.

<!-- section: s-23 -->
### Quando utilizar **GPT‑6 Luna**

```text
✅ Microdesenvolvimento: alteração local sob sua orientação
✅ Testes simples, fixtures, boilerplate, renomeações e transformações mecânicas
✅ Busca de ocorrências, resumos, logs e resumos de PR
✅ Worker ou subagente cujo resultado seja verificado imediatamente
```

OpenAI recomenda começar a Lua a **High**. Não tente converter a Lua em um agente fronteiriço com Extra High: se a tarefa se tornar ambígua ou conceitual, passa a Sol 6.2 em vez de pagar longas vezes em um modelo muito pequeno.

<!-- section: s-24 -->
### Quando utilizar **GPT‑6.2 Sol**

```text
✅ Issue padrão completa: descoberta → implementação → testes → PR
✅ Funcionalidade em vários arquivos ou bug não trivial
✅ Revisão independente de uma PR escrita pelo Claude
✅ Migração delimitada, compatibilidade e refatoração transversal
✅ Segunda opinião sólida sobre uma arquitetura proposta pelo Opus
```

```text
Light       → issue muito bem especificada, correção local, reprodução clara
Medium      → padrão para o trabalho agêntico diário
High        → funcionalidade complexa, causa raiz difícil, migração, muitos casos-limite
Extra High  → capacidade suficiente, com necessidade real de mais análise ou verificação
Ultra       → apenas quando o trabalho puder ser dividido em investigações independentes
```

<!-- section: s-25 -->
### Quando utilizar **GPT‑6.2 Astra**

```text
✅ Sol High falha por falta de capacidade ou julgamento, mesmo com contexto adequado
✅ Segurança, autenticação, contrato crítico ou decisão em que a direção errada custa várias rodadas de retrabalho
✅ Fluxo muito ambíguo de ponta a ponta, com muitas ferramentas ou uso de computador
✅ Revisão pontual por modelo de fronteira em uma decisão de alto impacto
```

Começa com **Astra Light**. Para uma tarefa realmente fronteiriça, Astra Light pode custar menos que um Sol Extra High, seguido de uma recuperação, porque evita uma má trajetória. Sube a Medium/High só se necessário; Extra High/Ultra ainda é excepcional.

<!-- section: s-26 -->
### Quando utilizar ** o modo `ultra` em ChatGPT Work / Codex**

```text
✅ Mapeamento de toda a base de código de uma aplicação legada
✅ Migração de vários módulos em worktree dedicado
✅ Auditoria paralela de arquitetura, testes, segurança e desempenho
✅ Divisão de uma refatoração em micro-PRs
✅ Missão em que várias análises independentes agregam valor
```

```text
❌ Pedido único de “reescreva direito”
❌ Tarefa interativa curta
❌ Repositório pouco testado sem limite de diff
❌ Alteração direta de arquivos críticos sem aprovação do plano
```

Nesta subsecção, `ultra` nome **modo de orquestra multi-agente do produto**, e não o nível de esforço `ultra` que alguns SDKs Codex Agora é adequado para as persianas independentes; evita-o quando os agentes escrevem no mesmo estado mutável ou quando uma única operação lenta domina a tarefa. Em uma aplicação legacy, começa por cartografiar, produzir um registro de dívida, propor testes de caracterização e depois cortar em microPRs. Não começa por escrever código.

Gálibo mínimo para uma missão `ultra` :

```text
Você atua como uma equipe de revisores e agentes em uma aplicação Scala legada.

Papéis a simular:
- arquiteto com experiência em sistemas legados
- líder técnico Scala
- revisor de segurança defensiva
- engenheiro de QA e testes
- mantenedor cético.

Objetivo:
[objetivo específico]

Restrições:
- preservar o comportamento observável até que haja validação
- parar antes de alterar build.sbt, migrações de banco ou contratos JSON públicos
- micro-PRs com menos de 300 linhas alteradas
- testes de caracterização antes de refatorar
- citar os arquivos examinados em cada conclusão
- distinguir fatos, hipóteses e recomendações.

Resultado esperado:
1. mapa do escopo
2. riscos
3. registro da dívida técnica
4. testes de caracterização prioritários
5. plano em micro-PRs
6. proposta da primeira PR, com implementação somente após a aprovação do plano.
```

<!-- section: s-27 -->
## Matriz de seleção modelo rápido

```text
Microdesenvolvimento sob controle humano  → GPT‑6 Luna High / Sonnet 5.5 Medium
Worker de leitura ou triagem de baixo risco → Haiku 5.5 / Qwen local / GPT‑6 Luna
Correção local com julgamento intermediário → GPT‑6.1 Terra Medium
Issue padrão de ponta a ponta             → GPT‑6.2 Sol Medium
Agente Claude de ponta a ponta            → Opus 5.5 Medium
Funcionalidade ou bug difícil             → GPT‑6.2 Sol High ou Opus 5.5 High, conforme a tarefa
Arquitetura ou causa raiz predominante    → Opus 5.5 High
Revisão cruzada                           → família diferente da do autor, Medium por padrão
Acompanhamento pós-PR no Codex            → GPT‑6.2 Sol Medium (Goal / Heartbeat / Cloud)
Sol High insuficiente                     → GPT‑6.2 Astra Light
Opus High insuficiente                    → Fable 5.2 Low
Trabalho sequencial longo > 30 min       → Opus 5.5 Extra (`xhigh`)
Trabalho paralelizável em toda a base    → GPT‑6.2 Sol Ultra, sobretudo com muita leitura
Tarefa de fronteira mais exigente         → Astra Medium+ / Fable Medium+ após comprovar a necessidade
```

Regra prática:

```text
O profissional sênior mantém a direção → modelo rápido e econômico.
O agente conduz o fluxo → Sol 6.2 ou Opus 5.5.
Compreender o problema é mais importante que a correção → prefira Opus.
A execução de ponta a ponta tem prioridade → prefira Sol 6.2.
Surge um limite de capacidade → Astra Light ou Fable Low antes do esforço extremo no modelo inferior.
Ultra somente quando houver vários eixos de trabalho realmente independentes.
```

<!-- section: s-28 -->
## Localização automática das tarefas de desenvolvimento

A matriz de seleção não deve permanecer apenas manual. Para evitar queimar créditos em tarefas simples ou, ao contrário, enviar uma tarefa crítica a um modelo demasiado fraco, adiciona um passo explícito de roteamento antes de cada tarefa de agente.

O princípio não é escolher o modelo mais inteligente, mas o modelo mais pequeno capaz de produzir um resultado mergeável com um risco aceitável.

```text
Solicitação / ticket / stack trace
→ classificação da tarefa
→ estimativa de dificuldade + risco
→ escolha do menor modelo aceitável
→ execução com permissões limitadas
→ testes determinísticos
→ escalada em caso de falha
→ registro de custo e qualidade
```

<!-- section: s-29 -->
### Arquitetura recomendada

```text
CLI / IDE / ticket
→ task-classifier
→ context-builder
→ model-router
→ agent-runner
→ test-runner
→ reviewer
→ registro de custo e qualidade
```

| Componente          | Função                                                         | Modelo / ferramenta recomendado                                                                             |
|--------------------|--------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| `task-classifier`  | Ordenar a tarefa, o risco e a dificuldade                 | **Jev** se a saída estiver fechada; Qwen local / Haiku se for necessário um raciocínio aberto         |
| `context-builder`  | Encontrar arquivos, relacionamentos, testes, docs e pedidos úteis | Sourcebot, ScalaSemantic MCP, Codebase-Memory MCP se polyglotte, rg, IntelliJ, Metals MCP, Context7   |
| `model-router`     | Escolher o modelo mais pequeno aceitável                      | Regras deterministas + Jev como sinal probabilista; OpenRouter apenas para escalada pontual  |
| `agent-runner`     | Executar com as permissões correctas                         | Codex, Claude Code subagentes, Aider, OpenCode, Qwen Code                                              |
| `test-runner`      | Validar de maneira determinista                              | sbt, IntelliJ, Metals MCP, CI                                                                         |
| `reviewer`         | Ler sem escrever                                           | Família oposta ao writer: Opus 5.5 Medium ou GPT‑6.2 Sol Medium; Astra/Fable apenas tão crítico |
| `cost-quality log` | Medir custo, qualidade, feedback e revisão            | Scripts locais, quadro de acompanhamento                                                                      |

<!-- section: s-30 -->
### Jev : decision layer, no coding model

**Jev 1.14 (`jev-1.14.0`)** é o modelo System One actual do TypeSafe AINão gera texto ou código: recebe um `state` e perguntas típicas, então devolve diretamente decisões probabilistas. O bom modelo mental é um **Semântica**: entrada aberta, ramos definidos pelo desenvolvedor.

| Primitiva | Utilização                                                           |
|-----------|-----------------------------------------------------------------|
| `Choice`  | escolher entre opções fechadas: modelo, agente, skill, estrada |
| `Score`   | notar em uma escala ordenada: risco, pertinência, prioridade   |
| `Noul`    | Estimar a probabilidade de uma proposta ser verdadeira.            |

Jev 1.14 custa **$0.042/M Tokens input** e não factura a saída. O regime padrão aceita **64K Tokens por pedido** e ** 32K para `state` + a questão mais longa** ; os limites de fluxo dependem da organização e leem-se na consola. Um contexto experimental mais longo e as entradas de imagem existem sob condições, sem se tornar o defeito do roteador. `jev-latest` ponta para `jev-1.14.0` : **aprieta a versão** tão logo quanto calibre limiares, pois a mudança de distribuição pode invalidar os limiares de risco.

> **OpenAI Decisions API.** Endpoint `POST /v1/decisions`, atualmente disponível em `gpt-6-luna`, com
> Respostas típicas `predicate`, `choice` e `score`. Até **400 Perguntas** podem compartilhar uma mesma entrada; texto,
> Imagens e dados estruturados são suportados de acordo com o campo. Preço padrão: **$0.10/M tokens de entrada**, **$0.01/M
> Tokens de entrada em cache lido**, sem facturação de saída, as escrituras de cache, entradas longas e processamentos
> As regiões seguem as suas tarifas. `task-classifier` e `model-router`, compara as decisões com as Jev nos mesmos.
> perguntas com uma calibração por tarefa e risco, nunca sobre o preço único do token.

Neste fluxo de trabalho, os melhores candidatos são:

```text
✅ classificação de tarefa, risco e dificuldade
✅ roteamento de modelos: Luna / Sol / Astra / Sonnet / Opus / Fable
✅ seleção progressiva de algumas skills em um catálogo amplo
✅ triagem dos resultados dos subagentes e avaliação da relevância do contexto
✅ sinal de mudança de assunto / “devemos considerar a compactação?”
✅ filtragem de notificações e decisões que merecem atenção humana

❌ escrever ou explicar Scala
❌ arquitetura ou análise de causa raiz em aberto
❌ cálculo, contagem ou comparação de datas
❌ decidir sozinho sobre push, implantação, exclusão, segredos ou migração de banco
```

Arquitetura recomendada:

```text
regras determinísticas
→ Jev para julgamentos fechados e frequentes
→ código combina probabilidades + limiares
→ LLM generativo se houver raciocínio em aberto ou confiança insuficiente
→ pessoa responsável se a ação for crítica ou irreversível
```

**Tipo de safe a correcta.** O argumento de que a exposição às alucinações é zero Jev não sai de uma estrutura ou de um conjunto de opções declarado; pode sempre seleccionar a opção errada. Uma avaliação independente sobre **346 009 pedidos / 37 datasets** encontra probabilidades `Choice` bem calibradas, mas também mostra que um limiar universal de `0.5` é ruim para algumas tarefas binários: os limiares devem ser **Calibrados por tarefa e risco**.

Três regras de integração:

1. **O código mantém a autoridade.** Os sinais deterministas (`touches_security`, arquivo crítico, ação destrutiva) sempre prevalecem sobre Jev.
2. ** Estado mínimo.** Jev também sofre * context rot* ; filtro antes do recurso e n.o envia que o que realmente muda a decisão.
3. **Prueba a estabilidade.** Sobre `Choice`, reordena pontualmente as opções; avaliações de `jev-1.13` indicam uma possível sensibilidade à ordem, para validar em `jev-1.14.0`. O `state` opositor também pode influenciar a resposta: Jev É um sinal, não uma sandbox.

<!-- section: s-31 -->
### Classificação mínima

O roteador deve produzir uma decisão estruturada, não uma resposta livre. Exemplo de saída esperado:

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

**Hierarquia dos sinais** : os critérios deterministas (`touches_*`, `expected_files`, tamanho de diff esperado) são os disparadores. *Primário* Enrutamento e escalada. Se a classificação vem de **Haiku/Qwen**, `confidence` Continua a ser uma autoestima secundária e mal calibrada. Se vem de **Jev**, utiliza a distribuição e a `confidence` voltas, mas com um **limiar calibrado por pergunta e nível de risco**Nunca um. `0.75` universal. Em ambos os casos, uma confiança elevada nunca deve. *de escalada* um sinal determinista crítico.

`reasoning_effort` deve ser padronizado por superfície: Claude utiliza `low | medium | high | xhigh | max` em modelos compatíveis, com **Opus 5.5 e Haiku 5.5 `medium` ** por defeito; Codex cartel **Light | Medium | High | Extra High | Ultra**, enquanto que aAPI OpenAI exposição de valores `low | medium | high | xhigh | max` segundo modelo. `multi_agent` O esforço é uma alavanca de qualidade e de custo, mas um terno superior a baixo esforço pode ser mais barato no total do que um tier inferior empurrada ao extremo.

<!-- section: s-32 -->
### Matriz automática de roteamento

| Sinal detectada                                               | Modelo inicial                | Escalada                                                                      |
|--------------------------------------------------------------|-------------------------------|-------------------------------------------------------------------------------|
| Resumo, classificação, grep, logs simples                           | Haiku 5.5 / Qwen              | Sonnet 5.5 Medium se ambíguo                                                   |
| Boilerplate, DTO, fixtures, edição mecânica                | GPT‑6 Luna High               | Sonnet 5.5 Medium se type/domínio sutil                                    |
| Teste simples ou não-regressão localizada                      | GPT‑6 Luna High               | Sonnet 5.5 Medium se regra profissional importante                                  |
| Patch objetivo, humano mantém a direção                       | Luna High / Sonnet 5.5 Medium | Sol 6.2 Light/Medium se necessário explorar                                |
| Patch bornado com julgamento intermediário                      | GPT‑6.1 Terra Medium           | GPT‑6.2 Sol Medium se necessário explorar |
| Faturação profissional limitada, 1 à 5 arquivos                        | GPT‑6.2 Sol Medium            | Sol High se dificuldade ; Opus Medium em review                                |
| Fatura 5 a 10 arquivos com invariantes                      | GPT‑6.2 Sol Medium/High       | Opus 5.5 High se arquitetura/root causa domina                               |
| Bug Scala sutil, implicacits, givens, efeitos                  | Opus 5.5 High                 | Suelo High para a hipótese independente ; Fable Low se capacidade insuficiente     |
| Migração de múltiplos módulos borneados                               | GPT‑6.2 Sol High              | Opus High em review ; Astra Light si Sol teto                             |
| Refator codebase-scale                                      | Opus 5.5 High                 | Extra tão longo horizonte; Fable Low si Opus teto                            |
| Revisão de uma PR Codex                                        | Opus 5.5 Medium               | High se risco crítico                                                       |
| Revisão de uma PR Claude                                       | GPT‑6.2 Sol Medium            | High e depois Astra Light se houver risco de fronteira                                      |
| Acompanhamento autónomo de um PR Codex                               | GPT‑6.2 Sol Medium            | High se diagnóstico difícil; Sol 6.1 Medium se 6.2 não estiver disponível             |
| Segurança / Auth / contrato crítico                           | GPT‑6.2 Astra Light + humano    | Astra Medium/High + review Opus High                                          |
| Ejes read-heavy independentes                                 | GPT‑6.2 Sol Ultra             | Astra Ultra só se a capacidade adicional for realmente necessária. |
| Mudança `build.sbt`, dependências, DB, contrato JSON público | Não há auto-escrita.           | Plano + validação humana                                                     |

<!-- section: s-33 -->
### Política de escalada

O roteamento automático deve funcionar como uma cascata controlada:

```text
Microciclo verificável: Qwen / Haiku / GPT‑6 Luna High / Sonnet 5.5 Medium
→ responsabilidade agêntica: GPT‑6.2 Sol Medium / Opus 5.5 Medium
→ dificuldade: Sol High / Opus High
→ limite de capacidade: Astra Light / Fable Low
→ esforço maior somente se a capacidade for suficiente, mas o raciocínio ficar aquém
→ Ultra somente se houver trabalho paralelizável
→ pessoa responsável
```

**Não mude de modelo em meio a uma conversa que se desvio.** Se o fracasso vem de uma trajetória contaminada a hipótese falsa repetida, alucinações que se acumulam, correcções que recriam outros erros a situação é em si mesma parte do problema. Sonnet 5.5 → Opus 5.5, Sol 6.2 → Astra o Opus 5.5 → Fable 5.2 :

```text
1. Encerre o modo de escrita.
2. Crie HANDOFF.md com objetivo, estado do diff, fatos verificados, tentativas malsucedidas, erro atual e incógnitas.
3. Abra uma nova sessão só com especificação + AGENTS.md + HANDOFF.md + arquivos e diff relevantes.
4. Escale o modelo nessa nova sessão se a dificuldade continuar justificando a escalada.
```

A escalada de **capacidade** é útil sobre um problema propriamente dito; não deve transportar a dívida conversacional de uma sessão já sesgada.

Escala automática se:

```text
- há um sinal determinístico crítico (touches_* sensível, diff acima do limite)
- autoconfiança do LLM < 0.75, ou confiança de Jev abaixo do limiar calibrado para esta decisão
- o mesmo erro de compilação ocorre 2 vezes
- o teste direcionado continua falhando após 2 correções
- diff fora do escopo
- mais arquivos alterados do que o previsto
- mais de 300 linhas inesperadas no diff
- alterações em build.sbt, plugins.sbt, migração de banco ou contrato JSON público
- API pública alterada
- o roteador detecta segurança, concorrência, desempenho ou dinheiro
- o modelo declara explicitamente alta incerteza
- o custo estimado de um erro supera o custo do modelo superior.
```

Interromps (sem escalar automaticamente) se:

```text
- max_cost_usd atingido (orçamento local)
- max_duration_minutes atingido (limite de tempo decorrido):
  uma sessão agêntica em ciclo é um modo de falha distinto de uma sessão que termina com erro,
  e escalar para um modelo mais caro não resolve o ciclo.
```

Desacelerar automaticamente se:

```text
- tarefa puramente textual
- sem necessidade de escrita
- sem risco de negócio
- menos de 20 linhas esperadas
- um único arquivo
- objetivo determinístico
- teste existente bem direcionado
- contexto estável e já conhecido no projeto.
```

<!-- section: s-34 -->
### Regras de não automação

Nunca deixe que um roteador decida por si só sobre uma escrita em:

```text
- build.sbt
- plugins.sbt
- resolvers
- versões de dependências
- migrações de banco
- contratos JSON públicos
- segurança
- autenticação
- autorização
- concorrência
- movimentação financeira
- exclusão de dados
- scripts de implantação ou infraestrutura.
```

Nesses casos, o roteador só pode propor:

```text
- modelo recomendado
- plano
- arquivos prováveis
- testes a executar
- riscos
- regra de parada.
```

<!-- section: s-35 -->
### Subagentes Claude Code Recomendações

**Calibração Codex 6.2.** Para um parente GPT‑6.2 Sol ou Astra, vê com o mesmo modelo e o mesmo esforço para os subagentes (recomendação oficial OpenAIA continuação, reduz o tier das tarefas verdadeiramente mecânicas, de saída controlável: Luna/Haiku para grep, extração, logs e resumos; Sol/Opus para invariantes, arquitetura e root causa. O mesmo princípio de medida vale lado Claude. Um revisor da outra família continua sendo uma sessão independente, não um worker menos caro do autor.

Claude Code é o melhor lugar para aplicar este roteamento diariamente, já que os subagentes podem ter seu próprio contexto, ferramentas e permissões.

```text
researcher
- Modelo: Haiku / Qwen se for externo
- Modo: read-only
- Função: encontrar arquivos, usos, testes e documentação

scala-implementer
- Modelo: Sonnet 5.5 `medium`
- Modo: escrita limitada ao repositório
- Função: implementar tarefas delimitadas com um plano claro

hard-debugger
- Modelo: Opus 5.5 `high`
- Modo: escrita limitada, plano obrigatório
- Função: bugs sutis de Scala, implicits, efeitos e causas distantes

migration-planner
- Modelo: Opus 5.5 `high`. Se Opus atingir seu limite, Fable 5.2 `low` (decisão pontual) ou `high` (missão longa)
- Modo: planejamento primeiro, worktree dedicado
- Função: migrações entre módulos, refatorações longas e estratégia de divisão
- Nota: avaliar Dynamic Workflows (Opus 5.5 + muitos subagentes em paralelo)
  como alternativa a um único agente Fable para migrações que envolvam toda a base

reviewer
- Modelo: Codex / GPT‑6.2 Sol `medium`. Astra `light` para tarefas críticas
- Modo: no-write
- Função: revisão independente, com achados classificados como bloqueantes, importantes ou opcionais

pr-summarizer
- Modelo: Qwen / GPT‑6 Luna
- Modo: no-write
- Função: resumo da PR, notas de lançamento e checklist final
```

<!-- section: s-36 -->
#### Isolamento de contexto: o papel principal dos suboficials nas tarefas prolongadas

O ganho dos subagentes não é apenas o paralelismo. Cada subagente trabalha numa **ventana de contexto fresco e isolado** ; o pai não precisa, portanto, acumular as buscas, logs, arquivos desviados e sem saída de cada subtareia. Este isolamento protege o contexto principal contra *context rot*.

A repartição recomendada é:

```text
AGENTE PRINCIPAL
- objetivo
- restrições e itens fora do escopo
- plano aprovado
- decisões tomadas
- diff atual
- evidências essenciais
- riscos em aberto

SUBAGENTES
- exploração de muitos arquivos
- busca com Sourcebot / rg
- caminhos de chamadas, hierarquias, usos e cadeias de givens via ScalaSemantic
- grafo estrutural entre linguagens via Codebase-Memory quando Java/Kotlin/Scala coexistem
- investigação em tempo real de tipos, givens e diagnósticos via Metals
- documentação externa
- grandes volumes de logs e suítes de testes
- mapeamento de módulo legado
```

Regra de decisão:

```text
Os detalhes dessa subtarefa ainda serão úteis ao agente principal depois que ela terminar?

NÃO → isole a subtarefa em um subagente
SIM → mantenha os detalhes no contexto do agente principal
```

A mensagem de delegação deve ser uma **contrato**, pois o subagente não deve depender de toda a conversa histórica do pai:

```text
Missão:
[escopo preciso]

Modo:
somente leitura / escrita limitada

Procure:
[perguntas específicas]

Evite:
[fora do escopo]

Retorne somente:
1. conclusão
2. evidências em arquivo:linha
3. testes ou comandos relevantes
4. incertezas restantes.

Resposta desejada: < 1–2K tokens.
```

A volta é uma interface, não uma transcrição. Se um subagente cama 80K Tokens e devolve 1,5K, o isolamento é útil; se lê 10K e devolve 8K, moveu sobretudo o ruído. Uma métrica simples a seguir nas tarefas longas é:

```text
isolation_ratio
= tokens consumidos pelo subagente
/ tokens retornados ao agente principal
```

Assim, o bom pattern é **Map → reduz** : vários workers especializados gastam o contexto local, depois o pai sintetiza alguns resultados curtos. Evita o anti-pattern reverse *context rot* no contexto raiz.

Para **tu workflow só Scala**, trata também o fan-out como um orçamento de Tokens/competidores:

```text
padrão                              → 1 agente ativo
2 investigações independentes      → 2 subagentes somente leitura
2 histórias de usuário independentes → até 2 implementadores no início (WIP inclui PRs em revisão)
3+ sessões paralelas               → apenas com medição de ganho e de capacidade de revisão
agente com escrita                 → sempre 1 por branch / PR / worktree
```

Pelo menos `parallel_sessions_peak`, `subagent_count` e `subagent_tokens`, um subagente protege o contexto do pai, mas carrega seu próprio contexto: portanto, nunca é agrate! , e se não trazer isolamento útil nem trabalho realmente paralelo, não o lança.

Para a coordenação, prefere uma **topologia em estrela** : o pai delega contratos independentes e sintetiza retornos. Evita as equipes onde os agentes falam livremente, compartilham um mailbox ou se distribuem eles mesmos um estado mutável. Neste guia, o coordenador **Delegador simples**, não um sistema social de agentes.

> **Orquestração Claude Code** : **Agente View** será responsável por supervisionar várias sessões e tarefas;
> **Agent Teams** permite a colaboração entre instâncias mas continua sendo experimental; **Ultrareview[** é uma revisão da nuvem.
> Multi-agente em pesquisa prévia. **Remote Control** permite monitorar uma sessão local a partir de outro dispositivo.
> Ao mesmo tempo que se mantém a execução e os MCP na máquina local. Estas superfícies completam os subagentes;
> Modificar
> não a regra ... um único writer por worktree ...

> **Mod `You should know` (2.1.287+)** : `cc-plugin-you-should-know` lança um side agente durante as tarefas longas.
> e mostra acima do prompt os elementos que você ou Claude poderia perder. É **desactivado por defeito** e
> seltragentiva via `/plugin enable cc-plugin-you-should-know@builtin`. Trátalo como um sinal de vigilância oportunista,
> nunca como um revisor independente, um oráculo ou um gate: suas observações ainda devem estar relacionadas a um teste,
> um teste ou um diff verificável.

> **Claude Code 2.1.27x: isolamento mais fino.** Desde 2.1.277, um subagente personalizado ou fornecido por um plugin pode
> declarar `omitClaudeMd` para não carregar `CLAUDE.md` usuário, projeto e local; as políticas administradas
> Reserve este modo aos trabalhadores de exploração muito especializados cujo contrato de delegação contenha
> Já todo o contexto necessário. A mesma versão permite atar `allowed_domains` a um comando.
> Bash/PowerShell/Monitor: a abertura de rede é válida para este comando, não para toda a sessão. ** confirma**
> n
> • normas mínimas por subagentes • e • autorizações mínimas por subtareia • • sem justificar a supressão do
> contexto projeto para um implementar que o precisa.
>
> Desde 2.1.278, o modo Auto usa por defeito um ** Classificar o lado servidor** nas superfícies compatíveis e
> Anthropic
> indica que este classificador não adiciona custos de classificação; `/status` indica se `Auto mode server` está activo.
> Isto reduz um overhead de roteamento, não os requisitos de autorização ou revisão. Por último, plugins e skills
> São convertidos em artefatos de teste: `claude plugin eval` (2.1.269) realiza uma série de avaliações da pontuação.
> e reproduzíveis com saída JSON/HTML, enquanto `/skill-doctor` ajuda a detectar os esquis carregados mas desnecessários.
> Portanto, uma mudança persistente de plugin ou skill deve passar por eval + review antes da promoção.
>
> As seguintes versões acrescentam duas ferramentas complementares para evitar a deriva do arness. Desde **2.1.283**,
> `/doctor prompt-audit` (também conhecido por `/checkup prompt-audit`) audita `CLAUDE.md`, skills, agentes e comandos para detectar
> n
> instruções que se tornaram obsoletas ou contraditórias após uma mudança de geração de modelos.
> Não- interactivo, **`--bare`** agora é documentado como a forma de lançar um arness mínimo: não
> auto-discovery dos hooks/plugins/MCP/memoria/instrução, e desde 2.1.286 apenas os servidores MCP explícita
> Não foram ligados, sem lembretes do sistema ou tarefas de fundo. Use `--bare` para **evals e scripts
> Leições**, não como modo diário predefinido.

<!-- section: s-37 -->
### OpenRouter para o roteamento API casual

Na **este workflow só precisa**, o roteamento principal não precisa de um gateway APIOs cinco caminhos diários já têm sua própria superfície e orçamento:

```text
Claude Code        → assinatura Claude Max
Codex              → assinatura ChatGPT
Qwen local         → MLX / llama.cpp / endpoint local
GitHub Copilot     → assinatura GitHub Copilot
JetBrains AI       → assinatura JetBrains AI
```

A necessidade API que resta é **excepcional** : quando Claude Code e depois Codex permanecem bloqueados e quer uma opinião de outra família de modelos, por exemplo **GLM, Kimi, Gemini, Grok ou um novo modelo para avaliar**. Nesse caso, **OpenRouter é o melhor defeito**: uma única chave, nenhum servidor que manter, acesso rápido a muitos modelos e fornecedores, faturamento centralizada e disponibilidade de fallback.

```text
Bloqueio persistente
→ extrair o mínimo de contexto útil
→ OpenRouter
   ├── GLM
   ├── Kimi
   ├── Gemini
   ├── Grok
   └── novo modelo a testar
→ comparar a análise com Claude / Codex
→ decisão humana
```

** Não conduza automaticamente o trabalho diário para OpenRouter.** A escolha do modelo de resgate deve continuar sendo explícita: o objetivo é precisamente obter outra perspectiva, não deixar que um roteador escolha silenciosamente uma família diferente.

<!-- section: s-38 -->
#### Fallbacks: provider sim, modelo não predefinido

OpenRouter pode mudar automaticamente entre providers. Para este guia, distingue dois níveis:

```text
Mesmo modelo, provedor A indisponível
→ mesmo modelo, provedor B
→ SIM: resiliência sem mudar a natureza do revisor

GLM indisponível
→ Gemini
→ Kimi
→ Grok
→ NÃO por padrão: a troca de modelo precisa ser visível e intencional
```

Assim, para uma investigação técnica, sempre se registra ** o modelo realmente utilizado**. Uma falha intermodelo pode esconder a razão pela qual uma conclusão difere de Claude ou Codex.

<!-- section: s-39 -->
#### Qwen local: permanece direto

Não acrescenta OpenRouter apenas para uniformar Qwen. `llama.cpp`, MLX ou arness local já podem expor um endpoint OpenAI-compatible. Enquanto houver apenas um ou dois modelos locais, a camada adicional não fornece valor suficiente:

```text
Qwen local
→ llama-server / MLX
→ Qwen Code / OpenCode / script local
```

<!-- section: s-40 -->
#### Confidencialidade com um agregador

Os fornecedores acessíveis através de OpenRouter podem ter diferentes políticas de retenção. Para código profissional sensível:

```text
- nunca envie o repositório inteiro por padrão
- prefira uma reprodução mínima, alguns tipos ou métodos, o stack trace e o teste direcionado
- anonimize o contexto de negócio se possível
- escolha explicitamente provedores compatíveis com os requisitos de retenção do projeto
- mantenha o código mais sensível em ambiente local ou com os provedores diretos já aprovados.
```

<!-- section: s-41 -->
### Metricos para logger

O roteador deve ser ajustado a dados reais, não a intuição. Para cada tarefa de agente, o clog:

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

Após duas semanas, ajusta os limiares:

```text
- se Qwen falhar com frequência em um tipo de tarefa, encaminhe diretamente ao Sonnet
- se Sonnet resolver um tipo de tarefa sem achados na revisão, dispense Opus
- se Opus reduzir muito os ciclos de correção, mantenha-o nessa classe de tarefa
- se Opus `xhigh/max` for suficiente para o que você enviava a Fable, volte ao Opus
- se Fable não reduzir o retrabalho humano, reserve-o para sessões realmente longas
- se `max` encontrar apenas observações opcionais, reduza para `high` ou `medium`.
```

<!-- section: s-42 -->
### Prompt roteador minimum (fallback generativo)

Sim. Jev está disponível e as saídas estão fechadas, prefiro `Choice` / `Score` / `Noul` Atômicos e depois combina os resultados em código. O prompt seguinte continua a ser útil quando é necessário um raciocínio aberto ou como baseline de comparação.

```text
Você é um roteador de tarefas de desenvolvimento de software para um projeto Scala/Java/Play/Spark.

Analise a solicitação abaixo e retorne somente JSON válido.

Objetivo: escolher o menor modelo capaz de produzir um resultado pronto para o merge com um risco aceitável.

Leve em conta:
- tipo de tarefa
- dificuldade
- risco de negócio
- tamanho provável do diff
- número provável de arquivos
- necessidade de escrita
- necessidade de documentação externa
- riscos específicos de Scala: implicits, givens, efeitos e serialização JSON
- arquivos e áreas críticas: build.sbt, migrações de banco, autenticação, segurança, concorrência e dinheiro
- modelo, esforço e, se necessário, modo `pro` ou multiagente (`ultra` no produto)
- limites de custo e duração
- regra de escalada
- condições de parada.

Os sinais determinísticos (arquivos críticos, tamanho do diff) têm prioridade sobre sua autoconfiança.

Solicitação:
[COLE A SOLICITAÇÃO]

Contexto disponível:
[COLE OS ARQUIVOS, O STACK TRACE, O DIFF STAT OU O RESUMO]
```

<!-- section: s-43 -->
### Princípio orientador do roteamento

```text
O roteador escolhe pelo custo e pela capacidade necessários à tarefa.
Ele escolhe o modelo mais barato capaz de produzir um diff pronto para o merge,
com regra explícita de escalada assim que o risco ou a incerteza aumentarem.
```

<!-- section: s-44 -->
## Impacto no orçamento mensal

*(orden relativo indicativo a partir das tarifas API padrão; a assinatura e a quota não se tornam mecanicamente em dólares API)*

| Modelo              |           Preço API input/output / M | Recomendação do volume                                                                          |
|---------------------|------------------------------------:|---------------------------------------------------------------------------------------------------|
| Qwen local          |                                   0 | Pré-análise e tarefas seguras em volume                                                             |
| **Jev 1.14**        | **$0.042/M input ; output grátis** | Decision layer: classificação, routing, escoring e seleção de skills de alta frequência        |
| **GPT‑6 Luna**      |                   **$0.10 / $0.50** | Micro- dev Codex, workers, classificação, testes simples                                                   |
| **Haiku 5.5**       |                   **$0.10 / $0.50** | Subagentes, classificação ; nível ×5 se input > 100K; esforço `medium` Configurável                        |
| **GPT‑6.2 Sol**     |                        **$2 / $10** | Falta Codex agente; excelente ponto de desempenho antes de Astra                                 |
| **Sonnet 5.5**      |                        **$2 / $10** | Falta de micro-dev Claude; `medium` para agente coding bem especificado                              |
| **Opus 5.5**        |                        **$4 / $20** | Falta de Claude agente a `medium` `high` para tarefas difíceis                             |
| **GPT‑6.2 Astra**   |                        **$8 / $40** | Escalada de capacidade ; começar em Light                                                          |
| **Fable 5.2**       |                        **$8 / $40** | Frontier Claude; começar em Low durante uma escalada de capacidade                                 |
| Extra / Max / Ultra |                            variável | Usar apenas depois da medição: mais esforço não é sinônimo de melhor custo por tarefa terminada |

> **O preço por token não é o TCO.** Avalia também Fable 5.2 `low` sobre tarefas limitadas e verificáveis: pode custar menos por tarefa resolvida.
> que um modelo inferior que procure , relee e backtracke mais; vice-versa , Opus 5.5 `medium` pode alcançar a
> a mesma qualidade que Fable em alguns workloads para uma fração do custo. Portanto, o benchmark local deve medir.
> **costo por mudança aceite**, reproduzidos e minutos humanos.

<!-- section: s-45 -->
## Regra anti-créditos queimados

Não lances Fable 5.2, GPT‑6.2 Astra, Opus 5.5 `Extra/Max` ou um modo `Ultra` dispendioso que, se você puder fornecer:

```text
- objetivo específico
- restrições
- arquivos ou módulos prováveis
- critérios de aceitação
- testes a executar
- itens fora do escopo
- limite explícito do diff
- limites de custo e duração
- regra de parada.
```

Um modelo muito forte em um rápido borrão não produz um bom resultado: produz uma deriva mais cara.

> **Limitações de execução em vez de disciplina por si só.** Vários ajustes Claude Code Transformam esta regra em
> guarda-fogo: `maxEffortLevel` limita o esforço a todos os fornecedores; uma regra deny que aponta para um parâmetro de ferramenta
> (por exemplo, `Agent(model:opus)`) proíbe lançar um subagente a um modelo caro; `CLAUDE_CODE_SUBAGENT_MODEL`
> fixa o modelo dos subagentes; `fallbackModel` lista até três modelos de retrocesso testados em ordem (a)
> periodizar, ver supra); `/usage` ventila o consumo por skill, subagente, plugin e servidor MCP ; e
> hooks veem o esforço corrente via `$CLAUDE_EFFORT`. Lado API, as **Grupo de orçamento** (beta
> `task-budgets-2026-03-13`, `output_config.task_budget`) dão ao modelo um orçamento de Tokens para todo o ciclo.
> Agente: É um orçamento. **indicativo**, não um teto, que deve ser duplicado com um `max_tokens` e um teto
> lado cliente; seu valor é parte da rápida rendição, pelo que muda a 'cache'. Verifica na doc a lista
> Modelos que são suportados antes de utilizar na Fable 5.2 ou Opus 5.5.

<!-- section: s-46 -->
#### Checklist pré-flight antes de qualquer tarefa > $2 de custo estimado

Antes de iniciar Fable 5.2, GPT‑6.2 Astra, Opus 5.5 com esforço elevado ou uma sessão multiagente, valida este checklist. Cada casa sem marcar é uma razão para NÃO iniciar e descer em modelo ou scope.

□ Objectivo formulado em 1 frase com verbo de acção □ Não objectivos explícitos (pelo menos 2) □ Ficheiros e módulos relevantes identificados (vias exatas) □ Critérios de aceitação de teste definidos □ Ordem de teste dirigida lista para executar □ Diff máximo aceitável fixado (por exemplo: < 300 linhas) □ Limite máximo de custo fixado (por exemplo: $5) e limite de duração (por exemplo: 30 min) □ Regra de paragem formulada [deter se [condição]] □ O plano foi validado pelo humano ANTES do modo write □ Worktree dedicado criado se a tarefa tocar > 5 Ficheiros □ Contexto mínimo preparado (não existe "toda a repos")

Estimativa dos custos rápidos (ordem de magnitude):

| Tarea               | Modelo      | Tokens estimados      | Custo estimado |
|---------------------|-------------|---------------------|-------------|
| Feature 3 Ficheiros  | Sonnet 5.5  | ~20K in / ~5K out   | ~$0.09      |
| Bug de múltiplos módulos   | Opus 5.5    | ~50K in / ~10K out  | ~$0.40      |
| Migração-quadro de trabalho | Fable 5.2   | ~200K in / ~50K out | ~$3.60      |
| Auditoria Astra max     | GPT‑6.2 Astra | ~100K in / ~20K out | ~$1.60      |

Se o custo estimado exceder 3x o custo do modelo inferior para a mesma tarefa, a diferença de qualidade deve ser justificada pelo risco. "Mais inteligente" não é uma justificação.
---

