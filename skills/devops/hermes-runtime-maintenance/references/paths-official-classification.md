Tabela canônica — raiz de ~/.hermes vs. .gitignore oficial (docs/user-guide/profile-distributions.md) e proveniência no código (/opt/hermes). Uso: auditoria rápida antes de tocar.

CATEGORIA | CAMINHOS OFICIAIS (nunca apagar/mover) | LIXO-VERDADEIRO (segundo data + não-no-código)
--- | --- | ---
Segredos | .env (symlink pro cofre), auth.json, auth.lock | (nenhum — nunca lixo)
Identidade | SOUL.md | (nenhum)
User data | memories/, plans/, workspace/, sessions/, logs/, cron/, home/, pastes/ | backups *.bak* órfãos sem original ativo
Runtime DB (ficheiros na **raiz**) | state.db(+shm/wal), kanban.db(+…), response_store.db(+…), runs_idempotency.db(+…), shared-state.db, projects.db, verification_evidence.db, channel_directory.json | (nenhum — todos ativos)
Pasta `state/` (subdir) | Heartbeats/sentinela Nous: gateway.heartbeat, gateway.lifecycle.json, dashboard_clients.heartbeat (ver gateway/shutdown_watchdog.py, lifecycle_ledger.py, scale_to_zero.py) — **não** substitui state.db | docs teus aqui
Runtime locks/status raiz | gateway_state.json, gateway.{pid,sock,lock}, processes.json, spawn-ledger.json, *.lock, .env.lock, .mcp-discovery.lock, .restart_last_processed.json, .update_check, install_id, .skills_prompt_snapshot.json, context_length_cache.yaml, models_dev_cache.*, provider_models_cache.json, shell-hooks-allowlist.json, tui-theme-boot.json, web-ui-build-stamp.json, webui-mvp/ | logs soltos na raiz → logs/
Caches regeneráveis | cache/, image_cache/, audio_cache/, models_dev_cache.*, ollama_cloud_models_cache.json, .cache/ | .npm/_cacache (fora do runtime), cache/uv dentro redundante com home/.cache/uv
Infra/estado do container | installs/ (binário docker), bin/ (tirith), scripts/, platforms/, pairing/, photon/, sandboxes/, proxy/, runtime/, terminal-sessions/, telemetry/, hooks/, mcp-tokens/, plugins/, plugin-update-checks/, skins/, bin/ | --

Regra: dado um item, se aparece no código (/opt/hermes via rg -m1) → oficial. Se NÃO aparece E não foi escrito recentemente (<72h) → candidato a lixo; antes de apagar, confirmar não é lock de processo vivo ou arquivo de estado.
