---
name: harness-insights
description: Mine Hermes sessions for failures and propose fixes.
version: 1.0.0
license: MIT
author: Nicholas Nagaita, Hermes Agent
platforms: [linux, macos]
metadata:
  hermes:
    tags: [self-improvement, observability, harness]
    related_skills: [hermes-runtime-maintenance, hermes-agent]
---

# Harness Insights Skill

Port of the HarnessKit 0.4.3 Observe -> Improve loop (vault: 002-DEV-IA/rascunhos-projetos/HarnessKit-0.4.3-v1) to Hermes. Hermes already logs everything in state.db and skills/.usage.json, so no shell hooks are needed: one read-only script mines the data, the agent judges it. Does NOT auto-apply anything.

## When to Use
- User asks to optimize/audit the agent itself, or "what keeps failing".
- Weekly, or after a burst of failed turns.

## Prerequisites
- python3 (stdlib only). Reads ~/.hermes/state.db with mode=ro (safe while gateway runs).

### How to Run
`terminal`: `python3 ~/.hermes/skills/software-development/harness-insights/scripts/mine.py --days 14`
Runs in <2s, zero LLM tokens, prints JSON. Each run saves a snapshot to `~/.hermes/state/harness-insights/snapshots/` and diffs against the last snapshot of the SAME `--days` window. `--no-save` for a dry look. `--home PATH` overrides the Hermes root (needed when state.db lives in a non-default location, e.g. `/home/dr/.hermes`).

## Procedure
1. Run the script. Read `alerts` first (fixed thresholds in `THRESH` at the top of mine.py: tool error >10%, tokens in:out >20:1, same-tool 3x loop >50, subagent sessions >50%, error cluster >=3), then `delta_vs_previous`, `top_errors`, `proposals_rejected_do_not_repropose`, `proposals_open_to_verify`.
2. For each error cluster >=3 occurrences, classify root cause: agent misuse (fix = pitfall line in the owning skill), environment (fix = config/infra), provider (fix = fallback/model).
1. For each clustered error, find the originating session via `session_search` or `/memory` using the cluster's first session id; inspect the exact failing tool-call's arguments before proposing the fix.
3. Max 5 proposals, ordered by occurrences. Each = target file, exact change, evidence count.
4. Agent-misuse fixes go into skills via `skill_manage` patch (one rule per lesson). Config changes: show plan, user confirms, apply via `terminal` + `hermes config set` (the `patch` tool refuses config.yaml).
- When patching a skill's SKILL.md, call `skill_view` first in the same review session (read-before-write guard).
5. Record every proposal in `~/.hermes/state/harness-insights/proposals.json` as `{"id","date","target","change","metric","baseline","status"}` with status accepted/rejected/reverted. Never re-propose a rejected one.
6. Next run, `delta_vs_previous` shows whether the `metric` of each accepted proposal dropped; no drop -> revert and mark `reverted`.

## HarnessKit principles kept (from the HarnessKit bible)
- Zero-token observation; LLM only for judgment.
- One session = one feature; fresh context beats bloated context.
- Lazy loading: index, not the full manual (Hermes skills index already does this).
- MCP diet: keep few servers enabled.
- Never re-propose a fix the user rejected.

## Dropped from HarnessKit (Hermes already does it)
- guardrails.sh -> Hermes approvals + tirith dangerous-command block.
- session-start/end hooks -> state.db + session_search.
- insights-history -> curator + .usage.json.
- Claude Code plugin manifest/hooks.json -> not portable; Hermes shell hooks use `hooks:` in config.yaml (stdin JSON, exit 2 blocks pre_tool_call).

## Pitfalls
|- Telegram `IPv4 ... failed` / `Dual-stack ... failed` warnings: Hermes already tries IPv4 literals first (TelegramFallbackTransport). They mean intermittent network timeouts, not missing IPv4 config; only act if `Connected to Telegram` stops appearing in gateway.log.
|- Python tracebacks aggregate by exception type only for error messages under 200 chars; longer ones still read `"error": "Traceback..."`. If `top_errors` fills with `execute_code: Traceback...` blobs, raise the regex cap in `norm()`.
|- The `tool_call_id` column on the `messages` table joins a terminal failure back to the command that caused it; some older sessions store it as NULL, in which case the script cannot classify which program failed — this is a data-quality gap, not a script bug.
- `skills.disabled` set via `hermes config set` prints "not a recognized config key" but IS read (prompt-size skills index drops). Verify with `hermes prompt-size`, not the warning.
- Terminal errors are labelled `terminal[<program>] exit=N: <error line>`; Python tracebacks as `Traceback -> <ExceptionType>`. If labels regress to `terminal: N`, the content format changed: status fields are read from the last 400 chars.
- Deltas between different `--days` windows are meaningless; the script only compares same-window snapshots.
- `terminal` exit_code!=0 with exit_code_meaning (grep no-match) is not an error; the script skips it.
- `execute_code > execute_code > execute_code` long runs mean looping in Python instead of finishing; batch work in one call.
- sessions with source=subagent inflate counts; filter by source when judging the user experience.
- Error clusters in `top_errors` show the FIRST session that produced that pattern. Inspect that session (via `/memory` or `session_search`) BEFORE writing the fix: the cluster label alone omits the arguments to the failing tool-call. The full command lives attached to the `tool_call_id` of that session's message, not in the cluster text.

## Verification
Script prints valid JSON with `sessions` > 0. After applying a fix, the targeted error count drops in the next run.
