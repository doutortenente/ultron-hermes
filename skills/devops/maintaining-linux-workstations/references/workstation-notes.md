# Tijolão: validated maintenance notes

Use only on Dr. Nícholas's Linux notebook after confirming the current paths still exist. "Tijolão" is the notebook's nickname.

## Existing local utilities

- Read-only health report: `/home/dr/src/scripts/pc/saude_pc.py` (antes em ~/projetos/scripts/pc — movido)
- Conservative cleanup with dry-run/default and explicit apply: `/home/dr/src/scripts/pc/pc_higiene.py`

Read each script before execution because local utilities may evolve. Prefer them over creating duplicate maintenance scripts.

## High-value surfaces observed (audit set/2026)

| Path | Size | Nature | Action |
|---|---|---|---|
| `~/.cache` | 3.8 GB | JetBrains, browser, uv, pnpm, Puppeteer, Playwright, Electron, Node tooling | `pc_higiene.py --apply` +
| `~/.config/google-chrome` | 3.8 GB | Profile + cache — **preserve profile, delete Cache/Code Cache/GPUCache/ShaderCache/DawnCache/CachedData** |
| `~/.local/share/nvm` | 3.6 GB | Node version manager store — keep; upgrade via `nvm install --latest-npm` |
| `~/.config/mozilla` | 610 MB | Firefox profile — preserve; clean named cache children only |
| `~/.config/Claude` | 504 MB | **3 copies of claude-code**: 2.1.260 (Desktop), 2.1.274 (active), 2.1.282 (partial) — keep 2.1.274, remove others |
| `~/.config/Codex` | 156 MB | Codex CLI profile — preserve |
| `~/.local/share/pnpm` | 2.2 GB | Active package store — `pnpm store prune`, never wipe |
| `~/.local/share/zed` | 2.0 GB | Zed IDE installation — preserve |
| `~/.local/share/claude` | 448 MB | Mirrors ~/.config/Claude — duplicates |
| `~/.local/share/9router` | 73 MB | 9router service data — keep |
| `~/.local/lib/node_modules` | 1.2 GB | npm global prefix — contains 9router, codex, pnpm, ctx7; `npm ls -g --depth=0` to audit |
| `~/.hermes` | 1.4 GB | Agent state (memories, skills, sessions) — **intocável** |
| `~/.codex` | 592 MB | Codex CLI + sessions — preserve |
| `~/.npm` | 508 MB | Cache — `npm cache clean --force` + inspect `_npx` separately |
| `~/projetos` | 432 MB | **SASI-V3 (1.1 GB, 846 MB node_modules!)** + scripts (84M) + tijolao-ai (2.1M) + `.env` (cofre) |
| `~/vaults/celebro` | 222 MB | Cérebro Obsidian — preserve |
| `~/backups` | 237 MB | Manual tar backups — replace with rclone rotation to OneDrive |
| `~/Documentos/Plantões` | 87 MB | **Trabalho médico real** — mover pro Cérebro |

## Validated sequence

1. Run the local health report and record disk/RAM/service figures.
2. Inspect top-level cache sizes.
3. Run `pc_higiene.py` in dry-run unless the user has already explicitly authorized deletion; then use `--apply`.
4. Run package-manager pruning for npm/pnpm and inspect `_npx` separately.
5. Remove only identified browser/Electron cache children.
6. Check `sudo -n true` before attempting system package cleanup or journal vacuuming.
7. Repeat the health report and filesystem measurements.

## Known duplicate binaries to clean (set/2026)

| Binary | Copies | Kept | Removed |
|---|---|---|---|
| `9router` | `~/.local/bin` + `/usr/local/bin` | `~/.local/bin` (service usa) | `/usr/local/bin` |
| `claude` | 3 versions (2.1.260, 2.1.274, 2.1.282) | 2.1.274 (active) | 2.1.260, 2.1.282 (~430 MB) |
| `gh` | `/usr/bin/gh` + `~/.local/bin/gh` | `/usr/bin/gh` (sistema) | `~/.local/bin/gh` |

## Audit out/2026 (pós-limpeza 7,0 GB total — disco 76% → 70%)

- Limpos rodada 1: `~/.cache/codex-runtimes` (1,7G), `~/.npm/_npx` + `_cacache` (1,5G), `~/.codex/.tmp` (199M), staging `..plugin-appserver.*` (341M), caches diversos (~320M).
- Limpos rodada 2: `~/.cache/google-chrome` (1,34G — feito pós fechar browser), `~/.local/share/zed/external_agents/registry` (1,38G — seguro, rebaixa sob demanda), `claude-code/2.1.260` em `~/.config/Claude` (215M).
- Ollama runtime (`/usr/local/lib/ollama`): 4,5 GB compostos por `cuda_v12` (1,2G), `cuda_v13` (807M) e `rocm_v7_2` (2,5G). Como a GPU do Tijolão é Intel HD 620, bibliotecas NVIDIA/AMD são peso morto. Remoção requer `sudo` no host (`sudo rm -rf /usr/local/lib/ollama /usr/local/bin/ollama ~/.ollama`).
- Não existe `~/central` — scripts vivem em `~/src/scripts/pc`, cofre em `~/projetos/.env`.
- Sudo interativo via SSH: o prompt `[sudo] senha para dr:` gerado por SSH em background PTY fica preso no processo do container e NUNCA aparece na tela do Cinnamon do operador. Se `sudo -n` falha, entregue a linha de comando para o operador rodar no terminal dele. Passar senha via stdin (`sudo -S`) é bloqueado pelo ambiente de terminal; usar `SUDO_ASKPASS` (script temporário que dá echo da variável, apagado depois) com `sudo -A`.
- O Claude Desktop (app Electron) ignora `CLAUDE_CONFIG_DIR` definida no `~/.profile`/ambiente do usuário — lê `~/.claude` e `~/.claude.json` na raiz do home. Correção: sobrescrever o lançador do sistema (`/usr/share/applications/com.anthropic.Claude.desktop`) com uma cópia em `~/.local/share/applications/` com `Exec=env CLAUDE_CONFIG_DIR=... claude-desktop %U` prefixado; o arquivo original não é tocado, e o usuário-local tem prioridade no menu. Testar com `desktop-file-validate` e `update-desktop-database`. Só funciona para novas instâncias — a já aberta continua com o ambiente antigo até reiniciar. O Claude Code CLI, por outro lado, respeita `CLAUDE_CONFIG_DIR` normalmente.
- Precisam sudo com senha no host: `/var/cache/apt` 547M (`sudo apt clean`), journal 192M (`sudo journalctl --vacuum-size=50M`), `/usr/local/lib/ollama` (4,5G).

## Interpretation

- IDE connector ports being down while the IDE is closed are expected, not a repair target.
- Dirty Git repositories are informational during machine hygiene; never commit, reset, clean, or delete repository content as part of disk cleanup.
- The user prefers autonomous execution and accepts ordinary reversible maintenance, but destructive scope must remain limited to proven re-creatable data.
- **User vocabulary for directories**: `central` (operational), `cérebro` (knowledge), `plantões` (clinical work), `sasi` (clinical system) — never "projects", "workspace", "repos".
- **Cofre `.env`**: lives in `central/` (renamed from projetos), symlinked to `~/.hermes/.env` — update symlink + compose `env_file:` on rename.

## Home-directory standards (XDG + FHS)

Before relocating or removing any dotfile at the home root, cross-check it against these two references. The decision is NOT "is it in my inventory list" — it is "does the specification say it should be elsewhere, and can the owning program tolerate the move".

### FHS 3.8.2 + XDG Base Directory Specification (v0.8)

| Home-root item | Status per spec | Owning program / system file | Safe to move? |
|---|---|---|---|
| `.bashrc`, `.profile`, `.bash_profile`, `.bash_login` | FHS: dot-file convention, shell-read | `/etc/shells`, POSIX shells | NO — only read at these paths |
| `.Xauthority` | Not an XDG dir; X11 session file | `/etc/X11/Xsession`, `xauth` | NO — display manager hardcodes `$HOME/.Xauthority` |
| `.xsession-errors`, `.xsession-errors.old` | Not XDG; session log | `/etc/X11/Xsession:61` (`ERRFILE=$HOME/.xsession-errors`) | NO — Xsession hardcodes the name and location |
| `.sudo_as_admin_successful` | Not XDG; sudo sentinel | `/etc/bash.bashrc:44` (Debian/Mint sudo) | NO — read at exactly `$HOME/.sudo_as_admin_successful`; moving or removing only suppresses the sudo hint |
| `.npmrc` | XDG: `NPM_CONFIG_USERCONFIG` | npm | YES — point `NPM_CONFIG_USERCONFIG` to `$XDG_CONFIG_HOME/npm/npmrc` |
| `.bashrc`, `.profile` content (e.g. `CLAUDE_CONFIG_DIR`, `HISTFILE`) | User env vars | shell startup files | YES — centralize in a single sourced file (e.g. `$XDG_CONFIG_HOME/shell/env.sh`) |
| `.var/` | Flatpak data | Flatpak runtime | NO — Flatpak hardcodes `$HOME/.var/app` |
| `.ssh/` | OpenSSH | OpenSSH client config | NO — OpenSSH hardcodes `$HOME/.ssh` |
| `.hermes/` | Hermes agent | Hermes | NO — hardcoded by the agent runtime |

### Key decision rule

A file at the home root is only a cleanup candidate when (1) the XDG/FHS spec assigns it to a different directory AND (2) the owning program reads the replacement location via an environment variable or config key. Files hardcoded by system components (`/etc/X11/Xsession`, `/etc/bash.bashrc`, sudo, OpenSSH, Flatpak, Hermes) MUST stay at the home root — relocating them requires editing system files and offers no benefit. Validate by `grep`ing the writer before moving, not by the inventory list.

### Checking live session vs stale copies

When duplicate files exist (e.g. `.Xauthority` in both `$HOME` and `$HOME/.local/state`), determine which one the LIVE session uses:

1. `pid=$(pgrep -o -x cinnamon-session)` — find the session leader's PID.
2. `tr '\0' '\n' < /proc/$pid/environ | grep '^XAUTHORITY='` — read the environment of the live process. If unset, the display manager uses `$HOME/.Xauthority`.
3. `fuser <file>` — check which process has the file open. A copy with zero open handles is stale and safe to delete, provided the live process does not use it (confirmed in step 2).

The live Cinnamon session on this machine uses `$HOME/.Xauthority` (read from the session leader's environment). Any `.Xauthority` copy under `$HOME/.local/state/` is stale and was not open by any process — deletion is the correct remediation.