# Auditoria B - parcial 5


## F1. catalogo raw nvidia + customModels da conexao nvidia (sem segredos) + settings/kv do DB

```
== raw: provedores com glm-5.3-flash ==
  deepinfra: contem glm-5.3-flash
  zai: contem glm-5.3-flash
  cloudflare-workers-ai: contem glm-5.3-flash
  engy: contem glm-5.3-flash
  nano-gpt: contem glm-5.3-flash
  crof: contem glm-5.3-flash
  baseten: contem glm-5.3-flash
  wandb: contem glm-5.3-flash
  umans-ai-coding-plan: contem glm-5.3-flash
  umans-ai: contem glm-5.3-flash
  siliconflow: contem glm-5.3-flash
  bothub: contem glm-5.3-flash
  privatemode-ai: contem glm-5.3-flash
  llmgateway-providers: contem glm-5.3-flash
  above: contem glm-5.3-flash
  kilo: contem glm-5.3-flash
  melious: contem glm-5.3-flash
  berget: contem glm-5.3-flash
  302ai: contem glm-5.3-flash
  openrouter: contem glm-5.3-flash
  iteracompute: contem glm-5.3-flash
  cline-pass: contem glm-5.3-flash
  modal: contem glm-5.3-flash
  coralbricks: contem glm-5.3-flash
  neuralwatt: contem glm-5.3-flash
  zenmux: contem glm-5.3-flash
  vultr: contem glm-5.3-flash
  huggingface: contem glm-5.3-flash
  vancine: contem glm-5.3-flash
  zhipuai-coding-plan: contem glm-5.3-flash
  aiand: contem glm-5.3-flash
  volcengine-coding-plan: contem glm-5.3-flash
  ollama-cloud: contem glm-5.3-flash
  nebius: contem glm-5.3-flash
  vercel: contem glm-5.3-flash
  zai-coding-plan: contem glm-5.3-flash
  greenpt: contem glm-5.3-flash
  hyper: contem glm-5.3-flash
  orcarouter: contem glm-5.3-flash
  friendli: contem glm-5.3-flash
  inco: contem glm-5.3-flash
  scnet-token-plan: contem glm-5.3-flash
  ofox: contem glm-5.3-flash
  aihubmix: contem glm-5.3-flash
  merge-gateway: contem glm-5.3-flash
  opper: contem glm-5.3-flash
  nvidia: contem glm-5.3-flash
  opencode-go: contem glm-5.3-flash
  tensorx: contem glm-5.3-flash
  pareto: contem glm-5.3-flash
  edenai: contem glm-5.3-flash
  tempr: contem glm-5.3-flash
  opencode: contem glm-5.3-flash
  zhipuai: contem glm-5.3-flash
  requesty: contem glm-5.3-flash
  synthetic: contem glm-5.3-flash
  llmgateway: contem glm-5.3-flash
  vivgrid: contem glm-5.3-flash
  tokengo: contem glm-5.3-flash
  togetherai: contem glm-5.3-flash
  cortecs: contem glm-5.3-flash
  crossmodel: contem glm-5.3-flash
  runinfra: contem glm-5.3-flash
  digitalocean: contem glm-5.3-flash
== raw: nvidia existe? True
  nvidia keys: ['baai/bge-m3', 'poolside/laguna-xs-2.1', 'abacusai/dracarys-llama-3.1-70b-instruct', 'z-ai/glm-5.3-flash', 'z-ai/glm-5.2', 'z-ai/glm-5.3', 'thinkingmachines/inkling', 'black-forest-labs/flux_1-schnell', 'black-forest-labs/flux.1-dev', 'black-forest-labs/flux_1-kontext-dev', 'black-forest-labs/flux_
  nvidia models com glm: []
  total models nvidia: 0
== conexao nvidia: data completo (apiKey removido) ==
nome: NVIDIABuild-Autogen-29
data top-level keys: ['backoffLevel', 'consecutiveUseCount', 'errorCode', 'lastError', 'lastErrorAt', 'lastUsedAt', 'modelLock_deepseek-ai/deepseek-v4-flash', 'modelLock_deepseek-ai/deepseek-v4-pro', 'modelLock_deepseek-ai/deepseek-v4.1-flash', 'modelLock_minimaxai/minimax-m2.7', 'modelLock_minimaxai/minimax-m3', 'modelLock_moonshotai/kimi-k2.6', 'modelLock_nemotron-3-ultra-550b-a55b', 'modelLock_nvidia/nemotron-3-ultra-550b-a55b', 'modelLock_z-ai/glm-5.2', 'modelLock_z-ai/glm-5.3-flash', 'providerSpecificData', 'rateLimitedUntil', 'testStatus']
providerSpecificData keys: ['connectionNoProxy', 'connectionProxyEnabled', 'connectionProxyUrl']
customModels: None
defaultModel: None
prefix: None
modelLock ativos (nao-null): {}
== settings: dump de chaves ==
 id 1 keys: ['authMode', 'capacityAdapter', 'ccFilterNaming', 'comboStrategies', 'comboStrategy', 'enableObservability', 'fallbackStrategy', 'headroomTimeoutMs', 'headroomUrl', 'mitmEnabled', 'mitmRouterBaseUrl', 'oidcClientId', 'oidcClientSecret', 'oidcIssuerUrl', 'oidcLoginLabel', 'oidcScopes', 'outboundProxyEnabled', 'password', 'ponytailEnabled', 'ponytailLevel', 'providerStrategies', 'providerThinking', 'rtkEnabled', 'ssoType', 'stickyRoundRobinLimit', 'tailscaleEnabled', 'tailscaleUrl', 'tunnelDashboardAccess', 'tunnelEnabled', 'tunnelUrl']
== kv: todas as chaves ==
   ('openrouter|nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free|llm', 161)
   ('nvidia', 149)
   ('openrouter|openrouter/free|llm', 91)
   ('oc|big-pickle|llm', 73)
   ('oc|mimo-v2.5-free|llm', 81)
   ('oc|nemotron-3-ultra-free|llm', 95)
   ('oc|hy3-free|llm', 69)
   ('oc|laguna-s-2.1-free|llm', 87)
   ('cf', 347)
   ('groq|openai/gpt-oss-20b|llm', 132)
   ('ag', 399)
   ('cx', 227)
   ('cc', 71)
   ('ollama', 75)
   ('gemini', 197)
   ('mistral', 24)
   ('groq', 92)
   ('oc|nemotron-3.5-lightning-free|llm', 107)
   ('oc|ling-3.0-flash-fin-free|llm', 99)
   ('oc', 69)
   ('gc', 101)
   ('gcli', 47)
   ('47895386-50aa-4e1a-bd36-8320729801631790016876542:call_33493', 3648)
   ('call_33493', 3648)
   ('47895386-50aa-4e1a-bd36-8320729801631790016876542:call_32303', 660)
   ('call_32303', 660)
   ('68f5b8ce-af32-4a34-ba0e-463c11a07f331790017483790:call_116414', 3132)
   ('call_116414', 3132)
   ('68f5b8ce-af32-4a34-ba0e-463c11a07f331790017483790:call_10598', 700)
   ('call_10598', 700)
   ('nvidia|z-ai/glm-5.3|llm', 123)
   ('a58cee24-e51b-414c-9304-633854d999ca1790720870750:call_107679', 1566)
   ('call_107679', 1566)
   ('a58cee24-e51b-414c-9304-633854d999ca1790720870750:call_165120', 3722)
   ('call_165120', 3722)
   ('a58cee24-e51b-414c-9304-633854d999ca1790720870750:call_147041', 2114)
   ('call_147041', 2114)
   ('a58cee24-e51b-414c-9304-633854d999ca1790720870750:call_159557', 4086)
   ('call_159557', 4086)
   ('a58cee24-e51b-414c-9304-633854d999ca1790720870750:call_102149', 446)
   ('call_102149', 446)
   ('a58cee24-e51b-414c-9304-633854d999ca1790720870750:call_108368', 2018)
   ('call_108368', 2018)
   ('a58cee24-e51b-414c-9304-633854d999ca1790720870750:call_180505', 3202)
   ('call_180505', 3202)
   ('a58cee24-e51b-414c-9304-633854d999ca1790720870750:call_165639', 726)
   ('call_165639', 726)
   ('a58cee24-e51b-414c-9304-633854d999ca1790720870750:call_168624', 686)
   ('call_168624', 686)
   ('a58cee24-e51b-414c-9304-633854d999ca1790720870750:call_154864', 1802)
```


## F2. GET /api/tunnel/status (sem auth) + /api/settings (sem auth)

```
tunnel/status: 401
{"error":"Unauthorized"}
settings: 401
{"error":"Unauthorized"}
```


## F3. journalctl -k desde boot: OOM/SIGKILL/memory + audit de kill

```
===KERNEL-DESDE-BOOT===
===KERNEL-0225-JANELA-AMPLA===
out 07 02:20:52 Tijolao kernel: usb 1-3: USB disconnect, device number 2
out 07 02:20:52 Tijolao kernel: [UFW BLOCK] IN=wlp2s0 OUT= MAC= SRC=2804:07f0:aa14:2f67:78ac:d4b4:5f9b:7d85 DST=ff02:0000:0000:0000:0000:0000:0000:000c LEN=655 TC=0 HOPLIMIT=1 FLOWLBL=860594 PROTO=UDP SPT=60635 DPT=3702 LEN=615 
out 07 02:20:52 Tijolao kernel: [UFW BLOCK] IN=wlp2s0 OUT= MAC= SRC=2804:07f0:aa14:2f67:c9b9:0560:e957:b476 DST=ff02:0000:0000:0000:0000:0000:0000:000c LEN=655 TC=0 HOPLIMIT=1 FLOWLBL=218336 PROTO=UDP SPT=34234 DPT=3702 LEN=615 
out 07 02:20:52 Tijolao kernel: [UFW BLOCK] IN=wlp2s0 OUT= MAC= SRC=192.168.15.186 DST=239.255.255.250 LEN=635 TOS=0x00 PREC=0x00 TTL=1 ID=59679 DF PROTO=UDP SPT=53242 DPT=3702 LEN=615 
out 07 02:20:52 Tijolao kernel: [UFW BLOCK] IN=wlp2s0 OUT= MAC= SRC=fe80:0000:0000:0000:f4d1:0aa3:c33d:4620 DST=ff02:0000:0000:0000:0000:0000:0000:000c LEN=655 TC=0 HOPLIMIT=1 FLOWLBL=329832 PROTO=UDP SPT=60940 DPT=3702 LEN=615 
out 07 02:20:52 Tijolao kernel: [UFW BLOCK] IN=docker0 OUT= MAC= SRC=172.17.0.1 DST=239.255.255.250 LEN=635 TOS=0x00 PREC=0x00 TTL=1 ID=34501 DF PROTO=UDP SPT=41888 DPT=3702 LEN=615 
out 07 02:20:52 Tijolao kernel: [UFW BLOCK] IN=wlp2s0 OUT= MAC=a8:6b:ad:dd:ab:9b:a8:6b:ad:dd:ab:9b:86:dd SRC=2804:07f0:aa14:2f67:78ac:d4b4:5f9b:7d85 DST=ff02:0000:0000:0000:0000:0000:0000:000c LEN=655 TC=0 HOPLIMIT=1 FLOWLBL=860594 PROTO=UDP SPT=60635 DPT=3702 LEN=615 
out 07 02:22:02 Tijolao kernel: usb 1-3: new full-speed USB device number 7 using xhci_hcd
out 07 02:22:02 Tijolao kernel: usb 1-3: New USB device found, idVendor=1ea7, idProduct=0064, bcdDevice= 2.00
out 07 02:22:02 Tijolao kernel: usb 1-3: New USB device strings: Mfr=0, Product=1, SerialNumber=0
out 07 02:22:02 Tijolao kernel: usb 1-3: Product: 2.4G Mouse
out 07 02:22:02 Tijolao kernel: input: 2.4G Mouse as /devices/pci0000:00/0000:00:14.0/usb1/1-3/1-3:1.0/0003:1EA7:0064.0004/input/input25
out 07 02:22:02 Tijolao kernel: input: 2.4G Mouse as /devices/pci0000:00/0000:00:14.0/usb1/1-3/1-3:1.0/0003:1EA7:0064.0004/input/input26
out 07 02:22:02 Tijolao kernel: hid-generic 0003:1EA7:0064.0004: input,hiddev0,hidraw0: USB HID v1.10 Mouse [2.4G Mouse] on usb-0000:00:14.0-3/input0
out 07 02:22:02 Tijolao kernel: [UFW BLOCK] IN=wlp2s0 OUT= MAC= SRC=2804:07f0:aa14:2f67:78ac:d4b4:5f9b:7d85 DST=ff02:0000:0000:0000:0000:0000:0000:000c LEN=655 TC=0 HOPLIMIT=1 FLOWLBL=870580 PROTO=UDP SPT=54261 DPT=3702 LEN=615 
out 07 02:22:02 Tijolao kernel: [UFW BLOCK] IN=wlp2s0 OUT= MAC= SRC=2804:07f0:aa14:2f67:c9b9:0560:e957:b476 DST=ff02:0000:0000:0000:0000:0000:0000:000c LEN=655 TC=0 HOPLIMIT=1 FLOWLBL=219132 PROTO=UDP SPT=39400 DPT=3702 LEN=615 
out 07 02:22:02 Tijolao kernel: [UFW BLOCK] IN=wlp2s0 OUT= MAC= SRC=192.168.15.186 DST=239.255.255.250 LEN=635 TOS=0x00 PREC=0x00 TTL=1 ID=64990 DF PROTO=UDP SPT=42550 DPT=3702 LEN=615 
out 07 02:22:02 Tijolao kernel: [UFW BLOCK] IN=wlp2s0 OUT= MAC= SRC=fe80:0000:0000:0000:f4d1:0aa3:c33d:4620 DST=ff02:0000:0000:0000:0000:0000:0000:000c LEN=655 TC=0 HOPLIMIT=1 FLOWLBL=562270 PROTO=UDP SPT=36821 DPT=3702 LEN=615 
out 07 02:22:02 Tijolao kernel: [UFW BLOCK] IN=docker0 OUT= MAC= SRC=172.17.0.1 DST=239.255.255.250 LEN=635 TOS=0x00 PREC=0x00 TTL=1 ID=33296 DF PROTO=UDP SPT=33803 DPT=3702 LEN=615 
out 07 02:34:02 Tijolao kernel: pcieport 0000:00:1c.0: Intel SPT PCH root port ACS workaround enabled
===USER-JOURNAL-SEM-UNIDADE-NA-JANELA===
out 07 02:25:36 Tijolao dbus-daemon[1147]: [session uid=1000 pid=1147] Activating via systemd: service name='org.gnome.Terminal' unit='gnome-terminal-server.service' requested by ':1.102' (uid=1000 pid=21596 comm="/usr/bin/gnome-terminal.real" label="unconfined")
out 07 02:25:36 Tijolao systemd[1060]: Created slice app-org.gnome.Terminal.slice - Slice /app/org.gnome.Terminal.
out 07 02:25:36 Tijolao systemd[1060]: Starting gnome-terminal-server.service - GNOME Terminal Server...
out 07 02:25:36 Tijolao dbus-daemon[1147]: [session uid=1000 pid=1147] Successfully activated service 'org.gnome.Terminal'
out 07 02:25:36 Tijolao systemd[1060]: Started gnome-terminal-server.service - GNOME Terminal Server.
out 07 02:25:36 Tijolao systemd[1060]: Started vte-spawn-d9e7143d-4931-40b1-9dda-9aaea1f2812f.scope - VTE child process 21612 launched by gnome-terminal-server process 21600.
out 07 02:25:43 Tijolao systemd[1060]: Started vte-spawn-ac047141-031a-4b21-bffa-f641ad76c67a.scope - VTE child process 21938 launched by gnome-terminal-server process 21600.
out 07 02:25:57 Tijolao node[22400]: ⚠ Network-exposed: reachable at http://192.168.15.186:20128 (bound 0.0.0.0). Use --host 127.0.0.1 for local-only.
out 07 02:25:57 Tijolao node[22400]: Server: http://localhost:20128
out 07 02:25:57 Tijolao node[22467]: ▲ Next.js 16.3.4
out 07 02:25:57 Tijolao node[22467]: - Local:         http://localhost:20128
out 07 02:25:57 Tijolao node[22467]: - Network:       http://0.0.0.0:20128
out 07 02:25:57 Tijolao node[22467]: ✓ Ready in 0ms
out 07 02:25:57 Tijolao node[22467]: ✓ Running next.config took 2ms
out 07 02:25:57 Tijolao node[22400]: 💡 Router is now running in system tray. Close this terminal if you want.
===SYSTEM-JOURNAL-NA-JANELA===
out 07 02:25:49 Tijolao systemd[1060]: 9router.service: Main process exited, code=killed, status=9/KILL
out 07 02:26:27 Tijolao node[22467]: [Tunnel] killed existing cloudflared
out 07 02:26:37 Tijolao earlyoom[663]: mem avail:  3441 of  7815 MiB (44.03%), swap free: 3907 of 3907 MiB (100.00%)
out 07 02:29:02 Tijolao systemd[1060]: 9router.service: Main process exited, code=killed, status=9/KILL
out 07 02:29:20 Tijolao node[23905]: [Tunnel] killed existing cloudflared
```


## F4. docker-compose.tijolao.yml (parte final)

```
:
      hermes-agent:
        condition: service_healthy
    network_mode: host
    env_file:
      - /home/dr/.local/secrets/tijolao.env
    environment:
      HOST: 127.0.0.1             # loopback: dispensa senha de sessao
      PORT: "3000"
      NODE_ENV: production
      HERMES_HOME: /home/dr/.hermes
      HERMES_WORKSPACE_DIR: /home/dr/src
      HERMES_API_URL: http://127.0.0.1:8642
      HERMES_DASHBOARD_URL: http://127.0.0.1:9119
      HERMES_API_TOKEN: ${API_SERVER_KEY:-}
      # Senha de sessao da interface: DESLIGADA de proposito.
      # Com HOST=127.0.0.1 nada fora do notebook alcanca a porta 3000, e exigir
      # senha a cada aba so atrapalha. Se um dia voce publicar a 3000 (Tailscale,
      # cloudflared, LAN), descomente a linha abaixo ANTES de publicar:
      # HERMES_PASSWORD: ${HERMES_DASHBOARD_PASSWORD:-}
      HERMES_UID: "1000"
      HERMES_GID: "1000"
      # --- Swarm: o workspace e CLIENTE tmux; o SERVIDOR roda no host ---
      # Assim `tmux new-session` despacha o worker como processo do HOST, onde
      # existe o wrapper `hermes` e o CLI do docker. O socket do docker continua
      # fora do container (decisao de seguranca do COMO-USAR.md).
      #
      # O codigo usa homedir() para achar ~/.local/bin/<wrapper> e o cwd do
      # worker. `HOME:` aqui nao adianta — o gosu do entrypoint o sobrescreve
      # com o passwd. HERMES_HOST_HOME faz o entrypoint reapontar o passwd.
      HERMES_HOST_HOME: /home/dr
      # resolveTmuxBin() tenta /opt/homebrew/bin/tmux e /usr/local/bin/tmux SEM
      # checar existencia (atalho de macOS). Em Linux isso devolve um caminho
      # inexistente. TMUX_BIN e o primeiro candidato e evita o problema.
      TMUX_BIN: /usr/bin/tmux
      HERMES_CLI_BIN: /home/dr/.local/bin/hermes
    volumes:
      - /home/dr/.hermes:/home/dr/.hermes
      - /home/dr/src:/home/dr/src
      - /home/dr/.claude/skills:/home/dr/.claude/skills:ro
      # socket do servidor tmux do host (cliente 3.3a x servidor 3.4: testado)
      - /tmp/tmux-1000:/tmp/tmux-1000
      # wrappers dos especialistas; o codigo confere existsSync antes de usar
      - /home/dr/.local/bin:/home/dr/.local/bin:ro
      # A roster do Swarm e lida de <cwd>/swarm.yaml, e o Dockerfile a assa na
      # imagem. Sem este mount, mexer na frota exigiria rebuild a cada ajuste.
      - /home/dr/src/tijolao-ai/hermes-stack/swarm.yaml:/app/swarm.yaml:ro
    healthcheck:
      test: ["CMD-SHELL", "curl -fsS http://127.0.0.1:3000/ >/dev/null || exit 1"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 30s

```


## F5. journal: 6 POSTs flash com desfecho; DONE por modelo

```
===TODOS-POSTs-FLASH===
80:out 07 02:30:17 Tijolao node[23905]: [02:30:17] 🟤 ▶ POST nvidia/z-ai/glm-5.3-flash → nvidia/z-ai/glm-5.3-flash · FMT: openai→openai · STREAM · 2 MSG · 18 TOOL · THINK:auto · ACC:NVIDIABuild-Autogen-29
83:out 07 02:33:47 Tijolao node[23905]: [02:33:47] 🟣 ▶ POST nvidia/z-ai/glm-5.3-flash → nvidia/z-ai/glm-5.3-flash · FMT: openai→openai · STREAM · 4 MSG · 18 TOOL · THINK:auto · ACC:NVIDIABuild-Autogen-29
85:out 07 02:36:11 Tijolao node[23905]: [02:36:11] 🟣 ▶ POST nvidia/z-ai/glm-5.3-flash → nvidia/z-ai/glm-5.3-flash · FMT: openai→openai · STREAM · 8 MSG · 18 TOOL · THINK:auto · ACC:NVIDIABuild-Autogen-29
86:out 07 02:36:14 Tijolao node[23905]: [02:36:14] 🟣 ▶ POST nvidia/z-ai/glm-5.3-flash → nvidia/z-ai/glm-5.3-flash · FMT: openai→openai · STREAM · 10 MSG · 18 TOOL · THINK:auto · ACC:NVIDIABuild-Autogen-29
87:out 07 02:40:20 Tijolao node[23905]: [02:40:20] 🟣 ✗ ERROR 502 · nvidia/z-ai/glm-5.3-flash · 249006ms
90:out 07 02:40:20 Tijolao node[23905]: [02:40:20] ⚠️  [AUTH] NVIDIABuild-Autogen-29 locked modelLock_z-ai/glm-5.3-flash for 30s [502]
93:out 07 02:40:20 Tijolao node[23905]: [02:40:20] ⚠️  [AUTH] nvidia | all 1 accounts locked for z-ai/glm-5.3-flash (reset after 30s) | lastError=[502]: fetch connect timeout
94:out 07 02:40:20 Tijolao node[23905]: [02:40:20] ⚠️  [CHAT] [nvidia/z-ai/glm-5.3-flash] [502]: fetch connect timeout (reset after 30s)
95:out 07 02:40:23 Tijolao node[23905]: [02:40:23] 🟣 ✗ ERROR 502 · nvidia/z-ai/glm-5.3-flash · 249006ms
98:out 07 02:40:23 Tijolao node[23905]: [02:40:23] ⚠️  [AUTH] NVIDIABuild-Autogen-29 locked modelLock_z-ai/glm-5.3-flash for 30s [502]
101:out 07 02:40:23 Tijolao node[23905]: [02:40:23] ⚠️  [AUTH] nvidia | all 1 accounts locked for z-ai/glm-5.3-flash (reset after 30s) | lastError=[502]: fetch connect timeout
102:out 07 02:40:23 Tijolao node[23905]: [02:40:23] ⚠️  [CHAT] [nvidia/z-ai/glm-5.3-flash] [502]: fetch connect timeout (reset after 30s)
103:out 07 02:40:53 Tijolao node[23905]: [02:40:53] 🟣 ▶ POST nvidia/z-ai/glm-5.3-flash → nvidia/z-ai/glm-5.3-flash · FMT: openai→openai · STREAM · 10 MSG · 18 TOOL · THINK:auto · ACC:NVIDIABuild-Autogen-29
104:out 07 02:45:02 Tijolao node[23905]: [02:45:02] 🟣 ✗ ERROR 502 · nvidia/z-ai/glm-5.3-flash · 249008ms
107:out 07 02:45:02 Tijolao node[23905]: [02:45:02] ⚠️  [AUTH] NVIDIABuild-Autogen-29 locked modelLock_z-ai/glm-5.3-flash for 30s [502]
110:out 07 02:45:02 Tijolao node[23905]: [02:45:02] ⚠️  [AUTH] nvidia | all 1 accounts locked for z-ai/glm-5.3-flash (reset after 30s) | lastError=[502]: fetch connect timeout
111:out 07 02:45:02 Tijolao node[23905]: [02:45:02] ⚠️  [CHAT] [nvidia/z-ai/glm-5.3-flash] [502]: fetch connect timeout (reset after 30s)
128:out 07 02:47:39 Tijolao node[23905]: [02:47:39] 🟤 ▶ POST nvidia/z-ai/glm-5.3-flash → nvidia/z-ai/glm-5.3-flash · FMT: openai→openai · STREAM · 1 MSG · THINK:auto · ACC:NVIDIABuild-Autogen-29
140:out 07 02:51:48 Tijolao node[23905]: [02:51:48] 🟤 ✗ ERROR 502 · nvidia/z-ai/glm-5.3-flash · 249006ms
143:out 07 02:51:48 Tijolao node[23905]: [02:51:48] ⚠️  [AUTH] NVIDIABuild-Autogen-29 locked modelLock_z-ai/glm-5.3-flash for 30s [502]
146:out 07 02:51:48 Tijolao node[23905]: [02:51:48] ⚠️  [AUTH] nvidia | all 1 accounts locked for z-ai/glm-5.3-flash (reset after 30s) | lastError=[502]: fetch connect timeout
147:out 07 02:51:48 Tijolao node[23905]: [02:51:48] ⚠️  [CHAT] [nvidia/z-ai/glm-5.3-flash] [502]: fetch connect timeout (reset after 30s)
===DONE-POR-MODELO===
DONE z-ai/glm-5.3 : 0
DONE z-ai/glm-5.3-flash: 0
DONE claude-opus-5-5: 0
DONE laguna: 0
DONE gemini: 0
===POST-SEMFALHA===
POSTs (todos): 76 ; DONEs: 67 ; ERRORs: 4
```


## F6. servico: primeira ativacao hoje + versoes anteriores no journal

```
out 07 01:26:43 Tijolao systemd[1060]: Started 9router.service - 9Router local AI gateway.
out 07 01:26:49 Tijolao node[1142]: 🚀 9router v0.5.95
out 07 02:25:54 Tijolao systemd[1060]: Started 9router.service - 9Router local AI gateway.
out 07 02:25:57 Tijolao node[22400]: 🚀 9router v0.5.95
out 07 02:29:07 Tijolao systemd[1060]: Started 9router.service - 9Router local AI gateway.
out 07 02:29:11 Tijolao node[23840]: 🚀 9router v0.5.95
===JOURNAL-COMPLETO-HOJE-32D===
3
```