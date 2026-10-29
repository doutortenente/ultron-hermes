---
name: hermes-desktop-tijolao
description: "Use when rebuilding or fixing Hermes Desktop on Tijolão."
---

# Hermes Desktop no Tijolão

O app (janela Electron) roda no HOST; o motor continua sendo o container `hermes-agent`. Nada de segundo Hermes.

## Estado (22-out-2026)

- App: `~/.local/opt/hermes-desktop` (346 MB), build da tag v0.22.2 = mesmo commit do container (d923a5eb).
- Lançador: `~/.local/bin/hermes-desktop`. Menu: `~/.local/share/applications/com.nousresearch.hermes.desktop`. Ícone: `~/.local/share/icons/hicolor/{256x256,512x512}/apps/hermes.png`.
- Backend: dashboard do container em `127.0.0.1:9119` (network_mode host, loopback, sem gate de login).
- Dados do app no host: `~/.config/Hermes` (userData) e logs em `~/.hermes/logs/desktop.log` (pasta compartilhada com o container, mesmo uid).

## Por que compilar e não baixar / não `hermes desktop`

1. Não existe binário Linux oficial (v0.22.x): a página /desktop só tem .dmg e .exe; README de apps/desktop diz "Linux desktop legs are disabled"; issue #98171 aberta. Antes de recompilar, reconferir as assets da release no GitHub.
2. `hermes desktop` no container não serve: a imagem não tem `apps/desktop` e o container não tem tela.
3. `install.sh` no host criaria um SEGUNDO Hermes (runtime + gateway disputando o Telegram). Proibido.

## Rebuild (quando o container mudar de versão)

Versão alvo: `docker exec hermes-agent hermes --version` (linha "upstream <sha>"; a tag vX.Y.Z aponta para esse sha).

Script (rodar no host; foi o que funcionou em 22-out):

```bash
#!/usr/bin/env bash
set -euo pipefail
TAG=${1:?uso: build.sh vX.Y.Z}
B=$HOME/.cache/hermes-desktop-build
mkdir -p "$B" && cd "$B"
exec >>"$B/build.log" 2>&1
[ -d hermes-agent ] || git clone -q --depth 1 --branch "$TAG" https://github.com/NousResearch/hermes-agent.git
export NVM_DIR=$HOME/.local/share/nvm; . "$NVM_DIR/nvm.sh"
# package.json exige npm <11.10 ou >=11.17 (engine-strict); o nvm tem 11.16 -> npm isolado so pro build
[ -x "$B/npm/bin/npm" ] || npm install -g --prefix "$B/npm" npm@11.21.1 --no-audit --no-fund
export PATH="$B/npm/bin:$PATH"
cd hermes-agent && npm ci --no-audit --no-fund
cd apps/desktop && npm run build && npm run builder -- --dir --publish never
```

Disparo com teto de RAM (8 GB na máquina):

```bash
export XDG_RUNTIME_DIR=/run/user/1000 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus
systemd-run --user --unit=hermes-desktop-build --collect --wait -p MemoryMax=2200M -p CPUWeight=50 "$B/build.sh" vX.Y.Z
```

Tempos medidos: clone 71 s, npm ci 6 min, build 1 min, electron-builder 2,5 min (baixa Electron 110 MB). Total 9 min 36 s; pico de RAM 560 MB, swap 0 (o teto de 2200M sobra). Saída: `apps/desktop/release/linux-unpacked/Hermes`.

Troca: fechar o app (`pgrep -x Hermes`, nunca `pkill -f` com padrão que case com a própria linha), `mv ~/.local/opt/hermes-desktop{,.old}`, `cp -a .../release/linux-unpacked ~/.local/opt/hermes-desktop`, abrir e provar, só então apagar `.old`, `~/.cache/hermes-desktop-build` (2,5 GB) e `~/.cache/electron` (110 MB).

## Lançador (conteúdo atual)

```bash
#!/usr/bin/env bash
set -uo pipefail
URL="${HERMES_DESKTOP_REMOTE_URL:-http://127.0.0.1:9119}"
APP="$HOME/.local/opt/hermes-desktop/Hermes"
TOKEN="${HERMES_DESKTOP_REMOTE_TOKEN:-$(curl -fsS -m 5 "$URL/" 2>/dev/null | grep -o '__HERMES_SESSION_TOKEN__="[^"]*"' | head -1 | cut -d'"' -f2)}"
if [ -z "$TOKEN" ]; then
  MSG="Backend do Hermes fora do ar em $URL. Ligue o container (tijolao up) e abra de novo."
  notify-send -i hermes "Hermes Desktop" "$MSG" 2>/dev/null || true
  echo "$MSG" >&2; exit 1
fi
export HERMES_DESKTOP_REMOTE_URL="$URL" HERMES_DESKTOP_REMOTE_TOKEN="$TOKEN"
if [ -z "${HERMES_DESKTOP_PASSWORD_STORE:-}" ] && [ -n "${GNOME_KEYRING_CONTROL:-}" ]; then
  export HERMES_DESKTOP_PASSWORD_STORE=gnome-libsecret
fi
exec "$APP" --disable-setuid-sandbox "$@"
```

## Prova (3 sinais, todos medidos em 22-out)

1. `~/.hermes/logs/desktop.log`: `[boot] Remote Hermes backend is ready`.
2. `~/.hermes/logs/agent.log`: `tui_gateway.ws: ws accepted peer=127.0.0.1:...` (linha de chat aberta; é o elo que falha quando "backend ready" mente).
3. Barra de status do app: `client vX` igual a `backend vX`; sessões reais do state.db na lateral.

Abrir pelo mesmo caminho do menu: env da sessão Cinnamon (`/proc/$(pgrep -u dr -x cinnamon)/environ` via `mapfile -d ""`) + `env -i "${ENVV[@]}" gtk-launch com.nousresearch.hermes` (retorna na hora). A ferramenta terminal recusa `setsid`/`nohup` em comando de primeiro plano.

Print: `DISPLAY=:0 XAUTHORITY=/home/dr/.Xauthority import -window <id> <arquivo>`, salvando em `~/.hermes/cache/scratch` (o vision_analyze do container não enxerga `~/.cache` do host).

## Armadilhas

- **Token muda a cada restart do container.** Por isso o lançador lê do HTML de `GET /`. `HERMES_DESKTOP_REMOTE_URL` sem `HERMES_DESKTOP_REMOTE_TOKEN` = erro fatal no boot do app.
- **`HERMES_DESKTOP_CWD` não vale com backend remoto.** A sessão abre em `/opt/data` (HOME do container, volume que o host não enxerga). Remédio provável: pasta padrão de projeto nas configurações do app = `/home/dr/src` (existe igual nos dois lados). Não testado em 22-out.
- **X11 WM_CLASS do app = "hermes","Hermes"** → `StartupWMClass=Hermes` na entrada do menu.
- **RAM: ~1,1–1,2 GB (soma de RSS) com o app aberto.** Disponível caiu de 4,1 para 2,9 GB.
- **Não dirigir a janela com xdotool se o Dr. pode estar no PC.** Em 22-out as teclas de teste caíram na tela que ele tinha aberto (Capabilities); conferido: nenhuma mensagem enviada, nada instalado.
- **Botão de update dentro do app: não testado nesta instalação.** Atualizar = recompilar na versão do container.
