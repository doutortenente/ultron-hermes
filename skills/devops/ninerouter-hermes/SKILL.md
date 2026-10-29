---
name: ninerouter-hermes
description: "Configure 9router gateway LLM local com Hermes no Tijolão."
---

# 9router + Hermes no Tijolão

O 9router é o gateway LLM local que roda no host (porta 20128). O Hermes se conecta via provider `custom` apontando `base_url: http://127.0.0.1:20128/v1` com `api_key: ${NINEROUTER_KEY_DEFAULT}` (modelo principal, delegação e os 17 `auxiliary.*`); `${NINEROUTER_KEY}` fica só no fallback. Esta skill cobre o ciclo operacional completo.

## Estado operacional conhecido (set/2026)

**Atualização 07-out-2026** (auditoria somente leitura): dados vivos = `~/.local/share/9router` (DATA_DIR/WorkingDirectory do service); `~/.9router` é legado de 23-set e recebe writes residuais do cli.js. `~/.config/autostart/9router.desktop` ainda aponta pro nvm velho — tray falha silenciosa no login (resíduo). `nvidia/z-ai/glm-5.3-flash` ficou cadastrado depois (07-out), mas o upstream NIM trava (timeout, 0 bytes) — problema da NVIDIA, não do 9router; base `nvidia/z-ai/glm-5.3` responde ~1-2s e virou o model.default. `providers.ollama-launch` no config.yaml aponta pra 11434 sem ollama no host (entrada órfã). **Rodar `9router` no terminal MATA a instância do service** (cli.js faz SIGKILL via pidfile 'already running') — para reiniciar use `systemctl --user restart 9router`.

- **Binário**: `~/.local/lib/node_modules/9router/cli.js` com node do nvm v24.16.0 (ExecStart do service; NÃO é bin/9router.js)
- **Versão**: 0.5.95 (2-out-2026, de 0.5.86). Verificar via `curl -s http://127.0.0.1:20128/api/version` → {"currentVersion","latestVersion","hasUpdate"} — sem auth, resposta imediata
- **Service tem `--skip-update`**: nunca se atualiza sozinho; atualização é sempre manual
- **Duplicata deletada (2-out-2026)**: cópia sudo em /usr/local/lib/node_modules/9router + symlink /usr/local/bin/9router. Causa: `npm install -g` com sudo cria segunda cópia que o service ignora — nunca instalar com sudo
- **Instalação correta**: `npm install -g 9router --prefix ~/.local` (sem nvm). O nvm vive em `~/.local/share/nvm` (movido de ~/.config/nvm em 02-out-2026; ~/.config/nvm NÃO existe mais — caminho morto).
- **Service**: `systemctl --user status 9router` — ativo, porta 20128.
- **Dashboard**: `http://localhost:20128` (login com senha do cofre `NINEROUTER_DASHBOARD_PASSWORD`).
- **Provider NVIDIA NIM**: conectado (1 Connected), catálogo nativo expõe até GLM-5.2; 5.3, kimi-k3 e deepseek-v4.1-flash são custom models.
- **Modelos custom NVIDIA**: cadastrar via API `POST /api/models/custom` (login por cookie; ver references/procedimentos.md) ou dashboard → Providers → NVIDIA → Add Model. O cadastro NÃO tem campo Thinking (só Vision/Reasoning); esforço vai por request em `reasoning_effort`.
- **07-out-2026**: Hermes agora em `nvidia/z-ai/glm-5.3` + `reasoning_effort: low`. `glm-5.3-flash` e `deepseek-v4.1-flash` estão cadastrados mas a NVIDIA não responde (fora do ar do lado deles, provado direto). `kimi-k3` funciona só com low/high/max.
- **Catálogo público do 9router**: `curl http://127.0.0.1:20128/v1/models` lista `nvidia/z-ai/glm-5.3` após adição.
- **Chat via 9router testado**: `curl .../v1/chat/completions -H "Authorization: Bearer $NINEROUTER_KEY" -d '{"model":"nvidia/z-ai/glm-5.3","reasoning_effort":"max",...}'` → responde com reasoning_tokens.

## Como o Hermes roteia para o 9router

O Hermes conecta ao 9router como uma API compatível com OpenAI:
- `provider: custom`
- `base_url: http://127.0.0.1:20128/v1`
- `model.default: nvidia/z-ai/glm-5.3` (o 9router recebe o ID do modelo e despacha para o provedor correspondente)
- `agent.reasoning_effort: low` (kimi-k3 recusa medium; aceita low/high/max)

**Atenção**: Nunca injetar `ANTHROPIC_BASE_URL` para o 9router — o Hermes se comunica via endpoint OpenAI (`/v1/chat/completions`) com token de autorização.

1. `npm install -g 9router --prefix ~/.local` (node do nvm no PATH; aviso allowScripts/postinstall é inofensivo)
2. `systemctl --user restart 9router`
3. Verificar: `curl -s http://127.0.0.1:20128/api/version` → currentVersion = latestVersion, hasUpdate false
4. Se catálogo NIM não atualizou: Provider NVIDIA → "Refresh" ou aguardar cache.

## Fluxo: adicionar modelo NIM custom (ex.: GLM-5.3)

1. Abrir dashboard, logar.
2. Providers → NVIDIA (Connected).
3. Botão "Add Model" (ícone `smart_toy` + texto).
4. Preencher:
   - **Model ID**: `z-ai/glm-5.3` (exato como a NIM expõe)
   - **Capabilities**: Vision / Reasoning (não existe campo Thinking na v0.5.95)
5. Botão "Add Model" no **rodapé do modal** (Cancel / Add Model).
6. Verificar em "Available Models": aparece `nvidia/z-ai/glm-5.3`.
7. Testar via API: `curl .../v1/chat/completions -d '{"model":"nvidia/z-ai/glm-5.3","reasoning_effort":"max"...}'`.

## Como o Hermes resolve o modelo

| Configuração | Efeito |
|---|---|
| `provider: custom` + `base_url: http://127.0.0.1:20128/v1` | Hermes envia requisições OpenAI-compatible ao 9router |
| `model.default: nvidia/z-ai/glm-5.3` no `config.yaml` | 9router recebe o model ID exato e despacha ao provedor ativo |
| Alias no Hermes (`model.aliases.glm53: nvidia/z-ai/glm-5.3`) | Permite `/model glm53` ou `model.default: glm53` |
| `agent.reasoning_effort: low` | Esforço de raciocínio enviado em cada request |

**Atenção com `fallback_providers`**:
- **Variável ≠ identidade da chave.** Nunca confundir o NOME da variável com a IDENTIDADE da chave: uma variável chamada `OPENAI_API_KEY` pode conter o valor do `NINEROUTER_KEY_DEFAULT`. O 9router aceita o valor (HTTP 200) e a API real do provedor recusa (HTTP 401/403). Sempre provar o valor — comparar o conteúdo de duas variáveis via `/proc/PID/environ`, e testar HTTP 200 no 9router vs HTTP 401/403 na API real — antes de remover ou duplicar uma credencial. Diagnosticar por nome de variável soa um alerta falso e faz você apagar/repetir chave que funciona. Ver `references/env-cred-trimming-checklist.md`.
- **Verificar antes de apagar.** Antes de remover qualquer chave, grep `config.yaml`, skills e código-fonte — incluindo aliases como `${OPENAI_API_KEY}` apontando pro 9router. Uma chave pode ser usada em 19 lugares pelo apelido enquanto a variável sozinha aparece em 0. Remover sem truth-check no endpoint em tempo real quebra o provisionamento de modelos sem mensagem apontando para a variável. Ver `references/env-cred-trimming-checklist.md`.
- `fallback_providers`: Se `model.default` falhar ou a lista de reserva contiver modelos genéricos (ex.: modelos gratuitos do OpenRouter), o Hermes cai silenciosamente neles (Kimi, DeepSeek, etc.). A lista de fallback deve ser explícita e controlada.

### Cadeia de Fallback Padrão Validada (4 níveis)
1. **Principal**: 9router (NVIDIA) `nvidia/z-ai/glm-5.3` (reasoning `low`)
2. **Reserva 1**: 9router `cc/claude-opus-5-5` (custom provider via 9router)
3. **Reserva 2**: OpenRouter `anthropic/claude-sonnet-4.5`
4. **Reserva 3**: Poolside direto `poolside/laguna-s-2.1` (`https://inference.poolside.ai/v1`, sem gateway)

Configuração via CLI mantendo referências do cofre:
```bash
hermes config set fallback_providers '[{"base_url":"http://127.0.0.1:20128/v1","model":"cc/claude-opus-5-5","provider":"custom","api_key":"${NINEROUTER_KEY}"},{"base_url":"https://openrouter.ai/api/v1","model":"anthropic/claude-sonnet-4.5","provider":"openrouter","api_key":"${OPENROUTER_API_KEY}"},{"base_url":"https://inference.poolside.ai/v1","model":"poolside/laguna-s-2.1","provider":"custom","api_key":"${POOLSIDE_API_KEY}"}]'
```

## Armadilhas

- **Nunca usar `${OPENAI_API_KEY}` para a chave do 9router.** `OPENAI_API_KEY` é nome reservado do Hermes: TTS/STT OpenAI e o cliente auxiliar a mandam para api.openai.com, onde a chave do 9router dá 401 silencioso. Endpoint custom = nome próprio (`${NINEROUTER_KEY_DEFAULT}` ou `key_env:`), padrão da doc (fallback-providers.md, providers.md). Corrigido 18-out-2026: 19 refs trocadas, OPENAI_API_KEY removida do .env.
- **`~/.local/secrets/` é montado read-only no container.** Escrever o .env pelo host via `tijolao-ssh-bridge` (`cat > .env.new` + `mv`, chmod 600). `~/.hermes/.env` é symlink para ele.
- **Mudar o .env exige recriar o container, não reiniciar serviço.** O compose (`~/.config/hermes-stack/docker-compose.tijolao.yml`) injeta o .env via `env_file` na CRIAÇÃO do container; `s6-svc -r` herda o env antigo. Recriar no host: `tijolao up` (mata a sessão que roda dentro do hermes-agent — disparar com `setsid nohup` e log em `~/.hermes/state/`).
- **Pool de credenciais guarda a chave antiga.** `auth.json` → `credential_pool.custom:9router` (source `model_config`) foi semeado com o texto literal `${OPENAI_API_KEY}` quando o .env estava vazio, e continuou sendo usado depois da troca → 401 "Invalid API key" e fallback para o Claude. Diagnóstico: comparar `secret_fingerprint` com sha256 do literal. Correção: `hermes auth remove custom:9router <id>` e depois `hermes_cli.auth.unsuppress_credential_source('custom:9router','model_config')` (o remove suprime a fonte; sem desfazer, não ressemeia).
- **GLM-5.3 via 9router: 400 `duplicate field reasoning_content` a partir da 2ª mensagem.** Causa medida: 9router em 127.0.0.1 = "endpoint local" → Hermes reenvia o raciocínio em `reasoning` E `reasoning_content` (`_LOCAL_CARRIERS`, agent/message_sanitization.py:658); o 9router converte `reasoning`→`reasoning_content` e o upstream recusa duplicado. A autocorreção do Hermes não dispara (frase "duplicate field" fora de `_UNKNOWN_FIELD_PHRASES`, :911). Docs (Context7) não têm opção de config para escolher o campo. NÃO é tamanho de conversa; `/new` não resolve.
- **Trocar refs no config.yaml: `hermes config set <caminho> '${VAR}'` (aspas simples)**, um caminho por chamada; o valor `${VAR}` é gravado literal. Conferir com diff contra o backup.

- **npm via nvm ≠ service systemd**. O service lê de `~/.local`. Atualizar pelo nvm deixa o service na versão velha. Sempre `--prefix ~/.local`.
- **`cli.js --version` é lento na 1ª execução** (passou de 100 s inicializando; parece travado). Para versão, use `curl http://127.0.0.1:20128/api/version`.
- **Dashboard SPA**: a versão NÃO está no HTML da home; vem de `/api/version`.
- **Catálogo NIM ≠ modelos disponíveis**. O 9router faz cache do catálogo NIM. GLM-5.3 pode funcionar na NIM mas não aparecer no 9router. Solução: Add Model manual.
- **Modal Add Model tem dois botões "Add Model"**: o do header abre, o do rodapé confirma. Clicar o do header de novo fecha o modal sem salvar.
- **Esforço = `reasoning_effort` por request** (não há campo no cadastro). Opções gerais: low/medium/high/max; kimi-k3 só aceita low/high/max.
- **Funnel Tailscale expõe 9router publicamente**: `https://tijolao.tail9e88c5.ts.net/v1/...` — responde 401 sem key (correto).
- **Modelos gratuitos no `fallback_providers` causam trocas fantasmas**. Nunca colocar modelos free sem controle na lista de reserva do `config.yaml`.
- **Nunca edite `config.yaml` na mão**. Use `hermes config set`. As variáveis como `${NINEROUTER_KEY}` são preservadas se passadas no JSON.

## Troca de modelo em setup 9router (regra operacional)

- **Para trocar o modelo principal**:
  1. Certifique-se de que o modelo está cadastrado e ativo no 9router (`curl http://127.0.0.1:20128/v1/models`).
  2. Ajuste o Hermes via CLI: `hermes config set model.default nvidia/z-ai/glm-5.3`.
  3. Ajustar esforço: `hermes config set agent.reasoning_effort low` (ou high/max).
  4. Teste em execução real: `hermes chat -q "Diga apenas OK"`.

## Verificação rápida de saúde

```bash
# No host (via SSH ponte)
curl -s http://127.0.0.1:20128/api/version   # currentVersion/latestVersion/hasUpdate (sem auth)
systemctl --user status 9router      # active (running)
curl -s http://127.0.0.1:20128/v1/models | jq -r '.data[].id' | grep glm-5.3
curl -s https://tijolao.tail9e88c5.ts.net/v1/models -o /dev/null -w '%{http_code}'
```

## Referências relacionadas

- `hermes-agent` skill → `references/providers-and-models.md` (aliases, custom provider)
- `hermes-agent` skill → `references/configuration.md` (config sections, toolsets)
- `tijolao-ssh-bridge` skill (ponte SSH para rodar comandos acima)