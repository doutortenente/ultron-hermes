# Auditoria C — Camada de sistema e integridade de referências do Tijolão
# Data: 07-out-2026 ~03:15 -03 (host: Tijolao, Linux Mint 22.3, kernel 7.0.0-38-generic, up 1:47)
# Modo: SOMENTE LEITURA. Coleta via SSH dr@localhost a partir do container hermes-agent.
# sudo -n: NEGADO ('sudo: uma senha é necessária') — portas/proc de processos root ficaram sem dono identificável.
# Fatos base (medidos): 9router.service user-enabled+active; node v24.16.0 em ~/.local/share/nvm; nenhuma unidade failed.


## RESUMO EXECUTIVO (ver detalhes nas seções abaixo)

### systemd --user (~/.config/systemd/user/)
- 4 units: 9router.service (enabled+active, ExecStart/WorkDir existem), hermes-dashboard.service (disabled+inactive),
  hermes-gateway.service (disabled+inactive), n8n.service (disabled+inactive, todos os caminhos existem).
- Nenhuma unit failed; nenhuma unit fantasma/órfã do operador; drop-in órfão de SISTEMA: /etc/systemd/system/ollama.service.d/override.conf (ollama removido, unit not-found).
- hermes-dashboard/hermes-gateway user units referenciam /home/dr/.hermes/hermes-agent/venv/bin/* que NÃO existe mais (instalação .hermes/hermes-agent antiga) — estavam disabled, inofensivas, mas com caminhos mortos.

### systemd sistema (fora de pacote)
- cloudflared.service (enabled+active, /usr/bin/cloudflared + token OK), cloudflared-update.service + cloudflared-update.timer (disabled).
- Override do operador em ollama.service.d (órfão). drop-ins de pacote: alloy.service.d/env.conf (root-only, não legível).

### cron
- crontab -l do dr: 'no crontab for dr'. /etc/cron.d: só pacotes (anacron, e2scrub_all, sysstat). Timers: só padrão do sistema + launchpadlib-cache-clean.timer (user). Hermes cron interno: ~/.hermes/cron/executions.db (banco SQLite de execuções, heartbeat ativo).

### autostart
- ~/.config/autostart/9router.desktop: Exec aponta para /home/dr/.config/nvm/... (nvm ANTIGO) — CAMINHO MORTO (node não existe lá). O 9router real sobe via systemd unit; este autostart duplicado/quebrado falha em silêncio a cada login.
- Demais entradas OK (blueman, bitwarden flatpak, copyq desabilitado, mintupdate, mintreport, print-applet/xapp/cinnamon-stats desabilitados com Hidden=true).

### portas (ss -tlnp)
22 sshd (root) | 53 resolved | 443+10000 tailscale serve/funnel (https://tijolao.tail9e88c5.ts.net → 9router UI 20128 e portal 3000) | 631 cups | 3000 node server-entry.js (hermes-workspace, container) | 5432 postgres | 8642 hermes gateway API | 9119 hermes dashboard | 20128 9router UI (next-server, 0.0.0.0) | 20241/20242 metrics cloudflared | 45351 HTTP root não identificado (404 'Page Not Found') | 54584/62838 internas tailscale.

### PATH e duplicatas
- PATH efetivo (login e interativo): ~/.local/bin : ~/.local/share/nvm/versions/node/v24.16.0/bin : sistema. .bashrc carrega nvm (NVM_DIR=~/.local/share/nvm); .profile carrega ~/.local/bin/env.
- SSH herda NVM_BIN/NVM_INC/PATH com nvm no ambiente da sessão (origem: environment herdado do ssh via systemd; não determinável sem root).
- Duplicatas: node v24.16.0 (nvm, vence) vs v18.19.1 (apt) | npm 11.16.0 (nvm) vs 9.2.0 (apt) | rclone 1.75.1 (~/.local/bin → ~/src/scripts/nuvem/bin/rclone, vence) vs 1.60.1-DEV (apt) | pnpm 11.20.0 (~/.local/bin → ~/.local/lib/node_modules, vence) | cloudflared: /usr/local/bin/cloudflared (symlink → /usr/bin, apt 2026.9.3), cloudflared.service usa /usr/bin (2026.8.3 apt?? versão metrics difere do binário) e 9router usa cópia própria ~/.local/share/9router/bin/cloudflared (2026.9.3).
- ~/.config/nvm: NÃO existe (limpo). npm prefix = ~/.local/share/nvm/versions/node/v24.16.0 (globais do npm caem no nvm/lib/node_modules, NÃO no ~/.local/lib/node_modules onde 9router/pnpm/codex/ctx7/tokentracker foram instalados com --prefix ~/.local — dois conjuntos globais divergentes).
- 9remote 2.5.8 instalado com sudo em /usr/local/lib/node_modules (root) + /usr/local/bin/9remote — resquício de instalação global sudo (mesma origem da duplicata do 9router apagada em 02-out).

### referências mortas (grep ~/...)
- ~/.bashrc, ~/.profile, ~/.config/systemd/user, ~/.local/bin, /home/dr/.hermes/config.yaml, profiles/*/config.yaml, ~/.hermes/cron: NENHUMA referência a /home/dr/projetos, .config/nvm, hermes-workspace, cofre.env, sasi, EXTRACAO.
- ~/src/tijolao-ai: services/hermes-workspace.service (unit antiga com WorkingDirectory=/home/dr/projetos/hermes-workspace e ExecStart /home/dr/.hermes/node/bin/node — AMBOS MORTOS; unit não instalada em nenhum dir systemd); scripts/verify-stack.sh lê /home/dr/projetos/hermes-workspace/.env (morto); hermes-stack/AGENTS.md + swarm.yaml mencionam SASI (descritivo, não executável).
- ~/.local/share/applications/claude-code-url-handler.desktop: Exec com aspas quebra validação simples, mas alvo /home/dr/.local/bin/claude existe (OK real).
- docker-compose.tijolao.yml: comentários referenciam o layout novo (~/.local/secrets), sem refs a ~/projetos.

### symlinks quebrados (find ~ -xdev -xtype l, excl. .cache/node_modules/.git/Trash)
- /home/dr/vaults/celebro/002-DEV-IA/arquivos-sasi/SASI_Copia_Repositorio_GH/.env → ../.env (inexistente)
- /home/dr/.local/share/pnpm/store/v11/projects/b8d7b298... → ../../../../../../projetos/SASI-V3 (~/projetos morto)
- /home/dr/.hermes/home/.config/pulse/Tijolao-runtime → /tmp/pulse-PKdhtXMmr18n (runtime antigo, inofensivo)
- /home/dr/.local/jdk-25/bin/devrig → /home/dr/.mcp-steroid/bin/devrig (inexistente)
- /home/dr/.local/qpdf-root/usr/share/doc/qpdf/changelog.Debian.gz → ../libqpdf29t64/... (inexistente)
- (+ locks de runtime: SingletonLock/Cookie/Socket de Chrome/Firefox/Codex/Bitwarden — normais de apps fechados)


---

# EVIDÊNCIA BRUTA (comando + saída por checagem)

## [b0_hostinfo]
**Comando:** `hostname; echo ---; uname -a; echo ---; date; echo ---; uptime; echo ---; id; echo ---; ls -la ~ | head -40`

```
Tijolao
---
Linux Tijolao 7.0.0-38-generic #38~24.04.4-Ubuntu SMP PREEMPT_DYNAMIC Mon Sep 14 16:37:11 UTC 2 x86_64 x86_64 x86_64 GNU/Linux
---
qua 07 out 2026 03:13:32 -03
---
 03:13:32 up  1:47,  2 users,  load average: 0,10, 0,13, 0,12
---
uid=1000(dr) gid=1000(dr) grupos=1000(dr),0(root),1(daemon),2(bin),3(sys),4(adm),6(disk),13(proxy),20(dialout),21(fax),24(cdrom),25(floppy),26(tape),27(sudo),29(audio),30(dip),44(video),46(plugdev),100(users),102(syslog),105(lpadmin),108(_s
---
total 204
drwxr-x--- 24 dr   dr    4096 out  7 02:27 .
drwxr-xr-x  3 root root  4096 jun  5 19:29 ..
drwxrwxr-x  6 dr   dr    4096 set 23 23:31 .9router
drwxr-xr-x  2 dr   dr    4096 out  4 16:15 Área de trabalho
drwxrwxr-x  2 dr   dr    4096 out  2 16:59 backups
-rw-------  1 dr   dr    1051 out  7 02:30 .bash_history
-rw-rw-r--  1 dr   dr     281 out  4 10:56 .bashrc
drwxr-xr-x 17 dr   dr    4096 out  7 02:45 .cache
drwx------  4 dr   dr    4096 out  7 02:27 .claude
-rw-------  1 dr   dr   52546 out  7 02:27 .claude.json
drwxrwxr-x  2 dr   dr    4096 out  7 02:27 .codex
drwx------ 42 dr   dr    4096 out  2 20:50 .config
drwx------  3 dr   dr    4096 set  9 21:51 .docker
drwxr-xr-x  3 dr   dr    4096 out  7 02:25 Downloads
-rw-------  1 dr   dr      74 out  2 05:39 .git-credentials
drwx------  3 dr   dr    4096 set  9 21:16 .gnome
-rw-rw-r--  1 dr   dr     245 out  1 20:00 .gtkrc-2.0
drwx------ 45 dr   dr    4096 out  7 03:12 .hermes
drwxr-xr-x  3 dr   dr    4096 out  4 16:13 Imagens
drwxrwxrwx  3 dr   dr    4096 out  7 01:13 .linuxmint
drwx------ 10 dr   dr    4096 set  7 08:21 .local
drwxrwxr-x  5 dr   dr    4096 out  4 08:26 .npm
drwx------  3 dr   dr    4096 jul 25 18:53 .pki
drwx------  2 dr   dr    4096 out  4 13:05 .poolside
-rw-rw-r--  1 dr   dr      26 set  9 12:47 .profile
drwxrwxr-x  8 dr   dr    4096 out  2 21:31 src
drwx------  2 dr   dr    4096 set 23 17:41 .ssh
-rw-r--r--  1 dr   dr       0 set  8 00:21 .sudo_as_admin_successful
drwxrwxr-x  3 dr   dr    4096 set 27 01:12 .themes
drwxr-xr-x  3 dr   dr    4096 ago  9 16:21 .var
drwxrwxr-x  4 dr   dr    4096 out  2 20:50 vaults
-rw-------  1 dr   dr      52 out  7 01:26 .Xauthority
-rw-------  1 dr   dr   14453 out  7 02:29 .xsession-errors
-rw-------  1 dr   dr   15930 out  7 01:25 .xsession-errors.old
```

## [b0_sudo]
**Comando:** `sudo -n true 2>&1; echo "sudo_rc=$?"`

```
sudo: uma senha é necessária
sudo_rc=1
```

## [s1_ls_unitdir]
**Comando:** `find ~/.config/systemd/user -maxdepth 3 \( -type f -o -type l \) -printf '%y %p -> %l\n' 2>&1 | sort | head -60`

```
f /home/dr/.config/systemd/user/9router.service -> 
f /home/dr/.config/systemd/user/hermes-dashboard.service -> 
f /home/dr/.config/systemd/user/hermes-gateway.service -> 
f /home/dr/.config/systemd/user/n8n.service -> 
l /home/dr/.config/systemd/user/default.target.wants/9router.service -> /home/dr/.config/systemd/user/9router.service
```

## [s1_list_unit_files]
**Comando:** `export XDG_RUNTIME_DIR=/run/user/$(id -u); systemctl --user list-unit-files --no-pager --no-legend 2>&1`

```
app-com.google.Chrome-6332.scope                                               transient -
app-flatpak-com.bitwarden.desktop-2270.scope                                   transient -
app-flatpak-com.bitwarden.desktop-2564.scope                                   transient -
vte-spawn-d9e7143d-4931-40b1-9dda-9aaea1f2812f.scope                           transient -
9router.service                                                                enabled   enabled
app-at\x2dspi\x2ddbus\x2dbus@autostart.service                                 generated -
app-cinnamon\x2dsettings\x2ddaemon\x2da11y\x2dsettings@autostart.service       generated -
app-cinnamon\x2dsettings\x2ddaemon\x2dautomount@autostart.service              generated -
app-cinnamon\x2dsettings\x2ddaemon\x2dbackground@autostart.service             generated -
app-cinnamon\x2dsettings\x2ddaemon\x2dclipboard@autostart.service              generated -
app-cinnamon\x2dsettings\x2ddaemon\x2dcolor@autostart.service                  generated -
app-cinnamon\x2dsettings\x2ddaemon\x2dhousekeeping@autostart.service           generated -
app-cinnamon\x2dsettings\x2ddaemon\x2dkeyboard@autostart.service               generated -
app-cinnamon\x2dsettings\x2ddaemon\x2dmedia\x2dkeys@autostart.service          generated -
app-cinnamon\x2dsettings\x2ddaemon\x2dpower@autostart.service                  generated -
app-cinnamon\x2dsettings\x2ddaemon\x2dprint\x2dnotifications@autostart.service generated -
app-cinnamon\x2dsettings\x2ddaemon\x2dscreensaver\x2dproxy@autostart.service   generated -
app-cinnamon\x2dsettings\x2ddaemon\x2dsettings\x2dremap@autostart.service      generated -
app-cinnamon\x2dsettings\x2ddaemon\x2dsmartcard@autostart.service              generated -
app-cinnamon\x2dsettings\x2ddaemon\x2dwacom@autostart.service                  generated -
app-cinnamon\x2dsettings\x2ddaemon\x2dxsettings@autostart.service              generated -
app-com.bitwarden.desktop@autostart.service                                    generated -
app-copyq@autostart.service                                                    generated -
app-geoclue\x2ddemo\x2dagent@autostart.service                                 generated -
app-gnome\x2dkeyring\x2dpkcs11@autostart.service                               generated -
app-gnome\x2dkeyring\x2dsecrets@autostart.service                              generated -
app-gnome\x2dkeyring\x2dssh@autostart.service                                  generated -
app-im\x2dlaunch@autostart.service                                             generated -
app-mate\x2dsettings\x2ddaemon@autostart.service                               generated -
app-mintreport@autostart.service                                               generated -
app-mintupdate@autostart.service                                               generated -
app-mintwelcome@autostart.service                                              generated -
app-nm\x2dapplet@autostart.service                                             generated -
app-onboard\x2dautostart@autostart.service                                     generated -
app-orca\x2dautostart@autostart.service                                        generated -
app-org.gnome.Evolution\x2dalarm\x2dnotify@autostart.service                   generated -
app-org.gnome.SettingsDaemon.DiskUtilityNotify@autostart.service               generated -
app-polkit\x2dgnome\x2dauthentication\x2dagent\x2d1@autostart.service          generated -
app-polkit\x2dmate\x2dauthentication\x2dagent\x2d1@autostart.service           generated -
app-sticky@autostart.service                                                   generated -
app-touchegg@autostart.service                                                 generated -
app-user\x2ddirs\x2dupdate\x2dgtk@autostart.service                            generated -
app-xdg\x2duser\x2ddirs@autostart.service                                      generated -
at-spi-dbus-bus.service                                                        static    -
blueman-applet.service                                                         static    -
blueman-manager.service                                                        static    -
colord-session.service                                                         static    -
dbus-org.bluez.obex.service                                                    alias     -
dbus.service                                                                   static    -
dconf.service                                                                  static    -
dirmngr.service                                                                static    -
evolution-addressbook-factory.service                                          static    -
evolution-calendar-factory.service                                             static    -
evolution-source-registry.service                                              static    -
evolution-user-prompter.service                                                static    -
filter-chain.service                                                           enabled   enabled
flatpak-oci-authenticator.service                                              static    -
flatpak-portal.service                                                         static    -
flatpak-session-helper.service                                                 static    -
gamemoded.service                                                              disabled  enabled
gcr-ssh-agent.service                                                          enabled   enabled
glib-pacrunner.service                                                         static    -
gnome-keyring-daemon.service                                                   enabled   enabled
gnome-terminal-server.service                                                  static    -
gpg-agent.service                                                              static    -
gvfs-afc-volume-monitor.service                                                static    -
gvfs-daemon.service                                                            static    -
gvfs-goa-volume-monitor.service                                                static    -
gvfs-gphoto2-volume-monitor.service                                            static    -
gvfs-metadata.service                                                          static    -
gvfs-mtp-volume-monitor.service                                                static    -
gvfs-udisks2-volume-monitor.service                                            static    -
hermes-dashboard.service                                                       disabled  enabled
hermes-gateway.service                                                         disabled  enabled
keyboxd.service                                                                static    -
launchpadlib-cache-clean.service                                               static    -
n8n.service                                                                    disabled  enabled
obex.service                                                                   enabled   enabled
org.freedesktop.IBus.session.generic.service                                   static    -
org.freedesktop.IBus.session.GNOME.service                                     enabled   enabled
org.gnome.SettingsDaemon.A11ySettings.service                                  static    -
org.gnome.SettingsDaemon.Color.service                                         static    -
org.gnome.SettingsDaemon.Datetime.service                                      static    -
org.gnome.SettingsDaemon.Housekeeping.service                                  static    -
org.gnome.SettingsDaemon.Keyboard.service                                      static    -
org.gnome.SettingsDaemon.MediaKeys.service                                     static    -
org.gnome.SettingsDaemon.Power.service                                         static    -
org.gnome.SettingsDaemon.PrintNotifications.service                            static    -
org.gnome.SettingsDaemon.Rfkill.service                                        static    -
org.gnome.SettingsDaemon.ScreensaverProxy.service                              static    -
org.gnome.SettingsDaemon.Sharing.service                                       static    -
org.gnome.SettingsDaemon.Smartcard.service                                     static    -
org.gnome.SettingsDaemon.Sound.service                                         static    -
org.gnome.SettingsDaemon.UsbProtection.service                                 static    -
org.gnome.SettingsDaemon.Wacom.service                                         static    -
org.gnome.SettingsDaemon.Wwan.service                                          static    -
org.gnome.SettingsDaemon.XSettings.service                                     static    -
pipewire-pulse.service                                                         enabled   enabled
pipewire.service                                                               enabled   enabled
pk-debconf-helper.service                                                      static    -
session-migration.service                                                      enabled   enabled
speech-dispatcher.service                                                      static    -
ssh-agent.service                                                              static    -
systemd-exit.service                                                           static    -
systemd-tmpfiles-clean.service                                                 static    -
systemd-tmpfiles-setup.service                                                 disabled  enabled
wireplumber.service                                                            enabled   enabled
wireplumber@.service                                                           disabled  enabled
xdg-desktop-portal-gtk.service                                                 static    -
xdg-desktop-portal-rewrite-launchers.service                                   enabled   enabled
xdg-desktop-portal-xapp.service                                                static    -
xdg-desktop-portal.service                                                     static    -
xdg-document-portal.service                                                    static    -
xdg-permission-store.service                                                   static    -
app.slice                                                                      static    -
background.slice                                                               static    -
session.slice                                                                  static    -
dbus.socket                                                                    static    -
dirmngr.socket                                                                 enabled   enabled
gcr-ssh-agent.socket                                                           enabled   enabled
gnome-keyring-daemon.socket                                                    enabled   enabled
gpg-agent-browser.socket                                                       enabled   enabled
gpg-agent-extra.socket                                                         enabled   enabled
gpg-agent-ssh.socket                                                           enabled   enabled
gpg-agent.socket                                                               enabled   enabled
keyboxd.socket                                                                 enabled   enabled
pipewire-pulse.socket                                                          enabled   enabled
pipewire.socket                                                                enabled   enabled
pk-debconf-helper.socket                                                       enabled   enabled
speech-dispatcher.socket                                                       enabled   enabled
basic.target                                                                   static    -
bluetooth.target                                                               static    -
default.target                                                                 static    -
exit.target                                                                    static    -
graphical-session-pre.target                                                   static    -
graphical-session.target                                                       static    -
org.gnome.SettingsDaemon.A11ySettings.target                                   static    -
org.gnome.SettingsDaemon.Color.target                                          static    -
org.gnome.SettingsDaemon.Datetime.target                                       static    -
org.gnome.SettingsDaemon.Housekeeping.target                                   static    -
org.gnome.SettingsDaemon.Keyboard.target                                       static    -
org.gnome.SettingsDaemon.MediaKeys.target                                      static    -
org.gnome.SettingsDaemon.Power.target                                          static    -
org.gnome.SettingsDaemon.PrintNotifications.target                             static    -
org.gnome.SettingsDaemon.Rfkill.target                                         static    -
org.gnome.SettingsDaemon.ScreensaverProxy.target                               static    -
org.gnome.SettingsDaemon.Sharing.target                                        static    -
org.gnome.SettingsDaemon.Smartcard.target                                      static    -
org.gnome.SettingsDaemon.Sound.target                                          static    -
org.gnome.SettingsDaemon.UsbProtection.target                                  static    -
org.gnome.SettingsDaemon.Wacom.target                                          static    -
org.gnome.SettingsDaemon.Wwan.target                                           static    -
org.gnome.SettingsDaemon.XSettings.target                                      static    -
paths.target                                                                   static    -
printer.target                                                                 static    -
shutdown.target                                                                static    -
smartcard.target                                                               static    -
sockets.target                                                                 static    -
sound.target                                                                   static    -
timers.target                                                                  static    -
xdg-desktop-autostart.target                                                   static    -
launchpadlib-cache-clean.timer                                                 enabled   enabled
systemd-tmpfiles-clean.timer                                                   disabled  enabled
```

## [s1_enabled]
**Comando:** `export XDG_RUNTIME_DIR=/run/user/$(id -u); systemctl --user list-unit-files --state=enabled --no-pager --no-legend 2>&1`

```
9router.service                              enabled enabled
filter-chain.service                         enabled enabled
gcr-ssh-agent.service                        enabled enabled
gnome-keyring-daemon.service                 enabled enabled
obex.service                                 enabled enabled
org.freedesktop.IBus.session.GNOME.service   enabled enabled
pipewire-pulse.service                       enabled enabled
pipewire.service                             enabled enabled
session-migration.service                    enabled enabled
wireplumber.service                          enabled enabled
xdg-desktop-portal-rewrite-launchers.service enabled enabled
dirmngr.socket                               enabled enabled
gcr-ssh-agent.socket                         enabled enabled
gnome-keyring-daemon.socket                  enabled enabled
gpg-agent-browser.socket                     enabled enabled
gpg-agent-extra.socket                       enabled enabled
gpg-agent-ssh.socket                         enabled enabled
gpg-agent.socket                             enabled enabled
keyboxd.socket                               enabled enabled
pipewire-pulse.socket                        enabled enabled
pipewire.socket                              enabled enabled
pk-debconf-helper.socket                     enabled enabled
speech-dispatcher.socket                     enabled enabled
launchpadlib-cache-clean.timer               enabled enabled
```

## [s1_list_units_all]
**Comando:** `export XDG_RUNTIME_DIR=/run/user/$(id -u); systemctl --user list-units --all --no-pager --no-legend 2>&1 | head -60`

```
  dev-cdrom.device                                                                                       loaded    active   plugged   HL-DT-ST_DVD+_-RW_GU90N
  dev-disk-by\x2ddiskseq-11.device                                                                       loaded    active   plugged   HL-DT-ST_DVD+_-RW_GU90N
  dev-disk-by\x2ddiskseq-9.device                                                                        loaded    active   plugged   ADATA_SU650
  dev-disk-by\x2ddiskseq-9\x2dpart1.device                                                               loaded    active   plugged   ADATA_SU650 EFI\x20System\x20Partition
  dev-disk-by\x2ddiskseq-9\x2dpart2.device                                                               loaded    active   plugged   ADATA_SU650 2
  dev-disk-by\x2did-ata\x2dADATA_SU650_2N332LA2BBGC.device                                               loaded    active   plugged   ADATA_SU650
  dev-disk-by\x2did-ata\x2dADATA_SU650_2N332LA2BBGC\x2dpart1.device                                      loaded    active   plugged   ADATA_SU650 EFI\x20System\x20Partition
  dev-disk-by\x2did-ata\x2dADATA_SU650_2N332LA2BBGC\x2dpart2.device                                      loaded    active   plugged   ADATA_SU650 2
  dev-disk-by\x2did-ata\x2dHL\x2dDT\x2dST_DVD\x2b_\x2dRW_GU90N_M1HH17G0804.device                        loaded    active   plugged   HL-DT-ST_DVD+_-RW_GU90N
  dev-disk-by\x2did-wwn\x2d0x5001480000000000.device                                                     loaded    active   plugged   HL-DT-ST_DVD+_-RW_GU90N
  dev-disk-by\x2dpartlabel-EFI\x5cx20System\x5cx20Partition.device                                       loaded    active   plugged   ADATA_SU650 EFI\x20System\x20Partition
  dev-disk-by\x2dpartuuid-9e43d5ab\x2d8c1c\x2d4aa1\x2d9d8b\x2d1f82109bd123.device                        loaded    active   plugged   ADATA_SU650 EFI\x20System\x20Partition
  dev-disk-by\x2dpartuuid-ff137625\x2dd0c4\x2d4a7b\x2da3c9\x2d7b4d9888bc44.device                        loaded    active   plugged   ADATA_SU650 2
  dev-disk-by\x2dpath-pci\x2d0000:00:17.0\x2data\x2d1.0.device                                           loaded    active   plugged   ADATA_SU650
  dev-disk-by\x2dpath-pci\x2d0000:00:17.0\x2data\x2d1.0\x2dpart1.device                                  loaded    active   plugged   ADATA_SU650 EFI\x20System\x20Partition
  dev-disk-by\x2dpath-pci\x2d0000:00:17.0\x2data\x2d1.0\x2dpart2.device                                  loaded    active   plugged   ADATA_SU650 2
  dev-disk-by\x2dpath-pci\x2d0000:00:17.0\x2data\x2d1.device                                             loaded    active   plugged   ADATA_SU650
  dev-disk-by\x2dpath-pci\x2d0000:00:17.0\x2data\x2d1\x2dpart1.device                                    loaded    active   plugged   ADATA_SU650 EFI\x20System\x20Partition
  dev-disk-by\x2dpath-pci\x2d0000:00:17.0\x2data\x2d1\x2dpart2.device                                    loaded    active   plugged   ADATA_SU650 2
  dev-disk-by\x2dpath-pci\x2d0000:00:17.0\x2data\x2d2.0.device                                           loaded    active   plugged   HL-DT-ST_DVD+_-RW_GU90N
  dev-disk-by\x2dpath-pci\x2d0000:00:17.0\x2data\x2d2.device                                             loaded    active   plugged   HL-DT-ST_DVD+_-RW_GU90N
  dev-disk-by\x2duuid-6464df49\x2d2c3a\x2d4f94\x2db2ec\x2dc752991afd6e.device                            loaded    active   plugged   ADATA_SU650 2
  dev-disk-by\x2duuid-B371\x2d5397.device                                                                loaded    active   plugged   ADATA_SU650 EFI\x20System\x20Partition
  dev-rfkill.device                                                                                      loaded    active   plugged   /dev/rfkill
  dev-sda.device                                                                                         loaded    active   plugged   ADATA_SU650
  dev-sda1.device                                                                                        loaded    active   plugged   ADATA_SU650 EFI\x20System\x20Partition
  dev-sda2.device                                                                                        loaded    active   plugged   ADATA_SU650 2
  dev-snd-by\x2dpath-pci\x2d0000:00:1f.3.device                                                          loaded    active   plugged   /dev/snd/by-path/pci-0000:00:1f.3
  dev-snd-controlC0.device                                                                               loaded    active   plugged   /dev/snd/controlC0
  dev-sr0.device                                                                                         loaded    active   plugged   HL-DT-ST_DVD+_-RW_GU90N
  dev-tpm0.device                                                                                        loaded    active   plugged   /dev/tpm0
  dev-tpmrm0.device                                                                                      loaded    active   plugged   /dev/tpmrm0
  dev-ttyprintk.device                                                                                   loaded    active   plugged   /dev/ttyprintk
  dev-ttyS0.device                                                                                       loaded    active   plugged   /dev/ttyS0
  dev-ttyS1.device                                                                                       loaded    active   plugged   /dev/ttyS1
  dev-ttyS10.device                                                                                      loaded    active   plugged   /dev/ttyS10
  dev-ttyS11.device                                                                                      loaded    active   plugged   /dev/ttyS11
  dev-ttyS12.device                                                                                      loaded    active   plugged   /dev/ttyS12
  dev-ttyS13.device                                                                                      loaded    active   plugged   /dev/ttyS13
  dev-ttyS14.device                                                                                      loaded    active   plugged   /dev/ttyS14
  dev-ttyS15.device                                                                                      loaded    active   plugged   /dev/ttyS15
  dev-ttyS16.device                                                                                      loaded    active   plugged   /dev/ttyS16
  dev-ttyS17.device                                                                                      loaded    active   plugged   /dev/ttyS17
  dev-ttyS18.device                                                                                      loaded    active   plugged   /dev/ttyS18
  dev-ttyS19.device                                                                                      loaded    active   plugged   /dev/ttyS19
  dev-ttyS2.device                                                                                       loaded    active   plugged   /dev/ttyS2
  dev-ttyS20.device                                                                                      loaded    active   plugged   /dev/ttyS20
  dev-ttyS21.device                                                                                      loaded    active   plugged   /dev/ttyS21
  dev-ttyS22.device                                                                                      loaded    active   plugged   /dev/ttyS22
  dev-ttyS23.device                                                                                      loaded    active   plugged   /dev/ttyS23
  dev-ttyS24.device                                                                                      loaded    active   plugged   /dev/ttyS24
  dev-ttyS25.device                                                                                      loaded    active   plugged   /dev/ttyS25
  dev-ttyS26.device                                                                                      loaded    active   plugged   /dev/ttyS26
  dev-ttyS27.device                                                                                      loaded    active   plugged   /dev/ttyS27
  dev-ttyS28.device                                                                                      loaded    active   plugged   /dev/ttyS28
  dev-ttyS29.device                                                                                      loaded    active   plugged   /dev/ttyS29
  dev-ttyS3.device                                                                                       loaded    active   plugged   /dev/ttyS3
  dev-ttyS30.device                                                                                      loaded    active   plugged   /dev/ttyS30
  dev-ttyS31.device                                                                                      loaded    active   plugged   /dev/ttyS31
  dev-ttyS4.device                                                                                       loaded    active   plugged   /dev/ttyS4
```

## [s1_ghost]
**Comando:** `export XDG_RUNTIME_DIR=/run/user/$(id -u); systemctl --user list-units --all --no-legend 2>&1 | grep -E 'ghost|not-found|masked|failed|bad' || echo NENHUM_FANTASMA_OU_FALHA`

```
● pipewire-media-session.service                                                                         not-found inactive dead      pipewire-media-session.service
● pipewire-session-manager.service                                                                       not-found inactive dead      pipewire-session-manager.service
● pulseaudio.service                                                                                     not-found inactive dead      pulseaudio.service
● pulseaudio.socket                                                                                      not-found inactive dead      pulseaudio.socket
● blockdev@dev-sda1.target                                                                               not-found inactive dead      blockdev@dev-sda1.target
● blockdev@dev-zram0.target                                                                              not-found inactive dead      blockdev@dev-zram0.target
● network-online.target                                                                                  not-found inactive dead      network-online.target
```

## [s1_timers]
**Comando:** `export XDG_RUNTIME_DIR=/run/user/$(id -u); systemctl --user list-timers --all --no-pager 2>&1`

```
NEXT                        LEFT LAST                              PASSED UNIT                           ACTIVATES
Thu 2026-10-08 01:32:00 -03  22h Wed 2026-10-07 01:32:00 -03 1h 41min ago launchpadlib-cache-clean.timer launchpadlib-cache-clean.service

1 timers listed.
```

## [s1_cat_units]
**Comando:** `for f in $(find ~/.config/systemd/user -maxdepth 3 -type f 2>/dev/null | sort); do echo "===== $f"; cat "$f"; echo; done 2>&1 | head -400`

```
===== /home/dr/.config/systemd/user/9router.service
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

===== /home/dr/.config/systemd/user/hermes-dashboard.service
[Unit]
Description=Hermes Agent Dashboard
After=network-online.target hermes-gateway.service
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=/home/dr/.hermes
Environment="PATH=/home/dr/.hermes/hermes-agent/venv/bin:/home/dr/.hermes/hermes-agent/node_modules/.bin:/home/dr/.hermes/node/bin:/home/dr/.hermes/node:/home/dr/.local/bin:/home/dr/.local/share/nvm/versions/node/v24.16.0/bin:/usr/local/bin
Environment="HERMES_HOME=/home/dr/.hermes"
ExecStart=/home/dr/.hermes/hermes-agent/venv/bin/hermes dashboard --host 127.0.0.1 --port 9119 --no-open --skip-build
Restart=always
RestartSec=5

[Install]
WantedBy=default.target

===== /home/dr/.config/systemd/user/hermes-gateway.service
[Unit]
Description=Hermes Agent Gateway - Messaging Platform Integration
After=network-online.target
Wants=network-online.target
StartLimitIntervalSec=0

[Service]
Type=simple
ExecStart=/home/dr/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main gateway run
WorkingDirectory=/home/dr/.hermes
Environment="PATH=/home/dr/.hermes/hermes-agent/venv/bin:/home/dr/.hermes/hermes-agent/node_modules/.bin:/home/dr/.hermes/node/bin:/home/dr/.hermes/node:/home/dr/.local/bin:/home/dr/.npm-global/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/
Environment="VIRTUAL_ENV=/home/dr/.hermes/hermes-agent/venv"
Environment="HERMES_HOME=/home/dr/.hermes"
Environment="HERMES_SUPERVISED_CHILD=1"
Restart=always
RestartSec=5
RestartForceExitStatus=75
RestartPreventExitStatus=78
KillMode=mixed
KillSignal=SIGTERM
ExecReload=/bin/kill -USR1 $MAINPID
ExecStopPost=-/home/dr/.hermes/hermes-agent/venv/bin/python -m gateway.cgroup_cleanup
TimeoutStopSec=70
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target

===== /home/dr/.config/systemd/user/n8n.service
[Unit]
Description=n8n Personal Automation
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=/home/dr/.local/share/n8n/.n8n
EnvironmentFile=/home/dr/.config/n8n/n8n.env
Environment="PATH=/home/dr/.local/share/nvm/versions/node/v24.16.0/bin:/usr/local/bin:/usr/bin:/bin"
Environment="NODE_OPTIONS=--max-old-space-size=1024"
UMask=0077
ExecStart=/home/dr/.local/share/nvm/versions/node/v24.16.0/bin/node /home/dr/.local/share/nvm/versions/node/v24.16.0/lib/node_modules/n8n/bin/n8n start
Restart=always
RestartSec=5
MemoryHigh=1G
MemoryMax=1536M

[Install]
WantedBy=default.target
```

## [s1_show_9router]
**Comando:** `export XDG_RUNTIME_DIR=/run/user/$(id -u); systemctl --user show 9router.service -p Id -p FragmentPath -p ActiveState -p UnitFileState -p ExecStart -p WorkingDirectory -p MainPID -p ExecMainStatus 2>&1`

```
MainPID=23840
ExecMainStatus=0
ExecStart={ path=/home/dr/.local/share/nvm/versions/node/v24.16.0/bin/node ; argv[]=/home/dr/.local/share/nvm/versions/node/v24.16.0/bin/node /home/dr/.local/lib/node_modules/9router/cli.js --no-browser --skip-update --log ; ignore_errors=n
WorkingDirectory=/home/dr/.local/share/9router
Id=9router.service
ActiveState=active
FragmentPath=/home/dr/.config/systemd/user/9router.service
UnitFileState=enabled
```

## [s1_user_meta]
**Comando:** `export XDG_RUNTIME_DIR=/run/user/$(id -u); systemctl --user get-default; loginctl show-user dr -p Linger 2>&1; echo ---; ls -la /etc/systemd/user/ 2>&1 | head -15; echo ---; find ~/.config/systemd/user -xtype l -printf 'BROKEN %p -> %l\n' 2>&1 | head -10; echo FIM`

```
default.target
Linger=yes
---
total 32
drwxr-xr-x 8 root root 4096 jan  8  2026 .
drwxr-xr-x 8 root root 4096 set  9 12:40 ..
lrwxrwxrwx 1 root root   34 jun  5 19:19 dbus-org.bluez.obex.service -> /usr/lib/systemd/user/obex.service
drwxr-xr-x 2 root root 4096 jan  8  2026 default.target.wants
drwxr-xr-x 2 root root 4096 jan  8  2026 gnome-session.target.wants
drwxr-xr-x 2 root root 4096 jan  8  2026 graphical-session-pre.target.wants
drwxr-xr-x 2 root root 4096 jan  8  2026 pipewire.service.wants
drwxr-xr-x 2 root root 4096 jan  8  2026 sockets.target.wants
drwxr-xr-x 2 root root 4096 jan  8  2026 timers.target.wants
---
FIM
```

## [s1_status_extra]
**Comando:** `export XDG_RUNTIME_DIR=/run/user/$(id -u); for u in hermes-dashboard.service hermes-gateway.service n8n.service; do echo "== $u"; systemctl --user is-enabled $u 2>&1; systemctl --user is-active $u 2>&1; systemctl --user show $u -p FragmentPath -p ActiveState -p UnitFileState -p ExecStart 2>&1 | head -8; done`

```
== hermes-dashboard.service
disabled
inactive
ExecStart={ path=/home/dr/.hermes/hermes-agent/venv/bin/hermes ; argv[]=/home/dr/.hermes/hermes-agent/venv/bin/hermes dashboard --host 127.0.0.1 --port 9119 --no-open --skip-build ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pi
ActiveState=inactive
FragmentPath=/home/dr/.config/systemd/user/hermes-dashboard.service
UnitFileState=disabled
== hermes-gateway.service
disabled
inactive
ExecStart={ path=/home/dr/.hermes/hermes-agent/venv/bin/python ; argv[]=/home/dr/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main gateway run ; ignore_errors=no ; start_time=[n/a] ; stop_time=[n/a] ; pid=0 ; code=(null) ; status=0/0 
ActiveState=inactive
FragmentPath=/home/dr/.config/systemd/user/hermes-gateway.service
UnitFileState=disabled
== n8n.service
disabled
inactive
ExecStart={ path=/home/dr/.local/share/nvm/versions/node/v24.16.0/bin/node ; argv[]=/home/dr/.local/share/nvm/versions/node/v24.16.0/bin/node /home/dr/.local/share/nvm/versions/node/v24.16.0/lib/node_modules/n8n/bin/n8n start ; ignore_error
ActiveState=inactive
FragmentPath=/home/dr/.config/systemd/user/n8n.service
UnitFileState=disabled
```

## [s1_paths_check]
**Comando:** `
for p in  /home/dr/.local/share/nvm/versions/node/v24.16.0/bin/node  /home/dr/.local/lib/node_modules/9router/cli.js  /home/dr/.local/share/9router  /home/dr/.hermes/hermes-agent/venv/bin/hermes  /home/dr/.hermes/hermes-agent/venv/bin/python  /home/dr/.hermes  /home/dr/.config/n8n/n8n.env  /home/dr/.local/share/n8n/.n8n  /home/dr/.local/share/nvm/versions/node/v24.16.0/lib/node_modules/n8n/bin/n8`

```
OK    /home/dr/.local/share/nvm/versions/node/v24.16.0/bin/node
OK    /home/dr/.local/lib/node_modules/9router/cli.js
OK    /home/dr/.local/share/9router
FALTA /home/dr/.hermes/hermes-agent/venv/bin/hermes
FALTA /home/dr/.hermes/hermes-agent/venv/bin/python
OK    /home/dr/.hermes
OK    /home/dr/.config/n8n/n8n.env
OK    /home/dr/.local/share/n8n/.n8n
OK    /home/dr/.local/share/nvm/versions/node/v24.16.0/lib/node_modules/n8n/bin/n8n
FALTA /home/dr/.hermes/hermes-agent/venv/bin/node
FALTA /home/dr/.hermes/node/bin
```

## [s2_ls_etc_units]
**Comando:** `find /etc/systemd/system -maxdepth 2 \( -type f -o -type l \) -printf '%y %p -> %l\n' 2>/dev/null | grep -v 'wants/\|\.target\.wants\|sockets\.target' | sort | head -50; echo ---WANTS---; ls /etc/systemd/system/*.wants/ /etc/systemd/system/*.target.wants/ 2>/dev/null | head -40`

```
f /etc/systemd/system/alloy.service.d/env.conf -> 
f /etc/systemd/system/cloudflared.service -> 
f /etc/systemd/system/cloudflared-update.service -> 
f /etc/systemd/system/cloudflared-update.timer -> 
f /etc/systemd/system/ollama.service.d/override.conf -> 
l /etc/systemd/system/casper-md5check.service -> /dev/null
l /etc/systemd/system/dbus-fi.w1.wpa_supplicant1.service -> /usr/lib/systemd/system/wpa_supplicant.service
l /etc/systemd/system/dbus-org.bluez.service -> /usr/lib/systemd/system/bluetooth.service
l /etc/systemd/system/dbus-org.freedesktop.Avahi.service -> /usr/lib/systemd/system/avahi-daemon.service
l /etc/systemd/system/dbus-org.freedesktop.ModemManager1.service -> /usr/lib/systemd/system/ModemManager.service
l /etc/systemd/system/dbus-org.freedesktop.nm-dispatcher.service -> /usr/lib/systemd/system/NetworkManager-dispatcher.service
l /etc/systemd/system/dbus-org.freedesktop.resolve1.service -> /usr/lib/systemd/system/systemd-resolved.service
l /etc/systemd/system/dbus-org.freedesktop.thermald.service -> /usr/lib/systemd/system/thermald.service
l /etc/systemd/system/dbus-org.freedesktop.timesync1.service -> /usr/lib/systemd/system/systemd-timesyncd.service
l /etc/systemd/system/display-manager.service -> /lib/systemd/system/lightdm.service
l /etc/systemd/system/smartd.service -> /usr/lib/systemd/system/smartmontools.service
l /etc/systemd/system/sshd.service -> /usr/lib/systemd/system/ssh.service
l /etc/systemd/system/ssh.service.requires/ssh.socket -> /usr/lib/systemd/system/ssh.socket
l /etc/systemd/system/syslog.service -> /usr/lib/systemd/system/rsyslog.service
---WANTS---
/etc/systemd/system/bluetooth.target.wants/:
bluetooth.service

/etc/systemd/system/bluetooth.target.wants/:
bluetooth.service

/etc/systemd/system/display-manager.service.wants/:
gpu-manager.service

/etc/systemd/system/emergency.target.wants/:
grub-initrd-fallback.service

/etc/systemd/system/emergency.target.wants/:
grub-initrd-fallback.service

/etc/systemd/system/final.target.wants/:
casper.service

/etc/systemd/system/final.target.wants/:
casper.service

/etc/systemd/system/getty.target.wants/:
getty@tty1.service

/etc/systemd/system/getty.target.wants/:
getty@tty1.service

/etc/systemd/system/graphical.target.wants/:
accounts-daemon.service
power-profiles-daemon.service
switcheroo-control.service
udisks2.service

/etc/systemd/system/graphical.target.wants/:
accounts-daemon.service
power-profiles-daemon.service
switcheroo-control.service
udisks2.service

/etc/systemd/system/hibernate.target.wants/:
```

## [s2_dpkg_owner]
**Comando:** `
for f in $(find /etc/systemd/system -maxdepth 1 -type f -name '*.service' -o -maxdepth 1 -type f -name '*.timer' -o -maxdepth 1 -type f -name '*.mount' 2>/dev/null | sort); do
  o=$(dpkg -S "$f" 2>/dev/null | head -1)
  if [ -z "$o" ]; then echo "NAO-PACOTE $f"; else echo "PACOTE     $f <= ${o%%:*}"; fi
done
echo ---SYMLINKS-TOPO---
for l in /etc/systemd/system/*.wants/*; do [ -e "$l" ] || echo "`

```
NAO-PACOTE /etc/systemd/system/cloudflared.service
NAO-PACOTE /etc/systemd/system/cloudflared-update.service
NAO-PACOTE /etc/systemd/system/cloudflared-update.timer
---SYMLINKS-TOPO---
FIM
```

## [s2_failed]
**Comando:** `export XDG_RUNTIME_DIR=/run/user/$(id -u); systemctl --failed --no-legend 2>&1 | head -10; echo ---USER-FAILED---; systemctl --user --failed --no-legend 2>&1 | head -10; echo FIM`

```
---USER-FAILED---
FIM
```

## [s2_masked_sys]
**Comando:** `systemctl list-unit-files --state=masked --no-legend 2>&1 | head -10; echo FIM`

```
alsa-utils.service       masked enabled
casper-md5check.service  masked enabled
cryptdisks-early.service masked enabled
cryptdisks.service       masked enabled
hwclock.service          masked enabled
saned.service            masked enabled
sudo.service             masked enabled
x11-common.service       masked enabled
FIM
```

## [c1_crontab_dr]
**Comando:** `crontab -l 2>&1`

```
no crontab for dr
```

## [c2_etc_cron]
**Comando:** `ls -la /etc/cron.d/ 2>&1; echo ---; for f in /etc/cron.d/*; do o=$(dpkg -S $f 2>/dev/null); [ -z "$o" ] && echo "NAO-PACOTE $f" || echo "PACOTE $f"; done 2>&1; echo ---CRON-DAILY-ETC---; ls /etc/cron.daily /etc/cron.hourly /etc/cron.weekly /etc/cron.monthly 2>/dev/null`

```
total 32
drwxr-xr-x   2 root root  4096 ago  7 14:46 .
drwxr-xr-x 168 root root 12288 out  7 01:21 ..
-rw-r--r--   1 root root   219 nov 17  2023 anacron
-rw-r--r--   1 root root   201 abr  8  2024 e2scrub_all
-rw-r--r--   1 root root   102 mar 30  2024 .placeholder
-rw-r--r--   1 root root   396 jan  9  2024 sysstat
---
PACOTE /etc/cron.d/anacron
PACOTE /etc/cron.d/e2scrub_all
PACOTE /etc/cron.d/sysstat
---CRON-DAILY-ETC---
/etc/cron.daily:
0anacron
apt-compat
aptitude
dpkg
google-chrome
logrotate
man-db
plocate
sysstat

/etc/cron.hourly:

/etc/cron.monthly:
0anacron

/etc/cron.weekly:
0anacron
man-db
```

## [c3_cron_spool]
**Comando:** `ls -la /var/spool/cron/crontabs/ 2>&1; echo ---; sudo -n ls /var/spool/cron/crontabs/ 2>&1 | head -5`

```
ls: não foi possível abrir o diretório '/var/spool/cron/crontabs/': Permissão negada
---
sudo: uma senha é necessária
```

## [c4_hermes_cron]
**Comando:** `ls -la ~/.hermes/cron/ 2>&1; echo ---; find ~/.hermes/cron -type f 2>/dev/null | head -20 | while read f; do echo "== $f"; head -30 "$f"; done 2>&1 | head -120`

```
total 52
drwx------  3 dr dr  4096 out  7 03:14 .
drwx------ 45 dr dr  4096 out  7 03:14 ..
-rw-r--r--  1 dr dr 24576 set  7 22:16 executions.db
-rw-------  1 dr dr    17 set 24 12:36 .hb_gc47vz1f.tmp
-rw-------  1 dr dr    18 set 15 16:32 .hb_mz3nkzdf.tmp
-rw-rw-r--  1 dr dr     0 ago 20 02:49 .jobs.lock
drwx------  2 dr dr  4096 ago 18 20:49 output
-rw-------  1 dr dr    18 out  7 03:14 ticker_heartbeat
-rw-------  1 dr dr    17 out  7 03:14 ticker_last_success
-rw-rw-r--  1 dr dr     0 out  7 03:14 .tick.lock
---
== /home/dr/.hermes/cron/executions.db
SQLite format 3   @                                                                     .��

� 
 
�

�(                                                                                                                                                                                                                                             
!!�_tableexecutionsexecutionsCREATE TABLE executions (
             id TEXT PRIMARY KEY,
             job_id TEXT NOT NULL,
             source TEXT NOT NULL,
             process_id TEXT NOT NULL,
             pid INTEGER NOT NULL,
             process_started_at INTEGER,
             status TEXT NOT NULL CHECK(status IN
               ('claimed','running','completed','failed','unknown')),
             claimed_at TEXT NOT NULL,
             started_at TEXT,
             finished_at TEXT,
             error TEXT
           , handoff_pending INTEGER NOT NULL DEFAULT 0, handoff_started_at REAL, delivery_outcome TEXT, scheduled_instant TEXT)�G!�Aindexidx_executions_status_claimedexecutionsCREATE INDEX idx_executions_status_claimed ON executions(
             id TEXT PRIMARY KEY,
             job_id TEXT NOT NULL,
             source TEXT NOT NULL,
             process_id TEXT NOT NULL,
             pid INTEGER NOT NULL,
             process_started_at INTEGER,
             status TEXT NOT NULL CHECK(status IN
               ('claimed','running','completed','fa�?!�]indexidx_executions_occurrenceexecutionsCREATE INDEX idx_executions_occurrence ON executions(job_id, scheduled_instant) WHERE status='completed'3G! indexsqlite_autoindex_exec
                                                                                                                                                                                                                                               
                                                                                                                                                                                                                                               
                                                                                                                                                                                                                                               
                                                                                                                                                                                                                                               
                                                                                                                                                                                                                                               
1790264187.812657== /home/dr/.hermes/cron/ticker_last_success
1791353672.259815== /home/dr/.hermes/cron/.jobs.lock
== /home/dr/.hermes/cron/.hb_mz3nkzdf.tmp
1789500768.2016926== /home/dr/.hermes/cron/.tick.lock
== /home/dr/.hermes/cron/ticker_heartbeat
```

## [s2_cloudflared_cat]
**Comando:** `cat /etc/systemd/system/cloudflared.service /etc/systemd/system/cloudflared-update.service /etc/systemd/system/cloudflared-update.timer 2>&1`

```
[Unit]
Description=Cloudflare Tunnel client
After=network-online.target
Wants=network-online.target

[Service]
TimeoutStartSec=15
Type=notify
ExecStart=/usr/bin/cloudflared --no-autoupdate tunnel run --token-file /etc/cloudflared/token
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
[Unit]
Description=Update cloudflared
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/bin/bash -c '/usr/bin/cloudflared update; code=$?; if [ $code -eq 11 ]; then systemctl restart cloudflared; exit 0; fi; exit $code'
[Unit]
Description=Update cloudflared

[Timer]
OnCalendar=daily

[Install]
WantedBy=timers.target
```

## [s2_cloudflared_status]
**Comando:** `systemctl is-enabled cloudflared.service cloudflared-update.timer 2>&1; systemctl is-active cloudflared.service cloudflared-update.timer 2>&1; systemctl list-timers --no-pager 2>&1 | grep -v '^$' | head -12`

```
enabled
disabled
active
inactive
NEXT                            LEFT LAST                              PASSED UNIT                         ACTIVATES
Wed 2026-10-07 03:32:12 -03    17min Wed 2026-10-07 02:34:00 -03    41min ago fwupd-refresh.timer          fwupd-refresh.service
Wed 2026-10-07 05:27:56 -03 2h 12min Wed 2026-10-07 00:32:22 -03            - motd-news.timer              motd-news.service
Wed 2026-10-07 06:09:41 -03 2h 54min Tue 2026-10-06 23:32:21 -03            - apt-daily-upgrade.timer      apt-daily-upgrade.service
Wed 2026-10-07 07:34:24 -03 4h 19min Tue 2026-10-06 23:32:21 -03            - anacron.timer                anacron.service
Wed 2026-10-07 17:26:10 -03      14h Tue 2026-10-06 23:32:21 -03            - apt-daily.timer              apt-daily.service
Thu 2026-10-08 00:00:00 -03      20h Wed 2026-10-07 00:00:13 -03            - dpkg-db-backup.timer         dpkg-db-backup.service
Thu 2026-10-08 00:00:00 -03      20h Wed 2026-10-07 00:00:13 -03            - logrotate.timer              logrotate.service
Thu 2026-10-08 01:42:00 -03      22h Wed 2026-10-07 01:42:00 -03 1h 33min ago systemd-tmpfiles-clean.timer systemd-tmpfiles-clean.service
Thu 2026-10-08 02:18:43 -03      23h Wed 2026-10-07 01:20:47 -03            - man-db.timer                 man-db.service
Sun 2026-10-11 03:10:44 -03   3 days Sun 2026-10-04 03:10:45 -03            - e2scrub_all.timer            e2scrub_all.service
Mon 2026-10-12 01:23:53 -03   4 days Mon 2026-10-05 00:50:41 -03            - fstrim.timer                 fstrim.service
```

## [s2_cloudflared_paths]
**Comando:** `for p in $(grep -hoE '(/[^ "]+)' /etc/systemd/system/cloudflared*.service /etc/systemd/system/cloudflared*.timer 2>/dev/null | grep -E '^/(usr|opt|home|etc|bin)' | sort -u | head -20); do [ -e "$p" ] && echo "OK    $p" || echo "FALTA $p"; done`

```
OK    /bin/bash
OK    /etc/cloudflared/token
OK    /usr/bin/cloudflared
```

## [s2_overrides]
**Comando:** `echo '== ollama override:'; cat /etc/systemd/system/ollama.service.d/override.conf 2>&1; echo; echo '== alloy env:'; cat /etc/systemd/system/alloy.service.d/env.conf 2>&1`

```
== ollama override:
# Ajuste do Ollama para o Tijolao — escrito em 18-ago-2026.
# Hardware: i7-7500U (2 nucleos/4 threads), 8 GB DDR4-2133 em CANAL UNICO (~17 GB/s
# teoricos), sem GPU com suporte ROCm. Objetivo: caber na RAM e nao cair no swap.
[Service]
# 1 modelo carregado por vez — dois nao cabem em 8 GB
Environment="OLLAMA_MAX_LOADED_MODELS=1"
# 1 requisicao simultanea — a RAM escala com NUM_PARALLEL x contexto
Environment="OLLAMA_NUM_PARALLEL=1"
# descarrega o modelo da RAM 5 min apos o ultimo uso
Environment="OLLAMA_KEEP_ALIVE=5m"
# atencao mais economica em memoria; pre-requisito do cache quantizado abaixo
Environment="OLLAMA_FLASH_ATTENTION=1"
# cache de contexto em 8 bits em vez de 16 = metade da memoria de contexto
Environment="OLLAMA_KV_CACHE_TYPE=q8_0"
# janela de contexto padrao
Environment="OLLAMA_CONTEXT_LENGTH=4096"

== alloy env:
cat: /etc/systemd/system/alloy.service.d/env.conf: Permissão negada
```

## [a1_autostart_ls]
**Comando:** `ls -la ~/.config/autostart/ 2>&1`

```
total 56
drwxrwxr-x  2 dr dr 4096 out  7 01:26 .
drwx------ 42 dr dr 4096 out  2 20:50 ..
-rw-rw-r--  1 dr dr  259 set  7 18:26 9router.desktop
-rw-rw-r--  1 dr dr 2601 set  7 06:27 blueman.desktop
-rw-rw-r--  1 dr dr  388 set  7 22:46 cinnamon-stats-tracker.desktop
-rw-rw-r--  1 dr dr  207 out  7 01:26 com.bitwarden.desktop.desktop
-rw-rw-r--  1 dr dr  140 set  5 19:10 copyq.desktop
-rw-rw-r--  1 dr dr   13 jun  6 04:40 mimeinfo.cache
-rw-rw-r--  1 dr dr 5137 set  7 22:46 mintreport.desktop
-rw-rw-r--  1 dr dr 6380 set  5 19:11 mintupdate.desktop
-rw-rw-r--  1 dr dr  445 set  7 22:46 print-applet.desktop
-rw-rw-r--  1 dr dr  299 set  7 22:46 xapp-sn-watcher.desktop
```

## [a2_autostart_desktops]
**Comando:** `
for f in ~/.config/autostart/*.desktop; do
  [ -e "$f" ] || continue
  echo "===== $f"
  grep -E '^(Exec|Name|Hidden|TryExec|Type|X-GNOME-Autostart-enabled)' "$f" 2>/dev/null | head -8
  exec_line=$(grep -m1 '^Exec=' "$f" | sed 's/^Exec=//' | sed 's/ %.*//')
  if [ -n "$exec_line" ]; then
    exe=$(echo "$exec_line" | awk '{print $1}')
    if command -v "$exe" >/dev/null 2>&1 || [ -x "$exe" ]; th`

```
===== /home/dr/.config/autostart/9router.desktop
Type=Application
Name=9Router
Exec=/home/dr/.config/nvm/versions/node/v24.16.0/bin/node /home/dr/.local/lib/node_modules/9router/cli.js --tray --skip-update
Hidden=false
X-GNOME-Autostart-enabled=true
  -> EXE NAO ENCONTRADO: /home/dr/.config/nvm/versions/node/v24.16.0/bin/node
===== /home/dr/.config/autostart/blueman.desktop
Name[be]=Аплет Blueman
Name[da]=Blueman-panelprogram
Name[de]=Blueman Applet
Name[el]=Εφαρμογή blueman
Name[en_GB]=Blueman Applet
Name[es]=Miniaplicación Blueman
Name[et]=Blueman rakend
Name[eu]=Blueman trepeta
  -> EXE OK: blueman-applet (/usr/bin/blueman-applet)
===== /home/dr/.config/autostart/cinnamon-stats-tracker.desktop
X-GNOME-Autostart-enabled=false
Name=Cinnamon Stats Tracker
Exec=cinnamon-stats-tracker
Type=Application
X-GNOME-Autostart-enabled=false
Hidden=true
  -> EXE NAO ENCONTRADO: cinnamon-stats-tracker
===== /home/dr/.config/autostart/com.bitwarden.desktop.desktop
Type=Application
Name=com.bitwarden.desktop
Exec=flatpak run --command=bitwarden.sh com.bitwarden.desktop --autostart %U
  -> EXE OK: flatpak (/usr/bin/flatpak)
===== /home/dr/.config/autostart/copyq.desktop
Type=Application
Name=CopyQ
Exec=copyq
X-GNOME-Autostart-enabled=false
  -> EXE OK: copyq (/usr/bin/copyq)
===== /home/dr/.config/autostart/mintreport.desktop
X-GNOME-Autostart-enabled=false
Name=System Reports
Name[am]=የ ስርአት መግለጫ
Name[ar]=تقارير النظام
Name[ast]=Reportes del sistema
Name[az]=Qurmaca Bildirimləri
Name[be]=Сістэмныя справаздачы
Name[bg]=Системен отчет
  -> EXE OK: mintreport-tray (/usr/bin/mintreport-tray)
===== /home/dr/.config/autostart/mintupdate.desktop
Name=Update Manager
Name[af]=Opdateringsbestuurder
Name[am]=የማሻሻያ አስተዳዳሪ
Name[ar]=مدير التحديث
Name[ar_AR]=مدير التحديث
Name[ar_MA]=مدير التحديث
Name[ast]=Xestor d'anovamientos
Name[az]=Yeniləmə İdarəçisi
  -> EXE OK: mintupdate-launcher (/usr/bin/mintupdate-launcher)
===== /home/dr/.config/autostart/print-applet.desktop
X-GNOME-Autostart-enabled=false
Name=Print Queue Applet
Exec=system-config-printer-applet
Type=Application
X-GNOME-Autostart-enabled=false
Hidden=true
  -> EXE NAO ENCONTRADO: system-config-printer-applet
===== /home/dr/.config/autostart/xapp-sn-watcher.desktop
X-GNOME-Autostart-enabled=false
Type=Application
Name=xapp-sn-watcher
Exec=/usr/lib/x86_64-linux-gnu/xapps/xapp-sn-watcher
X-GNOME-Autostart-enabled=false
Hidden=true
  -> EXE OK: /usr/lib/x86_64-linux-gnu/xapps/xapp-sn-watcher (/usr/lib/x86_64-linux-gnu/xapps/xapp-sn-watcher)
```

## [a3_local_share_apps]
**Comando:** `
ls ~/.local/share/applications/*.desktop 2>/dev/null | wc -l
for f in ~/.local/share/applications/*.desktop; do
  [ -e "$f" ] || continue
  echo "===== $(basename $f)"
  grep -E '^(Exec|Name)=' "$f" 2>/dev/null | head -4
  exec_line=$(grep -m1 '^Exec=' "$f" | sed 's/^Exec=//' | sed 's/ %.*//')
  exe=$(echo "$exec_line" | awk '{print $1}')
  if [ -n "$exe" ]; then
    if command -v "$exe" >/dev/nu`

```
8
===== chrome-bfigefacalffjneeeigcpgcijahfbdlf-Default.desktop
Name=Hermes Workspace
Exec=/opt/google/chrome/google-chrome --profile-directory=Default --app-id=bfigefacalffjneeeigcpgcijahfbdlf
  -> EXE OK: /opt/google/chrome/google-chrome
===== chrome-cmkncekebbebpfilplodngbpllndjkfo-Default.desktop
Name=Área de trabalho remota do Google Chrome
Exec=/opt/google/chrome/google-chrome --profile-directory=Default --app-id=cmkncekebbebpfilplodngbpllndjkfo
  -> EXE OK: /opt/google/chrome/google-chrome
===== chrome-fmpnliohjhemenmnlpbfagaolkdacoja-Default.desktop
Name=Claude
Exec=/opt/google/chrome/google-chrome --profile-directory=Default --app-id=fmpnliohjhemenmnlpbfagaolkdacoja
  -> EXE OK: /opt/google/chrome/google-chrome
===== chrome-kajebgjangihfbkjfejcanhanjmmbcfd-Default.desktop
Name=Gerenciador de Senhas do Google
Exec=/opt/google/chrome/google-chrome --profile-directory=Default --app-id=kajebgjangihfbkjfejcanhanjmmbcfd
  -> EXE OK: /opt/google/chrome/google-chrome
===== chrome-ljknakahiebfmdmakamebpbhbikdkjfm-Default.desktop
Name=Airtable
Exec=/opt/google/chrome/google-chrome --profile-directory=Default --app-id=ljknakahiebfmdmakamebpbhbikdkjfm
  -> EXE OK: /opt/google/chrome/google-chrome
===== chrome-obdbcdcjmdahkmldfngnemkgdlnidkbh-Default.desktop
Name=9Router - AI Infrastructure Management
Exec=/opt/google/chrome/google-chrome --profile-directory=Default --app-id=obdbcdcjmdahkmldfngnemkgdlnidkbh
  -> EXE OK: /opt/google/chrome/google-chrome
===== claude-code-url-handler.desktop
Name=Claude Code URL Handler
Exec="/home/dr/.local/bin/claude" --handle-uri %u
  -> EXE NAO ENCONTRADO: "/home/dr/.local/bin/claude"
===== dev.zed.Zed.desktop
Name=Zed
Exec=/home/dr/.local/zed.app/bin/zed %U
Exec=/home/dr/.local/zed.app/bin/zed --new %U
Name=Open a new workspace
  -> EXE OK: /home/dr/.local/zed.app/bin/zed
```

## [a4_claude_handler]
**Comando:** `cat ~/.local/share/applications/claude-code-url-handler.desktop 2>&1 | head -15; echo ---; ls -la ~/.local/bin/claude 2>&1; echo ---; command -v claude; type -a claude 2>&1 | head -5`

```
[Desktop Entry]
Name=Claude Code URL Handler
Comment=Handle claude-cli:// deep links for Claude Code
Exec="/home/dr/.local/bin/claude" --handle-uri %u
Type=Application
NoDisplay=true
MimeType=x-scheme-handler/claude-cli;
---
lrwxrwxrwx 1 dr dr 45 out  2 08:22 /home/dr/.local/bin/claude -> /home/dr/.local/share/claude/versions/2.1.285
---
/home/dr/.local/bin/claude
claude é /home/dr/.local/bin/claude
```

## [a5_nvm_residuo]
**Comando:** `ls -la ~/.config/nvm 2>&1; echo ---; ls -la ~/.local/share/nvm 2>&1 | head -8; echo ---; ls ~/.local/share/nvm/versions/node/ 2>&1`

```
ls: não foi possível acessar '/home/dr/.config/nvm': Arquivo ou diretório inexistente
---
total 340
drwxrwxr-x  7 dr dr   4096 set  7 08:21 .
drwxrwxr-x 40 dr dr   4096 out  7 02:25 ..
drwxrwxr-x  3 dr dr   4096 jun  6 03:42 alias
-rw-rw-r--  1 dr dr   2299 jun  6 03:42 bash_completion
-rw-rw-r--  1 dr dr   7560 jun  6 03:42 CODE_OF_CONDUCT.md
-rw-rw-r--  1 dr dr   4743 jun  6 03:42 CONTRIBUTING.md
-rw-rw-r--  1 dr dr   3600 jun  6 03:42 Dockerfile
---
v24.16.0
```

## [p1_ss_tlnp]
**Comando:** `ss -tlnp 2>&1 | head -50`

```
State  Recv-Q Send-Q               Local Address:Port  Peer Address:PortProcess                                     
LISTEN 0      4096                  100.91.46.87:10000      0.0.0.0:*                                               
LISTEN 0      4096                  100.91.46.87:54584      0.0.0.0:*                                               
LISTEN 0      511                        0.0.0.0:20128      0.0.0.0:*    users:(("next-server (v1",pid=23905,fd=21))
LISTEN 0      4096                     127.0.0.1:20242      0.0.0.0:*    users:(("cloudflared",pid=24062,fd=10))    
LISTEN 0      4096                     127.0.0.1:20241      0.0.0.0:*                                               
LISTEN 0      4096                 127.0.0.53%lo:53         0.0.0.0:*                                               
LISTEN 0      4096                    127.0.0.54:53         0.0.0.0:*                                               
LISTEN 0      4096                  100.91.46.87:443        0.0.0.0:*                                               
LISTEN 0      511                      127.0.0.1:3000       0.0.0.0:*    users:(("node",pid=1916,fd=18))            
LISTEN 0      200                      127.0.0.1:5432       0.0.0.0:*                                               
LISTEN 0      4096                       0.0.0.0:22         0.0.0.0:*                                               
LISTEN 0      128                      127.0.0.1:8642       0.0.0.0:*    users:(("hermes",pid=2768,fd=43))          
LISTEN 0      4096                     127.0.0.1:45351      0.0.0.0:*                                               
LISTEN 0      4096                     127.0.0.1:631        0.0.0.0:*                                               
LISTEN 0      2048                     127.0.0.1:9119       0.0.0.0:*    users:(("hermes",pid=2742,fd=22))          
LISTEN 0      511                          [::1]:3000          [::]:*    users:(("node",pid=1916,fd=19))            
LISTEN 0      4096                         [::1]:631           [::]:*                                               
LISTEN 0      4096   [fd7a:115c:a1e0::2001:2eee]:443           [::]:*                                               
LISTEN 0      4096                          [::]:22            [::]:*                                               
LISTEN 0      4096   [fd7a:115c:a1e0::2001:2eee]:10000         [::]:*                                               
LISTEN 0      4096   [fd7a:115c:a1e0::2001:2eee]:62838         [::]:*                                               
```

## [p2_ss_ulnp]
**Comando:** `ss -ulnp 2>&1 | head -20`

```
State  Recv-Q Send-Q                     Local Address:Port  Peer Address:PortProcess
UNCONN 0      0                             127.0.0.54:53         0.0.0.0:*          
UNCONN 0      0                          127.0.0.53%lo:53         0.0.0.0:*          
UNCONN 0      0                                0.0.0.0:41641      0.0.0.0:*          
UNCONN 0      0                                0.0.0.0:5353       0.0.0.0:*          
UNCONN 0      0                                0.0.0.0:54710      0.0.0.0:*          
UNCONN 0      0                                      *:52343            *:*          
UNCONN 0      0                                      *:56482            *:*          
UNCONN 0      0                                      *:33211            *:*          
UNCONN 0      0      [fe80::f4d1:aa3:c33d:4620]%wlp2s0:546           [::]:*          
UNCONN 0      0                                   [::]:41641         [::]:*          
UNCONN 0      0                                   [::]:5353          [::]:*          
UNCONN 0      0                                      *:42575            *:*          
UNCONN 0      0                                   [::]:51545         [::]:*          
```

## [p3_portmap]
**Comando:** ` ; for pid in $(ls /proc | grep -E "^[0-9]+$"); do ;   [ -r /proc/$pid/cmdline ] || continue ;   cmd=$(tr "\000" " " < /proc/$pid/cmdline 2>/dev/null | cut -c1-90) ;   exe=$(readlink /proc/$pid/exe 2>/dev/null); [ -z "$exe" ] && continue ;   uid=$(awk "/^Uid:/{print \$2}" /proc/$pid/status 2>/dev/null) ;   echo "PID=$pid uid=$uid exe=$exe cmd=$cmd" ; done 2>/dev/null | sort -u ; `

```
bash: -c: linha 1: erro de sintaxe próximo ao token inesperado `;'
bash: -c: linha 1: ` ; for pid in $(ls /proc | grep -E "^[0-9]+$"); do ;   [ -r /proc/$pid/cmdline ] || continue ;   cmd=$(tr "\000" " " < /proc/$pid/cmdline 2>/dev/null | cut -c1-90) ;   exe=$(readli
```

## [p3_portmap]
**Comando:** `for pid in $(ls /proc | grep -E "^[0-9]+$"); do [ -r /proc/$pid/cmdline ] || continue; cmd=$(xargs -0 -a /proc/$pid/cmdline echo 2>/dev/null | cut -c1-90); exe=$(readlink /proc/$pid/exe 2>/dev/null); [ -z "$exe" ] && continue; uid=$(awk "/^Uid:/{print \$2}" /proc/$pid/status 2>/dev/null); echo "PID=$pid uid=$uid exe=$exe cmd=$cmd"; done 2>/dev/null | sort -u`

```
PID=10885 uid=1000 exe=/usr/bin/nemo cmd=/usr/bin/nemo
PID=1143 uid=1000 exe=/usr/bin/pipewire cmd=/usr/bin/pipewire
PID=1144 uid=1000 exe=/usr/bin/pipewire cmd=/usr/bin/pipewire -c filter-chain.conf
PID=1145 uid=1000 exe=/usr/bin/wireplumber cmd=/usr/bin/wireplumber
PID=1146 uid=1000 exe=/usr/bin/pipewire cmd=/usr/bin/pipewire-pulse
PID=1147 uid=1000 exe=/usr/bin/dbus-daemon cmd=/usr/bin/dbus-daemon --session --address=systemd: --nofork --nopidfile --systemd-activatio
PID=1253 uid=1000 exe=/usr/libexec/xdg-permission-store cmd=/usr/libexec/xdg-permission-store
PID=1304 uid=1000 exe=/usr/lib/x86_64-linux-gnu/cinnamon-session-binary cmd=/usr/lib/x86_64-linux-gnu/cinnamon-session-binary --session cinnamon
PID=1466 uid=1000 exe=/usr/bin/ibus-daemon cmd=/usr/bin/ibus-daemon --daemonize --xim
PID=1507 uid=1000 exe=/usr/libexec/gvfsd cmd=/usr/libexec/gvfsd
PID=1540 uid=1000 exe=/usr/libexec/gvfsd-fuse cmd=/usr/libexec/gvfsd-fuse /run/user/1000/gvfs -f
PID=1545 uid=1000 exe=/usr/libexec/ibus-dconf cmd=/usr/libexec/ibus-dconf
PID=1549 uid=1000 exe=/usr/libexec/ibus-ui-gtk3 cmd=/usr/libexec/ibus-ui-gtk3
PID=1550 uid=1000 exe=/usr/libexec/ibus-extension-gtk3 cmd=/usr/libexec/ibus-extension-gtk3
PID=1559 uid=1000 exe=/usr/libexec/ibus-x11 cmd=/usr/libexec/ibus-x11 --kill-daemon
PID=1564 uid=1000 exe=/usr/libexec/ibus-portal cmd=/usr/libexec/ibus-portal
PID=1580 uid=1000 exe=/usr/bin/gnome-keyring-daemon cmd=/usr/bin/gnome-keyring-daemon --foreground --components=pkcs11,secrets --control-directory
PID=1598 uid=1000 exe=/usr/libexec/csd-print-notifications cmd=/usr/bin/csd-print-notifications
PID=1601 uid=1000 exe=/usr/libexec/csd-xsettings cmd=/usr/bin/csd-xsettings
PID=1603 uid=1000 exe=/usr/libexec/csd-wacom cmd=/usr/bin/csd-wacom
PID=1605 uid=1000 exe=/usr/libexec/csd-clipboard cmd=/usr/bin/csd-clipboard
PID=1610 uid=1000 exe=/usr/libexec/csd-keyboard cmd=/usr/bin/csd-keyboard
PID=1612 uid=1000 exe=/usr/libexec/at-spi-bus-launcher cmd=/usr/libexec/at-spi-bus-launcher --launch-immediately
PID=1621 uid=1000 exe=/usr/libexec/csd-housekeeping cmd=/usr/bin/csd-housekeeping
PID=1625 uid=1000 exe=/usr/libexec/csd-background cmd=/usr/bin/csd-background
PID=1627 uid=1000 exe=/usr/libexec/csd-power cmd=/usr/bin/csd-power
PID=1632 uid=1000 exe=/usr/libexec/csd-media-keys cmd=/usr/bin/csd-media-keys
PID=1637 uid=1000 exe=/usr/libexec/csd-settings-remap cmd=/usr/bin/csd-settings-remap
PID=1651 uid=1000 exe=/usr/bin/dbus-daemon cmd=/usr/bin/dbus-daemon --config-file=/usr/share/defaults/at-spi2/accessibility.conf --nofork
PID=1652 uid=1000 exe=/usr/libexec/csd-a11y-settings cmd=/usr/bin/csd-a11y-settings
PID=1654 uid=1000 exe=/usr/libexec/csd-color cmd=/usr/bin/csd-color
PID=1661 uid=1000 exe=/usr/libexec/csd-automount cmd=/usr/bin/csd-automount
PID=1663 uid=1000 exe=/usr/libexec/csd-screensaver-proxy cmd=/usr/bin/csd-screensaver-proxy
PID=1691 uid=1000 exe=/usr/libexec/dconf-service cmd=/usr/libexec/dconf-service
PID=1865 uid=1000 exe=/usr/libexec/at-spi2-registryd cmd=/usr/libexec/at-spi2-registryd --use-gnome-session
PID=18790 uid=1000 exe=/opt/google/chrome/chrome cmd=/opt/google/chrome/chrome --type=renderer --crashpad-handler-pid=6340 --enable-crash-repor
PID=18823 uid=1000 exe=/opt/google/chrome/chrome cmd=/opt/google/chrome/chrome --type=renderer --crashpad-handler-pid=6340 --enable-crash-repor
PID=18858 uid=1000 exe=/opt/google/chrome/chrome cmd=/opt/google/chrome/chrome --type=renderer --crashpad-handler-pid=6340 --enable-crash-repor
PID=1916 uid=1000 exe=/usr/local/bin/node cmd=node --max-old-space-size=2048 server-entry.js
PID=19179 uid=1000 exe=/opt/google/chrome/chrome cmd=/opt/google/chrome/chrome --type=renderer --crashpad-handler-pid=6340 --enable-crash-repor
PID=1989 uid=1000 exe=/usr/libexec/gvfs-udisks2-volume-monitor cmd=/usr/libexec/gvfs-udisks2-volume-monitor
PID=1996 uid=1000 exe=/usr/libexec/gvfs-afc-volume-monitor cmd=/usr/libexec/gvfs-afc-volume-monitor
PID=2003 uid=1000 exe=/usr/libexec/gvfs-mtp-volume-monitor cmd=/usr/libexec/gvfs-mtp-volume-monitor
PID=2014 uid=1000 exe=/usr/libexec/gvfs-gphoto2-volume-monitor cmd=/usr/libexec/gvfs-gphoto2-volume-monitor
PID=2027 uid=1000 exe=/usr/libexec/gvfs-goa-volume-monitor cmd=/usr/libexec/gvfs-goa-volume-monitor
PID=2033 uid=1000 exe=/usr/libexec/goa-daemon cmd=/usr/libexec/goa-daemon
PID=2040 uid=1000 exe=/usr/libexec/csd-printer cmd=/usr/libexec/csd-printer
PID=2047 uid=1000 exe=/usr/bin/python3.12 cmd=cinnamon-launcher                          
PID=20529 uid=1000 exe=/usr/libexec/gvfsd-network cmd=/usr/libexec/gvfsd-network --spawner :1.16 /org/gtk/gvfs/exec_spaw/1
PID=20538 uid=1000 exe=/usr/libexec/gvfsd-dnssd cmd=/usr/libexec/gvfsd-dnssd --spawner :1.16 /org/gtk/gvfs/exec_spaw/2
PID=2076 uid=1000 exe=/usr/libexec/goa-identity-service cmd=/usr/libexec/goa-identity-service
PID=2157 uid=1000 exe=/usr/libexec/ibus-engine-simple cmd=/usr/libexec/ibus-engine-simple
PID=21600 uid=1000 exe=/usr/libexec/gnome-terminal-server cmd=/usr/libexec/gnome-terminal-server
PID=21612 uid=1000 exe=/usr/bin/bash cmd=bash
PID=2170 uid=1000 exe=/usr/bin/cinnamon cmd=cinnamon --replace
PID=21856 uid=1000 exe=/usr/bin/docker cmd=docker exec -it hermes-agent hermes
PID=21889 uid=1000 exe=/usr/bin/python3.13 cmd=/opt/hermes/.venv/bin/python3 /opt/hermes/.venv/bin/hermes
PID=22172 uid=1000 exe=/usr/local/bin/node cmd=node /opt/data/.npm/_npx/f36605d6814ff2b0/node_modules/.bin/obsidian-mcp-server
PID=22178 uid=1000 exe=/usr/local/bin/node cmd=node /opt/data/.npm/_npx/3dfbf5a9eea4a1b3/node_modules/.bin/mcp-server-github
PID=22186 uid=1000 exe=/usr/local/bin/node cmd=node /opt/data/.npm/_npx/a3241bba59c344f5/node_modules/.bin/mcp-server-filesystem /home/dr
PID=22194 uid=1000 exe=/usr/bin/python3.13 cmd=/opt/hermes/.venv/bin/python3 /opt/hermes/tools/mcp_death_supervisor.py --parent-pgid 3147
PID=22349 uid=1000 exe=/usr/libexec/gvfsd-http cmd=/usr/libexec/gvfsd-http --spawner :1.16 /org/gtk/gvfs/exec_spaw/5
PID=22379 uid=1000 exe=/opt/google/chrome/chrome cmd=/opt/google/chrome/chrome --type=renderer --crashpad-handler-pid=6340 --enable-crash-repor
PID=2259 uid=1000 exe=/usr/libexec/geoclue-2.0/demos/agent cmd=/usr/libexec/geoclue-2.0/demos/agent
PID=2261 uid=1000 exe=/usr/libexec/evolution-data-server/evolution-alarm-notify cmd=/usr/libexec/evolution-data-server/evolution-alarm-notify
PID=2270 uid=1000 exe=/usr/bin/bwrap cmd=bwrap --args 40 -- bitwarden.sh --autostart
PID=2271 uid=1000 exe=/usr/bin/nemo-desktop cmd=/usr/bin/nemo-desktop
PID=2278 uid=1000 exe=/usr/bin/python3.12 cmd=cinnamon-killer-daemon                          
PID=2330 uid=1000 exe=/usr/libexec/evolution-source-registry cmd=/usr/libexec/evolution-source-registry
PID=2343 uid=1000 exe=/usr/libexec/gvfsd-metadata cmd=/usr/libexec/gvfsd-metadata
PID=2353 uid=1000 exe=/usr/libexec/evolution-calendar-factory cmd=/usr/libexec/evolution-calendar-factory
PID=23785 uid=1000 exe=/opt/google/chrome/chrome cmd=/opt/google/chrome/chrome --type=utility --utility-sub-type=network.mojom.NetworkService -
PID=23840 uid=1000 exe=/home/dr/.local/share/nvm/versions/node/v24.16.0/bin/node cmd=/home/dr/.local/share/nvm/versions/node/v24.16.0/bin/node /home/dr/.local/lib/node_modules
PID=23905 uid=1000 exe=/home/dr/.local/share/nvm/versions/node/v24.16.0/bin/node cmd=next-server (v16.3.4)                                                                     
PID=23921 uid=1000 exe=/home/dr/.cache/node-systray/2.1.4/tray_linux_release cmd=/home/dr/.cache/node-systray/2.1.4/tray_linux_release
PID=23941 uid=1000 exe=/usr/lib/claude-desktop/resources/chrome-native-host cmd=/usr/lib/claude-desktop/resources/chrome-native-host chrome-extension://fcoeoabgfenejglbff
PID=24007 uid=1000 exe=/opt/google/chrome/chrome cmd=/opt/google/chrome/chrome --type=renderer --crashpad-handler-pid=6340 --enable-crash-repor
PID=24062 uid=1000 exe=/home/dr/.local/share/9router/bin/cloudflared cmd=/home/dr/.local/share/9router/bin/cloudflared tunnel --url http://127.0.0.1:20128 --config
PID=2440 uid=1000 exe=/usr/libexec/gvfsd-trash cmd=/usr/libexec/gvfsd-trash --spawner :1.16 /org/gtk/gvfs/exec_spaw/0
PID=2451 uid=1000 exe=/usr/libexec/evolution-addressbook-factory cmd=/usr/libexec/evolution-addressbook-factory
PID=2515 uid=1000 exe=/usr/libexec/flatpak-session-helper cmd=/usr/libexec/flatpak-session-helper
PID=2520 uid=1000 exe=/usr/libexec/p11-kit/p11-kit-server cmd=server --sh -n /run/user/1000/.flatpak-helper/pkcs11-flatpak-2515 --provider p11-kit-trust
PID=2522 uid=1000 exe=/usr/libexec/xdg-document-portal cmd=/usr/libexec/xdg-document-portal
PID=2532 uid=1000 exe=/usr/bin/bwrap cmd=bwrap --args 40 -- xdg-dbus-proxy --args=43
PID=2533 uid=1000 exe=/usr/bin/xdg-dbus-proxy cmd=xdg-dbus-proxy --args=43
PID=2544 uid=1000 exe=/usr/bin/bwrap cmd=bwrap --args 40 -- bitwarden.sh --autostart
PID=2546 uid=1000 exe=/app/Bitwarden/bitwarden-app cmd=/app/Bitwarden/bitwarden-app --autostart --enable-features=UseOzonePlatform --ozone-platfo
PID=2551 uid=1000 exe=/usr/libexec/flatpak-portal cmd=/usr/libexec/flatpak-portal
PID=2558 uid=1000 exe=/app/Bitwarden/bitwarden-app cmd=/app/Bitwarden/bitwarden-app --type=zygote --no-zygote-sandbox
PID=2562 uid=1000 exe=/usr/bin/cat cmd=cat
PID=2563 uid=1000 exe=/usr/bin/cat cmd=cat
PID=2564 uid=1000 exe=/usr/bin/bwrap cmd=bwrap --args 43 -- /app/bin/zypak-helper child - /app/Bitwarden/bitwarden-app --type=zygot
PID=2578 uid=1000 exe=/usr/bin/bwrap cmd=bwrap --args 43 -- /app/bin/zypak-helper child - /app/Bitwarden/bitwarden-app --type=zygot
PID=2579 uid=1000 exe=/app/Bitwarden/bitwarden-app cmd=/app/Bitwarden/bitwarden-app --type=zygote
PID=2608 uid=1000 exe=/app/Bitwarden/bitwarden-app cmd=/app/Bitwarden/bitwarden-app --type=gpu-process --ozone-platform=x11 --enable-crash-report
PID=2614 uid=1000 exe=/app/Bitwarden/bitwarden-app cmd=/app/Bitwarden/bitwarden-app --type=utility --utility-sub-type=network.mojom.NetworkServic
PID=2629 uid=1000 exe=/usr/libexec/xdg-desktop-portal cmd=/usr/libexec/xdg-desktop-portal
PID=2634 uid=1000 exe=/usr/libexec/xdg-desktop-portal-xapp cmd=/usr/libexec/xdg-desktop-portal-xapp
PID=2644 uid=1000 exe=/usr/libexec/xdg-desktop-portal-gtk cmd=/usr/libexec/xdg-desktop-portal-gtk
PID=2649 uid=1000 exe=/app/Bitwarden/bitwarden-app cmd=/app/Bitwarden/bitwarden-app --type=renderer --enable-crash-reporter=36d9b6c5-c871-44dc-89
PID=2742 uid=1000 exe=/usr/bin/python3.13 cmd=/opt/hermes/.venv/bin/python3 /opt/hermes/.venv/bin/hermes dashboard --host 127.0.0.1 --po
PID=2765 uid=1000 exe=/package/admin/s6-2.15.0.0/command/s6-log cmd=s6-log 1 n10 s1000000 T /home/dr/.hermes/logs/gateways/evidencia
PID=2766 uid=1000 exe=/package/admin/s6-2.15.0.0/command/s6-log cmd=s6-log 1 n10 s1000000 T /home/dr/.hermes/logs/gateways/fiscal
PID=2768 uid=1000 exe=/usr/bin/python3.13 cmd=/opt/hermes/.venv/bin/python3 /opt/hermes/.venv/bin/hermes gateway run --replace
PID=2776 uid=1000 exe=/package/admin/s6-2.15.0.0/command/s6-log cmd=s6-log 1 n10 s1000000 T /home/dr/.hermes/logs/gateways/chefe
PID=2777 uid=1000 exe=/package/admin/s6-2.15.0.0/command/s6-log cmd=s6-log 1 n10 s1000000 T /home/dr/.hermes/logs/gateways/secretaria
PID=2778 uid=1000 exe=/package/admin/s6-2.15.0.0/command/s6-log cmd=s6-log 1 n10 s1000000 T /home/dr/.hermes/logs/gateways/default
PID=2784 uid=1000 exe=/package/admin/s6-2.15.0.0/command/s6-log cmd=s6-log 1 n10 s1000000 T /home/dr/.hermes/logs/gateways/residente
PID=2800 uid=1000 exe=/usr/bin/sleep cmd=sleep infinity
PID=2894 uid=1000 exe=/usr/local/bin/node cmd=node /opt/data/.npm/_npx/3dfbf5a9eea4a1b3/node_modules/.bin/mcp-server-github
PID=2895 uid=1000 exe=/usr/bin/python3.13 cmd=/opt/hermes/.venv/bin/python3 /opt/hermes/tools/mcp_death_supervisor.py --parent-pgid 145
PID=2905 uid=1000 exe=/usr/local/bin/node cmd=node /opt/data/.npm/_npx/a3241bba59c344f5/node_modules/.bin/mcp-server-filesystem /home/dr
PID=2914 uid=1000 exe=/usr/local/bin/node cmd=node /opt/data/.npm/_npx/f36605d6814ff2b0/node_modules/.bin/obsidian-mcp-server
PID=2970 uid=1000 exe=/usr/local/bin/node cmd=node /opt/data/.npm/_npx/f36605d6814ff2b0/node_modules/.bin/obsidian-mcp-server
PID=2972 uid=1000 exe=/usr/local/bin/node cmd=node /opt/data/.npm/_npx/3dfbf5a9eea4a1b3/node_modules/.bin/mcp-server-github
PID=2973 uid=1000 exe=/usr/local/bin/node cmd=node /opt/data/.npm/_npx/a3241bba59c344f5/node_modules/.bin/mcp-server-filesystem /home/dr
PID=2991 uid=1000 exe=/usr/bin/python3.13 cmd=/opt/hermes/.venv/bin/python3 /opt/hermes/tools/mcp_death_supervisor.py --parent-pgid 171
PID=32918 uid=1000 exe=/usr/bin/python3.13 cmd=/opt/hermes/.venv/bin/python3 /tmp/hermes_kernel_vxf7rron/hermes_kernel_runner.py
PID=3388 uid=1000 exe=/usr/libexec/p11-kit/p11-kit-remote cmd=p11-kit-remote --provider p11-kit-trust.so pkcs11:model=p11-kit-trust?write-protected=yes
PID=39213 uid=1000 exe=/usr/bin/python3.12 cmd=cinnamon-screensaver                                                         
PID=40458 uid=1000 exe=/usr/bin/python3.13 cmd=/opt/hermes/.venv/bin/python3 /tmp/hermes_kernel_u4b__xep/hermes_kernel_runner.py
PID=45465 uid=1000 exe=/usr/bin/python3.13 cmd=/opt/hermes/.venv/bin/python3 /tmp/hermes_kernel_gc4jhxhk/hermes_kernel_runner.py
PID=51091 uid=1000 exe=/usr/bin/python3.13 cmd=/opt/hermes/.venv/bin/python3 /tmp/hermes_kernel_5qtj1uw5/hermes_kernel_runner.py
PID=58480 uid=1000 exe=/usr/bin/ssh cmd=ssh -i /home/dr/.hermes/home/.ssh/id_ed25519 -o BatchMode=yes -o StrictHostKeyChecking=no 
PID=58497 uid=1000 exe=/usr/bin/bash cmd=bash -c for pid in $(ls /proc | grep -E "^[0-9]+$"); do [ -r /proc/$pid/cmdline ] || conti
PID=58801 uid=1000 exe=/usr/bin/bash cmd=bash -c for pid in $(ls /proc | grep -E "^[0-9]+$"); do [ -r /proc/$pid/cmdline ] || conti
PID=58802 uid=1000 exe=/usr/bin/sort cmd=sort -u
PID=6332 uid=1000 exe=/opt/google/chrome/chrome cmd=/opt/google/chrome/chrome
PID=6337 uid=1000 exe=/usr/bin/cat cmd=cat
PID=6338 uid=1000 exe=/usr/bin/cat cmd=cat
PID=6340 uid=1000 exe=/opt/google/chrome/chrome_crashpad_handler cmd=/opt/google/chrome/chrome_crashpad_handler --monitor-self --monitor-self-annotation=ptype=
PID=6342 uid=1000 exe=/opt/google/chrome/chrome_crashpad_handler cmd=/opt/google/chrome/chrome_crashpad_handler --no-periodic-tasks --monitor-self-annotation=p
PID=6348 uid=1000 exe=/opt/google/chrome/chrome cmd=/opt/google/chrome/chrome --type=zygote --no-zygote-sandbox --crashpad-handler-pid=6340 --
PID=6349 uid=1000 exe=/opt/google/chrome/chrome cmd=/opt/google/chrome/chrome --type=zygote --crashpad-handler-pid=6340 --enable-crash-reporte
PID=6351 uid=1000 exe=/opt/google/chrome/chrome cmd=/opt/google/chrome/chrome --type=zygote --crashpad-handler-pid=6340 --enable-crash-reporte
PID=6377 uid=1000 exe=/opt/google/chrome/chrome cmd=/opt/google/chrome/chrome --type=gpu-process --gpu-recent-crash-count=0 --ozone-platform=x
PID=6401 uid=1000 exe=/opt/google/chrome/chrome cmd=/opt/google/chrome/chrome --type=utility --utility-sub-type=storage.mojom.StorageService -
PID=6444 uid=1000 exe=/opt/google/chrome/chrome cmd=/opt/google/chrome/chrome --type=renderer --top-chrome-webui --crashpad-handler-pid=6340 -
PID=6518 uid=1000 exe=/opt/google/chrome/chrome cmd=/opt/google/chrome/chrome --type=renderer --crashpad-handler-pid=6340 --enable-crash-repor
```

## [p4_ss_full]
**Comando:** `ss -tlnp 2>&1`

```
State  Recv-Q Send-Q               Local Address:Port  Peer Address:PortProcess                                     
LISTEN 0      4096                  100.91.46.87:10000      0.0.0.0:*                                               
LISTEN 0      4096                  100.91.46.87:54584      0.0.0.0:*                                               
LISTEN 0      511                        0.0.0.0:20128      0.0.0.0:*    users:(("next-server (v1",pid=23905,fd=21))
LISTEN 0      4096                     127.0.0.1:20242      0.0.0.0:*    users:(("cloudflared",pid=24062,fd=10))    
LISTEN 0      4096                     127.0.0.1:20241      0.0.0.0:*                                               
LISTEN 0      4096                 127.0.0.53%lo:53         0.0.0.0:*                                               
LISTEN 0      4096                    127.0.0.54:53         0.0.0.0:*                                               
LISTEN 0      4096                  100.91.46.87:443        0.0.0.0:*                                               
LISTEN 0      511                      127.0.0.1:3000       0.0.0.0:*    users:(("node",pid=1916,fd=18))            
LISTEN 0      200                      127.0.0.1:5432       0.0.0.0:*                                               
LISTEN 0      4096                       0.0.0.0:22         0.0.0.0:*                                               
LISTEN 0      128                      127.0.0.1:8642       0.0.0.0:*    users:(("hermes",pid=2768,fd=43))          
LISTEN 0      4096                     127.0.0.1:45351      0.0.0.0:*                                               
LISTEN 0      4096                     127.0.0.1:631        0.0.0.0:*                                               
LISTEN 0      2048                     127.0.0.1:9119       0.0.0.0:*    users:(("hermes",pid=2742,fd=22))          
LISTEN 0      511                          [::1]:3000          [::]:*    users:(("node",pid=1916,fd=19))            
LISTEN 0      4096                         [::1]:631           [::]:*                                               
LISTEN 0      4096   [fd7a:115c:a1e0::2001:2eee]:443           [::]:*                                               
LISTEN 0      4096                          [::]:22            [::]:*                                               
LISTEN 0      4096   [fd7a:115c:a1e0::2001:2eee]:10000         [::]:*                                               
LISTEN 0      4096   [fd7a:115c:a1e0::2001:2eee]:62838         [::]:*                                               
```

## [p6_ps_aux_key]
**Comando:** `ps aux --sort=-rss 2>&1 | head -45`

```
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
dr         18790  1.6  7.7 1526487424 617772 ?   Sl   02:17   1:00 /opt/google/chrome/chrome --type=renderer --crashpad-handler-pid=6340 --enable-crash-reporter=10e07c55-073f-474b-ad01-082af193f891, --change-stack-guard-
dr          6332  0.9  5.1 55625544 414332 ?     Sl   01:38   0:58 /opt/google/chrome/chrome
dr         21889  4.2  4.1 2633292 329900 pts/0  Ssl+ 02:25   2:13 /opt/hermes/.venv/bin/python3 /opt/hermes/.venv/bin/hermes
dr          6377  0.9  3.3 55502144 270440 ?     Sl   01:38   0:57 /opt/google/chrome/chrome --type=gpu-process --gpu-recent-crash-count=0 --ozone-platform=x11 --crashpad-handler-pid=6340 --enable-crash-reporter=10e07c55
dr          2768  0.7  2.9 1423020 236804 ?      Ssl  01:26   0:51 /opt/hermes/.venv/bin/python3 /opt/hermes/.venv/bin/hermes gateway run --replace
dr         19179  1.4  2.8 1518461520 229884 ?   Sl   02:18   0:52 /opt/google/chrome/chrome --type=renderer --crashpad-handler-pid=6340 --enable-crash-reporter=10e07c55-073f-474b-ad01-082af193f891, --change-stack-guard-
dr          2742  0.7  2.7 1041344 221008 ?      Ssl  01:26   0:52 /opt/hermes/.venv/bin/python3 /opt/hermes/.venv/bin/hermes dashboard --host 127.0.0.1 --port 9119 --no-open
dr          2649  0.0  2.7 1518337236 218428 ?   Sl   01:26   0:04 /app/Bitwarden/bitwarden-app --type=renderer --enable-crash-reporter=36d9b6c5-c871-44dc-8992-69be3fa3a425,no_channel --user-data-dir=/home/dr/.var/app/co
dr         22379  0.1  2.6 1518413024 211528 ?   Sl   02:25   0:05 /opt/google/chrome/chrome --type=renderer --crashpad-handler-pid=6340 --enable-crash-reporter=10e07c55-073f-474b-ad01-082af193f891, --change-stack-guard-
dr          2546  0.0  2.6 1518610692 208248 ?   SLl  01:26   0:02 /app/Bitwarden/bitwarden-app --autostart --enable-features=UseOzonePlatform --ozone-platform=x11
dr         18823  0.1  2.4 1518407372 193296 ?   Sl   02:17   0:03 /opt/google/chrome/chrome --type=renderer --crashpad-handler-pid=6340 --enable-crash-reporter=10e07c55-073f-474b-ad01-082af193f891, --change-stack-guard-
dr          2170  1.5  2.3 4445680 188440 ?      Sl   01:26   1:43 cinnamon --replace
dr          6444  0.0  2.1 1518389308 173720 ?   Sl   01:38   0:01 /opt/google/chrome/chrome --type=renderer --top-chrome-webui --crashpad-handler-pid=6340 --enable-crash-reporter=10e07c55-073f-474b-ad01-082af193f891, --
dr         23905  1.0  2.0 10194056 163312 ?     Ssl  02:29   0:30 next-server (v16.3.4)
dr          1916  0.0  1.8 11678928 149484 ?     Sl   01:26   0:05 node --max-old-space-size=2048 server-entry.js
root        1119  0.6  1.8 1874408 146496 tty7   Ssl+ 01:26   0:46 /usr/lib/xorg/Xorg -core :0 -seat seat0 -auth /var/run/lightdm/root/:0 -nolisten tcp vt7 -novtswitch
dr         23785  0.0  1.7 54984760 139892 ?     Sl   02:29   0:01 /opt/google/chrome/chrome --type=utility --utility-sub-type=network.mojom.NetworkService --lang=pt-BR --service-sandbox-type=none --crashpad-handler-pid=
dr          6518  0.0  1.6 1520353660 135852 ?   Sl   01:38   0:01 /opt/google/chrome/chrome --type=renderer --crashpad-handler-pid=6340 --enable-crash-reporter=10e07c55-073f-474b-ad01-082af193f891, --extension-process -
dr         18858  0.0  1.6 1518373924 132924 ?   Sl   02:17   0:00 /opt/google/chrome/chrome --type=renderer --crashpad-handler-pid=6340 --enable-crash-reporter=10e07c55-073f-474b-ad01-082af193f891, --change-stack-guard-
dr          2970  0.0  1.5 3295160 127328 ?      Ssl  01:27   0:01 node /opt/data/.npm/_npx/f36605d6814ff2b0/node_modules/.bin/obsidian-mcp-server
dr         22172  0.0  1.5 3293684 127260 ?      Ssl  02:25   0:01 node /opt/data/.npm/_npx/f36605d6814ff2b0/node_modules/.bin/obsidian-mcp-server
dr          2608  0.0  1.5 55141484 126984 ?     Sl   01:26   0:00 /app/Bitwarden/bitwarden-app --type=gpu-process --ozone-platform=x11 --enable-crash-reporter=36d9b6c5-c871-44dc-8992-69be3fa3a425,no_channel --user-data-
dr          2914  0.0  1.5 3295104 126904 ?      Ssl  01:27   0:01 node /opt/data/.npm/_npx/f36605d6814ff2b0/node_modules/.bin/obsidian-mcp-server
root        1278  0.1  1.1 2803332 92328 ?       Ssl  01:26   0:07 /usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock
dr          1549  0.0  1.1 803532 92172 ?        Sl   01:26   0:00 /usr/libexec/ibus-ui-gtk3
dr         24007  0.0  1.0 1518365148 84032 ?    Sl   02:29   0:00 /opt/google/chrome/chrome --type=renderer --crashpad-handler-pid=6340 --enable-crash-reporter=10e07c55-073f-474b-ad01-082af193f891, --change-stack-guard-
dr          1550  0.0  1.0 722428 82728 ?        Sl   01:26   0:04 /usr/libexec/ibus-extension-gtk3
dr          1625  0.0  1.0 781984 80576 ?        Sl   01:26   0:00 /usr/bin/csd-background
dr          1654  0.0  0.9 950784 77180 ?        Sl   01:26   0:00 /usr/bin/csd-color
dr          1601  0.0  0.9 717056 77176 ?        Sl   01:26   0:00 /usr/bin/csd-xsettings
dr          2614  0.0  0.9 54870796 76796 ?      Sl   01:26   0:00 /app/Bitwarden/bitwarden-app --type=utility --utility-sub-type=network.mojom.NetworkService --lang=pt-BR --service-sandbox-type=none --enable-crash-repor
dr          1627  0.0  0.9 789916 76196 ?        Sl   01:26   0:00 /usr/bin/csd-power
dr          1661  0.0  0.9 788864 75280 ?        Sl   01:26   0:00 /usr/bin/csd-automount
dr          1603  0.0  0.9 715380 75064 ?        Sl   01:26   0:00 /usr/bin/csd-wacom
dr         10885  0.0  0.9 864356 75060 ?        Sl   01:51   0:04 /usr/bin/nemo
dr          1559  0.0  0.9 641252 74800 ?        Sl   01:26   0:00 /usr/libexec/ibus-x11 --kill-daemon
dr          1621  0.0  0.9 714972 74780 ?        Sl   01:26   0:00 /usr/bin/csd-housekeeping
dr          1610  0.0  0.9 788636 74712 ?        Sl   01:26   0:00 /usr/bin/csd-keyboard
dr          1605  0.0  0.9 640708 74196 ?        Sl   01:26   0:00 /usr/bin/csd-clipboard
dr          2972  0.0  0.9 1500900 73756 ?       Ssl  01:27   0:00 node /opt/data/.npm/_npx/3dfbf5a9eea4a1b3/node_modules/.bin/mcp-server-github
dr         22178  0.0  0.9 1500888 73540 ?       Ssl  02:25   0:00 node /opt/data/.npm/_npx/3dfbf5a9eea4a1b3/node_modules/.bin/mcp-server-github
dr          2894  0.0  0.8 1501396 71972 ?       Ssl  01:27   0:00 node /opt/data/.npm/_npx/3dfbf5a9eea4a1b3/node_modules/.bin/mcp-server-github
dr          6348  0.0  0.8 54988540 70232 ?      S    01:38   0:00 /opt/google/chrome/chrome --type=zygote --no-zygote-sandbox --crashpad-handler-pid=6340 --enable-crash-reporter=10e07c55-073f-474b-ad01-082af193f891, --c
dr          6349  0.0  0.8 54988528 70096 ?      S    01:38   0:00 /opt/google/chrome/chrome --type=zygote --crashpad-handler-pid=6340 --enable-crash-reporter=10e07c55-073f-474b-ad01-082af193f891, --change-stack-guard-on
```

## [p7_ps_rest]
**Comando:** `ps aux 2>&1 | grep -vE 'chrome|Bitwarden' | grep -E 'node|docker|hermes|ollama|next|tailscale|cloudflared|postgres|9router|n8n' | head -25`

```
root        1050  0.0  0.5 1355856 44584 ?       Ssl  01:26   0:02 /usr/sbin/tailscaled --state=/var/lib/tailscale/tailscaled.state --socket=/run/tailscale/tailscaled.sock --port=4
postgres    1110  0.0  0.3 225492 30524 ?        Ss   01:26   0:00 /usr/lib/postgresql/16/bin/postgres -D /var/lib/postgresql/16/main -c config_file=/etc/postgresql/16/main/postgre
postgres    1129  0.0  0.1 225624  8772 ?        Ss   01:26   0:00 postgres: 16/main: checkpointer 
postgres    1130  0.0  0.0 225648  7500 ?        Ss   01:26   0:00 postgres: 16/main: background writer 
postgres    1132  0.0  0.1 225492 10320 ?        Ss   01:26   0:00 postgres: 16/main: walwriter 
postgres    1133  0.0  0.1 227100  8668 ?        Ss   01:26   0:00 postgres: 16/main: autovacuum launcher 
postgres    1134  0.0  0.1 227076  8004 ?        Ss   01:26   0:00 postgres: 16/main: logical replication launcher 
root        1278  0.1  1.1 2803332 92328 ?       Ssl  01:26   0:07 /usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock
root        1821  0.0  0.0   2496  1028 ?        Ss   01:26   0:00 /usr/bin/tini -- /usr/local/bin/docker-entrypoint.sh node --max-old-space-size=2048 server-entry.js
dr          1916  0.0  1.8 11678928 147564 ?     Sl   01:26   0:05 node --max-old-space-size=2048 server-entry.js
root        2058  0.0  0.0   2680  1648 ?        Ss   01:26   0:00 /bin/sh -e /run/s6/basedir/scripts/rc.init top /opt/hermes/docker/main-wrapper.sh gateway run --replace
root        2080  0.0  0.0    232    68 ?        S    01:26   0:00 s6-supervise main-hermes
root        2238  0.2  0.3 1295280 24312 ?       Ssl  01:26   0:13 /usr/bin/cloudflared --no-autoupdate tunnel run --token-file /etc/cloudflared/token
root        2528  0.0  0.0   2716  2040 ?        Ss   01:26   0:00 fusermount3 -o rw,nosuid,nodev,fsname=portal,auto_unmount,subtype=portal -- /run/user/1000/doc
dr          2742  0.7  2.7 1041344 220928 ?      Ssl  01:26   0:52 /opt/hermes/.venv/bin/python3 /opt/hermes/.venv/bin/hermes dashboard --host 127.0.0.1 --port 9119 --no-open
dr          2765  0.0  0.0    296   132 ?        Ss   01:26   0:00 s6-log 1 n10 s1000000 T /home/dr/.hermes/logs/gateways/evidencia
dr          2766  0.0  0.0    296   132 ?        Ss   01:26   0:00 s6-log 1 n10 s1000000 T /home/dr/.hermes/logs/gateways/fiscal
dr          2768  0.7  2.9 1423020 236736 ?      Ssl  01:26   0:51 /opt/hermes/.venv/bin/python3 /opt/hermes/.venv/bin/hermes gateway run --replace
dr          2776  0.0  0.0    296   120 ?        Ss   01:26   0:00 s6-log 1 n10 s1000000 T /home/dr/.hermes/logs/gateways/chefe
dr          2777  0.0  0.0    296   132 ?        Ss   01:26   0:00 s6-log 1 n10 s1000000 T /home/dr/.hermes/logs/gateways/secretaria
dr          2778  0.0  0.0    320   152 ?        Ss   01:26   0:00 s6-log 1 n10 s1000000 T /home/dr/.hermes/logs/gateways/default
dr          2784  0.0  0.0    296   132 ?        Ss   01:26   0:00 s6-log 1 n10 s1000000 T /home/dr/.hermes/logs/gateways/residente
dr          2894  0.0  0.8 1501396 71972 ?       Ssl  01:27   0:00 node /opt/data/.npm/_npx/3dfbf5a9eea4a1b3/node_modules/.bin/mcp-server-github
dr          2895  0.0  0.1  20116 14520 ?        Ss   01:27   0:00 /opt/hermes/.venv/bin/python3 /opt/hermes/tools/mcp_death_supervisor.py --parent-pgid 145
dr          2905  0.0  0.8 1523560 68964 ?       Ssl  01:27   0:00 node /opt/data/.npm/_npx/a3241bba59c344f5/node_modules/.bin/mcp-server-filesystem /home/dr
```

## [p8_docker_ps]
**Comando:** `docker ps --format '{{.Names}} | {{.Image}} | {{.Ports}} | {{.Status}}' 2>&1 | head -10`

```
hermes-workspace | hermes-workspace:tijolao |  | Up 2 hours (healthy)
hermes-agent | nousresearch/hermes-agent:latest |  | Up 2 hours (healthy)
```

## [p9_pids_dos_sockets]
**Comando:** `
for pid in 1916 23905 24062 2768 2742; do
  echo "PID $pid:"
  echo "  exe=$(readlink /proc/$pid/exe 2>&1)"
  echo "  cwd=$(readlink /proc/$pid/cwd 2>&1)"
  xargs -0 -a /proc/$pid/cmdline echo 2>/dev/null | head -1
done`

```
PID 1916:
  exe=/usr/local/bin/node
  cwd=/app
node --max-old-space-size=2048 server-entry.js
PID 23905:
  exe=/home/dr/.local/share/nvm/versions/node/v24.16.0/bin/node
  cwd=/home/dr/.local/lib/node_modules/9router/app
next-server (v16.3.4)                                                                                                                                                         
PID 24062:
  exe=/home/dr/.local/share/9router/bin/cloudflared
  cwd=/tmp
/home/dr/.local/share/9router/bin/cloudflared tunnel --url http://127.0.0.1:20128 --config /tmp/cloudflared-quick-XFpbCK/config.yml --no-autoupdate --retries 99
PID 2768:
  exe=/usr/bin/python3.13
  cwd=/opt/data
/opt/hermes/.venv/bin/python3 /opt/hermes/.venv/bin/hermes gateway run --replace
PID 2742:
  exe=/usr/bin/python3.13
  cwd=/opt/data
/opt/hermes/.venv/bin/python3 /opt/hermes/.venv/bin/hermes dashboard --host 127.0.0.1 --port 9119 --no-open
```

## [p10_sockets_all]
**Comando:** `ss -tlnp 2>&1 | awk '{print $4, $6}' | sort -u; echo ---; ss -tnp 2>&1 | grep -E '3000|20128' | head -5`

```
0.0.0.0:20128 users:(("next-server
0.0.0.0:22 
100.91.46.87:10000 
100.91.46.87:443 
100.91.46.87:54584 
127.0.0.1:20241 
127.0.0.1:20242 users:(("cloudflared",pid=24062,fd=10))
127.0.0.1:3000 users:(("node",pid=1916,fd=18))
127.0.0.1:45351 
127.0.0.1:5432 
127.0.0.1:631 
127.0.0.1:8642 users:(("hermes",pid=2768,fd=43))
127.0.0.1:9119 users:(("hermes",pid=2742,fd=22))
127.0.0.53%lo:53 
127.0.0.54:53 
[::1]:3000 users:(("node",pid=1916,fd=19))
[::1]:631 
[::]:22 
[fd7a:115c:a1e0::2001:2eee]:10000 
[fd7a:115c:a1e0::2001:2eee]:443 
[fd7a:115c:a1e0::2001:2eee]:62838 
Local Peer
---
ESTAB 0      0                                     127.0.0.1:20128             127.0.0.1:54766 users:(("next-server (v1",pid=23905,fd=28))
ESTAB 0      0                                     127.0.0.1:36456             127.0.0.1:20128 users:(("hermes",pid=21889,fd=38))         
ESTAB 0      0                                     127.0.0.1:20128             127.0.0.1:44912 users:(("next-server (v1",pid=23905,fd=29))
ESTAB 0      0                                     127.0.0.1:44912             127.0.0.1:20128 users:(("hermes",pid=21889,fd=53))         
ESTAB 0      0                                     127.0.0.1:46630             127.0.0.1:20128 users:(("chrome",pid=23785,fd=39))         
```

## [p11_pid1916_container]
**Comando:** `docker ps -q 2>/dev/null | while read c; do echo "== $c: $(docker inspect -f '{{.Name}} pids={{.State.Pid}}' $c 2>/dev/null)"; done; echo ---; cat /proc/1821/cgroup 2>/dev/null | head -3; echo ---; cat /proc/1916/cgroup 2>/dev/null | head -3`

```
== c767a26af4e4: /hermes-workspace pids=1821
== 79cde1668e6f: /hermes-agent pids=1822
---
0::/system.slice/docker-***BLOB***.scope
---
0::/system.slice/docker-***BLOB***.scope
```

## [p12_tailscale_status]
**Comando:** `tailscale status --self 2>&1 | head -5; tailscale ip 2>&1 | head -3`

```
100.91.46.87   tijolao             ntg.trabalho@  linux  -                           
100.65.66.126  iphone-de-nicholas  ntg.trabalho@  iOS    offline, last seen 17d ago  

# Funnel on:
#     - https://tijolao.tail9e88c5.ts.net
100.91.46.87
fd7a:115c:a1e0::2001:2eee
```

## [p13_45351]
**Comando:** `ss -tlnp sport = :45351 2>&1; echo ---; ps aux | grep -iE 'ollama' | head -3; echo ---; ss -tlnp | grep -c 45351`

```
State  Recv-Q Send-Q Local Address:Port  Peer Address:PortProcess
LISTEN 0      4096       127.0.0.1:45351      0.0.0.0:*          
---
dr         70113 11.9  0.1  14436  9184 ?        S    03:17   0:00 ssh -i /home/dr/.hermes/home/.ssh/id_ed25519 -o BatchMode=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=8 dr@localhost ss -tlnp sport = :
dr         70125  4.7  0.1  14712  8200 ?        Ss   03:17   0:00 bash -c ss -tlnp sport = :45351 2>&1; echo ---; ps aux | grep -iE 'ollama' | head -3; echo ---; ss -tlnp | grep -c 45351
dr         70345  0.0  0.0   9540  2628 ?        S    03:17   0:00 grep -iE ollama
---
1
```

## [p14_node_pids_all]
**Comando:** `ps aux | grep -E 'node' | grep -v grep | grep -v chrome | awk '{print $2, $11, $12, $13}' | head -12`

```
1821 /usr/bin/tini -- /usr/local/bin/docker-entrypoint.sh
1916 node --max-old-space-size=2048 server-entry.js
2528 fusermount3 -o rw,nosuid,nodev,fsname=portal,auto_unmount,subtype=portal
2894 node /opt/data/.npm/_npx/3dfbf5a9eea4a1b3/node_modules/.bin/mcp-server-github 
2905 node /opt/data/.npm/_npx/a3241bba59c344f5/node_modules/.bin/mcp-server-filesystem /home/dr
2914 node /opt/data/.npm/_npx/f36605d6814ff2b0/node_modules/.bin/obsidian-mcp-server 
2970 node /opt/data/.npm/_npx/f36605d6814ff2b0/node_modules/.bin/obsidian-mcp-server 
2972 node /opt/data/.npm/_npx/3dfbf5a9eea4a1b3/node_modules/.bin/mcp-server-github 
2973 node /opt/data/.npm/_npx/a3241bba59c344f5/node_modules/.bin/mcp-server-filesystem /home/dr
22172 node /opt/data/.npm/_npx/f36605d6814ff2b0/node_modules/.bin/obsidian-mcp-server 
22178 node /opt/data/.npm/_npx/3dfbf5a9eea4a1b3/node_modules/.bin/mcp-server-github 
22186 node /opt/data/.npm/_npx/a3241bba59c344f5/node_modules/.bin/mcp-server-filesystem /home/dr
```

## [t1_path_login]
**Comando:** `bash -lc 'echo $PATH'`

```
/home/dr/.local/bin:/home/dr/.local/share/nvm/versions/node/v24.16.0/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
```

## [t2_path_interactive]
**Comando:** `bash -ic 'echo $PATH' 2>&1 | grep -v 'job control\|no job'`

```
bash: impossível definir grupo do processo do terminal (70843): ioctl inapropriado para dispositivo
bash: nenhum controle de trabalho neste shell
/home/dr/.local/bin:/home/dr/.local/bin:/home/dr/.local/share/nvm/versions/node/v24.16.0/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
```

## [t3_bashrc_profile]
**Comando:** `cat ~/.bashrc; echo '===== PROFILE ====='; cat ~/.profile 2>&1`

```
# >>> node via nvm (Hermes, 04-out-2026) >>>
export NVM_DIR="$HOME/.local/share/nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
# ~/.local/bin na frente do nvm: claude, codex e pnpm 11.20.0 seguem os mesmos de antes
export PATH="$HOME/.local/bin:$PATH"
# <<< node via nvm <<<
===== PROFILE =====

. "$HOME/.local/bin/env"
```

## [t4_type_all]
**Comando:** `bash -lc 'echo "== node: $(type -a node 2>&1 | head -6 | tr '\n' '|')"; echo "== npm: $(type -a npm 2>&1 | head -6 | tr '\n' '|')"; echo "== npx: $(type -a npx 2>&1 | head -6 | tr '\n' '|')"; echo "== nvm: $(type -a nvm 2>&1 | head -6 | tr '\n' '|')"; echo "== corepack: $(type -a corepack 2>&1 | head -6 | tr '\n' '|')"; echo "== pnpm: $(type -a pnpm 2>&1 | head -6 | tr '\n' '|')"; echo "== python3`

```
bash: linha 1: )"; echo "== nvm: $(type -a nvm 2>&1 | head -6 | tr n : comando não encontrado
bash: linha 1: )"; echo "== corepack: $(type -a corepack 2>&1 | head -6 | tr n : comando não encontrado
bash: linha 1: )"; echo "== uv: $(type -a uv 2>&1 | head -6 | tr n : comando não encontrado
bash: linha 1: )"; echo "== pnpm: $(type -a pnpm 2>&1 | head -6 | tr n : comando não encontrado
bash: linha 1: )"; echo "== claude: $(type -a claude 2>&1 | head -6 | tr n : comando não encontrado
bash: linha 1: )"; echo "== tailscale: $(type -a tailscale 2>&1 | head -6 | tr n : comando não encontrado
bash: linha 1: )"; echo "== 9router: $(type -a 9router 2>&1 | head -6 | tr n : comando não encontrado
bash: linha 1: )"; echo "== hermes: $(type -a hermes 2>&1 | head -6 | tr n : comando não encontrado
bash: linha 1: )"; echo "== npx: $(type -a npx 2>&1 | head -6 | tr n : comando não encontrado
bash: linha 1: )"; echo "== docker: $(type -a docker 2>&1 | head -6 | tr n : comando não encontrado
bash: linha 1: )"; echo "== npm: $(type -a npm 2>&1 | head -6 | tr n : comando não encontrado
bash: linha 1: )"; echo "== cloudflared: $(type -a cloudflared 2>&1 | head -6 | tr n : comando não encontrado
bash: linha 1: )": comando não encontrado
bash: linha 1: )"; echo "== python3: $(type -a python3 2>&1 | head -6 | tr n : comando não encontrado
bash: linha 1: )"; echo "== code: $(type -a code 2>&1 | head -6 | tr n : comando não encontrado
bash: linha 1: )"; echo "== pip: $(type -a pip 2>&1 | head -6 | tr n : comando não encontrado
bash: linha 1: )"; echo "== codex: $(type -a codex 2>&1 | head -6 | tr n : comando não encontrado
bash: linha 1: )"; echo "== pipx: $(type -a pipx 2>&1 | head -6 | tr n : comando não encontrado
bash: linha 1: )"; echo "== zed: $(type -a zed 2>&1 | head -6 | tr n : comando não encontrado
bash: linha 1: )"; echo "== git: $(type -a git 2>&1 | head -6 | tr n : comando não encontrado
bash: linha 1: )"; echo "== rclone: $(type -a rclone 2>&1 | head -6 | tr n : comando não encontrado
bash: linha 1: )"; echo "== ollama: $(type -a ollama 2>&1 | head -6 | tr n : comando não encontrado
bash: linha 1: )"; echo "== gh: $(type -a gh 2>&1 | head -6 | tr n : comando não encontrado
bash: -c: linha 2: encontrado EOF inesperado enquanto procurava por `)' correspondente
```

## [t5_docker_compose]
**Comando:** `bash -lc 'type -a "docker compose" 2>&1; docker compose version 2>&1 | head -1; docker --version 2>&1'`

```
bash: linha 1: type: docker compose: não encontrado
Docker Compose version 2.40.3+ds1-0ubuntu1~24.04.1
Docker version 29.1.3, build 29.1.3-0ubuntu3~24.04.2
```

## [t4_type_all]
**Comando:** `bash -lc 'for t in node npm npx nvm corepack pnpm python3 pip uv pipx rclone gh git claude codex docker tailscale cloudflared 9router hermes code zed ollama; do echo "== $t"; type -a $t 2>&1 | head -6; done'`

```
== node
node é /home/dr/.local/share/nvm/versions/node/v24.16.0/bin/node
node é /usr/bin/node
node é /bin/node
== npm
npm é /home/dr/.local/share/nvm/versions/node/v24.16.0/bin/npm
npm é /usr/bin/npm
npm é /bin/npm
== npx
npx é /home/dr/.local/share/nvm/versions/node/v24.16.0/bin/npx
npx é /usr/bin/npx
npx é /bin/npx
== nvm
bash: linha 1: type: nvm: não encontrado
== corepack
corepack é /home/dr/.local/share/nvm/versions/node/v24.16.0/bin/corepack
== pnpm
pnpm é /home/dr/.local/bin/pnpm
pnpm é /home/dr/.local/share/nvm/versions/node/v24.16.0/bin/pnpm
== python3
python3 é /usr/bin/python3
python3 é /bin/python3
== pip
pip é /usr/bin/pip
pip é /bin/pip
== uv
bash: linha 1: type: uv: não encontrado
== pipx
bash: linha 1: type: pipx: não encontrado
== rclone
rclone é /home/dr/.local/bin/rclone
rclone é /usr/bin/rclone
rclone é /bin/rclone
== gh
gh é /usr/bin/gh
gh é /bin/gh
== git
git é /usr/bin/git
git é /bin/git
== claude
claude é /home/dr/.local/bin/claude
== codex
codex é /home/dr/.local/bin/codex
== docker
docker é /usr/bin/docker
docker é /bin/docker
== tailscale
tailscale é /usr/bin/tailscale
tailscale é /bin/tailscale
== cloudflared
cloudflared é /usr/local/bin/cloudflared
cloudflared é /usr/bin/cloudflared
cloudflared é /bin/cloudflared
== 9router
9router é /home/dr/.local/bin/9router
== hermes
hermes é /home/dr/.local/bin/hermes
== code
bash: linha 1: type: code: não encontrado
== zed
zed é /home/dr/.local/bin/zed
== ollama
bash: linha 1: type: ollama: não encontrado
```

## [t6_versions]
**Comando:** `
echo "node: $(node --version 2>&1)"; echo "npm: $(npm --version 2>&1)"; echo "pnpm: $(pnpm --version 2>&1)"
echo "python3: $(python3 --version 2>&1)"; echo "pip: $(pip --version 2>&1 | head -1)"
echo "rclone: $(rclone version 2>&1 | head -1)"; echo "gh: $(gh --version 2>&1 | head -1)"; echo "git: $(git --version 2>&1)"
echo "docker: $(docker --version 2>&1)"; echo "tailscale: $(tailscale version `

```
node: v24.16.0
npm: 11.16.0
pnpm: 11.20.0
python3: Python 3.12.3
pip: pip 24.0 from /usr/lib/python3/dist-packages/pip (python 3.12)
rclone: rclone v1.75.1
gh: gh version 2.45.0 (2025-07-18 Ubuntu 2.45.0-1ubuntu0.3)
git: git version 2.43.0
docker: Docker version 29.1.3, build 29.1.3-0ubuntu3~24.04.2
tailscale: 1.102.4
cloudflared: cloudflared version 2026.9.3 (built 2026-09-24-16:07 UTC)
claude: 2.1.285 (Claude Code)
codex: codex-cli 0.153.4
9router: 0.5.95
hermes: Hermes Agent v0.21.1 (2026.9.7) · upstream cdf4c765
zed: Zed 1.22.0 76659a55a8c10ed355a070f8764a0b1733e3c115  – /home/dr/.local/zed.app/libexec/zed-editor
```

## [t7_npm_prefix]
**Comando:** `bash -lc 'npm config get prefix; echo ---; which -a node npm; echo ---; ls /usr/local/lib/node_modules 2>&1 | head; echo ---; ls ~/.local/lib/node_modules 2>&1 | head; echo ---; ls ~/.npm-global 2>&1 | head -3'`

```
/home/dr/.local/share/nvm/versions/node/v24.16.0
---
/home/dr/.local/share/nvm/versions/node/v24.16.0/bin/node
/usr/bin/node
/bin/node
/home/dr/.local/share/nvm/versions/node/v24.16.0/bin/npm
/usr/bin/npm
/bin/npm
---
9remote
better-sqlite3
sql.js
systray2
---
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
---
ls: não foi possível acessar '/home/dr/.npm-global': Arquivo ou diretório inexistente
```

## [t8_dpkg_origins]
**Comando:** `
for p in /usr/bin/node /usr/bin/npm /usr/bin/npx /usr/bin/python3 /usr/bin/pip /usr/bin/rclone /usr/bin/gh /usr/bin/git /usr/bin/docker /usr/bin/tailscale /usr/bin/cloudflared /usr/local/bin/cloudflared /usr/bin/zed /usr/local/bin/ollama /usr/bin/ollama; do
  [ -e "$p" ] || { echo "AUSENTE $p"; continue; }
  o=$(dpkg -S "$p" 2>/dev/null | head -1)
  if [ -z "$o" ]; then echo "MANUAL $p"; else ech`

```
APT    /usr/bin/node <= nodejs
APT    /usr/bin/npm <= npm
APT    /usr/bin/npx <= npm
APT    /usr/bin/python3 <= python3-minimal
APT    /usr/bin/pip <= python3-pip
APT    /usr/bin/rclone <= rclone
APT    /usr/bin/gh <= gh
APT    /usr/bin/git <= git
APT    /usr/bin/docker <= docker.io
APT    /usr/bin/tailscale <= tailscale
APT    /usr/bin/cloudflared <= cloudflared
MANUAL /usr/local/bin/cloudflared
AUSENTE /usr/bin/zed
AUSENTE /usr/local/bin/ollama
AUSENTE /usr/bin/ollama
---
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
ls: não foi possível acessar '/usr/bin/ollama': Arquivo ou diretório inexistente
ls: não foi possível acessar '/usr/local/bin/ollama': Arquivo ou diretório inexistente
inactive
```

## [t9_nvm_interactive]
**Comando:** `bash -ic 'type nvm 2>&1 | head -2; nvm current 2>&1 | head -2' 2>&1 | grep -vE 'job control|controle de trabalho'`

```
bash: impossível definir grupo do processo do terminal (76664): ioctl inapropriado para dispositivo
nvm é uma função
nvm () 
bash: [76882: 2 (255)] tcsetattr: ioctl inapropriado para dispositivo
v24.16.0
```

## [t10_localbin]
**Comando:** `ls -la ~/.local/bin/ 2>&1`

```
total 48460
drwxrwxr-x  2 dr dr     4096 out  4 16:29 .
drwx------ 10 dr dr     4096 set  7 08:21 ..
lrwxrwxrwx  1 dr dr       34 out  2 01:42 9router -> ../lib/node_modules/9router/cli.js
lrwxrwxrwx  1 dr dr       45 out  2 08:22 claude -> /home/dr/.local/share/claude/versions/2.1.285
lrwxrwxrwx  1 dr dr       46 set  5 13:08 codex -> ../lib/node_modules/@openai/codex/bin/codex.js
lrwxrwxrwx  1 dr dr       38 set  3 10:03 ctx7 -> ../lib/node_modules/ctx7/dist/index.js
-rw-rw-r--  1 dr dr      328 set  9 12:47 env
-rw-rw-r--  1 dr dr      165 set  9 12:47 env.fish
-rwxrwxr-x  1 dr dr      890 out  2 21:31 hermes
-rwxrwxr-x  1 dr dr      155 ago 18 01:23 hermes-acp
-rwxrwxr-x  1 dr dr      157 ago 18 01:23 hermes-agent
-rwxrwxr-x  1 dr dr       56 ago 18 20:49 local
-rwxr-xr-x  1 dr dr    14480 jul 25 19:01 obsidian
lrwxrwxrwx  1 dr dr       37 set  5 08:16 pn -> ../lib/node_modules/pnpm/bin/pnpm.mjs
lrwxrwxrwx  1 dr dr       37 set  5 08:16 pnpm -> ../lib/node_modules/pnpm/bin/pnpm.mjs
lrwxrwxrwx  1 dr dr       37 set  5 08:16 pnpx -> ../lib/node_modules/pnpm/bin/pnpx.mjs
lrwxrwxrwx  1 dr dr       37 set  5 08:16 pnx -> ../lib/node_modules/pnpm/bin/pnpx.mjs
-rwxr-xr-x  1 dr dr 49561762 ago 14 10:02 pool
-rwxrwxr-x  1 dr dr      145 set  2 17:42 qpdf
lrwxrwxrwx  1 dr dr       37 out  2 20:13 rclone -> /home/dr/src/scripts/nuvem/bin/rclone
-rwxrwxr-x  1 dr dr       78 out  2 21:31 tijolao
lrwxrwxrwx  1 dr dr       51 ago 20 10:55 tokentracker -> ../lib/node_modules/tokentracker-cli/bin/tracker.js
lrwxrwxrwx  1 dr dr       51 ago 20 10:55 tokentracker-cli -> ../lib/node_modules/tokentracker-cli/bin/tracker.js
lrwxrwxrwx  1 dr dr       51 ago 20 10:55 tracker -> ../lib/node_modules/tokentracker-cli/bin/tracker.js
lrwxrwxrwx  1 dr dr       31 set  3 17:46 zed -> /home/dr/.local/zed.app/bin/zed
```

## [t11_dup_versions]
**Comando:** `
echo "== node duplicado:"; /usr/bin/node --version 2>&1; echo "== npm apt:"; /usr/bin/npm --version 2>&1; echo "== rclone apt:"; /usr/bin/rclone version 2>&1 | head -1
echo "== pnpm nvm-dir:"; ~/.local/share/nvm/versions/node/v24.16.0/bin/pnpm --version 2>&1 | head -1
echo "== zed link:"; ls -la ~/.local/bin/zed 2>&1; readlink -f ~/.local/bin/zed 2>&1
echo "== 9remote em /usr/local/bin:"; ls -la `

```
== node duplicado:
v18.19.1
== npm apt:
9.2.0
== rclone apt:
rclone v1.60.1-DEV
== pnpm nvm-dir:
! Corepack is about to download https://registry.npmjs.org/pnpm/-/pnpm-12.9.1.tgz
== zed link:
lrwxrwxrwx 1 dr dr 31 set  3 17:46 /home/dr/.local/bin/zed -> /home/dr/.local/zed.app/bin/zed
/home/dr/.local/zed.app/bin/zed
== 9remote em /usr/local/bin:
total 24
drwxr-xr-x 6 root root 4096 out  2 01:42 .
drwxr-xr-x 4 root root 4096 out  2 01:10 ..
drwxr-xr-x 4 root root 4096 set 15 14:30 9remote
drwxr-xr-x 7 root root 4096 set 23 23:32 better-sqlite3
drwxr-xr-x 4 root root 4096 set 15 16:03 sql.js
drwxr-xr-x 4 root root 4096 set 15 16:05 systray2
```

## [t12_wrappers]
**Comando:** `
for f in hermes tijolao hermes-acp hermes-agent local qpdf; do
  echo "===== ~/.local/bin/$f"; head -12 ~/.local/bin/$f 2>&1
done`

```
===== ~/.local/bin/hermes
#!/usr/bin/env bash
# Hermes roda em container. Stack: ~/hermes-workspace/tijolao.sh
set -euo pipefail

STACK=~/hermes-workspace/tijolao.sh

# Aceita o container com qualquer nome (hermes-agent OU *-hermes-agent-1).
NOME=$(docker ps --format '{{.Names}}' | grep -E '^hermes-agent$|hermes-agent-1$' | head -1)

if [ -z "$NOME" ]; then
  echo "O Hermes esta desligado." >&2
  echo "Para ligar:  $STACK up" >&2
===== ~/.local/bin/tijolao
#!/usr/bin/env bash
exec /home/dr/src/tijolao-ai/hermes-stack/tijolao.sh "$@"
===== ~/.local/bin/hermes-acp
#!/usr/bin/env bash
unset PYTHONPATH
unset PYTHONHOME
exec "/home/dr/.hermes/hermes-agent/venv/bin/python" "/home/dr/.hermes/hermes-agent/hermes" acp "$@"
===== ~/.local/bin/hermes-agent
#!/usr/bin/env bash
unset PYTHONPATH
unset PYTHONHOME
exec "/home/dr/.hermes/hermes-agent/venv/bin/python" "/home/dr/.hermes/hermes-agent/run_agent.py" "$@"
===== ~/.local/bin/local
#!/bin/sh
exec /home/dr/.local/bin/hermes -p local "$@"
===== ~/.local/bin/qpdf
#!/bin/sh
exec env LD_LIBRARY_PATH="$HOME/.local/qpdf-root/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH" "$HOME/.local/qpdf-root/usr/bin/qpdf" "$@"
```

## [t13_9remote]
**Comando:** `ls -la /usr/local/lib/node_modules/9remote/package.json 2>&1; grep -m1 '"version"' /usr/local/lib/node_modules/9remote/package.json 2>&1; type -a 9remote 2>&1 | head -3`

```
-rw-r--r-- 1 root root 1988 set 15 14:30 /usr/local/lib/node_modules/9remote/package.json
  "version": "2.5.8",
9remote é /usr/local/bin/9remote
```

## [r1_bashrc_profile_refs]
**Comando:** `grep -nE '/home/dr/projetos|.config/nvm|/home/dr/hermes-workspace|cofre\.env|[sS][aA][sS][iI]|EXTRACAO' ~/.bashrc ~/.profile 2>&1 || echo NENHUMA_REF`

```
NENHUMA_REF
```

## [r2_systemd_user_refs]
**Comando:** `grep -rnE '/home/dr/projetos|.config/nvm|/home/dr/hermes-workspace|cofre\.env|[sS][aA][sS][iI]|EXTRACAO' ~/.config/systemd/user/ 2>/dev/null | grep -v Binary | head -30 || echo NENHUMA_REF`

```

```

## [r3_localbin_refs]
**Comando:** `timeout 30 grep -rnE '/home/dr/projetos|.config/nvm|/home/dr/hermes-workspace|cofre\.env|[sS][aA][sS][iI]|EXTRACAO' ~/.local/bin/ 2>/dev/null | grep -av 'Binary file' | head -30 || echo NENHUMA_REF`

```

```

## [r4_autostart_refs]
**Comando:** `grep -rnE '/home/dr/projetos|.config/nvm|/home/dr/hermes-workspace|cofre\.env|[sS][aA][sS][iI]|EXTRACAO' ~/.config/autostart/ ~/.local/share/applications/ 2>/dev/null | head -20 || echo NENHUMA_REF`

```
/home/dr/.config/autostart/9router.desktop:5:Exec=/home/dr/.config/nvm/versions/node/v24.16.0/bin/node /home/dr/.local/lib/node_modules/9router/cli.js --tray --
```

## [r5_hermes_configs]
**Comando:** `grep -nE '/home/dr/projetos|.config/nvm|/home/dr/hermes-workspace|cofre\.env|[sS][aA][sS][iI]|EXTRACAO' /home/dr/.hermes/config.yaml 2>/dev/null | head -20; echo ---PROFILES---; for f in /home/dr/.hermes/profiles/*/config.yaml; do echo "== $f"; grep -nE '/home/dr/projetos|.config/nvm|/home/dr/hermes-workspace|cofre\.env|[sS][aA][sS][iI]|EXTRACAO' "$f" 2>/dev/null | head -10; done; echo FIM`

```
---PROFILES---
== /home/dr/.hermes/profiles/chefe/config.yaml
== /home/dr/.hermes/profiles/evidencia/config.yaml
== /home/dr/.hermes/profiles/fiscal/config.yaml
== /home/dr/.hermes/profiles/residente/config.yaml
== /home/dr/.hermes/profiles/secretaria/config.yaml
FIM
```

## [r2_systemd_user_refs]
**Comando:** `grep -rnE '/home/dr/projetos|.config/nvm|/home/dr/hermes-workspace|cofre\.env|[sS][aA][sS][iI]|EXTRACAO' ~/.config/systemd/user/ 2>/dev/null | head -30; echo RC_DONE`

```
RC_DONE
```

## [r3_localbin_refs]
**Comando:** `timeout 30 grep -rnE '/home/dr/projetos|.config/nvm|/home/dr/hermes-workspace|cofre\.env|[sS][aA][sS][iI]|EXTRACAO' ~/.local/bin/ 2>/dev/null | head -30; echo RC_DONE`

```
RC_DONE
```

## [r6_tijolaoai_refs]
**Comando:** `cd /home/dr/src/tijolao-ai 2>/dev/null && timeout 60 grep -rnE '/home/dr/projetos|.config/nvm|/home/dr/hermes-workspace|cofre\.env|[sS][aA][sS][iI]|EXTRACAO' . --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=venv --exclude-dir=.venv 2>/dev/null | head -40; echo RC_DONE`

```
./services/hermes-workspace.service:8:WorkingDirectory=/home/dr/projetos/hermes-workspace
./services/hermes-workspace.service:9:EnvironmentFile=/home/dr/projetos/hermes-workspace/.env
./services/hermes-workspace.service:12:ExecStart=/home/dr/.hermes/node/bin/node /home/dr/projetos/hermes-workspace/server-entry.js
./scripts/verify-stack.sh:87:  '/home/dr/projetos/hermes-workspace/.env|HERMES_API_TOKEN' \
./scripts/verify-stack.sh:104:if [[ -f /home/dr/.hermes/.env && -f /home/dr/projetos/hermes-workspace/.env ]]; then
./scripts/verify-stack.sh:106:  workspace_key=$(sed -n 's/^HERMES_API_TOKEN=//p' /home/dr/projetos/hermes-workspace/.env | tail -n 1)
./hermes-stack/AGENTS.md:22:| `residente` | Implementação de produto, com ênfase no SASI | `poolside/laguna-s-2.1` | `FIZ` · `VERIFIQUEI` · `PENDÊNCIA` |
./hermes-stack/AGENTS.md:45:residente chat -q "Implemente o campo X na tabela Y do SASI"
./hermes-stack/swarm.yaml:75:  specialty: codigo de produto, com enfase no SASI
./hermes-stack/swarm.yaml:98:  - sasi
RC_DONE
```

## [r7_hermes_cron_refs]
**Comando:** `grep -rnE '/home/dr/projetos|.config/nvm|/home/dr/hermes-workspace|cofre\.env|[sS][aA][sS][iI]|EXTRACAO' ~/.hermes/cron/ 2>/dev/null | head -15; echo RC_DONE`

```
RC_DONE
```

## [r8_hermes_node_bin]
**Comando:** `ls -la /home/dr/.hermes/node/bin 2>&1; echo ---; ls -la /home/dr/.hermes/hermes-agent/venv/bin/ 2>&1 | head -12; echo ---; ls -la /home/dr/.hermes/.env 2>&1; ls -la /home/dr/.local/secrets/.env 2>&1`

```
ls: não foi possível acessar '/home/dr/.hermes/node/bin': Arquivo ou diretório inexistente
---
ls: não foi possível acessar '/home/dr/.hermes/hermes-agent/venv/bin/': Arquivo ou diretório inexistente
---
lrwxrwxrwx 1 dr dr 28 out  2 21:31 /home/dr/.hermes/.env -> /home/dr/.local/secrets/.env
-rw------- 1 dr dr 10439 out  4 12:30 /home/dr/.local/secrets/.env
```

## [r9_swarm_yaml_contexto]
**Comando:** `grep -n -B2 -A4 'sasi' /home/dr/src/tijolao-ai/hermes-stack/swarm.yaml 2>/dev/null | head -25`

```
96-  - feature
97-  - bugfix
98:  - sasi
99-  greenlightRequiredFor: *id001
100-  maxConcurrentTasks: 1
101-  acceptsBroadcast: true
102-  reviewRequired: false
```

## [r10_compose]
**Comando:** `find /home/dr/src/tijolao-ai -maxdepth 2 -name 'docker-compose*' -o -maxdepth 2 -name 'compose*.yml' 2>/dev/null | head -5`

```
/home/dr/src/tijolao-ai/hermes-stack/docker-compose.tijolao.yml
```

## [r11_compose_content]
**Comando:** `grep -nE 'projetos|volumes|/home/dr' /home/dr/src/tijolao-ai/docker-compose.tijolao.yml 2>/dev/null | head -20 || find /home/dr/src/tijolao-ai -maxdepth 3 -name '*.yml' -path '*compose*' 2>/dev/null`

```

```

## [r11_compose_content]
**Comando:** `grep -nE '/home/dr|projetos' /home/dr/src/tijolao-ai/hermes-stack/docker-compose.tijolao.yml 2>/dev/null | head -25; echo RC_DONE`

```
13:#   o estado real do Hermes ja existe em /home/dr/.hermes (config.yaml, skills,
15:#   Alem disso /home/dr/.hermes/.env e um symlink para /home/dr/.local/secrets/.env —
16:#   por isso /home/dr/src tambem e montado, no mesmo caminho, senao o
35:      - /home/dr/.local/secrets/tijolao.env
38:      # Aqui os tres sao reapontados para /home/dr porque o config.yaml tem
40:      #   skills.external_dirs -> /home/dr/.claude/skills
41:      #   OBSIDIAN_VAULT_PATH  -> /home/dr/vaults/celebro
43:      HERMES_HOME: /home/dr/.hermes
44:      HERMES_WRITE_SAFE_ROOT: /home/dr
45:      HERMES_LAZY_INSTALL_TARGET: /home/dr/.hermes/lazy-packages
55:      - /home/dr/.hermes:/home/dr/.hermes
56:      - /home/dr/src:/home/dr/src
58:      - /home/dr/.claude/skills:/home/dr/.claude/skills:ro
59:      - /home/dr/vaults/celebro:/home/dr/vaults/celebro
60:      - /home/dr/.local/secrets:***M***      context: /home/dr/src/hermes-workspace
85:      - /home/dr/.local/secrets/tijolao.env
90:      HERMES_HOME: /home/dr/.hermes
91:      HERMES_WORKSPACE_DIR: /home/dr/src
110:      HERMES_HOST_HOME: /home/dr
115:      HERMES_CLI_BIN: /home/dr/.local/bin/hermes
117:      - /home/dr/.hermes:/home/dr/.hermes
118:      - /home/dr/src:/home/dr/src
119:      - /home/dr/.claude/skills:/home/dr/.claude/skills:ro
123:      - /home/dr/.local/bin:/home/dr/.local/bin:ro
RC_DONE
```

## [r12_broken_symlinks]
**Comando:** `timeout 120 find ~ -xdev -xtype l \( -path '*/.cache/*' -o -path '*/node_modules/*' -o -path '*/.git/*' -o -path '*/.local/share/Trash/*' \) -prune -o -xtype l -print 2>/dev/null | head -60; echo RC_DONE`

```
/home/dr/vaults/celebro/002-DEV-IA/arquivos-sasi/SASI_Copia_Repositorio_GH/.env
/home/dr/.hermes/home/.config/pulse/Tijolao-runtime
/home/dr/.***BLOB***
/home/dr/.local/jdk-25/bin/devrig
/home/dr/.local/qpdf-root/usr/share/doc/qpdf/changelog.Debian.gz
/home/dr/.var/app/com.bitwarden.desktop/config/Bitwarden/SingletonLock
/home/dr/.var/app/com.bitwarden.desktop/config/Bitwarden/SingletonCookie
/home/dr/.config/mozilla/firefox/anboy4b3.default-release/lock
/home/dr/.config/mozilla/firefox/Z7T7IMRJ.Perfil 1/lock
/home/dr/.config/mozilla/firefox/gUijBASX.Perfil 1/lock
/home/dr/.config/mozilla/firefox/m96LufNT.Profile 2/lock
/home/dr/.config/mozilla/firefox/iy9xv9lq.default-release/lock
/home/dr/.config/mozilla/firefox/at9JjlGN.Perfil 3/lock
/home/dr/.config/Codex/SingletonLock
/home/dr/.config/Codex/SingletonSocket
/home/dr/.config/Codex/SingletonCookie
/home/dr/.config/google-chrome/SingletonLock
/home/dr/.config/google-chrome/SingletonCookie
RC_DONE
```

## [r13_broken_details]
**Comando:** `
for l in /home/dr/vaults/celebro/002-DEV-IA/arquivos-sasi/SASI_Copia_Repositorio_GH/.env /home/dr/.hermes/home/.config/pulse/Tijolao-runtime /home/dr/.local/jdk-25/bin/devrig /home/dr/.local/qpdf-root/usr/share/doc/qpdf/changelog.Debian.gz; do
  echo "== $l -> $(readlink "$l" 2>&1)"
done
echo ---; ls -la /home/dr/.hermes/home/.config/pulse/ 2>&1 | head -5
echo ---; ls /home/dr/vaults/celebro/002-`

```
== /home/dr/vaults/celebro/002-DEV-IA/arquivos-sasi/SASI_Copia_Repositorio_GH/.env -> ../.env
== /home/dr/.hermes/home/.config/pulse/Tijolao-runtime -> /tmp/pulse-PKdhtXMmr18n
== /home/dr/.local/jdk-25/bin/devrig -> /home/dr/.mcp-steroid/bin/devrig
== /home/dr/.local/qpdf-root/usr/share/doc/qpdf/changelog.Debian.gz -> ../libqpdf29t64/changelog.Debian.gz
---
total 8
drwx------ 2 dr dr 4096 set  8 23:58 .
drwxr-xr-x 6 dr dr 4096 set 23 16:25 ..
lrwxrwxrwx 1 dr dr   23 set  8 23:58 Tijolao-runtime -> /tmp/pulse-PKdhtXMmr18n
---
grafo-motor-clinico.png
imagens-referencia-layout-sasi-v3
resgate-stashes-src-sasi
SASI_Copia_Repositorio_GH
sasi-design-system
SASI-GEMINI-ANTIGOS
sasi-motor-clinico-v2
sasi-planilhas-antigas-e-mapas-taticos
sasi-skills-e-templates
SASIv3planoeanexos
```

## [r14_broken_all_verbose]
**Comando:** `timeout 120 find ~ -xdev \( -path '*/.cache/*' -o -path '*/node_modules/*' -o -path '*/.git/*' -o -path '*/.local/share/Trash/*' -o -path '*/.var/app/*' -o -path '*/.config/mozilla/*' -o -path '*/.config/google-chrome/*' -o -path '*/.config/Codex/*' \) -prune -o -xtype l -printf '%p ===TARGET=== %l\n' 2>/dev/null | head -40; echo RC_DONE`

```
/home/dr/vaults/celebro/002-DEV-IA/arquivos-sasi/SASI_Copia_Repositorio_GH/.env ===TARGET=== ../.env
/home/dr/.hermes/home/.config/pulse/Tijolao-runtime ===TARGET=== /tmp/pulse-PKdhtXMmr18n
/home/dr/.***BLOB*** ===TARGET=== ../../../../../../projetos/SASI-V3
/home/dr/.local/jdk-25/bin/devrig ===TARGET=== /home/dr/.mcp-steroid/bin/devrig
/home/dr/.local/qpdf-root/usr/share/doc/qpdf/changelog.Debian.gz ===TARGET=== ../libqpdf29t64/changelog.Debian.gz
RC_DONE
```

## [r15_blob_path]
**Comando:** `timeout 120 find ~ -xdev -maxdepth 1 -xtype l -printf '%p ===TARGET=== %l\n' 2>/dev/null | head -10; echo RC_DONE`

```
RC_DONE
```

## [r16_blob_find]
**Comando:** `timeout 60 find ~/.docker ~/.subversion ~/.gnupg ~/.local/share 2>/dev/null -xdev -xtype l -printf '%p ===TARGET=== %l\n' 2>/dev/null | grep -v 'Trash\|node_modules\|\.git/' | head -15; echo RC_DONE`

```
/home/dr/.***BLOB*** ===TARGET=== ../../../../../../projetos/SASI-V3
RC_DONE
```

## [r16_blob_path_raw]
**Comando:** `find ~/.local/share -xtype l`

```
/home/dr/.local/share/pnpm/store/v11/projects/b8d7b298ee51a73101e57a2edcb9eb39
```

## [r17_pnpm_link]
**Comando:** `readlink /home/dr/.local/share/pnpm/store/v11/projects/b8d7b298ee51a73101e57a2edcb9eb39; ls -la /home/dr/.local/share/pnpm/store/v11/projects/ 2>&1 | head -5`

```
../../../../../../projetos/SASI-V3
total 8
drwxrwxr-x 2 dr dr 4096 set  9 12:40 .
drwxrwxr-x 5 dr dr 4096 set  7 08:22 ..
lrwxrwxrwx 1 dr dr   34 ago 14 18:32 b8d7b298ee51a73101e57a2edcb9eb39 -> ../../../../../../projetos/SASI-V3
```

## [r18_unitdir_full]
**Comando:** `find ~/.config/systemd/user -type d 2>&1; ls -la ~/.config/systemd/user/ 2>&1`

```
/home/dr/.config/systemd/user
/home/dr/.config/systemd/user/default.target.wants
total 28
drwx------ 3 dr dr 4096 out  2 20:29 .
drwxrwxr-x 3 dr dr 4096 jul  6 06:55 ..
-rw-rw-r-- 1 dr dr  629 out  2 19:52 9router.service
drwxr-xr-x 2 dr dr 4096 out  2 20:25 default.target.wants
-rw-r--r-- 1 dr dr  658 out  2 19:52 hermes-dashboard.service
-rw-rw-r-- 1 dr dr 1037 set  2 01:49 hermes-gateway.service
-rw-r--r-- 1 dr dr  625 out  2 19:52 n8n.service
```

## [r19_hermes_cron_jobs]
**Comando:** `find ~/.hermes/cron -maxdepth 1 -type f -name '*.json' 2>/dev/null | head -5; ls ~/.hermes/jobs 2>&1 | head -5`

```
ls: não foi possível acessar '/home/dr/.hermes/jobs': Arquivo ou diretório inexistente
```

## [f1_9router_dirs]
**Comando:** `ls -la ~/.9router 2>&1 | head -8; echo ---; ls -la ~/.local/share/9router/bin/ 2>&1 | head -6; echo ---; ls ~/.local/share/9router/ 2>&1`

```
total 32
drwxrwxr-x  6 dr dr 4096 set 23 23:31 .
drwxr-x--- 24 dr dr 4096 out  7 02:27 ..
drwxrwxr-x  2 dr dr 4096 set 23 23:31 auth
drwxrwxr-x  3 dr dr 4096 out  7 02:25 db
-rw-------  1 dr dr   64 set 23 23:31 jwt-secret
drwxrwxr-x  3 dr dr 4096 set 23 23:31 logs
-rw-------  1 dr dr   64 set 23 23:31 machine-id
---
total 38840
drwxrwxr-x 2 dr dr     4096 set  7 19:14 .
drwxrwxr-x 9 dr dr     4096 out  7 02:26 ..
-rwxr-xr-x 1 dr dr 39763452 set  7 19:14 cloudflared
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
```

## [f2_tailscale_serve]
**Comando:** `tailscale serve status 2>&1 | head -10; tailscale funnel status 2>&1 | head -8`

```

# Funnel on:
#     - https://tijolao.tail9e88c5.ts.net

https://tijolao.tail9e88c5.ts.net:10000 (tailnet only)
|-- / proxy http://127.0.0.1:3000

https://tijolao.tail9e88c5.ts.net (Funnel on)
|-- / proxy http://127.0.0.1:20128


# Funnel on:
#     - https://tijolao.tail9e88c5.ts.net

https://tijolao.tail9e88c5.ts.net:10000 (tailnet only)
|-- / proxy http://127.0.0.1:3000

https://tijolao.tail9e88c5.ts.net (Funnel on)
```

## [f3_20241]
**Comando:** `ps aux | grep -iE 'cloudflared' | grep -v grep | awk '{print $2, $11, $12, $13, $14, $15}'`

```
2238 /usr/bin/cloudflared --no-autoupdate tunnel run --token-file
24062 /home/dr/.local/share/9router/bin/cloudflared tunnel --url http://127.0.0.1:20128 --config
```

## [f4_9router_proc]
**Comando:** `xargs -0 -a /proc/23840/cmdline echo 2>/dev/null; ls -l /proc/23840/fd 2>/dev/null | grep socket | wc -l; cat /proc/23840/net/tcp 2>/dev/null | awk 'NR>1 {print $2}' | head -20`

```
/home/dr/.local/share/nvm/versions/node/v24.16.0/bin/node /home/dr/.local/lib/node_modules/9router/cli.js --no-browser --skip-update --log
5
572E5B64:2710
572E5B64:D538
00000000:4EA0
0100007F:4F12
0100007F:4F11
3500007F:0035
3600007F:0035
572E5B64:01BB
0100007F:0BB8
0100007F:1538
00000000:0016
0100007F:21C2
0100007F:B127
0100007F:0277
0100007F:239F
BA0FA8C0:C5C2
BA0FA8C0:BB00
BA0FA8C0:D450
BA0FA8C0:D458
0100007F:0016
```

## [f5_45351_curl]
**Comando:** `timeout 3 curl -s -o /dev/null -w '%{http_code} %{content_type}' http://127.0.0.1:45351/ 2>&1; echo; timeout 3 curl -s http://127.0.0.1:45351/ 2>&1 | head -c 200`

```
404 text/plain; charset=utf-8
```

## [f6_54584_62838]
**Comando:** `timeout 3 curl -sk -o /dev/null -w '%{http_code}' https://100.91.46.87:54584/ 2>&1; echo; timeout 3 curl -s -o /dev/null -w '%{http_code}' http://100.91.46.87:10000/ 2>&1; echo`

```
000
400
```

## [f7_tailscaled_ports]
**Comando:** `ss -tlnp | grep -E '54584|62838|:443|:10000' 2>&1`

```
LISTEN 0      4096                  100.91.46.87:10000      0.0.0.0:*                                               
LISTEN 0      4096                  100.91.46.87:54584      0.0.0.0:*                                               
LISTEN 0      4096                  100.91.46.87:443        0.0.0.0:*                                               
LISTEN 0      4096   [fd7a:115c:a1e0::2001:2eee]:443           [::]:*                                               
LISTEN 0      4096   [fd7a:115c:a1e0::2001:2eee]:10000         [::]:*                                               
LISTEN 0      4096   [fd7a:115c:a1e0::2001:2eee]:62838         [::]:*                                               
```

## [f8_45351_owner]
**Comando:** `
for pid in 1110 1278 1050 1119 1821 2238 2058; do
  n=$(ls /proc/$pid/fd 2>/dev/null | wc -l)
  echo "pid $pid ($(/usr/bin/xargs -0 -a /proc/$pid/cmdline echo 2>/dev/null | cut -c1-50)): fds=$n (sem acesso = outro uid)"
done
#试探: node do 9router tem 5 sockets; 45351 é do usuário root? Tentar match inode
ss -tlnp | grep 45351
# ver se é do containerd-proxy
`

```
pid 1110 (/usr/lib/postgresql/16/bin/postgres -D /var/lib/po): fds=0 (sem acesso = outro uid)
pid 1278 (/usr/bin/dockerd -H fd:// --containerd=/run/contai): fds=0 (sem acesso = outro uid)
pid 1050 (/usr/sbin/tailscaled --state=/var/lib/tailscale/ta): fds=0 (sem acesso = outro uid)
pid 1119 (/usr/lib/xorg/Xorg -core :0 -seat seat0 -auth /var): fds=0 (sem acesso = outro uid)
pid 1821 (/usr/bin/tini -- /usr/local/bin/docker-entrypoint.): fds=0 (sem acesso = outro uid)
pid 2238 (/usr/bin/cloudflared --no-autoupdate tunnel run --): fds=0 (sem acesso = outro uid)
pid 2058 (/bin/sh -e /run/s6/basedir/scripts/rc.init top /op): fds=0 (sem acesso = outro uid)
LISTEN 0      4096                     127.0.0.1:45351      0.0.0.0:*                                               
```

## [f9_inode_scan]
**Comando:** `
inode=$(awk '$2=="0100007F:B127" {print $10}' /proc/net/tcp)
echo "inode 45351 = $inode"
for pid in $(ls /proc | grep -E "^[0-9]+$"); do
  if ls -l /proc/$pid/fd 2>/dev/null | grep -q "socket:\[$inode\]"; then
    echo "OWNER pid=$pid: $(xargs -0 -a /proc/$pid/cmdline echo 2>/dev/null | cut -c1-80)"
  fi
done 2>/dev/null | head -5
`

```
inode 45351 = 12159
```

## [f10_45351_body]
**Comando:** `timeout 3 curl -s -i http://127.0.0.1:45351/ 2>&1 | head -12; echo ---; timeout 3 curl -s http://127.0.0.1:45351/api/health 2>&1 | head -c 150`

```
HTTP/1.1 404 Not Found
Date: Wed, 07 Oct 2026 06:23:54 GMT
Content-Length: 19
Content-Type: text/plain; charset=utf-8

404: Page Not Found---
```

## [f11_20241_who]
**Comando:** `
# 20241 (0x4F11) e 20242 (0x4F12) — inodes
for porthex in 4F11 4F12; do
  inode=$(awk -v p=$porthex '$2 ~ ":" p "$" {print $10}' /proc/net/tcp | head -1)
  echo "== port $porthex inode=$inode"
done
ss -tlnp | grep -E '20241|20242'
`

```
== port 4F11 inode=17683
== port 4F12 inode=90124
LISTEN 0      4096                     127.0.0.1:20242      0.0.0.0:*    users:(("cloudflared",pid=24062,fd=10))    
LISTEN 0      4096                     127.0.0.1:20241      0.0.0.0:*                                               
```

## [f12_root_http_procs]
**Comando:** `
for pid in $(ls /proc | grep -E "^[0-9]+$"); do
  cmd=$(xargs -0 -a /proc/$pid/cmdline echo 2>/dev/null | cut -c1-70)
  uid=$(awk "/^Uid:/{print \$2}" /proc/$pid/status 2>/dev/null)
  [ "$uid" = "0" ] || continue
  case "$cmd" in
    *python*|*uvicorn*|*node*|*server*|*portal*|*proxy*|*s6*) echo "pid=$pid $cmd" ;;
  esac
done 2>/dev/null | head -20`

```
pid=1052 /usr/bin/python3 /usr/share/unattended-upgrades/unattended-upgrade-shu
pid=1821 /usr/bin/tini -- /usr/local/bin/docker-entrypoint.sh node --max-old-sp
pid=1822 /package/admin/s6/command/s6-svscan -d4 -- /run/service
pid=2058 /bin/sh -e /run/s6/basedir/scripts/rc.init top /opt/hermes/docker/main
pid=2059 s6-supervise s6-linux-init-shutdownd
pid=2065 /package/admin/s6-linux-init/command/s6-linux-init-shutdownd -d3 -c /r
pid=2078 s6-supervise s6rc-oneshot-runner
pid=2079 s6-supervise s6rc-fdholder
pid=2080 s6-supervise main-hermes
pid=2081 s6-supervise dashboard
pid=2087 /package/admin/s6/command/s6-ipcserverd -1 -- /package/admin/s6/comman
pid=2760 s6-supervise gateway-evidencia
pid=2761 s6-supervise gateway-evidencia/log
pid=2762 s6-supervise gateway-fiscal
pid=2763 s6-supervise gateway-fiscal/log
pid=2764 s6-supervise gateway-default
pid=2769 s6-supervise gateway-default/log
pid=2770 s6-supervise gateway-chefe
pid=2772 s6-supervise gateway-chefe/log
pid=2774 s6-supervise gateway-secretaria
```

## [f13_45351_hermes]
**Comando:** `timeout 3 curl -s http://127.0.0.1:45351/dashboard 2>&1 | head -c 200; echo; timeout 3 curl -s http://127.0.0.1:45351/health 2>&1 | head -c 200; echo; timeout 3 curl -sI http://127.0.0.1:9119/ 2>&1 | head -6`

```
404: Page Not Found
404: Page Not Found
HTTP/1.1 405 Method Not Allowed
date: Wed, 07 Oct 2026 06:24:12 GMT
server: uvicorn
allow: GET
content-length: 31
content-type: application/json
```

## [f14_9119_8642]
**Comando:** `timeout 3 curl -s http://127.0.0.1:9119/api/health 2>&1 | head -c 150; echo; timeout 3 curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8642/ 2>&1; echo`

```
{"ok":true,"version":"0.21.1","auth_required":false}
404
```

## [f15_docker_ports]
**Comando:** `docker inspect hermes-agent hermes-workspace --format '{{.Name}} network={{.HostConfig.NetworkMode}} ports={{.HostConfig.PortBindings}}' 2>&1`

```
/hermes-agent network=host ports=map[]
/hermes-workspace network=host ports=map[]
```

## [f16_sys_enabled_custom]
**Comando:** `
for d in /etc/systemd/system/multi-user.target.wants /etc/systemd/system/timers.target.wants /etc/systemd/system/*.target.wants; do
  [ -d "$d" ] && for l in $d/*; do [ -e "$l" ] || continue; t=$(readlink -f "$l"); echo "$l -> $t"; done
done 2>/dev/null | sort -u | head -40`

```
/etc/systemd/system/bluetooth.target.wants/bluetooth.service -> /usr/lib/systemd/system/bluetooth.service
/etc/systemd/system/emergency.target.wants/grub-initrd-fallback.service -> /usr/lib/systemd/system/grub-initrd-fallback.service
/etc/systemd/system/final.target.wants/casper.service -> /usr/lib/systemd/system/casper.service
/etc/systemd/system/getty.target.wants/getty@tty1.service -> /usr/lib/systemd/system/getty@.service
/etc/systemd/system/graphical.target.wants/accounts-daemon.service -> /usr/lib/systemd/system/accounts-daemon.service
/etc/systemd/system/graphical.target.wants/power-profiles-daemon.service -> /usr/lib/systemd/system/power-profiles-daemon.service
/etc/systemd/system/graphical.target.wants/switcheroo-control.service -> /usr/lib/systemd/system/switcheroo-control.service
/etc/systemd/system/graphical.target.wants/udisks2.service -> /usr/lib/systemd/system/udisks2.service
/etc/systemd/system/hibernate.target.wants/grub-common.service -> /usr/lib/systemd/system/grub-common.service
/etc/systemd/system/hybrid-sleep.target.wants/grub-common.service -> /usr/lib/systemd/system/grub-common.service
/etc/systemd/system/multi-user.target.wants/anacron.service -> /usr/lib/systemd/system/anacron.service
/etc/systemd/system/multi-user.target.wants/avahi-daemon.service -> /usr/lib/systemd/system/avahi-daemon.service
/etc/systemd/system/multi-user.target.wants/blueman-mechanism.service -> /usr/lib/systemd/system/blueman-mechanism.service
/etc/systemd/system/multi-user.target.wants/casper-md5check.service -> /usr/lib/systemd/system/casper-md5check.service
/etc/systemd/system/multi-user.target.wants/cloudflared.service -> /etc/systemd/system/cloudflared.service
/etc/systemd/system/multi-user.target.wants/console-setup.service -> /usr/lib/systemd/system/console-setup.service
/etc/systemd/system/multi-user.target.wants/containerd.service -> /usr/lib/systemd/system/containerd.service
/etc/systemd/system/multi-user.target.wants/cron.service -> /usr/lib/systemd/system/cron.service
/etc/systemd/system/multi-user.target.wants/cups-browsed.service -> /usr/lib/systemd/system/cups-browsed.service
/etc/systemd/system/multi-user.target.wants/cups.path -> /usr/lib/systemd/system/cups.path
/etc/systemd/system/multi-user.target.wants/cups.service -> /usr/lib/systemd/system/cups.service
/etc/systemd/system/multi-user.target.wants/dmesg.service -> /usr/lib/systemd/system/dmesg.service
/etc/systemd/system/multi-user.target.wants/docker.service -> /usr/lib/systemd/system/docker.service
/etc/systemd/system/multi-user.target.wants/e2scrub_reap.service -> /usr/lib/systemd/system/e2scrub_reap.service
/etc/systemd/system/multi-user.target.wants/earlyoom.service -> /usr/lib/systemd/system/earlyoom.service
/etc/systemd/system/multi-user.target.wants/grub-common.service -> /usr/lib/systemd/system/grub-common.service
/etc/systemd/system/multi-user.target.wants/grub-initrd-fallback.service -> /usr/lib/systemd/system/grub-initrd-fallback.service
/etc/systemd/system/multi-user.target.wants/irqbalance.service -> /usr/lib/systemd/system/irqbalance.service
/etc/systemd/system/multi-user.target.wants/kerneloops.service -> /usr/lib/systemd/system/kerneloops.service
/etc/systemd/system/multi-user.target.wants/lm-sensors.service -> /usr/lib/systemd/system/lm-sensors.service
/etc/systemd/system/multi-user.target.wants/mintsystem.service -> /usr/lib/systemd/system/mintsystem.service
/etc/systemd/system/multi-user.target.wants/ModemManager.service -> /usr/lib/systemd/system/ModemManager.service
/etc/systemd/system/multi-user.target.wants/networkd-dispatcher.service -> /usr/lib/systemd/system/networkd-dispatcher.service
/etc/systemd/system/multi-user.target.wants/NetworkManager.service -> /usr/lib/systemd/system/NetworkManager.service
/etc/systemd/system/multi-user.target.wants/openvpn.service -> /usr/lib/systemd/system/openvpn.service
/etc/systemd/system/multi-user.target.wants/postgresql.service -> /usr/lib/systemd/system/postgresql.service
/etc/systemd/system/multi-user.target.wants/qemu-kvm.service -> /usr/lib/systemd/system/qemu-kvm.service
/etc/systemd/system/multi-user.target.wants/remote-fs.target -> /usr/lib/systemd/system/remote-fs.target
/etc/systemd/system/multi-user.target.wants/rsyslog.service -> /usr/lib/systemd/system/rsyslog.service
/etc/systemd/system/multi-user.target.wants/run-qemu.mount -> /usr/lib/systemd/system/run-qemu.mount
```

## [f17_timers_wants]
**Comando:** `ls /etc/systemd/system/timers.target.wants/ 2>&1`

```
anacron.timer
apt-daily.timer
apt-daily-upgrade.timer
dpkg-db-backup.timer
e2scrub_all.timer
fstrim.timer
fwupd-refresh.timer
logrotate.timer
man-db.timer
motd-news.timer
```

## [f18_ollama_status]
**Comando:** `systemctl is-enabled ollama 2>&1; systemctl is-active ollama 2>&1; dpkg -S /etc/systemd/system/ollama.service.d/override.conf 2>&1 | head -1; dpkg -l ollama 2>&1 | tail -2`

```
not-found
inactive
dpkg-query: não foi encontrado caminho coincidindo com o padrão /etc/systemd/system/ollama.service.d/override.conf
dpkg-query: não foram encontrados pacotes coincidindo com ollama
```

## [f19_old_unit_installed]
**Comando:** `grep -rl 'hermes-workspace' ~/.config/systemd/user/ /etc/systemd/user/ 2>/dev/null | head -5; systemctl --user list-unit-files 2>/dev/null | grep -i workspace; echo RC_DONE`

```
RC_DONE
```

## [f20_env_file]
**Comando:** `cat ~/.local/bin/env 2>&1`

```
#!/bin/sh
# add binaries to PATH if they aren't added yet
# affix colons on either side of $PATH to simplify matching
case ":${PATH}:" in
    *:"$HOME/.local/bin":*)
        ;;
    *)
        # Prepending path in case a system-installed binary needs to be overridden
        export PATH="$HOME/.local/bin:$PATH"
        ;;
esac
```

## [f21_ollama_dir]
**Comando:** `ls -la /etc/systemd/system/ollama.service.d/ 2>&1; ls /etc/systemd/system/ollama.service 2>&1`

```
total 12
drwxr-xr-x  2 root root 4096 ago 18 20:36 .
drwxr-xr-x 25 root root 4096 out  2 01:10 ..
-rw-r--r--  1 root root  831 ago 18 20:38 override.conf
ls: não foi possível acessar '/etc/systemd/system/ollama.service': Arquivo ou diretório inexistente
```

## [f22_nvm_check]
**Comando:** `bash -lc 'nvm ls 2>/dev/null | head -5; nvm alias list 2>&1 | head -3' 2>&1 | grep -v controle; echo ---; cat ~/.local/share/nvm/alias/default 2>&1`

```
bash: linha 1: nvm: comando não encontrado
---
24
```

## [f23_9router_dup]
**Comando:** `grep -m1 '"version"' ~/.local/lib/node_modules/9router/package.json 2>&1; ls ~/.local/share/nvm/versions/node/v24.16.0/lib/node_modules/ 2>&1 | head -8`

```
  "version": "0.5.95",
@agentclientprotocol
@anthropic-ai
better-sqlite3
corepack
docx
@google
mongosh
n8n
```

## [f24_login_path_src]
**Comando:** `grep -rn 'nvm' /etc/profile.d/ /etc/environment 2>/dev/null | head -5; echo ---; bash -lc 'echo NVM_DIR=$NVM_DIR' 2>&1`

```
---
NVM_DIR=/home/dr/.local/share/nvm
```

## [f25_path_trace]
**Comando:** `bash -lc 'echo PATH inicial do login shell tem nvm: '$PATH'' 2>&1 | head -2`

```
PATH inicial do login shell tem nvm: /home/dr/.local/bin:/home/dr/.local/share/nvm/versions/node/v24.16.0/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
```

## [f26_other_rcs]
**Comando:** `ls -la ~/.bash_profile ~/.bash_login ~/.bash_aliases 2>&1; grep -n nvm /etc/profile 2>/dev/null | head -3; echo RC_DONE`

```
ls: não foi possível acessar '/home/dr/.bash_profile': Arquivo ou diretório inexistente
ls: não foi possível acessar '/home/dr/.bash_login': Arquivo ou diretório inexistente
ls: não foi possível acessar '/home/dr/.bash_aliases': Arquivo ou diretório inexistente
RC_DONE
```

## [f27_ssh_env]
**Comando:** `env | grep -E '^(PATH|NVM)' 2>&1; echo ---; cat /etc/environment 2>&1; echo ---; grep -rn 'NVM\|nvm' /etc/profile /etc/profile.d/*.sh 2>/dev/null | head -5; echo RC_DONE`

```
NVM_INC=/home/dr/.local/share/nvm/versions/node/v24.16.0/include/node
NVM_DIR=/home/dr/.local/share/nvm
NVM_CD_FLAGS=
PATH=/home/dr/.local/bin:/home/dr/.local/share/nvm/versions/node/v24.16.0/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
NVM_BIN=/home/dr/.local/share/nvm/versions/node/v24.16.0/bin
---
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin"
---
RC_DONE
```

## [f28_nonlogin_path]
**Comando:** `echo $PATH; echo ---; bash -c 'echo $PATH' | head -1`

```
/home/dr/.local/bin:/home/dr/.local/share/nvm/versions/node/v24.16.0/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
---
/home/dr/.local/bin:/home/dr/.local/share/nvm/versions/node/v24.16.0/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
```

## [f29_pam_env]
**Comando:** `ls -la ~/.pam_environment 2>&1; grep -rn 'nvm\|NVM' /etc/security/pam_env.conf 2>/dev/null | head -3; echo ---; cat /etc/systemd/user.conf 2>/dev/null | grep -v '^#' | grep -v '^$' | head -5; echo ---; ls /etc/environment.d/ ~/.config/environment.d/ 2>&1`

```
ls: não foi possível acessar '/home/dr/.pam_environment': Arquivo ou diretório inexistente
---
[Manager]
---
ls: não foi possível acessar '/home/dr/.config/environment.d/': Arquivo ou diretório inexistente
/etc/environment.d/:
90atk-adaptor.conf
90qt-a11y.conf
90qtwebengine-dictionaries-path.conf
```

## [f30_ssh_environment]
**Comando:** `grep -i 'permituserenvironment\|acceptenv' /etc/ssh/sshd_config 2>&1 | head -6; echo ---; cat ~/.ssh/environment 2>&1 | head -8`

```
#PermitUserEnvironment no
AcceptEnv LANG LC_*
---
cat: /home/dr/.ssh/environment: Arquivo ou diretório inexistente
```

## [f31_system_conf]
**Comando:** `grep -v '^#' /etc/systemd/system.conf 2>/dev/null | grep -v '^$' | head -8; echo ---; grep -rn 'NVM\|nvm' /etc/systemd/ 2>/dev/null | grep -v 'system/system\|\.wants' | head -8; echo RC_DONE`

```
[Manager]
---
RC_DONE
```

## [f32_sshd_service]
**Comando:** `systemctl cat ssh 2>&1 | head -30; systemctl show ssh -p Environment 2>&1 | head -3`

```
# /usr/lib/systemd/system/ssh.service
[Unit]
Description=OpenBSD Secure Shell server
Documentation=man:sshd(8) man:sshd_config(5)
After=network.target auditd.service
ConditionPathExists=!/etc/ssh/sshd_not_to_be_run

[Service]
EnvironmentFile=-/etc/default/ssh
ExecStartPre=/usr/sbin/sshd -t
ExecStart=/usr/sbin/sshd -D $SSHD_OPTS
ExecReload=/usr/sbin/sshd -t
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
Restart=on-failure
RestartPreventExitStatus=255
Type=notify
RuntimeDirectory=sshd
RuntimeDirectoryMode=0755

[Install]
WantedBy=multi-user.target
Alias=sshd.service
Environment=
```

## [f33_default_ssh]
**Comando:** `cat /etc/default/ssh 2>&1; echo ---; sudo -n cat /proc/$(pgrep -x sshd | head -1)/environ 2>&1 | tr '\0' '\n' | grep -E 'NVM|PATH' | head -5`

```
# Default settings for openssh-server. This file is sourced by /bin/sh from
# /etc/init.d/ssh.

# Options to pass to sshd
SSHD_OPTS=
---
```

## [f34_ssh_socket]
**Comando:** `systemctl is-active ssh.socket 2>&1; systemctl cat ssh.socket 2>&1 | grep -E 'Listen|Service' | head -4; systemctl show ssh.socket -p Environment 2>&1 | head -2`

```
active
ListenStream=0.0.0.0:22
ListenStream=[::]:22
Environment=
```

## [f35_pid1_environ]
**Comando:** `tr '\0' '\n' < /proc/1/environ 2>/dev/null | grep -E 'NVM|^PATH' | head -5; echo RC_DONE`

```
RC_DONE
bash: linha 1: /proc/1/environ: Permissão negada
```

## [f36_ssh_rc]
**Comando:** `ls -la ~/.ssh/rc /etc/ssh/sshrc 2>&1; echo RC_DONE`

```
ls: não foi possível acessar '/home/dr/.ssh/rc': Arquivo ou diretório inexistente
ls: não foi possível acessar '/etc/ssh/sshrc': Arquivo ou diretório inexistente
RC_DONE
```

## [f37_localbin_targets]
**Comando:** `for f in ~/.local/bin/*; do [ -L "$f" ] && [ ! -e "$f" ] && echo 'BROKEN:' "$f -> $(readlink "$f")"; done; echo RC_DONE`

```
RC_DONE
```

## [f38_globs]
**Comando:** `ls ~/.local/lib/node_modules/ 2>&1; echo ---; ls ~/.local/share/nvm/versions/node/v24.16.0/lib/node_modules/ 2>&1`

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
@agentclientprotocol
@anthropic-ai
better-sqlite3
corepack
docx
@google
mongosh
n8n
npm
@openai
supabase
vercel
```

## [f39_desktop_9router_content]
**Comando:** `cat ~/.config/autostart/9router.desktop 2>&1`

```
[Desktop Entry]
Type=Application
Name=9Router
Comment=9Router API Proxy
Exec=/home/dr/.config/nvm/versions/node/v24.16.0/bin/node /home/dr/.local/lib/node_modules/9router/cli.js --tray --skip-update
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
```

## [f40_20241_metrics]
**Comando:** `timeout 3 curl -s http://127.0.0.1:20241/metrics 2>&1 | head -3; timeout 3 curl -s http://127.0.0.1:20242/metrics 2>&1 | head -3`

```
# HELP build_info Build and version information
# TYPE build_info gauge
build_info{goversion="go1.26.8",revision="2026-09-24-16:07 UTC",type="",version="2026.9.3"} 1
# HELP build_info Build and version information
# TYPE build_info gauge
build_info{goversion="go1.26.4",revision="2026-08-31-10:04 UTC",type="",version="2026.8.3"} 1
```

## [f41_45351_id]
**Comando:** `docker exec hermes-agent sh -c 'ss -tlnp 2>/dev/null | grep 45351 || netstat -tlnp 2>/dev/null | grep 45351' 2>&1 | head -5`

```

```

## [f42_45351_more]
**Comando:** `
docker exec hermes-agent sh -c 'cat /run/service/dashboard/run 2>/dev/null | head -15' 2>&1
echo ---
docker exec hermes-agent sh -c 'ps aux 2>/dev/null | grep -iE "dashboard|45351" | head -5' 2>&1
echo ---
docker exec hermes-agent sh -c 'python3 -c "import socket; s=socket.socket(); s.settimeout(1); s.connect(("127.0.0.1",45351)); print(s.recv(100))" 2>&1' 2>&1 | head -3
`

```
#!/command/with-contenv sh
# shellcheck shell=sh
# Dashboard service. Always declared so s6 has a supervised slot; if
# HERMES_DASHBOARD isn't truthy the run script exits cleanly and the
# companion finish script returns 125 (s6's "permanent failure, do
# not restart" marker), so s6-svstat reports the slot as down. See
# also docker/s6-rc.d/dashboard/finish.

case "${HERMES_DASHBOARD:-}" in
    1|true|TRUE|True|yes|YES|Yes) ;;
    *)
        # Exit 0; the finish script will exit 125 → s6-supervise won't
        # restart us and the slot reports down. Using a clean exit
        # (rather than `exec sleep infinity`) means s6-svstat reflects
        # reality: when HERMES_DASHBOARD is unset, the service is NOT
---
root          31  0.0  0.0    232    12 ?        S    04:26   0:00 s6-supervise dashboard
hermes       145  0.7  2.5 1041344 202012 ?      Ssl  04:26   0:56 /opt/hermes/.venv/bin/python3 /opt/hermes/.venv/bin/hermes dashboard --host 127.0.0.1 --port 9119 --no-open
hermes      8263  9.2  0.1  14440  9232 ?        S    06:28   0:00 ssh -i /home/dr/.hermes/home/.ssh/id_ed25519 -o BatchMode=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=8 dr@localhost  docker exec herme
root        8272 20.0  0.0   2688  1884 ?        Ss   06:28   0:00 sh -c ps aux 2>/dev/null | grep -iE "dashboard|45351" | head -5
root        8279  0.0  0.0   3516  1768 ?        S    06:28   0:00 grep -iE dashboard|45351
---
  File "<string>", line 1
    import socket; s=socket.socket(); s.settimeout(1); s.connect((127.0.0.1,45351)); print(s.recv(100))
                                                                  ^^^^^^^
```

## [f43_portal]
**Comando:** `ps aux | grep -iE 'portal|2528' | grep -v grep | head -5; echo ---; docker exec hermes-agent sh -c 'ls /opt/hermes/docker 2>/dev/null; env | grep -iE "PORT|PORTAL" | head -8' 2>&1 | head -12`

```
dr          1564  0.0  0.0 310764  6632 ?        Sl   01:26   0:00 /usr/libexec/ibus-portal
dr          2522  0.0  0.0 611868  7208 ?        Ssl  01:26   0:00 /usr/libexec/xdg-document-portal
root        2528  0.0  0.0   2716  1896 ?        Ss   01:26   0:00 fusermount3 -o rw,nosuid,nodev,fsname=portal,auto_unmount,subtype=portal -- /run/user/1000/doc
dr          2551  0.0  0.1 371000 15520 ?        Ssl  01:26   0:00 /usr/libexec/flatpak-portal
dr          2608  0.0  1.5 55141484 126696 ?     Sl   01:26   0:00 /app/Bitwarden/bitwarden-app --type=gpu-process --ozone-platform=x11 --enable-crash-reporter=36d9b6c5-c871-44dc-8992-69be3fa3a425,no_channel --user-data-dir=/home/dr/.var/ap
---
SOUL.md
cont-init.d
entrypoint-dispatch.sh
entrypoint.sh
hermes-exec-shim.sh
main-wrapper.sh
s6-rc.d
stage2-hook.sh
tini-shim.sh
WIFI_BENEFICENCIA_PORTUGUESA=saude@hbpscs
API_SERVER_PORT=8642
OBSIDIAN_REST_INSECURE_PORT=27123
```

## [f44_45351_last]
**Comando:** `
for pid in $(ls /proc | grep -E "^[0-9]+$"); do
  uid=$(awk "/^Uid:/{print \$2}" /proc/$pid/status 2>/dev/null)
  [ "$uid" = "0" ] || continue
  exe=$(readlink /proc/$pid/exe 2>/dev/null)
  case "$exe" in
    *node*|*python*|*caddy*|*nginx*|*traefik*) echo "pid=$pid exe=$exe" ;;
  esac
done 2>/dev/null | head -10`

```

```

## [f45_9remote_proc]
**Comando:** `grep -rl '45351' /usr/local/lib/node_modules/9remote/dist/ 2>/dev/null | head -3; ps aux | grep -i 9remote | grep -v grep | head -3; echo RC_DONE`

```
RC_DONE
```

## [f46_workspace_listen]
**Comando:** `docker exec hermes-workspace sh -c 'ls /proc/net/tcp >/dev/null && cat /proc/net/tcp | awk "NR>1 {print \$2}" | head -15' 2>&1`

```
572E5B64:2710
572E5B64:D538
00000000:4EA0
0100007F:4F12
0100007F:4F11
3500007F:0035
3600007F:0035
572E5B64:01BB
0100007F:0BB8
0100007F:1538
00000000:0016
0100007F:21C2
0100007F:B127
0100007F:0277
0100007F:239F
```

## [f47_45351_headers]
**Comando:** `timeout 3 curl -s -X POST http://127.0.0.1:45351/ -H 'Content-Type: application/json' -d '{}' -i 2>&1 | head -8; timeout 3 curl -s http://127.0.0.1:45351/healthz 2>&1 | head -c 100`

```
HTTP/1.1 404 Not Found
Date: Wed, 07 Oct 2026 06:29:29 GMT
Content-Length: 19
Content-Type: text/plain; charset=utf-8
```

## [f48_workspace_ps]
**Comando:** `docker exec hermes-workspace sh -c 'ps aux 2>/dev/null | head -15' 2>&1`

```

```

## [f49_workspace_procs]
**Comando:** `
docker exec hermes-workspace sh -c 'for p in /proc/[0-9]*; do pid=${p#/proc/}; cmd=$(tr "\\0" " " < $p/cmdline 2>/dev/null | cut -c1-60); [ -n "$cmd" ] && echo "$pid $cmd"; done | head -12' 2>&1
`

```
1 /usr/bin/tini -- /usr/local/bin/docker-entrypoint.sh node --
1789 sh -c for p in /proc/[0-9]*; do pid=${p#/proc/}; cmd=$(tr "\
1795 sh -c for p in /proc/[0-9]*; do pid=${p#/proc/}; cmd=$(tr "\
1796 head -12 
8 node --max-old-space-size=2048 server-entry.js 
```

## [f50_agent_procs]
**Comando:** `
docker exec hermes-agent sh -c 'for p in /proc/[0-9]*; do pid=${p#/proc/}; cmd=$(tr "\\0" " " < $p/cmdline 2>/dev/null | cut -c1-70); [ -n "$cmd" ] && echo "$pid $cmd"; done | grep -vE "s6-|/proc/" | head -20' 2>&1
`

```
145 /opt/hermes/.venv/bin/python3 /opt/hermes/.venv/bin/hermes dashboard -
146 sleep infinity 
17 /bin/sh -e /run/s6/basedir/scripts/rc.init top /opt/hermes/docker/main
171 /opt/hermes/.venv/bin/python3 /opt/hermes/.venv/bin/hermes gateway run
203 sleep infinity 
251 node /opt/data/.npm/_npx/3dfbf5a9eea4a1b3/node_modules/.bin/mcp-server
252 /opt/hermes/.venv/bin/python3 /opt/hermes/tools/mcp_death_supervisor.p
262 node /opt/data/.npm/_npx/a3241bba59c344f5/node_modules/.bin/mcp-server
271 node /opt/data/.npm/_npx/f36605d6814ff2b0/node_modules/.bin/obsidian-m
303 node /opt/data/.npm/_npx/f36605d6814ff2b0/node_modules/.bin/obsidian-m
304 node /opt/data/.npm/_npx/3dfbf5a9eea4a1b3/node_modules/.bin/mcp-server
305 node /opt/data/.npm/_npx/a3241bba59c344f5/node_modules/.bin/mcp-server
3147 /opt/hermes/.venv/bin/python3 /opt/hermes/.venv/bin/hermes 
3182 node /opt/data/.npm/_npx/f36605d6814ff2b0/node_modules/.bin/obsidian-m
3188 node /opt/data/.npm/_npx/3dfbf5a9eea4a1b3/node_modules/.bin/mcp-server
3196 node /opt/data/.npm/_npx/a3241bba59c344f5/node_modules/.bin/mcp-server
3204 /opt/hermes/.venv/bin/python3 /opt/hermes/tools/mcp_death_supervisor.p
321 /opt/hermes/.venv/bin/python3 /opt/hermes/tools/mcp_death_supervisor.p
4952 /opt/hermes/.venv/bin/python3 /tmp/hermes_kernel_vxf7rron/hermes_kerne
6065 /opt/hermes/.venv/bin/python3 /tmp/hermes_kernel_u4b__xep/hermes_kerne
```

## [f51_agent_sockets]
**Comando:** `
docker exec hermes-agent sh -c 'for pid in 145 171 3147; do echo "pid $pid fds:"; for fd in /proc/$pid/fd/*; do t=$(readlink $fd 2>/dev/null); case $t in socket*) echo -n "$t ";; esac; done; echo; done' 2>&1 | head -10
`

```
pid 145 fds:

pid 171 fds:

pid 3147 fds:
```

## [f52_inodes]
**Comando:** `
inode_45351=12159
docker exec hermes-agent sh -c 'for pid in 1 8 17 145 146 171 203 3147; do for fd in /proc/$pid/fd/*; do t=$(readlink $fd 2>/dev/null); case $t in socket:\[12159\]) echo "MATCH pid=$pid $t";; esac; done; done; echo DONE' 2>&1
`

```
DONE
```
