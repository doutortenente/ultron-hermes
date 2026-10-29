# hermes-workspace — pesquisa, plano e aplicação (29-out-2026)

## Conclusão
Já está configurado e funcionando. Nada precisou ser reinstalado. Medido hoje:

| Item | Resultado medido |
|---|---|
| Container hermes-workspace | Up, healthy (imagem hermes-workspace:tijolao) |
| UI porta 3000 | HTTP 200 |
| Agente (gateway 8642 / dashboard 9119) | v0.22.2, gateway running, Telegram ligado |
| connection-status | "enhanced" — chat + APIs do dashboard ok |
| Fork vs upstream (outsourc-e) | 4 à frente, 0 atrás (upstream parado desde 22-ago-2026) |
| Acesso remoto | tailscale serve :10000 -> 3000 (só tailnet) |
| Rotas testadas | models, sessions, skills, mcp, files, memory/list, memory/read, hermes-config, hermes-tasks: todas ok |

Única falha: /api/memory (rota antiga) dá 404 do agente — a tela de Memória NÃO usa ela
(usa /api/memory/list e /read, que funcionam). Sem impacto.

## Pesquisa (fontes)
- Oficial do projeto: github.com/outsourc-e/hermes-workspace (comunitário, não oficial da Nous).
- Modos de uso hoje: (1) docker compose junto do agente, (2) imagem pronta ghcr.io/outsourc-e/hermes-workspace:latest
  (Coolify/Easypanel/Hostinger), (3) build do código-fonte, (4) instalador hermes-workspace.com.
- Boas práticas recorrentes (README + issues #50, #157, #560):
  1. HERMES_API_TOKEN = API_SERVER_KEY do agente (senão 401 em tudo menos /health).
  2. HERMES_API_URL :8642 e HERMES_DASHBOARD_URL :9119 apontando pro agente.
  3. Rede compartilhada com o agente (network_mode host/service) evita "connection refused".
  4. Publicou a 3000 fora do loopback -> ligar HERMES_PASSWORD, COOKIE_SECURE=1, TRUST_PROXY=1.
  5. Atualizar = git pull + rebuild; refazer prova de saúde.

## Configuração atual vs boas práticas
| Prática | Tijolão |
|---|---|
| Token = API_SERVER_KEY | sim (compose usa ${API_SERVER_KEY:?} — falha alto se faltar) |
| URLs do agente | sim |
| Rede compartilhada | network_mode: host |
| Senha de sessão | desligada; HOST=127.0.0.1 + tailscale serve só tailnet (decisão sua) |
| Pasta de trabalho | HERMES_WORKSPACE_DIR=/home/dr/src |

## Plano de manutenção (mensal)
1. ssh host: git -C ~/src/hermes-workspace fetch upstream && git rev-list --left-right --count HEAD...upstream/main
2. Se "atrás" > 0: git merge upstream/main na branch tijolao.
3. Rebuild: wrapper `tijolao` (compose em ~/.config/hermes-stack/docker-compose.tijolao.yml, --env-file do cofre).
4. Prova: curl 127.0.0.1:3000 (200) + /api/connection-status ("enhanced").

## Correção pendente de documentação
Skill hermes-workspace cita compose em ~/src/tijolao-ai/hermes-stack (NÃO existe) e agente v0.21.1.
Real: ~/.config/hermes-stack/docker-compose.tijolao.yml e v0.22.2.
