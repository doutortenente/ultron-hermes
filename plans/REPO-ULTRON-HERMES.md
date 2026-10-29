# ULTRON — config Hermes (Dr. Tenente)

Repositório **público** da parte versionável de `~/.hermes`: personalidade (`SOUL.md`), config do agente, planos e skills custom (`skills/devops/`). **Não** inclui runtime vivo (SQLite, `auth.json`, caches, `memories/`).

Stack completo ULTRON: Hermes + Tijolão (Docker) + n8n — ver `plans/ULTRON.md`.

## Clonar e usar

1. Backup do teu `~/.hermes` se já existir.
2. Copiar arquivos versionados para `~/.hermes` (mesclar com cuidado).
3. Criar `~/.local/secrets/.env` (ou symlink `~/.hermes/.env`) com pelo menos:

```bash
GITHUB_TOKEN=ghp_...
CONTEXT7_API_KEY=...
TELEGRAM_ALLOWED_CHATS=123456789
DASHBOARD_USERNAME=dr
DASHBOARD_PASSWORD_HASH='scrypt$...'
DASHBOARD_AUTH_SECRET=...
# Opcional: POSTGRES_MCP_DSN, NINEROUTER_KEY, ...
```

4. Context7 MCP: binário em `~/.hermes/home/.local/bin/context7-mcp` (ver `config.yaml`).
5. `hermes doctor` e gateway (`tijolao` ou `hermes gateway run`).

## MCP

`plans/MCP-AUDIT.md`

## Mapa da pasta

`plans/MAPA-HERMES-HOME.md`
