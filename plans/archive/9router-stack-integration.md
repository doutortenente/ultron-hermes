# 9Router Stack Integration Plan

> **For agentic workers:** Execute this plan task-by-task and verify every state change.

**Goal:** Integrate the existing local 9Router into Hermes as an optional model provider and as the canonical source of all upstream 9Router capability skills, without changing the current default model.

**Architecture:** Hermes keeps `openai-codex/gpt-5.6-sol` as primary. A named custom provider `nine-router` points to the local OpenAI-compatible API and reads its key from the Hermes secret file. The cloned repository supplies all 9Router skills through `skills.external_dirs`; the previously copied umbrella skill is removed to prevent duplicate sources.

**Tech Stack:** Hermes Agent config CLI, YAML configuration, `.env` secret scope, 9Router REST API, SQLite local state, Agent Skills.

---

### Task 1: Secure provider credentials

**Files:**
- Modify: `/home/dr/.hermes/.env`

- [ ] Read one active 9Router API key from `/home/dr/.9router/db/data.sqlite` without printing it.
- [ ] Store it as `NINEROUTER_KEY` in `/home/dr/.hermes/.env`, preserving all unrelated entries and mode `0600`.
- [ ] Verify only key presence and non-empty length; never print the value.

### Task 2: Register the optional Hermes provider

**Files:**
- Modify through `hermes config set`: `/home/dr/.hermes/config.yaml`

- [ ] Create `providers.nine-router.name = 9Router`.
- [ ] Create `providers.nine-router.api = http://127.0.0.1:20128/v1`.
- [ ] Create `providers.nine-router.key_env = NINEROUTER_KEY`.
- [ ] Create `providers.nine-router.transport = chat_completions`.
- [ ] Create `providers.nine-router.default_model = cx/gpt-5.6-sol`.
- [ ] Enable live model discovery.
- [ ] Confirm `model.provider` and `model.default` remain unchanged.

### Task 3: Make the repository the skill source

**Files:**
- Modify through `hermes config set`: `/home/dr/.hermes/config.yaml`
- Remove: `/home/dr/.hermes/skills/integrations/nine-router/`

- [ ] Add `/home/dr/projetos/9router/skills` to `skills.external_dirs` while preserving `/home/dr/.claude/skills`.
- [ ] Remove the copied `integrations/nine-router` skill installed from the raw URL.
- [ ] Verify nine repository skills are discoverable and no local copied 9Router skill remains.

### Task 4: End-to-end verification

- [ ] Verify 9Router health returns `{"ok":true}`.
- [ ] Verify the Hermes custom-provider inventory resolves `nine-router` with discovered models.
- [ ] Call `cx/gpt-5.6-sol` through 9Router using the secret and require exact response `9ROUTER_OK`.
- [ ] Verify one non-chat capability model catalog endpoint responds.
- [ ] Verify no 9Router key appears in `config.yaml` or command output.
- [ ] Verify the current Hermes default remains `openai-codex/gpt-5.6-sol`.
- [ ] Verify the 9Router Git checkout remains clean.
