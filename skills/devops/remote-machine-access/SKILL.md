---
name: remote-machine-access
description: "Use when accessing home machines via Tailscale and 9Remote."
version: 1.0.0
author: Nous Research
license: MIT
platforms: [linux, macos, windows]
required_credential_files:
  - path: ~/.hermes/remote-access.env
    description: Credentials for 9Router dashboard and Tailscale (NINEROUTER_DASHBOARD_PASSWORD, TAILSCALE_AUTH_KEY)
metadata:
  hermes:
    tags: [tailscale, 9router, 9remote, remote-access, infrastructure]
    homepage: https://github.com/NousResearch/hermes-agent
---

# Remote Machine Access (Tijolão / Home Lab)

Access the user's home machine ("Tijolão") and its services via Tailscale + 9Router + 9Remote. This is the path to reach Google Drive credentials, local files, and services that only exist on the physical machine.

## Architecture

- **Tailscale mesh**: `Tijolao.tail9e88c5.ts.net` (100.91.46.87) — encrypted overlay network
- **9Router dashboard**: `https://Tijolao.tail9e88c5.ts.net/dashboard` — manages API endpoints, proxy pools, API keys
- **9Remote** (installed on Tijolão): provides Terminal, Desktop (screen sharing), Files (browse/edit) via the same Tailscale URL
- **Services on Tijolão**: 9router (port 9119), n8n, hermes-gateway, hermes-workspace (port 3000), hermes-dashboard, extracao-clinica-sasi
- **Cofre**: `/home/dr/projetos/.env` on Tijolão holds all provider credentials (Google, OpenAI, etc.)

## Credentials

All secrets live in the cofre on Tijolão. This skill reads from a local mirror at `~/.hermes/remote-access.env` (create once, mode 0600):

```bash
# ~/.hermes/remote-access.env
NINEROUTER_DASHBOARD_PASSWORD=<from cofre §9>
TAILSCALE_AUTH_KEY=<from cofre §9 if needed>
```

## Procedure: Reach Tijolão from this session

### 1. Verify Tailscale connectivity

```bash
# From this machine
ping -c 2 Tijolao.tail9e88c5.ts.net
# Should resolve to 100.91.46.87 and respond
```

If unreachable: Tailscale is not running on this machine, or the tailnet is different. Ask the user to start Tailscale or verify the tailnet name.

### 2. Authenticate to 9Router dashboard

```bash
# Load password from local mirror
source ~/.hermes/remote-access.env
# Open dashboard in browser tool
# URL: https://Tijolao.tail9e88c5.ts.net/dashboard
# Submit password field with $NINEROUTER_DASHBOARD_PASSWORD
```

Dashboard shows: API endpoints (Local/Tunnel/Tailscale), API keys, proxy pools, skills, media providers.

### 3. Use 9Remote for full machine access

From the 9Router dashboard, navigate to **9Remote** (computer icon). Three capabilities:

| Capability | Use for |
|------------|---------|
| **Terminal** | Full shell, run commands, access cofre, run rclone |
| **Desktop** | Screen sharing, GUI apps, browser OAuth flows |
| **Files** | Browse/edit filesystem, download/upload |

**Terminal** is the primary path for this skill — it gives a real shell on Tijolão where rclone, gdrive, and the cofre are available.

### 4. Execute on Tijolão via 9Remote Terminal

Once in the 9Remote terminal:

```bash
# On Tijolão
source /home/dr/projetos/.env          # load all credentials
rclone lsd gdrive:                      # list Google Drive remotes
rclone copy gdrive:"Currículo_Dr_Nicholas_ABC_atualizado_2026.pdf" /tmp/
# ... any command that needs local creds or hardware
```

### 5. Browser OAuth flows (Google Drive, etc.)

Use **9Remote Desktop** for any OAuth consent screen that must run on the user's actual Google account:

1. Open 9Remote Desktop from dashboard
2. Navigate to `https://console.cloud.google.com/` in the remote browser
3. Complete OAuth consent — the browser runs on Tijolão with the user's logged-in session
4. Tokens save to Tijolão's `~/.config/rclone/rclone.conf` or `~/.hermes/google_token.json`

## Pitfalls

- **This session ≠ Tijolão**: Hermes runs in a container/VM without Tailscale, without the cofre, without rclone config. Never assume local access to `~/.config/rclone`, `~/projetos/.env`, or Google tokens.
- **9Remote is the bridge**: Without 9Remote installed and running on Tijolão, you cannot reach the terminal, desktop, or files. The dashboard alone only shows metadata.
- **OAuth must run on Tijolão**: Google OAuth consent screens require the user's actual browser session. Running OAuth in this session's browser tool hits "localhost:1" unreachable and fails. Use 9Remote Desktop.
- **Dashboard login ≠ machine access**: Logging into 9Router dashboard only proves network reachability. It does not grant shell or file access.
- **Cofre is on Tijolão**: The real `/home/dr/projetos/.env` lives on Tijolão. This session only has a curated subset in `~/.hermes/remote-access.env`.
- **Tailscale IP is stable**: `100.91.46.87` and `Tijolao.tail9e88c5.ts.net` are the canonical addresses. Do not hardcode LAN IPs.

## Quick Reference Commands

```bash
# Check Tailscale connectivity from here
tailscale ping Tijolao

# SSH direct (if SSH enabled on Tijolão)
ssh dr@Tijolao.tail9e88c5.ts.net

# 9Router API (with key from dashboard)
curl -H "Authorization: Bearer sk-..." https://Tijolao.tail9e88c5.ts.net/api/v1/models

# Rclone on Tijolão (after 9Remote Terminal)
rclone config show gdrive
rclone lsd gdrive:
rclone copy gdrive:foo/bar.pdf /tmp/
```

## Related Skills

- `google-workspace` — once you have Terminal on Tijolão, run its setup.py there to authorize Google Drive
- `maintaining-linux-workstations` — for Tijolão hygiene (RAM, ZRAM, ufw, smartmontools)
