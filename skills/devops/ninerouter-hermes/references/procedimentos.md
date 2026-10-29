# Procedimentos 9router + Hermes — Detalhados

Este arquivo contém os passos executáveis e decisões para operações comuns. O SKILL.md tem a visão geral; aqui está o "como fazer" para copiar/colar.

---

## 1. Atualizar 9router (método correto, validado set/2026)

```bash
# No host (via ponte SSH do Hermes)
ssh -i ~/.ssh/id_ed25519 -o BatchMode=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null dr@localhost \
  'npm install -g 9router --prefix ~/.local && systemctl --user restart 9router && 9router --version'
```

**Verificação**: saída deve mostrar versão ≥ 0.5.86 e service `active (running)`.

**Por que `--prefix ~/.local`**: o systemd service `--user` executa o binário de `~/.local/lib/node_modules/9router/bin/9router.js`. O nvm instala em `~/.config/nvm/versions/node/.../lib/node_modules/9router` — caminho diferente que o service ignora.

**Armadilha crítica**: npm via nvm instala em `~/.config/nvm/...` — o service systemd **não vê**. Sempre `--prefix ~/.local`.

---

## 2. Adicionar modelo NIM custom (GLM-5.3, Nemotron, etc.)

### Via dashboard (manual, visual)

1. Abrir `http://localhost:20128` no navegador (ou via browser_exec do Hermes).
2. Login: senha do cofre `NINEROUTER_DASHBOARD_PASSWORD`.
3. Providers → **NVIDIA** (deve mostrar "1 Connected").
4. Botão **"Add Model"** (ícone `smart_toy` + texto).
5. Modal abre:
   - **Model ID**: `z-ai/glm-5.3` (ou `nvidia/nemotron-3-ultra-550b-a55b`, etc.)
   - **Capabilities**: toggles Vision / Reasoning (NÃO existe campo Thinking na v0.5.95; o esforço vai por request em `reasoning_effort`)
6. Botão **"Add Model" no rodapé do modal** (não o do header — são dois botões com mesmo texto).
7. Verificar: em "Available Models" aparece `nvidia/z-ai/glm-5.3`.

### Via API (CONFIRMADO v0.5.95, sem reiniciar — mesma API do dashboard)

Rota protegida: logar primeiro (cookie JWT 24h), depois POST. Rodar no host via SSH. Id SEM prefixo `nvidia/`; /v1/models expõe como `nvidia/<id>`. POST repetido = upsert (added:false).

```bash
set -a; . ~/.local/secrets/.env; set +a; J=$(mktemp)
curl -s -c $J -o /dev/null -X POST http://127.0.0.1:20128/api/auth/login -H 'Content-Type: application/json' -d "{\"password\":\"$NINEROUTER_DASHBOARD_PASSWORD\"}"
curl -s -b $J -X POST http://127.0.0.1:20128/api/models/custom -H 'Content-Type: application/json' \
  -d '{"providerAlias":"nvidia","id":"z-ai/glm-5.3-flash","type":"llm","name":"z-ai/glm-5.3-flash","caps":{"vision":false,"reasoning":true}}'
rm -f $J
```

Listar: GET /api/models/custom (com cookie). Remover: DELETE /api/models/custom?providerAlias=nvidia&id=<id>&type=llm.

### Estado 07-out-2026 (modelos NVIDIA no 9router)

| Modelo | Chat funciona? |
|---|---|
| nvidia/z-ai/glm-5.3 | sim, ~1,3-2s, qualquer reasoning_effort |
| nvidia/moonshotai/kimi-k3 | sim, mas SÓ low/high/max (medium = erro 400) |
| nvidia/z-ai/glm-5.3-flash | NÃO: NVIDIA aceita o pedido e nunca responde (timeout; 5 chaves, stream/sem stream, direto e via 9router) |
| nvidia/deepseek-ai/deepseek-v4.1-flash | NÃO: mesmo sintoma do glm flash |

Modelos *flash* da NVIDIA estavam fora do ar, apesar de listados no catálogo deles. Antes de apostar em um, testar com curl direto em integrate.api.nvidia.com (timeout 60s). Hermes: model.default = nvidia/z-ai/glm-5.3, agent.reasoning_effort = low.

---

## 3. Testar modelo via 9router (chat completion)

```bash
KEY=$(grep '^NINEROUTER_KEY_DEFAULT=' /home/dr/projetos/.env | cut -d= -f2-)
curl -s http://127.0.0.1:20128/v1/chat/completions \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"nvidia/z-ai/glm-5.3","max_tokens":300,"reasoning_effort":"low","messages":[{"role":"user","content":"Teste"}]}' \
  | jq -r '.choices[0].message.content, .usage.completion_tokens_details.reasoning_tokens'
```

Espera-se: resposta + `reasoning_tokens` > 0.

---

## 4. Verificar saúde completa (script único)

```bash
ssh -i ~/.ssh/id_ed25519 -o BatchMode=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null dr@localhost <<'EOF'
set -e
echo "=== 9router version ===
9router --version
echo "=== Service status ===
systemctl --user is-active 9router
echo "=== Local catalog (glm-5.3) ===
curl -s http://127.0.0.1:20128/v1/models | jq -r '.data[].id' | grep glm-5.3 || echo 'NAO ENCONTRADO'
echo "=== Funnel public (HTTP code) ===
curl -s https://tijolao.tail9e88c5.ts.net/v1/models -o /dev/null -w '%{http_code}'
echo
echo "=== Hermes fallback count ===
grep -c 'fallback_providers' ~/.hermes/config.yaml
echo "=== Config model.default ===
grep -A2 '^model:' ~/.hermes/config.yaml | head -3
EOF
```

---

## 5. Criar alias amigável no Hermes (para `/model glm53`)

```bash
# No container Hermes (ou via hermes config set remoto)
hermes config set model.aliases.glm53 nvidia/z-ai/glm-5.3
# Verificar
hermes config get model.aliases.glm53
```

Agora `/model glm53` no CLI, Telegram, etc. resolve pro 9router.

---

## 6. Trocar modelo padrão persistente

1. Certificar que o modelo está ativo no 9router (`curl -s http://127.0.0.1:20128/v1/models | jq -r '.data[].id'`).
2. Configurar no Hermes via CLI: `hermes config set model.default nvidia/z-ai/glm-5.3`.
3. Configurar esforço de raciocínio se desejado: `hermes config set agent.reasoning_effort low` (o kimi-k3 recusa `medium`; aceita low/high/max).
4. (Opcional) Alias no Hermes: `hermes config set model.aliases.glm53 nvidia/z-ai/glm-5.3`.
5. Verificar com execução real: `hermes chat -q "Em uma frase: qual modelo você é?"`.

---

## 7. Debug: 9router não reinicia / porta 20128 não sobe

```bash
# Logs do service
journalctl --user -u 9router -n 50 --no-pager
# Processo na porta
ss -ltnp 'sport = :20128'
# Matar processo órfão e restart
pkill -f '9router.*bin/9router.js'; systemctl --user restart 9router
```

---

## 8. Debug: modelo adicionado mas não aparece no catálogo público

- Dashboard mostra em "Available Models" mas `curl /v1/models` não lista.
- Causa: cache do 9router. Solução: `systemctl --user restart 9router` ou aguardar (cache TTL ~5 min).
- Verificar: `curl -s http://127.0.0.1:20128/v1/models | jq '.data[] | select(.id | contains("glm-5.3"))'`.

---

## 9. Variáveis de ambiente críticas (host)

| Variável | Onde | Valor |
|---|---|---|
| `NINEROUTER_DASHBOARD_PASSWORD` | `/home/dr/projetos/.env` (host) | senha do dashboard |
| `NINEROUTER_KEY` / `NINEROUTER_KEY_DEFAULT` | `/home/dr/projetos/.env` (host) | key API para chamadas |
| `POOLSIDE_API_KEY` | `/home/dr/projetos/.env` (host) | API key Poolside direta |
| `OPENROUTER_API_KEY` | `/home/dr/projetos/.env` (host) | API key OpenRouter |

---

## 10. Limpeza de duplicatas descoberta set/2026

| Binário | Cópias | Mantida | Removida |
|---|---|---|---|
| `9router` | `~/.local/bin` + `/usr/local/bin` | `~/.local/bin` (service usa) | `/usr/local/bin` |

**Ação**: remover cópia root órfã após confirmar service ativo na cópia local.

---

## 11. Referência cruzada

- `tijolao-ssh-bridge`: ponte SSH para rodar comandos no host.
- `hermes-agent` → `references/providers-and-models.md`: aliases, custom provider config.
- `hermes-agent` → `references/configuration.md`: config sections, `hermes config set`.