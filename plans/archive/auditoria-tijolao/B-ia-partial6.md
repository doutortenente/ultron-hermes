# Auditoria B - parcial 6


## G1. raw nvidia: glm-5.3-flash vs glm-5.3 (campos/urls) + model-catalog.json nvidia

```
== nvidia raw: z-ai/glm-5.3-flash ==
{"i": ["image", "video", "pdf"], "c": 1000000, "o": 131072, "r": true}
== nvidia raw: z-ai/glm-5.3 ==
{"i": [], "c": 1000000, "o": 131072, "r": true}
== model-catalog.json: chaves glm da nvidia ==
  models key: deepinfra:glm-5.3-flash -> {"vision": true, "videoInput": true, "pdf": true}
  models key: glm:glm-5.3-flash -> {"vision": true, "videoInput": true, "pdf": true}
  models key: zai:glm-5.3-flash -> {"vision": true, "videoInput": true, "pdf": true}
  models key: glm:glm-5.3-flashx -> {"vision": true, "videoInput": true, "pdf": true}
  models key: zai:glm-5.3-flashx -> {"vision": true, "videoInput": true, "pdf": true}
  models key: cloudflare-ai:glm-5.3-flash -> {"vision": true}
  models key: cloudflare-workers-ai:glm-5.3-flash -> {"vision": true}
  models key: engy:glm-5.3-flash -> {"vision": true}
  models key: nano-gpt:glm-5.3-flash-apex-abliterated -> {"vision": true}
  models key: nano-gpt:glm-5.3-flash -> {"vision": true, "videoInput": true}
  models key: nano-gpt:glm-5.3-flash-uncensored -> {"vision": true}
  models key: nano-gpt:glm-5.3-flash-apex -> {"vision": true}
  models key: nano-gpt:glm-5.3-flash-cybersecurity -> {"vision": true}
  models key: crof:glm-5.3-flash -> {"vision": true, "videoInput": true, "pdf": true}
  models key: baseten:glm-5.3-fast -> {"vision": true}
  models key: baseten:glm-5.3-flash -> {"vision": true}
  models key: baseten:glm-5.3 -> {"vision": true}
  models key: wandb:glm-5.3-flash -> {"vision": true}
  models key: umans-ai-coding-plan:umans-glm-5.3-flash -> {"vision": true, "videoInput": true}
  models key: umans-ai:umans-glm-5.3-flash -> {"vision": true, "videoInput": true}
  models key: siliconflow:glm-5.3-flash -> {"vision": true}
  models key: bothub:glm-5.3-flash -> {"vision": true, "videoInput": true, "pdf": true}
  models key: privatemode-ai:glm-5.3-flash -> {"vision": true}
  models key: llmgateway-providers:glm-5.3-flash -> {"vision": true, "videoInput": true, "pdf": true}
  models key: above:glm-5.3-flash -> {"vision": true}
  models key: kilo:glm-5.3-flash -> {"vision": true, "videoInput": true}
  models key: kilo:glm-5.3-flashx -> {"vision": true, "videoInput": true}
  models key: melious:glm-5.3-flash -> {"vision": true, "videoInput": true}
  models key: berget:glm-5.3-flash -> {"vision": true, "videoInput": true}
  models key: 302ai:glm-5.3-flash -> {"vision": true, "videoInput": true, "pdf": true}
  models key: openrouter:glm-5.3-flash -> {"vision": true, "videoInput": true}
  models key: openrouter:glm-5.3-flashx -> {"vision": true, "videoInput": true}
  models key: iteracompute:glm-5.3-flash -> {"vision": true}
  models key: cline-pass:glm-5.3-flash -> {"vision": true, "videoInput": true, "pdf": true}
  models key: modal:glm-5.3-flash -> {"vision": true, "videoInput": true}
  models key: coralbricks:glm-5.3-flash-fp4 -> {"vision": true, "videoInput": true}
  models key: neuralwatt:glm-5.3-flash -> {"vision": true}
  models key: neuralwatt:glm-5.3-flash-flex -> {"vision": true}
  models key: zenmux:glm-5.3-flash -> {"vision": true, "videoInput": true, "pdf": true}
  models key: zenmux:glm-5.3-flashx -> {"vision": true, "videoInput": true, "pdf": true}
  models key: vultr:glm-5.3-flash -> {"vision": true, "videoInput": true}
  models key: huggingface:glm-5.3-flash -> {"vision": true}
  models key: vancine:glm-5.3-flash -> {"vision": true, "videoInput": true, "pdf": true}
  models key: zhipuai-coding-plan:glm-5.3-flash -> {"vision": true, "videoInput": true, "pdf": true}
  models key: aiand:glm-5.3-flash -> {"vision": true, "videoInput": true, "pdf": true}
  models key: volcengine-coding-plan:glm-5.3-flash -> {"vision": true, "videoInput": true, "pdf": true}
  models key: ollama-cloud:glm-5.3-flash -> {"vision": true, "videoInput": true, "pdf": true}
  models key: vercel:glm-5.3-flash -> {"vision": true}
  models key: vercel:glm-5.3-flashx -> {"vision": true}
  models key: zai-coding-plan:glm-5.3-flash -> {"vision": true, "videoInput": true, "pdf": true}
  models key: hyper:glm-5.3-flash -> {"vision": true}
  models key: orcarouter:glm-5.3-flash -> {"vision": true, "videoInput": true, "pdf": true}
  models key: orcarouter:glm-5.3-flash-free -> {"vision": true, "videoInput": true, "pdf": true}
  models key: friendli:glm-5.3-flash -> {"vision": true, "videoInput": true}
  models key: inco:glm-5.3-flash -> {"vision": true, "videoInput": true, "pdf": true}
  models key: scnet-token-plan:glm-5.3-flash -> {"vision": true, "videoInput": true, "pdf": true}
  models key: ofox:glm-5.3-flash -> {"vision": true, "videoInput": true, "pdf": true}
  models key: ofox:glm-5.3-flashx -> {"vision": true, "videoInput": true, "pdf": true}
  models key: aihubmix:glm-5.3-flash -> {"vision": true, "videoInput": true}
  models key: merge-gateway:glm-5.3-flash -> {"vision": true, "videoInput": true, "pdf": true}
  models key: nvidia:glm-5.3-flash -> {"vision": true, "videoInput": true, "pdf": true}
  models key: opencode-go:glm-5.3-flash -> {"vision": true, "videoInput": true, "pdf": true}
  models key: tensorx:glm-5.3-flash -> {"vision": true, "videoInput": true, "pdf": true}
  models key: pareto:glm-5.3-flash -> {"vision": true, "videoInput": true}
  models key: edenai:glm-5.3-flash -> {"vision": true, "videoInput": true}
  models key: tempr:glm-5.3-flash -> {"vision": true, "videoInput": true, "pdf": true}
  models key: tempr:glm-5.3-flashx -> {"vision": true, "videoInput": true, "pdf": true}
  models key: opencode:glm-5.3-flash -> {"vision": true, "videoInput": true, "pdf": true}
  models key: glm-cn:glm-5.3-flash -> {"vision": true, "videoInput": true, "pdf": true}
  models key: zhipuai:glm-5.3-flash -> {"vision": true, "videoInput": true, "pdf": true}
  models key: glm-cn:glm-5.3-flashx -> {"vision": true, "videoInput": true, "pdf": true}
  models key: zhipuai:glm-5.3-flashx -> {"vision": true, "videoInput": true, "pdf": true}
  models key: requesty:glm-5.3-flash -> {"vision": true, "videoInput": true, "pdf": true}
  models key: requesty:glm-5.3-flash@eu -> {"vision": true, "videoInput": true, "pdf": true}
  models key: synthetic:glm-5.3-flash -> {"vision": true}
  models key: llmgateway:glm-5.3-flash -> {"vision": true, "videoInput": true, "pdf": true}
  models key: vivgrid:glm-5.3-flash -> {"vision": true, "videoInput": true, "pdf": true}
  models key: tokengo:glm-5.3-flash -> {"vision": true, "videoInput": true, "pdf": true}
  models key: togetherai:glm-5.3-flash -> {"vision": true, "videoInput": true}
  models key: cortecs:glm-5.3-flash -> {"vision": true}
  models key: crossmodel:glm-5.3-flash -> {"vision": true, "videoInput": true}
  models key: runinfra:glm-5.3-flash -> {"vision": true}
  models key: digitalocean:glm-5.3-flash -> {"vision": true, "videoInput": true}
```


## G2. settings DB: valores de tunnelEnabled/tailscaleEnabled/mitm (sem password)

```
Traceback (most recent call last):
  File "<stdin>", line 5, in <module>
NameError: name 're' is not defined. Did you mean: 'r'? Or did you forget to import 're'?
```


## G3. processos node/9router extra + ~/.9router runtime stat + /tmp cloudflared

```
===PS-9ROUTER-NODE===
dr         23840  0.0  0.2 1515644 17048 ?       Ssl  02:29   0:00 /home/dr/.local/share/nvm/versions/node/v24.16.0/bin/node /home/dr/.local/lib/node_modules/9router/cli.js --no-browser --skip-update --log
dr         24062  0.0  0.3 1295296 26028 ?       Sl   02:29   0:00 /home/dr/.local/share/9router/bin/cloudflared tunnel --url http://127.0.0.1:20128 --config /tmp/cloudflared-quick-XFpbCK/config.yml --no-autoupdate --retries 99
===DOT-9ROUTER-RUNTIME-STAT===
2026-09-23 23:34:25.061374473 -0300 /home/dr/.9router/runtime/package.json
2026-10-07 03:18:31.253919434 -0300 /home/dr/.9router/runtime/node_modules
total 24
drwxrwxr-x  4 dr dr 4096 2026-09-23 23:34:25.059374413 -0300 .
drwxrwxr-x  6 dr dr 4096 2026-09-23 23:31:53.148168189 -0300 ..
drwxrwxr-x  2 dr dr 4096 2026-09-23 23:31:53.141168101 -0300 mitm
drwxrwxr-x 11 dr dr 4096 2026-10-07 03:18:31.253919434 -0300 node_modules
-rw-rw-r--  1 dr dr  122 2026-09-23 23:34:25.061374473 -0300 package.json
-rw-rw-r--  1 dr dr  509 2026-09-23 23:34:25.060374443 -0300 package-lock.json
===TMP-CLOUDFLARED===
===FD-DO-24062-CONFIG===
```


## G4. agent.log 48h: linhas de fallback

```
2026-10-07 04:27:10,954 WARNING hermes_plugins.telegram_platform.adapter: [Telegram] Discovering Telegram API fallback IPs via DNS-over-HTTPS…
2026-10-07 04:27:11,248 INFO hermes_plugins.telegram_platform.adapter: [Telegram] Auto-discovered Telegram fallback IPs: 149.154.166.110
2026-10-07 04:27:11,252 INFO hermes_plugins.telegram_platform.adapter: [Telegram] Telegram fallback IPs active: 149.154.166.110
2026-10-07 05:45:02,809 INFO [20261007_052543_e17379] agent.chat_completion_helpers: Fallback to custom/cc/claude-opus-5-5: clearing primary credential pool (pool_provider=custom:9router) to prevent cross-provider contamination
2026-10-07 05:45:02,851 INFO [20261007_052543_e17379] agent.chat_completion_helpers: Fallback cc/claude-opus-5-5: reasoning_config resolved: {'enabled': True, 'effort': 'ultra'}
2026-10-07 05:45:02,851 INFO [20261007_052543_e17379] agent.chat_completion_helpers: Fallback cc/claude-opus-5-5: extra_body resolved: None
2026-10-07 05:45:02,853 INFO [20261007_052543_e17379] agent.chat_completion_helpers: Fallback activated: nvidia/z-ai/glm-5.3-flash → cc/claude-opus-5-5 (custom)
2026-10-07 06:07:37,264 INFO agent.conversation_compression: context compression attempt telemetry: {"attempt_id":"9c5afd7dca5a4f56bdf26f3b6ab03e6d","chunk_count":0,"chunking":false,"commit_ms":48,"commit_status":"committed","event":"compression_attempt","fallback_used":false,"session_id":"20261007_055454_e135ec","split_status":"in_place_committed","total_duration_ms":57879}
===E-CONTEXTO-DAS-2-ULTIMAS-FALHAS-FLASH===
2026-10-07 05:45:02,853 INFO [20261007_052543_e17379] agent.chat_completion_helpers: Fallback activated: nvidia/z-ai/glm-5.3-flash → cc/claude-opus-5-5 (custom)
2026-10-07 05:54:54,371 INFO agent.model_metadata: Could not detect context length for model 'nvidia/z-ai/glm-5.3-flash' at http://127.0.0.1:20128/v1 — defaulting to 256,000 tokens (probe-down). Set model.context_length in config.yaml to override.
2026-10-07 05:54:54,371 INFO agent.model_metadata: Using hardcoded context length 1,048,576 for model 'nvidia/z-ai/glm-5.3-flash' (custom endpoint, catalog match on 'glm-5.3')
2026-10-07 06:11:27,105 WARNING [20261007_055454_0832cb] agent.tool_executor: Tool execute_code returned error (4.40s): {"status": "error", "output": "\n########## C1. /home/dr/.hermes/config.yaml ##########\nmodel:\n  default: nvidia/z-ai/glm-5.3-flash\n  provider: custom\n  base_url: http://127.0.0.1:20128/v1\n  api_
2026-10-07 06:37:26,821 INFO [20261007_055454_e135ec] agent.model_metadata: Could not detect context length for model 'nvidia/z-ai/glm-5.3-flash' at http://127.0.0.1:20128/v1 — defaulting to 256,000 tokens (probe-down). Set model.context_length in config.yaml to override.
2026-10-07 06:37:26,821 INFO [20261007_055454_e135ec] agent.model_metadata: Using hardcoded context length 1,048,576 for model 'nvidia/z-ai/glm-5.3-flash' (custom endpoint, catalog match on 'glm-5.3')

```


## G5. plugins/model-providers/custom/__init__.py: trecho do ultra

```
    host = (parsed.hostname or "").lower().rstrip(".")
    return bool(host) and (host == "ollama.com" or host.endswith(".ollama.com") or "ollama" in host.split("."))


class CustomProfile(ProviderProfile):
    """Custom/Ollama local provider — think=false and num_ctx support."""

    def build_api_kwargs_extras(
        self, *, reasoning_config: dict | None = None, ollama_num_ctx: int | None = None, **ctx: Any
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        extra_body: dict[str, Any] = {}
        top_level: dict[str, Any] = {}
        if ollama_num_ctx:
            extra_body["options"] = {"num_ctx": ollama_num_ctx}
        # disabled -> top-level reasoning_effort="none" (Ollama's /v1 ignores
        # extra_body.think) plus think=False only on Ollama URLs; enabled+effort ->
        # top-level reasoning_effort clamped to the OpenAI-compat wire (GLM/ARK,
        # vLLM and SGLang all top out at "max"; "ultra" verbatim 400s); enabled
        # without effort -> omit so the server default applies. Never emit
        # think=True (Ollama-only flag).
        if reasoning_config and isinstance(reasoning_config, dict):
            effort = (reasoning_config.get("effort") or "").strip().lower()
            if effort == "none" or reasoning_config.get("enabled", True) is False:
                # See #14820.
                top_level["reasoning_effort"] = "none"
                if _looks_like_ollama_endpoint(ctx.get("base_url")):
                    extra_body["think"] = False
            elif effort:
                top_level["reasoning_effort"] = clamp_effort(effort, OPENAI_COMPAT_WIRE_EFFORTS)
        return extra_body, top_level

    def fetch_models(
        self, *, api_key: ***MASKED*** | None = None, base_url: str | None = None, timeout: float = 8.0
    ) -> list[str] | None:
        """base_url is user-configured; fetch only if set."""
        if not (base_url or self.base_url):
            return None
        return super().fetch_models(api_key=***MASKED*** base_url=base_url, timeout=timeout)


custom = CustomProfile(
    name="custom", aliases=("ollama", "local", "vllm", "llamacpp", "llama.cpp", "llama-cpp"),
    env_vars=(),  # No fixed key — custom endpoint
    base_url="",  # User-configured
    # An arbitrary client ceiling can exceed a local server's actual output limit.
    # The endpoint owns its generation default.
)

register_provider(custom)

```


## G6. stat docker-compose.tijolao.yml + diff mounts vs compose (resumo)

```
mtime=2026-10-04 13:15:08.593491239 -0300 size=6387 /home/dr/src/tijolao-ai/hermes-stack/docker-compose.tijolao.yml
===PROJETOS-EXISTE===
drwxrwxr-x  8 dr   dr    4096 out  2 21:31 src
```


## G7. /v1/models: glm/nvidia/cx entradas (conf. final)

```
total: 34
flash no catalogo: False
base no catalogo: True
cx/gpt-5.6-sol puro: False
cx/gpt-5.6-sol[1m]: True
opus: True
laguna ps: False

```