<!-- section: chapter -->
# 10B. OpenRouter como alternativa pontual

Para o fluxo de trabalho atual, ** não é necessário nenhum gateway local** : OpenRouter só serve como porta de saída aos modelos de emergência. Cria uma chave dedicada, fixa um limite de despesas lado conta e selecciona explicitamente o modelo a testar.

```text
Claude Code / Codex bloqueados
→ preparar uma reprodução mínima
→ OpenRouter
→ escolher deliberadamente GLM / Kimi / Gemini / Grok
→ registrar no log da tarefa o nome do modelo e do provedor
```

O princípio é voluntário simples: **OpenRouter não se converte no caminho normal de desenvolvimento**. Claude Code, Codex, Qwen local, GitHub Copilot e JetBrains AI continuam a utilizar as suas superfícies nativas.

> Estado da estrada Gemini.** Google fechou o acesso
> gratuit/Pro/Ultra em Gemini CLI o 18 Junho 2026 ; seu sucessor Antigravity CLI é closed-source com uma quota
> grátis muito reduzido (orden de magnitude: ~20 Os pedidos/dia) já não têm um terceiro agente gratuito.
> Google: para um aviso Gemini em solução de problemas, a via racional continua sendo oAPI ou OpenRouter, o que esta seção é:
> Lição geral para todo o stack: nunca construa um fluxo de trabalho em uma quota gratuita
> Desaparecer no trimestre.

<!-- section: s-1 -->
## Configuração mínima

Uma única variável de ambiente é suficiente para os programas ou ferramentas que utilizam OpenRouter :

```bash
export OPENROUTER_API_KEY="..."
```

Por uma integração Scala pontual, mantenha a mesma exclusão `LlmClient[F[_]]` que na secção 7A e injeta uma configuração dedicada:

```scala
import zio.*

final case class OpenRouterConfig(
    apiKey: String,
    baseUrl: String = "https://openrouter.ai/api/v1"
)

object OpenRouterConfig:
  val layer: ZLayer[Any, SecurityException, OpenRouterConfig] =
    ZLayer.fromZIO {
      for
        key <- System.env("OPENROUTER_API_KEY").someOrFail(
                 SecurityException("OPENROUTER_API_KEY manquante")
               )
      yield OpenRouterConfig(key)
    }
```

O cliente conserva então um endpoint OpenAI-compatible sem introduzir um servidor local adicional.

<!-- section: s-2 -->
## Regras de Fallback

Para este guia:

```text
Provedor alternativo para o mesmo modelo
→ permitido

Troca automática para outro modelo
→ desativada por padrão
```

A mudança de provider melhora a disponibilidade sem mudar a natureza da análise. Uma mudança automática do modelo rompe pelo contrário o objetivo procurado: obter conscientemente uma opinião de outra família de modelos.

<!-- section: s-3 -->
## Regras de confidencialidade

OpenRouter adicione vários fornecedores cujas políticas podem diferir. Para código profissional:

```text
- envie só o contexto necessário
- prefira uma reprodução, o stack trace e apenas os arquivos envolvidos
- nunca envie o repositório inteiro por padrão
- anonimize dados de negócio e segredos
- escolha explicitamente provedores compatíveis com os requisitos do projeto
- mantenha as partes mais sensíveis em ambiente local ou com provedores diretos já aprovados.
```

<!-- section: s-4 -->
## O queOpenRouter não deve substituir

```text
Claude Code        → agente principal para raciocínio e depuração + revisor independente via assinatura Claude
Codex              → agente principal de implementação + revisor independente via assinatura ChatGPT
Qwen local         → modelo local direto
GitHub Copilot     → fluxo de trabalho no GitHub
JetBrains AI       → assistência na IDE
OpenRouter         → escalada excepcional para outros modelos
```

Esta separação evita transformar uma simples porta de emergência em uma nova camada de infraestrutura que deve ser mantida.

---

