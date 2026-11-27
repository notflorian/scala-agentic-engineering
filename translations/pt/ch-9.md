<!-- section: chapter -->
# 9. Integrações MCP prioritárias

<!-- section: s-1 -->
## Indispensables

| MCP                        | Função                                                                                 |
|----------------------------|--------------------------------------------------------------------------------------|
| **Metals MCP**             | Inteligência Scala ao vivo: compilação, diagnósticos, tipos, símbolos                      |
| **ScalaSemantic MCP**      | Grafio semântico Scala via SemanticDB: usos, hierarquias, call paths, givens     |
| **JetBrains MCP**          | Explique IntelliJ, arquivos abertos, ações IDE                                      |
| **Sourcebot**              | Pesquisa/discovery codebase multi-repos                                             |
| **Codebase-Memory MCP**    | Knowledge graph estrutural persistente polyglotte , sobretudo Java/Kotlin/cross-service |
| **GitHub MCP**             | Issues, PR, Actions, checks                                                          |
| **Context7**               | Documentação actualizada da libs                                                         |
| **Playwright MCP**         | Validação UI se o app web                                                             |
| **Sentry MCP**             | Diagnostic bugs prod                                                                 |
| **Postgres read-only MCP** | Plano, migração, petições                                                         |
| **ast-grep MCP**           | Investigação estrutural e refatores específicos                                           |

Características operacionais (que serão revistas no momento da instalação a evolução do transporte e as versões):

| MCP                    | Transporte típico               | Versão mínima notável                   | Manutenção de Junho 2026                                    |
|------------------------|---------------------------------|--------------------------------------------|----------------------------------------------------------|
| Metals MCP             | stdio; standalone desde 1.6.6 | Metals 1.5.3 (integrado), 1.6.6 (standalona) | Activo (Scalameta)                                        |
| ScalaSemantic MCP      | MCP local                       | SemanticDB necessário para o coração do índice  | Jovem; especializado Scala, para benchmarker no repo      |
| JetBrains MCP          | servidor integrado IDE             | IntelliJ 2025.2 (servidor)                  | Activo (JetBrains)                                        |
| Sourcebot              | HTTP                            | —                                          | Activo                                                    |
| Códigobase-Memory MCP    | MCP local                       | —                                          | Activo; Hybrid LSP documentado para Java/Kotlin, no Scala |
| GitHub MCP             | HTTP remoto ou stdio local     | —                                          | Activo (GitHub oficial)                                  |
| Context7               | HTTP distant                    | —                                          | Activo                                                    |
| Playwright MCP         | stdio                           | —                                          | Activo (Microsoft)                                        |
| Sentry MCP             | HTTP distant                    | —                                          | Activo (Sentry oficial)                                  |
| Postgres read-only MCP | stdio                           | —                                          | Variável de acordo com a implementação da auditoria de antes de prod     |
| ast-grep MCP           | stdio                           | —                                          | Activo                                                    |

> **Evolução do protocolo MCP para conhecer** : **MCP 2026-07-28 é agora a especificação publicada de referência**.
> O coração se converte em stateless: retirada das sessões de nível protocolario, de `Mcp-Session-Id` e, para essa revisão,
> `initialize` / `notifications/initialized` Cada pedido transporta em `_meta` a informação
> `server/discover` permite descobrir a identidade, as versões e as capacidades do cliente.
> capacidade do servidor. A revisão também formaliza o quadro de **Extensões**, **Tasks[** para o trabalho longo,
> **MCP Apps**, a autorização alinhada OAuth/OIDC e uma política de depreciação; `Roots`, `Sampling` e
> `Logging` para um novo desenvolvimento, **Objetivo 2026-07-28**, mas mantém testes de compatibilidade.
> 2025-11-25 até que todos os clientes/servidores utilizados sejam migrados. Claude Code 2.1.27x generalizou seu cliente.
> MCP v2 e Negociação 2026-07-28 as ligações HTTP diretas, incluindo Bedrock, Vertex, Foundry e
> instalações
> Sem telemetria; subsiste um modo legacy. Portanto, não supõe que todos os pares MCP de um ambiente.
> recente
> Migraram ao mesmo tempo.

> **MCP Events continua a ser uma extensão proposta, não o núcleo do protocolo.** ChatGPT sabe experimentar assinaturas.
> `events/list`, `events/subscribe` e `events/unsubscribe` com entrega webhook em servidores em MCP 2.0
> (`2026-07-28`). Isto é útil para os fluxos de trabalho de eventos • Comentário criado, incidente, mensagem, mudança
> de estado ? mas não faça que uma integração crítica dependa dessa extensão enquanto seu estado e suporte.
> Não se estabilizam os clientes/servidores.

<!-- section: s-2 -->
## ChatGPT e Codex : funções MCP Não confundir

É necessário distinguir **ChatGPT web**, as **clientes Codex locais** e o **Agentes API**. MCP descreve uma relação cliente/servidor; o fato de que um produto também pode expor uma API de orquestra não o converte em servidor MCP.

| Superfície                                                       | Função MCP e transporte                                                                            | Autenticação                                                                      | Leitura / escrita                                                                          |
|---------------------------------------------------------------|---------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **Codex CLI / extensão IDE / host Codex de ChatGPT Desktop** | **Client MCP** ; STIDO local e Streatable HTTP remoto; configuração compartilhada no mesmo host | Bearer, OAuth, CIMD e DCR; `codex mcp login` para OAuth                             | Dependendo das ferramentas do servidor, do sandbox e das autorizações; da leitura e escrita possíveis: |
| **ChatGPT web Pro**                                           | Cliente de apps MCP **distantes**                                                                   | OAuth de acordo com o app                                                                     | Developer modo limitado às ferramentas `read` / `fetch`                                           |
| **ChatGPT Web Business / Enterprise / Edu**                   | Cliente de aplicações MCP remotos; **full MCP em beta**                                                | OAuth + controle workspace/admin                                                     | Ferramentas de leitura e acções `write` / `modify` possíveis para MCP personalizados        |
| **OpenAI Agentes API**                                         | Cliente MCP hospedado ou a partir do ambiente; HTTP ou STDIO de acordo com a origem da conexão         | Headers/Bearer, caixa forte de credentials ou variáveis ambientais segundo o transporte | `allowed_tools` permite reduzir explicitamente a superfície exposta.                          |

> **Documentação OpenAI Em contraposição.** O Help Center detalhado mantém **Pro =
> `read`/`fetch`** e reserva o full MCP read/write a Business/Enterprise/Edu, enquanto a página de desenvolvedor"
> Generalista agora afirma que o developer mode dá o full MCP read/write a Plus e Pro. Enquanto ambos.
> fontes oficiais não convergem, mantenha o quadro anterior como hipótese conservadora e **detecta os
> capacidade real exposta pela conta/workspace** antes de desenhar um fluxo de trabalho de escrita.

**Codex já não é um servidor MCP.** `codex mcp-server` e o binário `codex-mcp-server` foram removidos. Uma integração que quer pilotar Codex como serviço deve migrar para **Codex App Server**, que usa seu próprio JSON- RCP e ** não é MCP ** ; Codex continua ao mesmo tempo que consome servidores MCP externos como cliente.

ChatGPT web não se liga diretamente a `localhost`. Para um MCP local, privado ou on-premise, explícalo através do **Secure MCP Tunnel** em vez de abrir o servidor publicamente. Duas limitações de superfície permanecem importantes: **Agente de moda não usa as apps MCP personalizadas**, et **Deep Research** só os utiliza em `read` / `fetch`.

<!-- section: s-3 -->
### Governar catálogo MCP como uma API versão

Quando um administrador aprova uma aplicação MCP em ChatGPT, o produto conserva um **snapshot aprovado ferramentas e seus itens**. Adicionar, retirar ou modificar uma ferramenta no servidor não faz automaticamente a nova superfície activa. Por conseguinte, uma evolução incompatível pode romper chamadas até que um administrador tenha revisto e publicado o catálogo, e ChatGPT não garante actualmente um alerta pró-activo sobre esta deriva.

```text
changement de nom / schéma / permission / nouvel outil MCP
→ diff de surface
→ review
→ validation admin
→ publication
```

Esta regra ** completa**, sem substitui-la, a política de segurança desta seção: versões encraviadas, permissões mínimas, logs de ferramentas e separação leitura/escrita.

<!-- section: s-4 -->
## Knowledge graph MCP para Scala, Java e Kotlin

**Sourcebot não é um knowledge graph.** Resta a camada de busca/discovery: encontrar rapidamente arquivos, símbolos, usos de texto e extractos relevantes, especialmente em vários respirarios. Um knowledge graph responde a outra classe de perguntas: relações entre símbolos, rotas de chamada, hierarquias, dependências estruturais e impacto de uma mudança.

<!-- section: s-5 -->
### Scala: Priorizar ScalaSemantic, completar com Metals

Para um depósito principalmente Scala, **ScalaSemantic MCP** é o melhor candidato identificado para a camada da camada da semântica da semântica. Não só reconstrue o código de um AST Tree-sitter: seu índice principal é alimentado por **SemanticDB**, portanto, mediante símbolos já resolvidos no momento da compilação. Apresenta pedidos globais adaptados aos agentes, em particular usos exatos, assinaturas, hierarquias, overloads, `call_path`, busca de givens e rastreamento de cadeias de implicits.

```text
Sourcebot
→ « où est X ? »
→ « quels fichiers parlent de Y ? »

ScalaSemantic MCP
→ « quels sont les usages exacts de ce symbole ? »
→ « quel chemin d'appel relie A à B ? »
→ « qui étend ce trait ? »
→ « quels givens peuvent produire T ? »
→ « de quels implicits dépend ce given ? »

Metals MCP
→ « quel est le type réel ici, maintenant ? »
→ « ce fichier compile-t-il ? »
→ « quels diagnostics le compilateur retourne-t-il ? »
→ « quels tests échouent ? »
```

ScalaSemantic e Metals são **adicionais**. ScalaSemantic é index-wide e excelente para as relações globais; Metals Continua a ser a fonte da verdade ao vivo para o buffer atual, a apresentação compilar, os diagnósticos, a compilação e os testes. SemanticDB representa principalmente o último estado compilado: se o código acaba de ser modificado sem recompilação, Metals pode ser mais fresco.

Também não apresenta ScalaSemantic como um Neo4j/RDF genérico: é mais precisamente um ** semantic code graph MCP**. Algumas operações continuam sendo aproximações de alto nível e não reproduzem necessariamente toda a lógica do compilador a um call local preciso. Em caso de contradição sobre a resolução efetiva de um tipo, de um overload ou de um given, **Metals/scalac ganha**.

<!-- section: s-6 -->
### Java e Kotlin: Codebase-Memory torna-se muito mais interessante.

**Codebase-Memory MCP** Construi um knowledge graph persistente de funções, classes, call chains, estradas HTTP e ligações cross-service desde Tree-sitter. Sua segunda passada **Java e Kotlin**. Nestas duas linguagens, portanto, é mais pertinente do que em Scala para as questões estruturais de código base-escalera.

```text
Java / Kotlin

Sourcebot
= recherche et discovery

Codebase-Memory MCP
= knowledge graph persistant
= call graph
= impact analysis
= architecture
= routes et relations cross-service

IntelliJ / LSP
= sémantique live et arbitrage local
```

Em um código base JVM poliglotis, a distribuição recomendada passa a ser:

```text
Scala pur
→ Sourcebot + ScalaSemantic + Metals

Java/Kotlin
→ Sourcebot + Codebase-Memory + IntelliJ/LSP

Scala + Java + Kotlin / microservices
→ Sourcebot
→ ScalaSemantic pour la sémantique Scala
→ Codebase-Memory pour la topologie polyglotte et cross-service
→ Metals / IntelliJ pour arbitrer la sémantique live
```

O critério determinante não é o de se tem uma base gráfica? ** que informação cria as bordas** :

```text
Tree-sitter
→ structure syntaxique et résolution heuristique

SemanticDB
→ symboles résolus par le compilateur Scala

LSP / presentation compiler
→ état sémantique live du code courant
```

Portanto, para o desenvolvimento Scala, prefere uma arista SemanticDB a uma arista reconstruída apenas desde o texto quando ambos estão disponíveis.

<!-- section: s-7 -->
### Efeito sobre o context engineering

Esta camada de gráfico é especialmente útil se você evita carregar dezenas de ficheiros. Um subagent read-only pode interrogar ScalaSemantic ou Codebase-Memory e depois rastrear apenas alguns caminhos, símbolos e testes `file:line` ao pai:

```text
question d'impact
→ subagent isolé
→ knowledge graph / semantic graph
→ 5–10 relations pertinentes
→ vérification Metals / IntelliJ si nécessaire
→ résumé < 1–2K tokens
→ parent
```

Isto aumenta o`isolation_ratio` e reduz diretamente o * context rot*. Em vez disso, não ativa mais de um MCP gráfico por princípio: benchmarkelas em dez tarefas reais e guarde apenas aqueles que reduzam o número de arquivos lidos, os tokens injetados ou os erros de compreensão.

<!-- section: s-8 -->
### Alternativas a conhecer sem padronizar-las

`agent4s` é um toolbox Scala MCP Interessante, baseado em Scalameta com SemanticDB opcional, que expõe, entre outras coisas, referências, hierarquias, dependências e call graph. Merece um bake-off se ScalaSemantic não cobrir uma classe de tarefas, mas não adiciona as duas primeiras.

Joern constrói um verdadeiro **Código Property Graph** muito rica para a análise de segurança e dados de fluxo, mas sua fonte frontal não aponta Scala A análise do bytecode JVM Scala é possível , à custa da perda de uma parte das abstrações fonte; portanto, reserva Joern a auditorias especializadas em vez do contexto cotidiano de Claude Code.

<!-- section: s-9 -->
## Metals MCP : a ferramenta Scala desaparecidos na maioria dos stacks

É provavelmente o MCP o mais subutilizada pelos desenvolvedores Scala. **Metals (language server Scala) atraca um servidor MCP da v.1.5.3** (Maio) 2025), y **v1.6.6 Osmium3 Março 2026) acrescentou um servidor MCP standalone** que gira sem um editor aberto, portanto, disponível diretamente por Claude Code o Codex CLI em terminal. Esta mesma versão adicionou o suporte de **templates Twirl de Play**, diretamente relevante para o seu estack.

As ferramentas expostas incluem, entre outras coisas: `compile-file`, `compile-full`, `compile-module`, `test`, `inspect`, `get-docs`, `get-usages`, `get-source`, `import-build`, `find-dep`, as ferramentas Scalafix, `glob-search` y `typed-glob-search`. A ferramenta chave para os riços agenticos permanece **`compile-file`** : o agente escreve, recolhe o arquivo, recebe os erros do tipo/implicits e corrige imediatamente, sem pagar um ciclo `sbt compile` completa em cada iteração.

Articulação com JetBrains MCP e ScalaSemantic:

```text
JetBrains MCP     = contexte IDE quand IntelliJ est ouvert (fichiers ouverts, inspections, run configs)
ScalaSemantic MCP = relations globales SemanticDB : usages, hiérarchies, call paths, givens
Metals MCP        = feedback compilateur live pour les agents terminal, même IDE fermé
```

Os três são complementares, não redundantes. Claude Code longa ou as tarefas lançadas fora do IED (CI local, worktree paralelo), Metals MCP é o que transforma o agente adivinha os tipos.

> **Versão Metals** : **Metals 1.6.9 é publicada desde 14 Setembro 2026 ** (após 1.6.8 do 23 Julio).
> MCP traz o `glob-search` a todos os módulos, a resolução dos resultados dos testes entre módulos, a
> sugestão de`import-build` quando não se encontra nenhum objetivo de edifício e um adesivo contra bloqueios sobre erros
> Isto é diretamente útil para os monorepos de Play/sbt Multi- Moyenses: toma 1.6.9 no mínimo para
> Existem milharestonas Metals 2, mas não as padronizam até que ocorra uma liberação estável.

<!-- section: s-10 -->
## Exemplo: fivela de teste-correção agentica em `compile-file`

Esqueleto ZIO do ciclo que faz o valor de Metals MCP O agente corrige contra o **compilador**, não contra sua própria confiança, com um borne de torres que materializa a regra 2 xadrez → stop Oh!

```scala
import zio.*

final case class Diagnostic(file: String, line: Int, message: String)
final case class CompileResult(success: Boolean, diagnostics: List[Diagnostic])

// Abstraction du client MCP : l'implémentation parle JSON-RPC à Metals en stdio
trait MetalsMcp:
  def compileFile(path: String): Task[CompileResult]

def fixLoop(
    llm: LlmClient[Task],
    metals: MetalsMcp,
    path: String,
    maxRounds: Int = 3
): Task[Either[CompileResult, CompileResult]] =

  def round(n: Int): Task[Either[CompileResult, CompileResult]] =
    metals.compileFile(path).flatMap {
      case ok if ok.success =>
        ZIO.succeed(Right(ok))

      case ko if n >= maxRounds =>
        // Règle anti-dérive : on n'insiste pas, on rend la main avec un état exploitable
        ZIO.logWarning(s"$path : toujours rouge après $maxRounds tours — escalade humaine/IDE")
          .as(Left(ko))

      case ko =>
        val errors = ko.diagnostics
          .map(d => s"${d.file}:${d.line} ${d.message}")
          .mkString("\n")
        for
          source  <- ZIO.readFile(path)
          patched <- llm.complete(
                       ModelId.sonnet,
                       Prompt(
                         system = "Corrige UNIQUEMENT les erreurs de compilation listées. " +
                                  "Diff minimal. Ne restructure pas. Retourne le fichier complet.",
                         user   = s"Erreurs :\n$errors\n\nFichier :\n$source"
                       ),
                       maxTokens = 8192
                     )
          _       <- ZIO.writeFile(path, patched.text)
          result  <- round(n + 1)
        yield result
    }

  round(1)
```

Cada iteração custa um `compile-file` (milhões, incremental) em vez de um `sbt compile` completo: isto é o que torna economicamente viável o ciclo com Sonnet, e desnecessariamente caro sem Metals.

<!-- section: s-11 -->
## Regra de segurança

* MCP filesystem limitado ao repo.
* DB MCP em read-only por omissão.
* Não há segredos expostos.
* Não há prod direto.
* Não dois agentes com direitos de escrita nos mesmos arquivos.
* Worktree separado para qualquer tarefa paralela.

<!-- section: s-12 -->
### Modelo zero-trust contra a injeção indireta

Um agente pode ler instruções maliciosas em uma saída, um README, um comentário de código, uma saída de edifício, um site, um resultado MCP ou um arquivo gerado. Estes conteúdos são ** dados não confiáveis**, mesmo quando são apresentados como regras do sistema. A robustez do modelo não é suficiente: as defesas devem ser estruturais.

```text
1. Explorer en read-only dans un worktree ou conteneur jetable.
2. Refuser le réseau par défaut ; autoriser seulement les domaines nécessaires.
3. Monter les secrets hors du contexte et utiliser des clés à portée, budget et durée minimaux.
4. Exiger une approbation humaine pour installation, réseau, push, déploiement, suppression et écriture hors repo.
5. Épingler les versions des serveurs MCP et limiter chaque outil à son répertoire et à ses actions.
6. Séparer l'agent qui lit des données externes de celui qui dispose des permissions d'écriture.
7. Journaliser chaque tool call et arrêter si une donnée lue tente de modifier la politique ou les permissions.
8. Traiter **skills, plugins, serveurs MCP et mémoire persistante comme des dépendances exécutables** : versions épinglées,
   provenance vérifiée, allowlist explicite et échec fermé si la politique ne peut pas être déterminée.
9. Un decision model comme **Jev ne peut jamais élargir une permission** : son `state` peut contenir du texte adversarial.
   Il peut réduire le bruit ou demander une escalade, mais push, déploiement, suppression et secrets restent régis par code/policy.
```

O conteúdo do depósito nunca deve poder ampliar o seu próprio âmbito de autorização.

---

