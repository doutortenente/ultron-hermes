---
name: hermes-runtime-maintenance
description: "Clean ~/.hermes without killing live gateway or MCPs."
---

# Limpeza de runtime Hermes (~/.hermes)

Manter a pasta de runtime do agente enxuta sem derrubar gateway, MCPs ou sessões ativas. A pasta vive de locks e caches em uso — confunde quem a limpa de fora.

## Sempre-verdadeiro

- **Runtime = ~/.hermes** (ou $HERMES_DIR). config.yaml, locks (.lock), *.db, auth.json e sockets são lidos constantemente pelo processo vivo — limpar sem identificar uso ativo pode matar conexão. **Gate permanente: nada de `rm`/`mv`/`hermes config` sobre este tree sem autorização explícita do usuário.** Diagnno-estudo e proponho; aprovação não é confirmação de erro, é protocolo.
- **home/** é HOME falso dos subprocessos (terminal.home_mode: auto), NÃO cache. .local/bin/ (ex.: context7-mcp) e .ssh/id_ed25519 dentro são referenciados pelo config.yaml e pelas skills — mover/limpar quebra MCP + bridge SSH ao host. Deixar como runtime ativo.
- **Locks (0 bytes) são sinônimos de vida** — .mcp-discovery.lock, gateway.lock, kanban.db.*.lock. Remover = forçar race condition; deixe-os.
- **Caches (state.db, models_dev_cache.json) têm papel** — não são 'lixo'; apagar sem anotação pode exigir re-login ou refetch de catálogo.


## Checklist: remover lixo sem matar runtime

1. Audite item a item contra a doc oficial antes de tocar: `du`/`stat` (tamanho + data) de cada raiz, e proveniência — `rg -lF --no-ignore -m1 <nome> /opt/hermes --glob '!.venv/**' --glob '!node_modules/**' | head -1` (ou `grep -rlF --exclude-dir=.venv --exclude-dir=node_modules`). **Nunca carregue a árvore inteira de /opt/hermes em memória** (timeout) — rg/grep pontual por item é a alavanca. Cruzar com o `.gitignore` de `docs/user-guide/profile-distributions.md`: state.db, response_store.db, gateway.pid, image_cache/, cache/, plans/, workspace/, home/, sandboxes/, backups/, bin/ são estado do framework — mover = quebrar. Lixo real é só o que não aparece no código E não foi gravado recentemente (conferir data de modificação).
2. Identifique backups órfãos — `find . -maxdepth 3 -type f \( -name '*.bak*' -o -name '*antes*' -o -name '*.old' \)`. Só delete se o original ativo existe ao lado.
3. sessions/request_dump_* são dumps antigos — seguros de apagar (sessions.json continua vivo e contém o estado real).
4. pastes/ é buffer de clipboard — apagar não mata nada.
5. **Logs soltos na raiz** (interrupt_debug.log, gateway-starts.log) estão FORA de logs/ — o agente não rotaciona esses nomes. Mover para logs/ (interrupt_debug.log regenera; não libera MB mas corrige o layout oficial do `.gitignore`). O log rotativo oficial (agent.log/errors.log, 5 MB ×3) já funciona — não toque.
5. .npm/_cacache e locks de package-lock são descartáveis.
6. Execute como usuário hermes (uid do runtime), nunca como root nesse tree — root grava arquivos inacessíveis ao agente.
7. Após limpeza, confirme runtime vivo: `ls gateway.lock .mcp-discovery.lock` e `curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8642/health`.
8. **Não equívale `home/.cache/uv` (800+ MB) com lixo** — é cache do uv espelhado de `~/.cache/uv`; confira se não está redundante antes de tocar. `cache/uv` (o interno) é runtime ativo → deixe.
9. **`installs/<hash>/` se regenera**: apagar os ~2 GB de `environments/*/workspace/tools/` (ffmpeg/python/chromium/node duplicando `/opt/hermes/tools`) é seguro — o launcher recria só o bootstrap de 16 K ao rodar `hermes` (verificado 21-out-2026: 2 GB apagados, gateway intacto). NÃO apague o bootstrap/`~/.local/bin/hermes` launcher em si.
10. **Sessions prune não libera DB size linearmente** — `hermes sessions prune --force` remove arquivos antigos, mas `state.db` (148 MB) persiste. Use `hermes sessions optimize` depois; o ganho é no filesystem, não sempre no `.db`.

## Armadilhas

- **Raiz de ~/.hermes com ~90 itens é normal.** Quase todos são caminhos fixos no código (/opt/hermes). Antes de mover/apagar: `search_files` pelo nome em /opt/hermes (excluir .venv/tests). Mover = quebrar. Lixo real é só o que não aparece no código E não é gravado recentemente (ver data de modificação).
- **home/** = HOME falso dos subprocessos (terminal.home_mode: auto). **workspace/**, **plans/**, **pastes/**, **webui-mvp/** são usados pelo runtime (webui-mvp/runs recebe gravações vivas) — não apagar.

- **`patch`/`write_file` em config.yaml é recusado** (arquivo de segurança). Use `hermes config set CHAVE VALOR`; para remover bloco, `terminal` com sed + `hermes config check` depois. Faça cópia em backups/config/ antes.
- **`hermes sessions prune/optimize` recusa enquanto gateway, dashboard ou a própria sessão seguram o state.db.** Ler a saída inteira: "Stop them first" = nada foi apagado. Não relatar sucesso sem conferir `hermes sessions stats` antes/depois.
- **`du` de ~/.hermes sobe sozinho**: installs/ (ambiente do container, ~2 GB) e lazy-packages/ são recriados pelo Hermes. Medir por pasta, não pelo total.

- **Deletar state.db sem aviso** mata memória de conversa — perde contexto acumulado.
- **Apagar auth.json** invalida login do gateway até re-auth.
- **Remover .env.bak antigo sem confirmar** que .env (symlink pro cofre) continua — raramente o backup é o atual.
- **Limpar home/ ou lsp/ sem ordem explícita** quebra instalação de dependências do agente — não é runtime lixo, é runtime funcionando.

## Manutenção documentada (sem rm manual)

- **Ordem obrigatória antes de qualquer script manual: (1) `hermes doctor --fix`, (2) config oficial (`sessions.auto_prune`, plugin `disk-cleanup`), (3) comandos oficiais (`sessions optimize/prune/optimize-storage --yes`). Só depois, e só se a doc não cobrir, script manual — o runtime sempre vence a mão (caches recriam, s6 religa). Erro real 21-out: persegui `optimize-storage` com script autônomo no host antes de rodar `doctor --fix`/ativar `auto_prune` — falso gatilho derrubou gateway+dashboard 40s sem necessidade.
- **`pkill -f <padrão>` mata a própria sessão SSH** se o padrão aparece na linha de comando (o wrapper do terminal ecoa o comando inteiro). Pra listar, usar truque de colchete `pgrep -f "optimiz[e]"`; pra matar, PID exato. Erro 21-out: matei minha própria sessão SSH.
- **Deletar `installs/*/environments/*/venv` quebra o `certifi` do web_extract** (caminho resolvido fica gravado). Correção: `mkdir -p <dir-pai> && ln -sfn /opt/hermes/.venv/lib/python3.14/site-packages/certifi <dir>/certifi`. Verificado 21-out.
- **state.db**: `hermes config set sessions.auto_prune true` (+ `retention_days`, 90 default) — poda automática oficial (docs/user-guide/sessions.md). Aplicado 21-out-2026.
- **Plugin embutido `disk-cleanup`** (`hermes plugins enable disk-cleanup`): rastreia lixo efêmero e limpa no fim da sessão; `/disk-cleanup status|dry-run|quick|deep`. Aplicado 21-out-2026.
- Skills paradas: `hermes curator prune --days N` arquiva SKILLS ADOTADAS (created_by != null), reversível via `curator restore`. **SKILLS BUNDLED/DEFAULT nunca-usadas NÃO são vistas pelo curator** (`nothing to prune` apesar de centenas nunca usadas) → desative via `hermes config set skills.disabled + <nomes>`; alavanca oficial, reversível, sobrevive a updates. Selecionar com `.usage.json`: created_by=null E uses=0.
- **Raiz com ~75-90 itens é o formato oficial** (varia por feature flags) — todos são caminhos fixos no código. O .gitignore de profile-distributions.md (docs) nomeia state.db, response_store.db, gateway.pid, image_cache/, cache/, plans/, workspace/, home/, sandboxes/, backups/, bin/ como estado do framework. Mover = quebrar.

- **Cofre `~/.local/secrets/` é montado :ro no container** — mover arquivo para lá de dentro falha (EROFS/EXDEV). Usar a ponte SSH (`tijolao-ssh-bridge`) com `cat | ssh 'cat >'` e conferir md5 dos dois lados (feito 21-out-2026).
- **`hermes config set` aceita chaves aninhadas** (ex.: `mcp_servers.github.env.GITHUB_PERSONAL_ACCESS_TOKEN '${GITHUB_TOKEN}'`) — forma correta de tirar segredo literal do config.yaml; `config get` resolve a referência e mostra o valor, conferir o cru com `search_files` no arquivo.
- **`sessions/sessions.json` é espelho legacy** — matar com `hermes config set gateway.write_sessions_json false` e apagar o arquivo; a verdade vive em `gateway_routing` no state.db.
- **`hermes sessions optimize/optimize-storage` exigem gateway parado** — dentro de uma sessão viva do gateway é bloqueio real (não usar --force); documentar como passo pós-downtime.

## Ver também

- `maintaining-linux-workstations` (limpeza de SO, não runtime)
- `references/paths-official-classification.md` — tabela canônica de caminhos oficiais vs. lixo (use na auditoria de raiz).
- `tijolao-ssh-bridge` (ponte SSH para rodar comandos no host)
- `ninerouter-hermes` (gateway 9router no Tijolão)
