# Mapa de `~/.hermes` (Tijolão)

**O que é:** pasta de **estado vivo** do Hermes — não é projeto de código. ~86 entradas na raiz é **normal** (caminhos fixos no agente).

**Regra de ouro:** não mover/apagar o que está na coluna “não mexer” sem saber o que faz. Limpeza pesada: skill `hermes-runtime-maintenance`.

---

## Núcleo (identidade + config)

| Caminho | Função |
|---------|--------|
| `config.yaml` | Preferências (modelo, MCP, Telegram, hooks ULTRON…) |
| `.env` | Symlink → `~/.local/secrets/.env` (senhas) |
| `auth.json` | Login OAuth do agente |
| `SOUL.md` | Personalidade do assistente |
| `memories/` | `USER.md` + `MEMORY.md` (memória longa) |
| `plans/` | Planos teus (ex.: ULTRON) — **dado seu**, não lixo |

---

## Conversa e gateway

| Caminho | Função |
|---------|--------|
| `state.db` | Histórico de sessões (grande = normal) |
| `sessions/` | Metadados de sessão; `request_dump_*` antigos podem apagar |
| `gateway*`, `gateway.sock` | Processo gateway (Telegram + API :8642) |
| `channel_directory.json` | Roteamento de canais |

---

## Onde você trabalha

| Caminho | Função |
|---------|--------|
| `workspace/` | Mesa de trabalho do agente (arquivos de tarefa) |
| `home/` | HOME “falso” dos subprocessos (`context7-mcp`, npm, ssh…) — **não apagar** |
| `~/src` | Código real (montado no Docker, não dentro de `.hermes`) |

---

## Automação e extras

| Caminho | Função |
|---------|--------|
| `cron/` | Tarefas agendadas do Hermes |
| `kanban/` + `kanban.db` | Quadro de tarefas |
| `plugins/`, `desktop-plugins/` | Honcho, disk-cleanup, etc. |
| `skills/` | Skills (catálogo + tuas em `devops/`) |
| `scripts/` | (vazio / removido whatsapp-bridge) |
| `webui-mvp/` | Gravações/UI experimental — runtime |
| `terminal-sessions/` | Estado terminal — runtime |

---

## Cache e peso (pode crescer de novo)

| Caminho | Tamanho típico | Nota |
|---------|----------------|------|
| `installs/` | ~1,6 GB | Ambientes do container; regenerável parcialmente |
| `cache/` | ~800 MB | Spillover, MCP, etc. |
| `home/` | ~400 MB | Cache npm/uv espelhado |
| `logs/` | dezenas MB | Logs oficiais rotativos |
| `models_dev_cache.json` | ~6 MB | Catálogo de modelos |

Plugin **`disk-cleanup`** + `hermes doctor --fix` = manutenção oficial antes de `rm` manual.

---

## Git nesta pasta

**Repo público:** [github.com/doutortenente/ultron-hermes](https://github.com/doutortenente/ultron-hermes) — só subset versionável (`README`, `config.yaml` com `${ENV}`, `SOUL.md`, `plans/`, `scripts/`, skills custom). **`memories/` fica fora do git** (dado pessoal).

Runtime (`auth.json`, `*.db`, caches) continua ignorado via `.gitignore`.

---

## Checklist rápido pós-restart

```bash
curl -fsS http://127.0.0.1:8642/health
~/.config/hermes-stack/scripts/ultron-health.sh
```

---

*Alinhado a `skills/devops/hermes-runtime-maintenance/references/paths-official-classification.md`.*
