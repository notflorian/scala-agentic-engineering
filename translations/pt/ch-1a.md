<!-- section: chapter -->
# 1A. Vibe coding, programação assistida por IA e programação agêntica

O termo **vibe coding**, popularizado por Andrej Karpathy em fevereiro de 2025, descrevia originalmente uma prática em que o programador delega quase toda a escrita do código, aceita as sugestões do modelo e avalia o trabalho principalmente pelo resultado observável. A abordagem funciona para protótipos descartáveis, explorações e interfaces de baixo risco. Como método de produção, ela é insuficiente para sistemas de negócio, financeiros, sensíveis à segurança ou que precisam durar.

Dois detalhes sobre a origem do termo ajudam a entender o debate em 2026. Karpathy explicou que o tuíte era, em parte, uma brincadeira voltada a projetos descartáveis de fim de semana. Ele nunca propôs o vibe coding como método de produção. Já em fevereiro de 2025, Simon Willison traçou uma distinção de referência. Aceitar diffs sem ler é vibe coding. Revisar cada linha e entender o que ela faz é programação assistida por IA. O problema surge quando se dispensa a revisão. No fim de 2025, o termo **vibe engineering** passou a descrever o trabalho de profissionais experientes que ganham muita velocidade com agentes LLM e mantêm plena responsabilidade pelo software. Revisão, testes e responsabilidade são o que distingue essas duas práticas e o foco deste guia.

É preciso distinguir três formas de trabalho:

| Moda                        | Controle Humano                                                     | Uso adequado                                     | Risco Principal                                           |
|-----------------------------|---------------------------------------------------------------------|--------------------------------------------------|------------------------------------------------------------|
| **Atividade Vibe Coding**             | Fácil, validação por sensação e execução                       | Protótipo, spike, ferramenta pessoal jogável        | Dívida invisível, segurança, compreensão perdida            |
| **Engenharia AI-assistida** | O desenvolvedor desenha e relaciona, o modelo acelera                 | Trabalho diário em código mantido              | Automatizar decisões que deveriam permanecer humanas    |
| **Agência de codificação**          | O agente explora, planeja, modifica e testa em um perímetro limitado | Tarefas bem especificadas com testes e permissões | Dériva, círculo, ação fora do perímetro, injeção indireta |

Para um idoso ScalaO objetivo não é “mais de vibe coding”, mas uma **Engenharia Agente Controlada ** :

```text
especificação verificável
→ contexto mínimo, mas suficiente
→ plano
→ permissões proporcionais
→ execução instrumentada
→ compilação e testes determinísticos
→ revisão independente
→ validação humana
```

**Prova-drivida de Engenharia Agente** • O SDD fixa o contrato, a engenharia harness torna suas limitações executáveis, e as provas determinam se a mudança pode avançar. Para cada exigência, combina uma prova independente (teste de comportamento, inspeção, referência ou medida de tempo), o SHA realmente validado e os riscos não cobertos. Uma afirmação do agente, uma revisão sem provas ou um simples estatuto verde não constituem um oráculo. O ciclo termina após a validação do artefato implementado, não simplesmente para a fusão (segmento 15B).

<!-- section: s-1 -->
## O que mostra o estado da arte em 2026

1. **Só o modelo não determina o sucesso.** Harness, ferramentas disponíveis, debugger, qualidade do contexto e testes podem alterar os resultados quase tão tanto quanto a escolha do modelo. As comparações entre os resultados publicados por fornecedores são válidas apenas se o harness, o esforço, as ferramentas e o protocolo são comparáveis.
2. **Os benchmarks curtos sobreestimam a autonomia longa.** Os agentes obtiveram bons resultados em saídas isoladas, mas caem fortemente nas evoluções multi-file, longas e históricas. SWE-EVO, por exemplo, visa tarefas muito mais longas do que SWE-bench e destaca essa diferença.
3. **SWE-bench Verified não é mais um bom padrão único.** OpenAI documentou problemas de contaminação e testes defeituosos. Para o código, prefere um portfólio que inclui tarefas auditadas SWE-bench, Terminal-BenchAvaliações e, acima de tudo, um referencial interno. Scala Não é público.
4. **A produtividade humana não é garantida por uma boa pontuação agente.** Um estudo aleatório do METR sobre desenvolvedores experientes em seus próprios depósitos observou um atraso com as ferramentas de início 2025. Os dados recolhidos depois sugerem uma melhoria possível, mas METR julga o novo teste não confiável devido a meio de seleção e medidas difíceis com vários agentes concorrentes. 2026. A medição local do tempo até a fusão permanece indispensável. ordem de tamanho da atualização de fevereiro 2026 Estimação pontual de aproximadamente 18 % de aceleração na subcoorte histórica (intervalo de confiança −38 % à +9 % e aproximadamente 4 % dos novos participantes (IC)
   −15 % à +9 %) — um sinal muito ruído para concluir, que o METR preferiu tratar refundando o protocolo em vez de publicar um único número. Detalhes decisivos para a condução: no ensaio inicial, os participantes estimaram em média ter sido ~20 % mais rápido graças à IA enquanto eles eram ~19 % mais lenta — a diferença entre percepção e medição é a razão pela qual este guia exige métricas locais (custo por mudança aceite, tempo até a fusão) em vez do sentimento das sessões.
5. **As instruções de depósito são úteis apenas se estiverem operacionais.** As pesquisas sobre `AGENTS.md` encontram um benefício quando o arquivo contém comandos, convenções não padrão, invariantes e regras de parada. Uma longa descrição geral da arquitetura pode aumentar o contexto sem melhorar o resultado.
6. **O multi-agente não é um multiplicador automático de inteligência.** Ele ajuda quando as subtrações são realmente independentes, que as responsabilidades e os arquivos são separados e que um agente raiz sintetiza. Em um estado mutável compartilhado, ele aumenta conflitos, custos e erros de coordenação.
7. **Um patch tecnicamente correto não é suficiente para avaliar um agente.** Também mede o cumprimento do âmbito, regras de interrupção e convenções, a qualidade do plano, a capacidade de relatar a incerteza e o custo de revisão humana. Dois agentes que passam os mesmos testes podem ter um valor muito diferente se um gerar duas vezes mais rework ou mudanças fora do perímetro.
8. **A memória, as habilidades e as regras persistentes se tornam uma superfície de engenharia.** Os agentes capazes de fazer evoluir a sua própria memória, suas habilidades ou seu roteamento nunca devem auto-promover essas mudanças. Qualquer evolução persistente deve ser difável, editável, testável, revisado e reversível antes de ativação.
9. **Uma grande janela de contexto não remove o *Contexto ROT*.** As avaliações 2026 distinguir a capacidade física da janela e a qualidade efetiva de uso do seu conteúdo: com a mesma tarefa, mais tokens podem deteriorar recuperação, cumprimento de restrições e raciocínio muito antes do limite máximo. 1M tokens”, mas manter um **Set de trabalho mínimo e decisivo**Os subagentes isolados são uma parada estrutural: eles consomem localmente muito contexto e apenas transmitem ao parente um resultado condensado.

Conclusão: o nível de fronteira aumenta a superfície de tarefas possíveis, mas a qualidade de engenharia ao redor do agente continua a ser o fator controlável mais importante.

<!-- section: s-2 -->
### Complementos metodológicos

> **SWE-bench Pro não substitui SWE-bench Verified.** OpenAI Agora, acredita-se que cerca de 30 % das tarefas de
> SWE-bench Pro também são defeituosas: testes muito rigorosos, exigências ocultas ausentes do prompt, cobertura
> insuficiente ou enganosa. auditoria do 8 Julho 2026
> (Pedro automatizado em linha: 27,4 % dos 731 Tarefas públicas marcadas; anotação por cinco engenheiros seniores: 34,1 %)
> Além disso, conduziu OpenAI à **Retirar explicitamente a sua recomendação** Avaliação de codificação de
> referência — um sinal mais forte do que a única estimativa. Portanto, o portfólio de avaliação certo combina vários eixos
> Em vez de um novo
> Classificação única.

| Ásia para medir                | Avaliação útil                 | O que ela revela                                                                               |
|------------------------------|----------------------------------|-------------------------------------------------------------------------------------------------|
| Correção de Depósito Clássico | SWE-bench, com auditoria de tarefas | Capacidade de reparação em fontes isoladas                                                       |
| Tarefas originais longas       | **A DEPSWE**                      | Contaminação reduzida, verificadores escritos para aceitar várias soluções válidas           |
| Cooperação iterativa      | **SWE-Interação** e SWE-Together | Descoberta de intenção, memória de restrições, necessidade de correções humanas            |
| Exploração de depósito         | **SWE-Exploração**                  | Localização em linha e eficácia do contexto                                     |
| Ciclo completo                | **SWE - Ciclo**                    | Reconstrução do ambiente, implementação e geração de testes em uma mesma trajetória |
| A realidade do seu trabalho       | **O Benchmark Scala Privado**        | Preço e qualidade em Play, Pekko, Tapir, Spark, implicitos, serialização e real build          |

Para uma tarefa de código, medir o **Custo por mudança aceite** Para o controle da entrega, o **Custo por mudança implementada e estável** (a seção 15b) Não a taxa de sucesso bruto:

```text
custo por alteração aceita
= tokens + latência + minutos de trabalho humano + CI + retrabalho + defeitos não detectados
```

Use uma unidade comum para cobrir esses custos (por exemplo, euros com um custo horário explícito), ou mantenha os componentes separados. Os tokens e minutos não se adicionam diretamente. Para o custo até a produção, adicione implementação, validação de tempo de execução, rollback/hotfix e defeitos observados durante uma janela fixada antes da medida. Não se considera estável apenas uma mudança terminando esta janela.

Não busque uma "produtividade de IA" global. Stratifica ao mínimo as medidas por **greenfield, manutenção, legacy, bugfix, migração, refactor e código crítico** • Os estudos 2026 Obter resultados contraditórios precisamente porque eles nem sempre medem as mesmas tarefas, desenvolvedores ou custos de revisão.

<!-- section: s-3 -->
### Um benchmark verde ainda não é um dif fusível

A avaliação do METR em 296 PRs gerados por agentes descobriu que o grau SWE-bench deu em média **24,2 Mais pontos de sucesso** que os manuseiros encarregados de avaliar se a mudança foi realmente útil e fusível; cerca de metade dos PRs que passavam os testes não teriam sido mergulhados. A amostra se refere apenas a três depósitos, modelos anteriores à geração mais recente e um único teste sem iteração no feedback manuseiro: isso não é um limite fundamental de capacidade, mas isso invalida a equivalência naiva `tests du benchmark passants = changement acceptable`.

Em tarefas longas, a SlopCodeBench também observa uma acumulação de duplação, verbosidade e erosão estrutural à medida que os pontos de verificação se encaixam. Uma rápida demanda de qualidade reduz alguns defeitos no início sem eliminar o seu crescimento. O bom regime de prova, portanto, cumula quatro barreiras independentes:

```text
contrato de negócio explícito
→ reprodução que falha antes da correção
→ testes determinísticos, propriedades e testes de mutação
→ revisão humana responsável do diff, do escopo e da facilidade de manutenção
```

Os pontos de referência servem para roteamento e experimentos; nunca devem se tornar uma autorização de autonomia ou de fusão.

> **Diferença entre escrever e entregar.** O trabalho de papel NBER *Escrever código vs. código de transporte* Observe, em mais de
> 500 000 Desenvolvedores GitHubA expectativa é que o aumento da atividade seja muito maior para os cometidos do que para os
> O estudo continua observativo com aparência: não demonstra efeito causal
> Assim, limite o WIP à capacidade de revisão e entrega, e medir até à produção.

<!-- section: s-4 -->
### Guarda de produção para o vibe coding

Estudos empíricos de 2026 em aplicativos realmente “vibe codificados” encontram famílias de defeitos recorrentes: lógica provisória deixada em produção, entradas não filtradas, segredos expostos, esquecimento de restrições ao longo das torres e otimização local que deteriora o sistema global. Um modelo mais forte ou melhor rápido reduz esses defeitos, mas não os elimina.

> **ordens de tamanho medidos em 2026.** A auditoria de 200 Aplicações verdadeiramente “vibe codificadas” e implementadas
> (1 471 Vulnerabilidades validadas) encontram pelo menos uma vulnerabilidade em **90 % dos depósitos**Entre os quais, mais de três
> Quartos de gravidade alta ou crítica; o controle de acesso quebrado aparece em 75,5 % dos depósitos, ou aproximadamente 20×
> A linha de base OWASP 2025. Um escaneamento independente de 1 400+ aplicações leva à mesma ordem de tamanho (65 %
> Tem pelo menos um problema de segurança. 58 % pelo menos uma vulnerabilidade crítica, 400+ Segredos expostos.
> A análise das causas raízes classifica esses defeitos em três famílias — **Memória** (Os conflitos esquecidos entre
> e as torres, **Objetivo** (Optimização local que deteriora o sistema global) e **Conhecimento** (Patrocinados perigosos
> Reproduídos): exatamente os três mecanismos que os gatos deterministas e a revista humana deste guia devem
> interromper, uma vez que nenhum remoto os corrigirá de forma duradoura.

```text
Protótipo por vibe coding
→ sem dados nem chaves de produção
→ testes funcionais + segurança + desempenho + facilidade de manutenção
→ revisão humana do diff e das dependências
→ migração para o fluxo agêntico controlado
→ só então: implantação
```

Uma sessão de codificação vibe nunca deve impulsionar diretamente na produção, mesmo quando a demonstração parece funcional. **Mudança do regime de prova**Não é apenas um passo para o gato.

