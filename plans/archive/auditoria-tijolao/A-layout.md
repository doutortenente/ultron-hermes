# Auditoria A — Layout Tijolão vs FHS/XDG (somente leitura)

Coleta: 2026-10-07T06:22:15 (UTC)
Método: SSH dr@localhost (ponte container->host). Todos du/find com timeout e -xdev/-x.

## 1.1 ls -la home (nível 1, ocultas incluídas)

`ls -la --time-style=+%Y-%m-%d /home/dr`

```
total 204
drwxr-x--- 24 dr   dr    4096 2026-10-07 .
drwxr-xr-x  3 root root  4096 2026-06-05 ..
drwxrwxr-x  6 dr   dr    4096 2026-09-23 .9router
drwxr-xr-x  2 dr   dr    4096 2026-10-04 Área de trabalho
drwxrwxr-x  2 dr   dr    4096 2026-10-02 backups
-rw-------  1 dr   dr    1051 2026-10-07 .bash_history
-rw-rw-r--  1 dr   dr     281 2026-10-04 .bashrc
drwxr-xr-x 17 dr   dr    4096 2026-10-07 .cache
drwx------  4 dr   dr    4096 2026-10-07 .claude
-rw-------  1 dr   dr   52546 2026-10-07 .claude.json
drwxrwxr-x  2 dr   dr    4096 2026-10-07 .codex
drwx------ 42 dr   dr    4096 2026-10-02 .config
drwx------  3 dr   dr    4096 2026-09-09 .docker
drwxr-xr-x  3 dr   dr    4096 2026-10-07 Downloads
-rw-------  1 dr   dr      74 2026-10-02 .git-credentials
drwx------  3 dr   dr    4096 2026-09-09 .gnome
-rw-rw-r--  1 dr   dr     245 2026-10-01 .gtkrc-2.0
drwx------ 45 dr   dr    4096 2026-10-07 .hermes
drwxr-xr-x  3 dr   dr    4096 2026-10-04 Imagens
drwxrwxrwx  3 dr   dr    4096 2026-10-07 .linuxmint
drwx------ 10 dr   dr    4096 2026-09-07 .local
drwxrwxr-x  5 dr   dr    4096 2026-10-04 .npm
drwx------  3 dr   dr    4096 2026-07-25 .pki
drwx------  2 dr   dr    4096 2026-10-04 .poolside
-rw-rw-r--  1 dr   dr      26 2026-09-09 .profile
drwxrwxr-x  8 dr   dr    4096 2026-10-02 src
drwx------  2 dr   dr    4096 2026-09-23 .ssh
-rw-r--r--  1 dr   dr       0 2026-09-08 .sudo_as_admin_successful
drwxrwxr-x  3 dr   dr    4096 2026-09-27 .themes
drwxr-xr-x  3 dr   dr    4096 2026-08-09 .var
drwxrwxr-x  4 dr   dr    4096 2026-10-02 vaults
-rw-------  1 dr   dr      52 2026-10-07 .Xauthority
-rw-------  1 dr   dr   14453 2026-10-07 .xsession-errors
-rw-------  1 dr   dr   15930 2026-10-07 .xsession-errors.old

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 1.2 du -xsh por entrada nível 1 (timeout 60 cada)

`cd /home/dr && for d in $(ls -A); do timeout 60 du -xsh -- "$d"; done`

```
31M	.9router
4,0K	backups
4,0K	.bash_history
4,0K	.bashrc
787M	.cache
16K	.claude
52K	.claude.json
8,0K	.codex
5,2G	.config
80K	.docker
68M	Downloads
4,0K	.git-credentials
28K	.gnome
4,0K	.gtkrc-2.0
1,9G	.hermes
2,3M	Imagens
16K	.linuxmint
12G	.local
613M	.npm
76K	.pki
8,0K	.poolside
4,0K	.profile
1,4G	src
8,0K	.ssh
0	.sudo_as_admin_successful
2,1M	.themes
322M	.var
368M	vaults
4,0K	.Xauthority
16K	.xsession-errors
16K	.xsession-errors.old

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 2.1 nível 2 de .local/.config/.cache (top por tamanho)

`cd /home/dr && timeout 60 du -xsh .local/* .local/*/* 2>/dev/null | sort -rh | head -40`

```
9,8G	.local/share
984M	.local/lib
313M	.local/zed.app
191M	.local/jdk-25
48M	.local/bin
29M	.local/state
308K	.local/qpdf-root
32K	.local/secrets

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 2.2 nível 2 .config

`cd /home/dr && timeout 60 du -xsh .config/* 2>/dev/null | sort -rh | head -30`

```
3,9G	.config/google-chrome
616M	.config/mozilla
379M	.config/Claude
254M	.config/Claude-3p
133M	.config/Codex
9,2M	.config/libreoffice
2,1M	.config/chromium
360K	.config/cinnamon
296K	.config/copyq
104K	.config/github-copilot
84K	.config/poolside
60K	.config/session
52K	.config/autostart
40K	.config/dconf
28K	.config/systemd
28K	.config/evolution
24K	.config/zed
24K	.config/kilerc
24K	.config/browser-harness
16K	.config/n8n
16K	.config/menus
12K	.config/xed
12K	.config/vivaldi
12K	.config/sticky
12K	.config/pix
12K	.config/ibus
12K	.config/git
12K	.config/gh
12K	.config/fish
8,0K	.config/xviewer

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 2.3 nível 2 .cache

`cd /home/dr && timeout 60 du -xsh .cache/* 2>/dev/null | sort -rh | head -20`

```
562M	.cache/google-chrome
162M	.cache/pip
38M	.cache/mintinstall
8,4M	.cache/mesa_shader_cache
7,5M	.cache/flatpak
3,5M	.cache/node-systray
1,9M	.cache/radv_builtin_shaders
1,8M	.cache/fontconfig
1000K	.cache/cs_backgrounds
468K	.cache/thumbnails
444K	.cache/evolution
216K	.cache/ibus
200K	.cache/wallpaper
12K	.cache/gtk-3.0
4,0K	.cache/zed
0	.cache/motd.legal-displayed

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 2.4 nível 2 dotdirs soltos (.9router .docker .claude .codex .poolside .gnome .linuxmint .pki .themes .var)

`cd /home/dr && timeout 60 du -xsh .9router/* .docker/* .claude/* .codex/* .poolside/* .gnome/* .linuxmint/* .pki/*/* .themes/* .var/* 2>/dev/null | head -80`

```
8,0K	.9router/auth
212K	.9router/db
4,0K	.9router/jwt-secret
8,0K	.9router/logs
4,0K	.9router/machine-id
30M	.9router/runtime
72K	.docker/buildx
4,0K	.claude/sessions
4,0K	.claude/settings.json
4,0K	.claude/skills
4,0K	.codex/config.toml
4,0K	.poolside/settings.local.yaml
24K	.gnome/apps
12K	.linuxmint/mintupdate
28K	.pki/nssdb/cert9.db
36K	.pki/nssdb/key4.db
4,0K	.pki/nssdb/pkcs11.txt
2,1M	.themes/CGreen
322M	.var/app

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 2.5 dono root dentro da home

`cd /home/dr && timeout 60 find . -xdev -maxdepth 3 \( -user root -o -not -user dr \) -printf '%u:%g %y %p\n' 2>/dev/null | head -30`

```
root:root d ./.claude/skills

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 2.6 datas (mtime) nível 1

`cd /home/dr && ls -A | while read d; do stat -c '%y %U:%G %n' -- "$d" 2>/dev/null | cut -c1-10,26-; done`

```
2026-09-238189 -0300 dr:dr .9router
2026-10-043735 -0300 dr:dr Área de trabalho
2026-10-024937 -0300 dr:dr backups
2026-10-076549 -0300 dr:dr .bash_history
2026-10-041682 -0300 dr:dr .bashrc
2026-10-074105 -0300 dr:dr .cache
2026-10-072865 -0300 dr:dr .claude
2026-10-072948 -0300 dr:dr .claude.json
2026-10-071823 -0300 dr:dr .codex
2026-10-025428 -0300 dr:dr .config
2026-09-091207 -0300 dr:dr .docker
2026-10-076877 -0300 dr:dr Downloads
2026-10-023252 -0300 dr:dr .git-credentials
2026-09-097909 -0300 dr:dr .gnome
2026-10-012133 -0300 dr:dr .gtkrc-2.0
2026-10-073799 -0300 dr:dr .hermes
2026-10-046310 -0300 dr:dr Imagens
2026-10-071517 -0300 dr:dr .linuxmint
2026-09-073001 -0300 dr:dr .local
2026-10-044376 -0300 dr:dr .npm
2026-07-250961 -0300 dr:dr .pki
2026-10-049408 -0300 dr:dr .poolside
2026-09-094163 -0300 dr:dr .profile
2026-10-020790 -0300 dr:dr src
2026-09-233927 -0300 dr:dr .ssh
2026-09-088312 -0300 dr:dr .sudo_as_admin_successful
2026-09-276533 -0300 dr:dr .themes
2026-08-092268 -0300 dr:dr .var
2026-10-026007 -0300 dr:dr vaults
2026-10-077653 -0300 dr:dr .Xauthority
2026-10-071694 -0300 dr:dr .xsession-errors
2026-10-079374 -0300 dr:dr .xsession-errors.old

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 3.1 user-dirs.dirs

`cat ~/.config/user-dirs.dirs 2>&1 || echo AUSENTE`

```
# This file is written by xdg-user-dirs-update
# If you want to change or add directories, just edit the line you're
# interested in. All local changes will be retained on the next run.
# Format is XDG_xxx_DIR="$HOME/yyy", where yyy is a shell-escaped
# homedir-relative path, or XDG_xxx_DIR="/yyy", where /yyy is an
# absolute path. No other format is supported.
# 
XDG_DESKTOP_DIR="$HOME/Área de trabalho"
XDG_DOWNLOAD_DIR="$HOME/Downloads"
XDG_TEMPLATES_DIR="$HOME/"
XDG_PUBLICSHARE_DIR="$HOME/"
XDG_DOCUMENTS_DIR="$HOME/vaults/Documentos"
XDG_MUSIC_DIR="$HOME/"
XDG_PICTURES_DIR="$HOME/Imagens"
XDG_VIDEOS_DIR="$HOME/"

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 3.2 pastas XDG esperadas

`for d in 'Área de trabalho' Documentos Downloads Imagens Música Vídeos Modelos Público; do [ -d "/home/dr/$d" ] && echo "EXISTE: $d" || echo "FALTA: $d"; done; ls -d /home/dr/Área* /home/dr/*ocumentos* 2>/dev/null`

```
EXISTE: Área de trabalho
FALTA: Documentos
EXISTE: Downloads
EXISTE: Imagens
FALTA: Música
FALTA: Vídeos
FALTA: Modelos
FALTA: Público
/home/dr/Área de trabalho

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 3.3 XDG efetivo no systemd --user

`systemctl --user show-environment 2>&1 | grep XDG`

```
XDG_DATA_DIRS=/usr/share/cinnamon:/home/dr/.local/share/flatpak/exports/share:/var/lib/flatpak/exports/share:/usr/local/share:/usr/share
XDG_RUNTIME_DIR=/run/user/1000
XDG_CONFIG_DIRS=/etc/xdg/xdg-cinnamon:/etc/xdg
XDG_CURRENT_DESKTOP=X-Cinnamon
XDG_GREETER_DATA_DIR=/var/lib/lightdm-data/dr
XDG_SEAT_PATH=/org/freedesktop/DisplayManager/Seat0
XDG_SESSION_CLASS=user
XDG_SESSION_DESKTOP=cinnamon
XDG_SESSION_PATH=/org/freedesktop/DisplayManager/Session0
XDG_SESSION_TYPE=x11

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 3.4 XDG_* definidas no shell/login

`env | grep -i XDG; echo ---; cat ~/.pam_environment 2>/dev/null; echo ---; grep -n 'XDG' ~/.profile ~/.bashrc 2>/dev/null`

```
XDG_SESSION_TYPE=tty
XDG_SESSION_CLASS=user
XDG_SESSION_ID=88
XDG_RUNTIME_DIR=/run/user/1000
---
---

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 3.5 .profile (mascarado)

`sed -E 's/(KEY|TOKEN|SECRET|PASS|PASSWORD|CRED)[A-Za-z0-9_]*=.*/\1=***MASK***/Ig' ~/.profile`

```
. "$HOME/.local/bin/env"

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 3.6 .bashrc (mascarado)

`sed -E 's/(KEY|TOKEN|SECRET|PASS|PASSWORD|CRED)[A-Za-z0-9_]*=.*/\1=***MASK***/Ig' ~/.bashrc | head -60`

```
# >>> node via nvm (Hermes, 04-out-2026) >>>
export NVM_DIR="$HOME/.local/share/nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
# ~/.local/bin na frente do nvm: claude, codex e pnpm 11.20.0 seguem os mesmos de antes
export PATH="$HOME/.local/bin:$PATH"
# <<< node via nvm <<<

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 3.7 nvm — onde está hoje

`ls -d ~/.local/share/nvm ~/.config/nvm ~/.nvm 2>&1; echo ---; grep -rn 'nvm' ~/.bashrc ~/.profile 2>/dev/null | head`

```
ls: não foi possível acessar '/home/dr/.config/nvm': Arquivo ou diretório inexistente
ls: não foi possível acessar '/home/dr/.nvm': Arquivo ou diretório inexistente
/home/dr/.local/share/nvm
---
/home/dr/.bashrc:1:# >>> node via nvm (Hermes, 04-out-2026) >>>
/home/dr/.bashrc:2:export NVM_DIR="$HOME/.local/share/nvm"
/home/dr/.bashrc:3:[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
/home/dr/.bashrc:4:# ~/.local/bin na frente do nvm: claude, codex e pnpm 11.20.0 seguem os mesmos de antes
/home/dr/.bashrc:6:# <<< node via nvm <<<

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 4.1 .local/bin completo (tipo, alvo, quebrado?)

`for f in /home/dr/.local/bin/*; do if [ -L "$f" ]; then t=$(readlink -f "$f"); [ -e "$f" ] && s=OK || s=QUEBRADO; echo "SYMLINK $(basename $f) -> $t [$s]"; elif [ -f "$x" ] && [ -x "$f" ]; then echo "BIN $(basename $f)"; else echo "FILE $(basename $f)"; fi; done`

```
SYMLINK 9router -> /home/dr/.local/lib/node_modules/9router/cli.js [OK]
SYMLINK claude -> /home/dr/.local/share/claude/versions/2.1.285 [OK]
SYMLINK codex -> /home/dr/.local/lib/node_modules/@openai/codex/bin/codex.js [OK]
SYMLINK ctx7 -> /home/dr/.local/lib/node_modules/ctx7/dist/index.js [OK]
FILE env
FILE env.fish
FILE hermes
FILE hermes-acp
FILE hermes-agent
FILE local
FILE obsidian
SYMLINK pn -> /home/dr/.local/lib/node_modules/pnpm/bin/pnpm.mjs [OK]
SYMLINK pnpm -> /home/dr/.local/lib/node_modules/pnpm/bin/pnpm.mjs [OK]
SYMLINK pnpx -> /home/dr/.local/lib/node_modules/pnpm/bin/pnpx.mjs [OK]
SYMLINK pnx -> /home/dr/.local/lib/node_modules/pnpm/bin/pnpx.mjs [OK]
FILE pool
FILE qpdf
SYMLINK rclone -> /home/dr/src/scripts/nuvem/bin/rclone [OK]
FILE tijolao
SYMLINK tokentracker -> /home/dr/.local/lib/node_modules/tokentracker-cli/bin/tracker.js [OK]
SYMLINK tokentracker-cli -> /home/dr/.local/lib/node_modules/tokentracker-cli/bin/tracker.js [OK]
SYMLINK tracker -> /home/dr/.local/lib/node_modules/tokentracker-cli/bin/tracker.js [OK]
SYMLINK zed -> /home/dr/.local/zed.app/bin/zed [OK]

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 4.2 .local/lib e .local/state nível 2

`timeout 60 du -xsh /home/dr/.local/lib/* /home/dr/.local/state/* 2>/dev/null | sort -rh | head -25`

```
984M	/home/dr/.local/lib/node_modules
28M	/home/dr/.local/state/poolside
676K	/home/dr/.local/state/codex
60K	/home/dr/.local/state/tirith
16K	/home/dr/.local/lib/python3.12
12K	/home/dr/.local/state/wireplumber
12K	/home/dr/.local/state/bash
8,0K	/home/dr/.local/state/pnpm
8,0K	/home/dr/.local/state/openai-codex
8,0K	/home/dr/.local/state/hermes
8,0K	/home/dr/.local/state/gh
8,0K	/home/dr/.local/state/context7
8,0K	/home/dr/.local/state/claude
8,0K	/home/dr/.local/state/cinnamon
4,0K	/home/dr/.local/state/fix-ide-mcp.log

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 4.3 .local/share top 15

`timeout 60 du -xsh /home/dr/.local/share/* 2>/dev/null | sort -rh | head -15`

```
3,6G	/home/dr/.local/share/nvm
2,2G	/home/dr/.local/share/pnpm
1,8G	/home/dr/.local/share/zed
1,7G	/home/dr/.local/share/Trash
450M	/home/dr/.local/share/claude
74M	/home/dr/.local/share/9router
64M	/home/dr/.local/share/n8n
54M	/home/dr/.local/share/fonts
21M	/home/dr/.local/share/cinnamon
1,6M	/home/dr/.local/share/locale
1,2M	/home/dr/.local/share/nemo
716K	/home/dr/.local/share/icons
448K	/home/dr/.local/share/gvfs-metadata
160K	/home/dr/.local/share/evolution
132K	/home/dr/.local/share/recently-used.xbel

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 4.4 .local/secrets (nomes e tamanhos APENAS)

`ls -la /home/dr/.local/secrets/ | awk '{print $5, $9}'`

```
4096 .
4096 ..
10439 .env
1675 obsidian-rest-rsa.pem
10418 tijolao.env

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 4.5 .local/share/9router vs ~/.9router (duplicata?)

`timeout 60 du -xsh /home/dr/.local/share/9router/* /home/dr/.local/share/nvm 2>/dev/null | sort -rh | head -12; echo ---; ls /home/dr/.local/share/9router/ 2>/dev/null`

```
3,6G	/home/dr/.local/share/nvm
38M	/home/dr/.local/share/9router/bin
30M	/home/dr/.local/share/9router/runtime
5,1M	/home/dr/.local/share/9router/db
564K	/home/dr/.local/share/9router/model-catalog-raw.json
280K	/home/dr/.local/share/9router/model-catalog.json
20K	/home/dr/.local/share/9router/tailscale
12K	/home/dr/.local/share/9router/tunnel
8,0K	/home/dr/.local/share/9router/logs
8,0K	/home/dr/.local/share/9router/auth
4,0K	/home/dr/.local/share/9router/machine-id
4,0K	/home/dr/.local/share/9router/jwt-secret
---
auth
bin
db
jwt-secret
logs
machine-id
model-catalog.json
model-catalog-raw.json
runtime
tailscale
tunnel

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 4.6 node_modules globais

`ls /home/dr/.local/lib/node_modules 2>/dev/null; echo ---; ls /home/dr/.config/nvm 2>/dev/null || true`

```
9router
@agentclientprotocol
better-sqlite3
ctx7
@google
@openai
opencode-ai
pnpm
sql.js
systray2
tokentracker-cli
---

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 5.1 ~/src nível 1

`timeout 60 du -xsh /home/dr/src/* 2>/dev/null | sort -rh; echo ---; ls -la /home/dr/src`

```
1,1G	/home/dr/src/sasi
164M	/home/dr/src/hermes-workspace
84M	/home/dr/src/scripts
49M	/home/dr/src/Claude-workspace
2,1M	/home/dr/src/tijolao-ai
408K	/home/dr/src/nim-bench
---
total 32
drwxrwxr-x  8 dr dr 4096 out  2 21:31 .
drwxr-x--- 24 dr dr 4096 out  7 02:27 ..
drwxrwxr-x 11 dr dr 4096 out  2 08:24 Claude-workspace
drwxrwxr-x 10 dr dr 4096 out  4 13:14 hermes-workspace
drwxr-xr-x  4 dr dr 4096 set 29 20:23 nim-bench
drwxr-xr-x 10 dr dr 4096 out  2 05:36 sasi
drwxrwxr-x  8 dr dr 4096 set  9 11:58 scripts
drwxrwxr-x  7 dr dr 4096 out  2 17:14 tijolao-ai

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 5.2 repos git em ~/src (branch/remote/sujos)

`for r in /home/dr/src/*/; do if [ -d "$r/.git" ] || git -C "$r" rev-parse --git-dir >/dev/null 2>&1; then b=$(git -C "$r" branch --show-current 2>/dev/null); rmt=$(git -C "$r" remote get-url origin 2>/dev/null || echo none); n=$(git -C "$r" status --porcelain 2>/dev/null | wc -l); sz=$(timeout 30 du -xsh "$r" 2>/dev/null | cut -f1); echo "REPO $r | $sz | branch=$b | dirty=$n | remote=$rmt"; else echo "NAO-GIT $r $(timeout 30 du -xsh $r 2>/dev/null | cut -f1)"; fi; done`

```
REPO /home/dr/src/Claude-workspace/ | 49M | branch=main | dirty=1 | remote=https://github.com/doutortenente/Claude.git
REPO /home/dr/src/hermes-workspace/ | 164M | branch=tijolao | dirty=0 | remote=https://github.com/doutortenente/hermes-workspace.git
NAO-GIT /home/dr/src/nim-bench/ 408K
NAO-GIT /home/dr/src/sasi/ 1,1G
REPO /home/dr/src/scripts/ | 84M | branch=main | dirty=5 | remote=https://github.com/doutortenente/scripts.git
REPO /home/dr/src/tijolao-ai/ | 2,1M | branch=main | dirty=27 | remote=https://github.com/doutortenente/tijolao-ai.git

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 5.3 pastas aninhadas suspeitas (repos dentro de repos / .git duplicados)

`find /home/dr/src -xdev -maxdepth 3 -name .git -type d 2>/dev/null`

```
/home/dr/src/hermes-workspace/.git
/home/dr/src/sasi/AUTOMACAO-SASI/.git
/home/dr/src/sasi/SASI-V3/.git
/home/dr/src/scripts/.git
/home/dr/src/tijolao-ai/.git
/home/dr/src/Claude-workspace/.git

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 5.4 ~/vaults

`timeout 60 du -xsh /home/dr/vaults/* /home/dr/vaults/*/* 2>/dev/null | sort -rh | head -20`

```
265M	/home/dr/vaults/celebro
104M	/home/dr/vaults/Documentos

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 5.5 ~/backups

`find /home/dr/backups -xdev -maxdepth 3 -printf '%y %s %TY-%Tm-%Td %p\n' 2>/dev/null | head -30`

```
d 4096 2026-10-02 /home/dr/backups

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 5.6 Área de trabalho / Downloads / Imagens (contagem + maiores)

`for d in 'Área de trabalho' Downloads Imagens; do echo "== $d"; find "/home/dr/$d" -xdev -type f 2>/dev/null | wc -l; timeout 40 find "/home/dr/$d" -xdev -type f -printf '%s %p\n' 2>/dev/null | sort -rn | head -5; done`

```
== Área de trabalho
13
13361 /home/dr/Área de trabalho/org.kde.kate.desktop
8576 /home/dr/Área de trabalho/google-chrome.desktop
6729 /home/dr/Área de trabalho/org.x.editor.desktop
4817 /home/dr/Área de trabalho/sticky.desktop
1190 /home/dr/Área de trabalho/com.anthropic.Claude.desktop
== Downloads
76
7483066 /home/dr/Downloads/DOCS-E-RASCUNHOS-PLANTOES/04-10-26-NOT/controles-uti2-04-10-26-not.pdf
6525308 /home/dr/Downloads/DOCS-E-RASCUNHOS-PLANTOES/PLANTAO-UTI2-26-09-26-NOT/docs-para-processar/27-09-26/controles-uti2-24h-27-09-26.pdf
6499365 /home/dr/Downloads/DOCS-E-RASCUNHOS-PLANTOES/PLANTAO-UTI2-26-09-26-NOT/docs-para-processar/prescricoes-uti2-26-09-26-not.pdf
6311336 /home/dr/Downloads/DOCS-E-RASCUNHOS-PLANTOES/03-10-26-uti2-noturno/controles-e-balanco-uti2-03-10-26.pdf
6100675 /home/dr/Downloads/DOCS-E-RASCUNHOS-PLANTOES/PLANTAO-UTI2-26-09-26-NOT/docs-para-processar/controles-das-06h-as-18h-uti2-26-09-26.pdf
== Imagens
4
1779160 /home/dr/Imagens/Wallpapers/CGreen-Wallpaper.png
507501 /home/dr/Imagens/Wallpapers/kobe-bryant-fanart-4u-1366x768.jpg
37930 /home/dr/Imagens/Wallpapers/baixada-2.jpeg
30140 /home/dr/Imagens/Wallpapers/baixada-1.jpeg

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 6.1 /opt

`ls -la /opt 2>&1; timeout 40 du -xsh /opt/* 2>/dev/null`

```
total 16
drwxr-xr-x  4 root root 4096 set 21 14:52 .
drwxr-xr-x 23 root root 4096 set  9 12:39 ..
drwx--x--x  4 root root 4096 jun 16 17:26 containerd
drwxr-xr-x  3 root root 4096 jun 10 05:37 google
4,0K	/opt/containerd
437M	/opt/google

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 6.2 /srv

`ls -la /srv 2>&1`

```
total 8
drwxr-xr-x  2 root root 4096 jan  8  2026 .
drwxr-xr-x 23 root root 4096 set  9 12:39 ..

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 6.3 /usr/local/{bin,lib,share,src}

`for d in bin lib share src; do echo "== /usr/local/$d"; ls -la /usr/local/$d 2>/dev/null | head -12; done`

```
== /usr/local/bin
total 36
drwxr-xr-x  2 root root 4096 out  2 01:42 .
drwxr-xr-x 10 root root 4096 jan  8  2026 ..
lrwxrwxrwx  1 root root   40 set 15 14:31 9remote -> ../lib/node_modules/9remote/dist/cli.cjs
-rwxr-xr-x  1 root root 8301 nov 20  2025 apt
lrwxrwxrwx  1 root root   20 set 24 21:51 cloudflared -> /usr/bin/cloudflared
-rwxr-xr-x  1 root root  536 abr 26  2022 gnome-help
-rwxr-xr-x  1 root root  196 fev  7  2019 highlight-mint
-rwxr-xr-x  1 root root 1201 mai 31  2023 search
-rwxr-xr-x  1 root root  553 abr 26  2022 yelp
== /usr/local/lib
total 16
drwxr-xr-x  4 root root 4096 out  2 01:10 .
drwxr-xr-x 10 root root 4096 jan  8  2026 ..
drwxr-xr-x  6 root root 4096 out  2 01:42 node_modules
drwxr-xr-x  3 root root 4096 jan  8  2026 python3.12
== /usr/local/share
total 32
drwxr-xr-x  8 root root  4096 set 21 14:45 .
drwxr-xr-x 10 root root  4096 jan  8  2026 ..
drwxr-xr-x  2 root root  4096 jan  8  2026 ca-certificates
drwxrwsr-x  2 root staff 4096 jan  8  2026 fonts
drwxr-xr-x  2 root root  4096 jan  8  2026 man
drwxr-xr-x  7 root root  4096 jan  8  2026 sgml
drwxr-xr-x  2 root root  4096 set 21 14:45 texmf
drwxr-xr-x  6 root root  4096 jan  8  2026 xml
== /usr/local/src
total 8
drwxr-xr-x  2 root root 4096 jan  8  2026 .
drwxr-xr-x 10 root root 4096 jan  8  2026 ..

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 6.4 snap list

`snap list 2>&1 | head -15`

```
bash: linha 1: snap: comando não encontrado

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 6.5 flatpak list

`flatpak list 2>&1 | head -15`

```
Bitwarden	com.bitwarden.desktop	2026.9.1	stable	system
Obsidian	md.obsidian.Obsidian	1.14.4	stable	system
Freedesktop Platform	org.freedesktop.Platform	freedesktop-sdk-25.08.17	25.08	system
Freedesktop Platform	org.freedesktop.Platform	freedesktop-sdk-26.08.2	26.08	system
Mesa	org.freedesktop.Platform.GL.default	26.2.2	25.08	system
Mesa (Extra)	org.freedesktop.Platform.GL.default	26.2.2	25.08-extra	system
Mesa	org.freedesktop.Platform.GL.default	26.2.2	26.08	system
Mesa (Extra)	org.freedesktop.Platform.GL.default	26.2.2	26.08-extra	system
Intel VAAPI driver	org.freedesktop.Platform.VAAPI.Intel		25.08	system
Intel VAAPI driver	org.freedesktop.Platform.VAAPI.Intel		26.08	system
AMD AMF driver	org.freedesktop.Platform.amd.amf		26.08	system
Codecs Extra Extension	org.freedesktop.Platform.codecs-extra		25.08-extra	system
Codecs Extra Extension	org.freedesktop.Platform.codecs-extra		26.08-extra	system
Freedesktop SDK	org.freedesktop.Sdk	freedesktop-sdk-25.08.17	25.08	system
GNOME Application Platform version 50	org.gnome.Platform		50	system

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 6.6 binários fora do apt em PATH do sistema

`for d in /usr/local/bin /usr/bin; do ls -p $d 2>/dev/null | head -3 >/dev/null; done; ls -la /usr/local/bin 2>/dev/null | head -20; echo ---; dpkg -S /usr/local/bin/* 2>&1 | head -5`

```
total 36
drwxr-xr-x  2 root root 4096 out  2 01:42 .
drwxr-xr-x 10 root root 4096 jan  8  2026 ..
lrwxrwxrwx  1 root root   40 set 15 14:31 9remote -> ../lib/node_modules/9remote/dist/cli.cjs
-rwxr-xr-x  1 root root 8301 nov 20  2025 apt
lrwxrwxrwx  1 root root   20 set 24 21:51 cloudflared -> /usr/bin/cloudflared
-rwxr-xr-x  1 root root  536 abr 26  2022 gnome-help
-rwxr-xr-x  1 root root  196 fev  7  2019 highlight-mint
-rwxr-xr-x  1 root root 1201 mai 31  2023 search
-rwxr-xr-x  1 root root  553 abr 26  2022 yelp
---
dpkg-query: não foi encontrado caminho coincidindo com o padrão /usr/local/bin/9remote
mintsystem: /usr/local/bin/apt
dpkg-query: não foi encontrado caminho coincidindo com o padrão /usr/local/bin/cloudflared
ubuntu-system-adjustments: /usr/local/bin/gnome-help
mintsystem: /usr/local/bin/highlight-mint

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 6.7 sudo -n funciona?

`sudo -n true 2>&1 && echo SUDO-OK || echo SUDO-NEGADO`

```
sudo: uma senha é necessária
SUDO-NEGADO

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 6.8 node/npm/python fora do apt

`which -a node npm python3 pip3 2>/dev/null; ls -la /usr/local/bin/node* /usr/local/bin/npm* 2>/dev/null; echo ---; ls /home/dr/.local/zed.app /home/dr/.local/jdk-25 2>/dev/null`

```
/home/dr/.local/share/nvm/versions/node/v24.16.0/bin/node
/usr/bin/node
/bin/node
/home/dr/.local/share/nvm/versions/node/v24.16.0/bin/npm
/usr/bin/npm
/bin/npm
/usr/bin/python3
/bin/python3
/usr/bin/pip3
/bin/pip3
---
/home/dr/.local/jdk-25:
bin
conf
legal
lib
NOTICE
release

/home/dr/.local/zed.app:
bin
lib
libexec
licenses.md
share

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 7.1 scripts duplicados (nomes iguais em lugares diferentes)

`find /home/dr/.local/bin /home/dr/src/scripts /home/dr/src/tijolao-ai /home/dr/src/hermes-workspace -xdev \( -name '*.sh' -o -name '*.py' -o -name 'rclone' \) -type f 2>/dev/null | awk -F/ '{print $NF}' | sort | uniq -d | head -15`

```
[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 7.2 9router: 3 locais?

`ls -d /home/dr/.9router /home/dr/.local/share/9router /home/dr/.local/lib/node_modules/9router /usr/local/lib/node_modules/9router 2>&1; echo ---; timeout 30 du -xsh /home/dr/.local/lib/node_modules/9router /usr/local/lib/node_modules/9router 2>/dev/null`

```
ls: não foi possível acessar '/usr/local/lib/node_modules/9router': Arquivo ou diretório inexistente
/home/dr/.9router
/home/dr/.local/lib/node_modules/9router
/home/dr/.local/share/9router
---
74M	/home/dr/.local/lib/node_modules/9router

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 7.3 Trash (o que é grande na lixeira)

`timeout 40 du -xsh /home/dr/.local/share/Trash /home/dr/.local/share/Trash/files/* 2>/dev/null | sort -rh | head -8`

```
1,7G	/home/dr/.local/share/Trash

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 7.4 pastas vazias na raiz da home

`find /home/dr -maxdepth 1 -type d -empty -printf '%p VAZIA\n' 2>/dev/null; find /home/dr/backups -maxdepth 2 2>/dev/null | head`

```
/home/dr/backups VAZIA
/home/dr/backups

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 7.5 .var/app (flatpak)

`timeout 40 du -xsh /home/dr/.var/app/* 2>/dev/null | sort -rh`

```
252M	/home/dr/.var/app/md.obsidian.Obsidian
39M	/home/dr/.var/app/org.telegram.desktop
16M	/home/dr/.var/app/io.github.shiftey.Desktop
16M	/home/dr/.var/app/com.bitwarden.desktop
568K	/home/dr/.var/app/org.kde.kate
16K	/home/dr/.var/app/org.mozilla.firefox

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 7.6 nvm duplicado? versões de node

`ls /home/dr/.local/share/nvm/versions/node/ 2>/dev/null; echo ---; /usr/bin/node --version 2>/dev/null; /home/dr/.local/share/nvm/versions/node/v24.16.0/bin/node --version 2>/dev/null`

```
v24.16.0
---
v18.19.1
v24.16.0

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 7.7 user-dirs locale ptbr e xdg-user-dirs-update

`locale 2>/dev/null | head -3; echo ---; xdg-user-dir DESKTOP DOWNLOAD DOCUMENTS 2>/dev/null; echo ---; ls -la /home/dr/vaults/Documentos | head -5`

```
LANG=pt_BR.UTF-8
LANGUAGE=pt_BR:pt:en
LC_CTYPE=C.UTF-8
---
/home/dr/Área de trabalho
---
total 168
drwxr-xr-x 5 dr dr   4096 out  4 15:41 .
drwxrwxr-x 4 dr dr   4096 out  2 20:50 ..
drwxr-xr-x 3 dr dr   4096 ago  1 01:07 Documentos-cadastro-dr-nicholas
-rw-rw-r-- 1 dr dr 149300 set 25 08:44 EXTRACAO-CLINICA-SASI.zip

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 7.8 systemd --user units

`ls /home/dr/.config/systemd/user/ 2>/dev/null; systemctl --user list-units --type=service --no-pager --no-legend 2>/dev/null | head`

```
9router.service
default.target.wants
hermes-dashboard.service
hermes-gateway.service
n8n.service
  9router.service                       loaded active running 9Router local AI gateway
  dbus.service                          loaded active running D-Bus User Message Bus
  dconf.service                         loaded active running User preferences database
  evolution-addressbook-factory.service loaded active running Evolution address book service
  evolution-calendar-factory.service    loaded active running Evolution calendar service
  evolution-source-registry.service     loaded active running Evolution source registry
  filter-chain.service                  loaded active running PipeWire filter chain daemon
  flatpak-portal.service                loaded active running flatpak portal
  flatpak-session-helper.service        loaded active running flatpak session helper
  gnome-keyring-daemon.service          loaded active running GNOME Keyring daemon

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 8.1 Trash files top

`timeout 40 du -xsh /home/dr/.local/share/Trash/files 2>/dev/null; ls /home/dr/.local/share/Trash/files 2>/dev/null | head -10`

```
1,7G	/home/dr/.local/share/Trash/files
agentic-harness-0.9.2-v1.zip
Agent Protocols-1.0.0-v1.zip
AI-Integration-Architect-1.0.0-v1.zip
arn-infra-v1.zip
chefe
chrome-devtools-mcp
claude
claude-cli-nodejs
Cloudflare-1.0.0-v1.zip
cs_themes

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 8.2 sasi nível 2 (o que pesa 1,1G?)

`timeout 60 du -xsh /home/dr/src/sasi/* 2>/dev/null | sort -rh | head -10`

```
1,1G	/home/dr/src/sasi/SASI-V3
1,4M	/home/dr/src/sasi/private
1,2M	/home/dr/src/sasi/evidence
724K	/home/dr/src/sasi/AUTOMACAO-SASI
308K	/home/dr/src/sasi/evidence-operational
236K	/home/dr/src/sasi/scripts
60K	/home/dr/src/sasi/src
40K	/home/dr/src/sasi/package-lock.json
40K	/home/dr/src/sasi/docs
4,0K	/home/dr/src/sasi/tsconfig.json

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 8.3 .hermes nível 2

`timeout 60 du -xsh /home/dr/.hermes/* 2>/dev/null | sort -rh | head -12`

```
1,2G	/home/dr/.hermes/home
218M	/home/dr/.hermes/profiles
120M	/home/dr/.hermes/state.db
89M	/home/dr/.hermes/lsp
55M	/home/dr/.hermes/skills
39M	/home/dr/.hermes/lazy-packages
38M	/home/dr/.hermes/bin
26M	/home/dr/.hermes/logs
16M	/home/dr/.hermes/cache
5,1M	/home/dr/.hermes/models_dev_cache.json
3,9M	/home/dr/.hermes/state.db-wal
2,4M	/home/dr/.hermes/sessions

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 8.4 docker config (só estrutura, sem conteúdo de credenciais)

`ls -la /home/dr/.docker/ 2>/dev/null; echo ---; ls /home/dr/.docker/buildx 2>/dev/null | head`

```
total 16
drwx------  3 dr dr 4096 set  9 21:51 .
drwxr-x--- 24 dr dr 4096 out  7 02:27 ..
drwx------  6 dr dr 4096 set 24 02:37 buildx
-rw-------  1 dr dr   74 set 24 02:37 .token_seed
-rw-------  1 dr dr    0 set  9 21:51 .token_seed.lock
---
activity
current
defaults
instances
refs

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 8.5 .npm e .cache/pip

`timeout 40 du -xsh /home/dr/.npm/_cacache /home/dr/.cache/pip 2>/dev/null`

```
378M	/home/dr/.npm/_cacache
162M	/home/dr/.cache/pip

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 8.6 .claude.json e .claude — tipos e datas

`ls -la /home/dr/.claude.json /home/dr/.claude/ 2>/dev/null; file /home/dr/.claude.json 2>/dev/null`

```
-rw------- 1 dr dr 52546 out  7 02:27 /home/dr/.claude.json

/home/dr/.claude/:
total 20
drwx------  4 dr   dr   4096 out  7 02:27 .
drwxr-x--- 24 dr   dr   4096 out  7 02:27 ..
drwx------  2 dr   dr   4096 out  4 16:20 sessions
-rw-rw-r--  1 dr   dr    420 out  7 02:27 settings.json
drwxr-xr-x  2 root root 4096 out  4 16:33 skills
/home/dr/.claude.json: JSON text data

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 8.7 poolside e codex: state em .local/state — correspondência com dotdirs

`ls -la /home/dr/.poolside/ /home/dr/.local/state/poolside/ 2>/dev/null | head -12`

```
/home/dr/.local/state/poolside/:
total 20
drwxr-xr-x  5 dr dr 4096 set  7 19:56 .
drwx------ 14 dr dr 4096 set 24 22:07 ..
drwxr-xr-x  4 dr dr 4096 set  7 19:56 pool
drwxr-xr-x  2 dr dr 4096 out  4 19:25 sessions
drwxr-xr-x  2 dr dr 4096 out  4 19:26 trajectories

/home/dr/.poolside/:
total 12
drwx------  2 dr dr 4096 out  4 13:05 .
drwxr-x--- 24 dr dr 4096 out  7 02:27 ..

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 8.8 google-chrome: 3,9G de profile em .config

`timeout 60 du -xsh /home/dr/.config/google-chrome/* 2>/dev/null | sort -rh | head -6`

```
3,6G	/home/dr/.config/google-chrome/Default
81M	/home/dr/.config/google-chrome/extensions_crx_cache
45M	/home/dr/.config/google-chrome/optimization_guide_model_store
28M	/home/dr/.config/google-chrome/component_crx_cache
23M	/home/dr/.config/google-chrome/WasmTtsEngine
22M	/home/dr/.config/google-chrome/Safe Browsing

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 9.1 Claude Code: docs de reloc de env (só head)

`grep -rn -m1 'XDG_CONFIG_HOME\|CLAUDE_CONFIG_DIR' /home/dr/.local/lib/node_modules/9router/node_modules 2>/dev/null | head -3`

```
[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 9.2 flatpak remotes + tamanho /var/lib/flatpak

`flatpak remotes 2>&1; echo ---; timeout 40 sudo -n du -xsh /var/lib/flatpak 2>&1 | tail -1; du -xsh /home/dr/.local/share/flatpak 2>/dev/null`

```
flathub	system
---
sudo: uma senha é necessária
64K	/home/dr/.local/share/flatpak

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 9.3 vaults/celebro nível 2

`timeout 40 du -xsh /home/dr/vaults/celebro/* 2>/dev/null | sort -rh | head -8`

```
154M	/home/dr/vaults/celebro/002-DEV-IA
15M	/home/dr/vaults/celebro/003-MEDICINA
4,9M	/home/dr/vaults/celebro/001-ADMINISTRATIVO
664K	/home/dr/vaults/celebro/004-IA-LEARNING
8,0K	/home/dr/vaults/celebro/MAPA-DO-TIJOLAO.md

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 9.4 pnpm store 2,2G — onde

`timeout 40 du -xsh /home/dr/.local/share/pnpm/* 2>/dev/null | sort -rh | head -8`

```
2,2G	/home/dr/.local/share/pnpm/store
4,0K	/home/dr/.local/share/pnpm/bin

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 9.5 zed 1,8G — breakdown

`timeout 40 du -xsh /home/dr/.local/share/zed/* 2>/dev/null | sort -rh | head -6`

```
518M	/home/dr/.local/share/zed/copilot
464M	/home/dr/.local/share/zed/languages
406M	/home/dr/.local/share/zed/extensions
294M	/home/dr/.local/share/zed/external_agents
83M	/home/dr/.local/share/zed/node
9,7M	/home/dr/.local/share/zed/prettier

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 9.6 nvm 3,6G — breakdown

`timeout 60 du -xsh /home/dr/.local/share/nvm/versions/node/* 2>/dev/null | sort -rh`

```
3,6G	/home/dr/.local/share/nvm/versions/node/v24.16.0

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 9.7 zed.app/jdk fora do XDG em .local raiz

`ls -d /home/dr/.local/* | head -20; echo ---; stat -c '%U %n' /home/dr/.local/zed.app /home/dr/.local/jdk-25 /home/dr/.local/qpdf-root`

```
/home/dr/.local/bin
/home/dr/.local/jdk-25
/home/dr/.local/lib
/home/dr/.local/qpdf-root
/home/dr/.local/secrets
/home/dr/.local/share
/home/dr/.local/state
/home/dr/.local/zed.app
---
dr /home/dr/.local/zed.app
dr /home/dr/.local/jdk-25
dr /home/dr/.local/qpdf-root

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 10.1 .config/Claude e .config/Claude-3p vs ~/.claude — duplicatas do Claude Code?

`timeout 40 du -xsh /home/dr/.config/Claude/* 2>/dev/null | sort -rh | head -6; echo ---; ls /home/dr/.config/Claude /home/dr/.config/Claude-3p 2>/dev/null`

```
223M	/home/dr/.config/Claude/claude-code
78M	/home/dr/.config/Claude/Cache
43M	/home/dr/.config/Claude/Code Cache
12M	/home/dr/.config/Claude/Partitions
8,5M	/home/dr/.config/Claude/local-agent-mode-sessions
4,4M	/home/dr/.config/Claude/IndexedDB
---
/home/dr/.config/Claude:
ant-device-registry.json
ant-did
blob_storage
buddy-tokens.json
ca-bundle.pem
Cache
chrome-import-sites.json
claude-code
claude-code-sessions
claude_desktop_config.json
Code Cache
config.json
Cookies
Cookies-journal
cowork-enabled-cli-ops.json
Crashpad
DawnGraphiteCache
DawnWebGPUCache
declarative_performance_observer.db
declarative_performance_observer.db-journal
Dictionaries
DIPS
extensions-blocklist.json
fcache
git-shadow
git-worktrees.json
GPUCache
IndexedDB
local-agent-mode-sessions
Local State
Local Storage
logs
mcp-user-tool-toggles.json
Network Persistent State
os-entry-points.json
Partitions
plan-usage-history.json
Preferences
scratch-workspaces
sentry
Session Storage
Shared Dictionary
SharedStorage
SharedStorage-wal
spaces-present
TransportSecurity
Trust Tokens
Trust Tokens-journal
WebStorage
window-state.json

/home/dr/.config/Claude-3p:
ant-did
blob_storage
ca-bundle.pem
Cache
ccd-ids.json
claude-code
claude-code-sessions
claude_desktop_config.json
Claude Extensions Settings
Code Cache
config.json
configLibrary
Cookies
Cookies-journal
cowork-enabled-cli-ops.json
custom3p-mcp-schemas.json
DawnGraphiteCache
DawnWebGPUCache
declarative_performance_observer.db
declarative_performance_observer.db-journal
Dictionaries
DIPS
git-shadow
git-worktrees.json
GPUCache
IndexedDB
local-agent-mode-sessions
Local State
Local Storage
logs
mcp-user-tool-toggles.json
model-catalog
Network Persistent State
Preferences
Session Storage
Shared Dictionary
spaces-present
TransportSecurity
Trust Tokens
Trust Tokens-journal
WebStorage
window-state.json

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 10.2 n8n service / n8n service aponta pra onde?

`systemctl --user cat n8n.service 2>/dev/null | grep -E 'ExecStart|WorkingDirectory|Environment' | sed 's/=.*/=<...>/'; echo ---; timeout 30 du -xsh /home/dr/.local/share/n8n 2>/dev/null`

```
WorkingDirectory=<...>
EnvironmentFile=<...>
Environment=<...>
Environment=<...>
ExecStart=<...>
---
64M	/home/dr/.local/share/n8n

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 10.3 scripts dir de ~/src/scripts (o que tem)

`ls /home/dr/src/scripts/ 2>/dev/null; echo ---; ls /home/dr/src/scripts/*/ 2>/dev/null | head -20`

```
indices
nuvem
obsidian
pc
sasi
---
/home/dr/src/scripts/indices/:
build_claude_index.py
build_dev_index.py
build_sasi_index.py
push_repo_index_to_postgres.py
query_claude_index.py
query_dev_index.py
query_sasi_index.py

/home/dr/src/scripts/nuvem/:
arquivar.py
bin
liga-onedrive-no-pc.sh
onedrive-index

/home/dr/src/scripts/obsidian/:
check-obsidian-api.sh

/home/dr/src/scripts/pc/:
faxina_dev.py

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 10.4 systemd user units: WorkingDirectory de cada

`for u in 9router hermes-gateway hermes-dashboard n8n; do echo "== $u"; systemctl --user cat $u.service 2>/dev/null | grep -E 'ExecStart|WorkingDirectory'; done`

```
== 9router
ExecStart=/home/dr/.local/share/nvm/versions/node/v24.16.0/bin/node /home/dr/.local/lib/node_modules/9router/cli.js --no-browser --skip-update --log
WorkingDirectory=/home/dr/.local/share/9router
== hermes-gateway
ExecStart=/home/dr/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main gateway run
WorkingDirectory=/home/dr/.hermes
== hermes-dashboard
WorkingDirectory=/home/dr/.hermes
ExecStart=/home/dr/.hermes/hermes-agent/venv/bin/hermes dashboard --host 127.0.0.1 --port 9119 --no-open --skip-build
== n8n
WorkingDirectory=/home/dr/.local/share/n8n/.n8n
ExecStart=/home/dr/.local/share/nvm/versions/node/v24.16.0/bin/node /home/dr/.local/share/nvm/versions/node/v24.16.0/lib/node_modules/n8n/bin/n8n start

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 10.5 .npm/_npx e outros caches npm

`ls /home/dr/.npm 2>/dev/null; echo ---; timeout 30 du -xsh /home/dr/.npm/* 2>/dev/null | sort -rh | head -6`

```
_cacache
_logs
_npx
_update-notifier-last-checked
---
378M	/home/dr/.npm/_cacache
236M	/home/dr/.npm/_npx
88K	/home/dr/.npm/_logs
0	/home/dr/.npm/_update-notifier-last-checked

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 10.6 dpkg vs node/npm do apt (qual node o sistema usa)

`/usr/bin/node --version; dpkg -l nodejs 2>/dev/null | tail -1`

```
v18.19.1
ii  nodejs         18.19.1+dfsg-6ubuntu5 amd64        evented I/O for V8 javascript - runtime executable

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 11.1 .claude.json — só nomes de chaves top-level (jq keys, sem valores)

`jq -r 'keys[]' /home/dr/.claude.json 2>/dev/null | head -30`

```
additionalModelCostsCache
additionalModelOptionsAnsweredAt
additionalModelOptionsCache
announcementImpressions
autoCompactWindowsCache
autoModeEnvSetup
autoUpdates
autoUpdatesProtectedForNative
cachedExperimentData
cachedExperimentFeatures
cachedExtraUsageDisabledReason
cachedGrowthBookFeatures
cachedGrowthBookFeaturesAt
changelogLastFetched
claudeAiMcpEverConnected
clientDataCacheSlots
closedIssuesLastChecked
firstStartTime
firstStartVersion
groveConfigCache
hasCompletedOnboarding
hasResetAutoModeOptInForDefaultOffer
hasSeenAutoDefaultNotice
installMethod
lastClawdEntranceVersion
lastOnboardingVersion
lastReleaseNotesSeen
machineID
migrationVersion
modelAccessCache

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 11.2 sasi nested repos: branch/remote/dirty

`for r in /home/dr/src/sasi/AUTOMACAO-SASI /home/dr/src/sasi/SASI-V3; do b=$(git -C $r branch --show-current 2>/dev/null); rmt=$(git -C $r remote get-url origin 2>/dev/null || echo none); n=$(git -C $r status --porcelain 2>/dev/null | wc -l); echo "$r branch=$b remote=$rmt dirty=$n"; done`

```
/home/dr/src/sasi/AUTOMACAO-SASI branch=main remote=https://github.com/doutortenente/AUTOMACAO-SASI.git dirty=0
/home/dr/src/sasi/SASI-V3 branch=chore/bump-deps-e-gitignore remote=https://github.com/doutortenente/SASI-V3.git dirty=9

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 11.3 SASI-V3: o que pesa 1,1G

`timeout 60 du -xsh /home/dr/src/sasi/SASI-V3/* 2>/dev/null | sort -rh | head -8`

```
846M	/home/dr/src/sasi/SASI-V3/node_modules
31M	/home/dr/src/sasi/SASI-V3/memory
1,5M	/home/dr/src/sasi/SASI-V3/src
396K	/home/dr/src/sasi/SASI-V3/tsconfig.tsbuildinfo
312K	/home/dr/src/sasi/SASI-V3/supabase
276K	/home/dr/src/sasi/SASI-V3/pnpm-lock.yaml
32K	/home/dr/src/sasi/SASI-V3/tests
24K	/home/dr/src/sasi/SASI-V3/CLAUDE.md

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 11.4 hermes-workspace repo: branch tijolao

`git -C /home/dr/src/hermes-workspace status --porcelain 2>/dev/null | head -5; git -C /home/dr/src/hermes-workspace log --oneline -1 2>/dev/null`

```
b06dd7c4 tijolao: config da maquina sai do fork; ficam so os defeitos do app

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 11.5 tailscale/app dirs em .var

`ls /home/dr/.var/app/ 2>/dev/null`

```
com.bitwarden.desktop
io.github.shiftey.Desktop
md.obsidian.Obsidian
org.kde.kate
org.mozilla.firefox
org.telegram.desktop

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 11.6 downloads breakdown

`timeout 40 du -xsh /home/dr/Downloads/* 2>/dev/null | sort -rh | head -8`

```
68M	/home/dr/Downloads/DOCS-E-RASCUNHOS-PLANTOES

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 11.7 zed.app e jdk-25 — de quem são (versões)

`/home/dr/.local/zed.app/bin/zed --version 2>/dev/null | head -1; ls /home/dr/.local/jdk-25/bin | head -3; readlink -f /home/dr/.local/share/claude/versions/2.1.285 2>/dev/null`

```
Zed 1.22.0 76659a55a8c10ed355a070f8764a0b1733e3c115  – /home/dr/.local/zed.app/libexec/zed-editor
devrig
java
jfr
/home/dr/.local/share/claude/versions/2.1.285

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 12.1 symlinks na raiz e nível 2 da home

`find /home/dr -xdev -maxdepth 2 -type l -printf '%p -> %l\n' 2>/dev/null | grep -v '.hermes/home' | head -20`

```
/home/dr/.hermes/.env -> /home/dr/.local/secrets/.env

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 12.2 .git-credentials — meta apenas (perm, tam, não conteúdo)

`stat -c '%A %s %U %y' /home/dr/.git-credentials 2>/dev/null`

```
-rw------- 74 dr 2026-10-02 05:39:45.059863252 -0300

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 12.3 flatpak apps system — tamanho real /var/lib/flatpak (sem sudo, via du negado?)

`timeout 30 du -xsh /var/lib/flatpak 2>&1 | tail -1`

```
5,9G	/var/lib/flatpak

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 12.4 mintinstall cache 38M e mozilla 616M breakdown

`timeout 40 du -xsh /home/dr/.config/mozilla/* /home/dr/.cache/mintinstall/* 2>/dev/null | sort -rh | head -8`

```
616M	/home/dr/.config/mozilla/firefox
24M	/home/dr/.cache/mintinstall/reviews.json
15M	/home/dr/.cache/mintinstall/pkginfo.json
4,0K	/home/dr/.cache/mintinstall/screenshots

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 12.5 poolside-cli? pool em .local/bin — o que é

`file /home/dr/.local/bin/pool 2>/dev/null; head -c 200 /home/dr/.local/bin/pool 2>/dev/null | strings | head -3`

```
/home/dr/.local/bin/pool: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, Go BuildID=redacted, BuildID[sha1]=498919aff001d8366249403a2544fba2d833084f, stripped

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 12.6 tijolao e qpdf em .local/bin — que scripts são

`file /home/dr/.local/bin/tijolao /home/dr/.local/bin/qpdf /home/dr/.local/bin/hermes 2>/dev/null; head -2 /home/dr/.local/bin/tijolao 2>/dev/null`

```
/home/dr/.local/bin/tijolao: Bourne-Again shell script, ASCII text executable
/home/dr/.local/bin/qpdf:    POSIX shell script, ASCII text executable
/home/dr/.local/bin/hermes:  Bourne-Again shell script, ASCII text executable
#!/usr/bin/env bash
exec /home/dr/src/tijolao-ai/hermes-stack/tijolao.sh "$@"

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 13.1 /usr/local/lib/node_modules (sudo-installs)

`ls /usr/local/lib/node_modules/ 2>/dev/null; timeout 40 du -xsh /usr/local/lib/node_modules/* 2>/dev/null`

```
9remote
better-sqlite3
sql.js
systray2
137M	/usr/local/lib/node_modules/9remote
29M	/usr/local/lib/node_modules/better-sqlite3
19M	/usr/local/lib/node_modules/sql.js
12M	/usr/local/lib/node_modules/systray2

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 13.2 cloudflared é do apt?

`dpkg -S /usr/bin/cloudflared 2>&1; /usr/bin/cloudflared --version 2>&1 | head -1`

```
cloudflared: /usr/bin/cloudflared
cloudflared version 2026.9.3 (built 2026-09-24-16:07 UTC)

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 13.3 Claude Code aceita CLAUDE_CONFIG_DIR? (grep no binário)

`grep -c 'CLAUDE_CONFIG_DIR' /home/dr/.local/share/claude/versions/2.1.285 2>/dev/null`

```
50

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 13.4 Codex aceita CODEX_HOME? (grep no cli.js)

`grep -c 'CODEX_HOME' /home/dr/.local/lib/node_modules/@openai/codex/bin/codex.js 2>/dev/null; grep -rl 'CODEX_HOME' /home/dr/.local/lib/node_modules/@openai/codex/ 2>/dev/null | head -3`

```
0
/home/dr/.local/lib/node_modules/@openai/codex/node_modules/@openai/codex-linux-x64/vendor/x86_64-unknown-linux-musl/bin/codex

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 13.5 9router: hardcoded ~/.9router? (sem cat de segredos)

`grep -o 'NINEROUTER[A-Z_]*\|\.9router\|XDG_[A-Z_]*' /home/dr/.local/lib/node_modules/9router/cli.js 2>/dev/null | sort | uniq -c | sort -rn | head -8`

```
3 .9router

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 13.6 pool (poolside) — strings de env

`strings /home/dr/.local/bin/pool 2>/dev/null | grep -E '^POOLSIDE|HOME|XDG' | head -10`

```
$HOME
8XDG_
POOLSIDEH90u,
POOLSIDEH90u/
Gonetcp6waitreadseek/tmpHOMEopenstatsynclink*?[\trimrpad%s%s    	%v
mkdirservedebugFlagslogintokenhttpslocalforcelinuxamd64%s/%slevel%s=%safter<nil>arrayfalseErrorsvqxXInt64Group%s:%d\u202DEBUGERROR&amp;&#34;&#39;:***@%d %sbytesRangeclose:pathHTTP1HTTP2%s %qAllow:http%s-%dsocksFoundchdirwrite$HOMEchmodlstatchowngetwdpipe2  [P]  [L]
%saudio/speechthreads/runsstring_checkimages/edits%s read (%s)-LiteralPath--admin-bindhttp://%s:%dcontainer_id/checkpointspartial_json/v0/messages [TRUNCATED]/tmp/plan.mdstay-in-planrunning '%s'exit code %dcommand '%s'user_messagelocal_searchdependenciestest_resultsXDG_BIN_HOMEapplicationsoperationRefexternalDocspropertyNameprompts/list%q before %qRCodeSuccessRCodeRefused{"not":true}%d questionscustom inputword forwardFetched fromThought for  (%s tokens)  No matchesenter select(unanswered)enter submitenter rewindenter deletespace selectenter resumeinvalid runemediareverse
]777;notify;XDG_DATA_HOMEXDG_DATA_DIRSXDG_MUSIC_DIRexternalValueallowReservedminPropertiesmaxPropertiesdiscriminator[DEBUG] %s %sprogressTokenLast-Event-IDPOST 
Manage secrets.pool-update-*Content-LengthPROTOCOL_ERRORINTERNAL_ERRORREFUSED_STREAMMAX_FRAME_SIZEERR_UNKNOWN_%dfirst_settingsping_on_streamtrailers_boguscontent-lengthread_frame_eof{$} not at endempty wildcardinvalid methodinternal errorPRI * HTTP/2.0parsing %q: %wunknown error unknown code: Not AcceptableCloseWrite: %whttptest.serve (core dumped)/proc/self/exeXDG_CACHE_HOMEtrimRightSpacehelp [command]%s version %s
[^a-zA-Z0-9_-]shell-python-1aws_cloudfrontopenai_api_keygoogle_api_keygeneric_bearerbranch_commitsschema_versionCLICOLOR_FORCEDefaultAppName--passivepopupXDG_STATE_HOMEuser-dirs.dirsXDG_VIDEOS_DIRinvalid headerrequest failedresources/listresources/readnil connectionnotifications/Mcp-Session-Idcalling %q: %wcalling %s: %v<url>%s</url>

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 13.7 Trash top por tamanho

`timeout 40 du -xsh /home/dr/.local/share/Trash/files/* 2>/dev/null | sort -rh | head -8`

```
825M	/home/dr/.local/share/Trash/files/google-chrome
656M	/home/dr/.local/share/Trash/files/puppeteer
143M	/home/dr/.local/share/Trash/files/mozilla
23M	/home/dr/.local/share/Trash/files/mesa_shader_cache
11M	/home/dr/.local/share/Trash/files/icon-cache.kcache
8,5M	/home/dr/.local/share/Trash/files/pkg
7,5M	/home/dr/.local/share/Trash/files/flatpak
5,4M	/home/dr/.local/share/Trash/files/thumbnails

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 13.8 .local/share/claude breakdown

`timeout 40 du -xsh /home/dr/.local/share/claude/* 2>/dev/null | sort -rh | head -8`

```
450M	/home/dr/.local/share/claude/versions

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 14.1 CODEX_HOME no binário rust do codex

`strings /home/dr/.local/lib/node_modules/@openai/codex/node_modules/@openai/codex-linux-x64/vendor/x86_64-unknown-linux-musl/bin/codex 2>/dev/null | grep -c 'CODEX_HOME'`

```
70

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 14.2 shells e dotfiles de shell restantes

`ls -la /home/dr/.zshrc /home/dr/.zprofile /home/dr/.bash_aliases 2>&1; echo ---; getent passwd dr`

```
ls: não foi possível acessar '/home/dr/.zshrc': Arquivo ou diretório inexistente
ls: não foi possível acessar '/home/dr/.zprofile': Arquivo ou diretório inexistente
ls: não foi possível acessar '/home/dr/.bash_aliases': Arquivo ou diretório inexistente
---
dr:x:1000:1000:Dr. Tenente ,,,:/home/dr:/bin/bash

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 14.3 npm config: cache prefix (onde npm acha que vive)

`npm config get cache prefix 2>/dev/null; echo ---; cat /home/dr/.npmrc 2>/dev/null || echo 'sem ~/.npmrc'`

```
cache=/home/dr/.npm
prefix=/home/dr/.local/share/nvm/versions/node/v24.16.0
---
sem ~/.npmrc

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 14.4 pastas vazias relevantes nível 2 (config e local)

`find /home/dr/.config /home/dr/.local -xdev -maxdepth 2 -type d -empty 2>/dev/null | head -15`

```
/home/dr/.config/Claude-3p/Claude Extensions Settings
/home/dr/.config/cinnamon-session/saved-session
/home/dr/.config/btop/themes
/home/dr/.config/Codex/Safe Browsing
/home/dr/.config/Codex/NativeMessagingHosts
/home/dr/.config/Codex/PrivacySandboxAttestationsPreloaded
/home/dr/.config/Codex/OriginTrials
/home/dr/.config/google-chrome/Local Traces
/home/dr/.config/google-chrome/Webstore Downloads
/home/dr/.config/google-chrome/DeferredBrowserMetrics
/home/dr/.config/google-chrome/PrivacySandboxAttestationsPreloaded
/home/dr/.config/google-chrome/OriginTrials
/home/dr/.config/copyq/themes
/home/dr/.config/Claude/git-shadow
/home/dr/.config/zed/themes

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 14.5 vaults/celebro — é repo git?

`git -C /home/dr/vaults/celebro rev-parse --git-dir 2>&1 | head -1; ls -a /home/dr/vaults/celebro | head -8`

```
.git
.
..
001-ADMINISTRATIVO
002-DEV-IA
003-MEDICINA
004-IA-LEARNING
.git
.gitignore

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 14.6 Documentos em vaults — realocado pelo user-dirs, apps respeitam?

`ls /home/dr/vaults/Documentos/ 2>/dev/null | head -8`

```
Documentos-cadastro-dr-nicholas
EXTRACAO-CLINICA-SASI.zip
Plantões
Tijolao

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 14.7 hermes-workspace: o que é (levemente)

`ls /home/dr/src/hermes-workspace/ 2>/dev/null | head -15`

```
agents
AGENTS.md
assets
CHANGELOG.md
CONTRIBUTING.md
docker
docker-compose.dev.yml
docker-compose.yml
Dockerfile
eslint.config.js
LICENSE
package.json
pnpm-lock.yaml
pnpm-workspace.yaml
prettier.config.js

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 15.1 .profile completo

`cat /home/dr/.profile`

```
. "$HOME/.local/bin/env"

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 15.2 .config/git e .config/gh conteúdo (só nomes)

`ls -la /home/dr/.config/git/ /home/dr/.config/gh/ 2>/dev/null`

```
/home/dr/.config/gh/:
total 16
drwxrwx--x  2 dr dr 4096 jun  6 15:22 .
drwx------ 42 dr dr 4096 out  2 20:50 ..
-rw-------  1 dr dr 1657 jun  6 15:22 config.yml
-rw-------  1 dr dr   70 ago 11 02:38 hosts.yml

/home/dr/.config/git/:
total 16
drwxrwxr-x  2 dr dr 4096 set  7 10:12 .
drwx------ 42 dr dr 4096 out  2 20:50 ..
-rw-rw-r--  1 dr dr  512 set  7 10:12 config
-rw-rw-r--  1 dr dr  364 jul 24 00:25 ignore

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 15.3 gitconfig global onde?

`git config --global --list --show-origin 2>/dev/null | awk -F'\t' '{print $1}' | sort -u | head; echo ---; ls -la /home/dr/.gitconfig 2>&1`

```
file:/home/dr/.config/git/config
---
ls: não foi possível acessar '/home/dr/.gitconfig': Arquivo ou diretório inexistente

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 15.4 Claude vs Claude-3p: datas de criação/instâncias

`stat -c '%y %n' /home/dr/.config/Claude /home/dr/.config/Claude-3p /home/dr/.config/Codex 2>/dev/null`

```
2026-10-02 01:22:30.459564000 -0300 /home/dr/.config/Claude
2026-10-02 08:11:41.667889754 -0300 /home/dr/.config/Claude-3p
2026-09-29 03:01:15.816554811 -0300 /home/dr/.config/Codex

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

## 15.5 hermes-workspace docker-compose montagens (só caminhos)

`grep -E 'volumes|/home/dr' /home/dr/src/hermes-workspace/docker-compose.yml 2>/dev/null | head -15`

```
#   Both volumes survive container recreation and `docker compose down`.
    volumes:
    volumes:
volumes:

[stderr]  'localhost' (ED25519) to the list of known hosts.
```

---
# RESUMO ESTRUTURADO (top achados)

## Dimensões da home (nível 1)
| pasta | tamanho | dono | padrão Unix/XDG |
|---|---|---|---|
| .local | 12G | dr | OK (~/.local/bin,lib,share,state corretos; zed.app/jdk-25/qpdf-root soltos na raiz de .local — não são subpastas XDG) |
| .config | 5,2G | dr | OK em estrutura (peso é profile Chrome 3,9G) |
| .hermes | 1,9G | dr | convenção do app (hermes-agent); aceita HERMES_HOME |
| src | 1,4G | dr | OK — layout pessoal recomendado (código-fonte fora do XDG é aceitável; FHS não define ~/src, mas é o padrão de fato do usuário) |
| .cache | 787M | dr | OK |
| .npm | 613M | dr | FORA — npm cache deveria estar sob XDG_CACHE_HOME (npm usa ~/.npm hardcoded; reloc: `npm config set cache ~/.cache/npm`) |
| .var | 322M | dr | OK — .var/app É o padrão XDG para flatpak |
| vaults | 368M | dr | XDG_DOCUMENTS_DIR aponta para cá (vaults/Documentos) |
| Downloads | 68M | dr | OK (XDG_DOWNLOAD_DIR) |
| Imagens | 2,3M | dr | OK (XDG_PICTURES_DIR) |
| .9router | 31M | dr | FORA — dados de app (db/auth/logs/runtime); o mesmo app também grava em .local/share/9router (DUPLICATA funcional) |
| .themes | 2,1M | dr | FORA — XDG_DATA_HOME/themes é o lugar padrão (~/.local/share/themes) |
| backups | 0 | dr | vazio desde 02-out |
| Área de trabalho | 4K | dr | OK (XDG_DESKTOP_DIR) |

## Conclusões principais
1. XDG básico OK: user-dirs.dirs pt-BR presente; Desktop/Downloads/Imagens existem; Documentos apontado para ~/vaults/Documentos; Modelos/Público/Música/Vídeos apontam para $HOME (desativados, nunca criados).
2. Node está duplicado: /usr/bin/node v18.19.1 (apt) + nvm v24.16.0 em ~/.local/share/nvm (3,6G). Tudo de prod (9router, n8n, claude, codex) usa o nvm.
3. 9router tem dados em DOIS lugares: ~/.9router (31M, db/auth/logs) e ~/.local/share/9router (74M, runtime/bin/db). Ambos ativos — WorkingDirectory do service é .local/share/9router.
4. npm grava cache em ~/.npm (613M, sendo 378M _cacache + 236M _npx) — sem ~/.npmrc; aceita reloc via `npm config set cache`.
5. 7,2G recuperáveis em caches/lixo: Trash 1,7G (google-chrome 825M, puppeteer 656M), .npm 613M, pip cache 162M, pnpm store 2,2G (reatribuível), nvm node_modules dupes.
6. Instalações fora do padrão no sistema: /usr/local/lib/node_modules/{9remote,better-sqlite3,sql.js,systray2} (197M, instaladas com sudo via npm, dpkg não conhece); /usr/local/bin/9remote e cloudflared symlink; /opt só tem containerd+google (apt/padrão).
7. ~/.local/share/zed = 1,8G (copilot 518M, languages 464M, extensions 406M) e .local/zed.app 313M — app instalado dentro de .local (Zed instala ali por padrão).
8. .config/Claude (379M) e .config/Claude-3p (254M) = DUAS instâncias do app desktop Claude (profile e profile de 3º); ~/.claude (CLI) + ~/.claude.json separados; CLI aceita CLAUDE_CONFIG_DIR (50 refs no binário).
9. Codex: ~/.codex (config.toml) + .config/Codex (133M, profile desktop Electron) + .local/state/{codex,openai-codex} (2 pastas de state!) — 4 locais; CODEX_HOME suportado (70 refs no binário rust).
10. .claude/skills é o ÚNICO item dono root dentro da home (montado :ro no container por design; o app do host lê).
11. flatpak system: 5,9G em /var/lib/flatpak (Bitwarden, Obsidian, Telegram...), dados de apps em ~/.var/app (322M) — correto XDG.
12. Lixeira 1,7G — nunca esvaziada desde 23-25/09.
13. sudo -n NEGADO — checagens que exigem root ficaram limitadas (ex.: dono de /var/lib/flatpak, dpkg -S completo).
14. SASI descontinuado ainda ocupa 1,1G em ~/src/sasi (node_modules 846M) com 2 repos aninhados (AUTOMACAO-SASI main clean; SASI-V3 chore/bump-deps-e-gitignore dirty=9).
15. Scripts distribuídos: ~/src/scripts (repo), wrappers em ~/.local/bin (tijolao→~/src/tijolao-ai, hermes→.hermes), rclone binário em ~/src/scripts/nuvem/bin (fora de .local/bin).
