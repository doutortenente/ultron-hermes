# Reorganização do Tijolão — execução 25-set-2026

> Fonte da verdade: `vaults/celebro/MAPA-DO-TIJOLAO.md` (tabela v3). Ordem nova do dono: **frota = GLM 5.3, raciocínio no máximo**.

## Decisões (donor: "execute")
1. Produtos mantidos → `~/src` (convenção FHS). `projetos/` vira só IaC + scratch do agente.
2. `tijolao-ai` **fica** onde está (alternativa "ou fica" do mapa).
3. n8n: **remover** (zumbi; Docker + restart=unless-stopped cobre o boot).
4. Frota: workers + orquestrador → `nvidia/z-ai/glm-5.3` + esforço máximo. **Evidencia fica em `cx/gpt-5.6-terra`** (GLM 5.3 não tem visão; perfil exige visão para auditoria clínica).
5. Cofre: mover preservando byte a byte (sha256) + symlink no caminho antigo.

## Sequência
- [ ] 0. Backup tar dos configs pequenos → `~/backups/`
- [ ] 1. Cofre: `projetos/.env` → `~/.local/secrets/tijolao.env` (0600, sha256 igual, symlink antigo, compose `env_file:` aponta novo caminho)
- [ ] 2. `~/src/`: mover `hermes-workspace` (fork), `scripts`, `sasi-apresentacao-web`
- [ ] 3. Patch de caminhos no stack compose + tijolao.sh/install.sh/wrappers (context do build → `~/src/hermes-workspace`)
- [ ] 4. Documentos: `Plantões/` → `vaults/celebro/Plantões`; docs GitHub/Tijolão → vault; remover zip EXTRAÇÃO (duplicata)
- [ ] 5. Zumbis: `~/.local/bin/gh`, claude `2.1.282`, `/usr/local/bin/9router` + units papel (se sudo), `n8n` do repo
- [ ] 6. Swarm: `swarm.yaml` + 5 perfis → glm-5.3 + esforço máx; validar com chamada real (wrapper `chefe`)
- [ ] 7. Esforço máx no perfil default (eu) via `hermes config set`
- [ ] 8. Re-home do `hermes-agent` p/ o stack compose (script destacado + sleep 90 + cron de verificação) — único passo que me reinicia
- [ ] 9. Atualizar MAPA-DO-TIJOLAO.md (linhas executadas) + commit tijolao-ai (sem push)
- [ ] 10. Airtable "Ações da sessão" (se token vivo)

## Invariantes
- Cofre: sha256 antes/depois idêntico; nada de chave impressa.
- Nada de push (greenlight só com ordem).
- Se sudo falhar: item vira pendência, não bloqueia o resto.
