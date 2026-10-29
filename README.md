# ULTRON — config Hermes (Dr. Tenente)

Repositório **público** da parte versionável de `~/.hermes`: personalidade (`SOUL.md`), config do agente, planos, scripts e skills custom. **Não** inclui runtime vivo (SQLite, `auth.json`, caches, `memories/`).

Stack completo ULTRON: Hermes + Tijolão (Docker) + n8n — ver `plans/ULTRON.md`.

## Clonar e usar

1. Backup do teu `~/.hermes` se já existir.
2. Copiar arquivos versionados para `~/.hermes` (mesclar com cuidado).
3. Criar `~/.local/secrets/.env` (ou symlink `~/.hermes/.env`) com pelo menos:

```bash
# Modelos / APIs (ajuste ao teu setup)
GITHUB_TOKEN=ghp_...
CONTEXT7_API_KEY=...

# Telegram + dashboard (não commitar)
TELEGRAM_ALLOWED_CHATS=123456789
DASHBOARD_USERNAME=dr
DASHBOARD_PASSWORD_HASH='scrypt$...'   # hermes dashboard / doc web-dashboard
DASHBOARD_AUTH_SECRET=...

# Opcional
POSTGRES_MCP_DSN=postgresql://...
NINEROUTER_KEY=...
```

4. Instalar binário Context7 no HOME falso do Hermes (se usar MCP context7):

```bash
# caminho referenciado em config.yaml
mkdir -p ~/.hermes/home/.local/bin
# instalar context7-mcp conforme doc Context7 / Hermes
```

5. `hermes doctor` e `hermes gateway run` (ou teu `tijolao`).

## MCP

Ver `plans/MCP-AUDIT.md`. Resumo: playwright com reciclo de memória; filesystem em `/home/dr`; postgres e cloudflare desligados até você ligar.

## Mapa da pasta runtime

`plans/MAPA-HERMES-HOME.md` — o que é normal na raiz de `~/.hermes` e o que não apagar.

## Licença

Config pessoal publicada para referência; reuse por sua conta e risco.
