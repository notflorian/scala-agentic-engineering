<!-- section: chapter -->
# 15A. CI/CD para fluxos de trabalho agênticos

A CI é o juiz final determinista do princípio orientador a condição de adaptá-lo aos PRs agentes, que têm modos de falha específicos: testes que não podem falhar, diffs fora de modelo, riços caros.

<!-- section: s-1 -->
## As quatro gatas específicas dos PRs agenticos

```text
1. Gate de tamanho e escopo: diff base → candidato, arquivos protegidos, tamanho e número de arquivos
2. Gate de qualidade dos testes: suítes realmente executadas + pontuação de mutação e mutantes relevantes conforme o risco
3. Gate de revisão: achados comprovados BLOCKING / REGRESSION_RISK resolvidos ou decididos por uma pessoa
4. Gate de orçamento: todo job que chama um LLM tem um timeout E um limite de custo
```

Dois eixos complementares a considerar uma vez que a base das quatro gatas foi estabelecida:

- **Control de deriva de arquitetura** :: A tecnologia Radar de Thoughtworks (abril) 2026 indica que o uso intensivo de agentes acelera a deriva entre o código real e a arquitetura de referência, e recomenda que se combinem controles deterministas (fitness functions, ArchUnit, que analisa o bytecode JVM e, portanto, funciona também em Scala compilado) com uma avaliação LLM periódica. Uma regra ArchUnit o módulo `api` não depende da implementação da mesma. CI custa menos que uma volta de agente e detenha uma deriva estrutural que nem escalafmt nem Stryker4s Não o veja.
- **Control de duplicação** : SlopCodeBench (secção 1A) mida uma acumulação de duplicação através dos checkpoints agentes; um scan type jscpd (detector de copiado colado que token as fontes Scala) nos ficheiros afetados transforma este sinal em métrica seguida ou mesmo em gate. A duplicação é o defeito menos visível em revisão humana e um dos mais caros em manutenção alocados.

Sobre GitHub, **Copilot Code Review ou Codex Código Review pode ser adicionado como sinal automático**, mas não substitui nenhum destes gates. Uma revisão do bot não é uma aprovação humana; verifica as regras GitHub Reales. Começa por uma revisão prévia solicitação ou na abertura, e depois reserva a revisão após a correção às mudanças que a justifiquem e aos novos SHA que requerem uma validação independente.

**Claude Approvals não é um teste de qualidade.** Uma regra `claude: approves` não ativa por si só Código de Revisão; `seats: 1` pode contar ao autor e `seats: 0` pode permitir uma merda sem leitura humana. GitHub pode também contar a aprovação do bot na sua quota de reviews. Para o fluxo de trabalho deste guia, guarda `claude: comments` No início, os aprovadores humanos independentes em equipe, e uma merda humana em solitário. Nunca usa um classificador probabilista como o único árbitro de uma mudança crítica.

A presença de `.claude/approvals.yml` pode desativar as revisões automáticas nos caminhos cobertos, mesmo em modo observa: para mantê-las, referência `claude/code_review` nas regras (por exemplo, baixo `advisory` Uma condição Approvals não lê os resultados de CI : conserva compila, testes, escalafmt, segurança e mutação testing como required checks GitHub Separados. Em equipe, protege o ramo-alvo e a política com CODEOWNERS, proíbe os bypass aos agentes e invalida as anteriores autorizações quando o diff muda. Só torna obrigatório o check Approvals após ter avaliado as decisões em observa; não active nem automerge nem merge fila sem uma gate humana efetiva para as mudanças que o exijam. Um check verde, uma discussão resolvida ou um comentário.
" aucun défaut" ne valent jamais une validation métier.

<!-- section: s-2 -->
### GitHub Rulesets e independência da gate

Impose dos required checks provenientes da integração esperada, sem bypass para as identidades dos agentes; protege os ramos-alvo, proibição de força-push e supressão, aprovação das modificações recentes e invalidação das antigas autorizações quando o diff muda. Em equipe, requer a aprovação de um humano independente, e `CODEOWNERS` para os arquivos de controle; em solitário, não configura uma regra impossível de satisfazer pelo autor, conserva o mergado humano e um controle de política separado. Não conta uma revisão bot como um humano. Uma merge fila é opcional, desde verificar `merge_group`, e exigir as gatas do commit de integração. Em caso de conflito, mudança de SHA ou avançado da base, reavalia o estado; uma CI verde sobre uma antiga revisão não valida ao novo candidato.

<!-- section: s-3 -->
## Exemplo: `.github/workflows/ai-review.yml`

Exemplo para o depósito de dois módulos da secção 11 (sbt 1.x). Fige as acções a um SHA completo auditado e verifica as suas dependências transitivas; atualize-as por PR dedicada. O SHA básico provém do evento GitHub, não de um campo de PR controlado pelo seu autor. `github.sha` é o candidato de integração para `pull_request` e `merge_group` ; a revisão humana refere-se ao diff base/PR head, diferente deste commit de teste. Para uma merge fila, os controlos devem ser realizados também no grupo de merge.

```yaml
name: ai-review
on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]
  merge_group:
    types: [checks_requested]

permissions:
  contents: read

concurrency:
  group: ai-review-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: true

jobs:
  deterministic-checks:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6
        with:
          fetch-depth: 0
          ref: ${{ github.sha }}
          persist-credentials: false
      - uses: actions/setup-java@b6effb05e454b25005698d916606bdc6ffcbf961 # v5
        with:
          distribution: temurin
          java-version: '21'
      - uses: sbt/setup-sbt@20cf087132cf939c160f0e53f87ba33634003e3e # v1

      # Validate the integration candidate; fail on a missing base or wrong checkout.
      - name: Validate candidate
        env:
          BASE_SHA: ${{ github.event.pull_request.base.sha || github.event.merge_group.base_sha }}
          CANDIDATE_SHA: ${{ github.sha }}
        run: |
          set -euo pipefail
          test "$(git rev-parse HEAD)" = "$CANDIDATE_SHA"
          test -n "$BASE_SHA"
          git merge-base --is-ancestor "$BASE_SHA" "$CANDIDATE_SHA"
          python3 scripts/ai-validate.py --base "$BASE_SHA" --mode validate \
            --receipt "$RUNNER_TEMP/validation.json"

  mutation-gate:
    needs: deterministic-checks
    runs-on: ubuntu-latest
    timeout-minutes: 40
    steps:
      - uses: actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803 # v6
        with:
          ref: ${{ github.sha }}
          persist-credentials: false
      - uses: actions/setup-java@b6effb05e454b25005698d916606bdc6ffcbf961 # v5
        with:
          distribution: temurin
          java-version: '21'
      - uses: sbt/setup-sbt@20cf087132cf939c160f0e53f87ba33634003e3e # v1
      # Configure Stryker's break threshold and inspect surviving mutants in the actual project.
      - name: Mutation testing
        run: sbt "project api" stryker
```

**Frontera de confiança CI :** na YAML O PR pode modificar os programas e o fluxo de trabalho que contém, ou mesmo os comandos de build ou os relatórios. Protege os fluxos de trabalho, os scripts, as regras de teste, as políticas e `CODEOWNERS` ; se disponível, impõe um required workflow de confiança proveniente de um depósito/commit protegido (ruleset de organisation) e carga ao validador a partir desta fonte e não a partir do candidato. Uma modificação legítima da política passa por um PR e uma validação humanas separadas. Em solitário sem required workflow externo, compara estes ficheiros à base e não autoriza nenhuma merge até que tenha sido revista uma modificação de gate. Não se base numa simples convenção `AGENTS.md`.

O checkout da PR pode executar código arbitrário através da sbt: nenhum segredo privilegiado, nenhum token da escrita, nem `pull_request_target` Os relatórios de testes são testes operacionais, não certificados invioláveis se o código de teste em si for hostil. Ficheiro os relatórios e a proveniência na CI de acordo com a política do projecto; a validação deve ser relaborada no candidato final (e no commit entregue se for diferente).

Pontos de doutrina:

* **os juízes deterministas passam primeiro** : compilar, formato e testes seletivos são baratos em comparação com uma chamada LLM Um trabalho LLM que gira em código que não compila é orçamento queimado;
* Se uma revisão LLM de CI for realmente automatizada, dá-lhe uma **clave API dedicada**, um prazo e um limite de despesas próprias do trabalho; para uma utilização principalmente interativa através das assinaturas Claude e ChatGPT, esta automação continua a ser opcional;
* **O trabalho LLM é read-only** : comenta a PR, nunca comete. Um agente que corrige na CI recria o problema 16, pior (sem humanos no ciclo);
* **`sbt --client` em locais, JVM fresca em CI** : o diabo sbt é a alavanca dos riços locais; em CI, uma cache de dependências controlada pode acelerar a resolução, mas não substitui os testes nem o isolamento. **sbt 2.0.0 é estável desde o 14 Junho 2026** ; utiliza pelo menos **2.0.7** (o **1.13.0** sobre o ramo 1.x) devido à correção da OSP/TCP do 21 Agosto: definições de edifício em Scala 3JDK 17 mínimo, cliente nativo `sbtn` (iniciar muito mais rápido, diretamente útil para riços agenticos), cache local/distante compatível Bazel y `test` Este guia segue a convenção. sbt 1.x: migração para o sbt 2.x é uma mudança de edifício crítico que nunca se delega em um agente.60+ ports, incluindo Play e Scala.js em curso), e posteriormente adaptação desses trabalhos.

**Autofix Codex em CI : exceção explícita ao trabalho de revisão read-only.** Se for realmente necessário um fluxo de correção hospedado, separa o trabalho de geração do patch (sem direito de push) do trabalho de publicação controlada; limita os disparadores aos eventos e atores aprovados. Nunca lança código não confiável procedente de uma PR com segredos ou um token de escrita privilegiado (em particular via `pull_request_target`) Fige as ações por SHA, aplica permissões mínimas, um timeout, um orçamento externo e um monte de competência por PR; verifica o head SHA antes da publicação, e depois volta a ativar os checks requeridos. Não força-push, auto-aprovação nem merge pelo trabalho LLM. Os comentários, logs e adesivos continuam a ser dados não confiáveis; o fracasso nunca deve provocar mudanças nos gates.

O mesmo corte é incorporado a GitLab CI:: três cursos de capacitação (`deterministic`, `mutation`, `llm-review`), inclusive gates, `rules: changes` para lançar Stryker apenas nos módulos afetados.

---

