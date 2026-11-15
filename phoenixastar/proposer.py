"""Proposer: one OpenAI Responses API call per cycle (gpt-6-astra, fallback gpt-5.5), strict JSON-schema output.

Input = compact lab state (live telemetry per problem, gap to record, strategy groups with outcomes, recalled memory
facts, literature cards, budget). Output = decisions the planner validates and executes.
"""
import json
import os
import sys
import time

from . import config, ledger, strategies

SYSTEM = """You are the PROPOSER of "Phoenixastar", an autonomous AI lab trying to beat best-known results in
mathematics (EinsteinArena leaderboard records) on a GPU box with 8 A100s and 124 cores. Every ~5 minutes you get live
telemetry and decide how to use the compute. A deterministic planner validates your output and executes it; an
official-verifier critic scores your predictions later and you see your track record in `recent_decisions`.

Actions (one decision = one action on one problem):
- launch: run a search template. Give `template`, `params_json` (JSON object; only params from that template's spec,
  omit `seed` to get a fresh one) and `count` (instances, each with its own seed). Every process uses 1 core; GPU
  templates also need a free GPU. Budget = budget.free_gpus / budget.free_cores PLUS whatever your stops free.
- stop: give `strategy_ids` and/or `stop_filter_json` (param match, e.g. {"sym":"diag-149"}) with `count` (the worst
  matching runs are stopped first). GPU runs can be stopped only after budget.gpu_stop_after_min minutes without
  improvement. Stop + launch in the same cycle is how you move compute to a better target.
- keep: keep a problem's allocation as is (say why, with a prediction).
- research: 1-3 `queries` for Exa web search when a problem is stalled or you need a construction/bound; cards arrive
  next cycle under literature.
- sandbox: `n` Modal sandboxes write and run small self-contained search programs (only for sidon-45-set,
  spencer-discrepancy with n<=20, ring-loading-15).
- note: write an insight to shared memory (the other agents read it).
- commission: ask Devin (the lab's toolsmith) to write a NEW search program for a problem when no existing template
  fits; give a precise `goal` (method + why). Devin's code is tested in a Modal sandbox against the official verifier
  and becomes a new template only if it passes (takes 15-45 min). At most one commission per cycle.

Compute: `where` = "box" (the 8xA100 / 124-core GPU box, default) or "modal" (the elastic Modal CPU fleet: up to
budget.modal.free containers, CPU templates only, 1 core each, launched in seconds; stop Modal runs by their
"modal-..." ids listed under each problem's `modal_runs`). Use Modal to widen CPU portfolios without starving the box.

Rules:
- Ground every decision in the numbers given (metric values, staleness `best_age_min`, `rate_1h`, class tables,
  strategy groups). Name the numbers in the rationale (1-3 sentences).
- Keep the box full: all 8 GPUs and ~cpu_target cores busy. Never exceed the budget. `gpu_map` lists every process
  on each GPU (a GPU may host two); a GPU counts as free only when nothing runs on it.
- A SAT symmetry class with unsat>0 is proved impossible (the planner stops it). For no-three-in-line, fewer violated
  lines in the current model and faster rounds mean closer to a solution; 149 points beats the record, 150 settles it.
- Spencer: bad_vectors is the number of sign vectors below the target discrepancy D (0 = success). Hadamard: best_log10
  must exceed the record; runs that sit exactly at the record value are not progressing.
- Give every launch/stop/keep a testable `prediction`: `metric` from that problem's metrics_allowed, `expected` value,
  `horizon_min` 10-30 (short horizons let the critic score you within the session). Be calibrated: look at which of your past predictions were refuted and adjust. Every metric
  is a running best that can never get worse, so a prediction that it merely stays at its current value is trivial
  and is not scored (outcome n/a): predict the improvement you actually expect, or give no prediction.
- `cite` = literature card ids that informed the decision; `memory_used` = memory fact ids you relied on. Only ids that
  appear in the input.
- At most 8 decisions per cycle. Prefer few, decisive moves over churn."""


def _schema(slugs):
    pred = {"type": "object", "properties": {"metric": {"type": "string"}, "expected": {"type": "number"},
                                             "horizon_min": {"type": "integer"}},
            "required": ["metric", "expected", "horizon_min"], "additionalProperties": False}
    dec = {"type": "object", "properties": {
        "problem": {"type": "string", "enum": slugs},
        "action": {"type": "string", "enum": ["launch", "stop", "keep", "research", "note", "sandbox", "commission"]},
        "where": {"type": ["string", "null"], "enum": ["box", "modal", None]},
        "goal": {"type": ["string", "null"]},
        "template": {"type": ["string", "null"]},
        "params_json": {"type": ["string", "null"]},
        "count": {"type": ["integer", "null"]},
        "strategy_ids": {"type": "array", "items": {"type": "string"}},
        "stop_filter_json": {"type": ["string", "null"]},
        "queries": {"type": "array", "items": {"type": "string"}},
        "n": {"type": ["integer", "null"]},
        "rationale": {"type": "string"},
        "prediction": {"anyOf": [pred, {"type": "null"}]},
        "cite": {"type": "array", "items": {"type": "integer"}},
        "memory_used": {"type": "array", "items": {"type": "string"}},
    }, "required": ["problem", "action", "where", "goal", "template", "params_json", "count", "strategy_ids",
                    "stop_filter_json", "queries", "n", "rationale", "prediction", "cite", "memory_used"],
       "additionalProperties": False}
    return {"type": "object", "properties": {"summary": {"type": "string"}, "decisions": {"type": "array", "items": dec}},
            "required": ["summary", "decisions"], "additionalProperties": False}


def _groups(procs, slug):
    """Strategy groups: identical template+params (seed aside) collapse into one row."""
    g = {}
    for p in procs:
        if p["problem"] != slug:
            continue
        key_params = {k: v for k, v in p["params"].items() if k != "seed"}
        key = (p["template"], json.dumps(key_params, sort_keys=True))
        row = g.setdefault(key, {"template": p["template"], "params": key_params, "count": 0, "adopted": 0, "ids": [],
                                 "metric": [], "improve_age_min": [], "gpus": []})
        row["count"] += 1
        row["adopted"] += int(bool(p.get("adopted")))
        row["ids"].append(p["id"])
        if p.get("metric_value") is not None:
            row["metric"].append(p["metric_value"])
        if p.get("improve_age_s") is not None:
            row["improve_age_min"].append(round(p["improve_age_s"] / 60, 1))
        if p.get("gpu") is not None:
            row["gpus"].append(p["gpu"])
    out = []
    for row in g.values():
        m, a = sorted(row["metric"]), sorted(row["improve_age_min"])
        out.append({"template": row["template"], "params": row["params"], "count": row["count"], "adopted": row["adopted"],
                    "ids": row["ids"] if row["count"] <= 4 else row["ids"][:3] + [f"... {row['count'] - 3} more"],
                    "metric_min": m[0] if m else None, "metric_median": m[len(m) // 2] if m else None,
                    "metric_max": m[-1] if m else None,
                    "improve_age_min_min": a[0] if a else None, "improve_age_min_median": a[len(a) // 2] if a else None,
                    "gpus": sorted(row["gpus"])})
    return out


def build_state(an, facts, cards, cycle):
    probs = []
    for slug, a in an["problems"].items():
        P = config.PROBLEMS[slug]
        if not P["active"] and not a["procs"]:
            continue
        best = ledger.get_best(slug)
        allowed = [a["metric"]] + [f"{a['metric']}@{k}" for k in sorted(a["sub"])] + sorted(a.get("extra") or {})
        entry = {"slug": slug, "title": P["title"], "scoring": P["scoring"], "record": P["record"], "holder": P["holder"],
                 "min_improvement": P["min_improvement"],
                 "our_best_verified": best["score"] if best and best.get("verified") else None,
                 "metric": {"name": a["metric"], "value": a["value"], "target": a["target"],
                            "lower_is_better": a["lower_is_better"], "by_target": a["sub"],
                            "secondary": a.get("extra") or {}},
                 "metrics_allowed": allowed, "status": a["status"], "best_age_min": a["best_age_min"] and round(a["best_age_min"], 1),
                 "rate_1h": a["rate_1h"], "ucb_priority": a["priority"], "procs": a["procs"], "gpus": a["gpus"],
                 "templates": {n: {"resource": t.get("resource", "cpu"), "params": strategies.public_params(t),
                                   **({"note": (t.get("note") or t.get("notes"))[:400]} if (t.get("note") or t.get("notes")) else {})}
                               for n, t in strategies.for_problem(slug).items()},
                 "strategy_groups": _groups(an["procs"], slug),
                 "memory": [{"id": f["id"], "agent": f["agent"], "text": f["text"][:300]} for f in facts.get(slug, [])],
                 "literature": [{"id": c["id"], "title": c["title"][:120], "highlight": c["highlight"][:300]} for c in cards.get(slug, [])]}
        try:
            from . import fleet
            mr = fleet.runs(slug)
            entry["modal_runs"] = [{"id": r["id"], "template": r["template"],
                                    "params": {k: v for k, v in (r["params"] or {}).items()},
                                    "metric_value": r["metric_value"]} for r in mr][:40]
            entry["modal_runs_total"] = len(mr)
        except Exception:  # noqa: BLE001
            entry["modal_runs"] = []
        if slug == "no-three-in-line-75":
            entry["sat_classes"] = [{k: c.get(k) for k in ("sym", "procs", "unsat", "found", "best_violated", "current_min",
                                                           "current_median", "rounds_median", "lines_median", "rounds_last_15min",
                                                           "no_round_yet")}
                                    | {"best_age_min": round((c.get("best_age_s") or 0) / 60, 1)}
                                    for c in sorted(an["classes"].values(), key=lambda c: c["sym"])]
        if slug in ("sidon-45-set",):
            from .planner import KNOWN_NEGATIVE
            entry["known"] = KNOWN_NEGATIVE.get(slug)
        probs.append(entry)
    recent = []
    for d in ledger.decisions(agent="proposer", limit=12):
        recent.append({"id": d["id"], "cycle": d["cycle"], "problem": d["problem"], "action": d["action"],
                       "params": d["params"], "prediction": d["prediction"], "outcome": d["outcome"],
                       "rationale": d["rationale"][:160]})
    rejected = [{"problem": d["problem"], "reason": d["rationale"][:200]} for d in ledger.decisions(agent="planner", limit=30)
                if d["action"] == "reject"][:6]
    b = an["budget"]
    gpu_map = {}
    for p in list(an["procs"]) + list(an.get("foreign") or []):
        if p.get("gpu") is not None:
            gpu_map.setdefault(str(p["gpu"]), []).append(f"{p['id']} ({p['problem']})")
    return {"cycle": cycle, "now": ledger.now(),
            "gpu_map": {k: gpu_map[k] for k in sorted(gpu_map, key=int)},
            "budget": {"free_gpus": b["free_gpus"], "free_cores": b["free_cores"], "cores_used": b["cores_used"],
                       "cpu_target": b["cpu_target"], "gpus_total": b["gpus_total"],
                       "gpu_stop_after_min": config.STALL_MIN_GPU_STOP, "max_cpu_stops": config.MAX_CPU_STOPS_PER_CYCLE,
                       "max_launches": config.MAX_LAUNCHES_PER_CYCLE, "modal": _modal_budget()},
            "problems": probs, "recent_decisions": recent, "recent_planner_rejections": rejected}


def _modal_budget():
    try:
        from . import fleet
        sm = fleet.summary()
        return {"running": sm["containers"], "free": fleet.free_slots(), "max": sm["max"], "cpu_only": True}
    except Exception as e:  # noqa: BLE001
        return {"running": 0, "free": 0, "error": str(e)[:120]}


def _client():
    if config.ROOT not in sys.path:
        sys.path.insert(0, config.ROOT)
    import envload
    envload.load()
    from openai import OpenAI
    return OpenAI(timeout=240)


def propose(state):
    """Returns (decisions, meta) where meta = {model, tokens, latency_ms, summary, error}."""
    slugs = sorted(config.PROBLEMS)
    schema = _schema(slugs)
    client = _client()
    last_err = None
    for model in (config.PROPOSER_MODEL, config.PROPOSER_FALLBACK):
        t0 = time.time()
        try:
            r = client.responses.create(model=model, instructions=SYSTEM, input=json.dumps(state, default=str),
                                        text={"format": {"type": "json_schema", "name": "lab_decisions", "schema": schema,
                                                         "strict": True}})
            out = json.loads(r.output_text)
            meta = {"model": model, "tokens": getattr(r.usage, "total_tokens", None) if r.usage else None,
                    "latency_ms": int((time.time() - t0) * 1000), "summary": out.get("summary", ""), "error": last_err}
            return normalize(out.get("decisions", []), state), meta
        except Exception as e:  # noqa: BLE001
            last_err = f"{model}: {type(e).__name__}: {str(e)[:300]}"
    raise RuntimeError(f"proposer failed on all models: {last_err}")


def normalize(decs, state):
    """Parse JSON-in-string fields and drop ids that were not in the input."""
    cite_ok = {c["id"] for p in state["problems"] for c in p["literature"]}
    mem_ok = {f["id"] for p in state["problems"] for f in p["memory"]}
    out = []
    for d in decs[:8]:
        d = dict(d)
        for k_in, k_out in (("params_json", "params"), ("stop_filter_json", "stop_filter")):
            raw = d.pop(k_in, None)
            try:
                v = json.loads(raw) if raw else {}
                d[k_out] = v if isinstance(v, dict) else {}
            except ValueError:
                d[k_out] = {}
        d["cite"] = [c for c in d.get("cite") or [] if c in cite_ok]
        d["memory_used"] = [m for m in d.get("memory_used") or [] if m in mem_ok]
        if d.get("prediction") and not isinstance(d["prediction"].get("expected"), (int, float)):
            d["prediction"] = None
        out.append(d)
    return out
