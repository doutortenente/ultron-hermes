# Auditoria B - parcial 3


## C1. /home/dr/.hermes/config.yaml (api_key como ${VAR} exibida; valores literais mascarados)

```
model:
  default: nvidia/z-ai/glm-5.3-flash
  provider: custom
  base_url: http://127.0.0.1:20128/v1
  api_key: ${OPENAI_API_KEY}
providers:
  ollama-launch:
    api: http://127.0.0.1:11434/v1
    default_model: minimax-m3:cloud
    models:
      - minimax-m3:cloud
    name: Ollama
  nine-router:
    name: 9Router
    api: http://127.0.0.1:20128/v1
    key_env: ***MASKED***
    transport: chat_completions
    default_model: cx/gpt-5.6-sol
    discover_models: true
  poolside:
    name: Poolside
    api: https://inference.poolside.ai/v1
    key_env: ***MASKED***
    transport: chat_completions
    default_model: poolside/laguna-s-2.1
    models:
      - poolside/laguna-s-2.1
      - poolside/laguna-xs-2.1
    discover_models: true
  manifest:
    base_url: ''
    key_env: ***MASKED***
fallback_providers:
  - base_url: http://127.0.0.1:20128/v1
    model: cc/claude-opus-5-5
    provider: custom
    api_key: ${NINEROUTER_KEY}
  - base_url: https://openrouter.ai/api/v1
    model: anthropic/claude-sonnet-4.5
    provider: openrouter
    api_key: ${OPENROUTER_API_KEY}
  - base_url: https://inference.poolside.ai/v1
    model: poolside/laguna-s-2.1
    provider: custom
    api_key: ${POOLSIDE_API_KEY}
toolsets:
  - hermes-cli
  - web
database:
  journal_mode: wal
runtime:
  nofile_soft_limit: 4096
agent:
  max_turns: 500
  personalities: {}
  reasoning_effort: ultra
  verbose: false
terminal:
  backend: local
  cwd: .
  timeout: 180
  home_mode: auto
  container_cpu: 1
  container_memory: 5120
  container_disk: 51200
  container_persistent: true
  docker_mount_cwd_to_workspace: false
  lifetime_seconds: 300
browser:
  inactivity_timeout: 120
tool_loop_guardrails:
  warnings_enabled: true
  hard_stop_enabled: true
  warn_after:
    exact_failure: 2
    same_tool_failure: 3
    idempotent_no_progress: 2
  hard_stop_after:
    exact_failure: 5
    same_tool_failure: 8
    idempotent_no_progress: 5
compression:
  enabled: true
  progress_notices: false
  threshold: 0.5
  target_ratio: 0.2
  tail_mode: lean
  protect_last_n: 20
  min_tail_user_messages: 3
  max_attempts: 3
  proactive_prune_tokens: 0
  proactive_prune_min_result_chars: 8000
  proactive_prune_min_reclaim_tokens: 4096
  protect_first_n: 3
  codex_gpt55_autoraise: true
  codex_app_server_auto: native
  codex_responses_native: false
  codex_responses_compact_threshold: 200000
  in_place: true
  idle_compact_after_seconds: 0
prompt_caching:
  cache_ttl: 5m
auxiliary:
  background_review:
    provider: custom
    model: ps/poolside/laguna-s-2.1
    base_url: http://127.0.0.1:20128/v1
    api_key: ${OPENAI_API_KEY}
  compression:
    provider: custom
    model: ps/poolside/laguna-s-2.1
    base_url: http://127.0.0.1:20128/v1
    api_key: ${OPENAI_API_KEY}
  skills_hub:
    provider: custom
    model: ps/poolside/laguna-s-2.1
    base_url: http://127.0.0.1:20128/v1
    api_key: ${OPENAI_API_KEY}
  approval:
    provider: custom
    model: ps/poolside/laguna-s-2.1
    base_url: http://127.0.0.1:20128/v1
    api_key: ${OPENAI_API_KEY}
  mcp:
    provider: custom
    model: ps/poolside/laguna-s-2.1
    base_url: http://127.0.0.1:20128/v1
    api_key: ${OPENAI_API_KEY}
  title_generation:
    provider: custom
    model: ps/poolside/laguna-s-2.1
    base_url: http://127.0.0.1:20128/v1
    api_key: ${OPENAI_API_KEY}
  memory_query_rewrite:
    provider: custom
    model: ps/poolside/laguna-s-2.1
    base_url: http://127.0.0.1:20128/v1
    api_key: ${OPENAI_API_KEY}
  tts_audio_tags:
    provider: custom
    model: ag/gemini-3.8-flash
    base_url: http://127.0.0.1:20128/v1
    api_key: ${OPENAI_API_KEY}
  triage_specifier:
    provider: custom
    model: ag/gemini-3.8-flash
    base_url: http://127.0.0.1:20128/v1
    api_key: ${OPENAI_API_KEY}
  kanban_decomposer:
    provider: custom
    model: cc/claude-haiku-4-5-20251001
    base_url: http://127.0.0.1:20128/v1
    api_key: ${OPENAI_API_KEY}
  profile_describer:
    provider: custom
    model: ag/gemini-3.8-flash
    base_url: http://127.0.0.1:20128/v1
    api_key: ${OPENAI_API_KEY}
  goal_judge:
    provider: custom
    model: cc/claude-haiku-4-5-20251001
    base_url: http://127.0.0.1:20128/v1
    api_key: ${OPENAI_API_KEY}
  curator:
    provider: custom
    model: ps/poolside/laguna-s-2.1
    base_url: http://127.0.0.1:20128/v1
    api_key: ${OPENAI_API_KEY}
  monitor:
    provider: custom
    model: ps/poolside/laguna-s-2.1
    base_url: http://127.0.0.1:20128/v1
    api_key: ${OPENAI_API_KEY}
  moa_reference:
    provider: custom
    model: ag/gemini-3.8-flash
    base_url: http://127.0.0.1:20128/v1
    api_key: ${OPENAI_API_KEY}
  moa_aggregator:
    provider: custom
    model: cc/claude-haiku-4-5-20251001
    base_url: http://127.0.0.1:20128/v1
    api_key: ${OPENAI_API_KEY}
  vision:
    provider: custom
    model: ag/gemini-3.8-flash
    base_url: http://127.0.0.1:20128/v1
    api_key: ${OPENAI_API_KEY}
display:
  compact: true
  busy_input_mode: interrupt
  bell_on_complete: false
  show_reasoning: true
  background_process_notifications: concise
  streaming: true
  skin: default
  interim_assistant_messages: true
  busy_ack_detail: true
  cleanup_progress: false
  long_running_notifications: true
  tool_progress: all
  personality: concise
  show_cost: true
stt:
  enabled: true
  language: pt
  local:
    model: base
  openai:
    model: whisper-1
    language: pt
context:
  engine: compressor
memory:
  memory_enabled: true
  user_profile_enabled: true
  memory_char_limit: 2200
  user_char_limit: 1375
  nudge_interval: 10
  flush_min_turns: 6
delegation:
  model: nvidia/z-ai/glm-5.3
  provider: custom
  base_url: http://127.0.0.1:20128/v1
  api_key: ${OPENAI_API_KEY}
skills:
  external_dirs:
    - /home/dr/.agents/skills
  creation_nudge_interval: 15
telegram:
  allowed_chats: '8791057362'
approvals:
  mode: false
  destructive_slash_confirm: false
command_allowlist:
  - recursive delete
  - script execution via -e/-c flag
  - overwrite system file via redirection
  - execute_code
  - pipe remote content to shell
kanban:
  review_dispatch: true
code_execution:
  max_tool_calls: 50
  timeout: 300
tools:
  tool_search:
    enabled: true
    threshold_pct: 2
    search_default_limit: 5
    listing: auto
    listing_max_tokens: 1200
streaming:
  enabled: true
onboarding:
  seen:
    busy_input_prompt: true
    tool_progress_prompt: true
telemetry:
  shared_metrics:
    enabled: false
updates:
  pre_update_backup: quick
  backup_keep: 5
  non_interactive_local_changes: stash
_config_version: 42
group_sessions_per_user: true
known_builtin_toolsets:
  cli:
    - browser
    - clarify
    - code_execution
    - computer_use
    - context_engine
    - cronjob
    - delegation
    - discord
    - discord_admin
    - file
    - homeassistant
    - image_gen
    - memory
    - session_search
    - skills
    - spotify
    - stt
    - terminal
    - todo
    - tts
    - video
    - video_gen
    - vision
    - web
    - x_search
    - yuanbao
known_plugin_toolsets:
  cli:
    - a2a
    - spotify
mcp_servers:
  obsidian:
    args:
      - -y
      - obsidian-mcp-server
    command: npx
    enabled: true
    env:
      OBSIDIAN_API_KEY: ***MASKED***
      OBSIDIAN_BASE_URL: http://127.0.0.1:27123
      OBSIDIAN_VAULT_PATH: /home/dr/vaults/celebro
  supabase:
    auth: oauth
    enabled: false
    type: http
    url: https://mcp.supabase.com/mcp?project_ref=idswehsvvqczzkiatuzu&read_only=true&features=docs%2Cdebugging%2Cdatabase%2Cdevelopment%2Cfunctions%2Cstorage
  playwright:
    command: npx
    args:
      - '@playwright/mcp@latest'
    enabled: false
  github:
    transport: stdio
    command: npx
    args:
      - -y
      - '@modelcontextprotocol/server-github'
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: ${GITHUB_TOKEN}
    enabled: true
  filesystem:
    transport: stdio
    command: npx
    args:
      - -y
      - '@modelcontextprotocol/server-filesystem'
      - /home/dr
    enabled: true
  postgres:
    transport: stdio
    command: npx
    args:
      - -y
      - '@modelcontextprotocol/server-postgres'
      - postgresql://user:pass@host:5432/db
    enabled: false
platform_toolsets:
  cli:
    - web
    - terminal
    - file
    - code_execution
    - vision
    - skills
    - todo
    - memory
    - session_search
    - clarify
    - delegation
    - cronjob
  discord:
    - hermes-discord
  homeassistant:
    - hermes-homeassistant
  qqbot:
    - hermes-qqbot
  signal:
    - hermes-signal
  slack:
    - hermes-slack
  telegram:
    - hermes-telegram
  whatsapp:
    - hermes-whatsapp
  yuanbao:
    - hermes-yuanbao
session_reset:
  at_hour: 4
  idle_minutes: 1440
  mode: none
dashboard:
  basic_auth:
    username: dr
    password_hash: scrypt$16384$8$1$QNh4seyxSirU6fjV3h6w8w==$wREjQal4T3yemJdxXXA0M5PXgDGNHsXytb4fCHwIQC8=

# ── Security ──────────────────────────────────────────────────────────
# Secret redaction is ON by default — strings that look like API keys,
# tokens, and passwords are masked in tool output, logs, and chat
# responses before the model or user ever sees them. Set redact_secrets
# to false to disable (e.g. when developing the redactor itself).
# tirith pre-exec scanning is enabled by default when the tirith binary
# is available. Configure via security.tirith_* keys or env vars
# (TIRITH_ENABLED, TIRITH_BIN, TIRITH_TIMEOUT, TIRITH_FAIL_OPEN).
#
# security:
#   redact_secrets: true
#   tirith_enabled: true
#   tirith_path: "tirith"
#   tirith_timeout: 5
#   tirith_fail_open: true

# ── Fallback Model ────────────────────────────────────────────────────
# Automatic provider failover when primary is unavailable.
# Uncomment and configure to enable. Triggers on rate limits (429),
# overload (529), service errors (503), or connection failures.
#
# Supported providers:
#   openrouter   (OPENROUTER_API_KEY)  — routes to any model
#   openai-codex (OAuth — hermes auth) — OpenAI Codex
#   nous         (OAuth — hermes auth) — Nous Portal
#   zai          (ZAI_API_KEY)         — Z.AI / GLM
#   kimi-coding  (KIMI_API_KEY)        — Kimi / Moonshot
#   kimi-coding-cn (KIMI_CN_API_KEY)   — Kimi / Moonshot (China)
#   minimax      (MINIMAX_API_KEY)     — MiniMax
#   minimax-cn   (MINIMAX_CN_API_KEY)  — MiniMax (China)
#   bedrock      (AWS IAM / boto3)     — AWS Bedrock (Converse API)
#
# For custom OpenAI-compatible endpoints, add base_url and key_env.
#
# fallback_model:
#   provider: openrouter
#   model: anthropic/claude-sonnet-4

```


## C2. perfis /home/dr/.hermes/profiles/*/config.yaml (topo de cada)

```
=== /home/dr/.hermes/profiles/chefe/ ===
model:
  default: "nvidia/z-ai/glm-5.3"
  provider: "custom"
  base_url: "http://127.0.0.1:20128/v1"
  api_key: ${NINEROUTER_KEY}
  reasoning_effort: max

=== /home/dr/.hermes/profiles/evidencia/ ===
model: cx/gpt-5.6-terra
providers:
  ollama-launch:
    api: http://127.0.0.1:11434/v1
    default_model: minimax-m3:cloud
    models:
      - minimax-m3:cloud
    name: Ollama
  nine-router:
    name: 9Router
    api: http://127.0.0.1:20128/v1
    key_env: ***MASKED***
    transport: chat_completions
    default_model: cx/gpt-5.6-terra
    discover_models: true
  poolside:
    name: Poolside
    api: https://inference.poolside.ai/v1
    key_env: ***MASKED***
    transport: chat_completions
    default_model: poolside/laguna-s-2.1
    models:
      - poolside/laguna-s-2.1
      - poolside/laguna-xs-2.1
    discover_models: true
fallback_providers:
  - base_url: https://openrouter.ai/api/v1
    model: nvidia/nemotron-3-ultra-550b-a55b:free
    provider: openrouter
  - base_url: https://openrouter.ai/api/v1
    model: nvidia/nemotron-3.5-lightning:free
    provider: openrouter
  - base_url: https://openrouter.ai/api/v1
    model: dots-studio/dots-3-note-preview:free
    provider: openrouter
  - base_url: https://openrouter.ai/api/v1
    model: poolside/laguna-s-2.1:free
    provider: openrouter
  - base_url: https://openrouter.ai/api/v1
    model: google/gemma-4-26b-a4b-it:free
    provider: openrouter
  - base_url: https://openrouter.ai/api/v1
    model: openai/gpt-oss-20b:free
    provider: openrouter
toolsets:
  - hermes-cli
  - web
database:
  journal_mode: wal
runtime:
  nofile_soft_limit: 4096
agent:
  max_turns: 500
  personalities: {}
  reasoning_effort: medium
  verbose: false
terminal:
  backend: local
  cwd: .
  timeout: 180
  home_mode: auto
  container_cpu: 1
  container_memory: 5120
  container_disk: 51200
  container_persistent: true
  docker_mount_cwd_to_workspace: false
  lifetime_seconds: 300
browser:
  inactivity_timeout: 120
tool_loop_guardrails:
  warnings_enabled: true
  hard_stop_enabled: true
  warn_after:
    exact_failure: 2
    same_tool_failure: 3
    idempotent_no_progress: 2
  hard_stop_after:
    exact_failure: 5
    same_tool_failure: 8
    idempotent_no_progress: 5
compression:
  enabled: true
  progress_notices: false
  threshold: 0.5
  target_ratio: 0.2
  tail_mode: lean
  protect_last_n: 20
  min_tail_user_messages: 3
  max_attempts: 3
  proactive_prune_tokens: 0
  proactive_prune_min_result_chars: 8000
  proactive_prune_min_reclaim_tokens: 4096
  protect_first_n: 3
  codex_gpt55_autoraise: true
  codex_app_server_auto: native
  codex_responses_native: false
  codex_responses_compact_threshold: 200000
  in_place: tru
=== /home/dr/.hermes/profiles/fiscal/ ===
model:
  default: "poolside/laguna-s-2.1"
  provider: "custom"
  base_url: "https://inference.poolside.ai/v1"
  api_key: ${POOLSIDE_API_KEY}

=== /home/dr/.hermes/profiles/residente/ ===
model:
  default: "nvidia/z-ai/glm-5.3"
  provider: "custom"
  base_url: "http://127.0.0.1:20128/v1"
  api_key: ${NINEROUTER_KEY}
  reasoning_effort: max

=== /home/dr/.hermes/profiles/secretaria/ ===
model:
  default: "nvidia/z-ai/glm-5.3"
  provider: "custom"
  base_url: "http://127.0.0.1:20128/v1"
  api_key: ${NINEROUTER_KEY}
  reasoning_effort: max


```


## C2b. env do container (HERMES/NINEROUTER; valores de chaves mascarados)

```
HERMES_DELEGATED_CHILD_CONTEXT=1
PWD=/opt/hermes
HERMES_REAL_HOME=/opt/data
HOME=/home/dr/.hermes/home
HERMES_KERNEL_SENTINEL=@@HERMES-KERNEL-VqEPQdNzHxJnplKrxCglcg@@
HERMES_KANBAN_BOARD=default
PYTHONPATH=/tmp/hermes_kernel_u4b__xep:/opt/hermes
HERMES_RPC_SOCKET=/tmp/hermes_rpc_929a842d8f364687a29718e515362b7e.sock
TERMINAL_CWD=/opt/hermes
HERMES_RPC_PERSISTENT=1
PATH=/opt/hermes/bin:/opt/hermes/.venv/bin:/opt/data/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HERMES_RPC_TOKEN=***MASKED***
HERMES_KERNEL_SPILL_DIR=/tmp/hermes_kernel_u4b__xep
HERMES_HOME=/home/dr/.hermes
Wed Oct  7 06:19:55 UTC 2026
Wed Oct  7 06:19:55 UTC 2026

```


## C3. logs Hermes 48h: contagens e exemplos

```
Janela: desde 2026-10-05 06:19 UTC (agora: 2026-10-07 06:19:55)
== agent.log ==
  API call failed = 2
  glm-5.3-flash = 41
  fetch connect timeout = 16
  503 = 27
  [Ff]all(ing)? ?back = 8
  Streaming failed = 2
  fallback = 4
== errors.log ==
  API call failed = 2
  glm-5.3-flash = 23
  fetch connect timeout = 20
  503 = 53
  [Ff]all(ing)? ?back = 1
  Streaming failed = 2
  fallback = 1
== gateway.log ==
  API call failed = 0
  glm-5.3-flash = 0
  fetch connect timeout = 0
  503 = 0
  [Ff]all(ing)? ?back = 3
  Streaming failed = 0
  fallback = 3
===EXEMPLOS-48h===
openai.InternalServerError: Error code: 503 - {'error': {'message': '[nvidia/z-ai/glm-5.3-flash] [502]: fetch failed (cause: ECONNRESET: read ECONNRESET) (reset after 30s)'}}
openai.InternalServerError: Error code: 503 - {'error': {'message': '[nvidia/z-ai/glm-5.3-flash] [502]: fetch failed (cause: ENOTFOUND: getaddrinfo ENOTFOUND integrate.api.nvidia.com) (reset after 30s)'}}
openai.InternalServerError: Error code: 503 - {'error': {'message': '[nvidia/z-ai/glm-5.3-flash] [502]: fetch connect timeout (reset after 9s)'}}
openai.InternalServerError: Error code: 503 - {'error': {'message': '[nvidia/z-ai/glm-5.3-flash] [502]: fetch connect timeout (reset after 30s)'}}
openai.InternalServerError: Error code: 503 - {'error': {'message': '[nvidia/z-ai/glm-5.3-flash] [502]: fetch connect timeout (reset after 30s)'}}
openai.InternalServerError: Error code: 503 - {'error': {'message': '[nvidia/z-ai/glm-5.3-flash] [502]: fetch connect timeout (reset after 30s)'}}

```


## C5. testes de chat via 9router (max_tokens 16, timeout 60)

```
NINEROUTER_KEY: AUSENTE
--- nvidia/z-ai/glm-5.3-flash -> HTTP+tempo: 401 0.004465
{"error":{"message":"Missing API key","type":"authentication_error","code":"invalid_api_key"}}
--- nvidia/z-ai/glm-5.3 -> HTTP+tempo: 401 0.003918
{"error":{"message":"Missing API key","type":"authentication_error","code":"invalid_api_key"}}

```


## C6. saude: status codes 8642/9119/3000

```
http://127.0.0.1:8642/health -> 200
http://127.0.0.1:9119/ -> 200
http://127.0.0.1:3000/ -> 200

```


## D1. journal 9router: linhas do flash, DONE por modelo, contexto das quedas, OOM

```
===FLASH-LINHAS===
22
out 07 02:40:20 Tijolao node[23905]: [02:40:20] 🟣 ✗ ERROR 502 · nvidia/z-ai/glm-5.3-flash · 249006ms
out 07 02:40:20 Tijolao node[23905]: [02:40:20] ⚠️  [AUTH] NVIDIABuild-Autogen-29 locked modelLock_z-ai/glm-5.3-flash for 30s [502]
out 07 02:40:20 Tijolao node[23905]: [02:40:20] ⚠️  [AUTH] nvidia | all 1 accounts locked for z-ai/glm-5.3-flash (reset after 30s) | lastError=[502]: fetch connect timeout
out 07 02:40:20 Tijolao node[23905]: [02:40:20] ⚠️  [CHAT] [nvidia/z-ai/glm-5.3-flash] [502]: fetch connect timeout (reset after 30s)
out 07 02:40:23 Tijolao node[23905]: [02:40:23] 🟣 ✗ ERROR 502 · nvidia/z-ai/glm-5.3-flash · 249006ms
out 07 02:40:23 Tijolao node[23905]: [02:40:23] ⚠️  [AUTH] NVIDIABuild-Autogen-29 locked modelLock_z-ai/glm-5.3-flash for 30s [502]
out 07 02:40:23 Tijolao node[23905]: [02:40:23] ⚠️  [AUTH] nvidia | all 1 accounts locked for z-ai/glm-5.3-flash (reset after 30s) | lastError=[502]: fetch connect timeout
out 07 02:40:23 Tijolao node[23905]: [02:40:23] ⚠️  [CHAT] [nvidia/z-ai/glm-5.3-flash] [502]: fetch connect timeout (reset after 30s)
out 07 02:45:02 Tijolao node[23905]: [02:45:02] 🟣 ✗ ERROR 502 · nvidia/z-ai/glm-5.3-flash · 249008ms
out 07 02:45:02 Tijolao node[23905]: [02:45:02] ⚠️  [AUTH] NVIDIABuild-Autogen-29 locked modelLock_z-ai/glm-5.3-flash for 30s [502]
out 07 02:45:02 Tijolao node[23905]: [02:45:02] ⚠️  [AUTH] nvidia | all 1 accounts locked for z-ai/glm-5.3-flash (reset after 30s) | lastError=[502]: fetch connect timeout
out 07 02:45:02 Tijolao node[23905]: [02:45:02] ⚠️  [CHAT] [nvidia/z-ai/glm-5.3-flash] [502]: fetch connect timeout (reset after 30s)
===FLASH-POST-EXEMPLO===
out 07 02:30:17 Tijolao node[23905]: [02:30:17] 🟤 ▶ POST nvidia/z-ai/glm-5.3-flash → nvidia/z-ai/glm-5.3-flash · FMT: openai→openai · STREAM · 2 MSG · 18 TOOL · THINK:auto · ACC:NVIDIABuild-Autogen-29
out 07 02:33:47 Tijolao node[23905]: [02:33:47] 🟣 ▶ POST nvidia/z-ai/glm-5.3-flash → nvidia/z-ai/glm-5.3-flash · FMT: openai→openai · STREAM · 4 MSG · 18 TOOL · THINK:auto · ACC:NVIDIABuild-Autogen-29
===DONE-POR-MODELO===
DONE glm-5.3 : 0 ; ERRO 502 glm-5.3 : 4
DONE glm-5.3-flash: 0 ; ERRO 502 glm-5.3-flash: 4
DONE claude-opus-5-5: 0 ; ERRO 502 claude-opus-5-5: 0
DONE laguna: 0 ; ERRO 502 laguna: 0
===QUEDA-0225-CONTEXTO===
out 07 02:25:49 Tijolao systemd[1060]: 9router.service: Main process exited, code=killed, status=9/KILL
out 07 02:25:49 Tijolao systemd[1060]: 9router.service: Failed with result 'signal'.
out 07 02:25:49 Tijolao systemd[1060]: 9router.service: Consumed 5.713s CPU time.
out 07 02:25:54 Tijolao systemd[1060]: 9router.service: Scheduled restart job, restart counter is at 1.
out 07 02:25:54 Tijolao systemd[1060]: Started 9router.service - 9Router local AI gateway.
out 07 02:25:57 Tijolao node[22400]: ⚠ Network-exposed: reachable at http://192.168.15.186:20128 (bound 0.0.0.0). Use --host 127.0.0.1 for local-only.
out 07 02:25:57 Tijolao node[22400]: 🚀 9router v0.5.95
out 07 02:25:57 Tijolao node[22400]: Server: http://localhost:20128
out 07 02:25:57 Tijolao node[22467]: ▲ Next.js 16.3.4
out 07 02:25:57 Tijolao node[22467]: - Local:         http://localhost:20128
out 07 02:25:57 Tijolao node[22467]: - Network:       http://0.0.0.0:20128
out 07 02:25:57 Tijolao node[22467]: ✓ Ready in 0ms
===QUEDA-0229-CONTEXTO===
out 07 02:29:02 Tijolao systemd[1060]: 9router.service: Main process exited, code=killed, status=9/KILL
out 07 02:29:02 Tijolao systemd[1060]: 9router.service: Failed with result 'signal'.
out 07 02:29:02 Tijolao systemd[1060]: 9router.service: Consumed 10.534s CPU time.
out 07 02:29:07 Tijolao systemd[1060]: 9router.service: Scheduled restart job, restart counter is at 2.
out 07 02:29:07 Tijolao systemd[1060]: Started 9router.service - 9Router local AI gateway.
out 07 02:29:11 Tijolao node[23840]: ⚠ Network-exposed: reachable at http://192.168.15.186:20128 (bound 0.0.0.0). Use --host 127.0.0.1 for local-only.
out 07 02:29:11 Tijolao node[23840]: 🚀 9router v0.5.95
out 07 02:29:11 Tijolao node[23840]: Server: http://localhost:20128
out 07 02:29:11 Tijolao node[23905]: ▲ Next.js 16.3.4
out 07 02:29:11 Tijolao node[23905]: - Local:         http://localhost:20128
out 07 02:29:11 Tijolao node[23905]: - Network:       http://0.0.0.0:20128
out 07 02:29:11 Tijolao node[23905]: ✓ Ready in 0ms
===KERNEL-OOM===
===MEM===
               total       usada       livre    compart.  buff/cache  disponível
Mem.:          7,6Gi       4,2Gi       659Mi       236Mi       3,3Gi       3,4Gi
```


## D2. host: glm-5.3-flash no catalog raw + DB (nomes/urls, sem chaves) + .9router mtimes + fd cloudflared

```
===CATALOG-RAW-GREP===
raw glm-5.3-flash ocorrencias: 88
   .deepinfra.zai-org/GLM-5.3-Flash
   .zai.glm-5.3-flash
   .zai.glm-5.3-flashx
   .cloudflare-workers-ai.@cf/zai-org/glm-5.3-flash
   .engy.glm-5.3-flash
   .nano-gpt.z-ai/glm-5.3-flash-apex-abliterated
   .nano-gpt.z-ai/glm-5.3-flash
   .nano-gpt.z-ai/glm-5.3-flash-uncensored
raw glm-5.3 (qualquer) ocorrencias: 176
catalog glm-5.3-flash ocorrencias: 81
   .models.deepinfra:glm-5.3-flash
   .models.glm:glm-5.3-flash
   .models.zai:glm-5.3-flash
   .models.glm:glm-5.3-flashx
   .models.zai:glm-5.3-flashx
   .models.cloudflare-ai:glm-5.3-flash
   .models.cloudflare-workers-ai:glm-5.3-flash
   .models.engy:glm-5.3-flash
catalog glm-5.3 (qualquer) ocorrencias: 87
===DB-TABELAS===
tabelas: ['_meta', 'settings', 'providerConnections', 'providerNodes', 'proxyPools', 'apiKeys', 'combos', 'kv', 'usageHistory', 'sqlite_sequence', 'usageDaily', 'requestDetails']
-- settings (cols: ['id', 'data'])
-- providerConnections (cols: ['id', 'provider', 'authType', 'name', 'email', 'priority', 'isActive', 'data', 'createdAt', 'updatedAt'])
    b5883d1c-d18f-45bf-ad7f-e0718791f11e | glm | apikey | glm-api | None | 1 | 0 | {"apiKey":"002d9044a3774144b6d24d841626d8d5.2tiy1ua52iWzP3C5","testStatus":"unav | 2026-08-22T22:30:01.136Z | 2026-08-22T22:30:15.544Z
    62d59186-a715-43e1-887c-0d89db4e72ca | glm-cn | apikey | glm-api | None | 1 | 0 | {"apiKey":"002d9044a3774144b6d24d841626d8d5.2tiy1ua52iWzP3C5","testStatus":"unav | 2026-08-23T00:00:38.105Z | 2026-08-23T00:00:47.883Z
-- providerNodes (cols: ['id', 'type', 'name', 'data', 'createdAt', 'updatedAt'])
-- combos (cols: ['id', 'name', 'kind', 'models', 'createdAt', 'updatedAt'])
-- usageHistory (cols: ['id', 'timestamp', 'provider', 'model', 'connectionId', 'apiKey', 'endpoint', 'promptTokens', 'completionTokens', 'cost', 'status', 'tokens', 'meta'])
    4 | 2026-08-22T22:15:43.383Z | gemini | gemini-3.5-flash-lite | 527bdd75-de9d-481e-9bfb-3e91db7aceef | /api/v1/chat/completions | 0.000247 | ok | {}
    5 | 2026-08-22T22:15:45.767Z | gemini | gemini-3.6-flash | 527bdd75-de9d-481e-9bfb-3e91db7aceef | /api/v1/chat/completions | 0.0031125000000000002 | ok | {}
    6 | 2026-08-22T22:15:46.532Z | gemini | gemini-3.1-flash-lite-preview | 527bdd75-de9d-481e-9bfb-3e91db7aceef | /api/v1/chat/completions | 0.0002515 | ok | {}
    7 | 2026-08-22T22:15:46.653Z | gemini | gemini-3-flash-preview | 527bdd75-de9d-481e-9bfb-3e91db7aceef | /api/v1/chat/completions | 0.0019135 | ok | {}
    9 | 2026-08-22T22:16:04.439Z | gemini | gemini-3.7-flash | 527bdd75-de9d-481e-9bfb-3e91db7aceef | /api/v1/chat/completions | 0.00096 | ok | {}
    17 | 2026-08-22T23:58:02.138Z | antigravity | gemini-3.7-flash-medium | 070f0a1f-e6a9-4082-b38a-c15fddf02d65 | /api/v1/chat/completions | 0.00103125 | ok | {}
    18 | 2026-08-22T23:58:08.830Z | antigravity | gemini-3.7-flash-high | 070f0a1f-e6a9-4082-b38a-c15fddf02d65 | /api/v1/chat/completions | 0.0014475 | ok | {}
    19 | 2026-08-22T23:58:18.316Z | antigravity | gemini-3.5-flash-extra-low | 070f0a1f-e6a9-4082-b38a-c15fddf02d65 | /api/v1/chat/completions | 0.000832 | ok | {}
    22 | 2026-08-22T23:58:30.935Z | antigravity | gemini-3-flash-agent | 070f0a1f-e6a9-4082-b38a-c15fddf02d65 | /api/v1/chat/completions | 0.001231 | ok | {}
    120 | 2026-08-27T02:17:38.389Z | gemini | gemini-3.7-flash | 527bdd75-de9d-481e-9bfb-3e91db7aceef | /v1/chat/completions | 0.000555 | ok | {}
    121 | 2026-08-27T02:18:48.991Z | antigravity | gemini-3.7-flash-high | 070f0a1f-e6a9-4082-b38a-c15fddf02d65 | /v1/chat/completions | 0.00132 | ok | {}
    122 | 2026-08-27T02:18:50.269Z | antigravity | gemini-3.6-flash-high | 070f0a1f-e6a9-4082-b38a-c15fddf02d65 | /v1/chat/completions | 0.0018975 | ok | {}
    297 | 2026-09-03T18:26:06.623Z | gemini | gemini-3.7-flash | 527bdd75-de9d-481e-9bfb-3e91db7aceef | /v1/chat/completions | 0.000657 | ok | {}
-- requestDetails (cols: ['id', 'timestamp', 'provider', 'model', 'connectionId', 'status', 'data'])
    2026-09-24T00:43:59.201Z-8g08km-gemini-3-8-flash | 2026-09-24T00:43:56.560Z | antigravity | gemini-3.8-flash | 070f0a1f-e6a9-4082-b38a-c15fddf02d65 | success | {"id":"2026-09-24T00:43:59.201Z-8g08km-gemini-3-8-flash","provider":"antigravity
    2026-09-25T05:33:30.407Z-rtge34-z-ai-glm-5-3 | 2026-09-25T05:33:25.384Z | nvidia | z-ai/glm-5.3 | 2e85a322-015f-4624-ac41-66e12570973f | success | {"id":"2026-09-25T05:33:30.407Z-rtge34-z-ai-glm-5-3","provider":"nvidia","model"
    1790314524432-npctyu1tx | 2026-09-25T05:35:24.438Z | nvidia | z-ai/glm-5.3 | 2e85a322-015f-4624-ac41-66e12570973f | success | {"id":"1790314524432-npctyu1tx","provider":"nvidia","model":"z-ai/glm-5.3","conn
    1790483778675-vrhpisgng | 2026-09-27T04:36:20.465Z | nvidia | z-ai/glm-5.3 | 2e85a322-015f-4624-ac41-66e12570973f | success | {"id":"1790483778675-vrhpisgng","provider":"nvidia","model":"z-ai/glm-5.3","conn
    2026-09-27T04:36:23.700Z-ndf43a-z-ai-glm-5-3 | 2026-09-27T04:36:23.005Z | nvidia | z-ai/glm-5.3 | 2e85a322-015f-4624-ac41-66e12570973f | success | {"id":"2026-09-27T04:36:23.700Z-ndf43a-z-ai-glm-5-3","provider":"nvidia","model"
    1790483812773-8og59clik | 2026-09-27T04:36:56.320Z | nvidia | z-ai/glm-5.3 | 2e85a322-015f-4624-ac41-66e12570973f | success | {"id":"1790483812773-8og59clik","provider":"nvidia","model":"z-ai/glm-5.3","conn
    2026-09-27T04:37:06.193Z-g5tmx7-z-ai-glm-5-3 | 2026-09-27T04:37:01.194Z | nvidia | z-ai/glm-5.3 | 2e85a322-015f-4624-ac41-66e12570973f | success | {"id":"2026-09-27T04:37:06.193Z-g5tmx7-z-ai-glm-5-3","provider":"nvidia","model"
    1790483824834-ajdusc39z | 2026-09-27T04:37:07.301Z | nvidia | z-ai/glm-5.3 | 2e85a322-015f-4624-ac41-66e12570973f | success | {"id":"1790483824834-ajdusc39z","provider":"nvidia","model":"z-ai/glm-5.3","conn
    2026-09-27T04:37:12.303Z-ndan6z-z-ai-glm-5-3 | 2026-09-27T04:37:11.637Z | nvidia | z-ai/glm-5.3 | 2e85a322-015f-4624-ac41-66e12570973f | success | {"id":"2026-09-27T04:37:12.303Z-ndan6z-z-ai-glm-5-3","provider":"nvidia","model"
    1790485713535-o64alz1h0 | 2026-09-27T05:08:40.003Z | nvidia | z-ai/glm-5.3 | 2e85a322-015f-4624-ac41-66e12570973f | success | {"id":"1790485713535-o64alz1h0","provider":"nvidia","model":"z-ai/glm-5.3","conn
    1790485729075-7unyt4o5i | 2026-09-27T05:09:02.324Z | nvidia | z-ai/glm-5.3 | 2e85a322-015f-4624-ac41-66e12570973f | success | {"id":"1790485729075-7unyt4o5i","provider":"nvidia","model":"z-ai/glm-5.3","conn
    2026-09-27T05:08:54.075Z-scz16w-z-ai-glm-5-3 | 2026-09-27T05:08:53.073Z | nvidia | z-ai/glm-5.3 | 2e85a322-015f-4624-ac41-66e12570973f | success | {"id":"2026-09-27T05:08:54.075Z-scz16w-z-ai-glm-5-3","provider":"nvidia","model"
    2026-09-27T05:09:02.043Z-3aokbd-z-ai-glm-5-3 | 2026-09-27T05:08:57.043Z | nvidia | z-ai/glm-5.3 | 2e85a322-015f-4624-ac41-66e12570973f | success | {"id":"2026-09-27T05:09:02.043Z-3aokbd-z-ai-glm-5-3","provider":"nvidia","model"
    1790486201067-q6kpc59s8 | 2026-09-27T05:16:41.128Z | antigravity | gemini-3.8-flash | 070f0a1f-e6a9-4082-b38a-c15fddf02d65 | success | {"id":"1790486201067-q6kpc59s8","provider":"antigravity","model":"gemini-3.8-fla
    1790720060989-kaal3ylwo | 2026-09-29T22:14:20.990Z | cloudflare-ai | @cf/zai-org/glm-4.7-flash | 4cf146d0-2dd3-496e-96d1-5ac3474f9a5d | success | {"id":"1790720060989-kaal3ylwo","provider":"cloudflare-ai","model":"@cf/zai-org/
    1790720062753-xoflpelq0 | 2026-09-29T22:14:22.772Z | antigravity | gemini-3.8-flash | 070f0a1f-e6a9-4082-b38a-c15fddf02d65 | success | {"id":"1790720062753-xoflpelq0","provider":"antigravity","model":"gemini-3.8-fla
    1790720069677-p2iltc4fl | 2026-09-29T22:14:29.678Z | cloudflare-ai | @cf/zai-org/glm-4.7-flash | 4cf146d0-2dd3-496e-96d1-5ac3474f9a5d | success | {"id":"1790720069677-p2iltc4fl","provider":"cloudflare-ai","model":"@cf/zai-org/
    1790720082871-dgk3wnoxi | 2026-09-29T22:14:42.872Z | cloudflare-ai | @cf/zai-org/glm-4.7-flash | 4cf146d0-2dd3-496e-96d1-5ac3474f9a5d | success | {"id":"1790720082871-dgk3wnoxi","provider":"cloudflare-ai","model":"@cf/zai-org/
    1790720084672-u8ebvwkni | 2026-09-29T22:14:44.685Z | antigravity | gemini-3.8-flash | 070f0a1f-e6a9-4082-b38a-c15fddf02d65 | success | {"id":"1790720084672-u8ebvwkni","provider":"antigravity","model":"gemini-3.8-fla
    1790720099093-n7en3bhrl | 2026-09-29T22:14:59.119Z | antigravity | gemini-3.8-flash | 070f0a1f-e6a9-4082-b38a-c15fddf02d65 | success | {"id":"1790720099093-n7en3bhrl","provider":"antigravity","model":"gemini-3.8-fla
    1790720144512-ndbdljnyo | 2026-09-29T22:15:44.517Z | antigravity | gemini-3.8-flash | 070f0a1f-e6a9-4082-b38a-c15fddf02d65 | success | {"id":"1790720144512-ndbdljnyo","provider":"antigravity","model":"gemini-3.8-fla
    1790720324758-1m3xqtma9 | 2026-09-29T22:18:44.760Z | antigravity | gemini-3.8-flash | 070f0a1f-e6a9-4082-b38a-c15fddf02d65 | success | {"id":"1790720324758-1m3xqtma9","provider":"antigravity","model":"gemini-3.8-fla
    1790720385100-srvot52bj | 2026-09-29T22:19:45.118Z | antigravity | gemini-3.8-flash | 070f0a1f-e6a9-4082-b38a-c15fddf02d65 | success | {"id":"1790720385100-srvot52bj","provider":"antigravity","model":"gemini-3.8-fla
    1790720441263-rx9ag0lu1 | 2026-09-29T22:20:41.305Z | antigravity | gemini-3.8-flash | 070f0a1f-e6a9-4082-b38a-c15fddf02d65 | success | {"id":"1790720441263-rx9ag0lu1","provider":"antigravity","model":"gemini-3.8-fla
    2026-09-29T22:26:10.072Z-4dnk28-gemini-3-8-flash | 2026-09-29T22:26:05.071Z | antigravity | gemini-3.8-flash | 070f0a1f-e6a9-4082-b38a-c15fddf02d65 | success | {"id":"2026-09-29T22:26:10.072Z-4dnk28-gemini-3-8-flash","provider":"antigravity
    1790720774297-9zlnbp2l6 | 2026-09-29T22:26:15.356Z | nvidia | z-ai/glm-5.3 | 2e85a322-015f-4624-ac41-66e12570973f | success | {"id":"1790720774297-9zlnbp2l6","provider":"nvidia","model":"z-ai/glm-5.3","conn
    2026-09-29T22:27:08.113Z-t0kiqy-gemini-3-8-flash | 2026-09-29T22:27:03.113Z | antigravity | gemini-3.8-flash | 070f0a1f-e6a9-4082-b38a-c15fddf02d65 | success | {"id":"2026-09-29T22:27:08.113Z-t0kiqy-gemini-3-8-flash","provider":"antigravity
    1790720829951-j7q1vj9dt | 2026-09-29T22:27:09.997Z | antigravity | gemini-3.8-flash | 070f0a1f-e6a9-4082-b38a-c15fddf02d65 | success | {"id":"1790720829951-j7q1vj9dt","provider":"antigravity","model":"gemini-3.8-fla
    1790720833455-q7tpw3zpv | 2026-09-29T22:27:13.455Z | nvidia | z-ai/glm-5.3 | 2e85a322-015f-4624-ac41-66e12570973f | success | {"id":"1790720833455-q7tpw3zpv","provider":"nvidia","model":"z-ai/glm-5.3","conn
    1790720874236-g9w1y51dq | 2026-09-29T22:27:54.432Z | antigravity | gemini-3.8-flash | 070f0a1f-e6a9-4082-b38a-c15fddf02d65 | success | {"id":"1790720874236-g9w1y51dq","provider":"antigravity","model":"gemini-3.8-fla
    1790720880106-m6fufw2d8 | 2026-09-29T22:28:00.137Z | antigravity | gemini-3.8-flash | 070f0a1f-e6a9-4082-b38a-c15fddf02d65 | success | {"id":"1790720880106-m6fufw2d8","provider":"antigravity","model":"gemini-3.8-fla
    1790720885883-74r5rlmlg | 2026-09-29T22:28:05.936Z | antigravity | gemini-3.8-flash | 070f0a1f-e6a9-4082-b38a-c15fddf02d65 | success | {"id":"1790720885883-74r5rlmlg","provider":"antigravity","model":"gemini-3.8-fla
    1790720890125-fyz4r6uct | 2026-09-29T22:28:10.162Z | antigravity | gemini-3.8-flash | 070f0a1f-e6a9-4082-b38a-c15fddf02d65 | success | {"id":"1790720890125-fyz4r6uct","provider":"antigravity","model":"gemini-3.8-fla
    1790720895472-cctimovgc | 2026-09-29T22:28:15.545Z | antigravity | gemini-3.8-flash | 070f0a1f-e6a9-4082-b38a-c15fddf02d65 | success | {"id":"1790720895472-cctimovgc","provider":"antigravity","model":"gemini-3.8-fla
    1790720904490-g5a6z8tyt | 2026-09-29T22:28:24.543Z | antigravity | gemini-3.8-flash | 070f0a1f-e6a9-4082-b38a-c15fddf02d65 | success | {"id":"1790720904490-g5a6z8tyt","provider":"antigravity","model":"gemini-3.8-fla
    1790720910306-mitlcm6uk | 2026-09-29T22:28:30.944Z | antigravity | gemini-3.8-flash | 070f0a1f-e6a9-4082-b38a-c15fddf02d65 | success | {"id":"1790720910306-mitlcm6uk","provider":"antigravity","model":"gemini-3.8-fla
    1790720917732-1w9dtuuia | 2026-09-29T22:28:37.740Z | antigravity | gemini-3.8-flash | 070f0a1f-e6a9-4082-b38a-c15fddf02d65 | success | {"id":"1790720917732-1w9dtuuia","provider":"antigravity","model":"gemini-3.8-fla
    1790720923987-7btqnal2k | 2026-09-29T22:28:44.007Z | antigravity | gemini-3.8-flash | 070f0a1f-e6a9-4082-b38a-c15fddf02d65 | success | {"id":"1790720923987-7btqnal2k","provider":"antigravity","model":"gemini-3.8-fla
    1790720931364-t74uta6sn | 2026-09-29T22:28:51.425Z | antigravity | gemini-3.8-flash | 070f0a1f-e6a9-4082-b38a-c15fddf02d65 | success | {"id":"1790720931364-t74uta6sn","provider":"antigravity","model":"gemini-3.8-fla
    1790720936591-3qflw9dpy | 2026-09-29T22:28:56.612Z | antigravity | gemini-3.8-flash | 070f0a1f-e6a9-4082-b38a-c15fddf02d65 | success | {"id":"1790720936591-3qflw9dpy","provider":"antigravity","model":"gemini-3.8-fla
    1790720940882-40ic9p1qb | 2026-09-29T22:29:00.954Z | antigravity | gemini-3.8-flash | 070f0a1f-e6a9-4082-b38a-c15fddf02d65 | success | {"id":"1790720940882-40ic9p1qb","provider":"antigravity","model":"gemini-3.8-fla
    1790720944325-2bx9bxd2e | 2026-09-29T22:29:05.115Z | antigravity | gemini-3.8-flash | 070f0a1f-e6a9-4082-b38a-c15fddf02d65 | success | {"id":"1790720944325-2bx9bxd2e","provider":"antigravity","model":"gemini-3.8-fla
    2026-09-29T22:42:19.436Z-w195sl-gemini-3-8-flash | 2026-09-29T22:42:14.433Z | antigravity | gemini-3.8-flash | 070f0a1f-e6a9-4082-b38a-c15fddf02d65 | error | {"id":"2026-09-29T22:42:19.436Z-w195sl-gemini-3-8-flash","provider":"antigravity
    2026-09-29T23:05:17.012Z-xuh4qd-gemini-3-8-flash | 2026-09-29T23:05:12.010Z | antigravity | gemini-3.8-flash | 070f0a1f-e6a9-4082-b38a-c15fddf02d65 | success | {"id":"2026-09-29T23:05:17.012Z-xuh4qd-gemini-3-8-flash","provider":"antigravity
===DOT-9ROUTER-MTIMES===
2026-09-23 23:31 /home/dr/.9router/logs
2026-09-23 23:31 /home/dr/.9router/logs/mitm
2026-09-23 23:31 /home/dr/.9router/machine-id
2026-09-23 23:31 /home/dr/.9router/runtime/mitm
2026-09-23 23:34 /home/dr/.9router/runtime
2026-09-23 23:34 /home/dr/.9router/runtime/package.json
2026-09-23 23:34 /home/dr/.9router/runtime/package-lock.json
2026-10-04 19:31 /home/dr/.9router/db/data.sqlite
2026-10-07 02:25 /home/dr/.9router/db
2026-10-07 02:25 /home/dr/.9router/db/data.sqlite-wal
2026-10-07 02:29 /home/dr/.9router/db/data.sqlite-shm
2026-10-07 03:18 /home/dr/.9router/runtime/node_modules
===CLOUDFLARED-CONFIG-FD===
```


## D3. hermes --help (diagnosticos disponiveis)

```
/opt/hermes/bin/hermes
usage: hermes [-h] [--version] [-z PROMPT] [--usage-file PATH] [-m MODEL]
              [--provider PROVIDER] [--reasoning LEVEL] [-t TOOLSETS]
              [--resume SESSION] [--no-restore-cwd] [--in DIR]
              [--continue [SESSION_NAME]] [--worktree] [--accept-hooks]
              [--skills SKILLS] [--yolo] [--pass-session-id]
              [--ignore-user-config] [--ignore-rules] [--safe-mode] [--tui]
              [--cli] [--dev]
              {chat,model,moa,fallback,worktree,browser,secrets,egress,migrate,gateway,proxy,lsp,setup,whatsapp,whatsapp-cloud,slack,send,login,logout,auth,status,pause,resume,cron,sync,webhook,peer,portal,kanban,project,hooks,doctor,verify,security,approvals,dump,debug,backup,checkpoints,import,import-agent,config,skin,console,pairing,skills,bundles,plugins,curator,pets,journey,learning,memory-graph,memory,tools,computer-use,mcp,sessions,insights,monitoring,claw,update,uninstall,acp,profile,completion,dashboard,serve,desktop,gui,logs,prompt-size} ...

Hermes Agent - AI assistant with tool-calling capabilities

positional arguments:
  {chat,model,moa,fallback,worktree,browser,secrets,egress,migrate,gateway,proxy,lsp,setup,whatsapp,whatsapp-cloud,slack,send,login,logout,auth,status,pause,resume,cron,sync,webhook,peer,portal,kanban,project,hooks,doctor,verify,security,approvals,dump,debug,backup,checkpoints,import,import-agent,config,skin,console,pairing,skills,bundles,plugins,curator,pets,journey,learning,memory-graph,memory,tools,computer-use,mcp,sessions,insights,monitoring,claw,update,uninstall,acp,profile,completion,dashboard,serve,desktop,gui,logs,prompt-size}
                        Command to run
    chat                Interactive chat with the agent
    model               Select default model and provider
    moa                 Configure Mixture of Agents provider/model slots
    fallback            Manage fallback providers (tried when the primary
                        model fails)
    worktree            Audit and reclaim accumulated git worktrees and merged
                        branches
    browser             Real-profile browsing helpers (close a browser locking
                        its profile)
    secrets             Manage external secret sources (Bitwarden, 1Password)
    egress              Manage the iron-proxy egress credential-injection
                        firewall
    migrate             Migrate configuration for retired models or deprecated
                        settings
    gateway             Messaging gateway management
    proxy               Local OpenAI-compatible proxy to OAuth providers
    lsp                 Language Server Protocol management
    setup               Interactive setup wizard
    whatsapp            Set up WhatsApp integration
    whatsapp-cloud      Set up WhatsApp Business Cloud API integration
    slack               Slack integration helpers (manifest generation, etc.)
    send                Send a message to a configured platform (scripts, cron
                        jobs, CI).
    logout              Clear authentication for an inference provider
    auth                Manage pooled provider credentials
    status              Show status of all components
    pause               Emergency stop: pause cron/kanban dispatch and new
                        gateway turns
    resume              Lift the emergency stop set by `hermes pause`
    cron                Cron job management
    sync                Skill Sync — sync your skills across devices and with
                        your team
    webhook             Manage dynamic webhook subscriptions
    peer                Bot-to-bot DMs across machines (peer Hermes gateways)
    portal              Set up Nous Portal (login, model pick, Tool Gateway);
                        see also `portal info`
    kanban              Multi-profile collaboration board (tasks, links,
                        comments)
    project             Manage projects (named, multi-folder workspaces)
    hooks               Inspect and manage shell-script hooks
    doctor              Check configuration and dependencies
    verify              Detect a project's run recipe and smoke-test it
    security            Supply-chain audit (OSV.dev) for venv, plugins, and
                        MCP servers
    approvals           Approval-prompt tools (mine history into allowlist
                        proposals)

```