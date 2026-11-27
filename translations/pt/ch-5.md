<!-- section: chapter -->
# 5. Fluxo de trabalho padrão para uma tarefa de negócio em Scala

<!-- section: s-1 -->
## Passo 0 : enquadre humano

Antes da IA, você escreve ou esclarece:

```text
Objetivo:
Comportamento atual:
Comportamento esperado:
Restrições de negócio:
API pública a preservar:
Arquivos que provavelmente serão afetados:
Testes direcionados:
Validação no ambiente de execução:
Risco:
Critério de aceitação:
```

Note os requisitos profissionais e invariantes importantes (`REQ-01`, `REQ-02`, etc. Para cada requisito, declara o teste ou o teste esperado antes da implementação; um requisito sem oráculo deve estar explicitamente marcado sem cobertura e arbitrado. No PR, associa requisito, comando/teste, resultado, SHA validado e limites do teste. A matriz de rastreabilidade pode permanecer muito curta para um ticket trivial.

`Validation harness` deve nomear ** antes do modo de write** os testes que o próprio agente possa executar: compilação seletiva, testes unitários/integração, ScalaCheck, escalafmt, eventualmente Stryker4s e controlo do diff. Se ainda não souber como demonstrar que a mudança é correta, a tarefa não está pronta para ser delegada.

Sem isso, você paga os modelos para descobrir o problema em vez de resolvê-lo.

> **Posicionamento contra o estado da arte 2026 (Spec-Driven Development land)** : este enquadre é exatamente o que
> a indústria foi formalizado sob o nome de SDD, convertido no contrapeso dominante no coding vibe
> artefato mais rentável produzido pelo ser humano quando o agente escreve o código. A ferramenta (GitHub Spec Kit, OpenSpec,
> AWS Kiro, notação EARS para requisitos de teste) pode estruturar esse fluxo de trabalho, mas não é obrigatório: este
> Guia prático já a variante ** spec-anchored** (a spec marco e sobrevive à tarefa, o código + os testes permanecem)
> a fonte da verdade), que é a postura recomendada para o código de ofícios existente, por oposição ao
> ** spec-as-source** (o humano só edita a spec), ainda experimental.
> campo: o nível de detalhe da spec deve seguir a *crítica* do código de definir um script descartável é
> O desperdício, a subestabilidade de um contrato público é uma deriva garantida.
>
> **Seleccionar ferramentas SDD sem framework-sprawl.** A paisagem SDD
> Agora supera os trinta frameworks (Spec Kit, OpenSpec, Kiro, BMAD-METHOD, GSD, Tessl...).
> prática que daí se depreende: **GitHub Spec Kit** para o greenfield (constituição → specify → clarify → plano →
> checklist → tasks → analyze → implement → converge, com passos de controle opcionais) ;
> **OpenSpec[** para brownfield iterativo das specs versionadas na repo com *delta markers[* por mudança, a
> posição mais próxima da variante spec-anchored deste guia; **AWS Kiro** se quiser a notação EARS integrada
> e o ecossistema AWS. Nenhum é um pré-requisito: se `AGENTS.md` + o pacote de análise anterior + as gatas CI
> (secção 15A) já estão fazendo o trabalho, adicionar um framework SDD acrescenta contexto, não qualidade.
> negociável: a spec vive no repo e se repassa como código a spec mantida fora de versão torna-se um segundo.
> Fonte da verdade divergente.

> **Dos arneses que não devem ser confundidos.** Um papel SDD publicado no 31 agosto 2026 propõe uma distinção útil entre
> **technical harness** (modelo, ferramentas, contexto, permissões, testes) e **methodological harness** (spec, papéis,
> responsabilidades, revisão e autoridade de liberdade). **confirma** a estrutura deste guia: melhorar
> Claude Code, Codex ou MCP não substitui a disciplina de especificação e validação humana.
> No entanto, principalmente conceitual e se apoia amplamente na literatura cinzenta; utiliza essa distinção.
> como quadro de concepção, não como prova empírica de que um quadro SDD, dado melhora a produtividade.

> **Primeira informação sobre a prática real.** O estudo CMU/Google
> and as Praticad Despertad! (declarative, não replicada) observa que os profissionais experientes já aplicam SDD de
> **selectiva, especialmente para novas funções ou alterações riscos**, com speces redigidos pelos agentes a partir de uma intenção
> humaine puis relues, et une vérification surtout par tests écrits par les agents. Le défaut principal est la
> **deriva silenciosa spec ↔ código[** quando não existe nenhum plano de manutenção; os reembolsos Thoughtworks acrescentam
> a * instrução bloat* (espejos e contextos que crescem até que o agente perde o fio). Isto confirma dois.
> Regras deste guia: dosagem por criticidade, e spec versão e repassada. Adiciona apenas uma terceira regra:
> ** um teste escrito pelo agente não valida sua própria spec** ; mantenha o teste de reprodução que falha antes do adesivo.
> e a mutação de testes (secção 5, etapa 4) No lado de ferramentas, **`/speckit.converge`** relee o código frente a
> `spec.md`, `plan.md` e `tasks.md` e **añade apenas as tarefas que faltam a `tasks.md`** É um controlo de
> coerência útil após a implementação, **no um oráculo** : nem os testes independentes nem a revisão humana devem
> ser suprimido com o pretexto de que Spec Kit anuncia Converged!

<!-- section: s-2 -->
#### Templato de spec operacional (copiar e colar)

Este template materializa a variante spec-anchored do guia. Vive no repo (por exemplo `specs/TICKET-123.md`) e é revisto como código.

<!-- section: s-3 -->
# SPEC: [TICKET-[123]] [Tiro curto]

<!-- section: s-4 -->
## 1Objetivo (1 oração, verbo de ação)

[Ex: "Adicionar uma taxa de desconto por etapas de quantidade ao serviço de DiscountService"]

<!-- section: s-5 -->
## 2 Não objetivos (explicito, anti-derivado)

- [Ex: "Não modificar o cálculo de desconto existente por código de desconto"]
- [Ex: "Não tocar o API público do módulo pricing"]

<!-- section: s-6 -->
## 3 Comportamento esperado (regras de trabalho, numeradas)

1. [Regla 1: se a quantidade >= 10 for entregue 5%]
2. [Regla 2: se a quantidade >= 50 for entregue 12%]
3. [Regla 3 : Os degraus não se acumulam, aplica-se o mais alto]

<!-- section: s-7 -->
## 4 Limitações técnicas

- API público que deve ser conservado: [firmas exatas]
- Serialização JSON : [sem alterações / adicionar campo X com backward compat]
- Desempenho: [não há consulta DB adicional no hot path]
- Concorrência: [estado imutável / atomicidade requerida]

<!-- section: s-8 -->
## 5. Ficheiros provavelmente afetados

- `src/main/scala/.../DiscountService.scala`
- `src/test/scala/.../DiscountServiceSpec.scala`

<!-- section: s-9 -->
## 6. Testes de aceitação (critérios de "dona")

| Não se aplica aos veículos das categorias A e B. | Teste esperado |
|----------------------|-----------------|
| REQ-01: limiar 10 | Teste unitário: 9 → 0 %, 10 → 5 % |
| REQ-02: limiar 50 | Prova unitária: 49 → 5 %, 50 → 12 % ; propriedade entregue ≤ 12 % |
| REQ-03: não acumulação | Teste de não retrocesso na acumulação; entrega por código de desconto sem alterações |
| REQ-04: contrato JSON | Teste de compatibilidade |
| REQ-05: desempenho | Medição do número de pedidos DB sobre a hipótese de integração |

- [ ] Mutação testeing: pontuação / mutantes importantes para justificar nos arquivos afetados
- [ ] Resultados relacionados ao SHA e aos requisitos; excepções e riscos residuais explícitos

<!-- section: s-10 -->
## 7 Riscos e mitigações

| Risco               | Probabilidade | Impacto | Mitigation                      |
|----------------------|-------------|--------|---------------------------------|
| [Arrondi BigDecimal] | Média       | Cima   | [Usar RoundingMode.HALF_UP] |

<!-- section: s-11 -->
## 8. Definição do done (checklist final)

- [ ] Compile sans warning
- [ ] Testes de objetivos verdes
- [ ] scalafmtCheckAll passage
- [ ] Revisão do segundo modelo realizada
- [ ] Diff < [N] linhas
- [ ] Não existem ficheiros fora do escore modificado

Nível de detalhe adaptado à criticidade:

- Script descartável → Seções 1, 2, 6 O suficiente
- Contrato público / dinheiro / segurança → todas as secções obrigatórias

---

<!-- section: s-12 -->
## Passo 1 : pesquisa específica

Use neste comando:

1. **Sourcebot** para localizar arquivos, usos, testes.
2. **IntelliJ** para verificar símbolos, tipos, hierarquias.
3. **Context7** se uma API externa ou uma versão recente está envolvida.
4. **Qwen local[** para produzir uma exposição informativa.

Prompt Qwen:

```text
Analise estes arquivos e produza:
- resumo do fluxo de negócio
- classes e métodos envolvidos
- invariantes a preservar
- testes existentes
- riscos
- ambiguidades
- um prompt claro para o Claude Code

Ainda não proponha uma correção.
```

---

<!-- section: s-13 -->
## Passo 2: plano pela lengüeta writer, sem alterações

Prompt writer (Codex ou Claude Code):

```text
Você é o agente responsável pela implementação desta tarefa.

Objetivo:
[objetivo]

Restrições:
- diff mínimo
- nenhuma alteração de API pública sem aprovação explícita
- preservar os comportamentos existentes
- adicionar ou adaptar testes
- trabalhar em etapas pequenas
- explicar os riscos
- fazer alterações somente após aprovação

Comece explorando o código e propondo um plano.
```

Regra dos documentos: **sem planos, sem write modo**. O plano deve enumerar os ficheiros a modificar, os ficheiros a não tocar, a estratégia de teste, os riscos e o tamanho esperado do 'diff'.

---

<!-- section: s-14 -->
## Passo 3: implementação por pequenos diffs

Prompt:

```text
Execute apenas a etapa 1.
Deixe as demais etapas como estão.
Mantenha o diff mínimo.
Após a alteração, informe:
- arquivos alterados
- motivo de cada alteração
- comando do teste direcionado
```

Para Scala, evita os grandes refatores automáticos. 30 à 300 linhas de diff quando possível. As voltas de campo e os estudos recentes sobre os PRs agentes convergem para pequenos e bornados PRs, mais fáceis de ler e menos propensos ao xadrez CI. A nível organizacional, o estudo da implantação Claude Code / Copilot CLI na Microsoft (arXiv, julho) 2026, dezenas de milhares de engenheiros) medida ~24% de PRs se estrelam mais nos adotadores da mesma forma que o efeito é real, mas materializa-se nos PRs *Revisables*Não em diffs gigantes.

---

<!-- section: s-15 -->
## Passo 4: validação IntelliJ + testes

Agentes LLM são conhecidos por escrever testes "happy path" (testes que passam mas não comprovam os casos de erro ou os limites). Scala/SBT :

```plaintext
scalafmtCheckAll
compile
Test / compile
testOnly <TestCiblé>
IntegrationTest / testOnly <TestCiblé>
```

Então só se o risco o justificar:

```plaintext
test
IntegrationTest / test
```

> **Nota sbt :** configuração `IntegrationTest` é **Despreciada desde sbt 1.9.0** em benefício de um subprojecto
> dedicado (por exemplo, um módulo `it` que `dependsOn(core % "test->test")`) ou testes taggés. Se o seu projecto o usar.
> Ainda, os comandos anteriores ainda são válidos, mas nunca permite que um agente migra esta configuração por si só
> Esse é exatamente o tipo de mudança. `build.sbt` que deve passar por uma validação explícita.
> módulo, &
> Você vai diretamente a um subprojeto `it`. Pense também em dar ao agente a ordem mais rápida disponível:
> `sbt --client` (ou Bloop) evita pagar o início da JVM por cada iteração do ciclo de teste-correcção, este
> que
> Na **sbt 2.x**, `sbt` já utiliza o modo cliente-servidor nativo `sbtn`
> Por omissão; `sbt --client` continua a ser uma forma explícita. Medir o início no projecto real: migração 1.x → 2.x
> e a alteração da `build.sbt` requerem validação humana (ver secção 15A).
>
> Sim. `serverConnectionType` está configurado para `Tcp`, sbt 1.4.0 à 2.0.6 é
> vulnerável a uma execução de código não autenticada através do BSP. Remove esta configuração ou passa pelo menos a **sbt 1.13.0
> o 2.0.7**. O transporte local por omissão (socket Unix ou named pipe) não será afetado.
> prioridade antes de expor o servidor sbt a um IDE, agente ou recipiente remoto.

<!-- section: s-16 -->
#### Otimização sbt para os riços agentivos

A velocidade do ciclo compilado-test é a primeira alavanca de produtividade de agentes. Configuração recomendada na `.sbtopts` (repo):

<!-- section: s-17 -->
# .sbtopts laço otimizado para riços agenticos

```plaintext
-J-Xms2g
-J-Xmx8g
-J-XX:+UseZGC
-J-XX:+UseStringDeduplication
-Dsbt.supershell=false
-Dsbt.color=false
-Dsbt.log.noformat=true
```

Explicação das opções:

- `UseZGC`: opção de medição contra o G1 por defeito no depósito real; não promete um ganho sistemático nem pausas sempre inferiores a 1 ms
- `supershell=false` e `color=false`: reduzir o ruído nas saídas que o agente separe (menos tokens, menos context rot)
- `noformat=true`: Ídem, saídas brutas mais fáceis de parser

Sob sbt 2.x, `sbt` já lança o cliente nativo por defeito; `sbtn` permanece uma entrada explícita útil:

<!-- section: s-18 -->
# Primeiro lançamento (inicie o servidor)

`sbt`

<!-- section: s-19 -->
# Apelações posteriores do agente (início quase instantâneo)

`sbtn "compile"` `sbtn "testOnly *DiscountServiceSpec"`

Configuração do Servidor no `project/server.sbt`:

```scala
// Keep the build server on a local transport.
Global / serverConnectionType := ConnectionType.Local
```

O transporte local é normalmente o defeito: **não mostra o servidor sbt em TCP** Para acelerar os agentes. `build.sbt` Apenas para mascarar recompilações ou verificações: `onChangedBuildSource := IgnoreSourceChanges`, `Test / fork := false` e a desactivação de Scaladoc pode tornar o resultado não representativo da CI ou modificar os comportamentos dos testes. Preferir o módulo e as suites (`project`, `testOnly`) sem alterar sua semântica. **sbt 2.x, `test` É incremental e pode voltar a usar os seus resultados na 'cache'** : utiliza `testFull` para uma validação completa antes de uma PR ou em CI.

**Benchmark antes/depois no seu depósito.** Comparado com JVM e as mesmas opções, em pelo menos dez ciclos de compilação incrementais + testes seletivos: latência média, p95, reinícios sbt, pressão de memória e estabilidade de testes. Não apresente poupança cifrada em outro projeto como garantia.

Para Play Framework ou projetos de vários módulos:

```plaintext
sbt "project api" compile
sbt "project api" "testOnly *DiscountServiceSpec"
sbt "project integration" "testOnly *OrderFlowSpec"
```

O ponto essencial continua a ser: não só pede à IA a prudência do teste, dá voltas aos testes. Os protetores deterministas atingem as instruções textuais.

Escolha as validações segundo o risco real, sem apilar ferramentas desnecessárias:

| Risco Scala/JVM | Teste relevante |
|------------------|-------------------|
| Cálculo do trabalho | ScalaCheck, limites, mutações de testeing |
| Compatibilidade binário / TASTy | MiMa / TASTy-MiMa quando pertinente |
| REST / JSON | Testes de contratos, esquemas e compatibilidade |
| Concorrência e efeitos | Ordenação controlada, cancellation, timeout, liberation des ressources |
| Spark | Datasets deterministas, nulls, esquema, partições, idempotence |
| Desempenho JVM | JMH ou benchmark objetivo reprodutível |
| Arquitetura | Escalafix / fitness functions em bytecode ou fontes |
| Segurança | SAST que cobrem realmente Scala, SCA, segredo digitalizado e testes de autorização |

**CodeQL Java/Kotlin não demonstra um cobertor Scala** : verifica a lista de linguagens compatíveis e experimenta o analisador escolhido sobre defeitos conhecidos. Não assimilou um scanner de dependências a uma análise das fontes.


<!-- section: s-20 -->
### Valor probatório dos testes gerados

Uma prova escrita pelo mesmo agente que a implementação não é um oráculo independente. Os trabalhos recentes apontam que os agentes produzem frequentemente testes de observação ou de impressão sem asserções discriminatórias; aumentar o número de testes pelo prompt não basta para melhorar a taxa de resolução. Outras avaliações por mutação mostram que as suites verdes detectam mal defeitos realistas gerados por agentes, e que sua eficácia se deteriora quando o código evolui mesmo sem alterações semânticas esperadas.

Portanto, para um bugfix mantém o teste mais rentável:

```text
1. adicione um teste de reprodução mínimo
2. verifique se ele falha no commit-base pelo motivo esperado
3. aplique a correção
4. verifique se o teste e depois a suíte relevante passam
5. varie o oráculo: propriedades, casos-limite, testes metamórficos ou mutantes direcionados
6. peça revisão do teste antes da implementação quando o domínio for crítico.
```

Não estabeleça um limiar de mutação universal que incite a jogar a métrica da velocidade da velocidade. Comparar a pontuação no perímetro em causa, requer uma justificação para cada mutante que sobrevive importante e sou sobretudo o ** delta de mutação pontuação**, retrocessos escapadas e retornos de revisão. Um teste que não podia falhar antes do adesivo não demonstra o adesivo.

**A etapa de endurecimento (Mutação Testing):** Uma vez que a IA escreveu os testes e são verdes, valida sua robustez com Stryker4s :

```plaintext
sbt "project api" stryker
```

Uma pontuação baixa ** pode** revelar provas insuficientes, mas também mutantes equivalentes, não relevantes ou mal direcionados. Examina primeiro os mutantes sobreviventes, o seu impacto profissional e as exclusões; não adiciona afirmações artificiais para aumentar a pontuação. Se um mutante importante permanecer vivo, devolve o relatório ao agente pedindo um ** teste de comportamento observável independente do adesivo **, e depois reiniciar os testes seletivos.

---

<!-- section: s-21 -->
#### Passo 5: Obligar a verificação antes da declaração de terminação

Agentes LLM Adiciona esta instrução sistemática ao final de cada aplicação rápida:

Antes de declarar que esta tarefa terminou, você DICE:

1. Executar o comando de compilação e mostrar o resultado
2. Executar o teste- alvo e mostrar o resultado
3. Verificar o 'diff' da base aprovada, as alterações committadas e não committadas e os ficheiros não seguidos
4. Listar os ficheiros modificados com a razão de cada alteração
5. Se um passo falhar, corrigir e começar de novo 1 Não diga "dona" a menos que os 5 pontos anteriores estejam satisfeitos.

Para automatizar estas verificações, usa os programas comuns da secção 5 (hooks) CI da secção 15A. O hook `PostToolUse` compila somente: `Test/compile` Os resultados das suites e o diff completo devem estar associados ao SHA candidato, e o CI um Stop hook não é um teste de completação; não deve impedir uma parada de bloqueio.

Variante para tarefas críticas (segurança, dinheiro, contrato público):

Antes de declarar que esta tarefa terminou, executa e mostra:

1. sbt compila (zero erro, zero warning novo)
2. sbt "testOnly *SpecCible" (todos verdes)
3. sbt scalafmtCheckAll (formateo conforme)
4. Diff base → candidato e estado Git completa (apenas os ficheiros do plano)
5. Verifique se o 'diff' NÃO contém: TODO, FIXME, println de debug, importação não utilizada, mudança de assinatura pública não pedida Mostra o resultado de cada passo. Se um passo falha, corrige e reanuda. Não declare "dona" antes de os 's' 5 passos são verdes.

---

<!-- section: s-22 -->
## Passo 6 : self-review pelo writer

Prompt:

```text
Revise seu próprio diff antes de encaminhá-lo ao revisor independente.
Liste:
- riscos de negócio
- casos-limite
- testes ausentes
- alterações desnecessárias
- arquivos que precisam de revisão manual
- hipóteses adotadas
```

Este passo frequentemente elimina erros evidentes antes de revisão externa. ** Nunca vale a pena a aprovar.** : o agente que escreveu o diff compartilha as mesmas hipóteses que sua implementação e não pode constituir a gate final. O writer pode limpar; um contexto fresco de **Otras famílias de modelos** deve apresentar suas conclusões independentes.

---

<!-- section: s-23 -->
## Passo 7: revisão independente por outra família de modelos

Prompt reviewer: **Opus 5.5 Medium** se Codex escreveu , **GPT‑6.2 Sol Medium** Se Claude escreveu. Sube a High para um PR arriscado e para Astra Light/Fable Low apenas se a capacidade adicional for justificada:

```text
Atue como revisor sênior independente de código Scala/JVM.

Revise o SHA exato da ponta da PR em relação à base de merge, à especificação aprovada, aos critérios de aceitação e ao AGENTS.md.
Trabalhe em uma nova sessão somente leitura. Não modifique a implementação. Forme sua própria avaliação
antes de consultar o raciocínio do agente que fez as alterações.

Priorize a correção funcional, as invariantes preservadas, as regressões, a compatibilidade, a qualidade dos oráculos de teste,
o tratamento de erros, a segurança no uso de recursos, a concorrência, o desempenho, a segurança e os desvios de escopo.

Para cada constatação que exija ação, informe a gravidade, o arquivo e a linha, o SHA revisado, o requisito ou a invariante violada,
um cenário concreto de falha ou reprodução, a menor correção plausível e a incerteza remanescente.
Distinga defeitos verificados de hipóteses. Ignore preferências de estilo e refatorações sem relação com a tarefa.
Apresente apenas um parecer conciso e constatações sustentadas por evidências. Nunca invente constatações.
Nunca aprove nem faça o merge da PR por conta própria.
```

Variante com classificação de gravidade máquina-explotável ? melhor para classificação e um gato alimentado apenas por findings validados independentemente (ver exemplo de descodificação tipo na secção 12) :

```text
Classifique cada achado com exatamente um destes rótulos:
- BLOCKING        : bug de negócio, perda de dados, vulnerabilidade ou quebra de contrato público
- REGRESSION_RISK : comportamento existente possivelmente alterado, caso-limite sem cobertura
- STYLE           : legibilidade, convenção, nomenclatura — nunca bloqueante
- OUT_OF_SCOPE    : melhoria válida fora do chamado — ignore nesta PR

Retorne somente JSON válido:
{
  "findings": [ { "severity": "...", "file": "...", "message": "..." } ],
  "summary": "..."
}
```

A regra de gate associada: `BLOCKING` e `REGRESSION_RISK` devem ser tratados ou impugnados explicitamente antes da mermelada; `STYLE` é opcional; `OUT_OF_SCOPE` Parte no backlog, nunca no diff corrente.

Estas marcas continuam a ser ** hipóteses de revisão**, não feitos. Cada retorno bloqueado deve levar um teste verificável: ficheiro e linha, contrato violado, reprodução, teste que falha ou regra estática precisa. Sem teste, passa para a classificação humana; a auto-etiqueta de um modelo nunca deve bloquear por si só uma merda. Esta validação evita os falsos positivos caros e os riços do autor IA ↔ repassar IA que queimam créditos sem nova informação.

O pattern recomendado continua a ser: **um writer, um reviewer da outra família**A revisão cruzada é uma hipótese de trabalho, não uma garantia: um estudo *Cross-Model LLM Code Review* sobre 116 problemas algoritmicos com Opus 4.7 / GPT-5.5 observa um ganho Codex → Claude71,6 → 89,7 % de sucesso) e uma diminuição Claude → Codex (91,4 → 82,8 % quando a revisão reesscreve o programa sem efectuar os testes. Não deduz nenhuma classificação dos modelos actuais em Scala. O revisor detecta e justifica; o writer corrige após a classificação. Medirá os verdadeiros/falso positivo, defeitos faltados e retrocessos introduzidos pelas correcções. Após uma correção menor, revisão dirigida das mudanças e invariantes; revisão completa apenas se o risco ou o alcance mudou.

> **Esforço e limites da revisão.** Sobre 90 adesivos Django, um estudo *How Much Effort Does an AI Code Reviewer
> Need?* Encontrar Opus 5.5 Medium não inferior a High numa margem predefinida de 15 pontos, a um custo médio
> inferior em aproximadamente 20 %. Mesmo High aceita 45 % dos adesivos considerados incorrectos pelo oráculo reforçado; alguns
> As marcas continuam a ser questionáveis.Bench-v2 (584 defeitos reutilizáveis associados a PRs) confirma que a cobertura
> Os defeitos pelos agentes são limitados. Esses resultados consentem Medium para o dia a dia, mas não demonstram nem
> a equivalência universal Medium/High ou a eficácia dos modelos atuais em Scala. Sem gate autonome LLM.

 Por defeito: **Suelo 6.2 Medium escreve → Opus 5.5 Medium review**, ou ** Opus 5.5 Medium/High escrito → Suelo 6.2 Medium review**- Luna/Haiku são utilizados para tarefas mecânicas; Astra/Fable só se mobilizam em escalada. `Ultra` reserva-se às missões desvinculadas em eixos independentes.

---

<!-- section: s-24 -->
## Passo 8: correção seletiva

Nunca pede ao revisor que aplique automaticamente todas as suas sugestões. Selecciona os reembolsos úteis e volta a **writer original**:

```text
Aprovo estes achados da revisão:
[lista]

Corrija apenas esses pontos.
Ignore as sugestões opcionais.
Mantenha o diff mínimo.
Execute novamente os testes direcionados.
```

** Deixe de rever quando os critérios são verdes.** Um passo corretivo após o repassar é o defeito; um segundo só é justificado por um finding `BLOCKING` / `REGRESSION_RISK` novo e fundamentado, um teste vermelho ou um teste determinista. Não utilize um prompt do tipo lago itero ainda até que seja perfeito a: para além do melhor checkpoint, o agente acaba frequentemente inventando mudanças para satisfazer a demanda e pode degradar o diff.

Se necessário um novo passe, compara sistematicamente o novo diff com o checkpoint anterior e mantém a versão que melhor satisfaz **spec + testes + scope**, não a versão mais recente.

Se você delega a correção pós-PR para Codex (Goal mode, Heartbeat ou Cloud), `/steward` ou PR Steward (secção 12), transfere explicitamente o ownership do ramo, com o SHA de saída, a spec e as únicas devoluções autorizadas. Deixe de controlar antes de o writer original ser recuperado. Qualquer novo commit recupera as validações pertinentes; a revisão independente deve referir-se ao diff final, não ao SHA antes da correção automática.

<!-- section: s-25 -->
## Passo 9: Guardafuegos anti-deriva agentes

Adiciona regras de paragem explícitas, que reduzem os diffs desnecessários, os riços de correção e os créditos queimados:

```text
Pare imediatamente se:
- o agente tocar em um arquivo fora do plano sem explicação
- o agente alterar build.sbt, plugins.sbt, resolvers ou versões sem aprovação explícita
- o mesmo erro de compilação ocorrer 2 vezes
- os testes direcionados falharem 2 vezes por causas diferentes
- o diff ultrapassar o tamanho anunciado
- a correção começar a alterar a arquitetura em vez de resolver o ticket
- o agente tentar uma escrita destrutiva, push, implantação, compartilhamento externo ou ação sobre segredos
  sem autorização explícita.
```

Neste caso, você não volte a subir o fix de it. Mais bem pede:

```text
Pare. Resuma o estado exato:
- arquivos alterados
- hipóteses adotadas
- erro atual
- comandos executados
- próxima ação mínima proposta
Não faça alterações.
```

> **Retomar a mão sem pagar o dobro da mesma exploração.** Três mecanismos Claude Code a conhecer:
>
> - **Checkpoints** : cada prompt cria um checkpoint (snapshot de arquivos antes de cada edição pelas ferramentas de
>   Claude). `Échap Échap` ou `/rewind` restaura a conversa, o código ou ambos em um ponto anterior, incluindo
>   Depois de fechar o terminal. Limite conhecido: apenas as mudanças feitas através das ferramentas de edição de Claude.
>   Ainda não os lançados em Bash, um checkpoint não substitui nem um commit nem o worktree.
> - **`/compact` não lave uma má hipótese** : a compacção resume a conversa e * conserva* Assim,
>   Quando o agente retorna duas vezes à mesma pista falsa, o desfile é:
>   `/clear` e depois um rápido estreito com o novo estado não uma compacção adicional.
> - **Permissões em deny-by-default** : `settings.json` aceita regras allow / ask / deny; combina um allowlist
>   estreitamente com deny explícito (red, arquivos críticos, push) em vez de aprovar à mão em ciclo.
>   Esta é a versão produz as regras de não automação da secção 3.
> - **Auto modo por omissão** : a partir de 14 agosto 2026, o modo de auto é o modo de permissão por omissão das notícias.
>   Sessões nos planos Pro, Max e Team. Seu classificador reduz as interrupções, mas não é uma gate.
>   trabalho: verifica que as suas regras `deny` sobre `build.sbt`, migrações, fluxos de trabalho CI e push permanecem activas (os)
>   *hard deny rules* do carro forma bloqueado sem ter em conta as excepções `allow`, e mantém os hooks abaixo.

<!-- section: s-26 -->
#### Claude Mods: Quando superar os hooks clássicos

Desde **Claude Code 2.1.287**, um **Mod** é um plugin cujos hadlers JavaScript/TypeScript sloven no processo Claude CodeUn handler pode **Observar, reescrever ou aceitar** um evento: tool call, prompt, torre, controle ou renderização da interface da interface. É uma camada diferente de MCP : um MCP fornece ferramentas de um processo/serviço externo; um Mod pode mudar o comportamento do próprio arness. **3 Outubro 2026**, a versão 2.1.288 Já acrescenta. `$.ui.selection()` e vários adesivos Mods/plugins: API como **jovem e evolutivo**, e clique na versão Claude Code para todo Mod que se torna crítico em seu fluxo de trabalho.

| Necessidade                                                                                                 | Primitiva a preferir |
|--------------------------------------------------------------------------------------------------------|----------------------|
| Repetir as instruções / um método                                                                 | **Skill**            |
| Acesso a um sistema ou ferramenta externa                                                        | **MCP**              |
| Bloquear, autorizar ou registrar um evento com uma regra simples                                        | **Settings hook**    |
| UI interativa, estado compartilhado entre eventos, controle local, intercepção/reescrita de um evento | **Mod**              |

A Mods API pode gravar comandos, tools e subagentes, ligar a um modelo, ler o estado e o uso da sessão, manter uma store partilhada, ler/escrever arquivos, iniciar um processo, ligar a HTTP ou a MCP, e comunicar com outras sessões. Os Mods funcionam com seus hooks no terminal JetBrains Os elementos da unidade de controle da qualidade não são devolvidos a todas as superfícies headless/cloud, nem ao código- tab de Claude Desktop.

**Não substitua os três hooks shell a seguir por um Mod apenas porque possível.** Para as gatas simples e deterministas (`build.sbt`, migrações, diff max, testes obrigatórios), um settings hook continua a ser mais pequeno, mais legível e mais fácil de auditar. Use um Mod apenas se precisar de um estado cross-event, um fluxo de trabalho interativo, um fluxo de trabalho interativo ou uma interceptação que o hook clássico expressa mal.

> **Fronteira de confiança muito mais ampla.** Um Mod s
> Prompts, tool calls, variáveis de ambiente e settings, iniciar processos ou fazer rede, reescrever uma
> solicitação e gastar quota através de chamadas modelo. Os processos que inicia são ** fora do sandbox Bash** de
> Claude.
> Um Mod instalado também pode aprovar alguns tool calls que uma regra `ask` ou um `PreToolUse` usuário teria
> Parem.
> Portanto, as permissões Claude não são um sandbox em torno do código do plugin.

Antes de instalar ou promover um Mod de terceiros:

```text
1. Verifique a origem no marketplace e fixe a versão ou commit quando possível.
2. Leia .claude-plugin/plugin.json, hooks/hooks.json, o módulo register.*, bin/ e .mcp.json, se houver.
3. claude plugin validate ./mon-mod
   → examine sobretudo as linhas hooks: e calls: sem executar o Mod.
4. claude --plugin-dir ./mon-mod plugin details <nom>
   → verifique o inventário real dos componentes.
5. claude plugin test ./mon-mod
   → testes determinísticos de hooks, sem sessão, login ou rede.
6. Se o plugin tiver avaliações, execute claude plugin eval ... antes de promovê-lo.
7. Faça o primeiro teste com --plugin-dir em um worktree descartável. Use --safe-mode para recuperação.
```

Para uma organização, um verdadeiro controlo deve viver na **managed settings** (`allowManagedModsOnly`, ordem dos plugins geridos, `disableAllHooks` e no Mod integrado `cc-plugin-sec-default`, não na boa vontade de um Mod utilizador. Para uso sozinho, a regra equivalente é simples: **Built-ins / código pessoal auditado > plugin comunitário opaco**, e nenhuma atualização automática de um Mod sensível sem reletura do diff da versão.

<!-- section: s-27 -->
#### Configuração comum dos hooks Claude Code / Codex

Separada **feedback local** e **gate de validação**. Um hook num pedido `Edit` não vê necessariamente as escrituras Bash, MCP ou IDE; não pode garantir o confinamento. Suprímase `ai-guard.sh` baseado na busca de cadeias num comando: os caminhos dinâmicos, symlinks e execuções indiretas escapam a este filtro. Aplica as permissões/sandbox da secção 12 ; controla os caminhos realmente modificados no diff final. Os hooks não são um substituto da CI independente.

Exemplos para um projeto de confiança, `.claude/settings.json` :

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$(git rev-parse --show-toplevel)/scripts/ai-compile-check.sh\"",
            "timeout": 120
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$(git rev-parse --show-toplevel)/scripts/ai-stop-audit.sh\""
          }
        ]
      }
    ]
  }
}
```

Y `.codex/hooks.json` :

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "apply_patch",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$(git rev-parse --show-toplevel)/scripts/ai-compile-check.sh\"",
            "timeout": 120
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$(git rev-parse --show-toplevel)/scripts/ai-stop-audit.sh\""
          }
        ]
      }
    ]
  }
}
```

Os dois arneses chamam os mesmos programas (os eventos e payloads próprios das ferramentas permanecem separados). Codex requer releer e aprovar as definições de hooks não geridos (`/hooks`); não desactivar este controlo. Um worktree pode carregar os hooks do checkout principal; verifica as fontes realmente executadas. Os hooks e os programas de confiança devem ser protegidos da escrita pelo agente; em ambiente gerido, os colocar fora do worktree. Não executa hooks de projecto não auditados.

Script `scripts/ai-compile-check.sh` (feedback de compilação apenas; pode ser desactualizado se muito frequente):

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
logFile=$(mktemp)
trap 'rm -f "$logFile"' EXIT
# Capture the process exit code, not a pattern in the logs.
if sbt --client "Test/compile" >"$logFile" 2>&1; then
  exit 0
else
  exitCode=$?
  printf 'sbt Test/compile failed (exit %s)\n' "$exitCode" >&2
  tail -n 40 "$logFile" >&2
  exit 2
fi
```

O resultado baseia-se no código de retorno da sbt, mesmo sem linha `[error]`. `Test/compile` Compile os testes mas não as execute. `grep` ou um pedido RTK como árbitro do sucesso; conserva o código de retorno do comando original. Na presença de várias sessões, não lança compilações concorrentes ao mesmo servidor sbt.

Script `scripts/ai-stop-audit.sh` (chamada não bloqueada, comum aos dois arneses):

```bash
#!/usr/bin/env bash
set -euo pipefail
# No transcript heuristics and no forced retry on legitimate blockers.
cat >/dev/null
printf '%s\n' '{"systemMessage":"Completion requires a fresh validation receipt for the exact candidate SHA and independent CI; report blockers without claiming done."}'
```

O Stop hook nunca procura um comando na transcrição: uma menção de `testOnly` Não obrigue o agente a continuar quando um invariante ou um orçamento imponha uma parada. Para completar, requer o relatório estruturado de `scripts/ai-validate.py` (secção 11) e os checks CI Os testes locais produzidos sob a identidade do agente são úteis para o diagnóstico, mas falsificaveis: a política de CI, seus scripts e seus resultados devem viver numa fronteira independente do agente.

Um Mod Claude privilegiado ou um hook não confiável pode modificar o oleoduto; conserva as restrições externas e os controlos administrados. A gate final não pode ser modificada e então auto-aprobado pelo writer. Os hooks podem ser ignorados ou não são ativados de acordo com a superfície; verifica os acontecimentos, caminhos e permissões eficazes antes da adoção.

<!-- section: s-28 -->
#### Protocolo de recuperação quando o agente ciclo

Um ciclo- agente (o mesmo erro, a mesma correcção, o mesmo erro) é um modo de falha diferente do fracasso simples. A escalada do modelo não a corrige. Aqui está o protocolo na 4 passos:

**Paso R1 - Parada e extração de estado (0 token adicional)**

Pare o agente imediatamente.

Não mude nada. 5 Pontos:

1. Ficheiros modificados até agora (diff desde a base aprovada + git status)
2. Hipótese atual sobre a causa
3. O que foi tentado e por que falhou.
4. A próxima acção mínima que proporá
5. O que você não tem certeza.

**Paso R2 Diagnóstico humano com IED (5-10 min)**

Use IntelliJ para verificar o que o agente não pode ver:

- O tipo de expressão real (Ctrl+Shift+P / Tipo info)
- A resolução efectiva de um implícito/given (Ctrl+B sobre implicit)
- A hierarquia de tipos esperada vs produzida
- O breakpoint debugger sobre o comportamento inesperado

O objetivo é encontrar a informação estrutural que falta ao agente.

**Paso R3 a sessão fresca com contexto restrito**

/clear Novo prompt com o AMO:

- Objectivo (1 frase)
- O ficheiro ou método exacto em causa
- O erro exato (copiado desde IDE, não desde transcrição)
- A informação estrutural encontrada em R2
- "Só propõe uma mudança mínima. Compile e tente."

**Paso R4 Se falhar após R3, escalada de modelo**

Só agora se justifica a escalada de Sonnet → Opus → Fable, pois o contexto é limpo e o problema está bem levantado.

Anti-pattern absoluto: Reanudar o mesmo modelo no mesmo contexto com a esperança de um resultado diferente. É a definição do ciclo.

> **Reanclaje periódico, o desfile medido contra a deriva longa.**
> A pesquisa 2026 sobre o agente drift ? (degradação do comportamento medida em trajetórias longas e longas)
> sistemas multi-agentes) converge em três famílias de mitigações: consolidação episódica da história em
> Resumos estruturados, ancoragem comportamental adaptativa (reinyectação periódica da carta e do objetivo)
> corrente) e enrutado tendo em conta a deriva. Tradução imediata para suas sessões:
> - ** reinjete a carta** (objectivo, não objetivos, invariantes, definição de doação) em cada marco e a volta de
>   Subagento não só ao primeiro prompt: uma restrição que já não está na janela recente já não existe;
> - ** generaliza o ficheiro de estado** (`MIGRATION_STATE.md`) em todo o período de sessões longo, não apenas às missões.
>   Fable: é a âncora que sobrevive às compações e às reposições;
> - ** circuito breakers de duplo limiar**: um aviso sobre a repetição de um mesmo tool call ou de uma mesma
>   erro e depois parada dura na segunda repetição idêntica , em vez de um único limiar brutal;
> - **sessão fresca em caso de ciclo** : a escalada do modelo não corrige um ciclo (secção 3) ; `/clear` +
>   estado + carta relegada, sim.

---

