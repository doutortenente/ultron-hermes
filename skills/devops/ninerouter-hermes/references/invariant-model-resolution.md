# Invariant: Como o Hermes Resolve Modelos via 9router

---

## A Arquitetura Real

```
Hermes Agent (container)
    │
    │ base_url: http://127.0.0.1:20128/v1
    │ Authorization: Bearer ${NINEROUTER_KEY}
    ▼
9router (host, porta 20128)
    │
    ├─ Providers cadastrados (NVIDIA NIM, etc.)
    ├─ Catálogo de modelos por provider
    └─ Dispatch baseado no model ID recebido
```

---

## O Que NÃO Fazer

| Tentativa | Por que falha |
|---|---|
| Injetar `ANTHROPIC_BASE_URL` | Hermes opera via OpenAI-compatible endpoints (`/v1/chat/completions`) com token Bearer, não formato Anthropic |
| Manter modelos free no `fallback_providers` | Provoca troca silenciosa e imprevisível de modelos (Kimi, DeepSeek, etc.) |
| Configurar `model.default` com ID não cadastrado no 9router | 9router retorna erro ou força fallback |

---

## O Que Funciona

### 1. Modelo ativo e cadastrado no 9router

O 9router despacha modelos que estão cadastrados no provedor (ex.: NVIDIA NIM). Se o modelo for custom (ex.: `z-ai/glm-5.3`), ele precisa ser adicionado no dashboard do 9router.
Verificação: `curl http://127.0.0.1:20128/v1/models | jq -r '.data[].id'` deve listar o modelo.

### 2. Configuração no Hermes

```bash
hermes config set model.default nvidia/z-ai/glm-5.3
hermes config set agent.reasoning_effort low
```

O Hermes envia `model: nvidia/z-ai/glm-5.3` na chamada OpenAI-compatible ao 9router, que encaminha à NVIDIA NIM.

### 3. Cadeia de Fallback Estruturada

Em vez de modelos livres que variam a cada chamada, manter fallback explícito e testado:
1. 9router (NVIDIA) `nvidia/z-ai/glm-5.3` (reasoning `max`)
2. 9router `cc/claude-opus-5-5`
3. OpenRouter `anthropic/claude-sonnet-4.5`
4. Poolside direto `poolside/laguna-s-2.1` (`https://inference.poolside.ai/v1`)