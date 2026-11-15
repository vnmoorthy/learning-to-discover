"""Deterministic layer under the LLM.

- analyze(): per-problem progress rate, staleness and a UCB-style priority (gap closed per compute-hour + exploration).
- provable_kills(): strategies that cannot succeed (SAT class proved UNSAT, target already reached).
- plan(): turns proposer output into validated, budget-respecting actions (stops first, then launches).
- refill(): any GPU or core left idle after that goes to the highest-priority problem / most promising SAT class.
- execute(): runs the actions on the box and records every step as a decision.
"""
import json
import math
import random
import re
import time

from . import box, config, events, ledger, monitor, strategies

ABBR = {"nothree_sat": "nt", "spencer_gpu": "sp", "hadamard_gpu": "hd", "sidon_extend": "si"}
KNOWN_NEGATIVE = {
    "sidon-45-set": "exact search proved there is no 1-point extension of the Ma-Tang 14-point set and no 2-point "
                    "extension with both points in [-3000, 4000] (runs/sidon_extend.log)",
}


# ---------------------------------------------------------------- analysis
def _history_rate(slug, metric, lower, minutes=60):
    """Metric improvement over the last `minutes` (positive = better), from stored telemetry."""
    h = ledger.metric_history(slug, metric, limit=400)
    if len(h) < 2:
        return 0.0
    now = time.time()
    old = None
    for t, v in h:
        ts = ledger.parse_iso(t) or now
        if ts >= now - minutes * 60:
            old = v if old is None else old
            break
        old = v
    cur = h[-1][1]
    if old is None:
        return 0.0
    return (old - cur) if lower else (cur - old)


def analyze():
    cur = monitor.current()
    metrics = cur.get("metrics") or {}
    classes = cur.get("classes") or {}
    procs = cur.get("procs") or []
    foreign = cur.get("foreign") or []
    bud = monitor.budget()
    total_procs = max(1, len(procs) + len(foreign))
    launched_counts = {r["problem"]: r["c"] for r in ledger.q("SELECT problem, COUNT(*) c FROM strategies GROUP BY problem")}
    n_total = sum(launched_counts.values()) or 1
    out = {}
    for slug, P in config.PROBLEMS.items():
        m = metrics.get(slug) or {}
        mine = [p for p in procs if p["problem"] == slug]
        gpus = len({p["gpu"] for p in mine if p.get("gpu") is not None})
        tpls = strategies.for_problem(slug)
        age_min = (m.get("best_age_s") or 0) / 60 if m.get("best_age_s") is not None else None
        best = ledger.get_best(slug)
        value = m.get("value")
        target = P["target"]
        gap = None
        if value is not None and target is not None:
            gap = (value - target) if P["lower_is_better"] else (target - value)
        rate = _history_rate(slug, m.get("name") or P["metric"], P["lower_is_better"])
        compute_h = max(0.05, (len(mine) or 0.5) * 1.0)    # process-hours per wall hour
        norm = abs(gap) if gap not in (None, 0) else 1.0
        gain_per_ch = (rate / norm) / compute_h if norm else 0.0
        explore = 0.15 * math.sqrt(math.log(1 + n_total) / (1 + launched_counts.get(slug, 0)))
        stale_pen = 0.1 * min(1.0, (age_min or 0) / 120)
        prio = round(gain_per_ch * 100 + explore - stale_pen + (0.3 if P["active"] else -1), 4)
        stalled = bool(mine) and age_min is not None and age_min >= config.STALL_MIN
        if best and best.get("beats_record"):
            st = "record"
        elif slug == "no-three-in-line-75" and classes and all(c["unsat"] for c in classes.values()):
            st = "proved-negative"
        elif not mine:
            st = "proved-negative" if slug in KNOWN_NEGATIVE else "idle"
        else:
            st = "stalled" if stalled else "searching"
        out[slug] = {"slug": slug, "metric": m.get("name") or P["metric"], "value": value, "target": target, "gap": gap,
                     "lower_is_better": P["lower_is_better"], "sub": m.get("sub") or {}, "best_age_min": age_min,
                     "stalled": stalled, "status": st, "procs": len(mine), "gpus": gpus,
                     "share": round(len(mine) / total_procs, 3), "rate_1h": rate, "priority": prio,
                     "templates": sorted(tpls), "resources": sorted({t.get("resource", "cpu") for t in tpls.values()}),
                     "unsat_classes": m.get("unsat_classes") or [], "extra": m.get("extra") or {}}
    return {"problems": out, "classes": classes, "budget": bud, "procs": procs, "foreign": foreign}


def class_rank(classes):
    """SAT classes ordered most-promising first (not UNSAT, fewest violated lines, most recent improvement)."""
    ok = [c for c in classes.values() if not c["unsat"] and c["best_violated"] is not None]
    return sorted(ok, key=lambda c: (c["best_violated"], c.get("best_age_s") or 1e9))


# ---------------------------------------------------------------- ids / seeds
def used_seeds(template):
    seeds = set()
    for s in ledger.strategies():
        if s["template"] == template and isinstance(s["params"].get("seed"), int):
            seeds.add(s["params"]["seed"])
    snap = monitor.current().get("snap") or {}
    fam = (strategies.get(template).get("out") or "").replace("runs/", "")
    for path, li in (snap.get("logs") or {}).items():
        if li.get("family") == fam and isinstance(li.get("seed"), int):
            seeds.add(li["seed"])
        m = re.search(r"_s(\d+)\.log$", path)
        if m and f"/runs/{fam}/" in path:
            seeds.add(int(m.group(1)))
    return seeds


def fresh_seed(template, taken):
    s = config.LAUNCH_SEED_BASE
    used = used_seeds(template) | taken
    while s in used:
        s += 1
    taken.add(s)
    return s


def make_id(template, params, test=False):
    ab = ABBR.get(template, template)
    bits = []
    if "sym" in params:
        bits.append(str(params["sym"]))
    if "n" in params and "D" in params:
        bits.append(f"n{params['n']}D{params['D']}")
    if "perturb" in params:
        bits.append(f"p{params['perturb']}")
    if "seed" in params:
        bits.append(f"s{params['seed']}")
    sid = ("test-" if test else "") + "-".join([ab] + bits)
    sid = re.sub(r"[^A-Za-z0-9_.-]", "", sid)[:70]
    base, k = sid, 2
    while ledger.get_strategy(sid):
        sid = f"{base}-{k}"; k += 1
    return sid


# ---------------------------------------------------------------- provable kills
def provable_kills(an):
    """[(strategy, rationale)] for strategies that provably cannot improve our result."""
    kills = []
    procs = an["procs"]
    for sym, c in an["classes"].items():
        if c["unsat"]:
            victims = [p for p in procs if p["template"] == "nothree_sat" and p["params"].get("sym") == sym]
            for p in victims:
                kills.append((p, f"Symmetry class {sym} was proved UNSAT by another seed (the lazy-line encoding is a "
                                 f"relaxation, so UNSAT is a proof): no configuration of this size exists in {sym}; "
                                 f"this run cannot succeed."))
    best = ledger.get_best("no-three-in-line-75")
    if best and best.get("verified") and best.get("score"):
        sc = int(best["score"])
        for p in procs:
            if p["template"] != "nothree_sat":
                continue
            m = re.search(r"-(\d+)$", str(p["params"].get("sym", "")))
            if m and int(m.group(1)) <= sc:
                kills.append((p, f"We already hold a verified {sc}-point configuration; a {m.group(1)}-point class cannot "
                                 f"improve on it."))
    # no progress for N cycles (conservative, capped): CPU runs that never produced a first result, GPU runs that
    # have not improved for DEAD_GPU_STALL_MIN minutes. Their capacity goes back to refill.
    dead = []
    for p in procs:
        et_min = (p.get("etime_s") or 0) / 60
        if p["resource"] == "cpu" and p.get("metric_value") is None and et_min >= config.DEAD_NO_RESULT_MIN:
            dead.append((p, f"No progress: {p['id']} has produced no result in {et_min:.0f} min "
                            f"(limit {config.DEAD_NO_RESULT_MIN} min); its core goes to the most promising target."))
        elif p["resource"] == "gpu" and (p.get("improve_age_s") or 0) / 60 >= config.DEAD_GPU_STALL_MIN:
            dead.append((p, f"No progress: {p['id']} has not improved its best ({p.get('metric_value')}) for "
                            f"{(p.get('improve_age_s') or 0) / 60:.0f} min (limit {config.DEAD_GPU_STALL_MIN} min); "
                            f"the GPU is refilled with a different configuration."))
    dead.sort(key=lambda z: -((z[0].get("improve_age_s") or 0) + (z[0].get("etime_s") or 0)))
    kills += dead[:config.MAX_DEAD_KILLS_PER_CYCLE]
    seen, out = set(), []
    for p, r in kills:
        if p["id"] not in seen:
            seen.add(p["id"]); out.append((p, r))
    return out


# ---------------------------------------------------------------- planning
def _gpu_default_params(slug, rng, an):
    if slug == "spencer-discrepancy":
        # choose the (n, D) target with the fewest bad vectors relative to its size
        sub = an["problems"][slug]["sub"]
        n, D = 20, 8
        if sub:
            best = min(sub.items(), key=lambda kv: kv[1] / 2 ** (int(re.match(r"n(\d+)", kv[0]).group(1)) - 1))
            mm = re.match(r"n(\d+)D(\d+)", best[0])
            n, D = int(mm.group(1)), int(mm.group(2))
        return {"n": n, "D": D, "init": rng.choice(["random", "paley"]) if n == 20 else "random",
                "tenure": rng.choice([15, 25, 40, 60]), "restart": rng.choice([5000, 20000, 50000])}
    if slug == "hadamard-det-51":
        return {"chains": 512, "perturb": rng.choice([20, 40, 80, 160, 240]), "tenure": rng.choice([40, 80, 150]),
                "restart": rng.choice([2000, 4000, 8000])}
    return {}


def _cpu_default(an, rng):
    """(template, params, why) for one more CPU process on the most promising target."""
    ranked = class_rank(an["classes"])
    if ranked and "nothree_sat" in strategies.templates():
        c = ranked[0]
        return "nothree_sat", {"sym": c["sym"], "solver": "cadical195", "presolve-slopes": rng.choice([2, 3])}, \
            (f"most promising SAT class {c['sym']} (best model {c['best_violated']} violated lines, "
             f"{c['procs']} runs alive)")
    # otherwise the highest-priority problem that has a CPU template
    cands = [(a["priority"], s) for s, a in an["problems"].items()
             if "cpu" in a["resources"] and a["status"] not in ("record",) and s not in KNOWN_NEGATIVE]
    for _, slug in sorted(cands, reverse=True):
        for name, t in strategies.for_problem(slug).items():
            if t.get("resource", "cpu") == "cpu" and name != "sidon_extend":
                return name, {}, f"highest-priority CPU problem {slug}"
    return None, None, None


def _problem_for_gpu(an):
    cands = [(a["priority"], s) for s, a in an["problems"].items() if "gpu" in a["resources"] and a["status"] != "record"]
    return [s for _, s in sorted(cands, reverse=True)]


def plan(proposals, an, cycle, test=False):
    """Validate proposer decisions against the schema and the budget.
    Returns (actions, rejections). actions: dicts with kind in stop|launch|research|sandbox|keep|note."""
    rng = random.Random(cycle * 7919 + 17)
    bud = an["budget"]
    free_gpus = list(bud["free_gpus"])
    free_cores = bud["cpu_target"] - bud["cores_used"]     # may be negative when over target
    procs = {p["id"]: p for p in an["procs"]}
    actions, rejections, taken_seeds, stopping = [], [], {}, set()
    cpu_stops = gpu_stops = launches = 0

    # 1) provable kills first (never the LLM's call)
    def frees(p):   # in test mode only test- strategies are really stopped (the rest is a logged dry run)
        return not test or str(p["id"]).startswith("test-")

    owners = {}     # gpu -> ids still running there; a GPU becomes free only when its last owner stops
    for q in list(an["procs"]) + list(an.get("foreign") or []):
        if q.get("gpu") is not None:
            owners.setdefault(int(q["gpu"]), set()).add(q["id"])

    def release_gpu(p):
        g = p.get("gpu")
        if g is None:
            return
        owners.get(int(g), set()).discard(p["id"])
        if not owners.get(int(g)) and int(g) not in free_gpus:
            free_gpus.append(int(g))

    grouped = {}
    for p, why in provable_kills(an):
        if p["id"] in stopping:
            continue
        stopping.add(p["id"])
        key = (p["problem"], why if not why.startswith("No progress") else why.split(":")[0] + p["resource"])
        g = grouped.get(key)
        if g is None:
            g = grouped[key] = {"kind": "stop", "agent": "planner", "problem": p["problem"], "recs": [], "rationale": why,
                                "deterministic": True}
            actions.append(g)
        elif why.startswith("No progress"):
            g["rationale"] = (f"No progress: {len(g['recs']) + 1} {p['resource'].upper()} runs exceeded the no-progress limit "
                              f"({config.DEAD_NO_RESULT_MIN} min without a first result for CPU, {config.DEAD_GPU_STALL_MIN} "
                              f"min without improvement for GPU); their capacity goes back to refill.")
        g["recs"].append(p)
        if frees(p):
            if p["resource"] == "gpu":
                release_gpu(p)
            free_cores += 1

    # 2a) Modal fleet stops (cancel FunctionCalls; they never touch the box budget)
    from . import fleet
    for d in proposals:
        if d["action"] != "stop":
            continue
        mids = [i for i in (d.get("strategy_ids") or []) if str(i).startswith("modal-")]
        if d.get("where") == "modal" and d.get("stop_filter"):
            filt = d["stop_filter"]; tpl = d.get("template")
            cand = [r for r in fleet.runs(d["problem"]) if (not tpl or r["template"] == tpl)
                    and all(str(r["params"].get(k)) == str(v) for k, v in filt.items())]
            mids += [r["id"] for r in cand[:max(1, int(d.get("count") or 1))]]
        mids = [i for i in dict.fromkeys(mids) if i not in stopping]
        if mids:
            stopping.update(mids)
            actions.append({"kind": "modal_stop", "agent": "proposer", "problem": d["problem"], "ids": mids,
                            "rationale": d.get("rationale", ""), "decision": d})
            d = dict(d); d["strategy_ids"] = [i for i in (d.get("strategy_ids") or []) if not str(i).startswith("modal-")]

    # 2) proposer stops
    for d in proposals:
        if d["action"] != "stop" or d.get("where") == "modal":
            continue
        ids = [i for i in (d.get("strategy_ids") or []) if not str(i).startswith("modal-")]
        if d.get("strategy_id"):
            ids.append(d["strategy_id"])
        filt = d.get("stop_filter") or {}
        if filt:
            tpl = d.get("template")
            cand = [p for p in an["procs"] if (not tpl or p["template"] == tpl) and p["problem"] == d["problem"]
                    and all(str(p["params"].get(k)) == str(v) for k, v in filt.items()) and p["id"] not in stopping]
            lib = an["problems"][d["problem"]]["lower_is_better"]
            # worst runs first; a run that has not reported a metric yet counts as the worst
            cand.sort(key=lambda p: (p.get("metric_value") is not None,
                                     -(p.get("metric_value") or 0) if lib else (p.get("metric_value") or 0)))
            ids += [p["id"] for p in cand[:max(1, int(d.get("count") or 1))]]
        recs, why_not = [], []
        for sid in dict.fromkeys(ids):
            p = procs.get(sid)
            if not p:
                why_not.append(f"{sid}: not a running strategy"); continue
            if sid in stopping:
                continue
            if p["resource"] == "gpu":
                age = (p.get("improve_age_s") or 0) / 60
                if age < config.STALL_MIN_GPU_STOP:
                    why_not.append(f"{sid}: GPU run improved {age:.0f} min ago (< {config.STALL_MIN_GPU_STOP} min stall rule)"); continue
                if gpu_stops >= config.MAX_GPU_STOPS_PER_CYCLE:
                    why_not.append(f"{sid}: GPU stop cap {config.MAX_GPU_STOPS_PER_CYCLE}/cycle"); continue
                gpu_stops += 1
                if frees(p):
                    release_gpu(p)
            else:
                if cpu_stops >= config.MAX_CPU_STOPS_PER_CYCLE:
                    why_not.append(f"{sid}: CPU stop cap {config.MAX_CPU_STOPS_PER_CYCLE}/cycle"); continue
                cpu_stops += 1
            if frees(p):
                free_cores += 1
            stopping.add(sid)
            recs.append(p)
        if recs:
            actions.append({"kind": "stop", "agent": "proposer", "problem": d["problem"], "recs": recs,
                            "rationale": d.get("rationale", ""), "decision": d})
        if why_not:
            rejections.append({"decision": d, "reason": "; ".join(why_not[:8]) + (f" (+{len(why_not) - 8} more)" if len(why_not) > 8 else "")})

    # 3a) proposer launches on the Modal fleet (CPU templates; capacity = free Modal slots, not box cores)
    modal_free = fleet.free_slots()
    for d in proposals:
        if d["action"] != "launch" or d.get("where") != "modal":
            continue
        tpl = d.get("template")
        try:
            t = strategies.get(tpl)
        except ValueError as e:
            rejections.append({"decision": d, "reason": str(e)}); continue
        if t.get("problem") != d["problem"]:
            rejections.append({"decision": d, "reason": f"template {tpl} is for {t.get('problem')}, not {d['problem']}"}); continue
        if t.get("resource") == "gpu":
            rejections.append({"decision": d, "reason": "Modal fleet is CPU-only on this account; GPU templates run on the box"}); continue
        count = max(1, min(int(d.get("count") or 1), 64))
        items, why_not = [], []
        for k in range(count):
            if modal_free <= 0:
                why_not.append(f"Modal fleet full ({fleet.MODAL_MAX} containers)"); break
            params = dict(d.get("params") or {})
            ts = taken_seeds.setdefault(tpl, set())
            if "seed" in (t.get("params") or {}):
                if not isinstance(params.get("seed"), int) or params["seed"] in used_seeds(tpl) | ts or k > 0:
                    params["seed"] = fresh_seed(tpl, ts)
                else:
                    ts.add(params["seed"])
            try:
                params = strategies.validate(tpl, params)
            except ValueError as e:
                why_not.append(str(e)); break
            modal_free -= 1
            items.append({"template": tpl, "params": params, "gpu": None, "where": "modal",
                          "id": "modal-" + make_id(tpl, params, test)})
        if items:
            actions.append({"kind": "modal_launch", "agent": "proposer", "problem": d["problem"], "items": items,
                            "rationale": d.get("rationale", ""), "decision": d})
        if why_not:
            rejections.append({"decision": d, "reason": f"launched {len(items)}/{count} on Modal: " + "; ".join(dict.fromkeys(why_not))})

    # 3) proposer launches (within what is free after the stops)
    for d in proposals:
        if d["action"] != "launch" or d.get("where") == "modal":
            continue
        tpl = d.get("template")
        try:
            t = strategies.get(tpl)
        except ValueError as e:
            rejections.append({"decision": d, "reason": str(e)}); continue
        if t.get("problem") != d["problem"]:
            rejections.append({"decision": d, "reason": f"template {tpl} is for {t.get('problem')}, not {d['problem']}"}); continue
        count = max(1, min(int(d.get("count") or 1), 64))
        items, why_not = [], []
        for k in range(count):
            if launches >= config.MAX_LAUNCHES_PER_CYCLE:
                why_not.append(f"launch cap {config.MAX_LAUNCHES_PER_CYCLE}/cycle"); break
            params = dict(d.get("params") or {})
            ts = taken_seeds.setdefault(tpl, set())
            if "seed" in (t.get("params") or {}):
                if not isinstance(params.get("seed"), int) or params["seed"] in used_seeds(tpl) | ts or k > 0:
                    params["seed"] = fresh_seed(tpl, ts)
                else:
                    ts.add(params["seed"])
            try:
                params = strategies.validate(tpl, params)
            except ValueError as e:
                why_not.append(str(e)); break
            gpu = None
            if t.get("resource") == "gpu":
                if not free_gpus:
                    why_not.append("no free GPU"); break
                gpu = free_gpus.pop(0)
            if free_cores <= 0 and gpu is None:      # a free GPU is always worth its one driver core
                why_not.append(f"no free CPU core (target {config.CPU_TARGET} busy)"); break
            free_cores -= 1
            launches += 1
            items.append({"template": tpl, "params": params, "gpu": gpu, "id": make_id(tpl, params, test)})
        if items:
            actions.append({"kind": "launch", "agent": "proposer", "problem": d["problem"], "items": items,
                            "rationale": d.get("rationale", ""), "decision": d})
        if why_not:
            rejections.append({"decision": d, "reason": f"launched {len(items)}/{count}: " + "; ".join(dict.fromkeys(why_not))})

    # 4) research / sandbox / keep / note pass through
    for d in proposals:
        if d["action"] == "commission":
            actions.append({"kind": "commission", "agent": "proposer", "problem": d["problem"], "rationale": d.get("rationale", ""),
                            "goal": (d.get("goal") or d.get("rationale") or "")[:1500], "decision": d})
            continue
        if d["action"] in ("research", "sandbox", "keep", "note"):
            a = {"kind": d["action"], "agent": "proposer", "problem": d["problem"], "rationale": d.get("rationale", ""),
                 "decision": d}
            if d["action"] == "research":
                a["queries"] = [q for q in (d.get("queries") or []) if q][:3]
            if d["action"] == "sandbox":
                a["n"] = max(1, min(int(d.get("n") or 4), 16))
            actions.append(a)

    # 5) refill whatever is still idle (keep all 8 GPUs and ~CPU_TARGET cores busy)
    actions += refill(an, free_gpus, free_cores, rng, taken_seeds, test, launches)
    return actions, rejections


def refill(an, free_gpus, free_cores, rng, taken_seeds, test=False, launches=0):
    acts = []
    order = _problem_for_gpu(an)
    for g in list(free_gpus):      # an idle GPU is always refilled (its driver process needs one core)
        if not order or launches >= config.MAX_LAUNCHES_PER_CYCLE:
            break
        slug = order[0]
        tpl = next((n for n, t in strategies.for_problem(slug).items() if t.get("resource") == "gpu"), None)
        if not tpl:
            order = order[1:]
            continue
        params = _gpu_default_params(slug, rng, an)
        params["seed"] = fresh_seed(tpl, taken_seeds.setdefault(tpl, set()))
        try:
            params = strategies.validate(tpl, params)
        except ValueError:
            continue
        a = an["problems"][slug]
        acts.append({"kind": "launch", "agent": "planner", "problem": slug,
                     "items": [{"template": tpl, "params": params, "gpu": g, "id": make_id(tpl, params, test)}],
                     "rationale": f"Refill: GPU {g} is idle. {slug} has the highest UCB priority among GPU problems "
                                  f"({a['priority']}; metric {a['metric']}={a['value']}, best {a['best_age_min'] and round(a['best_age_min'])} min old), "
                                  f"so it gets a fresh {tpl} run with varied params {json.dumps({k: v for k, v in params.items() if k != 'seed'})}."})
        free_gpus.remove(g)
        free_cores -= 1
        launches += 1
        order = order[1:] + order[:1]   # alternate GPU problems when several GPUs are idle
    if free_cores >= 2 and launches < config.MAX_LAUNCHES_PER_CYCLE:
        n = min(free_cores, config.MAX_LAUNCHES_PER_CYCLE - launches)
        tpl, base, why = _cpu_default(an, rng)
        if tpl and n > 0:
            items = []
            for _ in range(n):
                params = dict(base)
                if "seed" in (strategies.get(tpl).get("params") or {}):
                    params["seed"] = fresh_seed(tpl, taken_seeds.setdefault(tpl, set()))
                params["presolve-slopes"] = rng.choice([2, 3]) if tpl == "nothree_sat" else params.get("presolve-slopes")
                params = {k: v for k, v in params.items() if v is not None}
                try:
                    params = strategies.validate(tpl, params)
                except ValueError:
                    break
                items.append({"template": tpl, "params": params, "gpu": None, "id": make_id(tpl, params, test)})
            if items:
                slug = strategies.get(tpl)["problem"]
                acts.append({"kind": "launch", "agent": "planner", "problem": slug, "items": items,
                             "rationale": f"Refill: {free_cores} cores idle below the {config.CPU_TARGET}-core target; "
                                          f"moving them to the {why}."})
    return acts


# ---------------------------------------------------------------- execution
def execute(actions, cycle, proposer_ids=None):
    """Run actions on the box. Returns list of {action, ok, decision_id, ...}."""
    from . import literature, memory
    results = []
    proposer_ids = proposer_ids or {}
    for a in actions:
        src = proposer_ids.get(id(a.get("decision"))) if a.get("decision") is not None else None
        if a["kind"] == "stop":
            res = box.stop_many(a["recs"])
            okids = [sid for sid, r in res.items() if r["ok"]]
            for p in a["recs"]:
                r = res.get(p["id"], {})
                if r.get("ok"):
                    ledger.upsert_strategy({"id": p["id"], "status": "stopped", "stopped_at": ledger.now(),
                                            "stop_reason": a["rationale"][:300]})
            errs = {sid: r["error"] for sid, r in res.items() if not r["ok"]}
            did = ledger.add_decision(
                cycle, a["agent"] if a["agent"] == "planner" else "executor", "stop", a["problem"],
                {"strategy_ids": okids, "failed": errs, "proposer_decision": src,
                 "templates": sorted({p["template"] for p in a["recs"]}),
                 "params": [{k: v for k, v in p["params"].items()} for p in a["recs"]][:6]},
                (a["rationale"] if a["agent"] == "planner" else f"Executed proposer decision #{src}: ") +
                (f" Stopped {len(okids)}/{len(a['recs'])}." if a["agent"] == "planner" else
                 f"stopped {len(okids)}/{len(a['recs'])} strategies ({', '.join(okids[:6])}{'...' if len(okids) > 6 else ''})."))
            events.publish("decision", ledger.get_decision(did))
            if a["agent"] == "planner" and okids:
                fid = memory.write("planner", a["problem"], f"Stopped {len(okids)} runs ({', '.join(okids[:4])}...): {a['rationale']}",
                                   ["kill"])
                ledger.update_decision(did, memory_writes=[fid])
            results.append({"src": src, "kind": "stop", "ok": bool(okids), "ids": okids, "errors": errs, "decision_id": did})
        elif a["kind"] == "launch":
            res = box.launch_many(a["items"])
            okids = []
            for it in a["items"]:
                r = res.get(it["id"], {})
                if r.get("ok"):
                    okids.append(it["id"])
                    t = strategies.get(it["template"])
                    ledger.upsert_strategy({"id": it["id"], "problem": a["problem"], "template": it["template"],
                                            "params": r["params"], "resource": t.get("resource", "cpu"), "gpu": it["gpu"],
                                            "pid": r["pid"], "started_at": ledger.now(), "status": "running", "adopted": 0,
                                            "log": f"/home/ubuntu/ltd/{r['log']}", "decision_id": src,
                                            "test": int(it["id"].startswith("test-"))})
            errs = {it["id"]: res.get(it["id"], {}).get("error") for it in a["items"] if not res.get(it["id"], {}).get("ok")}
            summary = ", ".join(f"{it['id']}{'@gpu' + str(it['gpu']) if it['gpu'] is not None else ''}" for it in a["items"][:6])
            did = ledger.add_decision(
                cycle, "planner" if a["agent"] == "planner" else "executor", "launch", a["problem"],
                {"template": a["items"][0]["template"], "count": len(a["items"]), "strategy_ids": okids, "failed": errs,
                 "params": a["items"][0]["params"], "gpus": [it["gpu"] for it in a["items"] if it["gpu"] is not None],
                 "proposer_decision": src},
                (a["rationale"] + f" Launched {len(okids)}/{len(a['items'])}: {summary}{'...' if len(a['items']) > 6 else ''}.")
                if a["agent"] == "planner" else
                f"Executed proposer decision #{src}: launched {len(okids)}/{len(a['items'])} ({summary}{'...' if len(a['items']) > 6 else ''}).")
            events.publish("decision", ledger.get_decision(did))
            results.append({"src": src, "kind": "launch", "ok": bool(okids), "ids": okids, "errors": errs, "decision_id": did})
        elif a["kind"] == "modal_launch":
            from . import fleet
            res = fleet.launch(a["items"])
            okids = []
            for it in a["items"]:
                r = res.get(it["id"], {})
                if r.get("ok"):
                    okids.append(it["id"])
                    ledger.upsert_strategy({"id": it["id"], "problem": a["problem"], "template": it["template"],
                                            "params": it["params"], "resource": "modal", "gpu": None, "pid": None,
                                            "started_at": ledger.now(), "status": "running", "adopted": 0,
                                            "cmdline": f"modal call {r['call_id']}", "log": r["log"], "decision_id": src,
                                            "test": int("test-" in it["id"])})
            errs = {it["id"]: res.get(it["id"], {}).get("error") for it in a["items"] if not res.get(it["id"], {}).get("ok")}
            did = ledger.add_decision(
                cycle, "executor", "modal_launch", a["problem"],
                {"template": a["items"][0]["template"], "count": len(a["items"]), "strategy_ids": okids, "failed": errs,
                 "params": a["items"][0]["params"], "where": "modal", "proposer_decision": src},
                f"Executed proposer decision #{src}: started {len(okids)}/{len(a['items'])} Modal containers "
                f"({a['items'][0]['template']}).")
            events.publish("decision", ledger.get_decision(did))
            results.append({"src": src, "kind": "modal_launch", "ok": bool(okids), "ids": okids, "errors": errs, "decision_id": did})
        elif a["kind"] == "modal_stop":
            from . import fleet
            res = fleet.stop(a["ids"])
            okids = [i for i, r in res.items() if r.get("ok")]
            errs = {i: r.get("error") for i, r in res.items() if not r.get("ok")}
            did = ledger.add_decision(cycle, "executor", "modal_stop", a["problem"],
                                      {"strategy_ids": okids, "failed": errs, "where": "modal", "proposer_decision": src},
                                      f"Executed proposer decision #{src}: cancelled {len(okids)}/{len(a['ids'])} Modal containers.")
            events.publish("decision", ledger.get_decision(did))
            results.append({"src": src, "kind": "modal_stop", "ok": bool(okids), "ids": okids, "errors": errs, "decision_id": did})
        elif a["kind"] == "commission":
            try:
                from . import toolsmith
                rec = toolsmith.request(a["problem"], a["goal"])
                ok, err, url = True, None, rec.get("url")
            except Exception as e:  # noqa: BLE001
                ok, err, url = False, f"{type(e).__name__}: {str(e)[:200]}", None
            did = ledger.add_decision(cycle, "toolsmith", "commission", a["problem"],
                                      {"goal": a["goal"][:400], "devin_session": url, "proposer_decision": src, "error": err},
                                      (f"Commissioned a new search strategy from Devin for {a['problem']}: {a['goal'][:300]}"
                                       if ok else f"Could not open a Devin session: {err}"))
            events.publish("decision", ledger.get_decision(did))
            results.append({"src": src, "kind": "commission", "ok": ok, "error": err, "decision_id": did})
        elif a["kind"] == "research":
            ids, n = [], 0
            for qtext in a.get("queries") or []:
                try:
                    cards, cached, lat = literature.search(a["problem"], qtext)
                    ids += [c["id"] for c in cards]; n += 1
                except Exception as e:  # noqa: BLE001
                    events.log(f"exa search failed: {e}", "warn")
            did = ledger.add_decision(cycle, "literature", "search", a["problem"], {"queries": a.get("queries"), "proposer_decision": src},
                                      f"Exa search requested by proposer decision #{src}: {n} queries, {len(set(ids))} sources stored "
                                      f"for the next cycle.", sources=sorted(set(ids)), link_sources=False)
            events.publish("decision", ledger.get_decision(did))
            results.append({"src": src, "kind": "research", "ok": n > 0, "decision_id": did, "sources": ids})
        elif a["kind"] == "keep":
            results.append({"src": src, "kind": "keep", "ok": True, "decision_id": src})
        elif a["kind"] == "note" and a.get("rationale"):
            fid = memory.write("proposer", a["problem"], f"Note: {a['rationale'][:600]}", ["note"])
            if src:
                ledger.update_decision(src, memory_writes=[fid])
            results.append({"src": src, "kind": "note", "ok": True, "decision_id": src, "fact": fid})
        elif a["kind"] == "sandbox":
            try:
                from . import sandboxes  # owned by another builder
                sandboxes.start_batch_async(a["problem"], a["n"], context=a.get("rationale", ""))
                ok, err = True, None
            except Exception as e:  # noqa: BLE001
                ok, err = False, f"phoenixastar.sandboxes unavailable or failed: {type(e).__name__}: {e}"
            did = ledger.add_decision(cycle, "sandbox", "start_batch", a["problem"], {"n": a["n"], "proposer_decision": src, "error": err},
                                      f"{'Started' if ok else 'Could not start'} {a['n']} Modal sandbox programs for {a['problem']}"
                                      f"{'' if ok else ': ' + err}.")
            events.publish("decision", ledger.get_decision(did))
            results.append({"src": src, "kind": "sandbox", "ok": ok, "error": err, "decision_id": did})
    return results
