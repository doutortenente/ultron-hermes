#!/usr/bin/env python3
"""Zero-token mining of Hermes state.db -> JSON report (HarnessKit 'observe' port).

Usage: mine.py [--days N] [--home ~/.hermes] [--no-save]
Read-only on state.db (mode=ro). No LLM calls.
Each run saves a dated snapshot to <home>/state/harness-insights/snapshots/ and
reports the delta of every metric vs the previous snapshot, plus threshold alerts.
Proposal history (accepted/rejected/reverted) lives in proposals.json next to it.
"""
import argparse, collections, json, os, re, sqlite3, time
from pathlib import Path

# Fixed thresholds (HarnessKit-style quantified rules). Breach -> alert.
THRESH = {
    "tool_error_pct": 10,      # per tool, with >= MIN_CALLS calls
    "min_calls": 10,
    "tokens_in_out_ratio": 20,
    "loop_3step": 50,          # same tool 3x in a row, count
    "subagent_session_pct": 50,
    "error_cluster": 3,        # same normalized error >= N -> must get root cause
}

ap = argparse.ArgumentParser()
ap.add_argument("--days", type=int, default=14)
ap.add_argument("--home", default=os.environ.get("HERMES_HOME", str(Path.home() / ".hermes")))
ap.add_argument("--no-save", action="store_true", help="do not write a snapshot")
a = ap.parse_args()
home = Path(a.home).expanduser()
outdir = home / "state" / "harness-insights"
snapdir = outdir / "snapshots"
since = time.time() - a.days * 86400

db = sqlite3.connect(f"file:{home/'state.db'}?mode=ro", uri=True)
sess = db.execute(
    "select id, source, model, message_count, tool_call_count, input_tokens, output_tokens, end_reason "
    "from sessions where started_at >= ?", (since,)).fetchall()
ids = [s[0] for s in sess]
q = ",".join("?" * len(ids)) or "''"


def norm(t):
    t = re.sub(r"/[\w./-]+", "<path>", t)
    t = re.sub(r"\b[0-9a-f]{6,}\b", "<id>", t)
    return re.sub(r"\d+", "N", t)[:110]


# Map tool_call_id -> arguments, so terminal failures can be grouped by command.
call_args = {}
for (tc,) in db.execute(
        f"select tool_calls from messages where role='assistant' and tool_calls is not null "
        f"and session_id in ({q})", ids):
    try:
        for c in json.loads(tc):
            fn = c.get("function") or {}
            call_args[c.get("id")] = fn.get("arguments") or ""
    except (ValueError, TypeError):
        pass


def term_class(c, cid):
    """terminal failure -> '<first program> exit=N: <last stderr-ish line>'."""
    try:
        d = json.loads(c)
    except ValueError:
        d = {}
    code = d.get("exit_code")
    try:
        cmd = json.loads(call_args.get(cid, "") or "{}").get("command", "")
    except ValueError:
        cmd = ""
    # first real program, skipping cd/env/timeout/sudo wrappers
    prog = "?"
    for part in re.split(r"&&|;|\|\||\|", cmd):
        toks = part.strip().split()
        while toks and (toks[0] in ("cd", "timeout", "sudo", "env", "nohup") or "=" in toks[0]
                        or toks[0].startswith("-") or re.fullmatch(r"\d+[smh]?", toks[0])):
            if toks[0] == "cd":
                toks = []
                break
            toks = toks[1:]
        if toks:
            prog = os.path.basename(toks[0])
            break
    out = (d.get("output") or "").strip().splitlines()
    tail = next((l for l in reversed(out) if re.search(r"error|denied|not found|no such|fail|refused|timed? ?out", l, re.I)),
                out[-1] if out else "")
    return f"terminal[{prog}] exit={code}: {norm(tail)[:80]}"


errors = collections.Counter()
per_tool = collections.Counter()
err_tool = collections.Counter()
seqs = collections.Counter()
skills = collections.Counter()
last = {}
for sid, tool, content, cid in db.execute(
        f"select session_id, tool_name, content, tool_call_id from messages "
        f"where role='tool' and session_id in ({q}) order by id", ids):
    tool = tool or "?"
    per_tool[tool] += 1
    c = content or ""
    head = c[-400:] if tool == "terminal" else c  # terminal status fields are at the end
    is_err = False
    if '"exit_code_meaning"' not in c:
        m = re.search(r'"error":\s*"([^"]{5,200})', c)
        if m:
            msg = m.group(1)
            if msg.startswith("Traceback"):  # group Python failures by exception type
                full = re.search(r'"error":\s*"((?:[^"\\]|\\.)*)"', c)
                lines = [l for l in (full.group(1) if full else msg).split("\\n") if l.strip()]
                exc = next((l for l in reversed(lines) if re.match(r"\s*[\w.]+(Error|Exception|Exit|Interrupt)\b", l)),
                           lines[-1] if lines else msg)
                msg = "Traceback -> " + exc.strip()
            is_err, label = True, f"{tool}: {norm(msg)}"
        elif re.search(r'"exit_code":\s*([1-9]\d*)', head):
            is_err = True
            label = term_class(c, cid) if tool == "terminal" else f"{tool}: exit!=0"
    if is_err:
        err_tool[tool] += 1
        errors[label] += 1
    if tool == "skill_view":
        n = re.search(r'"name":\s*"([^"]+)"', c)
        if n:
            skills[n.group(1)] += 1
    w = last.setdefault(sid, [])
    w.append(tool)
    if len(w) >= 3:
        seqs[" > ".join(w[-3:])] += 1

usage = {}
up = home / "skills" / ".usage.json"
if up.exists():
    usage = json.loads(up.read_text())
never = sorted(k for k, v in usage.items() if not v.get("use_count") and not v.get("view_count"))

tin = sum(s[5] or 0 for s in sess)
tout = sum(s[6] or 0 for s in sess)
src = collections.Counter(s[1] for s in sess)
metrics = {  # flat numeric counters: these are what gets diffed between runs
    "sessions": len(sess),
    "subagent_sessions": src.get("subagent", 0),
    "tokens_in": tin,
    "tokens_out": tout,
    "tokens_in_out_ratio": round(tin / tout, 1) if tout else None,
    "tool_calls": sum(per_tool.values()),
    "tool_errors": sum(err_tool.values()),
    "skills_never_used": len(never),
}
for t, n in per_tool.items():
    if n >= THRESH["min_calls"]:
        metrics[f"err_pct.{t}"] = round(100 * err_tool[t] / n, 1)
for s, n in seqs.items():
    p = s.split(" > ")
    if len(set(p)) == 1:
        metrics[f"loop.{p[0]}"] = n

alerts = []
for t, n in per_tool.items():
    if n >= THRESH["min_calls"] and 100 * err_tool[t] / n > THRESH["tool_error_pct"]:
        alerts.append(f"{t}: {err_tool[t]}/{n} errors ({100*err_tool[t]//n}%) > {THRESH['tool_error_pct']}%")
r = metrics["tokens_in_out_ratio"]
if r and r > THRESH["tokens_in_out_ratio"]:
    alerts.append(f"tokens in:out {r}:1 > {THRESH['tokens_in_out_ratio']}:1 (bloated context)")
for k, v in metrics.items():
    if k.startswith("loop.") and v > THRESH["loop_3step"]:
        alerts.append(f"{k} {v}x > {THRESH['loop_3step']} (looping instead of batching)")
if sess and 100 * metrics["subagent_sessions"] / len(sess) > THRESH["subagent_session_pct"]:
    alerts.append(f"subagent sessions {metrics['subagent_sessions']}/{len(sess)} > {THRESH['subagent_session_pct']}%")
for e, n in errors.most_common():
    if n >= THRESH["error_cluster"]:
        alerts.append(f"error cluster x{n}: {e}")

# Delta vs previous snapshot
prev, prev_name = None, None
if snapdir.exists():
    snaps = sorted(snapdir.glob(f"*-d{a.days}.json"))  # same window only
    if snaps:
        prev_name = snaps[-1].name
        try:
            prev = json.loads(snaps[-1].read_text()).get("metrics", {})
        except ValueError:
            prev = None
delta = None
if prev is not None:
    delta = {}
    for k in sorted(set(metrics) | set(prev)):
        old, new = prev.get(k), metrics.get(k)
        if old != new:
            delta[k] = {"before": old, "now": new}

proposals = []
pp = outdir / "proposals.json"
if pp.exists():
    try:
        proposals = json.loads(pp.read_text())
    except ValueError:
        pass

report = {
    "window_days": a.days,
    "previous_snapshot": prev_name,
    "alerts": alerts,
    "delta_vs_previous": delta,
    "metrics": metrics,
    "by_source": src.most_common(),
    "by_model": collections.Counter(s[2] for s in sess).most_common(8),
    "end_reasons": collections.Counter(s[7] for s in sess).most_common(6),
    "top_errors": errors.most_common(15),
    "repeated_3step_sequences": [s for s in seqs.most_common(10) if s[1] >= 5],
    "skills_loaded": skills.most_common(15),
    "skills_never_used": never,
    "proposals_rejected_do_not_repropose": [p for p in proposals if p.get("status") == "rejected"],
    "proposals_open_to_verify": [p for p in proposals if p.get("status") == "accepted"],
}

if not a.no_save:
    snapdir.mkdir(parents=True, exist_ok=True)
    name = time.strftime("%Y-%m-%dT%H%M%S") + f"-d{a.days}.json"
    (snapdir / name).write_text(json.dumps({"metrics": metrics, "alerts": alerts,
                                            "top_errors": report["top_errors"]}, ensure_ascii=False, indent=1))
    report["saved_snapshot"] = str(snapdir / name)
    if not pp.exists():
        pp.write_text("[]\n")

print(json.dumps(report, ensure_ascii=False, indent=1))
