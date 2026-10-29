# Auditoria MCP (`config.yaml`) — 29-out-2026

Referência: [Hermes MCP config](https://github.com/nousresearch/hermes-agent/blob/main/website/docs/reference/mcp-config-reference.md) + skill local `hermes-agent/references/native-mcp.md`.

## Estado por servidor

| Servidor | Transporte | Status | Notas |
|----------|------------|--------|-------|
| **playwright** | stdio (`npx`) | Ativo | Corrigido: `-y`, `--headless`, reciclo `idle_timeout_seconds: 900` / `max_lifetime_seconds: 86400` (doc oficial — evita Chromium eterno na RAM). |
| **github** | stdio | Ativo | Token só via `env.GITHUB_PERSONAL_ACCESS_TOKEN: ${GITHUB_TOKEN}` (filtragem de env do Hermes). |
| **filesystem** | stdio | Ativo | Raiz `/home/dr` — escopo amplo de propósito; risco = qualquer skill pode pedir leitura/escrita nessa árvore. |
| **postgres** | stdio | `enabled: false` | Sem conexão/discovery enquanto desligado; DSN placeholder `${POSTGRES_MCP_DSN}`. |
| **context7** | stdio (binário em `home/.local/bin/`) | Ativo | `connect_timeout: 120` — cold start do binário; **não mover `home/`** (runtime falso). |
| **cloudflare** | HTTP + OAuth | `enabled: false` | Mantido no YAML para reativar com `hermes mcp login cloudflare`; exclude de tools pesadas já definido. |

## O que a doc exige e você já cumpre

- Chaves sob `mcp_servers:` (não `mcp:` / `servers:`).
- Segredos em `${VAR}` / `env:` explícito — nada de PAT literal no YAML.
- Servidor desligado = `enabled: false` (postgres, cloudflare), não apagar bloco.

## Verificação

```bash
hermes doctor          # MCP + token GitHub
curl -fsS http://127.0.0.1:8642/health
```

Gateway recarrega MCP em ~1 min após editar `config.yaml` (ou reiniciar gateway).
