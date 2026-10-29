# Auditoria B (IA) - evidencia parcial


## A1. unit 9router.service + systemctl show + data

```
===UNIT-FILE===
[Unit]
Description=9Router local AI gateway
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/home/dr/.local/share/nvm/versions/node/v24.16.0/bin/node /home/dr/.local/lib/node_modules/9router/cli.js --no-browser --skip-update --log
WorkingDirectory=/home/dr/.local/share/9router
Environment="HOME=/home/dr"
Environment="DATA_DIR=/home/dr/.local/share/9router"
Environment="PATH=/home/dr/.local/share/nvm/versions/node/v24.16.0/bin:/home/dr/.local/bin:/usr/local/bin:/usr/bin:/bin"
Restart=on-failure
RestartSec=5
KillMode=control-group
TimeoutStopSec=20

[Install]
WantedBy=default.target
===SHOW===
MainPID=23840
NRestarts=2
ExecMainStartTimestamp=Wed 2026-10-07 02:29:07 -03
ExecStart={ path=/home/dr/.local/share/nvm/versions/node/v24.16.0/bin/node ; argv[]=/home/dr/.local/share/nvm/versions/node/v24.16.0/bin/node /home/dr/.local/lib/node_modules/9router/cli.js --no-browser --skip-update --log ; ignore_errors=no ; start_time=[Wed 2026-10-07 02:29:07 -03] ; stop_time=[n/a] ; pid=23840 ; code=(null) ; status=0/0 }
Environment=HOME=/home/dr DATA_DIR=/home/dr/.local/share/9router PATH=/home/dr/.local/share/nvm/versions/node/v24.16.0/bin:/home/dr/.local/bin:/usr/local/bin:/usr/bin:/bin
WorkingDirectory=/home/dr/.local/share/9router
ActiveState=active
SubState=running
===NOW===
2026-10-07 03:06:56 -03
2026-10-07 01:26:31
```


## A2. caminhos citados + diretorios de dados

```
===PATHS===
EXISTS: /home/dr/.local/share/nvm/versions/node/v24.16.0/bin/node
EXISTS: /home/dr/.local/lib/node_modules/9router/cli.js
EXISTS: /home/dr/.local/share/9router
EXISTS: /home/dr/.9router
EXISTS: /home/dr/.cache/node-systray
MISSING: /home/dr/projetos
EXISTS: /home/dr/src/tijolao-ai/hermes-stack/docker-compose.tijolao.yml
===DU===
75M	/home/dr/.local/share/9router
31M	/home/dr/.9router
===LS-SHARE-9ROUTER===
total 888
drwxrwxr-x  9 dr dr   4096 out  7 02:26 .
drwxrwxr-x 40 dr dr   4096 out  7 02:25 ..
drwxrwxr-x  2 dr dr   4096 ago 22 19:02 auth
drwxrwxr-x  2 dr dr   4096 set  7 19:14 bin
drwxrwxr-x  3 dr dr   4096 out  2 16:59 db
-rw-------  1 dr dr     64 ago 22 19:02 jwt-secret
drwxrwxr-x  3 dr dr   4096 ago 22 19:02 logs
-rw-------  1 dr dr     64 ago 22 19:02 machine-id
-rw-rw-r--  1 dr dr 282986 out  7 02:26 model-catalog.json
-rw-rw-r--  1 dr dr 576484 out  7 02:26 model-catalog-raw.json
drwxrwxr-x  4 dr dr   4096 ago 22 19:02 runtime
drwxrwxr-x  3 dr dr   4096 set  7 20:58 tailscale
drwxrwxr-x  2 dr dr   4096 out  7 02:29 tunnel
===LS-DOT-9ROUTER===
total 32
drwxrwxr-x  6 dr dr 4096 set 23 23:31 .
drwxr-x--- 24 dr dr 4096 out  7 02:27 ..
drwxrwxr-x  2 dr dr 4096 set 23 23:31 auth
drwxrwxr-x  3 dr dr 4096 out  7 02:25 db
-rw-------  1 dr dr   64 set 23 23:31 jwt-secret
drwxrwxr-x  3 dr dr 4096 set 23 23:31 logs
-rw-------  1 dr dr   64 set 23 23:31 machine-id
drwxrwxr-x  4 dr dr 4096 set 23 23:34 runtime
```


## A3. /proc do processo 9router (cwd, environ, filhos)

```
MainPID=23840
cwd=/home/dr/.local/share/9router
===ENVIRON-VARS-que-conteem-DATA-DIR-HOME-PATH-NINEROUTER===
HOME=/home/dr
PATH=/home/dr/.local/share/nvm/versions/node/v24.16.0/bin:/home/dr/.local/bin:/usr/local/bin:/usr/bin:/bin
XDG_DATA_DIRS=/usr/share/cinnamon:/home/dr/.local/share/flatpak/exports/share:/var/lib/flatpak/exports/share:/usr/local/share:/usr/share
XDG_RUNTIME_DIR=/run/user/1000
QTWEBENGINE_DICTIONARIES_PATH=/usr/share/hunspell-bdic/
XDG_CONFIG_DIRS=/etc/xdg/xdg-cinnamon:/etc/xdg
XDG_GREETER_DATA_DIR=/var/lib/lightdm-data/dr
XDG_SEAT_PATH=/org/freedesktop/DisplayManager/Seat0
XDG_SESSION_PATH=/org/freedesktop/DisplayManager/Session0
DATA_DIR=/home/dr/.local/share/9router
===CHILDREN===
  23905   23840 qua out  7 02:29:10 2026       37:46 next-server (v16.3.4)
  23921   23840 qua out  7 02:29:10 2026       37:46 /home/dr/.cache/node-systray/2.1.4/tray_linux_release
===CHILD-CWD===
child 23905 cwd: /home/dr/.local/lib/node_modules/9router/app
child 23921 cwd: /home/dr/.local/share/9router
===CLOUDFLARED-CONFIG===
```


## A4. docker ps + inspect hermes-agent/hermes-workspace

```
===PS===
hermes-workspace | hermes-workspace:tijolao | Up 2 hours (healthy)
hermes-agent | nousresearch/hermes-agent:latest | Up 2 hours (healthy)
===INSPECT-hermes-agent===
Image=nousresearch/hermes-agent:latest
Created=2026-10-04T19:34:23.846192112Z
RestartPolicy=unless-stopped
NetworkMode=host
{"com.docker.compose.config-hash":"4812d7fa95ae100f287770b3b35f5590398b82f68fdfcab418f14d9452318f0b","com.docker.compose.container-number":"1","com.docker.compose.depends_on":"","com.docker.compose.image":"sha256:89673e40882bdf461665f66ecfe6ce4964964f1055b4f03e3e870a72061e8ab6","com.docker.compose.oneoff":"False","com.docker.compose.project":"hermes","com.docker.compose.project.config_files":"/home/dr/src/tijolao-ai/hermes-stack/docker-compose.tijolao.yml","com.docker.compose.project.working_dir":"/home/dr/src/tijolao-ai/hermes-stack","com.docker.compose.replace":"hermes-agent","com.docker.compose.service":"hermes-agent","com.docker.compose.version":"2.40.3","org.opencontainers.image.revision":"cdf4c765213d7f4f7562f642e2b2df00d42c8ffd"}
[{"Type":"bind","Source":"/home/dr/.claude/skills","Destination":"/home/dr/.claude/skills","Mode":"ro","RW":false,"Propagation":"rprivate"},{"Type":"bind","Source":"/home/dr/.hermes","Destination":"/home/dr/.hermes","Mode":"rw","RW":true,"Propagation":"rprivate"},{"Type":"bind","Source":"/home/dr/.local/secrets","Destination":"/home/dr/.local/secrets","Mode":"ro","RW":false,"Propagation":"rprivate"},{"Type":"bind","Source":"/home/dr/src","Destination":"/home/dr/src","Mode":"rw","RW":true,"Propagation":"rprivate"},{"Type":"bind","Source":"/home/dr/vaults/celebro","Destination":"/home/dr/vaults/celebro","Mode":"rw","RW":true,"Propagation":"rprivate"},{"Type":"volume","Name":"197f05151a5a8ff48c3202e8cb6966d1f21eda3a3dfffde5f5132f122943db8a","Source":"/var/lib/docker/volumes/197f05151a5a8ff48c3202e8cb6966d1f21eda3a3dfffde5f5132f122943db8a/_data","Destination":"/opt/data","Driver":"local","Mode":"z","RW":true,"Propagation":""}]
===INSPECT-hermes-workspace===
Image=hermes-workspace:tijolao
Created=2026-10-04T19:34:27.463330987Z
RestartPolicy=unless-stopped
NetworkMode=host
{"com.docker.compose.config-hash":"fc8fc36f47e1a560ff0a5699a8a3e3a172aada9c05aae64a400f0223f749a5a2","com.docker.compose.container-number":"1","com.docker.compose.depends_on":"hermes-agent:service_healthy:false","com.docker.compose.image":"sha256:c5a3080e124fcf97413979bca93e2a79f89e42f938613005e97cfcd8a78ef677","com.docker.compose.oneoff":"False","com.docker.compose.project":"hermes","com.docker.compose.project.config_files":"/home/dr/src/tijolao-ai/hermes-stack/docker-compose.tijolao.yml","com.docker.compose.project.working_dir":"/home/dr/src/tijolao-ai/hermes-stack","com.docker.compose.replace":"hermes-workspace","com.docker.compose.service":"hermes-workspace","com.docker.compose.version":"2.40.3"}
[{"Type":"bind","Source":"/home/dr/.hermes","Destination":"/home/dr/.hermes","Mode":"rw","RW":true,"Propagation":"rprivate"},{"Type":"bind","Source":"/home/dr/.local/bin","Destination":"/home/dr/.local/bin","Mode":"ro","RW":false,"Propagation":"rprivate"},{"Type":"bind","Source":"/home/dr/src","Destination":"/home/dr/src","Mode":"rw","RW":true,"Propagation":"rprivate"},{"Type":"bind","Source":"/tmp/tmux-1000","Destination":"/tmp/tmux-1000","Mode":"rw","RW":true,"Propagation":"rprivate"},{"Type":"bind","Source":"/home/dr/src/tijolao-ai/hermes-stack/swarm.yaml","Destination":"/app/swarm.yaml","Mode":"ro","RW":false,"Propagation":"rprivate"},{"Type":"bind","Source":"/home/dr/.claude/skills","Destination":"/home/dr/.claude/skills","Mode":"ro","RW":false,"Propagation":"rprivate"}]
```


## A5. tailscale serve/funnel + ollama + cloudflared

```
===TS-SERVE===

# Funnel on:
#     - https://tijolao.tail9e88c5.ts.net

https://tijolao.tail9e88c5.ts.net:10000 (tailnet only)
|-- / proxy http://127.0.0.1:3000

https://tijolao.tail9e88c5.ts.net (Funnel on)
|-- / proxy http://127.0.0.1:20128

===TS-FUNNEL===

# Funnel on:
#     - https://tijolao.tail9e88c5.ts.net

https://tijolao.tail9e88c5.ts.net:10000 (tailnet only)
|-- / proxy http://127.0.0.1:3000

https://tijolao.tail9e88c5.ts.net (Funnel on)
|-- / proxy http://127.0.0.1:20128

===OLLAMA===
curl11434=000
===CLOUDFLARED-PS===
2238 /usr/bin/cloudflared --no-autoupdate tunnel run --token-file /etc/cloudflared/token
24062 /home/dr/.local/share/9router/bin/cloudflared tunnel --url http://127.0.0.1:20128 --config /tmp/cloudflared-quick-XFpbCK/config.yml --no-autoupdate --retries 99
   2238 qua out  7 01:26:49 2026    01:40:08 /usr/bin/cloudflared --no-autoupdate tunnel run --token-file /etc/cloudflared/token
  24062 qua out  7 02:29:19 2026       37:37 /home/dr/.local/share/9router/bin/cloudflared tunnel --url http://127.0.0.1:20128 --config /tmp/cloudflared-quick-XFpbCK/config.yml --no-autoupdate --retries 99
===SYSTEMD-USER-UNITS===
  sys-devices-virtual-net-tailscale0.device                                                              loaded    active   plugged   /sys/devices/virtual/net/tailscale0
  sys-subsystem-net-devices-tailscale0.device                                                            loaded    active   plugged   /sys/subsystem/net/devices/tailscale0
  9router.service                                                                                        loaded    active   running   9Router local AI gateway
```


## A6. cli.js 9router: contexto de cloudflared/tunnel + listing data dir

```
===CLIJS-TUNNEL-TERMS===
      5 tunnel
      3 tunnelDir
      3 killTunnelByPidFile
      2 tunnelEnabled
===CLIJS-CLOUDFLARED-CONTEXTO===
// Kill tunnel processes (cloudflared/tailscale) by their PID files
  killByPidFile(path.join(tunnelDir, "cloudflared.pid"));
// Kill cloudflared whose --url targets this app's port (covers stale PID file case)
tive -WindowStyle Hidden -Command "Get-WmiObject Win32_Process -Filter 'Name=\\"cloudflared.exe\\"' | Select-Object ProcessId,CommandLine | ConvertTo-Csv -NoTypeInformatio
        if (line.includes("cloudflared") && portMatchers.some(m => line.includes(m))) {
      // Background: MITM + tunnel/cloudflared run on separate ports/processes —
      // Kill cloudflared/tailscale via PID file (only this app's tunnel)
===DATA-DIR-FILES===
/home/dr/.local/share/9router/model-catalog.json 282986 bytes
/home/dr/.local/share/9router/db/data.sqlite-shm 32768 bytes
/home/dr/.local/share/9router/db/data.sqlite-wal 416152 bytes
/home/dr/.local/share/9router/db/data.sqlite 5074944 bytes
/home/dr/.local/share/9router/model-catalog-raw.json 576484 bytes
/home/dr/.local/share/9router/machine-id 64 bytes
/home/dr/.local/share/9router/auth/cli-secret 64 bytes
/home/dr/.local/share/9router/bin/cloudflared 39763452 bytes
/home/dr/.local/share/9router/jwt-secret 64 bytes
/home/dr/.local/share/9router/tunnel/state.json 110 bytes
/home/dr/.local/share/9router/tunnel/cloudflared.pid 5 bytes
/home/dr/.local/share/9router/runtime/package-lock.json 533 bytes
/home/dr/.local/share/9router/runtime/package.json 212 bytes
```