# Checklist: trim unused credentials without breaking the stack

Use ON the SSH bridge (`tijolao-ssh-bridge`) when reducing a `.env`/`NINEROUTER_*` block to only the keys actually consumed by Hermes + 9router. Each step is a gate; stopping early risks a live key disappearing from the process env.

## 1. Enumerate names
List every "KEY=..." line in the candidate file. Do NOT read values — work from names + fingerprints only.

## 2. Probe usage (three sources, parallel)
- config.yaml: grep -n "${NAME}" /home/dr/.hermes/config.yaml (include aliases like ${OPENAI_API_KEY}).
- skills: grep -rlw NAME /home/dr/.hermes/skills.
- Hermes source: grep -rlw NAME /opt/hermes/tools /opt/hermes/hermes_cli /opt/hermes/gateway.

### 3. Verify value identity (never by name)
To compare two variables whose names differ but whose values may be identical, inspect `/proc/<PID>/environ` directly (split on null). If both resolve to the SAME value, they are mirrors — remove one copy, NEVER both. This catches the `OPENAI_API_KEY` trap: a variable named `OPENAI_API_KEY` that holds the 9router value passes grep-by-name checks but fails against the real OpenAI API.

## 4. Endpoint truth-check (HTTP only, never show value)
```
curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:20128/v1/models -H "Authorization: Bearer $VAR"
```
- 200 on 9router = value belongs to 9router.
- 401/403 on the provider's real API = value does NOT match the variable name.

## 5. Atomic edit
Removal via write_file, NEVER echo >>. Validate YAML/JSON. .env is 0600 at ~/.local/secrets/.env.

## 6. Restart + live model call (final gate)
NOT dashboard /health. Make a real call:

hermes chat -q "Diga apenas OK"  # 2-5s; GLM response = key survived

If fails, restore .env from quarantine immediately.

## Pitfalls
- Removing FIRECRAWL_API_KEY breaks web_extract with misleading error (scrape failed), NOT unauthorized.
- Removing CONTEXT7_API_KEY breaks context7 skill on first use, not on boot.
- Removing NINEROUTER_KEY_DEFAULT while config.yaml references ${OPENAI_API_KEY} alias = silent GLM fallback.
- config.yaml always overrides .env for referenced vars — removal order: values first, names second.
- `hermes config set <path> '${VAR}'` writes the literal `${VAR}` token (NOT the expanded value) only if the value is single-quoted; double quotes or no quotes cause shell/variable interpolation at write time. Trap for credential trimming: always use single quotes for variable references so the token, not the key, lands in config.yaml.
