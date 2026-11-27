<!-- section: chapter -->
# 10B. OpenRouter como alternativa pontual

Para o fluxo de trabalho atual, ** não é necessário nenhum gateway local** : OpenRouter só serve como porta de saída aos modelos de emergência. Cria uma chave dedicada, fixa um limite de despesas lado conta e selecciona explicitamente o modelo a testar.

```text
Claude Code / Codex bloqués
→ préparer un reproducer minimal
→ OpenRouter
→ choisir volontairement GLM / Kimi / Gemini / Grok
→ conserver le nom du modèle et du provider dans le journal de tâche
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
Provider fallback pour le même modèle
→ autorisé

Fallback automatique vers un autre modèle
→ désactivé par défaut
```

A mudança de provider melhora a disponibilidade sem mudar a natureza da análise. Uma mudança automática do modelo rompe pelo contrário o objetivo procurado: obter conscientemente uma opinião de outra família de modelos.

<!-- section: s-3 -->
## Regras de confidencialidade

OpenRouter adicione vários fornecedores cujas políticas podem diferir. Para código profissional:

```text
- envoyer le minimum de contexte nécessaire ;
- préférer un reproducer, une stack trace et les fichiers strictement concernés ;
- ne jamais envoyer le repository entier par défaut ;
- anonymiser les données métier et secrets ;
- choisir explicitement les providers compatibles avec les exigences du projet ;
- garder les parties les plus sensibles en local ou chez les fournisseurs directs déjà approuvés.
```

<!-- section: s-4 -->
## O queOpenRouter não deve substituir

```text
Claude Code        → agent principal raisonnement/debug + reviewer croisé via abonnement Claude
Codex              → agent principal d'exécution + reviewer croisé via abonnement ChatGPT
Qwen local         → modèle local direct
GitHub Copilot     → workflow GitHub
JetBrains AI       → assistance IDE
OpenRouter         → escalade exceptionnelle vers d'autres modèles
```

Esta separação evita transformar uma simples porta de emergência em uma nova camada de infraestrutura que deve ser mantida.

---

