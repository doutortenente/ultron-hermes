# Auditoria B - parcial 7


## H1. DB: valores das settings de tunnel/tailscale/mitm + kv das conexoes + requestDetails glm 48h

```
== settings (valores nao-segredo) ==
  tunnelEnabled = True
  tunnelUrl = https://establishment-whatever-presenting-easter.trycloudflare.com
  tailscaleEnabled = True
  tailscaleUrl = https://tijolao.tail9e88c5.ts.net
  tunnelDashboardAccess = True
  mitmEnabled = False
  ponytailEnabled = False
  ponytailLevel = lite
  outboundProxyEnabled = False
  rtkEnabled = False
== kv: nvidia / cc / cx / ag / ps (conteudo) ==
  [nvidia] -> ["z-ai/glm-5.2","minimaxai/minimax-m2.7","minimaxai/minimax-m3","moonshotai/kimi-k2.6","deepseek-ai/deepseek-v4-pro","deepseek-ai/deepseek-v4-flash"]
  [cc] -> ["claude-fable-5","claude-fable-5-1","claude-opus-5","claude-sonnet-5"]
  [cx] -> ["gpt-5.6-terra-review","gpt-5.6-luna-review","gpt-5.4-review","gpt-5.4-mini","gpt-5.4-mini-review","gpt-5.3-codex-spark-review","gpt-5.4","gpt-5.5-review","gpt-5.6-sol-review","gpt-5.6-sol","gpt-5.3-codex-spark","gpt-6-astra"]
  [ag] -> ["gemini-3.6-flash-low","gemini-3.7-flash-low","gemini-3.7-flash-high","gemini-3.6-flash-medium","gemini-3.5-flash-high","gemini-3-flash-agent","gemini-3.5-flash-low","gemini-3.5-flash-extra-low","claude-sonnet-4-6","gemini-3.8-flash-medium","gemini-3.8-flash-low","gemini-3.7-flash-medium","gemini-3.6-flash-high","gemini-3-flash","gpt-oss-120b-medium","gemini-3.1-pro-low","gemini-3.8-flash-high"]
  [cf] -> ["@cf/meta/llama-3.1-8b-instruct-awq","@cf/moonshotai/kimi-k2.6","@cf/moonshotai/kimi-k2.5","@cf/qwen/qwq-32b","@cf/qwen/qwen2.5-coder-32b-instruct","@cf/meta/llama-3.1-8b-instruct-fp8-fast","@cf/mistralai/mistral-small-3.1-24b-instruct","@cf/meta/llama-3.2-3b-instruct","@cf/meta/llama-3.2-1b-instruct","@cf/meta/llama-3.1-70b-instruct-fp8-fast"]
== kv: algum glm-5.3-flash ==
(fim kv flash)
== requestDetails: glm-5.3-flash (todas) ==
   ('2026-10-07T06:27:48.319Z', 'z-ai/glm-5.3-flash', 'success')
   ('2026-10-07T05:51:48.752Z', 'z-ai/glm-5.3-flash', 'error')
   ('2026-10-07T05:45:02.765Z', 'z-ai/glm-5.3-flash', 'error')
   ('2026-10-07T05:40:23.689Z', 'z-ai/glm-5.3-flash', 'error')
   ('2026-10-07T05:40:20.963Z', 'z-ai/glm-5.3-flash', 'error')
   ('2026-10-07T05:36:11.603Z', 'z-ai/glm-5.3-flash', 'success')
   ('2026-10-07T05:31:03.151Z', 'z-ai/glm-5.3-flash', 'success')
   ('2026-10-04T22:54:17.283Z', 'z-ai/glm-5.3-flash', 'error')
   ('2026-10-04T22:34:21.486Z', 'z-ai/glm-5.3-flash', 'error')
   ('2026-10-04T22:29:42.426Z', 'z-ai/glm-5.3-flash', 'error')
== requestDetails: z-ai/glm-5.3 (base) ultimas 5 ==
   ('2026-10-07T06:52:22.832Z', 'z-ai/glm-5.3', 'success')
   ('2026-10-07T06:52:20.022Z', 'z-ai/glm-5.3', 'success')
   ('2026-10-07T06:52:14.956Z', 'z-ai/glm-5.3', 'success')
   ('2026-10-07T06:52:01.661Z', 'z-ai/glm-5.3', 'success')
   ('2026-10-07T06:51:21.031Z', 'z-ai/glm-5.3', 'success')
== usageHistory: status != ok nas ultimas 48h ==
   ('2026-08-24T12:42:40.698Z', 'mistral', 'mistral-embed', 'success')
   ('2026-08-24T12:36:22.245Z', 'mistral', 'mistral-embed', 'success')
```


## H2. journal 9router: contagem final desde boot ate agora

```
linhas: 667 ; agora: 2026-10-07 03:53:30 -03
ERROR 502: 4
fetch connect timeout: 20
locked modelLock: 4
accounts locked: 4
POST flash: 7
POST glm-5.3-base: 258
POST opus: 11
POST laguna: 2
DONE: 266
tunnel spawns: 2
===EVENTOS-DE-ERRO-502-DISTINTOS===
out 07 02:40:20 Tijolao node[23905]: [02:40:20] 🟣 ✗ ERROR 502 · nvidia/z-ai/glm-5.3-flash · 249006ms
out 07 02:40:23 Tijolao node[23905]: [02:40:23] 🟣 ✗ ERROR 502 · nvidia/z-ai/glm-5.3-flash · 249006ms
out 07 02:45:02 Tijolao node[23905]: [02:45:02] 🟣 ✗ ERROR 502 · nvidia/z-ai/glm-5.3-flash · 249008ms
out 07 02:51:48 Tijolao node[23905]: [02:51:48] 🟤 ✗ ERROR 502 · nvidia/z-ai/glm-5.3-flash · 249006ms
===ULTIMAS-8-LINHAS===
out 07 03:51:23 Tijolao node[23905]: [03:51:23] 🟤 ▶ POST nvidia/z-ai/glm-5.3 → nvidia/z-ai/glm-5.3 · FMT: openai→openai · STREAM · 132 MSG · 15 TOOL · THINK:max · ACC:NVIDIABuild-Autogen-29
out 07 03:52:01 Tijolao node[23905]: [03:52:01] 🟤 📊 DONE 38183ms · TTFT 32219ms · IN 135820 (CACHE ↻135296) · OUT 257
out 07 03:52:03 Tijolao node[23905]: [03:52:03] 🟤 ▶ POST nvidia/z-ai/glm-5.3 → nvidia/z-ai/glm-5.3 · FMT: openai→openai · STREAM · 134 MSG · 15 TOOL · THINK:max · ACC:NVIDIABuild-Autogen-29
out 07 03:52:14 Tijolao node[23905]: [03:52:14] 🟤 📊 DONE 11637ms · TTFT 2507ms · IN 136428 (CACHE ↻136000) · OUT 232
out 07 03:52:15 Tijolao node[23905]: [03:52:15] 🟤 ▶ POST nvidia/z-ai/glm-5.3 → nvidia/z-ai/glm-5.3 · FMT: openai→openai · STREAM · 136 MSG · 15 TOOL · THINK:max · ACC:NVIDIABuild-Autogen-29
out 07 03:52:20 Tijolao node[23905]: [03:52:20] 🟤 📊 DONE 4978ms · TTFT 1511ms · IN 138844 (CACHE ↻136576) · OUT 236
out 07 03:52:20 Tijolao node[23905]: [03:52:20] 🟤 ▶ POST nvidia/z-ai/glm-5.3 → nvidia/z-ai/glm-5.3 · FMT: openai→openai · STREAM · 138 MSG · 15 TOOL · THINK:max · ACC:NVIDIABuild-Autogen-29
out 07 03:53:29 Tijolao node[23905]: [03:53:29] 🟤 📊 DONE 573256ms · TTFT 1513ms · IN 95543 (CACHE ↻88768) · OUT 13242
===FLASH-MEU-TESTE-0620UTC===
out 07 03:29:33 Tijolao node[23905]: [03:29:33] 🟤 ▶ POST nvidia/z-ai/glm-5.3 → nvidia/z-ai/glm-5.3 · FMT: openai→openai · STREAM · 119 MSG · 15 TOOL · THINK:max · ACC:NVIDIABuild-Autogen-29
out 07 03:29:36 Tijolao node[23905]: [03:29:36] 🟤 📊 DONE 2992ms · TTFT 948ms · IN 74962 (CACHE ↻74752) · OUT 119
out 07 03:29:36 Tijolao node[23905]: [03:29:36] 🟤 ▶ POST nvidia/z-ai/glm-5.3 → nvidia/z-ai/glm-5.3 · FMT: openai→openai · STREAM · 121 MSG · 15 TOOL · THINK:max · ACC:NVIDIABuild-Autogen-29
out 07 03:29:44 Tijolao node[23905]: [03:29:44] 🟤 📊 DONE 334884ms · TTFT 939ms · IN 47733 (CACHE ↻46720) · OUT 10529
out 07 03:29:44 Tijolao node[23905]: [03:29:44] 🟤 📊 DONE 7992ms · TTFT 935ms · IN 75303 (CACHE ↻75008) · OUT 293
out 07 03:29:45 Tijolao node[23905]: [03:29:45] 🟤 ▶ POST nvidia/z-ai/glm-5.3 → nvidia/z-ai/glm-5.3 · FMT: openai→openai · STREAM · 123 MSG · 15 TOOL · THINK:max · ACC:NVIDIABuild-Autogen-29
out 07 03:29:55 Tijolao node[23905]: [03:29:55] 🟤 📊 DONE 10531ms · TTFT 1721ms · IN 76239 (CACHE ↻75520) · OUT 421
out 07 03:29:56 Tijolao node[23905]: [03:29:56] 🟤 ▶ POST nvidia/z-ai/glm-5.3 → nvidia/z-ai/glm-5.3 · FMT: openai→openai · STREAM · 125 MSG · 15 TOOL · THINK:max · ACC:NVIDIABuild-Autogen-29
```


## H3. processos com fds em ~/.9router ou ~/.local/share/9router

```
pid 23840: <nenhum fd aberto nessas arvores>
pid 23905: /home/dr/.local/share/9router/db/data.sqlite
/home/dr/.local/share/9router/db/data.sqlite-shm
/home/dr/.local/share/9router/db/data.sqlite-wal
pid 23921: <nenhum fd aberto nessas arvores>
pid 24062: <nenhum fd aberto nessas arvores>
===LSOF-9ROUTER===
```