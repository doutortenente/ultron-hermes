# Auditoria B - parcial 4


## E1. DB 9router: nvidia conn (campos seguros), settings/kv tunnel, requestDetails por modelo/status

```
== providerConnections: todas as linhas (data sem segredos) ==
nvidia | NVIDIABuild-Autogen-29 | isActive= 1 | prio= 1 | {"apiKey":"***MASKED***", "testStatus": "active", "providerSpecificData": {"connectionProxyEnabled": false, "connectionProxyUrl": "", "connectionNoProxy": ""}, "modelLock_deepseek-ai/deepseek-v4-pro": null, "errorCode": null, "backoffLevel": 0, "modelLock_z-ai/glm-5.2": null, "modelLock_minimaxai/minimax-m2.7": null, "modelLock_deepseek-ai/deepseek-v4-flash": null, "modelLock_moonshotai/kimi-k2.6": null, "modelLock_minimaxai/minimax-m3": null, "modelLock_nemotron-3-ultra-550b-a55b": null, "modelLock_nvidia/nemotron-3-ultra-550b-a55b": null, "lastUsedAt": "2026-09-03T18:26:07.398Z", "consecuti | upd 2026-10-07T05:54:56.302Z
groq | groq-apikey | isActive= 0 | prio= 1 | {"apiKey":"***MASKED***", "testStatus": "active", "providerSpecificData": {"connectionProxyEnabled": false, "connectionProxyUrl": "", "connectionNoProxy": ""}, "modelLock_qwen/qwen3-32b": null, "errorCode": null, "backoffLevel": 0, "modelLock_llama-3.3-70b-versatile": null, "modelLock_meta-llama/llama-4-maverick-17b-128e-instruct": null, "modelLock_openai/gpt-oss-120b": null, "lastUsedAt": "2026-09-03T18:26:06.929Z", "consecutiveUseCount": 1, "modelLock_llama-3.1-8b-instant": null, "modelLock_compound-mini": null} | upd 2026-09-30T00:24:55.050Z
gemini | Google-ai-studio-teste-final-08-26 | isActive= 0 | prio= 1 | {"apiKey":"***MASKED***", "testStatus": "unavailable", "providerSpecificData": {"connectionProxyEnabled": false, "connectionProxyUrl": "", "connectionNoProxy": ""}, "modelLock_gemini-2.5-pro": null, "errorCode": 429, "backoffLevel": 1, "modelLock_gemini-3.1-pro-preview": "2026-10-04T18:59:00.301Z", "modelLock_gemini-2.5-flash": null, "modelLock_gemini-2.5-flash-lite": null, "lastUsedAt": "2026-09-03T18:26:04.732Z", "consecutiveUseCount": 1, "lastError": "[429]: {\n  \"error\": {\n    \"code\": 429,\n    \"message\": \"You exceeded your current quota, please check your plan and billing details | upd 2026-10-04T18:59:05.602Z
ollama | ollama-api-key | isActive= 0 | prio= 1 | {"apiKey":"***MASKED***", "testStatus": "active", "providerSpecificData": {"connectionProxyEnabled": false, "connectionProxyUrl": "", "connectionNoProxy": ""}, "modelLock_glm-4.7-flash": null, "errorCode": null, "backoffLevel": 0, "modelLock_glm-5": null, "modelLock_minimax-m2.5": null, "modelLock_qwen3.5": null, "modelLock_kimi-k2.5": null, "modelLock_qwen3:4b": null, "modelLock_qwen3-hermes:latest": null, "lastUsedAt": "2026-09-03T18:26:06.629Z", "consecutiveUseCount": 1, "modelLock_minimax-m3": null} | upd 2026-09-15T17:27:48.749Z
glm | glm-api | isActive= 0 | prio= 1 | {"apiKey":"***MASKED***", "testStatus": "unavailable", "providerSpecificData": {"connectionProxyEnabled": false, "connectionProxyUrl": "", "connectionNoProxy": ""}, "modelLock_glm-4.7": "2026-08-22T22:30:10.273Z", "lastError": "[429]: {\"error\":{\"code\":\"1113\",\"message\":\"Insufficient balance or no resource package. Please rechar", "errorCode": 429, "lastErrorAt": "2026-08-22T22:30:10.208Z", "backoffLevel": 7, "modelLock_glm-4.6v": "2026-08-22T22:30:15.795Z", "modelLock_glm-5.1": "2026-08-22T22:30:24.239Z", "modelLock_glm-5.2": "2026-08-22T22:30:40.922Z", "modelLock_glm-5.3": "2026-08-2 | upd 2026-08-22T22:30:15.544Z
openrouter | openrouter-2 | isActive= 1 | prio= 2 | {"apiKey":"***MASKED***", "testStatus": "active", "providerSpecificData": {"connectionProxyEnabled": false, "connectionProxyUrl": "", "connectionNoProxy": ""}, "modelLock_z-ai/glm-5.2:free": null, "errorCode": null, "backoffLevel": 0, "modelLock_google/lyria-3-clip-preview": null, "modelLock_google/lyria-3-pro-preview": null, "modelLock_google/gemma-4-26b-a4b-it:free": null, "modelLock_google/gemma-4-31b-it:free": null, "modelLock_nvidia/nemotron-3-super-120b-a12b:free": null, "modelLock_cohere/north-mini-code:free": null, "modelLock_nvidia/nemotron-3-nano-30b-a3b:free": null, "modelLock_stea | upd 2026-09-15T17:29:57.848Z
openrouter | openrouter-1 | isActive= 1 | prio= 1 | {"apiKey":"***MASKED***", "testStatus": "unavailable", "providerSpecificData": {"connectionProxyEnabled": false, "connectionProxyUrl": "", "connectionNoProxy": ""}, "modelLock_z-ai/glm-5.2:free": "2026-08-28T01:47:51.417Z", "lastError": "[401]: {\"error\":{\"message\":\"User not found.\",\"code\":401}}", "errorCode": 401, "lastErrorAt": "2026-09-15T17:28:57.666Z", "backoffLevel": 0, "modelLock_nvidia/nemotron-3-ultra-550b-a55b:free": "2026-09-15T17:30:57.666Z", "modelLock_nvidia/nemotron-3.5-lightning:free": "2026-08-27T02:24:44.850Z", "modelLock_google/gemma-4-31b-it:free": "2026-08-28T01:48 | upd 2026-09-15T17:28:57.666Z
codex | ntg.trabalho@gmail.com | isActive= 1 | prio= 1 | {"accessToken": "***MASKED***", "refreshToken": "***MASKED***", "expiresAt": "2026-10-12T04:18:21.821Z", "testStatus": "unavailable", "expiresIn": 864000, "idToken": "***MASKED***", "lastRefreshAt": "2026-10-02T04:18:21.821Z", "providerSpecificData": {"chatgptAccountId": "08547595-11ce-4fdd-90de-bfdc5ab00866", "chatgptPlanType": "plus"}, "modelLock_gpt-5.3-codex-spark-review": null, "errorCode": 429, "backoffLevel": 0, "modelLock_gpt-5.3-codex-spark": null, "modelLock_gpt-5.6-sol": null, "modelLock_gpt-5.6-terra": "2026-10-04T16:26:23.991Z", "modelLock_gpt-5.6-luna": "2026-09-29T22:44:47.170Z" | upd 2026-10-04T15:56:23.991Z
github | doutortenente | isActive= 0 | prio= 1 | {"displayName": "doutortenente", "accessToken": "***MASKED***", "testStatus": "active", "providerSpecificData": {"copilotToken": "tid=53ba97eba8969ccfaf5824285e92ff81;exp=1791007138;iat=1790920738;sku=free_limited_copilot;proxy-ep=proxy.individual.githubcopilot.com;st=dotcom;chat=1;cit=1;editor_preview_features=1;client_byok=0;agent_mode=1;agent_mode_auto_approval=1;mcp=1;blackbird_external_indexing=1;rt=1;ip=177.94.254.144;asn=AS27699;cq=2000;sl=0;rd=1792972800:3dd732b2e7591d6e2429bc24f8119bd9e756ad13382204c5992e54eb4ecb7055", "copilotTokenExpiresAt": 1791007138, "githubUserId": 271285107, "g | upd 2026-10-02T05:58:58.488Z
antigravity | ntg.trabalho@gmail.com | isActive= 1 | prio= 1 | {"accessToken": "***MASKED***", "refreshToken": "***MASKED***", "expiresAt": "2026-10-07T06:59:20.103Z", "scope": "https://www.googleapis.com/auth/experimentsandconfigs https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/cloud-platform https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/cclog openid", "projectId": "grounded-shell-z9p3r", "testStatus": "unavailable", "expiresIn": 3599, "lastRefreshAt": "2026-10-07T05:59:21.103Z", "lastUsedAt": "2026-09-03T18:24:59.328Z", "consecutiveUseCount": 3, "modelLock_gemini-pro-agent": null, "errorC | upd 2026-10-07T05:59:21.104Z
mistral | Vibe-API | isActive= 0 | prio= 1 | {"apiKey":"***MASKED***", "testStatus": "active", "providerSpecificData": {"connectionProxyEnabled": false, "connectionProxyUrl": "", "connectionNoProxy": ""}, "modelLock_mistral-large-latest": "2026-09-15T17:25:59.257Z", "errorCode": 403, "backoffLevel": 0, "modelLock_codestral-latest": null} | upd 2026-09-30T00:24:49.407Z
glm-cn | glm-api | isActive= 0 | prio= 1 | {"apiKey":"***MASKED***", "testStatus": "unavailable", "providerSpecificData": {"connectionProxyEnabled": false, "connectionProxyUrl": "", "connectionNoProxy": ""}, "modelLock_glm-4.7": "2026-08-23T00:00:42.150Z", "lastError": "[429]: {\"error\":{\"code\":\"1113\",\"message\":\"余额不足或无可用资源包,请充值。\"}}", "errorCode": 429, "lastErrorAt": "2026-08-23T00:00:45.709Z", "backoffLevel": 7, "modelLock_glm-4.5-air": "2026-08-23T00:00:46.365Z", "modelLock_glm-5": "2026-08-23T00:00:50.949Z", "modelLock_glm-5.3": "2026-08-23T00:00:59.448Z", "modelLock_glm-5.2": "2026-08-23T00:01:16.371Z", "modelLock_glm-5.1" | upd 2026-08-23T00:00:47.883Z
openai | openai-api-key | isActive= 0 | prio= 1 | {"apiKey":"***MASKED***", "testStatus": "unavailable", "providerSpecificData": {"connectionProxyEnabled": false, "connectionProxyUrl": "", "connectionNoProxy": ""}, "modelLock_gpt-5": "2026-08-23T00:02:13.161Z", "lastError": "[429]: {\n    \"error\": {\n        \"message\": \"You have no credits remaining. Add credits to continue u", "errorCode": 429, "lastErrorAt": "2026-08-23T00:02:18.523Z", "backoffLevel": 10, "modelLock_gpt-4o-mini": "2026-08-23T00:02:17.623Z", "modelLock_gpt-4.1": "2026-08-23T00:02:21.937Z", "modelLock_gpt-4.1-nano": "2026-08-23T00:02:30.505Z", "modelLock_o3-pro": "2026- | upd 2026-08-23T00:02:26.417Z
poolside | poolside-api | isActive= 1 | prio= 1 | {"apiKey":"***MASKED***", "testStatus": "active", "providerSpecificData": {"connectionProxyEnabled": false, "connectionProxyUrl": "", "connectionNoProxy": ""}, "lastUsedAt": "2026-09-03T18:06:29.846Z", "consecutiveUseCount": 2, "modelLock_laguna-s-2.1": null, "errorCode": null, "backoffLevel": 0, "modelLock_laguna-xs-2.1": null} | upd 2026-10-04T15:22:26.076Z
openrouter | Buceta do caralho | isActive= 1 | prio= 3 | {"apiKey":"***MASKED***", "testStatus": "unavailable", "providerSpecificData": {"connectionProxyEnabled": false, "connectionProxyUrl": "", "connectionNoProxy": ""}, "lastUsedAt": "2026-10-02T22:34:26.568Z", "consecutiveUseCount": 1, "modelLock_google/lyria-3-pro-preview": null, "errorCode": 502, "backoffLevel": 0, "modelLock_z-ai/glm-5.2:free": null, "modelLock_poolside/laguna-xs-2.1:free": null, "modelLock_nvidia/nemotron-3-nano-30b-a3b:free": null, "modelLock_thinkingmachines/inkling:free": null, "modelLock_google/gemma-4-26b-a4b-it:free": null, "modelLock_thinkingmachines/inkling-small:fre | upd 2026-10-02T22:34:26.568Z
gemini-cli | ntg.trabalho@gmail.com | isActive= 0 | prio= 1 | {"accessToken": "***MASKED***", "refreshToken": "***MASKED***", "expiresAt": "2026-10-04T19:57:47.310Z", "scope": "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/cloud-platform openid", "projectId": "", "testStatus": "unavailable", "expiresIn": 3599, "lastUsedAt": "2026-09-03T18:05:18.258Z", "consecutiveUseCount": 1, "modelLock_gemini-3.1-pro-preview": "2026-10-04T18:59:49.212Z", "errorCode": 403, "backoffLevel": 0, "modelLock_gemini-2.5-flash": null, "modelLock_gemini-3.1-flash-lite-preview": null, "modelLock_gem | upd 2026-10-04T18:58:15.204Z
cerebras | Default Key | isActive= 0 | prio= 2 | {"apiKey":"***MASKED***", "testStatus": "unavailable", "providerSpecificData": {"connectionProxyEnabled": false, "connectionProxyUrl": "", "connectionNoProxy": ""}, "lastUsedAt": "2026-09-03T18:10:04.587Z", "consecutiveUseCount": 3, "modelLock_zai-glm-4.7": "2026-09-15T17:25:48.475Z", "errorCode": 404, "backoffLevel": 0, "modelLock_gpt-oss-120b": "2026-09-15T17:25:44.308Z", "modelLock_llama-4-scout-17b-16e-instruct": "2026-09-15T17:25:47.688Z", "modelLock_qwen-3-235b-a22b-instruct-2507": "2026-09-15T17:25:46.156Z", "modelLock_qwen-3-32b": "2026-09-15T17:25:47.063Z", "modelLock_llama-3.3-70b": | upd 2026-09-15T17:23:50.646Z
cerebras | celebras-api | isActive= 0 | prio= 1 | {"apiKey":"***MASKED***", "testStatus": "unavailable", "providerSpecificData": {"connectionProxyEnabled": false, "connectionProxyUrl": "", "connectionNoProxy": ""}, "lastUsedAt": "2026-09-03T18:10:04.412Z", "consecutiveUseCount": 3, "modelLock_zai-glm-4.7": "2026-09-15T17:25:48.301Z", "errorCode": 404, "backoffLevel": 0, "modelLock_gpt-oss-120b": "2026-09-15T17:25:44.088Z", "modelLock_llama-4-scout-17b-16e-instruct": "2026-09-15T17:25:47.511Z", "modelLock_qwen-3-235b-a22b-instruct-2507": "2026-09-15T17:25:45.980Z", "modelLock_qwen-3-32b": "2026-09-15T17:25:46.900Z", "modelLock_llama-3.3-70b": | upd 2026-09-15T17:23:50.198Z
cloudflare-ai | cloudflare-api | isActive= 1 | prio= 1 | {"apiKey":"***MASKED***", "testStatus": "active", "providerSpecificData": {"accountId": "dc7a6db66a4829e742f351dbf7d4e3a2", "connectionProxyEnabled": false, "connectionProxyUrl": "", "connectionNoProxy": ""}, "modelLock_@cf/meta/llama-3.1-8b-instruct-awq": null, "errorCode": null, "backoffLevel": 0, "modelLock_@cf/moonshotai/kimi-k2.6": null, "modelLock_@cf/moonshotai/kimi-k2.5": null} | upd 2026-09-15T17:21:04.704Z
grok-cli | ntg.trabalho@gmail.com | isActive= 0 | prio= 1 | {"displayName": "Nicholas Teixeira", "accessToken": "***MASKED***", "refreshToken": "***MASKED***", "expiresAt": "2026-10-02T11:58:59.551Z", "scope": "openid profile email offline_access grok-cli:access api:access conversations:read conversations:write", "testStatus": "active", "expiresIn": 21600, "providerSpecificData": {"authMethod": "device_code", "idToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6Im9hdXRoMi1wcm9kdWN0aW9uLTIwMjYtMDItMTkifQ.eyJpc3MiOiJodHRwczovL2F1dGgueC5haSIsInN1YiI6IjgxYWEwMGIwLTI3NzUtNDc5OC05Y2Y4LTBjMWQ3ODBjZDdmNiIsImF1ZCI6ImIxYTAwNDkyLTA3M2EtNDdlYS04MTZmLTRjMzI5MjY0 | upd 2026-10-02T05:58:59.551Z
claude | Account 1 | isActive= 1 | prio= 1 | {"accessToken": "***MASKED***", "refreshToken": "***MASKED***", "expiresAt": "2026-10-07T13:26:52.985Z", "scope": "user:inference user:profile", "testStatus": "active", "expiresIn": 28800, "lastRefreshAt": "2026-10-07T05:26:52.985Z", "modelLock_claude-sonnet-5-5": null, "errorCode": null, "backoffLevel": 0, "modelLock_claude-opus-5-5": null, "lastError": null, "lastErrorAt": null, "rateLimitedUntil": null} | upd 2026-10-07T05:54:58.931Z
== settings: chaves relacionadas a tunnel/publicUrl/expose ==
Traceback (most recent call last):
  File "<stdin>", line 16, in <module>
  File "/usr/lib/python3.12/re/__init__.py", line 186, in sub
    return _compile(pattern, flags).sub(repl, string, count)
           ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/re/__init__.py", line 307, in _compile
    p = _compiler.compile(pattern, flags)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/re/_compiler.py", line 745, in compile
    p = _parser.parse(p, flags)
        ^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/re/_parser.py", line 979, in parse
    p = _parse_sub(source, state, flags & SRE_FLAG_VERBOSE, 0)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/re/_parser.py", line 460, in _parse_sub
    itemsappend(_parse(source, state, verbose, nested + 1,
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/re/_parser.py", line 862, in _parse
    p = _parse_sub(source, state, sub_verbose, nested + 1)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/re/_parser.py", line 460, in _parse_sub
    itemsappend(_parse(source, state, verbose, nested + 1,
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.12/re/_parser.py", line 840, in _parse
    raise source.error('global flags not at the start '
re.error: global flags not at the start of the expression at position 2
```


## E2. model-catalog raw: modelos glm sob nvidia; flash existe em quais providers

```
nvidia+glm no raw catalog: 0
glm-5.3-flash aparece em (top paths):
top keys raw: ['deepinfra', 'perplexity-agent', 'bailing', 'poe', 'cerebras', 'groq', 'blueclaw', 'zai', 'empiriolabs', 'sensenova', 'alibaba-token-plan', 'cloudflare-workers-ai', 'engy', 'poolside', 'nano-gpt', 'abliteration-ai', 'crof', 'standardcompute', 'cloudferro-sherlock', 'anthropic']
```


## E3. ~/.9router: conteudo detalhado (mtimes, tamanhos)

```
2026-09-23 23:31       4096 /home/dr/.9router/runtime/mitm
2026-10-07 03:18       4096 /home/dr/.9router/runtime/node_modules
2026-10-02 01:45       4096 /home/dr/.9router/runtime/node_modules/.bin
2026-10-07 03:18       4096 /home/dr/.9router/runtime/node_modules/debug
2026-10-07 03:18       4096 /home/dr/.9router/runtime/node_modules/fs-extra
2026-10-07 03:18       4096 /home/dr/.9router/runtime/node_modules/graceful-fs
2026-10-07 03:18       4096 /home/dr/.9router/runtime/node_modules/jsonfile
2026-10-07 03:18       4096 /home/dr/.9router/runtime/node_modules/ms
2026-09-23 23:34       4096 /home/dr/.9router/runtime/node_modules/sql.js
2026-10-07 03:18       4096 /home/dr/.9router/runtime/node_modules/systray2
2026-10-07 03:18       4096 /home/dr/.9router/runtime/node_modules/universalify
2026-09-23 23:34        509 /home/dr/.9router/runtime/package-lock.json
2026-09-23 23:31         64 /home/dr/.9router/auth/cli-secret
2026-09-23 23:31         64 /home/dr/.9router/jwt-secret
2026-09-23 23:31         64 /home/dr/.9router/machine-id
===DB-SIZE===
4,0K	/home/dr/.9router/db/backups
172K	/home/dr/.9router/db/data.sqlite
32K	/home/dr/.9router/db/data.sqlite-shm
0	/home/dr/.9router/db/data.sqlite-wal
```


## E4. journal desde boot: contagens exatas por tipo + janelas

```
linhas totais: 259 (desde boot 01:26:31 ate agora)
===CONTAGENS-EXATAS===
ERROR 502 (router): 4
fetch connect timeout: 20
locked modelLock: 4
[AUTH] linhas: 10
all N accounts locked: 4
POST flash: 6
POST glm-5.3 (base): 57
POST claude-opus-5-5: 11
POST laguna: 2
DONE linhas: 67
===PRIMEIRO-ULTIMO-ERRO-502===
out 07 02:40:20 Tijolao node[23905]: [02:40:20] 🟣 ✗ ERROR 502 · nvidia/z-ai/glm-5.3-flash · 249006ms
out 07 02:51:48 Tijolao node[23905]: [02:51:48] 🟤 ✗ ERROR 502 · nvidia/z-ai/glm-5.3-flash · 249006ms
===FLASH: primeiro e ultimo POST===
out 07 02:30:17 Tijolao node[23905]: [02:30:17] 🟤 ▶ POST nvidia/z-ai/glm-5.3-flash → nvidia/z-ai/glm-5.3-flash · FMT: openai→openai · STREAM · 2 MSG · 18 TOOL · THINK:auto · ACC:NVIDIABuild-Autogen-29
out 07 02:47:39 Tijolao node[23905]: [02:47:39] 🟤 ▶ POST nvidia/z-ai/glm-5.3-flash → nvidia/z-ai/glm-5.3-flash · FMT: openai→openai · STREAM · 1 MSG · THINK:auto · ACC:NVIDIABuild-Autogen-29
===OPUS: POST e DONE seguinte===
out 07 02:45:02 Tijolao node[23905]: [02:45:02] 🟤 ▶ POST cc/claude-opus-5-5 → claude/claude-opus-5-5 · FMT: openai→claude · STREAM · 7 MSG · 38 TOOL · THINK:max · ACC:Account 1
out 07 02:45:20 Tijolao node[23905]: [02:45:20] 🟤 📊 DONE 17727ms · TTFT 2466ms · IN 31914 (CACHE +31861) · OUT 1433
out 07 02:45:21 Tijolao node[23905]: [02:45:21] 🟤 ▶ POST cc/claude-opus-5-5 → claude/claude-opus-5-5 · FMT: openai→claude · STREAM · 9 MSG · 38 TOOL · THINK:max · ACC:Account 1
out 07 02:45:28 Tijolao node[23905]: [02:45:28] 🟤 📊 DONE 6926ms · TTFT 1792ms · IN 41162 (CACHE ↻31861 +9299) · OUT 655
out 07 02:45:29 Tijolao node[23905]: [02:45:29] 🟤 ▶ POST cc/claude-opus-5-5 → claude/claude-opus-5-5 · FMT: openai→claude · STREAM · 11 MSG · 38 TOOL · THINK:max · ACC:Account 1
out 07 02:45:34 Tijolao node[23905]: [02:45:34] 🟤 📊 DONE 5403ms · TTFT 1278ms · IN 42666 (CACHE ↻41160 +1504) · OUT 379
bash: linha 23: erro de sintaxe próximo ao token inesperado `('
bash: linha 23: `echo ===BASE: POST e DONE seguinte (pos 03:00)==='
```


## E5. bash history: comandos 9router/cloudflared recentes (timestamps)

```
history: /home/dr/.bash_history existe, 62 linhas
12:sudo npm i -g 9router@latest --prefer-online
13:9router
14:9router
15:sudo npm i -g 9router@latest --prefer-online
16:9router
31:npm i -g 9router@latest --prefer-online
51:9router
52:9router
61:9router
62:9router
9router
9router
9router
9router
-rw------- 1 dr dr 1051 2026-10-07 02:30:05.189746549 -0300 /home/dr/.bash_history
```


## E6. docker-compose.tijolao.yml (conteudo)

```
# Stack Hermes do Tijolao — arquivo proprio, NAO e override do upstream.
# Use sempre via ./tijolao.sh (que passa -f docker-compose.tijolao.yml).
# O docker-compose.yml original do upstream fica intacto, so como referencia.
#
# Por que rede host nos dois servicos:
#   ~/.hermes/config.yaml aponta para servicos de loopback do HOST —
#   9Router em http://127.0.0.1:20128/v1 e Ollama em http://127.0.0.1:11434/v1.
#   Em rede bridge, 127.0.0.1 dentro do container e o proprio container e nada
#   disso responde. Com network_mode: host o mesmo config.yaml funciona dentro e
#   fora do container, sem reescrever base_url e sem host.docker.internal.
#
# Por que bind mount em vez de volume nomeado:
#   o estado real do Hermes ja existe em /home/dr/.hermes (config.yaml, skills,
#   kanban.db, auth.json, cron). Volume nomeado criaria um SEGUNDO estado vazio.
#   Alem disso /home/dr/.hermes/.env e um symlink para /home/dr/.local/secrets/.env —
#   por isso /home/dr/src tambem e montado, no mesmo caminho, senao o
#   symlink fica pendurado dentro do container.
#
# Nada e publicado alem do loopback: 3000 (UI), 8642 (gateway), 9119 (dashboard).

name: hermes

services:
  hermes-agent:
    image: nousresearch/hermes-agent:latest
    container_name: hermes-agent
    restart: unless-stopped
    # O entrypoint da imagem cai na CLI interativa, que sai na hora sob `up -d`.
    # `gateway run` e o processo longo que serve a API e o health.
    command: ["gateway", "run", "--replace"]
    network_mode: host
    env_file:
      # Caminho absoluto no cofre da maquina (~/.local/secrets, montado :ro no container).
      # Cofre da maquina desde 25-set-2026 (reorg v3 do MAPA-DO-TIJOLAO).
      - /home/dr/.local/secrets/tijolao.env
    environment:
      # A imagem vem com HERMES_HOME=/opt/data e HERMES_WRITE_SAFE_ROOT=/opt/data.
      # Aqui os tres sao reapontados para /home/dr porque o config.yaml tem
      # caminhos absolutos do host dentro dele:
      #   skills.external_dirs -> /home/dr/.claude/skills
      #   OBSIDIAN_VAULT_PATH  -> /home/dr/vaults/celebro
      # Com os mesmos caminhos dentro do container, o config vale nos dois lados.
      HERMES_HOME: /home/dr/.hermes
      HERMES_WRITE_SAFE_ROOT: /home/dr
      HERMES_LAZY_INSTALL_TARGET: /home/dr/.hermes/lazy-packages
      HERMES_UID: "1000"          # = uid do dr, para o bind mount ser legivel
      HERMES_GID: "1000"
      HERMES_DASHBOARD: "1"
      HERMES_DASHBOARD_HOST: 127.0.0.1
      HERMES_DASHBOARD_PORT: "9119"
      API_SERVER_ENABLED: "true"
      API_SERVER_HOST: 127.0.0.1  # loopback only (a maquina tem Tailscale)
      API_SERVER_PORT: "8642"
    volumes:
      - /home/dr/.hermes:/home/dr/.hermes
      - /home/dr/src:/home/dr/src
      # exigidos pelo config.yaml (ver comentario acima)
      - /home/dr/.claude/skills:/home/dr/.claude/skills:ro
      - /home/dr/vaults/celebro:/home/dr/vaults/celebro
      - /home/dr/.local/secrets:/home/dr/.local/secrets:ro
    healthcheck:
      # As DUAS portas. Se so 8642 for testada, o compose libera o workspace
      # antes de o dashboard (9119) existir: ele sobe em mode=disconnected e so
      # se recupera na sondagem seguinte — ~18 min de "Offline" a cada restart.
      test: ["CMD-SHELL", "curl -fsS http://127.0.0.1:8642/health && curl -fsS http://127.0.0.1:9119/api/status || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 6
      start_period: 40s

  hermes-workspace:
    build:
      # O compose vive neste repo (tijolao-ai); o codigo do app vive no checkout
      # do fork. Caminho absoluto de proposito: esta e a config DESTA maquina.
      context: /home/dr/src/hermes-workspace
      dockerfile: ./Dockerfile
    image: hermes-workspace:tijolao
    container_name: hermes-workspace
    restart: unless-stopped
    depends_on:
      hermes-agent:
        condition: service_healthy
    network_mode: host
    env_file:
      - /home/dr/.local/secrets/tijolao.env
    environment:
      HOST: 127.0.0.1             # loopback:
```


## E8. teste chat flash autenticado (chave do cofre, nao impressa; max_tokens 16, timeout 60)

```
usando variavel: NINEROUTER_KEY (valor oculto)
flash -> HTTP+tempo: 200 34.345390
{"id":"chatcmpl-4c6ef349-eeca-4922-9c19-e2103e11946c","choices":[{"index":0,"message":{"content":null,"role":"assistant","reasoning_content":"The user has sent a message in Portuguese: \"responda so: ok"},"finish_reason":"length","logprobs":null}],"created":1791354466,"model":"z-ai/glm-5.3-flash","service_tier":null,"system_fingerprint":null,"object":"chat.completion","usage":{"prompt_tokens":18,"

```


## E9. hermes doctor

```

┌─────────────────────────────────────────────────────────┐
│                 🩺 Hermes Doctor                        │
└─────────────────────────────────────────────────────────┘

◆ Security Advisories
  ✓ No active security advisories

◆ MCP Server Security
  ✓ No suspicious MCP stdio commands

◆ Python Environment
  ✓ Python 3.13.5
  ✓ SQLite 3.53.4
    → SQLite source id: 2026-07-24 19:02:57 bf7c7f30031888f4e796e429ab39…
    → state.db: WAL journal mode (121.7 MB)
    → cron/executions.db: WAL journal mode (24.0 KB)
    → projects.db: WAL journal mode (44.0 KB)
    → response_store.db: WAL journal mode (20.0 KB)
    → verification_evidence.db: WAL journal mode (60.0 KB)
    → kanban.db: WAL journal mode (120.0 KB)
  ✓ Virtual environment active
  ✓ Version files consistent (0.21.1)

◆ SSL / CA Certificates
  ✓ SSL CA certificate bundle is valid

◆ Required Packages
  ✓ OpenAI SDK
  ✓ Rich (terminal UI)
  ✓ python-dotenv
  ✓ PyYAML
  ✓ HTTPX
  ✓ Croniter (cron expressions) (optional)
  ✓ python-telegram-bot (optional)
  ✓ discord.py (optional)

◆ Configuration Files
  ✓ Managed scope active: 0 config key(s), 0 env key(s) pinned by /etc/hermes
  ✓ /home/dr/.hermes/.env file exists
  ✓ API key or custom endpoint configured
  ✓ /home/dr/.hermes/config.yaml exists
  ✓ Config version up to date (v42)
  ✓ No deprecated config keys or env vars

◆ xAI Model Retirement (May 15, 2026)
  ✓ No retired xAI models in config

◆ Plugin import paths (removed Sep 14, 2026)
  ✓ No enabled plugin imports paths removed on 2026-09-14

◆ Auth Providers
  ⚠ Nous Portal auth (not logged in)
  ✓ OpenAI Codex auth (logged in)
  ⚠ MiniMax OAuth (not logged in)
  ⚠ xAI OAuth (not logged in)
    → No xAI OAuth credentials stored. Select xAI Grok OAuth (SuperGrok / Premium+) in `hermes model`.

◆ Directory Structure
  ✓ /home/dr/.hermes directory exists

```


## E10. hermes status

```

┌─────────────────────────────────────────────────────────┐
│                 ⚕ Hermes Agent Status                  │
└─────────────────────────────────────────────────────────┘

◆ Environment
  Project:      /opt/hermes
  Python:       3.13.5
  .env file:    ✓ exists
  Model:        nvidia/z-ai/glm-5.3-flash
  Provider:     Custom endpoint

◆ API Keys
  OpenRouter    ✓ sk-o...47f5
  OpenAI        ✓ sk-2...5aa7
  Google / Gemini  ✗ (not set)
  DeepSeek      ✓ sk-3...41c3
  xAI / Grok    ✓ xai-...MwjS
  NVIDIA NIM    ✓ nvap...k4iw
  Z.AI / GLM    ✗ (not set)
  Kimi          ✗ (not set)
  StepFun Step Plan  ✗ (not set)
  MiniMax       ✗ (not set)
  MiniMax-CN    ✗ (not set)
  DeepInfra     ✗ (not set)
  Firecrawl     ✓ fc-4...831a
  Tavily        ✗ (not set)
  Perplexity    ✗ (not set)
  Keenable      ✗ (not set)
  Browser Use   ✗ (not set)
  Browserbase   ✗ (not set)
  FAL           ✗ (not set)
  ElevenLabs    ✗ (not set)
  GitHub        ✗ (not set)
  Anthropic     ✗ (not set)

◆ Auth Providers
  Nous Portal   ✗ not logged in (run: hermes portal)
  OpenAI Codex  ✓ logged in
    Auth file:  /home/dr/.hermes/auth.json

```